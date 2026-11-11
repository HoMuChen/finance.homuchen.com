"""月營收 → 當季 EPS 即時推估（台積電、聯發科）。

用法：
    uv run -q --with duckdb python tools/eps_nowcast.py                          # 輸出到終端
    uv run -q --with duckdb python tools/eps_nowcast.py --out reports/eps-nowcast-2026-11-10.md
    uv run -q --with duckdb python tools/eps_nowcast.py --ids 2330

每月 10 日前後月營收公布後跑一次。資料：
- 月營收、單季財報：fire-auto 的 R2 資料湖（tw.main.revenue／tw.main.fin）。
- 財測與 R2 還沒收錄的已公布季度：data/eps_guidance.json（每季法說後手動更新）。

兩種推估：
- A 上季淨利率法：上季 EPS ×（本季營收 ÷ 上季營收），等於假設淨利率跟上季一樣（涂敏峰的做法）。
- B 財測營益率法：本季營收 × 財測營益率中值 ×（上季淨利 ÷ 上季營業利益）÷ 股數。
  沒有營益率財測時，用毛利率中值減費用率中值。
季內營收還沒到齊時，本季營收用財測中值；同時列「已公布月份月均 × 3」的外推做對照。

公開 repo：計算用 R2（FinMind），但報告裡的月營收金額只用公開資訊觀測站的官方數字
（data/tw_monthly_revenue.csv，標 [官方]），不顯示 FinMind 的金額。缺的月份會自動從 MOPS
「上市公司每月營業收入彙總表」抓（--offline 不抓），並和 R2 比對，不一致會警告。
"""

import argparse
import csv
import datetime as dt
import json
import pathlib
import re
import ssl
import statistics
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from r2 import connect  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUIDANCE = ROOT / "data/eps_guidance.json"
OFFICIAL = ROOT / "data/tw_monthly_revenue.csv"
OFFICIAL_FIELDS = ["stock_id", "name", "month", "revenue", "unit", "source_url", "source_date", "quality"]
MOPS_URL = "https://mopsov.twse.com.tw/nas/t21/{market}/t21sc03_{roc}_{month}_0.html"
MOPS_CACHE = ROOT / "cache/mops"
BACKTEST_QUARTERS = 12
SHOW_MONTHS = 6


def qkey(year, month):
    return f"{year}Q{(month - 1) // 3 + 1}"


def qprev(q):
    y, n = int(q[:4]), int(q[-1])
    return f"{y - 1}Q4" if n == 1 else f"{y}Q{n - 1}"


def qmonths(q):
    y, n = int(q[:4]), int(q[-1])
    return [(y, 3 * (n - 1) + i) for i in (1, 2, 3)]


def mid(r):
    return (r[0] + r[1]) / 2


# ---------- 資料 ----------

def load(con, sid):
    rev = {(y, m): v / 1e9 for y, m, v in con.execute(
        "SELECT revenue_year, revenue_month, revenue FROM tw.main.revenue WHERE stock_id = ?", [sid]).fetchall()}
    fin = {}
    for d, t, v in con.execute(
            "SELECT date, type, value FROM tw.main.fin WHERE stock_id = ? AND type IN "
            "('Revenue', 'OperatingIncome', 'EquityAttributableToOwnersOfParent', 'EPS')", [sid]).fetchall():
        q = fin.setdefault(qkey(d.year, d.month), {})
        q[{"Revenue": "revenue", "OperatingIncome": "operating_income",
           "EquityAttributableToOwnersOfParent": "net_income", "EPS": "eps"}[t]] = v if t == "EPS" else v / 1e9
    return rev, fin


def load_official():
    """官方月營收：{(stock_id, (y, m)): row}，revenue 單位千元。"""
    if not OFFICIAL.exists():
        return {}
    with open(OFFICIAL, newline="") as f:
        return {(r["stock_id"], tuple(map(int, r["month"].split("-")))): r for r in csv.DictReader(f)}


def fetch_mops(y, m, market="sii"):
    """公開資訊觀測站月營收彙總表（全部上市或上櫃公司一頁）→ {stock_id: 當月營收千元}。"""
    url = MOPS_URL.format(market=market, roc=y - 1911, month=m)
    cache = MOPS_CACHE / f"t21sc03_{market}_{y}_{m:02d}.html"
    if cache.exists():
        raw = cache.read_bytes()
    else:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        # 證交所憑證缺 Subject Key Identifier，Python 3.13 的 VERIFY_X509_STRICT 會擋；
        # 只關這一項嚴格檢查，憑證鏈與主機名稱照常驗證。
        ctx = ssl.create_default_context()
        ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            raw = r.read()
        time.sleep(1)
    text = re.sub(r"<[^>]+>", "|", raw.decode("cp950", errors="replace"))
    out = {}
    for sid, rev in re.findall(r"\|(\d{4})\|+[^|]+\|+\s*([\d,]+)\|", text):
        out.setdefault(sid, int(rev.replace(",", "")))
    if not out:
        raise RuntimeError(f"解析不到 MOPS 月營收：{url}")
    if not cache.exists():  # 解析成功才快取，還沒公布的空頁面不留下來
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(raw)
    return out, url


