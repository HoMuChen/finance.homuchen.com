# L3 終端需求與價格（Token 用量、API 價格、付費用戶、企業採用）

> 建立日期：2026-10-19（資料截至 2026-10-18 左右）
> 對應框架：第五組「價格與使用量」+ 第三層終端需求
> 標記：**[官方]** 財報／SEC／公司正式揭露；**[報導:媒體]** 媒體引述；**[估計:機構]** 分析師／研究機構估算；**[二手]** 僅見於聚合站／部落格，可信度低，待驗證
> 原則：查不到寫「查不到」；矛盾數字並列，不擇一。

---

## 1. Token 用量時間序列

### 1.1 Google（全產品表面「每月處理 token 數」）

| 時間 | 數值 | 口徑 | 標記 | 來源 |
|---|---|---|---|---|
| 2024-05（I/O 2024） | 9.7 兆／月 | 全產品表面 | [官方]（I/O 2026 主題演講回溯） | https://blog.google/innovation-and-ai/sundar-pichai-io-2026/ |
| 2025-05（I/O 2025） | 480 兆／月 | 全產品表面 | [官方] | https://x.com/Google/status/2056783102085640252 |
| 2025-07（Q2'25 財報） | 980 兆／月 | 全產品表面（「doubling since May」） | [官方] | https://www.aol.com/finance/alphabet-googl-q2-2025-earnings-214332197.html |
| 2025-10（Q3'25 財報） | >1.3 千兆（quadrillion）／月 | 全產品表面，「年增 >20x」 | [官方] | https://s206.q4cdn.com/479360582/files/doc_events/2025/Oct/29/2025_Q3_Earnings_Transcript.pdf |
| 2026-05-19（I/O 2026） | >3.2 千兆／月 | 全產品表面，年增約 7x | [官方] | https://x.com/Google/status/2056783102085640252 ；https://www.shacknews.com/article/149205/google-3-2-quadrillion-monthly-ai-tokens |
| 2026-07 之後 | 查不到更新的「全表面」月 token 數 | — | — | Q3'26 財報預計 10 月底發布，屆時更新 |

> 注意：此口徑含 AI Overviews 等免費表面，**不等於付費需求**。另有評論指 2025 年中至年底的月增量放緩約 57%（Tom Tunguz，經 Wing VC 轉引）[估計:Tunguz] https://www.wing.vc/content/who-makes-money-when-inference-gets-10x-cheaper

### 1.2 Google（客戶直接 API 用量，每分鐘 token）— 較接近付費需求

| 季度（發布日） | 每分鐘 API token | 季增 | 標記 | 來源 |
|---|---|---|---|---|
| Q3'25（2025-10-29） | 70 億 | — | [官方] | https://s206.q4cdn.com/479360582/files/doc_events/2025/Oct/29/2025_Q3_Earnings_Transcript.pdf |
| Q4'25（2026-02-04） | >100 億 | +43% | [官方] | https://s206.q4cdn.com/479360582/files/doc_events/2026/Feb/04/2025_Q4_Earnings_Transcript.pdf |
| Q1'26（2026-04-29） | >160 億 | +60% | [官方] | https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000043/googexhibit991q12026.htm |
| Q2'26（2026-07-22） | 220 億 | +38% | [官方] | https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm |

> 換算：220 億/分 × 60 × 24 × 30 ≈ **950 兆／月**（僅 API）。有二手來源寫成「1 quadrillion／月」，係四捨五入。一年內（Q3'25→Q2'26）API 用量約 3.1x。

### 1.3 Microsoft（Azure AI Foundry）

| 時間 | 數值 | 標記 | 來源 |
|---|---|---|---|
| FY25 Q3（2025-04） | 單季處理 >100 兆 token，年增 5x；其中單月（3 月）50 兆 | [官方] | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY25Q3 |
| FY25 全年（2025-07 財報） | Foundry API 全年 >500 兆 token，年增 >7x | [官方] | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptQandAFY25q4 |
| FY26 Q2（2026-01） | >250 家客戶今年將處理 >1 兆 token | [官方] | https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2 |
| FY26 Q3（2026-04） | >300 家客戶將處理 >1 兆 token（季增 30%）；>10,000 客戶用 >1 個模型 | [官方] | https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3 ；https://licenseq.com/microsoft-fy26-q3-results-explained/ |
| FY26 Q4（2026-07-29） | 「年化 1 兆 token 的 Foundry 客戶數年增 4x」；Foundry 客戶 100,000 家、營收年增 >1 倍 | [官方]（逐字稿） | https://www.investing.com/news/transcripts/earnings-call-transcript-microsoft-q4-2026-beats-forecasts-stock-jumps-8-93CH-4822020 |
| FY26 總 token 量 | **查不到**：自 FY25 後微軟改揭露「客戶數」而非總 token 數 | — | — |

### 1.4 OpenRouter（第三方路由平台，公開度最高但規模小、偏開發者／程式）

| 時間 | 每週 token | 標記 | 來源 |
|---|---|---|---|
| 2024 年初 | 約 100 億／週 | [報導:CryptoBriefing] | https://cryptobriefing.com/openrouter-9000x-token-usage-growth/ |
| 2025-11 前後 | 約 5 兆／週 | [官方]（B 輪新聞稿回溯） | https://secure.businesswire.com/news/home/20260526953416/en/ |
| 2026-01 → 2026-07 | 約 7 兆 → >56 兆／週 | [估計:ARK Invest]（經二手轉引） | https://www.startuphub.ai/news/ai-token-demand-just-broke-its-forecast |
| 2026-05-26 | 約 25 兆／週（≈100 兆／月），6 個月 5x；>8M 用戶 | [官方] 新聞稿 | https://secure.businesswire.com/news/home/20260526953416/en/ |
| 2026 年中 | >90 兆／週 | [報導:CryptoBriefing] | https://cryptobriefing.com/openrouter-9000x-token-usage-growth/ |
| 2026-08-31～09-06 | 「115 quadrillion」（應為 115 兆之誤） | [二手:Octagon AI 預測市場頁] | https://www.octagonai.co/markets/science-and-technology/tokens/openrouter-ai-token-usage-in-september/ |
| 結構 | Agent 工作負載約占 71%（2026-08 初）；程式類由 ~11% 升至 >50%；中位 prompt 長度 ~1,500→>6,000 token | [報導]／[官方研究:OpenRouter×a16z 100T token 研究] | https://cryptobriefing.com/hermes-agent-1-5-trillion-tokens-openrouter/ ；https://www.wing.vc/content/who-makes-money-when-inference-gets-10x-cheaper |

