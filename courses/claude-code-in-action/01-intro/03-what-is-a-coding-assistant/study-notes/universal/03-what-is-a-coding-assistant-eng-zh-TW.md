# What Is a Coding Assistant — 工程師深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (tool interfaces), 2.5 (built-in tools), 1.1 (agentic loops) |
| 來源 | claude-code-in-action / 01-intro / Lesson 03 |

---

## 一句話摘要

Coding assistant 是一個包在 agentic loop 裡的 language model — 它透過 tool use 機制蒐集上下文、規劃步驟、執行動作，因為 LM 本身只能處理文字。

---

## Agentic Loop：助手如何思考


![Agentic Loop Cycle](../../visuals/agentic-loop-cycle-zh-TW.svg)
*圖：Agent 迴圈 — 蒐集上下文、規劃、執行、評估、重複。*

每個 coding assistant 都遵循同一個基本循環：

<!-- diagram: agentic-loop — Task → Gather Context (讀檔、搜尋程式碼) → Plan (拆解步驟) → Take Action (編輯檔案、執行指令) → Evaluate → Loop or Finish -->

1. **蒐集上下文 (Gather context)** — 讀取檔案、搜尋程式碼庫、理解目前狀態
2. **規劃 (Plan)** — 把任務拆成步驟，決定執行哪些動作
3. **執行動作 (Take action)** — 執行工具（讀取、寫入、跑指令）
4. **評估 (Evaluate)** — 檢查任務是否完成；若否，回到步驟一

這不是單次問答。它是一個 **多輪循環**，助手會根據工具回傳的結果持續調整策略。

> 💡 **核心觀念**
>
> Agentic loop 是 coding assistant 與 chatbot 的根本差異。Chatbot 給你一次回應；coding assistant 會持續工作直到任務完成。

---

## Tool Use：連結文字與行動


![Tool Use Bridge Mechanism](../../visuals/tool-use-bridge-mechanism-zh-TW.svg)
*圖：工具使用如何連接文本生成與真實世界動作。*

核心問題：**language model 只能處理和產生文字**。它無法讀檔、跑指令或修改程式碼。它是純粹的 text-in, text-out 函式。

Tool use 是彌補這個缺口的機制：

<!-- diagram: tool-use-flow — 使用者提問 → Coding assistant 把工具說明加入 LM context → LM 用結構化格式回應 (e.g., "ReadFile: main.go") → 助手攔截並執行 → 把檔案內容送回 LM → LM 產生最終回答 -->

**以 ReadFile 為例的完整流程：**

1. 你問：「main function 做了什麼？」
2. Coding assistant 把工具描述加入 LM 的 context
3. LM 用結構化格式回應：`ReadFile: main.go`
4. 助手攔截這個請求，從磁碟讀取實際檔案
5. 檔案內容被送回 LM
6. LM 現在有了真實程式碼，產生有根據的回答

LM 從未接觸過檔案系統。助手是將文字請求轉換為真實動作的中介者。

```
User: "main.go 做了什麼？"
     │
     ▼
┌─────────────────────────┐
│  Coding assistant 把     │
│  工具描述加入 LM context  │
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│  LM 回應：               │
│  "ReadFile: main.go"    │
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│  助手執行：              │
│  從磁碟讀取 main.go      │
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│  檔案內容送回 LM          │
└────────┬────────────────┘
         ▼
┌─────────────────────────┐
│  LM 根據真實程式碼        │
│  產生最終回答             │
└─────────────────────────┘
```

> 🎬 **講師影片觀點**
>
> 講師強調 coding assistant 會「把指令加入 context」告訴 LM 如何請求工具。LM 並非天生知道怎麼呼叫工具 — 它必須透過 prompt/context 學會用助手能解析並執行的結構化格式回應。

---

## 為什麼 Claude 的 Tool Use 不同

並非所有 language model 的 tool use 能力都一樣。Claude 系列（Opus、Sonnet、Haiku）在這項能力上 **特別強**。這很重要，因為：

| 優勢 | 說明 |
|------|------|
| **處理複雜任務** | 強大的 tool use 意味著 Claude 能在多輪對話中可靠地串聯多個工具，不會迷失方向 |
| **可擴充平台** | 因為 Claude 擅長理解工具描述，你可以新增自訂工具，Claude 只需最少設定就能正確使用 |
| **更好的安全性** | Claude Code 不需要預先索引你的程式碼庫。它透過工具按需讀取檔案，你的程式碼不會儲存在任何外部系統 |

> 💡 **核心觀念**
>
> Tool use 的品質是 Claude Code 能作為產品存在的基礎。如果 Claude 的 tool use 平庸，把它包在 agentic loop 裡只會產生不可靠的結果。模型在結構化工具呼叫上的強項才是根基。

---

## 熟悉的類比