def ensure_official(official, sid, name, months, market, offline):
    """把缺的月份從 MOPS 補進 data/tw_monthly_revenue.csv。"""
    missing = [k for k in months if (sid, k) not in official]
    if offline or not missing:
        return []
    new = []
    for y, m in missing:
        vals, url = fetch_mops(y, m, market)
        if sid in vals:
            row = {"stock_id": sid, "name": name, "month": f"{y}-{m:02d}", "revenue": vals[sid],
                   "unit": "TWD_thousand", "source_url": url, "source_date": dt.date.today().isoformat(),
                   "quality": "官方"}
            official[(sid, (y, m))] = row
            new.append(row)
    if new:
        exists = OFFICIAL.exists()
        with open(OFFICIAL, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=OFFICIAL_FIELDS)
            if not exists:
                w.writeheader()
            w.writerows(new)
    return new


def merge_reported(fin, reported):
    """R2 沒有的季度才用 json 的 reported；R2 有了以 R2 為準。"""
    out = {q: dict(v) for q, v in fin.items()}
    for q, v in reported.items():
        if q not in out or "eps" not in out[q]:
            out[q] = {k: v[k] for k in ("revenue", "operating_income", "net_income", "eps") if k in v}
    return out


def shares(fin):
    """股數（十億股）＝最近一季 R2 財報的母公司淨利 ÷ EPS。"""
    for q in sorted(fin, reverse=True):
        f = fin[q]
        if f.get("eps") and f.get("net_income"):
            return f["net_income"] / f["eps"], q
    raise RuntimeError("找不到同時有 EPS 與淨利的季度")


def fill_from_official(rev, official, sid, name, market, offline, today):
    """R2 還沒收錄、但 MOPS 已公布的月份：用官方金額補進計算（千元 → 十億元）。

    R2 有時整批月營收進來了，個別公司卻晚幾天才有（例如 2026-10 的台積電、聯發科）。
    只往 R2 最新月份之後補，補到上個月為止；抓不到就停。
    """
    filled = []
    y, m = max(rev)
    while True:
        y, m = (y, m + 1) if m < 12 else (y + 1, 1)
        if (y, m) >= (today.year, today.month):
            break
        if (sid, (y, m)) not in official and not offline:
            try:
                ensure_official(official, sid, name, [(y, m)], market, offline)
            except Exception as e:  # 還沒公布或網路問題：只用 R2 的月份
                print(f"{name}：MOPS {y}-{m:02d} 抓不到（{e}），只用 R2 的月份", file=sys.stderr)
                break
        row = official.get((sid, (y, m)))
        if not row:
            break
        rev[(y, m)] = int(row["revenue"]) / 1e6
        filled.append((y, m))
    return filled


# ---------- 計算 ----------

def yoy_table(rev, n=6):
    rows = []
    for (y, m) in sorted(rev)[-n:]:
        cur, last = rev[(y, m)], rev.get((y - 1, m))
        prev = rev.get((y, m - 1) if m > 1 else (y - 1, 12))
        rows.append(((y, m), cur / last - 1 if last else None, cur / prev - 1 if prev else None))
    return rows


def slowing(rev):
    """年增率連續 3 個月下滑（見頂檢查清單第 4 項）。"""
    ks = sorted(rev)[-4:]
    yoys = [rev[(y, m)] / rev[(y - 1, m)] - 1 for (y, m) in ks if (y - 1, m) in rev]
    return len(yoys) == 4 and all(b < a for a, b in zip(yoys, yoys[1:]))


def backtest_a(fin, sh):
    """A 法在歷史上的誤差：用『實際』季營收代入，看上季淨利率不變的假設差多少。"""
    errs = []
    qs = sorted(q for q in fin if fin[q].get("revenue") and fin[q].get("net_income"))
    for q in qs[-BACKTEST_QUARTERS:]:
        p = fin.get(qprev(q))
        if not p or not p.get("revenue") or not p.get("net_income"):
            continue
        eps_p = p.get("eps") or p["net_income"] / sh
        eps_q = fin[q].get("eps") or fin[q]["net_income"] / sh
        est = eps_p * fin[q]["revenue"] / p["revenue"]
        errs.append((q, est / eps_q - 1))
    return errs


