# X：循環交易、融資結構與 Neocloud

> 資料截至：2026-10-19（收集日）
> 標記：**[官方]** 公司揭露 / SEC 申報；**[報導:媒體]** 媒體引述內部文件或知情人士；**[估計:機構]** 分析師或研究機構估算
> 「投資金額」多為最高額或分期條件式；「採購承諾」多為多年期合約總價值，非已支付金額。

---

## 一、循環交易地圖

```
投資方 ──股權/擔保──▶ 模型公司 ──多年期採購承諾──▶ 投資方（雲端 / 晶片）
                                     │
                                     └─▶ 投資方認列為營收 / RPO / backlog
```

### 1.1 總表

| # | 投資方 → 被投資方 | 投資金額 | 被投資方 → 投資方採購承諾 | 時間 | 標記 | 來源 |
|---|---|---|---|---|---|---|
| 1 | **Microsoft → OpenAI** | 累計 ~$13B+（2019 起）；持股約 27% | Azure 增量 **$250B**；OpenAI 付 Microsoft 20% 營收分成至 2030（設上限）；2025 年實付 Microsoft ~$17.2B | 2019–2023 投資；2025-10-28 重組；2026-04-27 修約 | 投資 [報導]；$250B/27% [官方]；$17.2B [報導:外洩報表] | https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/ ；https://venturebeat.com/technology/microsoft-and-openai-gut-their-exclusive-deal-freeing-openai-to-sell-on-aws-and-google-cloud ；https://feedbagel.com/post/leaked-openai-spent-34-billion-in-2025-against-13-billion-in-revenue-with-a-17-b |
| 1a | ↳ Microsoft RPO 中的 OpenAI | — | 商業 RPO $625B 中約 **45%（~$281B）** 來自 OpenAI（2025-12 季）；FY26 年底 RPO $678B，排除 OpenAI 僅成長 25%，推估 OpenAI 占 ~32% | 2026-01、2026-07 | 45% [官方:Microsoft 財報會議]；32% [估計:Benzinga] | https://cloudwars.com/cloud/microsoft-q2-rpo-soars-110-led-by-openai-commitment-of-281-billion/ ；https://www.webull.com/news/15317720163771392 |
| 2 | **Amazon → OpenAI** | **$50B**（$15B + $13.7B + $21.3B，已於 2026 Q3 前完成） | AWS **$100B / 8 年**（由 2025-11 的 $38B 擴大），~2 GW Trainium | 2026-02-27 | [官方:Amazon/OpenAI、Amazon SEC 申報] | https://press.aboutamazon.com/2026/2/openai-and-amazon-announce-strategic-partnership ；https://www.pymnts.com/news/artificial-intelligence/2026/amazon-completes-50-billion-dollar-investment-openai/ |
| 3 | **Amazon → Anthropic** | 先前 $8B + 2026-04 新增 $5B（另 $20B 依商業里程碑），合計最高 ~$33B | AWS **>$100B / 10 年**，最高 5 GW；Project Rainier（~50 萬顆 Trainium2） | 2023–2024；2026-04-20 | [官方:Amazon/Anthropic]；累計 $13B [報導:次級] | https://siliconangle.com/2026/04/20/amazon-invest-25b-anthropic-part-expanded-cloud-partnership/ ；https://www.datacenterdynamics.com/en/news/amazon-invests-5bn-in-anthropic-anthropic-agrees-to-lease-5gw-of-ai-capacity/ |
| 4 | **Google → Anthropic** | 先前 >$3B（~14%，NYT）；2026-04 新增 $10B 現金（$350B 估值）+ 最高 $30B 依績效 | Google Cloud **5 GW TPU / 5 年**；另 Google+Broadcom 多 GW TPU（Broadcom 申報約 3.5 GW，2027 起，另 2026 已供 ~1 GW） | 2023–2025；2026-04-06（TPU）；2026-04-24（投資） | 投資/GW [官方:Anthropic]；3.5GW [官方:Broadcom 申報，經 TNW] | https://news.bloomberglaw.com/antitrust/google-plans-to-invest-up-to-40-billion-in-anthropic ；https://www.anthropic.com/news/google-broadcom-partnership-compute ；https://thenextweb.com/news/anthropic-google-broadcom-compute-deal |
| 4a | ↳ Google 帳面利得 | — | Alphabet Q2 2026 淨利 $112.1B（去年同期 $28.2B），大量來自 Anthropic 與 SpaceX 持股評價利得 | 2026-07-22 | [官方/報導] | https://startupfortune.com/google-cloud-grew-82-in-q2-2026-and-the-514-billion-backlog-tells-you-everything-about-who-is-winning-the-ai-race/ |
| 4b | ↳ Broadcom 為 Anthropic 擔保 | — | Apollo 主導 $35B 機架融資；**Broadcom 擔保最高 $29B** Anthropic 五年租賃義務；Alphabet 另擔保部分資料中心/電力融資 | 2026-08 | [報導:MLQ 轉述] | https://mlq.ai/news/googles-anthropic-compute-buildout-splits-risk-among-broadcom-wall-street-and-data-center-developers/ |
| 5 | **Microsoft + NVIDIA → Anthropic** | NVIDIA 最高 $10B、Microsoft 最高 $5B | Azure **$30B**（另可追加至 1 GW），採 NVIDIA Grace Blackwell / Vera Rubin | 2025-11-18 | [官方] | https://finance.yahoo.com/news/microsoft-nvidia-invest-anthropic-startup-113316065.html ；https://www.theregister.com/2025/11/18/anthropic_microsoft_nvidia_ai_deals/ |
| 6 | **NVIDIA → OpenAI** | 原 LOI 最高 $100B（未簽約、未撥款）→ 實際 **$30B 股權**（2026-03 輪） | 原 LOI 10 GW NVIDIA 系統；OpenAI 經 Oracle/Microsoft/CoreWeave 等間接採購 NVIDIA GPU | 2025-09-22；2026-02-27 | [官方/報導:WSJ/Fortune] | https://fortune.com/2026/02/02/jensen-huang-nvidia-ceo-on-openai-investment-never-a-commitment/ ；https://www.cnbc.com/2026/02/03/nvidia-openai-stalled-on-their-mega-deal-ai-giants-need-each-other.html |
| 6a | ↳ **NVIDIA 擔保 OpenAI 租約** | 擔保上限 **$105B**（SB Energy PORTS 園區，Ohio Pike County，~4.25 GW，9 期，首期 FY2029）；另 3.8 GW 選擇權；總最大曝險 $108.5B | OpenAI 關係企業為承租方 | 2026-08 | [官方:NVIDIA 10-Q（截至 2026-07-26）] | https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000075/nvda-20260726.htm |
| 7 | **NVIDIA → xAI** | 最高 $2B（xAI ~$20B GPU SPV 之股權部分）；並參與 2026-01 Series E | SPV 購買 NVIDIA GPU 再租給 xAI（lease-to-own） | 2025-10；2026-01 | [報導:Bloomberg，經 Sacra] | https://sacra.com/c/xai/ |
| 8 | **NVIDIA → CoreWeave** | 持股約 11–12%；2026-01-26 加碼 $2B（$87.20/股） | NVIDIA 反向：**$6.3B 未售容量回購保證**（至 2032-04）；CoreWeave 為 NVIDIA GPU 大買家 | 2023 起；2025-09；2026-01 | [官方] | https://www.computing.co.uk/news/2026/nvidia-invests-2-billion-in-coreweave ；https://sacra.com/c/coreweave/ |
| 9 | **NVIDIA → Lambda** | 投資人 | NVIDIA 向 Lambda 回租 GPU：$1.3B/4 年（1 萬台伺服器）+ $200M（8 千台）；Lambda 借 $917M 向 NVIDIA 購晶片以履約 | 2025-09 | [報導:The Information/Bloomberg] | https://thenextweb.com/news/lambda-917-million-gpu-leveraged-loan-nvidia-morgan-stanley |
| 10 | **NVIDIA 整體生態系** | 權益投資 **$99B**（非上市 $47.9B + 上市 $42.8B + 長期 $5.0B；其中 $36.9B 受短期鎖定）；另 **$25B** 投資承諾（$18B 於 2027 前） | NVIDIA 自身的 AI cloud 協議 $36B、R&D 雲端 $29B（向客戶回買算力） | 截至 2026-07-26 | [官方:NVIDIA 10-Q] | https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000075/nvda-20260726.htm |
| 11 | **AMD → OpenAI** | 認股權證最高 1.6 億股（約 AMD 10%），行使價 $0.01，依 1→6 GW 部署與股價（至 $600）歸屬 | 6 GW AMD Instinct（MI450 起，首 GW 2026 H2）；截至 2026-06-27 **尚無歸屬** | 2025-10-06 | [官方:AMD 8-K/10-K/10-Q] | https://ir.amd.com/news-events/press-releases/detail/1260/ ；https://www.fool.com/investing/2026/10/05/amd-has-promised-openai-and-meta-up-to-320-million-shares-for-a-penny-each-here-s-what-that-does-to-the-share-count/ |
| 11a | **AMD → Meta** | 同類認股權證 1.6 億股 | Meta GPU 採購（GW 規模） | 2026 | [官方:AMD 申報，經 Motley Fool] | 同上 |
| 12 | **Oracle ↔ OpenAI** | Oracle 未投資 OpenAI 股權；為 Stargate JV 合作方 | **~$300B / 5 年**、4.5 GW，2027 起；Oracle 為此向 NVIDIA 採購 ~$40B GB200 | 2025-07/09 | [報導:WSJ]；GW [官方] | https://intuitionlabs.ai/articles/oracle-openai-300b-deal-analysis |
| 13 | **SoftBank → OpenAI** | 2026-03 輪 $30B；累計報導 $64.6B | SoftBank 子公司 SB Energy 為 OpenAI 建 Milam（1.2 GW）及 Ohio 站點並持有硬體；SoftBank 尋求 $40B 貸款支應 | 2025–2026 | [報導:Bloomberg/Dealroom] | https://news.bloomberglaw.com/tech-and-telecom-law/openai-valued-at-852-billion-after-closing-122-billion-round ；https://www.techtimes.com/articles/316807/20260519/openai-cut-stargates-spending-pledge-14-trillion-600-billion-now-renting-what-it-vowed-build.htm |
| 14 | **OpenAI/SoftBank → SB Energy** | 2026-01 合計投資 $1B | SB Energy 為 OpenAI 建 Milam 1.2 GW | 2026-01 | [報導] | https://epoch.ai/blog/openai-stargate-where-the-us-sites-stand |
| 15 | **Altman → Cerebras**（個人） | Altman 為 Cerebras 投資人 | OpenAI 向 Cerebras 採購 >$10B / 750 MW | 2026-01-14 | [報導:Bloomberg] | https://www.bloomberg.com/news/articles/2026-01-14/openai-forges-10-billion-deal-with-cerebras-for-ai-computing |
| 16 | **Anthropic → SpaceX/xAI**（競爭者間） | — | Anthropic 付 ~$1.25B/月（年化 ~$15B）至 2029-05 租 Colossus 1/2；90 天可終止 | 2026-05 | [官方:SpaceX S-1；Anthropic 確認月費] | https://letsdatascience.com/news/anthropic-signs-125b-per-month-colossus-compute-deal-c892b829 |
| 17 | Anthropic → Nscale | — | 報導 $45B 租用 Vera Rubin 算力（Nscale 為 NVIDIA 投資組合公司） | 2026 | [報導] | https://finance.yahoo.com/news/microsoft-nvidia-invest-anthropic-startup-113316065.html |