| 概念 | 類比 | 為什麼適合 |
|------|------|-----------|
| Tool use | API middleware — 攔截並執行結構化請求 | 助手攔截 LM 的「請求」並轉換為真實動作 |
| 沒有工具的 LM | 顧問能給建議但無法登入你的系統 | 聰明但物理上無法執行任何事 |
| Agentic loop | REPL (Read-Eval-Print Loop) | 持續的輸入、執行、輸出、重複循環 |
| 工具描述 | OpenAPI spec / Swagger 文件 | 告訴消費者有哪些 endpoint、接受什麼、回傳什麼 |
| LM 的工具回應 | HTTP 請求 — 有 method 和 parameters 的結構化格式 | `ReadFile: main.go` 就像 `GET /files/main.go` |

---

## 考試重點：Tool Use 基礎

本課建立了 D1 和 D2 考試的 **基礎心智模型**：

| 考試概念 | 本課教了什麼 |
|---------|------------|
| **Tool interface 設計 (2.1)** | 工具需要清楚的描述，LM 才知道何時、如何使用 |
| **內建工具選擇 (2.5)** | Claude Code 內建 ReadFile、Write、Bash 等工具 — 針對任務選擇正確的工具 |
| **Agentic loop (1.1)** | 蒐集-規劃-執行循環是每個 coding assistant 的架構 |

考試測試的關鍵區別：

- **LM vs. coding assistant** — LM 是大腦；coding assistant 是完整系統（大腦 + 工具 + 循環）
- **工具描述品質很重要** — 描述模糊的工具會被誤用；描述清楚的工具會被正確使用
- **不需索引 = 更好的安全性** — Claude Code 按需讀取，不是從預建索引讀取

> 🎯 **考試提醒**
>
> 當題目問「coding assistant 內部如何運作」，答案圍繞 agentic loop + tool use 機制。不要與 prompt engineering 混淆 — tool use 是一個 **架構** 模式，不是 prompting 技巧。

---

## 練習題

### Q1: Tool Use 機制

一位初級工程師問：「如果 language model 只能處理文字，Claude Code 怎麼讀取檔案？」哪個解釋最準確？

- A. Claude Code 會預先把整個程式碼庫索引到模型的訓練資料中
- B. Language model 產生結構化的工具請求，coding assistant 攔截、在檔案系統上執行，再把結果回傳給模型
- C. Claude Code 使用另一個專門訓練來讀檔的較小模型
- D. Language model 透過內建 API 直接存取檔案系統

<details><summary>答案</summary>

**B** — 這正是課程描述的機制。LM 產生結構化請求（如 `ReadFile: main.go`），助手執行它，再把內容送回。

- A 錯誤 — Claude Code 不做預先索引；這被明確指出是安全優勢
- C 錯誤 — 沒有獨立的讀檔模型
- D 錯誤 — LM 無法直接存取任何東西；它們是 text-in, text-out

考試哲學：**Architecture > Prompt** — tool use 是結構性機制，不是 prompt 技巧
</details>

### Q2: 透過 Tool Use 實現擴充性

你的團隊想為 Claude Code 增加一個自訂的資料庫查詢工具。根據本課描述的 tool use 機制，成功的最關鍵因素是什麼？

- A. 用資料庫查詢範例微調模型
- B. 撰寫清楚的工具描述，讓模型知道何時以及如何請求資料庫查詢
- C. 預先載入所有資料庫 schema 到模型的 context window
- D. 為每種可能的查詢模式建立 few-shot 範例

<details><summary>答案</summary>

**B** — 課程解釋 coding assistant 把工具描述加入 LM 的 context，LM 根據這些描述學會使用工具。清楚的描述是正確使用工具的關鍵。

- A 不必要 — Claude 不需微調就能處理 tool use
- C 不切實際且浪費 context window
- D 無法擴展，效果也不如好的工具描述

考試哲學：**Tool description > Few-shot** — 好的工具介面描述比範例更有效
</details>

### Q3: 安全架構

一個重視安全的組織正在評估 Claude Code，他們擔心程式碼外洩。根據本課，關於 Claude Code 架構的哪個說法正確？

- A. Claude Code 需要把整個程式碼庫上傳到 Anthropic 的伺服器進行索引
- B. Claude Code 建立本地向量資料庫進行語義搜尋
- C. Claude Code 透過 tool use 按需讀取檔案，不需要預先索引或外部儲存
- D. Claude Code 只能處理在對話中明確分享的程式碼

<details><summary>答案</summary>

**C** — 課程明確指出 Claude Code 基於工具的架構不需要預先索引。檔案在模型透過 tool use 機制請求時按需讀取。

- A 與 Claude Code 的運作方式相反
- B 描述的是 RAG 方法，不是 Claude Code 的運作方式
- D 過於限制 — Claude Code 可以透過工具讀取任何檔案，不只是對話中的內容

考試哲學：**Proportionate response** — 在做安全評估前先理解實際架構
</details>
