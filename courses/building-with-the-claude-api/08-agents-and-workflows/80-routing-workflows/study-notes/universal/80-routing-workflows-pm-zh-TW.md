# Routing Workflows — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.2(agentic 模式 — routing)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 80 |

---

## 一句話總結

Routing 是「檢傷分類台」workflow — 在做真正的工作前,先用一個快速分類器決定哪個專用 pipeline 處理這個請求。當產品處理截然不同的請求類型,且每類都值得不同處理時,就是正確的架構。

---

## 心智模型:醫院檢傷分類台

走進急診室時,你第一個見到的是檢傷護理師。他們問幾個問題決定你去哪裡:

| 檢傷結果 | Pipeline |
|---------|---------|
| 胸痛 | 心臟科 |
| 骨折 | 骨科 |
| 發燒咳嗽 | 一般內科 |
| 精神相關 | 身心科 |

檢傷護理師不是心臟科或骨科醫師 — 他們是分類器。他們把病人送給能真正治療的專科。每個專科都為自己的案件量最佳化,不是為「什麼都做」。

Routing workflow 就是檢傷分類台。一個小分類器 LLM 呼叫決定哪個專用 prompt(或子 pipeline)處理請求。每個專科只做一件事做得很好。

---

## 產品場景

### 適合 Routing 的情境

| 場景 | 為什麼 Routing |
|------|---------------|
| 客服 bot(帳務 / 技術 / 退款)| 每類需要不同的工具、KB、語氣 |
| 內容生成(教育 / 娛樂 / 評論)— 課程範例 | 每類需要不同的風格 |
| 多領域助手(coding / 寫作 / 數學)| 每領域需要不同 context 和 prompt |
| 意圖型 routing(問題 / 任務 / 閒聊)| 不同回應型態、不同延遲預算 |
| 多層級模型選擇 | 簡單請求送 Haiku、複雜請求送 Opus |
| 在地化 pipeline(英 / 中 / 日)| 不同 prompt、在地特定工具 |

### 不適合 Routing 的情境

| 場景 | 更好的選擇 |
|------|-----------|
| 單一請求型態且範圍窄 | 一個 prompt 就好 |
| 分類器無法區分的重疊類別 | Chaining 或 agent |
| 對延遲超敏感(每 ms 都要省)| 跳過分類呼叫,用一個好 prompt |
| 類別不斷變動 | Routing 很脆 — 考慮 agent |

---

## 兩步結構

```
使用者輸入 ──→ [檢傷 LLM 呼叫] ──→ 類別 ──→ [專科 pipeline] ──→ 輸出
```

1. **檢傷呼叫** — 快速、便宜、結構化輸出(一個類別標籤)
2. **專科呼叫** — 較慢、較貴、為該類最佳化

PM 必須在 PRD 明確說明兩次呼叫。各有自己的延遲預算、模型選擇、prompt、eval、fallback 行為。

---

## PM 必須理解的 `tool_choice` 技巧

工程應該用 Claude tool use 搭配 `tool_choice` 強制特定 tool 呼叫來實作分類器。PM 不用寫程式,但要懂為什麼這很重要:

- **可靠度** — 強制結構化 tool call 保證分類器回傳有效類別,不是自由文字「應該是教育類?」
- **安全** — `enum` 清單防止 Claude 發明你的 pipeline 處理不了的新類別
- **Debug** — 結構化輸出容易 log 和檢查

如果工程說「我們會問 Claude 再 parse 回應」,要回推:那很脆。要求用 `tool_choice={"type": "tool", "name": "..."}` + enum schema。

---

## PM 決策框架

| 問題 | 是 | 行動 |
|------|----|------|
| 你的產品處理截然不同的請求類型? | 是 | Routing 候選 |
| 類別可以寫在一頁紙上嗎? | 是 | 類別夠清楚 |
| 每類都能因為專用 prompt 或 tool set 受益? | 是 | Routing |
| Claude(或更便宜的分類器)能可靠分類? | 是 | Routing 可行 |
| 多一次 LLM 呼叫的延遲和成本可接受? | 是 | 出貨 |
| 類別是否大量重疊? | 否 | Routing 才可靠 |