> **矛盾**：5 月官方 25 兆／週 vs ARK「7 月 >56 兆」 vs CryptoBriefing「年中 >90 兆」——口徑（是否含免費模型、是否營收加權）不明。官方 rankings 頁（資料至 2026-10-18）未顯示總量，**最新官方總量查不到**。

### 1.5 OpenAI API

| 時間 | 數值 | 標記 | 來源 |
|---|---|---|---|
| 2025-10（DevDay 2025，Altman） | API 每分鐘約 60 億 token（兩年 20x） | [官方發言，經二手轉引] | https://www.longtermwiki.com/sourcing/fact/f_DJyrjvvvIg |
| 2025 年底 | 「>150 億 token／分」 | [二手:aiwiki]，與上筆矛盾 | https://aiwiki.ai/wiki/openai_api |
| 2026 | **查不到**官方更新 | — | — |

### 1.6 其他
- Deloitte 2026 研究：67% 企業每月消耗 >10 億 token [估計:Deloitte，經 OpenRouter 新聞稿引用] https://secure.businesswire.com/news/home/20260526953416/en/
- Anthropic 總 token 量：**查不到**公開數字。

---

## 2. 價格

### 2.1 旗艦模型每百萬 token 定價（標準層，美元；輸入/輸出）

**OpenAI**

| 模型 | 發布 | 輸入 | 輸出 | 混合價（3:1）* | 標記／來源 |
|---|---|---|---|---|---|
| GPT-4 (8k) | 2023-03 | 30 | 60 | 37.5 | [官方]上市價（Wing VC 整理） |
| GPT-4 Turbo | 2023-11 | 10 | 30 | 15 | [官方]上市價 |
| GPT-4o | 2024-05 | 5 | 15 | 7.5 | [官方]上市價 |
| GPT-4o (2024-08) | 2024-08 | 2.50 | 10 | 4.4 | [官方] 現行價目表 |
| GPT-4.1 | 2025-04 | 2 | 8 | 3.5 | [官方] |
| GPT-5 / 5.1 | 2025-08 / 2025-11 | 1.25 | 10 | 3.4 | [官方] |
| GPT-5.2 | 2025-12 | 1.75 | 14 | 4.8 | [官方] |
| GPT-5.4 | 2026-03 | 2.50 | 15 | 5.6 | [官方] |
| GPT-5.5 | 2026-04-23 | 5 | 30 | 11.3 | [官方]價；日期 [報導:Framia/Box] |
| GPT-5.6 Sol | 2026-07-09 | 上市 5 / 30（報導）；現行價目表 4 / 20 | — | 11.3→8 | **矛盾**：報導 $5/$30 vs 官方現行 $4/$20，調價日期查不到 |
| GPT-5.6 Terra / Luna | 2026-07-09；07-30 降價 | Terra 2.50/15→2/12；Luna 1/6→0.20/1.20 | — | — | [官方]現行價；降價 [報導:iClarified 等] https://www.iclarified.com/101633/openai-cuts-gpt56-luna-pricing-by-80-terra-by-20 |
| GPT-6 Astra（最高階） | 2026-09-03（報導） | 10 | 50 | 20 | [官方]價；>272K context 20/75 |
| GPT-6 Sol（主力） | 2026-09-22 | 2 | 10 | 4 | [官方]價；較 5.6 Sol 降 50% [報導:Yahoo Finance] https://finance.yahoo.com/technology/ai/articles/openai-cuts-gpt-6-sol-111351382.html |
| GPT-6 Luna（低價） | 2026-09-22 | 0.10 | 0.50 | 0.2 | [官方] |

官方價目表：https://developers.openai.com/api/docs/pricing （2026-10-19 擷取）

**Anthropic**

| 模型 | 發布 | 輸入 | 輸出 | 混合價（3:1） | 標記／來源 |
|---|---|---|---|---|---|
| Claude 3 Opus | 2024-03 | 15 | 75 | 30 | [官方]上市價（已不在現行表） |
| Claude Opus 4 / 4.1 | 2025-05 / 2025-08 | 15 | 75 | 30 | [官方] |
| Claude Opus 4.5 | 2025-11-24 | 5 | 25 | 10 | [官方]，較 4.1 降 67% |
| Claude Opus 4.6 / 4.7 / 4.8 | 2026-02-05 / 2026-04-16 / 查不到 | 5 | 25 | 10 | [官方]價；日期 [二手:OrcaRouter] |
| Claude Opus 5 | 2026-07-24（報導） | 5 | 25 | 10 | [官方]價 |
| Claude Opus 5.5 | 2026-09-22（報導） | 4 | 20 | 8 | [官方]價；Fast mode 8/40；Anthropic 稱預設設定下比 Opus 5 便宜 40%，獨立測試在 max effort 下無節省 [報導:metricnexus] |
| Claude Fable 5 / 5.1、Mythos 5 / 5.1（最高階，Mythos 限量） | 查不到確切日期 | 10 | 50 | 20 | [官方] |
| Sonnet 系列 | 3.5→4.6 維持 3/15；Sonnet 5 / 5.5 | 3→2 | 15→10 | 6.75→4 | [官方] |
| Haiku 4.5 → Haiku 5.5 | — | 1 → 0.10（≤100K） | 5 → 0.50 | — | [官方] |

官方價目表：https://platform.claude.com/docs/en/docs/about-claude/pricing （2026-10-19 擷取）

**Google Gemini**

| 模型 | 發布 | 輸入 | 輸出 | 混合價（3:1） | 標記／來源 |
|---|---|---|---|---|---|
| Gemini 1.5 Pro | 2024-05 | 3.50 | 10.50 | 5.25 | [官方]上市價（≤128K），2024-10 降至 1.25/5 |
| Gemini 2.5 Pro | 2025 | 1.25（≤200K）/2.50 | 10 / 15 | 3.4 | [官方] |
| Gemini 3.1 Pro Preview | 2026 | 2（≤200K）/4 | 12 / 18 | 4.5 | [官方] |
| Gemini 4 Argon | 2026-10（報導 10-04 或 10-11） | 2 → **2026-12-01 起 4** | 10 → **20** | 4 → 8 | [官方] 價目表明列漲價 |
| Gemini 3.6 / 3.8 Flash | 2026 | 0.75 → **2027-01-01 起 1.50** | 3.75 → **7.50** | — | [官方] 價目表明列漲價 |
| Gemini 2.5 Flash-Lite / 3.5 Flash-Lite | — | 0.10 / 0.30 | 0.40 / 2.50 | — | [官方] |

