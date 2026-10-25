"""低檔加碼輔助訊號：大盤融資維持率 → 目前燈號 → 歷史跌破事件與之後報酬。

用法：
    python3 tools/margin_signal.py                                   # 輸出到終端
    python3 tools/margin_signal.py --out reports/margin-2026-10-25.md
    python3 tools/margin_signal.py --offline                         # 只用快取
    python3 tools/margin_signal.py --cycle-top                       # 見頂檢查清單已出現 2–3 項時，只認最深一階

維持率低代表融資戶被追繳、被迫賣出，是籌碼面的止跌訊號，不代表基本面。
只當 U6 加碼價的輔助，不單獨決定加碼；也不放進凱利的預期報酬。
資料 2015 年起，期間台股長多、沒有長空頭，事件只有 5–7 次，結果只能看方向。
"""

import argparse
import datetime as dt
import pathlib

import numpy as np

from kelly import CACHE, _cached, finmind_token

START = "2015-01-01"
URL = "https://api.finmindtrade.com/api/v4/data?dataset={ds}&start_date={start}"
TIERS = [(150, "第一階"), (145, "第二階"), (140, "第三階")]
COOLDOWN_DAYS = 87  # 約 60 個交易日內再跌破，視為同一次事件
HORIZONS = (20, 60, 120, 250)
BETA_YEARS = 5


# ---------- 資料 ----------

def _load(dataset, data_id=None, offline=False):
    url = URL.format(ds=dataset, start=START) + (f"&data_id={data_id}" if data_id else "")
    headers = {"Authorization": f"Bearer {finmind_token()}"} if not offline else {}
    path = CACHE / f"finmind_{dataset}_{data_id or 'all'}_{START[:4]}.json"
    raw = _cached(path, url, headers, offline)
    if raw.get("status") != 200:
        raise RuntimeError(f"FinMind {dataset} {data_id or ''}: {raw.get('msg')}")
    return raw["data"]


def _series(rows, value, keep=lambda r: True):
    return {dt.date.fromisoformat(r["date"]): r[value] for r in rows if keep(r) and r[value]}


def load_all(offline):
    mm = _series(_load("TaiwanTotalExchangeMarginMaintenance", offline=offline), "TotalExchangeMarginMaintenance")
    margin = _series(_load("TaiwanStockTotalMarginPurchaseShortSale", offline=offline), "TodayBalance",
                     lambda r: r["name"] == "MarginPurchaseMoney")
    taiex = _series(_load("TaiwanStockPrice", "TAIEX", offline), "close")
    tri = _series(_load("TaiwanStockTotalReturnIndex", "TAIEX", offline), "price")
    tsmc = _series(_load("TaiwanStockPriceAdj", "2330", offline), "close")
    dates = sorted(set(mm) & set(margin) & set(taiex) & set(tri) & set(tsmc))
    arr = lambda s: np.array([s[d] for d in dates], dtype=float)
    return dates, {"mm": arr(mm), "margin": arr(margin) / 1e8, "taiex": arr(taiex), "tri": arr(tri), "tsmc": arr(tsmc)}


# ---------- 計算 ----------

def fwd(x, i, h):
    return x[i + h] / x[i] - 1 if i + h < len(x) else None


def drawdown_from_high(x, i, window=250):
    return x[i] / x[max(0, i - window + 1):i + 1].max() - 1


def further_drop(x, i, window=60):
    nxt = x[i + 1:i + 1 + window]
    return min(nxt.min() / x[i] - 1, 0.0) if len(nxt) else None


def episodes(dates, mm, threshold):
    """首次跌破門檻的日子；距上次低於門檻超過 COOLDOWN_DAYS 才算新事件。"""
    out, last = [], None
    for i, (d, v) in enumerate(zip(dates, mm)):
        if v < threshold:
            if last is None or (d - last).days > COOLDOWN_DAYS:
                out.append(i)
            last = d
    return out


def tsmc_beta(dates, s, h=20):
    cutoff = dates[-1] - dt.timedelta(days=365 * BETA_YEARS)
    idx = [i for i, d in enumerate(dates) if d >= cutoff]
    a, b = np.log(s["tsmc"][idx]), np.log(s["taiex"][idx])
    return float(np.polyfit(b[h:] - b[:-h], a[h:] - a[:-h], 1)[0])


# ---------- 報告 ----------

def sp(x):
    return "—" if x is None else f"{x:+.1%}"