全部是 → routing 是對的選擇。一個「否」通常就否決了。

---

## PM 必須要求的 Production 規格

1. **Enum 限制的 tool 分類器** — 用 `tool_choice` 搭配預定義 enum,不用自由文字
2. **低信心 fallback** — 分類器不確定時,route 到預設/通用 pipeline 或人工審查
3. **Per-category 可觀測性** — log 類別分佈、每類轉換率、每類失敗率
4. **便宜分類器模型** — 分類用小模型(例如 Haiku)降成本
5. **每分支 eval** — 每個專科 pipeline 需要自己的 eval 資料集;通用 eval 會漏掉 per-category 品質下降
6. **濫用保護** — 惡意輸入可能試圖觸發錯誤分支;要驗證類別選擇合理

---

## 業務價值論述

- **品質** — 「每種請求型態都有專屬、最佳化的處理器,而不是一個通用 prompt 應付全部」
- **可擴充** — 「加一個新請求型態 = 加一個新分支,現有型態零回歸風險」
- **成本** — 「簡單請求送便宜模型,複雜請求送頂級模型」
- **延遲** — 「便宜分類 + 聚焦專科常常比慢通用 prompt 還快」
- **可觀測性** — 「我們看得到使用者送哪種請求,哪種表現差」

---

## PM 常見錯誤

1. **類別太多。** PM 愛建分類,分類器討厭分類太多。控制在 10 以下。超過就 chain 或子分類。
2. **類別重疊。** 一個請求可以歸兩類時,分類器會搖擺。定義類別要讓每個請求有唯一歸屬。
3. **沒有 fallback pipeline。** 不要假設分類器一定對。為低信心案件準備預設「通用」pipeline。
4. **把 routing 和 agent 混淆。** Routing workflow 仍是 workflow — 程式碼在分類後挑 pipeline。Agent 則是讓 Claude 自主挑工具。PM 在設計文件中常搞混。
5. **忘了 per-category metric。** 有 routing 的產品需要每類一個 dashboard — 否則看不出哪個分支在退化。

---

> **關鍵洞察**
>
> Routing 是「檢傷分類台」workflow — 先分類,再分派到專科。當你的 app 處理多樣化請求型態、每種都值得聚焦處理時,就是標準產品選擇。Production 關鍵細節是分類器實作:用強制 tool use + enum input schema 保證有效類別標籤。考試記得:**routing 是 workflow(程式碼分派),不是 agent(Claude 決定)。**

---

## CCA 考試關聯

- **D1(22%)主要**: Routing 是四大 workflow 模式之一,預期有情境題。
- **D2(18%)次要**: `tool_choice="tool"` 強制工具使用會被明確測試。
- **D5(20%)次要**: Production 模式 — 便宜分類器模型、每分支 eval、fallback pipeline。
- 訊號字:「categorize」、「classifier」、「dispatch」、「different types of requests」、「specialized pipeline」。
- 陷阱: routing ≠ agent。Routing 是一次分類呼叫後的預定分派。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Routing 的產品定義? | 檢傷步驟分類請求,再由程式碼分派到專用 pipeline |
| 檢傷分類台的類比是什麼? | 護理師問幾個問題後把病人送去心臟科、骨科或一般內科 |
| 為什麼分類器要用強制 tool use? | 從 enum 保證結構化類別標籤,不用 parse 自由文字 |
| PM 設計 routing 功能的關鍵錯誤? | 類別太多或重疊 — 分類器會不可靠 |
| Routing 最必要的 production guardrail? | 低信心分類器輸出的 fallback/預設 pipeline |
| Routing 是 workflow 還是 agent? | Workflow — 程式碼在分類後掌握分派決策 |
| PM 應該要求的成本最佳化? | 分類器步驟用更小/便宜的模型(分類比生成簡單)|
| Routing 產品除了整體品質還需要什麼 metric? | Per-category metric — 類別分佈與每分支失敗率 |