官方價目表：https://ai.google.dev/gemini-api/docs/pricing （2026-10-19 擷取）

\* 混合價 = (3×輸入 + 輸出)/4，為本檔自行計算，便於比較；未計快取折扣（各家快取讀取約 1 折）。

**重點觀察**
1. 「同一檔位」價格持續下降：OpenAI 主力檔 GPT-4 $37.5 → GPT-6 Sol $4（3.5 年約 -89%）；Anthropic Opus 檔 $30 → $8（-73%）。
2. 但 **2026 年出現「更高一檔」並回漲**：GPT-5.5（$11.3）、GPT-6 Astra（$20）、Claude Fable/Mythos（$20）——前沿能力的定價不再單向下跌。Wing VC：旗艦價 $30 → $1.25 → 回到約 $5（GPT-5.5）。
3. **Google 首度在官方價目表公告漲價**（Gemini 4 Argon 12 月翻倍、Flash 系列 2027-01 翻倍），原價被定位為「促銷期」——可能反映算力供給吃緊或補貼退場，是需重點追蹤的訊號。
4. 每 token 價格 ≠ 每任務成本：Artificial Analysis 測得完成 Intelligence Index 每任務成本 GPT-5.6 Sol $1.04、Claude Opus 5 $2.03、Claude Fable 5 $2.75 [估計:Artificial Analysis，經 DoIT 轉引] https://www.doit.com/blog/cost-per-task-vs-cost-per-token ；Opus 4.7 新 tokenizer 使相同工作成本 +12～27% [官方研究:OpenRouter] https://openrouter.ai/blog/opus-47-tokenizer-analysis

### 2.2 「同等能力價格」年降幅估計

| 機構 | 日期 | 估計 | 方法／注意 | 標記 | 來源 |
|---|---|---|---|---|---|
| a16z「LLMflation」 | 2024-11 | 同等能力（MMLU）成本**每年降 10x**；GPT-3 級 $60→$0.06（2021-11→2024 末，約 1000x） | 以 MMLU 分數定義能力；作者承認污染問題 | [估計:a16z] | https://www.a16z.com/llmflation-llm-inference-cost |
| Epoch AI | 2025-03-12 | 依門檻不同每年降 **9x～900x**，中位約 **50x/年**；GPT-4 級 GPQA 每年降 40x | 最快降幅集中在最近一年，未必持續 | [估計:Epoch AI] | https://epoch.ai/data-insights/llm-inference-price-trends |
| arXiv「The Price of Progress」 | 2025-11 | 前沿模型同等表現價格每年降 **5x～10x**；扣除硬體與開源後演算法效率約 3x/年 | NeurIPS 2025 workshop | [估計:學術] | https://arxiv.org/html/2511.23455v1 |
| Stanford HAI AI Index 2025 | 2025-04 | GPT-3.5 級價格約 18 個月降 280x | 二手轉引 | [估計:Stanford HAI] | （經 Wing VC 轉引）|
| Wing VC | 2026-08 | GPT-4 級自 2023-03 降約 300x；Blackwell 使代表性 MoE 服務成本由 Hopper ~$0.20 降至 $0.02～0.05 /M | 綜合 a16z/Epoch/推論商資料 | [估計:Wing VC] | https://www.wing.vc/content/who-makes-money-when-inference-gets-10x-cheaper |
| Bain | 2026-06 | 每 token 成本 2024-12→2025-12 **減半** | 混合口徑 | [估計:Bain，經 Fortune] | https://fortune.com/2026/06/17/why-is-ai-spending-increasing-as-tokens-get-cheaper-jevons-paradox/ |
| Silicon Data Token Expenditure Index | 2026 | 每 token 價格自 2023 年降 >90%；指數 2026-05 末 ~2.0 → 08-19 ~1.0（約 -50%） | 商業指數，方法未公開 | [估計:Silicon Data] | 同上；https://www.investing.com/analysis/collapsing-token-prices-jevons-paradox-not-a-demand-crash-200686144 |

> **矛盾並列**：「每年 10x」（a16z）、「中位 50x」（Epoch）、「前沿 5–10x」（arXiv）、「一年減半」（Bain）——差異來自「固定能力 vs 前沿」「標價 vs 實際組合」。對 CapEx 判讀較相關的是 Bain／Silicon Data 的「實際支付單價」，降幅遠小於固定能力口徑。

### 2.3 GPU 租價（算力現貨價，2026-10-28 新增）

token 價格是模型公司賣給終端的價格，GPU 租價是 neocloud 賣給模型公司的價格。需求若轉弱，租價會比 CapEx 指引、月營收更早反映；neocloud 拿 GPU 抵押借錢，租價也決定擔保品價值。

**Silicon Data B200 租價指數（SDB200RT，美元／GPU 小時，neocloud 與 GPU 市集）**

| 日期 | 數值 | 說明 | 標記 | 來源 |
|---|---|---|---|---|
| 2026 年初 | ~4.40 | 由 9/1 值與年初至今 +27.6% 回推，本檔自算 | [估計:回推] | 同下 |
| 2026-06 | 5.42 → 5.36 | 月內 5.26–5.45 | [官方:Silicon Data] | https://www.silicondata.com/blog/b200-rental-price-august-2026-update |
| 2026-07 | 5.63 → 5.67 | 月內最高 6.01 | [官方:Silicon Data] | 同上 |
| 2026-08 | 5.67 → 5.62 | 年化波動 7.1%，2026 年最低 | [官方:Silicon Data] | 同上 |
| 2026-09-01 | **5.62** | 年初至今 **+27.6%** | [官方:Silicon Data] | 同上 |
| 2026-10-10 | 5.93 | | [二手] | 經搜尋摘要轉引，未見原文 |
| 2026-10-27 | **6.47** | 7 日 +11.9%；較年初約 +47%（本檔自算） | [官方:Silicon Data] | https://www.silicondata.com/products/silicon-index/b200 |