def nowcast(q, g, rev, fin, sh):
    p = fin.get(qprev(q))
    if not p:
        raise RuntimeError(f"{qprev(q)} 沒有財報資料，請在 eps_guidance.json 的 reported 補上")
    eps_p = p.get("eps") or p["net_income"] / sh
    fx = g["fx"] if g["currency"] == "USD" else 1.0
    g_lo, g_hi = g["revenue"][0] * fx, g["revenue"][1] * fx
    g_mid = (g_lo + g_hi) / 2
    if "operating_margin" in g:
        om = [x / 100 for x in g["operating_margin"]]
    else:
        om = [(g["gross_margin"][0] - g["opex_ratio"][1]) / 100, (g["gross_margin"][1] - g["opex_ratio"][0]) / 100]
    ni_oi = p["net_income"] / p["operating_income"]
    known = [rev[k] for k in qmonths(q) if k in rev]
    k = len(known)
    qtd = sum(known)
    est = qtd if k == 3 else g_mid
    r = {
        "q": q, "prev": qprev(q), "k": k, "fx": fx, "currency": g["currency"],
        "g_mid": g_mid, "g_lo": g_lo, "g_hi": g_hi, "om": om, "ni_oi": ni_oi,
        "progress": qtd / g_mid if k else 0.0,
        "need": {lab: (v - qtd) / (3 - k) / (qtd / k) - 1 for lab, v in
                 (("下緣", g_lo), ("中值", g_mid), ("上緣", g_hi))} if 0 < k < 3 else None,
        "runrate": qtd / k * 3 if k else None,
        "est": est,
        "qoq": est / p["revenue"] - 1,
        "eps_prev": eps_p,
        "eps_a": eps_p * est / p["revenue"],
        "eps_b": est * mid(om) * ni_oi / sh,
        "eps_b_lo": (est if k == 3 else g_lo) * om[0] * ni_oi / sh,
        "eps_b_hi": (est if k == 3 else g_hi) * om[1] * ni_oi / sh,
        "prev_om": p["operating_income"] / p["revenue"],
        "source": g["source"],
    }
    if k:
        r["eps_a_runrate"] = eps_p * r["runrate"] / p["revenue"]
        r["eps_b_runrate"] = r["runrate"] * mid(om) * ni_oi / sh
    return r


# ---------- 輸出 ----------

def pct(x, sign=True):
    return "–" if x is None else (f"{x:+.1%}" if sign else f"{x:.1%}")


def bn(row):
    return f"{int(row['revenue']) / 1e6:,.1f}" if row else "–"


