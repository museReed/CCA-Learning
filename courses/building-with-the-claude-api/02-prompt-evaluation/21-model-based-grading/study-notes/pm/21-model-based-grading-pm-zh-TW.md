# 模型評分 Model-Based Grading — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任務聲明 | 3.4（LLM-as-judge 評分）、3.3（測試案例執行）、5.4（eval 驅動迭代） |
| 來源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 21 |

---

## 一句話重點

Model-based grading 就是把「這個 AI 輸出感覺不錯嗎？」變成 dashboard 上的一個數字 —— 讓 prompt engineering 不再靠 vibes，而是變成可衡量的產品 workflow。

---

## 為什麼 PM 要在意

沒有評分 eval，每次改 prompt 都是信仰之躍。有人動一下 system prompt、看十筆輸出、就上線。下列基本問題根本答不出來：

- 這週的 prompt 改動到底有沒有提升 helpfulness？
- 新指令是不是搞壞了 completeness？
- 我們是不是在不知情的狀況下退化了 safety？

Model-based grading 給你**每個 prompt 版本的品質指標** —— 一個可以像 DAU 或 conversion rate 一樣隨時間繪製的數字。它把 prompt engineering 從手藝變成工程。

---

## 心智模型：餐廳評論家

把三種 grader 想成三種餐廳評論系統：

| Grader 類型 | 餐廳比喻 | 優點 | 缺點 |
|-------------|----------|------|------|
| **Code grader** | 帶檢查表的衛生稽查員 | 快、便宜、100% 一致 | 只能檢查規則、不能判斷味道 |
| **Model grader** | 用 email 寫評論的 freelance 美食評論家 | 能判斷味道、可便宜擴展 | 每次造訪意見略有不同 |
| **Human grader** | 親自到場的米其林密探 | 最深入、最細膩 | 慢又貴 |

真正的連鎖餐廳三種都用。PM 在打造 AI 功能時也該如此：code graders 做規則遵守、model graders 做體驗品質、high stakes（安全、法務、品牌）時用 human graders。

---

## 產品使用情境

### 何時用 Model Graders

| 情境 | 為什麼 model grader 適合 |
|------|-------------------------|
| 「這個客服回應有沒有幫上忙？」 | Helpfulness 是代碼無法判斷的主觀題 |
| 「AI 有沒有照我們的指令做？」 | 指令遵循是語義層面的問題 |
| 「這個摘要完整嗎？」 | Completeness 取決於意義，不是字數 |
| 「這個回應感覺安全、符合品牌嗎？」 | 語氣與安全需要 model 的判斷 |

### 何時**不要**用 Model Graders

| 情境 | 更好的替代 |
|------|-----------|
| 「輸出是不是合法的 JSON？」 | 用 code grader —— deterministic 且免費 |
| 「回應是不是 200 字以內？」 | 用 code grader —— 很瑣碎 |
| 「答案是不是跟已知正解相符？」 | 用 code grader 做字串比對 |
| 「這個有沒有違反我們最敏感的政策？」 | 棘手 case 走 human graders |

---

## 每個 PM 該爭取的那一招

來源的 grader prompt 依序要求 model 回傳四件事：

1. Strengths（1-3 項）
2. Weaknesses（1-3 項）
3. Reasoning（簡短解釋）
4. Score（1-10）

這是**整課最重要的設計決策**。來源指出：沒有 strengths 和 weaknesses，model graders 都會打 6 分 —— 追蹤改善完全沒用。

PM 應該堅持保留這個結構，即使工程端壓力要求「簡化 grader」。strengths 和 weaknesses 也直接可用作 PM 的產物：變成 prompt 修改 backlog，reasoning 也讓 CS 和 QA 在退化時能追溯原因。

---

## PM 決策框架

當團隊提議加 model-based grading，請問：

| 問題 | 若答 Yes | 行動 |
|------|---------|------|
| 我們有寫下清楚的評分標準嗎？ | Yes | 繼續 —— grader 需要先有標準 |
| 要衡量的品質維度是主觀的（helpfulness、completeness）？ | Yes | Model grader 是對的選擇 |
| 要衡量的品質維度是 deterministic（valid JSON、長度）？ | Yes | 改用 code grader |
| 我們在乎**絕對**分數嗎？ | No | 很好 —— 信 delta，不信絕對數字 |
| reasoning 欄位有 log 而且可 review？ | Yes | 繼續 —— 這是評分可追溯的關鍵 |

---

## 常見 PM 錯誤

1. **把 grader 分數當 ground truth** —— model graders 有隨機性。要信 prompt 版本之間的 delta，不要信絕對數字。
2. **跳過標準定義** —— 跟工程說「直接評就好」會產出一個到處打 6 分的 grader。一定要先定 rubric。
3. **沒預留 grader 迭代預算** —— grader 本身也是個 prompt，需要調。要排週期給它。
4. **該用 code grader 卻用 model grader** —— 浪費 token、拖慢迭代。規則類檢查一律優先 code grader。
5. **沒記錄 reasoning** —— 分數意外時，你需要辯護理由才能跟工程或 QA debug。

> **關鍵洞察**
>
> Model-based grading 把 prompt engineering 從手藝變成產品 workflow。Grader 本身不是 feature —— grader 是**量測儀器**，讓你有信心改善真正的 feature。懂這點的 PM 能在幾週內交付品質提升；跳過這步的 PM 只能交付 vibes 和希望。

---

## CCA 考試相關性

- **D3（Evaluation）**：Model-based grading 是 LLM-as-judge 的範式。要知道何時選 model vs code vs human，以及 grader prompt 必須包含什麼（strengths、weaknesses、reasoning、score）。
- **D5（Enterprise Deployment）**：Graders 支撐 eval 驅動迭代 —— 考題會圍繞生產環境量測 prompt 改善。
- 注意：「你要衡量 helpfulness / instruction following / completeness」→ model grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Model-based grading 解決什麼產品問題？ | 把主觀的 AI 輸出品質變成 PM 可繪製、可迭代的數字。 |
| 三種 grader 類型是什麼？ | Code graders、model graders、human graders。 |
| PM 何時該選 model grader 而非 code grader？ | 當品質維度是主觀的 —— helpfulness、completeness、instruction following、safety。 |
| 為什麼 model grader 必須回傳 strengths 和 weaknesses，而不只是分數？ | 沒有它們，model 會退化到 6 分左右，指標失效。 |
| 三種 grader 的餐廳比喻？ | 衛生稽查員（code）、freelance 美食評論家（model）、米其林密探（human）。 |
| PM 該信哪種分數 —— 絕對或 delta？ | Prompt 版本之間的 delta —— model graders 絕對值有隨機性。 |
| Model graders 擅長哪些維度？ | Response quality、instruction following、completeness、helpfulness、safety。 |
| grader 到底是 feature 還是量測儀器？ | 量測儀器 —— 它存在的目的是讓你有信心改善真正的 feature。 |