- **矛盾並列**：同一頁的 FAQ 寫「目前價格 $5.45」，與標題的 6.47 不一致，頁面未說明（FAQ 可能未更新）。
- **期限結構（2026-09-07）**：現貨 5.69；遠期 3 個月 5.68、6 個月 5.41、12 個月 **5.03**，逆價差（遠期低於現貨）。Silicon Data 的解讀是「反映現在鎖定長約的成本」，不是預測租價會跌。
- **其他世代（2026-09-07）**：H100 2.63、H200 3.29；B200 約為 H100 的 2.2 倍。比值穩定，Silicon Data 解讀為世代價差，不是新品溢價。
- **不同指數不能混用**：Ornn OCPI-B200 在 2026-10-25 是 $9.70（https://data.ornn.com/markets/b200），口徑不同。
- **CME 算力期貨**：CME 與 Silicon Data 於 2026-08-11 宣布，以 H100、B200 租價指數為標的的期貨（GPU1、GPU2；每口 730 GPU 小時，現金交割，掛 36 個月）預定 **2026-10-05** 在 NYMEX 上市，須待監管審查。**是否已實際開始交易、成交量多少，查不到。**[官方:CME] https://www.cmegroup.com/media-room/press-releases/2026/8/11/cme_group_and_silicondatatolaunchcomputefuturesonoctober5tounloc.html
- **影片引用**：AI懶人報 EP442（2026-10-24）引用「9 月初約 $5.6、今年漲 27%」，與 Silicon Data 8 月報告一致。

> **判讀**：B200 租價 2026 年持續上漲、10 月再加速，和「需求超過供給」（微軟、台積電、黃仁勳說法）一致，目前看不到需求轉弱。要觀察的是：(1) 租價轉為持續下跌，特別是新一代 GPU 上量時，舊世代跌幅是否超過世代價差；(2) CME 期貨若有成交，遠期曲線的逆價差是否擴大。指數 2025 年才開始，沒有經歷過下行週期，**目前只記錄、不設門檻**；累積幾季後再評估是否放進見頂檢查清單，作為第 1 項（CapEx 放緩）的領先指標。

---

## 3. 價格彈性證據（Jevons 悖論）

| 案例 | 價格變化 | 用量／營收變化 | 標記 | 來源 |
|---|---|---|---|---|
| 全市場（Bain） | 每 token 成本 2024-12→2025-12 -50% | token 消耗 +450%（≈5.5x）→ 支出約 2.75x | [估計:Bain] | https://fortune.com/2026/06/17/why-is-ai-spending-increasing-as-tokens-get-cheaper-jevons-paradox/ |
| 全市場（Silicon Data） | 單價自 2023 降 >90% | LLM 支出自 2025 末翻倍 | [估計:Silicon Data] | 同上 |
| Google | 每 prompt 能耗 12 個月降 33x | 總用電 2025 年 +37%；月 token 2 年 ~330x | [官方]（Google 揭露，經 Wing VC 整理） | https://www.wing.vc/content/who-makes-money-when-inference-gets-10x-cheaper |
| OpenAI GPT-5.6 Luna / Terra（2026-07-30） | Luna -80%、Terra -20% | 傳 Luna 用量 ~14x、Terra ~5x，營收上升（無具體數字） | [報導:Investing.com 引述未具名報導]，**未能以官方來源驗證** | https://www.investing.com/analysis/collapsing-token-prices-jevons-paradox-not-a-demand-crash-200686144 |
| OpenAI GPT-6 Sol（2026-09-22） | 較 5.6 Sol -50% | 用量反應：查不到 | [報導:Yahoo Finance] | https://finance.yahoo.com/technology/ai/articles/openai-cuts-gpt-6-sol-111351382.html |
| Claude Opus 4.5（2025-11） | -67% | 降價後 Anthropic run-rate 由 ~$9B（2025 末）→ $14B（2026-02）→ $30B（2026-04）→ $47B（2026-05）→ ~$65B（2026-07 末）；但無法區分價格效應 vs Claude Code/模型能力 | [官方]／[報導:Bloomberg/Reuters] | https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth ；https://epoch.ai/gradient-updates/an-update-on-ais-most-important-number |
| Ramp 企業帳單 | — | 企業月 AI 支出 2025-02→2026-02 **4x**；最大支出者約每 4 個月有 1 個月成本跳升 ≥50% | [官方:Ramp] | https://ramp.com/leading-indicators/the-tokenmaxxing-economy-splits-off-and-up |
| Uber | — | 2026 年前 4 個月用完全年 AI 預算；之後每員工每月上限 $1,500 | [報導:Bloomberg，經 Fortune] | https://fortune.com/2026/06/17/why-is-ai-spending-increasing-as-tokens-get-cheaper-jevons-paradox/ |
| DeepSeek 衝擊（2025-01） | 效率衝擊 | NVIDIA 單日市值 -$589B；18 個月後訂單能見度約 $1T | [估計:Wing VC 整理] | https://www.wing.vc/content/who-makes-money-when-inference-gets-10x-cheaper |
| Agent 化 | — | Agentic coding 任務 token 用量約為 code chat 的 1000x | [估計:Stanford Digital Economy Lab，經 Wing VC] | 同上 |
| 理論模型 | 50% API 降價 | 模擬顯示 token 消耗凸性增長（非實證） | [估計:學術] | https://arxiv.org/pdf/2601.12339 |

> 小結：總支出隨單價下跌而上升的「相關性」證據充分，但**嚴謹的因果彈性估計查不到**（模型升級、agent 化、算力供給限制同時發生）。

---

## 4. 使用者與付費

### 4.1 消費端

