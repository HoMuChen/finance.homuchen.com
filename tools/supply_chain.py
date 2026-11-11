"""台灣 AI 供應鏈月營收旁證：每月監測 + 領先落後檢驗。

用法：
    uv run -q --with duckdb python tools/supply_chain.py                    # 每月監測表（終端）
    uv run -q --with duckdb python tools/supply_chain.py --out reports/supply-chain-2026-11-10.md
    uv run -q --with duckdb python tools/supply_chain.py leadlag            # 領先落後檢驗
    uv run -q --with duckdb python tools/supply_chain.py leadlag --out reports/supply-chain-leadlag-2026-11-02.md

候選三組（2026-11-02 使用者選定）：下游組裝、CoWoS 設備、封測與 ASIC。leadlag 檢驗全部候選；
每月監測只留通過或值得觀察的（MONITOR，見 data/L1_nvidia_tsmc.md 第 11 節）。
指標用「近 3 個月營收合計的年增率」（3M 年增），比單月穩定。組別合計只加總當月與去年同月都有資料的成員。

領先落後的判斷標準（看結果前定好，2026-11-02）：
- 台灣公司月營收都在次月 10 日前公布，和台積電月營收同步的公司，提供不了更早的資訊。
  所以「對台積電月營收」要領先 ≥ 1 個月，且相關係數在全期與 2020 年後都 ≥ 0.5，才算領先指標。
- CoWoS 設備「對台積電 CapEx」（季，近 4 季合計年增）同步即可：CapEx 一季才揭露一次，月營收比它早。
- 下游組裝對四大雲 CapEx：資料只有 2024Q1 起（年增 7 季），只描述、不判定。
年增率是重疊視窗，相關係數會偏高；另列 3 個月差分的相關做穩健性檢查。

公開 repo：輸出只放年增率、相關係數與領先月數，不放 FinMind 的月營收原始金額。
"""

import argparse
import csv
import datetime as dt
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from r2 import connect  # noqa: E402
from eps_nowcast import MOPS_CACHE, fetch_mops  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANDIDATES = {
    "下游組裝": {"2382": "廣達", "3231": "緯創", "6669": "緯穎", "2317": "鴻海"},
    "CoWoS 設備": {"3131": "弘塑", "6187": "萬潤"},
    "封測與 ASIC": {"3374": "精材", "2449": "京元電", "6515": "穎崴", "6223": "旺矽", "3661": "世芯-KY", "3443": "創意"},
}
# 2026-11-02 leadlag 結果：沒有一家領先台積電月營收；弘塑對台積電 CapEx 同步相關 0.50（2020 後 0.56）→ 留；
# 下游組裝對四大雲 CapEx 同季相關 0.90 但只有 7 季 → 留作觀察；封測與 ASIC、萬潤 → 剔除。
MONITOR = {
    "下游組裝": CANDIDATES["下游組裝"],
    "CoWoS 設備": {"3131": "弘塑"},
}
TSMC = "2330"
HYPERSCALERS = ("MSFT", "GOOGL", "AMZN", "META", "ORCL")
MAX_LAG_M, MAX_LAG_Q = 12, 4
MIN_CORR = 0.5
SINCE_RECENT = (2020, 1)
OTC = {"3131", "6187", "6223", "6515", "3374"}  # 上櫃公司，MOPS 彙總表在 otc 頁


# ---------- 資料 ----------

def load_revenue(con, ids):
    rows = con.execute(
        f"SELECT stock_id, revenue_year, revenue_month, revenue FROM tw.main.revenue "
        f"WHERE stock_id IN ({','.join('?' * len(ids))})", list(ids)).fetchall()
    rev = {}
    for sid, y, m, v in rows:
        if v:
            rev.setdefault(sid, {})[(int(y), int(m))] = float(v)
    return rev


def load_tsmc_capex(con):
    """單季 CapEx（取得不動產、廠房及設備，現金流量表為年初累計 → 相減）。"""
    ytd = {(d.year, (d.month - 1) // 3 + 1): -v for d, v in con.execute(
        "SELECT date, value FROM tw.main.cf WHERE stock_id = ? AND type = 'PropertyAndPlantAndEquipment'",
        [TSMC]).fetchall()}
    return {(y, q): v - ytd.get((y, q - 1), 0) if q > 1 else v
            for (y, q), v in ytd.items() if q == 1 or (y, q - 1) in ytd}


