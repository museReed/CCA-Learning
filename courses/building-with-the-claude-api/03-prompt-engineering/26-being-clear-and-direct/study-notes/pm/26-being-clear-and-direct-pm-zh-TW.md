# Being Clear and Direct — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 設計與迭代）、1.1（指令遵循） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 26 |

---

## 一句話總結

寫 prompt 就像寫 design brief——用祈使動詞開頭、講清楚要什麼交付物，不要用客氣的問句。

---

## PM 為什麼該在乎

Prompt 的第一行就像 PRD 或 design brief 的第一句。如果工程師或設計師從第一句看不出要產什麼，後面整份文件都在救火。Claude 也一樣。這堂課顯示：單一最高槓桿的 prompt 編輯——把第一行從問句改成祈使句——在 10 分制 eval 上帶來可量測的分數跳升（2.32 → 3.92）。這個產品品質 delta 比大多數 A/B test 看得到的還大，而且只要改一句話。

---

## 心智模型：Design Brief

比較弱 vs 強 brief 對設計師的落地感：

| Brief 風格 | 設計師反應 | Claude 反應 |
|-----------|-----------|-------------|
| 「我們在想或許可以重做 onboarding flow，感覺怪怪的？」 | 「好喔……你到底想要什麼？」 | 產出模糊回應，要求澄清或猜範圍 |
| 「Redesign onboarding flow，目標降低 step 2 drop-off。交付物：3 個 Figma frame，週五前。」 | 「收到，開始了。」 | 產出對齊的結構化 artifact |

Prompt 就是 brief，Claude 是合作者。動詞+交付物開頭的 brief 永遠贏過用 context 或問句開頭的 brief。

---

## 兩個原則翻成產品語言

| 原則 | 定義 | PM 翻譯 |
|------|------|---------|
| **Clarity** | 簡單語言、對要什麼沒有模糊 | User story：「As a X, I want Y so that Z」，沒人要用猜的 |
| **Directness** | 指令而非問句、action verb 開頭 | Acceptance criteria：「Given / When / Then」，祈使、可測 |

PM 如果已經會寫好 Jira ticket，其實已經會寫 clear and direct 的 prompt。能力可以 transfer。

---

## 產品應用場景

### 什麼時候 clarity + directness 是第一個要改的

| 功能 | 症狀 | 修法 |
|------|------|------|
| AI 摘要長度不一致 | Prompt 問「Can you summarize this?」 | 改：「Write a 3-sentence summary covering the main argument, supporting evidence, and conclusion.」 |
| AI 寫手太話嘮 | Prompt 用問句開頭 | 改祈使：「Draft a professional email declining the meeting.」 |
| 內部文件抽取漏欄位 | Prompt 說「Tell me about the contract」 | 改：「Extract the effective date, party names, and total value from the contract.」 |

### 什麼時候這招不夠

光靠 clarity and directness 有上限——課程只跑到 3.92/10。要再上去需要 specificity（Lesson 27）、examples、structure。把 clear+direct 當成**最小可用 prompt**，不是最終產品。

---

## PM 決策框架

在 PRD review 看團隊的 AI prompt 時問：

| 問題 | 如果 No，就 flag |
|------|------------------|
| 第一行是動詞開頭嗎？ | Flag——改祈使句 |
| 從第一句看得出 Claude 會產什麼嗎？ | Flag——brief 不清楚 |
| 有保留語嗎（「maybe」「if possible」「could you」）？ | Flag——拿掉 |
| Prompt 有指定輸出格式或長度嗎？ | Flag——加 constraint |
| 新進同事看第一行不需 context 就懂嗎？ | Flag——簡化用字 |

本質上就是對 prompt 做一次 PRD lint。

---

## 隱藏的產品勝利

Clear + direct prompt 不只分數比較高——它**失敗得更可預測**。模糊 prompt 可以用一百種方式失敗（太長、太短、主題跑掉、格式錯、太話嘮、離品牌調性）。祈使 prompt 只用一種方式失敗：要的 artifact 在某個具體、可除錯的點錯了。

可預測的失敗是產品資產。QA 可以寫針對性測試、on-call 看得出 bug 形狀、eval rubric 也跟得上。

---

## 常見 PM 錯誤

1. **太客氣的 prompt** — 「Could you please kindly...」PM 常把 AI prompt 當成寫信給陌生人。Claude 不需要禮貌，它需要清楚。
2. **Context 前置** — 把指令埋在三句背景後面。指令先、context 後。
3. **用問不用命** — 把 Claude 當成可能拒絕你。它不會，直接下祈使句。
4. **覺得「太簡單所以跳過」** — 課程測出一行改動 +1.6 分，不要跳過簡單的勝利。
5. **以為 clear+direct 就結束了** — 這是地板不是天花板，上面還需要 specificity 和 examples。

> **Key Insight**
>
> AI 功能裡最便宜的產品品質勝利，就是把每個 prompt 的第一行改寫成動詞開頭的祈使句。零工程成本、可量測的分數提升、讓功能失敗模式變可預測。PM 在 review AI prompt 時第一個該 audit 的就是第一行。

---

## CCA 考試相關性

- **D3 (Evaluation & Iteration)**：「問句 → 祈使句」是 prompt 改進迴圈中最便宜的第一步。
- **D1 (Agentic Architecture)**：同一條規則套用到 agent system prompt——先祈使，再 preamble。
- 考題給弱 prompt 時，改寫成祈使句的版本通常就是正解。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 第一個該 audit 的是 prompt 哪部分？ | 第一行——它定調且影響回應品質比其他部分都大。 |
| 跟 clear-and-direct prompt 類比的 PM 產物是什麼？ | 好的 design brief 或 Jira ticket——動詞開頭、有具體交付物、不保留。 |
| 光靠 clarity + directness 量到的分數進步？ | 2.32 → 3.92 的 +1.6 分，改一行來的。 |
| 為什麼模糊 prompt 的產品風險不只是品質？ | 因為它失敗模式不可預測，無法 debug、測試、預防。 |
| 「Design brief」類比？ | 模糊 brief 讓設計師用猜的，動詞+交付物 brief 可以立刻開工；Claude 一樣。 |
| 列三個 PM 該從 prompt 移除的保留語？ | 「Maybe」「if possible」「could you」，任何讓指令看起來選配的字。 |
| Clear and direct 夠用嗎？ | 不夠，這是地板。還需要 specificity、examples、structure 才能拿高分。 |