| 產品 | 時間 | 數值 | 標記 | 來源 |
|---|---|---|---|---|
| ChatGPT WAU | 2025-10（DevDay 2025） | 8 億 | [官方:Altman 於 DevDay 2025 發言，本次未重新取得原始連結] | 待補 URL |
| ChatGPT WAU | 2026-02-27 | 9 億 WAU；**5,000 萬付費訂閱**（含 4 種個人／商業方案） | [官方]（經 TechCrunch） | https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users |
| ChatGPT WAU | 2026-07～09 | >10 億（日期矛盾：2026-07-31 / 2026-08 末 CMO / 2026-09-08 確認、8 月中快照） | [報導:多家，未見官方部落格] | https://cryptobriefing.com/chatgpt-one-billion-weekly-users/ ；https://thenextweb.com/news/chatgpt-1-billion-weekly-active-users-openai-target |
| ChatGPT WAU | 2026-09-29 | 12 億（單一來源） | [二手:technologychecker] 待驗證 | https://technologychecker.io/blog/chatgpt-statistics |
| ChatGPT App MAU | 2026-05 | >10 億 MAU（App） | [估計:Sensor Tower] | 同上 eWeek/quashbugs |
| ChatGPT 付費數 2026-02 之後 | — | **查不到**官方更新 | — | — |
| Gemini App MAU | 2025-10（Q3'25） | 6.5 億 | [官方] | https://s206.q4cdn.com/479360582/files/doc_events/2025/Oct/29/2025_Q3_Earnings_Transcript.pdf |
| Gemini App MAU | 2026-02（Q4'25） | >7.5 億 | [官方] | https://pulse2.com/google-gemini-surpasses-750-million-monthly-active-users |
| Gemini App MAU | 2026-05（I/O 2026） | >9 億 | [官方]（日期報導不一） | https://quashbugs.com/blog/gemini-app-active-user-statistics |
| Gemini App MAU | 2026-07-22（Q2'26） | 9.5 億 | [官方] | https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm |
| Gemini App MAU | 2026-08-11 | >10 億（僅 Gemini App+Chrome 內 Gemini，不含 Search/Gmail） | [官方:Josh Woodward，經 Neowin] | https://www.neowin.net/news/gemini-reaches-1-billion-monthly-users-as-google-flexes-its-massive-distribution-advantage/ |
| Google 付費訂閱（全部） | 2026-04 | 3.5 億（主要為 YouTube、Google One；Q1'26「消費者 AI 方案最強一季」，未拆數） | [官方] | https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000043/googexhibit991q12026.htm |
| Claude 消費端 | 2026 | 官方未揭露總數；「付費訂閱 2026 年內翻倍以上、DAU 年初至今 >3x」 | [官方:發言人] | https://techcrunch.com/2026/03/06/claudes-consumer-growth-surge-continues-after-pentagon-deal-debacle/ |
| Claude 用戶估計 | 2026 初 / 2026-05 | 1,800 萬～3,000 萬（2026 初）vs 2.45 億 MAU（2026-05，Sensor Tower）；付費轉換率 13% | [估計:各方，差距極大] | https://www.usecarly.com/blog/claude-statistics/ ；https://thenextweb.com/news/anthropic-claude-paying-consumers-growth-chatgpt-indagari |
| Claude 美國付費消費者 | 2026-01→06 | 付費用戶與營收 +約 75%（2,800 萬美國消費者刷卡樣本） | [估計:Indagari] | https://thenextweb.com/news/anthropic-claude-paying-consumers-growth-chatgpt-indagari |

### 4.2 企業／開發者端

| 產品 | 時間 | 數值 | 標記 | 來源 |
|---|---|---|---|---|
| Microsoft 365 Copilot 付費席次 | 2026-01（FY26 Q2） | 約 1,500 萬 | [官方] | https://licenseq.com/microsoft-fy26-q3-results-explained/ |
| 同上 | 2026-04（FY26 Q3） | >2,000 萬；Accenture 74 萬席 | [官方] | 同上 |
| 同上 | 2026-07-29（FY26 Q4） | >3,000 萬，淨增季增 >1 倍；>5 萬席客戶數年增 >7x | [官方] | https://www.investing.com/news/transcripts/earnings-call-transcript-microsoft-q4-2026-beats-forecasts-stock-jumps-8-93CH-4822020 |
| 同上（反面） | 2026 | 顧問觀察：客戶數千席中活躍率常 <30% | [估計:LicenseQ 軼事] | https://licenseq.com/microsoft-fy26-q3-results-explained/ |
| Microsoft AI 業務年化營收 | 2026-04 | >$370 億，年增 123% | [官方]（FY26 Q3）；另「$37B Copilot ARR」說法被指從未在電話會議提及 | https://licenseq.com/microsoft-fy26-q3-results-explained/ ；https://www.digitalapplied.com/blog/microsoft-fy26-q4-earnings-copilot-arr |
| GitHub Copilot 用戶（累計） | 2025-04 / 2025-07 / 2025-10 / 2026-07 | 1,500 萬 / 2,000 萬 / 2,600 萬 / **5,000 萬** | [官方] | https://techcrunch.com/2025/07/30/github-copilot-crosses-20-million-all-time-users/ ；FY26 Q4 逐字稿 |
| GitHub Copilot 付費訂閱 | 2024-01 / 2026-01 | 130 萬 / 470 萬 | [官方，經二手] | https://secondtalent.com/resources/github-copilot-statistics |
| GitHub Copilot 營收 | FY26 Q4 | 季增 >60%；2026-06-01 起改用量計價 | [官方] | 同上逐字稿；licenseq |
| Gemini Enterprise | Q1'26 / Q2'26 | 付費 MAU 季增 40% / 近 90% Fortune 100 使用 | [官方] | Alphabet 8-K（見上） |
| Gemini 開發者 | Q2'26 | 每月 >900 萬開發者 | [官方] | https://www.thewrap.com/industry-news/business/alphabet-earnings-q2-2026/ |

### 4.3 AI 應用層公司營收（ARR / run-rate，均非 GAAP）

| 公司 | 時間序列 | 標記 | 來源 |
|---|---|---|---|
| **Claude Code** | $500M（2025-09）→ $1B（2025-11）→ **>$2.5B（2026-02）**；WAU 年初至 2 月翻倍、商業訂閱 4x。2026-02 後**查不到官方更新**；$8B / $15B 說法僅見追蹤站預測 | [官方] 至 2026-02 | https://www.constellationr.com/insights/news/anthropics-claude-code-revenue-doubled-jan-1 ；https://www.gradually.ai/en/claude-code-statistics/ |
| **Cursor（Anysphere）** | ~$100M（2025 初）→ $1B（2025-11）→ $2B（2026-02）→ $3B（2026-04 末）→ **>$4B（2026-06 初）**；企業占比 65%～75%（矛盾）；SpaceX 以 $60B 全股票收購（完成與否報導矛盾） | [報導:知情人士] | https://dealroom.co/news/134107-cursor-tops-4b-annualized-revenue/ ；https://en.wikipedia.org/wiki/Anysphere |
| **Perplexity** | ~$232M（2025 末）→ >$450M（2026-03，FT）/ ~$500M（2026-04）→ ~$750M（2026-08，Sacra） | [報導:FT]／[估計:Sacra] | https://clinkbill.com/arr-leaderboard/perplexity ；https://valueaddvc.com/blog/perplexity-ai-valuation-revenue-2026-23b-450m-arr |
| **Lovable** | $300M（2026-02）→ $400M（2026-03，BI）→ $500M（2026-06，公司告 TechCrunch）→ >$600M（2026-09 末，TechCrunch）；2026-08 以 $13.3B 估值募 $400M | [官方:公司告知媒體] | https://northeasttimes.com/2026/08/13/lovable-the-app-building-startup-just-doubled-its-value-to-13-3-billion/ |
| **Replit** | ~$150M（2025 末，部分來源）/ ~$300M（2025-12）→ ~$525M（2026-04）；目標 2026 末 $1B | [報導:CNBC 等]，來源間矛盾 | https://www.cnbc.com/2026/05/19/replit-cnbc-disruptor-50-ranking.html ；https://valueaddvc.com/blog/how-does-replit-make-money-525m-arr-9b-valuation-and-the-ai-agent-business-model-explained |
| **Harvey** | $100M（2025-08）→ $190M（2026-01，CNBC）→ Q2'26 單季淨增 >$100M ARR（公司 2026-08-04）→ $400M（2026-09-09，arr.club，未驗證） | [官方]部分／[二手] | https://tech-insider.org/harvey-ai-200m-arr-manifold-odds-2026/ ；https://www.arr.club/weekly/2026-06-22 |