### 1.2 投資 vs 採購比（「每 $1 投資換回多少採購承諾」）

| 配對 | 投資 | 採購承諾 | 倍數 |
|---|---|---|---|
| Microsoft ↔ OpenAI | ~$13B | $250B（增量） | ~19x |
| Amazon ↔ OpenAI | $50B | $100B | 2x |
| Amazon ↔ Anthropic | 最高 ~$33B | >$100B | ~3x |
| Google ↔ Anthropic | 最高 ~$43B | 5 GW TPU（金額未揭露） | 查不到 |
| Microsoft ↔ Anthropic | 最高 $5B | $30B | 6x |
| NVIDIA ↔ Anthropic | 最高 $10B | $30B Azure（NVIDIA 系統，間接） | ~3x（間接） |
| NVIDIA ↔ OpenAI | $30B 股權 + $105B 租約擔保 | 間接（經雲端） | — |

[估計:本資料庫推算]

---

## 二、融資結構

### 2.1 Meta Hyperion SPV（Blue Owl / Beignet Investor LLC）

| 項目 | 數字 | 標記 | 來源 |
|---|---|---|---|
| 結構 | Blue Owl 持 80%、Meta 持 20%；Meta 長期承租營運；債務不在 Meta 資產負債表上 | [官方/報導] | https://fortune.com/2025/10/31/metas-27-billion-bet-turns-ai-compute-into-wall-streets-hottest-new-investment/ |
| 債券 | **$27.3B**、6.581% 優先擔保票據、2049 到期（23.6 年）；S&P A+ | [官方:發行文件，經 IFR] | https://www.ifre.com/ifr-awards/2327933/financing-package-blue-owl-capitalbeignet-investors-us27.3bn-23.6-year-bond |
| 主要買家 | Pimco ~$18B；BlackRock >$3B | [報導] | 同上；https://www.npr.org/transcripts/nx-s1-5619276 |
| 規模 | Richland Parish, Louisiana，5 GW，總投資 >$50B | [報導] | https://theedgemalaysia.com/node/819893 （2026-10） |
| **二級市場** | 交易價 **91 美分**、殖利率最高 7.55%；利差 ~230bp（發行時 185bp，7 月紀錄 255bp） | [報導:Bloomberg via The Edge, 2026-10] | 同上 |
| Meta CDS | 突破 7 月高點，逼近 100bp | [報導] | 同上 |
| 風險 | S&P 警告建設與營運期「實質信用風險」可能轉回 Meta | [官方:S&P] | 同上 |

