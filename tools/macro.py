"""總經訊號：只追會改動模型參數的幾個指標。每月跑一次，加上每次 FOMC 會後。

用法：
    python3 tools/macro.py                                  # 輸出到終端
    python3 tools/macro.py --out reports/macro-2026-11-03.md
    python3 tools/macro.py --offline                        # 只用快取

資料：
- 美債名目與實質殖利率：美國財政部 Daily Treasury Par Yield Curve（公有領域，報告直接列數字）。
- 失業率（Sahm 規則）：BLS LNS14000000（公有領域）。
- USD/TWD：FinMind 台銀即期買賣中價。這是公開 repo，報告只列四捨五入到 0.1 的水準與變化幅度。
- 信用利差代理：Yahoo Finance 的 HYG／IEI、LQD／IEF 還原價，報告只列相對報酬。
- FOMC 決議、門檻、觸發時的模型動作：data/macro.json（手動維護）。

這台機器連不上 FRED，所以信用利差用 ETF 相對報酬代替 ICE BofA OAS。
只依賴標準函式庫與 numpy。快取在 cache/macro/ 與 cache/prices/（不進 git）。
"""

import argparse
import csv
import datetime as dt
import io
import json
import pathlib
import time
import urllib.request

import numpy as np

from kelly import ROOT, _finmind, _yahoo

CONFIG = ROOT / "data" / "macro.json"
MCACHE = ROOT / "cache" / "macro"
TREASURY = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
            "daily-treasury-rates.csv/{y}/all?type={t}&field_tdr_date_value={y}&page&_format=csv")
NOMINAL, REAL = "daily_treasury_yield_curve", "daily_treasury_real_yield_curve"
BLS = "https://api.bls.gov/publicAPI/v1/timeseries/data/{s}"
UNRATE = "LNS14000000"  # 失業率，季調
UA = {"User-Agent": "Mozilla/5.0"}
YEARS = 3
HORIZONS = (21, 63, 126)  # 交易日：約 1、3、6 個月


# ---------- 資料 ----------

def _text(path, url, offline, max_age_h=12):
    MCACHE.mkdir(parents=True, exist_ok=True)
    fresh = path.exists() and time.time() - path.stat().st_mtime < max_age_h * 3600
    if not offline and not fresh:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            path.write_bytes(r.read())
    if not path.exists():
        raise RuntimeError(f"沒有快取 {path.name}，先不加 --offline 跑一次")
    return path.read_text()


def treasury(kind, col, offline):
    """財政部每日殖利率；過去年度 30 天更新一次快取，今年 12 小時。"""
    out, this = {}, dt.date.today().year
    for y in range(this - YEARS + 1, this + 1):
        txt = _text(MCACHE / f"treasury_{kind}_{y}.csv", TREASURY.format(y=y, t=kind), offline,
                    12 if y == this else 24 * 30)
        for row in csv.DictReader(io.StringIO(txt)):
            if row.get(col):
                m, d, yy = row["Date"].split("/")
                out[dt.date(int(yy), int(m), int(d))] = float(row[col])
    return out


def unemployment(offline):
    raw = json.loads(_text(MCACHE / "bls_unrate.json", BLS.format(s=UNRATE), offline))
    if raw.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS {UNRATE}: {raw.get('message')}")
    out = {}
    for r in raw["Results"]["series"][0]["data"]:
        if r["period"].startswith("M") and r["period"] != "M13":
            try:
                out[(int(r["year"]), int(r["period"][1:]))] = float(r["value"])
            except ValueError:
                pass  # 2025-10 因政府停擺沒有公布
    return out


# ---------- 計算 ----------

def back(ym, n):
    t = ym[0] * 12 + ym[1] - 1 - n
    return t // 12, t % 12 + 1


def sahm(u):
    """失業率 3 個月均值，減去前 12 個月裡最低的 3 個月均值。窗內缺月就用有的月份平均。"""
    def avg3(ym):
        vals = [u[k] for k in (back(ym, i) for i in range(3)) if k in u]
        return sum(vals) / len(vals) if vals else None
    last = max(u)
    cur = avg3(last)
    low = min(a for a in (avg3(back(last, n)) for n in range(1, 13)) if a is not None)
    return last, cur, low, cur - low


def at(series, day):
    """day 當天或之前最近一筆。"""
    ks = [d for d in series if d <= day]
    return (max(ks), series[max(ks)]) if ks else (None, None)


def window(series, end, days=365):
    return {d: v for d, v in series.items() if end - dt.timedelta(days=days) < d <= end}