---

## 5. 企業採用

### 5.1 美國人口普查局 BTOS（AI 使用率，雙週調查）

| 期間 | 使用率 | 問卷口徑 | 標記 | 來源 |
|---|---|---|---|---|
| 2023-10-23～11-05 | 3.9%（標題 3.8%） | 舊：「用於生產商品或服務」 | [官方] | https://census.gov/library/stories/2023/11/businesses-use-ai.html |
| 2024 初 | 4.6% | 舊 | [估計:EIG 整理官方數據] | https://eig.org/?p=24816 |
| 2025-09 | 約 10% | 舊 | [估計:EIG] | 同上 |
| 2025-11（改題後首期） | 17.3% | 新：「用於任何業務功能」 | [官方，經 Fed 引用] | https://www.federalreserve.gov/econres/notes/feds-notes/monitoring-ai-adoption-in-the-u-s-economy-20260403.html |
| 2025-12～2026-05 | 17%～20%；預期 6 個月內 20%～23% | 新 | [官方] | https://www.census.gov/library/stories/2026/05/ai-use-businesses.html |
| 截至 2026-05-03 | **19.8%**；≥250 人企業 37%、100–249 人 32%、≤4 人 <20%；資訊業 39.7%、金融保險 33.9%、零售 ~14% | 新 | [官方] | 同上 |
| Census 工作論文（2025-11～2026-01） | 18% 企業於某業務功能使用 AI；就業加權 32% | 新（AI 補充問卷） | [官方:CES-WP-26-25] | https://www2.census.gov/library/working-papers/2026/adrm/ces/CES-WP-26-25.pdf |
| 2026-05 之後 | **查不到**（未取得官方原始時序表） | — | — | — |

> **口徑斷層**：2025-11 改題，前後不可直接拼接。新口徑下 6 個月僅 17%→20%，**擴散速度溫和**。

### 5.2 Ramp AI Index（Ramp 平台上付費 AI 的企業占比；偏新創／中小／科技型）

| 時間 | 整體 | Anthropic | OpenAI | 標記 | 來源 |
|---|---|---|---|---|---|
| 2025-03 | ~35% | 24.4% | — | [官方:Ramp] | https://ramp.com/leading-indicators/the-tokenmaxxing-economy-splits-off-and-up |
| 2026-03 | 50.4% | 30.6% | 35.2% | [官方:Ramp] | 同上 |
| 2026-04 | — | 34.4% | 32.3%（Anthropic 首度超越） | [報導:TechCrunch/The Decoder] | https://the-decoder.com/anthropic-overtakes-openai-in-b2b-adoption-for-the-first-time-according-to-ramp-spending-data/ |
| 2026-07 | **55.7%**（歷史新高） | 43.5% | 39.7% | [官方:Ramp Summer 2026 報告] | https://assets.ramp.com/nextjs/files/2026-Summer-Business-Spending-Report.pdf |
| 2026-08 | 56.1% | 43.8% | 39.8% | [報導:letsdatascience/fourweekmba] | https://letsdatascience.com/news/anthropic-gains-on-enterprise-ai-spending-share-36467987 |
| 矛盾 | fourweekmba 2026-06：Anthropic 41% / OpenAI ~38% | — | — | [二手] | — |

其他：Anthropic 年付 >$1M 客戶自 2026-02 翻倍至 1,000 家（Ramp 文引述）；Ramp 指 Q3'26 迄今 OpenAI 成長快於 Anthropic。

### 5.3 支出規模與預算調查

| 機構 | 日期 | 數據 | 標記 | 來源 |
|---|---|---|---|---|
| Menlo Ventures | 2025-12 | 企業生成式 AI 支出 2025 年 **$37B**（2024 $11.5B，2023 $1.7B）；應用層 $19B（其中程式 $4B）、基礎模型 API $12.5B | [估計:Menlo] | https://letsdatascience.com/news/enterprises-increase-ai-spending-to-37bn-6d854973 |
| Gartner | 2026-01 / 2026-05 | 2026 全球 AI 支出 $2.52T（+44%）→ $2.59T（+47%）；另有報導 $2.67T（日期不明）；基礎設施占 >45%；Gartner 稱 2026 全年處於「幻滅低谷」 | [估計:Gartner] | https://gartner.com/en/newsroom/press-releases/2026-05-19-gartner-forecasts-worldwide-ai-spending-to-grow-47-percent-in-2026 |
| a16z CIO 調查 | 2025 | 預期 LLM 支出未來一年平均 +~75%；「創新預算」占 LLM 支出由 25% 降至 7%（轉入常態預算）。**2026 版查不到** | [估計:a16z] | https://a16z.com/ai-enterprise-2025/ |
| RBC | 2026 | 117 位 IT 主管中 90% 計畫 2026 增加 AI 支出 | [估計:RBC] | https://www.itiger.com/news/1158049519 |
| Verdantix | 2025 | 352 位主管中過半預期 AI 預算年增僅 1%～9% | [估計:Verdantix] | https://marketing.verdantix.com/blog/verdantix-2025-global-ai-survey--three-takeaways-for-corporate-leaders |
| McKinsey State of AI 2026 | 2026-08 | 88% 組織至少一個功能常態使用 AI；**僅 37% 稱 AI 對 EBIT 有貢獻（與去年持平）**；高績效者（≥5% EBIT 來自 AI）約 6% 持平；80% 稱個人生產力提升；~20% 稱 AI 營運成本限制使用 | [估計:McKinsey] | https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/the%20state%20of%20ai/the-state-of-ai-in-2026-on-the-road-to-roi.pdf ；https://www.fm-magazine.com/news/2026/sep/companies-financial-value-from-ai-holds-firm-in-2026/ |
| JPMorgan AM | 2026-01-09 | 55% 美國成人每週使用生成式 AI；17% 美國企業採用 | [估計:JPM 引用] | https://am.jpmorgan.com/us/en/asset-management/liq/insights/market-insights/market-updates/on-the-minds-of-investors/how-is-ai-being-monetized.html |

