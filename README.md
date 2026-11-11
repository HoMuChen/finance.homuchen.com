# AI CapEx 合理性追蹤與凱利配置工具

追蹤 AI 基礎設施投資能否被真實付費需求吸收，並用情境加權的多資產凱利公式評估台積電與 BTC 的配置比例。

> 本 repo 為個人研究筆記，資料可能有誤或過時，**不構成投資建議**。

## 研究框架

把 AI 產業拆成三層因果鏈，每季更新：

```
第三層 終端需求 ──付費──▶ 第二層 模型公司 ──採購算力──▶ 第一層 基礎設施（雲端 / NVIDIA / 台積電）
```

三個核心比率：

| 指標 | 定義 | 回答的問題 |
|---|---|---|
| A | 模型公司營收 ÷ 運算成本 | 商業化效率有沒有改善？ |
| B | Δ 年化雲端營收 ÷ Δ 年度 CapEx | 新增投資能不能轉成新增收入？ |
| C | NVIDIA 資料中心營收 ÷ 台積電 HPC 營收 | 需求有沒有傳導到晶圓端？ |

## 檔案結構

| 路徑 | 內容 |
|---|---|
| `00_研究規劃.md` | 要收集的資料、欄位與資料品質標記 |
| `01_總結儀表板.md` | 核心比率、情境判讀、更新時程、台積電 EPS 情境、見頂檢查清單 |
| `02_配置決策紀錄.md` | 每次評估的配置比例、判斷前提、情境假設、凱利結果（只記比例，不記金額） |
| `data/` | 各層原始資料，每筆標註 [官方]／[報導]／[估計] 與來源 |
| `portfolio/<日期>.json` | 凱利工具的輸入：配置比例、決策價格、情境與機率 |
| `reports/<日期>.md` | 凱利工具的輸出 |
| `tools/kelly.py` | 凱利配置重算工具 |
| `tools/margin_signal.py` | 大盤融資維持率低檔加碼輔助訊號 |
| `reports/margin-<日期>.md` | 融資維持率訊號的輸出 |
| `tools/r2.py` | 唯讀連線 fire-auto 的台股 R2 資料湖 |
| `tools/eps_nowcast.py` | 月營收 → 當季 EPS 即時推估（台積電、聯發科） |
| `data/eps_guidance.json` | `eps_nowcast.py` 的輸入：財測、R2 還沒收錄的已公布季度 |
| `data/tw_monthly_revenue.csv` | 台積電、聯發科官方月營收（公開資訊觀測站，`eps_nowcast.py` 自動補） |
| `reports/eps-nowcast-<日期>.md` | 當季 EPS 推估的輸出 |
| `tools/supply_chain.py` | 台灣 AI 供應鏈月營收旁證：每月監測與領先落後檢驗 |
| `reports/supply-chain-<日期>.md`、`reports/supply-chain-leadlag-<日期>.md` | 供應鏈監測與檢驗的輸出 |
| `tools/inventory_cycle.py` | 台灣電子業存貨周轉天數年增（見頂檢查清單第 5 項的台灣旁證） |
| `reports/inventory-<日期>.md` | 庫存循環的輸出 |
| `tools/macro.py` | 總經訊號：FOMC、美債殖利率、USD/TWD、高收益利差代理、Sahm 規則；背景讀數非農就業、CPI 電價、美台利差 |
| `data/macro.json` | `macro.py` 的手動輸入：FOMC 與台灣央行決議、門檻、觸發時的模型動作 |
| `reports/macro-<日期>.md` | 總經訊號的輸出 |

## 凱利工具

依賴：Python 3 與 numpy。FinMind token 放在 `.env.local`（不進版控）：

```
FINMIND_TOKEN=<your token>
```

