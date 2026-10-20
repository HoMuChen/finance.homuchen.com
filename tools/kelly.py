"""季度配置重算工具：抓價格 → 算波動與相關係數 → 依情境算預期報酬 → 多資產凱利。

用法：
    python3 tools/kelly.py portfolio/2026-10-20.json              # 輸出到終端
    python3 tools/kelly.py portfolio/2026-10-20.json --out reports/2026-10-20.md
    python3 tools/kelly.py portfolio/2026-10-20.json --offline    # 只用快取價格
    python3 tools/kelly.py portfolio/2026-10-20.json --amounts portfolio/private.json  # 差距以 NT$ 顯示，僅輸出到終端

設定檔只放比例（weight）；實際金額放 portfolio/private.json（不進 git）。

只依賴標準函式庫與 numpy。價格快取在 cache/prices/（不進 git）。
"""

import argparse
import datetime as dt
import json
import pathlib
import time
import urllib.request

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache" / "prices"
FX_TICKER = "TWD=X"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5y&interval=1d"


# ---------- 價格 ----------

def fetch(ticker, offline=False, max_age_h=12):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{ticker}.json"
    fresh = path.exists() and time.time() - path.stat().st_mtime < max_age_h * 3600
    if not offline and not fresh:
        req = urllib.request.Request(YAHOO.format(t=ticker), headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            path.write_bytes(r.read())
    res = json.loads(path.read_text())["chart"]["result"][0]
    ind = res["indicators"]
    closes = ind["adjclose"][0]["adjclose"] if "adjclose" in ind else ind["quote"][0]["close"]
    tz = dt.timedelta(seconds=res["meta"].get("gmtoffset", 0))
    out = {}
    for ts, p in zip(res["timestamp"], closes):
        if p is not None:
            out[(dt.datetime.fromtimestamp(ts, dt.timezone.utc) + tz).date()] = p
    return out


def weekly(series):
    """每週最後一個交易日（週一到週五）收盤。日報酬會因台股與 BTC 收盤時間不同步而低估相關性。"""
    w = {}
    for d in sorted(series):
        if d.weekday() <= 4:
            w[d.isocalendar()[:2]] = series[d]
    return w


def to_twd(series, fx):
    return {d: p * fx[d] for d, p in series.items() if d in fx}


# ---------- 統計 ----------

def weekly_log_returns(weeklies, years):
    cutoff = (dt.date.today() - dt.timedelta(days=365 * years)).isocalendar()[:2]
    keys = sorted(set.intersection(*(set(w) for w in weeklies)))
    keys = [k for k in keys if k >= cutoff]
    m = np.array([[w[k] for k in keys] for w in weeklies])
    return np.diff(np.log(m), axis=1)


def daily_vol(series, years):
    cutoff = dt.date.today() - dt.timedelta(days=365 * years)
    v = np.array([series[d] for d in sorted(series) if d >= cutoff and d.weekday() <= 4])
    return float(np.diff(np.log(v)).std(ddof=1) * np.sqrt(252))


def scenario_stats(asset):
    probs = np.array([s["prob"] for s in asset["scenarios"]])
    if abs(probs.sum() - 1) > 1e-6:
        raise ValueError(f"{asset['name']} 情境機率加總 {probs.sum():.3f} ≠ 1")
    prices = np.array([s["price"] for s in asset["scenarios"]])
    rets = prices / asset["price"] - 1 + asset.get("income_12m", 0) / asset["price"]
    return float(probs @ rets), probs, rets


def kelly(mu, vols, rho_mat, rf, fraction):
    cov = np.outer(vols, vols) * rho_mat
    return np.linalg.solve(cov, mu - rf) * fraction


def with_rho(rho_mat, rho):
    m = np.full_like(rho_mat, rho)
    np.fill_diagonal(m, 1.0)
    return m


# ---------- 報告 ----------

def pct(x):
    return f"{x:+.1%}" if x < 0 else f"{x:.1%}"


def twd(x):
    return f"{x:+,.0f}"


def build(cfg, offline, total_twd=None):
    assets = cfg["assets"]
    names = [a["name"] for a in assets]
    fx = fetch(FX_TICKER, offline)
    series = {}
    for a in assets:
        s = fetch(a["ticker"], offline)
        series[a["name"]] = to_twd(s, fx) if a["currency"] == "USD" else s
    weeklies = [weekly(series[n]) for n in names]

    lines = [f"# 凱利配置重算：{cfg['as_of']}", "",
             f"產生時間：{dt.datetime.now():%Y-%m-%d %H:%M}，設定檔情境以 `as_of` 當日的決策價格為準。", ""]

    # 市價對照
    lines += ["## 價格", "", "| 資產 | 設定檔價格 | 最新市價 | 差異 |", "|---|---|---|---|"]
    for a in assets:
        raw = fetch(a["ticker"], offline=True)
        last = raw[max(raw)]
        lines.append(f"| {a['name']} | {a['price']:,} | {last:,.0f}（{max(raw)}） | {pct(last / a['price'] - 1)} |")
    lines.append("")

    # 波動與相關
    lines += ["## 波動與相關係數（USD 資產換算台幣；相關係數用週報酬）", "",
              "| 期間 | " + " | ".join(f"{n} 波動 日／週" for n in names) + " | 相關係數 |",
              "|---|" + "---|" * (len(names) + 1)]
    stats = {}
    for y in (1, 2, 3, 5):
        r = weekly_log_returns(weeklies, y)
        wv = r.std(axis=1, ddof=1) * np.sqrt(52)
        dv = np.array([daily_vol(series[n], y) for n in names])
        rho = np.corrcoef(r)
        stats[y] = {"daily": dv, "weekly": wv, "max": np.maximum(dv, wv), "rho": rho}
        off = ", ".join(f"{rho[i, j]:+.2f}" for i in range(len(names)) for j in range(i + 1, len(names)))
        lines.append(f"| {y} 年（n={r.shape[1]} 週） | " + " | ".join(f"{d:.0%}／{w:.0%}" for d, w in zip(dv, wv)) + f" | {off} |")
    lines.append("")

    # 情境
    mus = []
    for a in assets:
        mu, probs, rets = scenario_stats(a)
        mus.append(mu)
        lines += [f"## {a['name']} 情境（決策價 {a['price']:,}）", "",
                  "| 情境 | 價格 | 報酬 | 機率 | 依據 |", "|---|---|---|---|---|"]
        for s, r in zip(a["scenarios"], rets):
            lines.append(f"| {s['name']} | {s['price']:,} | {pct(r)} | {s['prob']:.0%} | {s.get('basis', '')} |")
        lines += [f"| **加權預期報酬** | | **{pct(mu)}** | | {a.get('income_note', '')} |", ""]
    mus = np.array(mus)

    # 凱利
    rf, frac = cfg["risk_free"], cfg["kelly_fraction"]
    st_vol = stats[cfg["vol_window_years"]]
    vols = st_vol[cfg.get("vol_method", "max")]
    if cfg.get("vol_override"):
        vols = np.array([cfg["vol_override"].get(n, v) for n, v in zip(names, vols)])
    rho = stats[cfg["rho_window_years"]]["rho"]
    current = np.array([a["weight"] for a in assets])
    if abs(current.sum() + cfg["cash_like_weight"] - 1) > 1e-3:
        raise ValueError("資產 weight 加 cash_like_weight 應等於 1")
    lines_vol = [f"使用波動：" + "、".join(f"{n} {v:.0%}" for n, v in zip(names, vols))
              + f"（{cfg['vol_window_years']} 年，方法 {cfg.get('vol_method', 'max')}）；"
              + f"相關係數取 {cfg['rho_window_years']} 年週報酬。", ""]
    cases = [
        (f"實測相關（{cfg['rho_window_years']} 年）", rho),
        (f"壓力相關 {cfg['stress_rho']}", with_rho(rho, cfg["stress_rho"])),
    ]
    lines += [f"## 凱利建議（{frac:g}× 凱利，無風險利率 {rf:.1%}）", ""] + lines_vol + [
              "| 假設 | " + " | ".join(names) + " | 高風險合計 |", "|---|" + "---|" * (len(names) + 1)]
    results = {}
    for label, rm in cases:
        f = kelly(mus, vols, rm, rf, frac)
        results[label] = f
        lines.append(f"| {label} | " + " | ".join(f"{x:.0%}" for x in f) + f" | {f.sum():.0%} |")
    lines.append("| **目前** | " + " | ".join(f"**{x:.0%}**" for x in current) + f" | **{current.sum():.0%}** |")
    unit, scale = ("NT$", total_twd) if total_twd else ("百分點", 100)
    lines += ["", f"### 與目前部位的差距（{unit}，正值＝模型建議加碼）", "",
              "| 假設 | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for label, f in results.items():
        lines.append(f"| {label} | " + " | ".join(twd((x - c) * scale) for x, c in zip(f, current)) + " |")
    lines.append("")

    # 敏感度：把最差情境機率往上調，從基本情境移過去
    lines += ["## 敏感度：最差情境機率 +10 個百分點（自基本情境移入）", "",
              "| 調整資產 | 該資產預期報酬 | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
    for i, a in enumerate(assets):
        _, probs, rets = scenario_stats(a)
        p = probs.copy()
        worst, base = int(np.argmin(rets)), int(np.argmax(probs))
        shift = min(0.10, p[base])
        p[worst] += shift
        p[base] -= shift
        m = mus.copy()
        m[i] = float(p @ rets)
        f = kelly(m, vols, rho, rf, frac)
        lines.append(f"| {a['name']} | {pct(m[i])} | " + " | ".join(f"{x:.0%}" for x in f) + " |")
    lines += ["", "> 凱利只放大輸入的判斷。預期報酬差 1 個百分點，比例可差 10–40 個百分點；以上僅為上限參考，非投資建議。", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--amounts", help="不進 git 的金額檔（含 total_twd），提供時差距改以 NT$ 顯示；輸出請勿 commit")
    args = ap.parse_args()
    cfg = json.loads(pathlib.Path(args.config).read_text())
    total = json.loads(pathlib.Path(args.amounts).read_text())["total_twd"] if args.amounts else None
    report = build(cfg, args.offline, total)
    if args.out:
        pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.out).write_text(report)
        print(f"已寫入 {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
