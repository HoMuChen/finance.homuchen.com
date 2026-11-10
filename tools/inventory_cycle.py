"""台灣電子業庫存循環：存貨周轉天數年增（見頂檢查清單第 5 項的台灣版旁證）。

用法：
    uv run -q --with duckdb python tools/inventory_cycle.py                                  # 輸出到終端
    uv run -q --with duckdb python tools/inventory_cycle.py --out reports/inventory-2026-11-10.md
    uv run -q --with duckdb python tools/inventory_cycle.py --threshold 8                    # 改門檻看敏感度

每季財報截止日（5/16、8/15、11/15、次年 4/1）之後跑一次。

計算（2026-11-10 定）：
- 存貨周轉天數 = 平均存貨（期初＋期末）÷ 單季營業成本 × 91。用營業成本、不用營收，
  因為毛利率變動（例如記憶體漲價壓縮組裝廠毛利）會讓「存貨年增 − 營收年增」高估囤貨。
- 組別合計只加總當季與去年同季都有資料的公司，再和去年同季比，消掉 Q4 旺季的季節性。
- 時間點用 `avail_date`（法定截止日），沒有前視。大公司法說較早，實際上可以更早知道。
- 組別：非半導體電子業（組裝、零組件、通路、光電、網通）、半導體 ex-台積電、台積電（對照）。
- 某季公司數不到前 4 季最多的 90%，標「未到齊」，不算燈號。

訊號：半導體 ex-台積電天數年增 > +6 天。門檻是看過 2014–2026 的資料後訂的（事後），
樣本只有 2015、2022 兩次提前與 2019 一次落後誤報，只能看方向。
"""

import argparse
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from r2 import connect  # noqa: E402

ELEC = ("半導體業", "電子零組件業", "光電業", "電腦及週邊設備業", "通信網路業",
        "其他電子業", "電子通路業", "電子工業", "其他電子類")
GROUPS = {"semi_ex": "半導體 ex-台積電", "other_elec": "非半導體電子業", "tsmc": "台積電（對照）"}
SIGNAL_GROUP = "semi_ex"
THRESHOLD = 6.0
COMPLETE = 0.9
SINCE = "2014-03-31"
MEMORY_MODULE = {"8299": "群聯", "3260": "威剛", "2451": "創見", "4967": "十銓", "8271": "宇瞻"}
WATCH = {"2454": "聯發科", "3661": "世芯-KY", **MEMORY_MODULE, "2376": "技嘉", "2357": "華碩", "2330": "台積電"}

BASE = f"""
WITH u AS (SELECT stock_id, name, industry FROM tw.universe WHERE industry IN ({",".join(f"'{i}'" for i in ELEC)})),
inv AS (SELECT stock_id, date, value inv, avail_date FROM tw.bs WHERE type = 'Inventories' AND value IS NOT NULL),
c AS (SELECT stock_id, date, value cogs FROM tw.fin WHERE type = 'CostOfGoodsSold' AND value > 0),
x AS (
  SELECT u.stock_id, u.name,
         CASE WHEN u.stock_id = '2330' THEN 'tsmc' WHEN u.industry = '半導體業' THEN 'semi_ex' ELSE 'other_elec' END grp,
         i.date, i.avail_date, (i.inv + p.inv) / 2 ai, c.cogs
  FROM u JOIN inv i USING (stock_id)
  JOIN inv p ON p.stock_id = i.stock_id AND p.date = last_day(i.date - INTERVAL 3 MONTH)
  JOIN c ON c.stock_id = i.stock_id AND c.date = i.date),
pair AS (
  SELECT a.*, b.ai ai_1y, b.cogs cogs_1y
  FROM x a JOIN x b ON a.stock_id = b.stock_id AND b.date = last_day(a.date - INTERVAL 12 MONTH))
"""


# ---------- 資料 ----------

def load_groups(con):
    rows = con.execute(BASE + f"""
        SELECT grp, date, max(avail_date), count(*),
               sum(ai) / sum(cogs) * 91, sum(ai_1y) / sum(cogs_1y) * 91
        FROM pair WHERE date >= DATE '{SINCE}' GROUP BY 1, 2 ORDER BY 1, 2""").fetchall()
    out = {g: [] for g in GROUPS}
    for g, d, avail, n, dio, dio1 in rows:
        out[g].append({"date": d, "avail": avail, "n": n, "dio": dio, "dio_1y": dio1, "d": dio - dio1})
    for g, qs in out.items():
        for i, q in enumerate(qs):
            prev = [p["n"] for p in qs[max(0, i - 4):i]]
            q["complete"] = not prev or q["n"] >= COMPLETE * max(prev)
    return out