### 2.2 Oracle 發債與 CDS

| 項目 | 數字 | 標記 | 來源 |
|---|---|---|---|
| 2025-09 發債 | $18B（當時科技業最大之一） | [官方] | https://www.cnbc.com/2025/12/09/oracles-ai-fueled-debt-load-has-investors-on-edge-ahead-of-earnings.html |
| 2026-02-02 發債 | **$25B**，8 檔、3–40 年；訂單最高 $155B | [官方/報導:IFR] | https://www.ifre.com/bonds/2379081/oracle-returns-with-another-jumbo-bond-to-fund-ai-expansion |
| 2026 融資計畫 | $45–50B（債 + 股）：$5B 強制可轉換特別股（6.5%）+ $20B ATM 普通股；稱 2026 不再發債 | [官方] | https://www.ifre.com/equities/2379787/oracle-takes-bottom-up-approach-to-funding-2026-capex |
| ATM 執行 | Q1 FY27 已出售 $20B 普通股 | [官方:Q1 FY27 財報] | https://www.oracle.com/news/announcement/q1fy27-earnings-release-2026-09-10/ |
| 專案融資 | NM Project Jupiter $18B 銀團貸款（2025-11）；$38B 貸款洽談（2025-11）；Abilene $9.6B 銀行債 + ~$5B 股本 | [報導:Reuters] | https://intuitionlabs.ai/articles/oracle-openai-300b-deal-analysis |
| 總債務 | ~$111.6B（2025-08，含租賃，FactSet）；~$130B；~$167B（定義未明）——**並列，口徑不一** | [報導] | https://www.cnbc.com/2025/12/09/oracles-ai-fueled-debt-load-has-investors-on-edge-ahead-of-earnings.html ；https://startupmap.iamsterdam.com/news/note/oracle-taps-25b-bond-as-debt-hits-130b-and-rating-slips-to-junk-s-edge |
| 信評 | S&P 2026-07 降至 **BBB-**（垃圾級上一階）；Moody's Baa2 負向展望 | [官方:S&P/Moody's，經 Reuters] | https://startupfortune.com/sps-downgrade-leaves-oracle-financing-openais-bet-years-before-it-pays-off/ |
| **5 年期 CDS** | **288bp（2026-10-15，歷史新高）**；一週前 260bp；2026-07-17 198bp；降評後 ~203bp | [報導:S&P Global MI/LSEG 數據] | https://www.securitasglobal.com/risk-perspectives/oracle-cds-record-288-basis-points-ai-debt/ ；https://finance.yahoo.com/markets/stocks/articles/oracles-default-insurance-hits-record-122137367.html |
| RPO | $455B（Q1 FY26）→ $553B（Q3 FY26）→ **$664B（Q1 FY27，2026-08-31）**；約一半 36 個月內轉營收 | [官方] | https://www.oracle.com/news/announcement/q1fy27-earnings-release-2026-09-10/ |
| Q1 FY27 現金流 | CFO $23.1B、CapEx $28.5B、**FCF -$5B**（另報 -$5.4B） | [官方] | 同上；https://www.tikr.com/blog/oracles-ai-boom-has-664-billion-in-backlog-can-its-cash-flow-catch-up-heres-what-its-numbers-are-saying |
| FY27 CapEx | 最高 $90–95B（淨現金 CapEx ≤$70B，客戶預付最高 $25B）——並列 $70B 說法 | [官方/報導] | 同上 |
| 其他 | 股東集體訴訟（2026-02）；內部人出售 ~$1.87B | [報導] | https://www.techtimes.com/articles/316807/20260519/openai-cut-stargates-spending-pledge-14-trillion-600-billion-now-renting-what-it-vowed-build.htm |