```bash
python3 tools/kelly.py portfolio/2026-10-20.json                         # 輸出到終端
python3 tools/kelly.py portfolio/2026-10-20.json --out reports/2026-10-20.md
python3 tools/kelly.py portfolio/2026-10-20.json --offline               # 只用快取價格
python3 tools/kelly.py portfolio/2026-10-20.json --amounts portfolio/private.json  # 差距以 NT$ 顯示
```

計算流程：

1. 抓 5 年日價格，快取在 `cache/prices/`：台股（還原股價）與 USD/TWD 匯率用 FinMind，FinMind 沒有的資產（如 BTC）用 Yahoo Finance。USD 資產換算成台幣。
2. 計算年化波動（日、週波動取較大者）與週報酬相關係數。
3. 依設定檔的情境（目標價 × 機率）計算一年期加權預期報酬。
4. 計算多資產分數凱利 f = k · Σ⁻¹(μ − r)，分別用實測相關與壓力相關，並和目前比例比較。
5. 敏感度：把最差情境機率調高 10 個百分點後重算。

`portfolio/private.json`（實際金額）已列入 `.gitignore`，不會進版控。格式：

```json
{"total_twd": 1000000}
```

## 融資維持率訊號

低檔加碼的輔助判斷，只輔助 `02_配置決策紀錄.md` 的 U6 加碼價，不放進凱利。規則與歷史表現見 `01_總結儀表板.md`。

```bash
python3 tools/margin_signal.py                                   # 輸出到終端
python3 tools/margin_signal.py --out reports/margin-2026-10-25.md
python3 tools/margin_signal.py --cycle-top                       # 見頂檢查清單已出現 2–3 項時，只認維持率 < 140
```

資料用 FinMind 2015 年起的大盤融資維持率、融資餘額、加權指數與報酬指數、台積電還原股價，快取在 `cache/prices/`。輸出包括目前燈號（< 150／145／140 三階）、粗估的觸發位置，以及歷史上每次首次跌破後的 20–250 日報酬。

**維持率只用 FinMind 的 `TaiwanTotalExchangeMarginMaintenance`**，不要和 R2 的 `market.mkt_maint` 混用（原因見下一節）。

## 當季 EPS 即時推估

每月 10 日前後月營收公布後跑一次，看季內營收進度有沒有偏離財測，以及當季 EPS 落在哪裡。

```bash
uv run -q --with duckdb python tools/eps_nowcast.py                                      # 輸出到終端
uv run -q --with duckdb python tools/eps_nowcast.py --out reports/eps-nowcast-2026-11-10.md
uv run -q --with duckdb python tools/eps_nowcast.py --ids 2330
```

- 月營收與單季財報讀 R2（`tw.revenue`、`tw.fin`）。R2 常常整批月營收進來了，個別公司卻晚幾天才有（例如 2026-10 的台積電、聯發科）；這時最新月份會改用 MOPS 官方金額計算，報告會註明。財測和「法說已公布、R2 還沒收錄」的季度寫在 `data/eps_guidance.json`，每季法說後更新。R2 的財報在法定截止日後才會有（Q1 5/16、Q2 8/15、Q3 11/15、Q4 次年 4/1）。
- 兩種推估：
  - **A 上季淨利率法**：上季 EPS ×（本季營收 ÷ 上季營收）。
  - **B 財測營益率法**：本季營收 × 財測營益率中值 ×（上季淨利 ÷ 上季營業利益）÷ 股數。沒有營益率財測時，用毛利率減費用率。
- 季內營收還沒到齊時，本季營收用財測中值，同時列出：
  - 季內進度。
  - 剩下月份的月營收要比已公布月均高或低多少，才達得到財測。
  - 月均外推的對照值。
- 報告也列出 A 法過去 12 季的誤差（代入實際季營收）。營收大幅跳升、費用率下降的季度（例如聯發科 2026Q4），A 法會低估，要看 B 法。
- 月營收金額只用公開資訊觀測站「上市公司每月營業收入彙總表」的官方數字，存在 `data/tw_monthly_revenue.csv`（單位千元，標 [官方] 與來源網址）。
  - 缺的月份會自動從 MOPS 抓，原始頁面快取在 `cache/mops/`；`--offline` 不抓。
  - 年增、月增和推估仍由 R2 計算，並逐月和官方金額比對，不一致會在報告裡警告。
  - FinMind 的數字不會出現在報告裡。