### 5.4 「95% 試點無回報」與反駁

| 研究 | 日期 | 結論 | 方法限制 | 標記 | 來源 |
|---|---|---|---|---|---|
| MIT NANDA「The GenAI Divide」 | 2025-07（初步報告），2025-08 Fortune 報導 | 95% 組織的生成式 AI 計畫無可衡量回報 | 樣本：>300 公開案例、52 組織訪談、153 位主管問卷（報導數字不一）；「失敗」定義為 6 個月內無可量化營收／成本效益，過窄 | [估計:MIT NANDA] | https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo |
| Wharton × GBK「Accountable Acceleration」 | 2025-10-28 | 約 3/4 企業主管稱生成式 AI 投資已有正 ROI；82% 每週使用；72% 有追蹤獲利／生產力指標 | >800 位美國企業決策者自評；VP 以上較樂觀、中階主管較保守；「74%」為二手轉寫 | [估計:Wharton] | https://www.businesswire.com/news/home/20251028556241/en/ |
| McKinsey 2026 | 2026-08 | 37% 見 EBIT 影響（持平）—介於兩者之間 | 自評問卷 | [估計:McKinsey] | 見上 |

> 判讀：MIT 量的是「6 個月內可量化財務回報」，Wharton 量的是「主管自評 ROI」，McKinsey 量的是「EBIT 歸因」——三者並不矛盾，共同指向「使用普及、財務歸因仍集中於少數」。

---

## 6. 整體 AI 營收規模 vs CapEx

### 6.1 回本所需營收估算

| 機構 | 日期 | 估算 | 方法 | 標記 | 來源 |
|---|---|---|---|---|---|
| Sequoia（David Cahn）「AI's $200B Question」 | 2023-09 | 需 $200B／年營收 | NVIDIA 年化營收 ×2（資料中心總成本）×2（終端毛利 50%） | [估計:Sequoia] | https://www.techdogs.com/tech-news/td-newsdesk/600-bn-revenue-needed-to-justify-ai-hardware-spend-report |
| Sequoia「AI's $600B Question」 | 2024-06 | 需 $600B／年；缺口約 $500B | 同上 | [估計:Sequoia] | 同上；Forbes 2026-06 稱缺口 2026 年持續擴大 https://www.forbes.com/sites/jasonkirsch/2026/06/02/the-ai-capex-to-revenue-gap-is-widening---and-markets-are-starting-to-notice/ |
| Bain Global Technology Report 2025 | 2025-09-23 | 2030 年需 **$2T／年**營收支撐算力；預估短缺 **$800B**；全球增量算力 200GW | 即使把 AI 節省全部再投資仍短缺 | [估計:Bain] | https://www.bloomberg.com/news/articles/2025-09-23/an-800-billion-revenue-shortfall-threatens-ai-future-bain-says |
| Bain（2026 版，未取得原文） | 2026-09 | 2031 年需 **~$6T／年**；現有應用可產生 $1.2T～1.8T；缺口 $4.2T～4.8T | — | [報導:Open Magazine 引述 Bain] | https://openthemagazine.com/technology/ai-needs-6-trillion-in-annual-revenue-by-2031-to-justify-compute-spending-bain |
| JPMorgan Asset Management | 2025-11（首見）/ 2026-01-09 頁面 | 10% 報酬需 **~$650B／年**營收（≈每位 iPhone 用戶每月 $35）；以當年 hyperscaler CapEx $533B 為基礎 | 永續年金式 | [估計:JPM] | https://am.jpmorgan.com/us/en/asset-management/liq/insights/market-insights/market-updates/on-the-minds-of-investors/how-is-ai-being-monetized.html |
| Goldman Sachs | 2026-09-24 | 以 2026–27 平均 CapEx 計，hyperscaler（AMZN/GOOGL/META/MSFT/ORCL/SPCX）**損益兩平需 ~$308B／年** AI 營收；10%～20% 報酬需 **$417B～526B**；CapEx 預測 2027 $1.2T、2028 $1.4T；實現 ROIC 由 40% 降至 25% | 兩平 = 年折舊 + 營運費用；以累計 CapEx 計算會更高 | [估計:Goldman] | https://www.edwardconard.com/macro-roundup/goldman-estimates-based-on-average-annual-capex-in-2026-27-that-hyperscalers-need-308b-in-annual-ai-revenues-over-the-next-few-years-to-break-even-and-417-526b-for-a-10-20/ ；https://www.gspublishing.com/content/research/en/reports/2026/09/24/17991761-4354-496a-bf3a-26b281c829fc.pdf |
| CFA 式分析 | 2026 | 25% 報酬門檻下需 ~$169B AI 歸屬營收（2028 末） | — | [估計:二手] | https://alcapitaladvisory.com/research/intelligence/ai-infrastructure.html |

### 6.2 實際 AI 營收規模估計

| 項目 | 時間 | 數值 | 標記 | 來源 |
|---|---|---|---|---|
| 生成式 AI 全產業（去重） | 2026-06 | **~$175B 年化**（Exponential View「接近 $200B」） | [估計:Epoch/Exponential View] | https://epoch.ai/gradient-updates/an-update-on-ais-most-important-number |
| OpenAI + Anthropic 合計 run-rate | 2026 初 → 2026-08 | ~$30B → **~$105B**（3.5x）；Q1 末約 $55B | [估計:Epoch，基於報導] | 同上 |
| 同上（另一口徑） | 2026-09 | ~$135B（Anthropic ~$65B + OpenAI ~$70B） | [二手:Manifold 市場] | https://manifold.markets/AlexMiller3a5e/what-will-openai-anthropics-combine |
| 會計差異 | — | Anthropic 經雲端轉售的 token 以總額認列、OpenAI 僅認列分潤 → Anthropic 相對高估 | [估計:Epoch] | 同上 |
| Microsoft AI 業務 | 2026-04 | >$37B 年化 | [官方] | 見 4.2 |
| 2026 hyperscaler CapEx | 2026 | $646B（Apollo）/ ~$700B+（Reuters 系）/ ~$725B / ~$800B（Goldman）/ $700–900B（CreditSights）/ $1.009T（UBS，較廣口徑） | [估計:各機構] | https://www.apolloacademy.com/how-much-is-646-billion/ ；https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/ |