> RPO 中 OpenAI 占比：Oracle **未揭露**；以 $300B 合約對 $664B RPO 粗估約 45%。[估計:本資料庫推算]

### 2.3 xAI / SpaceXAI 融資

| 項目 | 數字 | 標記 | 來源 |
|---|---|---|---|
| Series E | $20B @ $230B（2026-01；NVIDIA、Cisco、Tesla 等參與） | [報導:Sacra] | https://sacra.com/c/xai/ |
| GPU SPV（一） | ~$20B lease-to-own：$7.5B 股權（含 NVIDIA 最高 $2B）+ $12.5B 債 | [報導:Bloomberg via Sacra] | 同上 |
| GPU SPV（二） | $5.4B 購 GB200 租給 SpaceX：Apollo 主導 $3.5B 債 + Valor 主導 $1.9B 股 | [報導] | https://jinlow.substack.com/p/what-the-2056-spacex-bond-is-telling |
| SpaceX 併購 | 2026-02 全股票；xAI 估 ~$250B，合併 ~$1.25T（另有 $125B 說法，並列） | [報導:Reuters 等] | https://www.revenuememo.com/p/who-owns-xai |
| SpaceX IPO | 2026-06-12 Nasdaq（SPCX），募 ~$75B，估值 ~$1.75–1.77T | [報導] | https://en.wikipedia.org/wiki/SpaceXAI |
| 新債計畫 | ~$40B（$10B 銀行貸款 + $30B 投資級債），Apollo/Pimco；CDS 據報 194bp 紀錄 | [報導:2026-10，次級] | https://pomegra.io/news/spacex-spcx-q3-2026-earnings-first-profit-in-focus |
| 現金需求 | 2026–2027 最高 ~$120B | [估計:Morgan Stanley] | https://jinlow.substack.com/p/what-the-2056-spacex-bond-is-telling |