## 供應鏈月營收旁證

```bash
uv run -q --with duckdb python tools/supply_chain.py                                       # 每月監測
uv run -q --with duckdb python tools/supply_chain.py --out reports/supply-chain-2026-11-10.md
uv run -q --with duckdb python tools/supply_chain.py leadlag                               # 領先落後檢驗（全部候選）
```

- 每月監測只留兩組：
  - 下游組裝（廣達、緯創、緯穎、鴻海）：雲端 CapEx 的月頻代理。
  - 弘塑：台積電 CapEx 執行的旁證。
- R2 缺個別公司的最新月份時，同樣用 MOPS 月營收彙總表補（上市、上櫃分開抓），報告底下會註明；`--offline` 只用本機快取。
- `leadlag` 會重跑全部 12 家候選，四大雲季報後可以累積樣本重新檢查。
- 剔除原因和判斷標準見 `data/L1_nvidia_tsmc.md` 第 11 節。結論是沒有一家領先台積電月營收。

## 總經訊號

每月美國就業報告公布後（第一個週五之後）跑一次，每次 FOMC 會後也跑一次。只追會改動模型參數的指標，判讀見 `01_總結儀表板.md`「總經訊號」一節。

```bash
python3 tools/macro.py                                  # 輸出到終端
python3 tools/macro.py --out reports/macro-2026-11-03.md
python3 tools/macro.py --offline                        # 只用快取
```

| 指標 | 資料源 | 報告裡列什麼 |
|---|---|---|
| 美 2 年期、10 年期名目與實質殖利率 | 美國財政部 Daily Treasury Par Yield Curve | 數字（公有領域） |
| 失業率 → Sahm 規則 | BLS `LNS14000000` | 數字（公有領域） |
| CPI 電價、整體 CPI（背景，不設門檻） | BLS `CUUR0000SEHF01`、`CUUR0000SA0`，未季調年增 | 數字（公有領域） |
| USD/TWD | FinMind 台銀即期中價 | 只列四捨五入到 0.1 的水準與變化 |
| 高收益、投資級信用利差代理 | Yahoo Finance：HYG／IEI、LQD／IEF 還原價 | 只列相對報酬 |
| FOMC 決議 | `data/macro.json`（手動，來源是 Fed 聲明） | 數字與連結 |
| 台灣央行重貼現率 | `data/macro.json` 的 `cbc`（手動，來源是報導；央行官網新聞稿可補） | 數字與連結 |

- 每次 FOMC 會後，在 `data/macro.json` 的 `fomc` 補一筆，並更新 `next_fomc` 和 `market_note`。台灣央行理監事會（每季）會後在 `cbc` 補一筆，並更新 `next_cbc`。
- 門檻（`signals.*.threshold`）和觸發時的模型動作（`signals.*.action`）都在同一個檔案。觸發只代表要回頭檢查對應的假設，不會自動改 `portfolio/` 設定檔。
- 這台機器連不上 FRED，所以信用利差用 ETF 相對報酬代替 ICE BofA OAS，只能看量級。
- 快取在 `cache/macro/`（財政部、BLS）與 `cache/prices/`（FinMind、Yahoo）。

## 庫存循環

每季財報截止日（5/16、8/15、11/15、次年 4/1）之後跑一次。

```bash
uv run -q --with duckdb python tools/inventory_cycle.py                                   # 輸出到終端
uv run -q --with duckdb python tools/inventory_cycle.py --out reports/inventory-2026-11-10.md
uv run -q --with duckdb python tools/inventory_cycle.py --threshold 10                    # 改門檻看敏感度
```