def build(offline, cycle_top=False):
    dates, s = load_all(offline)
    mm, margin, taiex, tsmc = s["mm"], s["margin"], s["taiex"], s["tsmc"]
    n, last = len(dates), len(dates) - 1
    today = dates[last]
    pctl = (mm < mm[last]).mean()
    i_hi = int(np.argmax(margin))
    i_20, i_250 = max(0, last - 20), max(0, last - 250)
    hi_250 = taiex[max(0, last - 249):].max()

    lines = [f"# 融資維持率加碼訊號：{today}", "",
             f"產生時間：{dt.datetime.now():%Y-%m-%d %H:%M}；資料 {dates[0]} 起，共 {n} 個交易日（FinMind）。", "",
             "## 目前狀態", "", "| 項目 | 數值 |", "|---|---|",
             f"| 大盤融資維持率 | **{mm[last]:.1f}**（{dates[0].year} 年起第 {pctl * 100:.0f} 百分位） |",
             f"| 融資餘額 | {margin[last]:,.0f} 億（歷史高點 {margin[i_hi]:,.0f} 億，{dates[i_hi]}）；"
             f"20 日 {sp(margin[last] / margin[i_20] - 1)}、年增 {sp(margin[last] / margin[i_250] - 1)} |",
             f"| 加權指數 | {taiex[last]:,.0f}（250 日高點 {hi_250:,.0f}，回落 {sp(taiex[last] / hi_250 - 1)}） |",
             f"| 台積電（還原） | {tsmc[last]:,.0f} |", ""]

    # 燈號
    active = TIERS[-1:] if cycle_top else TIERS
    lines += ["## 燈號", "",
              "見頂檢查清單已出現 2–3 項（`--cycle-top`）：只認第三階，前兩階可能只是空頭的第一段。"
              if cycle_top else "一般情況：三階都算；見頂檢查清單出現 2–3 項時改用 `--cycle-top`。", "",
              "| 階段 | 條件 | 維持率還要下降 | 狀態 |", "|---|---|---|---|"]
    for th, name in TIERS:
        hit = mm[last] < th
        state = ("**觸發**" if hit else "未觸發") if (th, name) in active else "不採用"
        lines.append(f"| {name} | < {th} | {'—' if hit else sp(th / mm[last] - 1)} | {state} |")
    lines.append("")

    # 觸發位置粗估：用歷史第一階事件當時的「距 250 日高點回落」換算
    first = episodes(dates, mm, TIERS[0][0])
    dds = np.array([drawdown_from_high(taiex, i) for i in first])
    beta = tsmc_beta(dates, s)
    lines += ["## 第一階大約在哪裡觸發（粗估）", "",
              f"歷史 {len(first)} 次跌破 {TIERS[0][0]} 時，加權指數距 250 日高點回落 "
              f"{dds.max():+.0%} 到 {dds.min():+.0%}（中位數 {np.median(dds):+.0%}）。"
              f"套用到目前高點 {hi_250:,.0f}，台積電用 {BETA_YEARS} 年 20 日報酬 beta {beta:.2f} 換算：", "",
              "| 回落幅度 | 加權指數 | 距現在 | 台積電（約） |", "|---|---|---|---|"]
    for label, dd in (("較淺", dds.max()), ("中位數", float(np.median(dds))), ("較深", dds.min())):
        lvl = hi_250 * (1 + dd)
        move = lvl / taiex[last] - 1
        lines.append(f"| {label} {dd:+.0%} | {lvl:,.0f} | {sp(move)} | {tsmc[last] * (1 + beta * move):,.0f} |")
    lines += ["", "> 維持率也受新增融資、個股漲跌分布影響，這只是量級參考。2026-07 加權指數回落 16% 時，維持率最低 157，沒有跌破 150。", ""]

    # 歷史事件
    lines += ["## 歷史事件：首次跌破後的報酬（加權報酬指數；台積電為還原股價）", ""]
    for th, name in TIERS:
        ep = episodes(dates, mm, th)
        lines += [f"### {name}：維持率 < {th}（{len(ep)} 次）", "",
                  "| 日期 | 維持率 | 指數距高點 | " + " | ".join(f"{h} 日" for h in HORIZONS)
                  + " | 台積電 250 日 | 之後 60 日最多再跌 |",
                  "|---|---|---|" + "---|" * len(HORIZONS) + "---|---|"]
        for i in ep:
            lines.append(f"| {dates[i]} | {mm[i]:.1f} | {sp(drawdown_from_high(taiex, i))} | "
                         + " | ".join(sp(fwd(s["tri"], i, h)) for h in HORIZONS)
                         + f" | {sp(fwd(tsmc, i, 250))} | {sp(further_drop(taiex, i))} |")
        r250 = [r for r in (fwd(s["tri"], i, 250) for i in ep) if r is not None]
        if r250:
            lines.append(f"| **250 日為正 {sum(r > 0 for r in r250)}/{len(r250)}** | | | | | | "
                         f"**中位數 {np.median(r250):+.1%}** | | |")
        lines.append("")

    lines += ["> 樣本 2015 年起，期間台股長多，沒有 2008 年那種跌破後續跌的長空頭；事件少、報酬重疊，只能看方向。"
              "2022-05 跌破 150 後台積電 120 日仍 −22%，真正低點要到維持率 < 140。", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--cycle-top", action="store_true", help="見頂檢查清單已出現 2–3 項：只認第三階")
    args = ap.parse_args()
    report = build(args.offline, args.cycle_top)
    if args.out:
        pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.out).write_text(report)
        print(f"已寫入 {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
