# Temperature — PM 視角

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（模型設定）、5.3（production 模式）、5.4（evaluation 與可靠度） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 11 |

---

## 一句話總結

Temperature 是 Claude 的「創意旋鈕」——它控制使用者看到回應的變異程度。身為 PM，為每個 feature 選對 temperature，就是你把輸出行為對齊使用者期望的方式：事實任務用可預測的，創意任務用多變的。

---

## 心智模型：廚師類比

想像在餐廳點餐：

| Temperature | 廚師行為 | 食客期望 |
|-------------|---------|---------|
| 0.0 | 每次都照食譜做出完全一樣的菜 | 「我要招牌牛排——和上次一模一樣」 |
| 0.5 | 照食譜做但加入小而有品味的變化 | 「按你的風格來，但保持招牌味」 |
| 1.0 | 自由即興——每盤都是新創作 | 「驚喜我——主廚選擇，永遠不一樣」 |

如果食客點的是醫療處方卻拿到「主廚選擇」，那是災難。如果食客點的是 tasting menu 卻每晚拿到同一道菜，那很無趣。Temperature 是這個 feature 要給使用者哪種體驗的產品決策。

---

## 為什麼 PM 要在乎

Temperature 是少數幾個**直接形塑使用者體驗**的 Claude 參數。它不是技術細節——它是產品政策。

- **低 temperature** = 產品承諾*一致性與可靠*
- **高 temperature** = 產品承諾*多樣與驚喜*
- **中 temperature** = 產品承諾*品質帶點人味*

如果你的資料抽取功能每次回傳不同 JSON 結構，使用者會失去信任。如果你的 brainstorming 工具每次造訪都回傳同樣三個點子，使用者會不再打開它。Temperature 是修復這兩者最簡單的槓桿。

---

## 產品使用情境

### 低 Temperature (0.0 – 0.3)

| 產品 | 為什麼低？ |
|------|-----------|
| 支援工單分類 | 同輸入必須得到同 label |
| 發票資料抽取 | 下游系統預期確定性欄位 |
| 醫療 / 法律說明 | 措辭變異可能有法律風險 |
| Code 助手 | 使用者預期同 bug 拿到同 fix |
| 內容審核 | 一致性是公平性要求 |

### 中 Temperature (0.4 – 0.7)

| 產品 | 為什麼中？ |
|------|-----------|
| 會議摘要 | 連貫結構 + 自然措辭 |
| 家教解說 | 一致教學法帶人聲 |
| Email 草稿助手 | 事實為根但不機械 |
| 知識庫回答 | 可靠事實加可讀變化 |

### 高 Temperature (0.8 – 1.0)

| 產品 | 為什麼高？ |
|------|-----------|
| Brainstorming / 發想工具 | 使用者要很多不同點子 |
| 行銷文案生成器 | 新穎就是全部意義 |
| 命名 / slogan 生成器 | 多樣性 > 精確 |
| 虛構 / 遊戲對白 | 驚喜驅動 engagement |

---

## PM 決策框架

規劃 AI feature 時問四個問題：

1. **同樣輸入需要產生同樣輸出嗎？** → 低 temperature。沒有例外
2. **下游 parser 或 automation 會消費這個輸出嗎？** → 低 temperature。變異會打破 pipeline
3. **使用者會把兩次執行並列比較嗎？** → 低或中。不一致會被當成 bug
4. **多樣性是價值主張的一部分嗎？** → 高。鎖死

把答案寫進 PRD，當作驗收標準的一部分。「Temperature: 0.2, fixed」是真實的產品需求，不是調校細節。

---

## Temperature 修不了什麼

Temperature 是 sampling 旋鈕，不是品質修復。當真正的問題是下列時，不要伸手抓它：

- **壞 prompt** → 先改 prompt；temperature 是第二層
- **缺少 context** → 加 retrieved data 或 tools；temperature 無法捏造事實
- **模型尺寸不對** → 輸出真的不夠聰明就升級 model 階層
- **Persona 不一致** → 那是 system prompt 的工作，不是 temperature

常見失敗模式：PM 在 production 看到「hallucination」，把 temperature 降到 0 上線。Hallucination 是壞 prompt 造成的，不是 temperature。這個 fix 毫無作用。

---

## 常見 PM 錯誤

1. **所有功能都讓 temperature 停在預設 1.0**——對 chat 很好，對抽取很糟。每個 feature 要選
2. **把低 temperature 和高準確度搞混**——它只代表低變異。一致的錯答案還是錯
3. **沒在 PRD 指定 temperature**——工程師會選一個他們覺得順手的，你會在上線後繼承這個不一致
4. **沒改 prompt 就做 temperature 高 vs 低的 A/B test**——你可能在測錯的變數
5. **在法律敏感文案用高 temperature**——它總有一天會生成 off-brand 的東西，你會在會議室裡被約談

> **Key Insight**
>
> Temperature 是產品政策決策，不是工程調校旋鈕。它編碼的是你和使用者關於「能預期多少變異」的契約。刻意決定它、寫進 PRD、每個 feature 鎖死。最糟的結果是因為 temperature 由「第一個寫 code 的人」決定而產品不一致。

---

## CCA 考試重點

- **D5 (Enterprise Deployment)**：temperature 是標準 production 設定參數。預期會考情境題，問給定產品該用哪個區段
- 注意「如何確保分類輸出一致？」這種問法——答案是低 temperature
- 注意「如何生成多樣的行銷文案變體？」這種問法——答案是高 temperature

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 在產品層面，temperature 控制什麼？ | 使用者看到回應的變異程度——低 = 一致，高 = 多變 |
| 資料抽取工具該用哪個 temperature 區段？ | 低（0.0–0.3）——確定性是產品需求 |
| Brainstorming 工具該用哪個 temperature 區段？ | 高（0.8–1.0）——多樣性就是價值主張 |
| 會議摘要該用哪個 temperature 區段？ | 中（0.4–0.7）——連貫但自然 |
| 低 temperature 等於高準確度嗎？ | 不等於——它只代表低變異。可重複的錯答還是錯 |
| Temperature 該寫進 PRD 嗎？ | 應該——它是產品政策，不是工程調校細節 |
| Temperature 0 vs 1 的廚師類比是什麼？ | 0 = 招牌菜每次完全一樣；1 = 主廚選擇，從不相同 |
| Temperature 修不了哪些產品問題？ | 壞 prompt、缺 context、錯 model、persona drift。Temperature 是第二層 |
| 為什麼法律 / 醫療文案用 temperature 1.0 危險？ | 罕見不尋常措辭可能有法律風險；你要的是一致性，不是創意 |