### 2.4 CoreWeave 債務與 backlog

| 項目 | 數字 | 標記 | 來源 |
|---|---|---|---|
| Q2 2026 營收 | $2,575M（+112% YoY） | [官方] | https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx |
| Q2 營業損益 | -$49M（GAAP）；調整後 +$128M | [官方] | 同上 |
| Q2 淨損 | -$626M | [官方] | 同上 |
| **Q2 利息費用（淨）** | **$640M**（= 營收的 25%）；Q3 指引 $860–940M | [官方] | 同上；https://www.cnbc.com/2026/08/11/coreweave-crwv-q2-earnings-report-2026.html |
| 總債務 | ~$35.1B（追索 $31.4B + 無追索 $3.7B；本資料庫依資產負債表加總） | [官方] | 同上 |
| Q2 融資 | 毛債務 $13.5B；$3.1B 延遲提款定期貸款；Jane Street $1B 策略投資；>$10B 無擔保債與可轉債（含首檔歐元債） | [官方] | 同上 |
| Backlog | $60.7B（2025 年底）→ ~$99B（Q1 2026）→ **~$104B（2026-06-30）**，另 Q3 初新增 >$25B；TechTimes 報 $129B（並列） | [官方] | 同上；https://www.techtimes.com/articles/324054/20260812/coreweave-q2-2026-129b-backlog-grew-296b-six-weeks-despite-50-default-odds.htm |
| 2026 指引 | 營收 $12.4–13.2B；CapEx $35–39B | [官方:財報會議] | https://www.cnbc.com/2026/08/11/coreweave-crwv-q2-earnings-report-2026.html |
| 電力 | 運轉 1.5 GW；簽約 ~3.7 GW | [官方] | 同上 |
| 違約機率 | 市場隱含違約機率約 50%（標題說法，方法未明） | [報導:TechTimes] | https://www.techtimes.com/articles/324054/20260812/coreweave-q2-2026-129b-backlog-grew-296b-six-weeks-despite-50-default-odds.htm |

### 2.5 私募信貸對資料中心放款