def rel_returns(a, b):
    """a 相對 b 的報酬（價格比的變化），回傳最後日期與各期間結果。"""
    ds = sorted(set(a) & set(b))
    r = np.array([a[d] / b[d] for d in ds])
    return ds[-1], {h: r[-1] / r[-1 - h] - 1 for h in HORIZONS if len(r) > h}


def fomc_state(cfg, today):
    rows = sorted(cfg["fomc"], key=lambda r: r["date"])
    since = today - dt.timedelta(days=183)
    recent = [r for r in rows if dt.date.fromisoformat(r["date"]) >= since]
    return rows, sum(r["action"] == "hike" for r in recent), sum(r["action"] == "cut" for r in recent)


# ---------- 報告 ----------

ACTION = {"hike": "升息", "cut": "降息", "hold": "按兵不動"}


def sp(x):
    return "—" if x is None else f"{x:+.1%}"


def state(hit):
    return "**觸發**" if hit else "未觸發"


def build(offline):
    cfg = json.loads(CONFIG.read_text())
    sig = cfg["signals"]
    today = dt.date.today()

    y2, y10 = treasury(NOMINAL, "2 Yr", offline), treasury(NOMINAL, "10 Yr", offline)
    r10 = treasury(REAL, "10 YR", offline)
    u = unemployment(offline)
    fx = _finmind("TaiwanExchangeRate", "USD", offline)
    etf = {t: _yahoo(t, offline) for t in ("HYG", "IEI", "LQD", "IEF")}

    rows, hikes, cuts = fomc_state(cfg, today)
    cur = rows[-1]
    mid = (cur["low"] + cur["high"]) / 2

    d10, v10 = at(y10, today)
    d2, v2 = at(y2, today)
    dr, vr = at(r10, today)
    w10 = window(y10, d10)
    hi10_d = max(w10, key=w10.get)

    dfx, vfx = at(fx, today)
    fx_cfg = sig["usdtwd"]
    eps_fx = (vfx / fx_cfg["eps_fx_base"] - 1) * fx_cfg["eps_sensitivity"]
    _, fx_1y = at(fx, dfx - dt.timedelta(days=365))

    d_hy, hy = rel_returns(etf["HYG"], etf["IEI"])
    _, ig = rel_returns(etf["LQD"], etf["IEF"])
    ym, u3, u_low, s = sahm(u)

    hits = {
        "fomc_hikes_6m": hikes >= sig["fomc_hikes_6m"]["threshold"],
        "us10y": v10 > sig["us10y"]["threshold"],
        "usdtwd": vfx < fx_cfg["threshold"],
        "hy_excess_3m": hy[63] < sig["hy_excess_3m"]["threshold"],
        "sahm": s >= sig["sahm"]["threshold"],
    }

    lines = [f"# 總經訊號：{today}", "",
             f"產生時間：{dt.datetime.now():%Y-%m-%d %H:%M}。資料日期：美債 {d10}（財政部）、實質殖利率 {dr}、"
             f"USD/TWD {dfx}（FinMind 台銀中價）、ETF {d_hy}（Yahoo）、失業率 {ym[0]}-{ym[1]:02d}（BLS）、"
             f"FOMC 決議 {cur['date']}（`data/macro.json`）。", "",
             f"## 燈號（{sum(hits.values())}／{len(hits)} 項觸發）", "",
             "| 指標 | 目前 | 觸發條件 | 狀態 | 觸發時的模型動作 |", "|---|---|---|---|---|"]


    def row(name, now, key, gap):
        st = state(hits[key]) + ("" if hits[key] else f"，{gap}")
        lines.append(f"| {name} | {now} | {sig[key]['rule']} | {st} | {sig[key]['action']} |")

    th10, th_hy, th_s = sig["us10y"]["threshold"], sig["hy_excess_3m"]["threshold"], sig["sahm"]["threshold"]
    row("FOMC", f"{cur['low']:.2f}–{cur['high']:.2f}%（{cur['date']} {ACTION[cur['action']]}）；"
        f"近 6 個月升息 {hikes} 次、降息 {cuts} 次", "fomc_hikes_6m",
        f"再升息 {sig['fomc_hikes_6m']['threshold'] - hikes} 次觸發")
    row("美 10 年期殖利率", f"{v10:.2f}%（1 年高點 {w10[hi10_d]:.2f}%，{hi10_d}）", "us10y",
        f"還差 {(th10 - v10) * 100:.0f}bp")
    row("USD/TWD", f"{vfx:.1f}（1 年前 {fx_1y:.1f}）；相對 EPS 假設匯率 {fx_cfg['eps_fx_base']:.0f}，"
        f"EPS 影響 {sp(eps_fx)}", "usdtwd", f"台幣再升值 {1 - fx_cfg['threshold'] / vfx:.1%} 觸發")
    row("高收益信用利差（代理）", f"HYG 相對 IEI 3 個月 {sp(hy[63])}", "hy_excess_3m",
        f"還差 {(hy[63] - th_hy) * 100:.1f} 個百分點")
    row("Sahm 規則", f"{s:+.2f}（{ym[0]}-{ym[1]:02d}；3 個月均值 {u3:.2f}%，前 12 個月低點 {u_low:.2f}%）", "sahm",
        f"還差 {th_s - s:.2f}")

    # 殖利率
    def pct(v):
        return "—" if v is None else f"{v:.2f}%"

    def yrow(name, ser):
        d = max(ser)
        w = window(ser, d)
        _, v3 = at(ser, d - dt.timedelta(days=91))
        _, v12 = at(ser, d - dt.timedelta(days=365))
        lines.append(f"| {name} | {pct(ser[d])} | {pct(v3)} | {pct(v12)} | {pct(max(w.values()))} | {pct(min(w.values()))} |")

    curve = {d: y10[d] - y2[d] for d in y10 if d in y2}
    gap = v2 - mid
    view = "市場預期再升息" if gap > 0.25 else "市場預期降息" if gap < -0.25 else "市場預期大致持平"
    note = cfg["market_note"]
    lines += ["", "## 殖利率與政策利率（財政部）", "",
              "| 項目 | 最新 | 3 個月前 | 1 年前 | 1 年高 | 1 年低 |", "|---|---|---|---|---|---|"]
    yrow("美 2 年期", y2)
    yrow("美 10 年期", y10)
    yrow("美 10 年期實質（TIPS）", r10)
    yrow("10 年 − 2 年", curve)
    lines += ["",
              f"- 政策利率中值 {mid:.3f}%；2 年期減政策利率中值 {gap * 100:+.0f}bp → {view}。這是粗略代理，沒有扣除期限溢酬。",
              f"- {note['text']}（[{note['quality']}] {note['date']}，{note['source']}）。",
              f"- 下次 FOMC：{cfg['next_fomc']}。"]

    # FOMC
    lines += ["", "## FOMC 決議（近 8 次，`data/macro.json`）", "",
              "| 日期 | 決議 | 目標區間 | 投票 | 品質 |", "|---|---|---|---|---|"]
    for r in rows[-8:]:
        lines.append(f"| {r['date']} | {ACTION[r['action']]} | {r['low']:.2f}–{r['high']:.2f}% | "
                     f"{r['vote'] or '—'} | [{r['quality']}]({r['source']}) |")

    # 信用利差代理
    lines += ["", "## 信用利差代理（ETF 相對報酬，Yahoo 還原價）", "",
              "| 組合 | 1 個月 | 3 個月 | 6 個月 | 說明 |", "|---|---|---|---|---|",
              f"| HYG 相對 IEI（高收益） | {sp(hy.get(21))} | {sp(hy.get(63))} | {sp(hy.get(126))} | "
              f"{sig['hy_excess_3m']['note']} |",
              f"| LQD 相對 IEF（投資級） | {sp(ig.get(21))} | {sp(ig.get(63))} | {sp(ig.get(126))} | "
              "存續期間相近（約 8 年對 7 年），−2% 約等於投資級利差擴大 25bp；只看方向，不設門檻 |"]

    # 失業率
    ms = sorted(u)[-6:]
    first, last = back(max(u), 14), max(u)
    missing = [f"{y}-{m:02d}" for y, m in (back(last, n) for n in range(15)) if (y, m) not in u and (y, m) >= first]
    lines += ["", "## 失業率（BLS，季調）", "",
              "| " + " | ".join(f"{y}-{m:02d}" for y, m in ms) + " |", "|" + "---|" * len(ms),
              "| " + " | ".join(f"{u[k]:.1f}%" for k in ms) + " |"]
    if missing:
        lines += ["", f"- {'、'.join(missing)} 沒有公布（2025 年政府停擺），Sahm 計算時該窗用其餘月份平均。"]

    lines += ["", "## 怎麼用", "",
              "- 觸發只代表要回頭檢查對應的假設，不會自動改配置。動作寫在 `data/macro.json`，改完 `portfolio/` 設定檔後重跑凱利。",
              "- 升息循環中，台積電和 BTC 都像長存續期的風險資產，2022 年兩者同年大跌。FOMC 和 Sahm 兩項是改用壓力相關係數的主要依據。",
              "- 這是公開 repo：USD/TWD 只列四捨五入值與變化，ETF 只列相對報酬，不放 FinMind 和 Yahoo 的原始序列。", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    report = build(args.offline)
    if args.out:
        pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.out).write_text(report)
        print(f"已寫入 {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
