# System Prompts — PM 視角

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（模型選擇與設定）、5.3（production 模式）、1.2（agentic loop 基礎） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 09 |

---

## 一句話總結

System prompt 是你在每段對話開始時交給 Claude 的「職位說明」——它把泛用 AI 變成你產品的專屬 persona，是 PM 對輸出品質與品牌一致性最有槓桿的單一控制點。

---

## 為什麼 PM 要在乎

沒有 system prompt，你產品裡的每個使用者都在跟同一個通用 Claude 對話——任何人在 Claude.ai 都拿得到。這不是產品，這是一層薄薄的 wrapper。System prompt 才是你差異化的所在。

| 沒有 system prompt | 有精心設計的 system prompt |
|--------------------|----------------------------|
| 泛用、有幫助但不具體的回應 | 品牌語氣、一致的 tone |
| 直接給答案，跳過使用者旅程 | 圍繞使用者目標設計的體驗 |
| 跟其他 Claude 整合行為一模一樣 | 差異化的產品行為 |
| 沒有 guardrails——無關問題照答 | 有範圍限制、優雅拒絕 |
| 格式不可預測 | 可靠、可解析的結構 |

數學家教的例子很說明問題。沒有引導的話，Claude 對「5x + 2 = 3」會直接給答案。真正的家教產品不要這樣——它要的是**教學體驗**，不是答案。System prompt 就是你編碼「這是家教，不是計算機」的地方。

---

## 心智模型：新人 Onboarding 簡報

想像你聘了一位世界級顧問。他很聰明，但第一天對你公司、客戶、品牌語氣一無所知。你會怎麼做？你會給他一份 onboarding 簡報：

- 「你是一家企業 SaaS 公司的 lead customer success manager」
- 「我們的 tone 是友善但專業——絕不用 emoji，永遠用客戶名字署名」
- 「絕不承諾無法驗證的時程」
- 「這是我們最強 CSM 寫的三封範例信——照這個風格」

那份簡報就是 system prompt。Claude 收到的每個使用者查詢都是一封新的客戶信——簡報形塑每封回覆的樣子。

---

## 產品使用情境

### 什麼時候 System Prompt 是關鍵

| 情境 | 為什麼 system prompt 重要 |
|------|---------------------------|
| 客服 chatbot | 品牌語氣、升級規則、知識邊界 |
| 數學 / 語言家教 | 教學立場（引導而非直接解答） |
| 法律 / 醫療助理 | 硬 guardrails、免責聲明、範圍限制 |
| Code review 工具 | 技術 persona、嚴重度標準、輸出 schema |
| 內部 HR bot | 以公司政策為真相來源、隱私規則 |

### 什麼時候 System Prompt 沒那麼重要

| 情境 | 原因 |
|------|------|
| 通用 ChatGPT 式 playground | 使用者預期看到原味 assistant 行為 |
| 一次性研究查詢 | 沒有可重複的 workflow 要編碼 |
| PMF 前的原型 | 迭代速度勝過 persona 打磨 |

---

## 每個 Production System Prompt 都需要的五件事

1. **身份**——「You are ...」Claude 要扮演誰？
2. **任務範圍**——什麼在範圍內？什麼在範圍外？
3. **語氣 & 格式**——Tone、長度、結構、是否用 markdown
4. **Guardrails**——安全、隱私、法律、品牌的硬規則
5. **範例**——一兩個黃金標準輸出，錨定風格

如果你的 system prompt 缺了這五個其中任何一個，就有一個品質 bug 在等著發生。

---

## PM 決策框架

在規劃新的 AI 功能時，問這些問題：

| 問題 | 如果答 Yes | 意涵 |
|------|-----------|------|
| 這個功能有特定 persona 或 role 嗎？ | Yes | System prompt——明確定義 |
| 有 Claude 該拒絕的主題嗎？ | Yes | System prompt——編碼拒絕規則 |
| 有必須的輸出格式（JSON、markdown、條列）嗎？ | Yes | System prompt——指定結構 |
| 需要品牌語氣一致性嗎？ | Yes | System prompt——鎖定 tone |
| 多輪對話中行為要保持穩定嗎？ | Yes | System prompt——持續性 context |
| Context 每個使用者 / 每個查詢都不同嗎？ | Yes | **不是** system prompt——放在 `messages` |

最後一列是大多數 PM 會踩的陷阱：把每位使用者的資料塞進 system prompt，因為「指令應該放那」。動態 context 屬於 `messages`，不是 `system`——否則你會破壞 prompt caching 並浪費錢。

---

## 常見 PM 錯誤

1. **把 system prompt 當作一次性產出**——它是產品。版本化、A/B 測試、量化回歸。品質下降時，第一個要看的就是 system prompt
2. **寫模糊的指令**——「要有幫助又友善」沒用。「永遠用三個條列回覆、總字數不超過 40 字、絕不用驚嘆號」才可執行
3. **把動態資料塞進 system prompt**——每位使用者的 context 要放 messages，caching 才能生效
4. **沒在 PRD 指定 system prompt**——工程師會寫一個預設的，而且一定跟你想像的不一樣。把 system prompt 列為驗收標準
5. **把使用者請求複製進「system message」**——system prompt 是環境規則，不是當前任務。混了就不可預測

> **Key Insight**
>
> System prompt 是你唯一能確保 Claude 表現得像*你的*產品，而不是通用 assistant 的地方。它是 PM 在 AI 功能上能擁有的最高槓桿製品——槓桿比 model 選擇、temperature、甚至 tool 選擇都還大。如果你把它外包給沒有產品 context 的工程師寫，你的功能就會感覺像 Claude 的 wrapper，而不是產品。

---

## CCA 考試重點

- **D5 (Enterprise Deployment)**：system prompt 是在企業部署中強制行為一致性的標準 production 機制
- **D1 (Agentic Architecture)**：system prompt 是每個 agent 穩定的身份層，貫穿 tool-use loops
- 注意「如何強制品牌語氣 / 拒絕規則 / 輸出格式？」這種情境——考試答案一定是 system prompt，不是逐條 message engineering

---

## Flashcards

| 題目 | 答案 |
|------|------|
| System prompt 的 PM 級定義是什麼？ | 你交給 Claude 的「職位說明」或 onboarding 簡報——定義整段對話的 persona、範圍、語氣、guardrails |
| Production system prompt 的五個核心元素？ | 身份、任務範圍、語氣 & 格式、guardrails、範例 |
| 為什麼每位使用者的資料不該放 system prompt？ | 因為 system prompt 應該穩定且可 cache；每位使用者的資料要放 `messages`，caching 才有效且 context 可隨 turn 演化 |
| 沒寫 system prompt 最大的產品風險是什麼？ | 你的功能會變成通用 Claude 的薄 wrapper——沒有差異化、語氣不一致、沒有 guardrails |
| 在數學家教產品中，system prompt 防止什麼？ | 防止 Claude 直接給答案，強制逐步 Socratic 引導 |
| 「要有幫助」該放進 system prompt 嗎？ | 不該——它模糊且沒有實際約束。具體、可測試的規則（「永遠最多三個條列」）才是能提升品質的 |
| 團隊裡誰該擁有 system prompt？ | PM——它編碼的是產品意圖。工程師實作；PM 定義契約、版本化、A/B 測試 |
| System prompt 設計最直接對應 CCA 哪個 domain？ | D5 Enterprise Deployment——它是在規模下強制 production 級一致性的方式 |