def load_taiex(con):
    return dict(con.execute("SELECT date, close FROM tw.market.taiex ORDER BY date").fetchall())


def load_watch(con, quarters):
    ids = ",".join(f"'{s}'" for s in WATCH)
    ds = ",".join(f"DATE '{d}'" for d in quarters)
    rows = con.execute(BASE + f"SELECT stock_id, date, ai / cogs * 91 FROM x "
                              f"WHERE stock_id IN ({ids}) AND date IN ({ds})").fetchall()
    return {(s, d): v for s, d, v in rows}


def load_contrib(con, date, n=10):
    return con.execute(BASE + f"""
        SELECT stock_id, name, ai_1y / cogs_1y * 91, ai / cogs * 91, cogs / cogs_1y - 1
        FROM pair WHERE grp = '{SIGNAL_GROUP}' AND date = DATE '{date}'
        ORDER BY ai - ai_1y DESC LIMIT {n}""").fetchall()


# ---------- 計算 ----------

def forward(taiex, day, horizon=250):
    ds = sorted(taiex)
    idx = next((i for i, d in enumerate(ds) if d >= day), None)
    if idx is None:
        return None
    p0, path = taiex[ds[idx]], [taiex[d] for d in ds[idx:idx + horizon + 1]]
    full = len(path) > horizon
    return {"day": ds[idx], "level": p0,
            "r6": path[125] / p0 - 1 if len(path) > 125 else None,
            "r12": path[-1] / p0 - 1 if full else None,
            "mdd": min(path) / p0 - 1, "full": full}


def events(qs, thr):
    """訊號開始的季度：天數年增 > thr、資料到齊，且上一季沒有亮。"""
    out, prev = [], False
    for q in qs:
        on = q["complete"] and q["d"] > thr
        if on and not prev:
            out.append(q)
        if q["complete"]:
            prev = on
    return out


# ---------- 輸出 ----------

def sgn(x, nd=1):
    return f"{x:+.{nd}f}"


def pct(x):
    return "—" if x is None else f"{x * 100:+.1f}%"


def qlabel(d):
    return f"{d.year}Q{(d.month - 1) // 3 + 1}"