| 項目 | 數字 | 標記 | 來源 |
|---|---|---|---|
| 全球資料中心支出 2025–2028 | ~$2.9T；hyperscaler 自有現金流可支應 ~$1.4T，**融資缺口 ~$1.5T** | [估計:Morgan Stanley] | https://www.morganstanley.com/content/dam/msdotcom/en/assets/pdfs/Research_Bridging-Data-Center-Gap.pdf |
| 其中私募信貸 | **>$800B**（以資產基礎融資為主） | [估計:Morgan Stanley] | 同上 |
| 其中公司債 / 證券化 / 股權與 JV | ~$200B / ~$150B / ~$350B | [估計:Morgan Stanley] | 同上 |
| 表外融資與租賃結構 | ~$3T（NVIDIA、Broadcom、Amazon、Alphabet 等） | [估計:Morgan Stanley，via The Edge] | https://theedgemalaysia.com/node/819893 |
| 已發生私募信貸實際放款總額 | **查不到**權威統計 | — | — |
| 代表案例 | Meta Hyperion $27.3B（Blue Owl/Pimco）；Anthropic TPU 機架 $35B（Apollo）；xAI SPV $12.5B + $3.5B 債（Apollo）；Lambda ~$1B 短期私募債（JPMorgan 安排）；Oracle NM $18B 銀團 | [報導] | 見各節 |

### 2.6 Hyperscaler 發債總額

| 期間 | 數字 | 範圍 | 標記 | 來源 |
|---|---|---|---|---|
| 2020–2024 年均 | ~$28B | 五大（MSFT/GOOGL/AMZN/META/ORCL）美元公司債 | [估計:BofA] | https://finance.yahoo.com/news/ai-hyperscalers-drive-higher-us-225314460.html |
| 2025 | ~$121B | 同上 | [估計:BofA] | 同上 |
| 2026 YTD（至 8/10） | ~$220B | 五大 | [估計:BNP Paribas，via Reuters] | https://mlq.ai/news/hyperscaler-bond-issuance-reaches-about-220-billion-as-ai-financing-costs-rise/ |
| 2026 YTD（至 9 月） | >$180B（美元債） | 五大 + SpaceX | [估計:TwentyFour AM] | https://blog.twentyfouram.com/insights/how-hyperscaler-issuance-is-reshaping-the-treasury-curve |
| 2026 YTD | ~$250B | hyperscalers（Bloomberg） | [報導] | https://theedgemalaysia.com/node/819893 |
| 2026 全年 / 2027 預測 | $250B / $400B | | [估計:Goldman Sachs] | https://finance.yahoo.com/news/ai-hyperscalers-drive-higher-us-225314460.html |
| Amazon 2026 | >$92B 等值（多幣別，至 9 月初） | | [報導] | https://blog.twentyfouram.com/insights/how-hyperscaler-issuance-is-reshaping-the-treasury-curve |
| 發行讓價 | 中位數新發讓價 2.25bp（2025）→ 12bp（2026） | | [估計] | https://www.investing.com/analysis/ai-bond-issuance-tests-the-markets-appetite-for-longdated-tech-debt-200680972 |

> 數字因幣別、截止日、是否含 Oracle/SpaceX 而不同，請勿直接相加。

---

## 三、Neocloud

| 公司 | 營收 | Backlog | 客戶集中度 | 其他 | 標記 / 來源 |
|---|---|---|---|---|---|
| **CoreWeave** | FY2025 $5.13B；Q2 2026 $2.58B；2026 指引 $12.4–13.2B | ~$104B（6/30）+ >$25B（Q3 初） | **Microsoft：35%（2023）→ 62%（2024）→ 67%（2025，應收帳款 68%）**；Q1 2026 最大客戶 45%、第二大 20%（未具名）；管理層目標單一客戶 ≤35% | 大客戶合約：OpenAI 最高 $22.4B；Meta $14.2B（至 2031）+ ~$21B（2026-03，至 2032）≈ $35.2B；Anthropic（2026-04）；NVIDIA $6.3B 回購保證 | [官方:10-K/10-Q；集中度經次級彙整] https://sec-api.io/insights/coreweave-crwv-2026-revenue-analysis-top-customer-concentration-exposure ；https://www.tikr.com/blog/coreweave-revenue-doubled-to-2-1-billion-last-quarter-with-99-billion-in-contracts-already-signed ；https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000222/crwv-20260331.htm ；https://thenextweb.com/news/meta-coreweave-21-billion-ai-cloud-deal |
| **Nebius** | Q2 2026 $582.3M（+454% YoY；另報 $620M 並列）；ARR $3B（6 月底）；2026 指引營收 $3–3.4B、年底 ARR $7–9B | >$40B | Microsoft $17.4–19.4B（2025-09，Vineland NJ，>10 萬顆 GB300）；Meta $3B / 5 年（2025-11） | 調整後 EBITDA $236M（41%）；GAAP 淨損 -$190M；大單預付 50–60% CapEx | [官方/報導:Zacks] https://www.storagenewsletter.com/2026/08/20/nebius-fiscal-2q26-financial-results/ ；https://www.chartmill.com/news/external/121574/nebius-surges-34-post-q2-will-40b-backlog-power-further-growth ；https://www.datacenterdynamics.com/en/news/nebius-signs-3bn-deal-with-meta-says-current-available-capacity-is-sold-out-as-it-targets-25gw-by-end-of-2026/ |
| **Lambda** | 2026 預計 >$1.5B | $15B（6 月）→ **$50B（9 月）** | Microsoft 多十億美元合約（GB300）；NVIDIA 回租 ~$1.5B | 2026-10 擬募最高 $4B（pre $14.5B，Blackstone/Coatue）；IPO 延至 2027 | [報導:Bloomberg/WSJ] https://aiweekly.co/alerts/nvidia-backed-lambda-in-talks-for-3b-pre-ipo-round-at-12b-valuation-as-2026 ；https://letsdatascience.com/news/lambda-pursues-4-billion-pre-ipo-funding-round-909f4022 ；https://datacenterdynamics.com/en/news/microsoft-signs-multi-billion-dollar-cloud-capacity-deal-with-lambda |
| **SpaceXAI（Colossus）** | Anthropic 租金 ~$15B/年 | 至 2029-05 | Anthropic 單一大客戶（90 天可終止） | — | 見 1.1 #16 |
| Nscale | 查不到 | Anthropic $45B（報導）；Microsoft 接手 Narvik 租約 | — | NVIDIA 投資組合公司 | [報導] |