- 存貨周轉天數 = 平均存貨（期初＋期末）÷ 單季營業成本 × 91，讀 R2 的 `tw.bs`、`tw.fin`，時間點用 `avail_date`。
- 組別：半導體 ex-台積電（燈號）、非半導體電子業、台積電（對照）。合計只加總當季與去年同季都有資料的公司，和去年同季比。
- 燈號：半導體 ex-台積電天數年增 > +6 天。某季公司數不到前 4 季最多的 90%，標「未到齊」，不算燈號。
- 報告另列訊號開始後的加權指數表現、存貨增加最多的公司，和觀察名單（記憶體模組廠、ASIC 廠、PC 品牌）。不放存貨原始金額。
- 判讀與限制見 `01_總結儀表板.md` 見頂檢查清單第 5 項補充。

## R2 台股資料湖（fire-auto）

fire-auto 每個交易日 00:30 更新前一個交易日的資料，發布成 DuckDB catalog：`r2://trading-homuchen-com/v1/catalog.duckdb`。資料源是 FinMind，**僅限個人使用**：報告裡列出 FinMind 的數字沒關係（2026-11-03 決定）。

金鑰放 `.env.local`：`R2_ACCOUNT_ID`，加上 `R2_READ_ACCESS_KEY_ID`／`R2_READ_SECRET_ACCESS_KEY`（沒有就讀 `R2_WRITE_*`）。一律唯讀掛載。本機不用另外裝 duckdb：

```bash
uv run -q --with duckdb python tools/r2.py                     # 列出所有表與說明
uv run -q --with duckdb python tools/r2.py "DESCRIBE tw.price"
uv run -q --with duckdb python tools/r2.py "SELECT date, close FROM tw.price WHERE stock_id = '2330' ORDER BY date DESC LIMIT 5"
```

程式裡用 `from r2 import connect; con = connect()`，再用 `con.sql(...)` 查詢。

主要的表：`tw.universe`（含下市股）、`tw.price`（原始價與還原價 `adj_*`）、`tw.revenue`、`tw.fin`／`bs`／`cf`、`tw.inst`、`tw.margin`、`tw.sbl`（借券賣出餘額，單位股）、`tw.per`、`tw.holding`、`tw.broker`（只有 1,439 檔）、`tw.orderbook.*`，以及 `tw.market.*`（加權指數、報酬指數、台指期、選擇權、自建台指 VIX、市場寬度 `breadth`、自建維持率 `mkt_maint`）。

注意事項：

- **防前視**：財報和營收用 `avail_date` 對齊，不要用 `date`；股票池要用含下市股的 point-in-time 版本。最近 10 天的日資料和最新 3 季財報會被覆蓋修正。
- **`tw.revenue` 的 `date` 是公布月份**：`date = 2026-10-01` 是 9 月營收。要看營收月份用 `revenue_month`／`revenue_year`。
- 查 `broker`、`orderbook` 一定要帶 `date`／`day` 條件，否則會掃過全部 2 千多個檔。
- **`market.mkt_maint` 是 fire-auto 自建的維持率**：Σ（個股融資張數 × 1000 × 收盤價）÷ 上市融資總金額，包含上市 ETF、存託憑證、特別股，不含融券擔保品與保證金。它和 FinMind 序列的相關係數 0.976，低點日期相同，但差距會隨時間漂移：2015 年 R2 高約 3 點，2023 年後 R2 低 2.5–4 點（2026-10 約低 4 點）。`margin_signal.py` 的門檻是用 FinMind 序列校準的，所以燈號只看 FinMind；要改用 R2，門檻得用 R2 自己的歷史重新回測。

## 每季更新流程

1. 財報或法說後更新 `data/` 與 `01_總結儀表板.md`。
2. 複製 `portfolio/` 最新的設定檔，改成新日期，更新比例、價格與情境機率。
3. 執行 `tools/kelly.py` 產生新報告。
4. 在 `02_配置決策紀錄.md` 新增一筆紀錄，不覆蓋舊紀錄。