def load_hyperscaler_capex():
    tot = {}
    with open(ROOT / "data/L1_hyperscalers.csv") as f:
        for r in csv.DictReader(f):
            if r["metric"] == "capex_cash_ppe" and r["company"] in HYPERSCALERS and r["value_usd_bn"]:
                y, q = int(r["calendar_quarter"][:4]), int(r["calendar_quarter"][-1])
                tot.setdefault((y, q), {})[r["company"]] = float(r["value_usd_bn"])
    return {k: sum(v.values()) for k, v in tot.items() if len(v) == len(HYPERSCALERS)}


# ---------- 序列 ----------

def mshift(ym, k):
    y, m = ym
    i = y * 12 + (m - 1) + k
    return (i // 12, i % 12 + 1)


def qshift(yq, k):
    y, q = yq
    i = y * 4 + (q - 1) + k
    return (i // 4, i % 4 + 1)


def roll_yoy(members, months, window=3, shift=mshift, lag=12):
    """近 window 期合計的年增率；成員只計入本期與去年同期整個視窗都有資料者。"""
    out = {}
    for t in months:
        cur = prev = 0.0
        n = 0
        for s in members:
            w = [shift(t, -i) for i in range(window)]
            wl = [shift(x, -lag) for x in w]
            if all(x in s for x in w + wl):
                cur += sum(s[x] for x in w)
                prev += sum(s[x] for x in wl)
                n += 1
        if n and prev > 0:
            out[t] = cur / prev - 1
    return out


def to_quarterly(series):
    q = {}
    for (y, m), v in series.items():
        q.setdefault((y, (m - 1) // 3 + 1), []).append(v)
    return {k: sum(v) for k, v in q.items() if len(v) == 3}


def xcorr(x, y, lags, shift, since=None):
    """corr(x_t, y_{t+L})；L > 0 表示 x 領先 y L 期。"""
    res = {}
    for lag in lags:
        pairs = [(x[t], y[shift(t, lag)]) for t in x if shift(t, lag) in y and (since is None or t >= since)]
        if len(pairs) >= 8:
            a, b = zip(*pairs)
            res[lag] = (statistics.correlation(a, b), len(pairs))
    return res


def diff(series, k, shift):
    return {t: v - series[shift(t, -k)] for t, v in series.items() if shift(t, -k) in series}


# ---------- 監測 ----------

def fill_latest(rev, last, offline=False):
    """R2 已有最新月份、但個別公司還沒收錄時，用 MOPS 官方月營收補（只補最新一個月）。"""
    filled, cache = [], {}
    for sid, series in rev.items():
        market = "otc" if sid in OTC else "sii"
        cached = (MOPS_CACHE / f"t21sc03_{market}_{last[0]}_{last[1]:02d}.html").exists()
        if last in series or (offline and not cached):  # 離線時只用本機快取
            continue
        if market not in cache:
            try:
                cache[market] = fetch_mops(*last, market)[0]
            except Exception as e:
                print(f"MOPS {market} {last[0]}-{last[1]:02d} 抓不到（{e}）", file=sys.stderr)
                cache[market] = {}
        if sid in cache[market]:
            series[last] = cache[market][sid] * 1000.0  # 千元 → 元，和 R2 同單位
            filled.append(sid)
    return filled


def monitor(con, offline=False):
    ids = [s for g in MONITOR.values() for s in g] + [TSMC]
    rev = load_revenue(con, ids)
    last = max(max(v) for v in rev.values())
    filled = fill_latest(rev, last, offline)
    months = [mshift(last, -i) for i in range(5, -1, -1)]
    lines = [f"# 台灣 AI 供應鏈月營收旁證（資料至 {last[0]}-{last[1]:02d}）", "",
             "由 `tools/supply_chain.py` 產生。數字為近 3 個月營收合計的年增率（3M 年增）；"
             "「放緩」＝3M 年增連續 3 個月下滑。不放月營收原始金額。", "",
             "| 公司 | " + " | ".join(f"{y}-{m:02d}" for y, m in months) + " | 單月年增 | 放緩 |",
             "|---|" + "---|" * (len(months) + 2)]

    def row(label, members, bold=False):
        r3 = roll_yoy(members, months + [mshift(months[0], -i) for i in range(1, 4)])
        r1 = roll_yoy(members, [last], window=1)
        seq = [r3.get(mshift(last, -i)) for i in range(3, -1, -1)]
        slow = all(v is not None for v in seq) and all(b < a for a, b in zip(seq, seq[1:]))
        cells = [f"{r3[t]:+.0%}" if t in r3 else "–" for t in months]
        name = f"**{label}**" if bold else label
        return f"| {name} | " + " | ".join(cells) + f" | {r1[last]:+.0%} | {'**是**' if slow else ''} |" \
            if last in r1 else f"| {name} | " + " | ".join(cells) + " | – | |"

    lines.append(row("台積電（對照）", [rev[TSMC]], bold=True))
    for g, members in MONITOR.items():
        if len(members) == 1:
            (s, n), = members.items()
            lines.append(row(f"{g}：{n} {s}", [rev[s]], bold=True))
            continue
        lines.append(row(f"{g}（合計）", [rev[s] for s in members if s in rev], bold=True))
        for s, n in members.items():
            if s in rev:
                lines.append(row(f"　{n} {s}", [rev[s]]))
    if filled:
        names = {s: n for g in MONITOR.values() for s, n in g.items()} | {TSMC: "台積電"}
        lines += ["", f"- {last[0]}-{last[1]:02d} R2 還沒收錄：" + "、".join(f"{names[s]} {s}" for s in filled) +
                  "，改用公開資訊觀測站月營收彙總表的官方金額計算。"]
    return "\n".join(lines)


# ---------- 領先落後 ----------

def best(res):
    lag, (c, n) = max(res.items(), key=lambda kv: kv[1][0])
    return lag, c, n


def leadlag(con):
    ids = [s for g in CANDIDATES.values() for s in g] + [TSMC]
    rev = load_revenue(con, ids)
    allm = sorted({t for s in rev.values() for t in s})
    tsmc = roll_yoy([rev[TSMC]], allm)
    tsmc_d = diff(tsmc, 3, mshift)
    capex_q = load_tsmc_capex(con)
    capex_ttm = roll_yoy([capex_q], sorted(capex_q), window=4, shift=qshift, lag=4)
    hyper = load_hyperscaler_capex()
    hyper_yoy = {t: v / hyper[qshift(t, -4)] - 1 for t, v in hyper.items() if qshift(t, -4) in hyper}

    lines = ["# 供應鏈月營收的領先落後檢驗", "",
             f"由 `tools/supply_chain.py leadlag` 產生（{dt.date.today().isoformat()}）。"
             "相關係數＝corr(公司 3M 年增_t, 台積電 3M 年增_t+L)，L > 0 表示公司領先 L 個月；"
             f"L 掃 −{MAX_LAG_M}～+{MAX_LAG_M}。差分＝3M 年增的 3 個月變化。", "",
             "## 1. 對台積電月營收（月）", "",
             "| 公司 | 起始 | 全期 L=0 | 全期最佳 L（相關） | 2020 後 L=0 | 2020 後最佳 L（相關） | 差分最佳 L（相關） | 判定 |",
             "|---|---|---|---|---|---|---|---|"]
    lags_m = range(-MAX_LAG_M, MAX_LAG_M + 1)
    verdicts = {}

    def test(label, members):
        x = roll_yoy(members, allm)
        if not x:
            return
        full = xcorr(x, tsmc, lags_m, mshift)
        rec = xcorr(x, tsmc, lags_m, mshift, since=SINCE_RECENT)
        dres = xcorr(diff(x, 3, mshift), tsmc_d, lags_m, mshift)
        bf, br, bd = best(full), best(rec), best(dres)
        lead = bf[0] >= 1 and br[0] >= 1 and bf[1] >= MIN_CORR and br[1] >= MIN_CORR
        sync = max(full[0][0], rec[0][0]) >= MIN_CORR
        verdict = "領先" if lead else ("同步（無時間優勢）" if sync else "關聯弱")
        verdicts[label] = verdict
        start = min(x)
        lines.append(f"| {label} | {start[0]}-{start[1]:02d} | {full[0][0]:.2f} | {bf[0]:+d}（{bf[1]:.2f}） | "
                     f"{rec[0][0]:.2f} | {br[0]:+d}（{br[1]:.2f}） | {bd[0]:+d}（{bd[1]:.2f}） | {verdict} |")

    for g, members in CANDIDATES.items():
        test(f"**{g}（合計）**", [rev[s] for s in members if s in rev])
        for s, n in members.items():
            if s in rev:
                test(f"{n} {s}", [rev[s]])

    lines += ["", "## 2. CoWoS 設備對台積電 CapEx（季，近 4 季合計年增）", "",
              "相關係數＝corr(設備營收年增_t, 台積電 CapEx 年增_t+L)，L 以季計；L < 0 表示設備營收落後 CapEx。", "",
              "| 公司 | 全期 L=0 | 全期最佳 L（相關） | 2020 後 L=0 | 2020 後最佳 L（相關） | 樣本季數 | 判定 |",
              "|---|---|---|---|---|---|---|"]
    lags_q = range(-MAX_LAG_Q, MAX_LAG_Q + 1)
    for label, members in [("**CoWoS 設備（合計）**", [rev[s] for s in CANDIDATES["CoWoS 設備"]])] + \
            [(f"{n} {s}", [rev[s]]) for s, n in CANDIDATES["CoWoS 設備"].items()]:
        q = roll_yoy([to_quarterly(m) for m in members], sorted(capex_ttm), window=4, shift=qshift, lag=4)
        res = xcorr(q, capex_ttm, lags_q, qshift)
        rec = xcorr(q, capex_ttm, lags_q, qshift, since=SINCE_RECENT)
        b, br = best(res), best(rec)
        ok = res.get(0, (0, 0))[0] >= MIN_CORR or (abs(b[0]) <= 1 and b[1] >= MIN_CORR)
        lines.append(f"| {label} | {res[0][0]:.2f} | {b[0]:+d}（{b[1]:.2f}） | {rec[0][0]:.2f} | "
                     f"{br[0]:+d}（{br[1]:.2f}） | {b[2]} | {'可當旁證' if ok else '關聯弱'} |")

    lines += ["", "## 3. 下游組裝對四大雲現金 CapEx（季年增，2025Q1 起，只描述）", "",
              "| 季度 | 四大雲＋Oracle CapEx 年增 | 下游組裝營收年增 |", "|---|---|---|"]
    down_q = roll_yoy([to_quarterly(rev[s]) for s in CANDIDATES["下游組裝"]], sorted(hyper_yoy), window=1, shift=qshift, lag=4)
    for t in sorted(hyper_yoy):
        lines.append(f"| {t[0]}Q{t[1]} | {hyper_yoy[t]:+.0%} | {down_q[t]:+.0%} |" if t in down_q else
                     f"| {t[0]}Q{t[1]} | {hyper_yoy[t]:+.0%} | – |")
    pairs = [(hyper_yoy[t], down_q[t]) for t in hyper_yoy if t in down_q]
    if len(pairs) >= 4:
        a, b = zip(*pairs)
        lines += ["", f"同季相關係數 {statistics.correlation(a, b):.2f}（{len(pairs)} 季，樣本太少，只當參考）。"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", nargs="?", default="monitor", choices=["monitor", "leadlag"])
    ap.add_argument("--out", help="寫入 markdown 檔")
    ap.add_argument("--offline", action="store_true", help="R2 缺最新月份時只用本機 MOPS 快取，不連網")
    a = ap.parse_args()
    con = connect()
    text = monitor(con, a.offline) if a.mode == "monitor" else leadlag(con)
    if a.out:
        pathlib.Path(a.out).write_text(text + "\n")
        print(f"已寫入 {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