---

## 四、重複計算風險評估

### 4.1 同一筆錢被計算多次的路徑

**路徑 A：股權 → 採購 → 營收（典型循環）**
- Amazon 投資 OpenAI $50B → OpenAI 承諾 AWS $100B → AWS 認列 backlog/營收。Amazon 投出的錢，有相當比例以 AWS 營收形式回流，且同時被計為 (1) OpenAI 融資、(2) AWS backlog、(3) Amazon 的投資資產（未來以評價利得進入淨利）。
- Google 投資 Anthropic → Anthropic 買 TPU → Google Cloud 營收 + backlog $514B；Anthropic 估值上升 → Alphabet 認列鉅額評價利得（Q2 淨利 $112B vs 去年 $28B）。**同一個 Anthropic 成長故事，在 Google 帳上同時出現在營收與非營業利得兩處。**
- Microsoft ↔ OpenAI：OpenAI 2025 年付 Microsoft ~$17.2B（相當於 OpenAI 營收 $13.07B 的 132%），其資金來源大部分是外部股權融資，含 Microsoft 自身早期投資。

**路徑 B：晶片商「投資 / 擔保 / 回購」撐住客戶需求**
- NVIDIA 投資 CoreWeave + $6.3B 回購未售容量 → CoreWeave 用債務買 NVIDIA GPU → NVIDIA 認列營收。若終端需求不足，NVIDIA 自己是最後買家。
- NVIDIA 向 Lambda 回租 GPU，而 Lambda 借錢向 NVIDIA 買 GPU 來履行這份回租合約 —— **NVIDIA 同時是供應商、客戶與股東**。
- NVIDIA 為 OpenAI 的 Ohio 租約擔保最高 $105B（2026-08，10-Q 揭露）：等於 NVIDIA 以資產負債表為 OpenAI 的信用背書，以確保未來 GPU 訂單。這是原 $100B「投資」LOI 失敗後，以「擔保」形式的替代品。
- NVIDIA 權益投資已達 $99B（2026-07），且向客戶回買 $65B 雲端算力（AI cloud $36B + R&D cloud $29B）。
- AMD 以 1.6 億股（約 10%）認股權證換取 OpenAI 6 GW 訂單，另對 Meta 給同等權證 —— 實質是以股權折讓換營收。

**路徑 C：Backlog 層層堆疊**
同一筆 OpenAI 終端支出，可能同時出現在：
1. OpenAI 的「算力承諾」（$1.4T 口徑）；
2. Oracle RPO（$300B / $664B）；
3. Oracle 向 NVIDIA 的 GPU 採購（~$40B）→ NVIDIA 營收；
4. Oracle 向 Crusoe / Vantage / SB Energy 的租約；
5. 若經 CoreWeave：CoreWeave backlog + Microsoft 的 CoreWeave 採購 + Microsoft 對 OpenAI 的 RPO（Microsoft 本身是 CoreWeave 67% 營收來源，而 Microsoft 的部分算力是轉供 OpenAI）。