def build(thr):
    con = connect()
    g = load_groups(con)
    taiex = load_taiex(con)
    sig = g[SIGNAL_GROUP]
    done = [q for q in sig if q["complete"]]
    last = done[-1]
    streak = 0
    for q in reversed(done):
        if q["d"] <= thr:
            break
        streak += 1
    pending = [q for q in sig if not q["complete"] and q["date"] > last["date"]]

    L = [f"# 台灣電子業庫存循環（資料至 {qlabel(sig[-1]['date'])}，{dt.date.today()} 產生）", "",
         "由 `tools/inventory_cycle.py` 產生。存貨周轉天數 = 平均存貨 ÷ 單季營業成本 × 91；"
         "組別合計只加總當季與去年同季都有資料的公司。時間點是法定截止日（`avail_date`）。不放存貨原始金額。", ""]

    state = "**亮**" if last["d"] > thr else "未亮"
    L += ["## 燈號", "",
          f"- 半導體 ex-台積電 {qlabel(last['date'])}（{last['avail']} 可得）天數 {last['dio']:.0f}，"
          f"年增 {sgn(last['d'])} 天，門檻 > +{thr:g} → {state}"
          + (f"，連續 {streak} 季。" if streak else "。")]
    for q in pending:
        L.append(f"- {qlabel(q['date'])} 未到齊（{q['n']} 家），暫看 {q['dio']:.0f} 天、年增 {sgn(q['d'])}，"
                 f"截止日 {q['avail']} 後重跑。")
    L += ["- 觸發時的動作：見頂檢查清單第 5 項（NVIDIA DSO、庫存）記為「台灣旁證成立」，"
          "對照記憶體模組廠與 ASIC 廠的明細判斷是價格（投入成本上漲）還是數量。不自動改 `portfolio/`。", ""]

    L += ["## 近 8 季", "", "| 季度 | 可得日 | " + " | ".join(GROUPS.values()) + " |",
          "|---|---|" + "---|" * len(GROUPS)]
    by_date = {g_: {q["date"]: q for q in qs} for g_, qs in g.items()}
    for q in sig[-8:]:
        cells = []
        for g_ in GROUPS:
            r = by_date[g_].get(q["date"])
            if r is None:
                cells.append("—")
            else:
                mark = "" if r["complete"] else f"（未到齊 {r['n']} 家）"
                cells.append(f"{r['dio']:.0f} 天（{sgn(r['d'])}）{mark}")
        L.append(f"| {qlabel(q['date'])} | {q['avail']} | " + " | ".join(cells) + " |")
    L += ["", "括號內是天數年增。", ""]

    L += ["## 訊號開始後的加權指數", "",
          f"半導體 ex-台積電天數年增首次 > +{thr:g}（上一季沒亮）的季度，從可得日起算。", "",
          "| 季度 | 可得日 | 天數年增 | 加權 | 6 個月 | 12 個月 | 12 個月內最大跌幅 |",
          "|---|---|---|---|---|---|---|"]
    for e in events(sig, thr):
        f = forward(taiex, e["avail"])
        if f is None:
            L.append(f"| {qlabel(e['date'])} | {e['avail']} | {sgn(e['d'])} | — | — | — | — |")
            continue
        mdd = pct(f["mdd"]) + ("" if f["full"] else "（未滿 12 個月）")
        L.append(f"| {qlabel(e['date'])} | {e['avail']} | {sgn(e['d'])} | {f['level']:,.0f} | "
                 f"{pct(f['r6'])} | {pct(f['r12'])} | {mdd} |")
    base = [forward(taiex, q["avail"]) for q in done]
    base = [b for b in base if b and b["full"]]
    if base:
        r12 = sorted(b["r12"] for b in base)
        mdd = sorted(b["mdd"] for b in base)
        L += ["", f"對照：{qlabel(done[0]['date'])} 起所有季度的可得日（{len(base)} 次），12 個月報酬中位數 "
                  f"{pct(r12[len(r12) // 2])}，12 個月內最大跌幅中位數 {pct(mdd[len(mdd) // 2])}。"]
    L += ["", "解讀（2026-11-10）：",
          "- 2015Q1 在加權高點（4/27）後 3 週亮；2021Q3 在高點（2022-01-04）前 7 週亮。",
          "- 2018Q4 是 2018 年下跌之後的落後確認，亮的時候跌勢已過；12 個月內的最大跌幅來自 2020-03 疫情，不算命中。",
          "- 2026Q1 在 2026-05-16 亮，之後加權又漲到 10/6 的 49,823（約 +22%）才回落，提前約 5 個月。",
          "- 樣本只有 4 次，門檻是事後訂的，只看方向。", ""]

    L += [f"## 半導體 ex-台積電：{qlabel(last['date'])} 存貨增加最多的公司", "",
          "| 公司 | 去年同季天數 | 本季天數 | 營業成本年增 | 類別 |", "|---|---|---|---|---|"]
    for sid, name, d1, d0, cy in load_contrib(con, last["date"]):
        kind = "記憶體模組" if sid in MEMORY_MODULE else ""
        L.append(f"| {name} {sid} | {d1:.0f} | {d0:.0f} | {pct(cy)} | {kind} |")
    L += ["", "依存貨增加金額排序。記憶體模組廠在缺貨、漲價時囤貨，報價轉折時會有存貨跌價；"
              "投入成本上漲也會讓天數機械性變高（存貨按成本計價，比營業成本先反映）。", ""]

    qs = [q["date"] for q in sig[-6:]]
    w = load_watch(con, qs)
    L += ["## 觀察名單：存貨周轉天數", "", "| 公司 | " + " | ".join(qlabel(d) for d in qs) + " |",
          "|---|" + "---|" * len(qs)]
    for sid, name in WATCH.items():
        L.append(f"| {name} {sid} | " + " | ".join(
            f"{w[(sid, d)]:.0f}" if (sid, d) in w else "—" for d in qs) + " |")
    L += ["", "2022 年對照：聯發科 2022Q4 125、技嘉 2022Q2 147、華碩 2022Q2 176、台積電 2022Q2 87。", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="寫入 markdown 檔")
    ap.add_argument("--threshold", type=float, default=THRESHOLD, help="天數年增門檻（預設 6）")
    a = ap.parse_args()
    text = build(a.threshold)
    if a.out:
        pathlib.Path(a.out).write_text(text + "\n")
        print(f"已寫入 {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