> **粗略比值（本檔自算，僅供方向）**：全產業 AI 營收 ~$175–200B（年化）÷ 2026 hyperscaler CapEx ~$650–800B ≈ **0.22–0.31**。對照 Goldman 兩平門檻 ~$308B：目前全產業年化營收約達門檻的 57%–65%；但 Goldman 門檻只算 hyperscaler 自身 CapEx，未含 neocloud、模型公司自建與主權 AI。注意：營收含模型公司付給雲端的錢（重複計算風險），且 run-rate ≠ 已實現營收。

---

## 7. 價格×用量的判讀

1. **用量成長遠快於單價下跌**：Google API token 一年約 3x（7B→22B/分）、全表面一年 ~7x；OpenRouter 半年 5x；Bain 估 2025 年 token 消耗 +450%、單價 -50%。→ **支出（價×量）一年約 2.5–3x**，與 OpenAI+Anthropic 合計 run-rate 2025 年 >4x、2026 年前 8 個月 3.5x 的方向一致。在 2025–2026 這段期間，需求的價格彈性明顯 >1（Jevons 式），但因果無法乾淨辨識。
2. **成長動能來自 agent／程式**，不是聊天：OpenRouter agent 占 71%、程式 >50%；Claude Code、Cursor、Codex、GitHub Copilot 轉用量計價。每任務 token 是 chat 的 ~1000x，這讓「每 token 降價」反而推高總帳單（Ramp：企業月 AI 支出一年 4x；Uber 4 個月燒完年度預算）。
3. **價格曲線出現分岔**：同能力價格仍快速下跌（a16z 10x/年、Epoch 中位 50x/年），但前沿檔位 2026 年回升（GPT-5.5 $5/$30、GPT-6 Astra 與 Claude Fable $10/$50），Google 更正式公告 Gemini 4 Argon 與 Flash 系列**漲價一倍**。可能解讀：(a) 算力供不應求（微軟稱需求仍超過供給），供應商取得定價權 → 對 CapEx 回收是正面訊號；(b) 促銷補貼退場 → 若漲價後用量大幅回落，代表先前需求有部分是補貼撐出來的。**12 月至 2027-01 Google 漲價後的用量反應是關鍵觀察點。**
4. **消費端規模大、變現深度有限**：ChatGPT ~9億–10億 WAU 僅 5,000 萬付費（~5%）；Gemini 10 億 MAU 多為分發帶動。付費成長主力在企業與開發者（M365 Copilot 一季內 2,000 萬→3,000 萬席；Ramp 付費採用 56%）。
5. **企業端「用了」不等於「賺了」**：BTOS 新口徑僅 ~20% 企業使用 AI、半年僅升約 3 個百分點；McKinsey 只有 37% 見 EBIT 貢獻且一年持平。需求集中於科技型／大型企業，廣度擴散慢於 token 量的增長。
6. **對 CapEx 合理性的含意**：年化 AI 營收 ~$175–200B，Goldman 兩平門檻 ~$308B、10–20% 報酬需 $417–526B、JPM 10% 報酬需 $650B、Bain 2030 年 $2T。以目前約 2.5–3x/年的支出成長，1 年左右可越過兩平門檻、約 2 年可達合理報酬門檻——**前提是價×量成長不放緩，且漲價後用量不回落**。Epoch 已觀察到 2026 年合計營收翻倍時間由 1 季拉長到約 4 個月，需持續追蹤。

---

## 8. 資料缺口

| 缺口 | 說明 / 下一步 |
|---|---|
| Alphabet Q3'26（10 月底）、Microsoft FY27 Q1（10 月底）財報 | 尚未發布；發布後更新 API token/分、Copilot 席次、Gemini MAU |
| Google 2026-05 之後「全表面」月 token | 查不到；觀察 Q3'26 電話會議 |
| Microsoft 總 token 量 | FY25 後改揭露「兆 token 客戶數」，總量查不到 |
| OpenAI API 吞吐量 | 最後可信數字為 2025-10 的 60 億/分（另有 150 億/分矛盾說法）；2026 查不到 |
| Anthropic token 量、Claude 消費端 MAU、付費訂閱數 | 官方未揭露；估計值 1,800 萬～2.45 億落差過大 |
| Claude Code 2026-02 後營收 | 查不到官方數字；待 Anthropic IPO 申報文件（若有） |
| ChatGPT 付費訂閱 2026-02 後 | 查不到官方更新；10 億 WAU 日期報導矛盾 |
| OpenRouter 最新官方總量 | rankings 頁未顯示；各來源 25 兆～115 兆／週落差大 |
| 價格彈性因果估計 | 僅相關性證據；GPT-5.6 Luna「用量 14x」未獲官方驗證 |
| GPT-5.6 Sol 價格 | 報導 $5/$30 vs 官方現行 $4/$20，調價日期不明 |
| Claude Opus 4.8、Fable 5/Mythos 5、Gemini 4 Argon 發布日期 | 查不到可靠的官方日期 |
| BTOS 2026-05 後時序 | 需直接下載 census.gov BTOS 資料表 |
| Ramp 9～10 月 | 僅二手來源；需 Ramp 官方 AI Index 頁（擷取失敗） |
| Menlo 2026 版、a16z 2026 CIO 調查 | 查不到（可能尚未發布） |
| Bain 2026 Technology Report 原文 | 僅見媒體轉述 $6T（2031）數字 |
| Sequoia 2025/2026 更新版 | 查不到 Cahn 正式更新 |
| 應用層公司（Perplexity、Replit、Harvey） | 多為 Sacra / 聚合站估計，缺公司正式揭露 |
| GPU 租價長期序列 | Silicon Data 指數 2025 年才開始、無下行週期；官網頁 6.47 與 FAQ 5.45 矛盾；CME 算力期貨是否已上市、成交量查不到。每月更新 2.3 節 |
| 「AI 營收」去重口徑 | 模型公司營收與雲端 AI 營收存在重複計算，尚無公認去重方法（Epoch $175B 方法未公開） |