**粗估規模**：OpenAI 相關的 backlog/RPO 加總 —— Microsoft ~$281B + Oracle ~$300B + AWS $100B + CoreWeave $22.4B + Cerebras $10B ≈ **$700B+**，對照 OpenAI 2026E 營收 $36B 與 2026–2030 累計營收預測 $840B。也就是說，**OpenAI 未來五年預期營收幾乎全數已被既有算力承諾預先「認領」**，而這些承諾的履約能力依賴持續的外部融資（FT：現有資金 2028 年可能耗盡）。[估計:本資料庫推算]

**路徑 D：ARR 毛額 vs 淨額**
- OpenAI ARR $50B（淨額）vs $70B（以 Anthropic 毛額口徑）。若 Anthropic 的 ARR 含經 AWS Bedrock / Google Vertex / Azure 轉售的毛額，則雲端業者的 AI 營收與 Anthropic 的 ARR 之間存在重疊（同一筆客戶付款，雲端認列一次、Anthropic 再以毛額認列一次）。來源：https://finance.yahoo.com/technology/article/openais-annualized-revenue-20-billion-lower-than-prior-investor-estimates-174058048.html

**路徑 E：競爭者互為客戶**
- Anthropic 每月付 SpaceX/xAI $1.25B → 撐起 xAI 外部營收（xAI Q1 2026 AI 分部營收僅 $818M）→ 協助 SpaceX IPO 估值 → SpaceX 發債 $40B 擴建 → 更多 GPU 採購。Anthropic 資金又來自 Amazon/Google 投資。

### 4.2 風險訊號彙整

| 訊號 | 數據 | 意涵 |
|---|---|---|
| 信用市場已開始定價 | Oracle CDS 288bp（新高）、S&P BBB-；Meta Hyperion 債 91 美分；Meta CDS 近 100bp；新發讓價 2.25→12bp | 債權人要求更高補償，融資鏈最脆弱環節是 Oracle、CoreWeave、SPV |
| 客戶集中 | CoreWeave 67% 來自 Microsoft；Microsoft RPO 32–45% 來自 OpenAI；Oracle RPO 約 45% 估來自 OpenAI | 單一模型公司失速會同時擊中多家 |
| 承諾/營收比 | OpenAI 明確合約 ~$682B ÷ 2026E 營收 $36B ≈ 19x | 履約依賴持續融資 |
| 投資承諾縮水 | NVIDIA $100B → $30B；Stargate $1.4T → $600B（公司目標）；Abilene 擴建取消 | 早期頭條數字不應直接計入需求 |
| 晶片商轉為擔保人 | NVIDIA 擔保 $105B 租約、$6.3B 回購保證；Broadcom 擔保 Anthropic $29B 租約 | 需求風險從模型公司轉移到供應商資產負債表 |
| 利息侵蝕 | CoreWeave Q2 利息 $640M = 營收 25%，Q3 指引更高 | neocloud 對利率與續約高度敏感 |

---

## 資料缺口

1. **各雲端 RPO 中 AI 實驗室占比**：僅 Microsoft 曾揭露 OpenAI 占 45%（一次）；Oracle、AWS、Google Cloud 未揭露。
2. **Google 對 Anthropic 累計投資與持股比例**：最新數字查不到（NYT 早期 >$3B / ~14%）。
3. **Microsoft 對 OpenAI 實際累計投資**：$13B 為常見報導數字，未見最新官方確認；2026-03 輪 Microsoft 是否參與未揭露。
4. **Google ↔ Anthropic 5 GW TPU 合約金額**：未揭露。
5. **私募信貸實際已放款總額**：僅 Morgan Stanley 前瞻估計，無實際存量統計。
6. **Oracle 總債務**：$111.6B / $130B / $167B 口徑不一，未從 10-Q 直接核實。
7. **CoreWeave 2026 具名客戶占比**：Q1 2026 最大客戶 45% 未具名；Q2 數字查不到；OpenAI 占 backlog 比例未揭露。
8. **NVIDIA $99B 權益投資明細**：10-Q 未逐一列出 OpenAI、Anthropic、xAI、CoreWeave 等個別帳面值。
9. **AMD 首 GW 是否已交付 / 權證是否已歸屬**：待 AMD Q3 2026 財報（10 月底）。
10. **SpaceX $40B 新債與 CDS 194bp**：僅單一次級來源。
11. **Nscale–Anthropic $45B、Lambda backlog $50B**：僅報導，未見官方確認。
12. **Microsoft–OpenAI 營收分成上限金額**：未揭露。