def render(results, asof):
    out = [f"# 月營收 → 當季 EPS 推估（{asof}）", "",
           "由 `tools/eps_nowcast.py` 產生。A＝上季淨利率不變；B＝財測營益率中值 × 上季淨利÷營業利益。",
           "季內營收未到齊時，本季營收用財測中值；「月均外推」只是對照。",
           "月營收金額取自公開資訊觀測站「上市公司每月營業收入彙總表」[官方]（`data/tw_monthly_revenue.csv`）；"
           "年增、月增與推估由 R2 計算，並與官方金額比對。", ""]
    for sid, name, rows, yoys, slow, bt, sh, sh_q, off, mism, filled in results:
        out += [f"## {name}（{sid}）", ""]
        out += ["**月營收**", "", "| 月份 | 營收（NT$B，官方） | 年增 | 月增 |", "|---|---|---|---|"]
        out += [f"| {y}-{m:02d} | {bn(off.get((y, m)))} | {pct(a)} | {pct(b)} |" for (y, m), a, b in yoys]
        out += ["", f"- 年增率連續 3 個月下滑：{'**是**' if slow else '否'}"]
        if mism:
            out += ["- ⚠ 官方金額與 R2 不一致：" + "、".join(f"{y}-{m:02d}" for y, m in mism) + "（以官方為準，檢查 R2）"]
        elif len(off) > len(filled):
            out += [f"- 官方金額與 R2 一致（{len(off) - len(filled)} 個月）"]
        if filled:
            out += ["- " + "、".join(f"{y}-{m:02d}" for y, m in filled) +
                    " R2 還沒收錄，年增、月增與推估改用官方金額計算"]
        out += [""]
        for r in rows:
            unit = f"US$ × {r['fx']}" if r["currency"] == "USD" else "NT$"
            out += [f"**{r['q']}**（財測 {unit}；已公布 {r['k']}/3 個月）", ""]
            qtd = [off.get(k) for k in qmonths(r["q"]) if off.get(k)]
            if qtd:
                out += [f"- 季內已公布營收 NT${sum(int(x['revenue']) for x in qtd) / 1e6:,.1f}B（官方）；"
                        f"財測 NT${r['g_lo']:,.1f}–{r['g_hi']:,.1f}B，中值 {r['g_mid']:,.1f}B"]
            else:
                out += [f"- 財測 NT${r['g_lo']:,.1f}–{r['g_hi']:,.1f}B，中值 {r['g_mid']:,.1f}B"]
            if 0 < r["k"] < 3:
                need = "、".join(f"{lab} {pct(v)}" for lab, v in r["need"].items())
                out += [f"- 季內進度：財測中值的 {pct(r['progress'], False)}（每月平均要達 1/3 ≈ 33.3%）",
                        f"- 剩下月份的月營收要比已公布月均：{need}"]
            elif r["k"] == 3:
                out += [f"- 季營收已到齊：為財測中值的 {pct(r['progress'], False)}"]
            out += [f"- 本季營收{'（實際）' if r['k'] == 3 else '（財測中值）'}季增 {pct(r['qoq'])}；"
                    f"財測營益率 {r['om'][0]:.1%}–{r['om'][1]:.1%}（上季實際 {r['prev_om']:.1%}），"
                    f"上季淨利÷營業利益 {r['ni_oi']:.3f}",
                    "", "| 推估 | EPS（元） | 說明 |", "|---|---|---|",
                    f"| 上季實際（{r['prev']}） | {r['eps_prev']:.2f} | |",
                    f"| A 上季淨利率法 | {r['eps_a']:.2f} | 本季營收 ÷ 上季營收 × 上季 EPS |",
                    f"| B 財測營益率法 | **{r['eps_b']:.2f}** | 區間 {r['eps_b_lo']:.2f}–{r['eps_b_hi']:.2f}"
                    f"（{'營益率上下緣' if r['k'] == 3 else '營收與營益率同取上下緣'}） |"]
            if r["k"] and r["k"] < 3:
                out += [f"| 月均外推（A／B） | {r['eps_a_runrate']:.2f}／{r['eps_b_runrate']:.2f} | "
                        f"已公布月份月均 × 3，季底月份常較高，偏保守 |"]
            out += ["", f"財測來源：{r['source']}", ""]
        if bt:
            errs = [e for _, e in bt]
            worst = max(bt, key=lambda x: abs(x[1]))
            out += [f"**A 法的歷史誤差**（最近 {len(bt)} 季，代入實際季營收）：中位數絕對誤差 "
                    f"{statistics.median(abs(e) for e in errs):.1%}，平均 {pct(statistics.mean(errs))}，"
                    f"最大 {worst[0]} {pct(worst[1])}。毛利率或業外變動大的季度，A 法會偏離。", ""]
        out += [f"股數：{sh:.2f} 十億股（{sh_q} 財報淨利 ÷ EPS）", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*", help="股票代號（預設 eps_guidance.json 全部）")
    ap.add_argument("--out", help="寫入 markdown 檔")
    ap.add_argument("--offline", action="store_true", help="不從 MOPS 補官方月營收")
    a = ap.parse_args()
    cfg = json.loads(GUIDANCE.read_text())
    ids = a.ids or [k for k in cfg if not k.startswith("_")]
    con = connect()
    official = load_official()
    results = []
    for sid in ids:
        c = cfg[sid]
        rev, fin_r2 = load(con, sid)
        filled = fill_from_official(rev, official, sid, c["name"], c.get("market", "sii"), a.offline,
                                    dt.date.today())
        if filled:
            print(f"{c['name']}：R2 沒有 " + "、".join(f"{y}-{m:02d}" for y, m in filled) +
                  "，改用 MOPS 官方月營收", file=sys.stderr)
        sh, sh_q = shares(fin_r2)
        fin = merge_reported(fin_r2, c.get("reported", {}))
        rows = [nowcast(q, g, rev, fin, sh) for q, g in sorted(c["guidance"].items())]
        months = sorted(set(sorted(rev)[-SHOW_MONTHS:]) |
                        {k for q in c["guidance"] for k in qmonths(q) if k in rev})
        added = ensure_official(official, sid, c["name"], months, c.get("market", "sii"), a.offline)
        if added:
            print(f"{c['name']}：從 MOPS 補了 {len(added)} 個月官方月營收 → {OFFICIAL.relative_to(ROOT)}", file=sys.stderr)
        off = {k: official[(sid, k)] for k in months if (sid, k) in official}
        mism = [k for k, r in sorted(off.items())
                if k not in filled and abs(int(r["revenue"]) / 1e6 / rev[k] - 1) > 1e-6]
        results.append((sid, c["name"], rows, yoy_table(rev, SHOW_MONTHS), slowing(rev), backtest_a(fin_r2, sh),
                        sh, sh_q, off, mism, filled))
    text = render(results, dt.date.today().isoformat())
    if a.out:
        pathlib.Path(a.out).write_text(text + "\n")
        print(f"已寫入 {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
