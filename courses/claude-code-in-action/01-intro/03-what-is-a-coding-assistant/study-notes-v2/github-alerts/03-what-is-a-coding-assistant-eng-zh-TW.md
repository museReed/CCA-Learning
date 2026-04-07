# What is a Coding Assistant? — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1: Agentic Architecture & Orchestration, D2: Tool Design & MCP Integration |
| Task Statements | 1.1 (agentic loops), 2.1 (tool interfaces), 2.5 (built-in tools) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE]
> 本節所有內容均直接來自官方課程教材（影片字幕 + 講師投影片）。

## One-Liner / TL;DR

Coding assistant 是一個代理式系統，將語言模型包裝上工具 — 使其能夠蒐集上下文、制定計畫，並對真實程式碼庫採取行動。

## Core Concepts

### Coding Assistant 究竟是什麼

Coding assistant 不僅僅是一個寫程式碼的工具。它是一個使用語言模型來處理複雜程式設計任務的精密系統。關鍵洞察：語言模型本身無法進行程式設計 — 它需要一個編排層（orchestration layer）將它連接到外部世界。

### Coding Assistant 的運作方式 — 三步驟循環

當你給 coding assistant 一個任務（例如：根據錯誤訊息修復 bug），它會遵循以下循環：

| 步驟 | 動作 | 細節 |
|------|------|------|
| 1 | **蒐集上下文（Gather context）** | 理解錯誤指向什麼、哪些檔案相關、閱讀堆疊追蹤、檢查相關程式碼 |
| 2 | **制定計畫（Formulate a plan）** | 決定如何解決問題 — 模型推理最佳方法 |
| 3 | **採取行動（Take action）** | 實施解決方案 — 寫程式碼、執行命令、修改檔案 |

> [!IMPORTANT]
> 第一步（蒐集上下文）和最後一步（採取行動）都需要助手**與外部世界互動**。這是根本的挑戰 — 也是工具使用（tool use）存在的原因。

### Tool Use 的挑戰

語言模型本身只能處理文字並返回文字。它們無法：
- 從檔案系統讀取檔案
- 執行 shell 命令
- 寫入檔案
- 存取網路

如果你直接問一個語言模型「讀取 main.go 的內容」，它會告訴你它做不到。模型無法存取你的檔案系統 — 它只能操作它收到的文字。

### Tool Use 的運作方式 — 五步驟流程

這是連接純文字模型與真實世界程式設計之間的橋樑機制：

| 步驟 | 發生什麼事 |
|------|-----------|
| 1 | **你提問**：「main.go 檔案裡寫了什麼程式碼？」 |
| 2 | **Coding assistant** 在你的請求後附加工具指令（告訴模型有哪些工具可用以及如何調用） |
| 3 | **語言模型回應**：`ReadFile: main.go`（結構化的工具呼叫，不是自然語言回答） |
| 4 | **Coding assistant** 攔截此回應，從磁碟讀取實際檔案，並將檔案內容傳回模型 |
| 5 | **語言模型**根據真實的檔案內容提供最終回答 |

這個系統讓語言模型能有效地「讀取檔案」、「寫程式碼」和「執行命令」— 即使它們本質上是文字進、文字出的系統。

> [!NOTE]
> **「Tool use」**是標準術語。所有與外部系統互動的語言模型都以這種方式運作 — 這不是 Claude 獨有的，但 Claude 在這方面特別強。

### 為什麼 Claude 的 Tool Use 很重要

Claude（Opus、Sonnet、Haiku）在 tool use 方面特別強。這帶來三個具體好處：

| 好處 | 說明 |
|------|------|
| **處理更困難的任務** | Claude 能以有趣且出乎意料的方式組合工具，並能有效使用從未見過的工具 |
| **可擴展平台** | 容易向系統新增工具 — Claude 無需重新訓練即可適應新的工具定義 |
| **更好的安全性** | 不需要為你的程式碼庫建立索引；不需要將程式碼庫發送到外部伺服器。模型透過工具呼叫按需讀取檔案 |

## Demo Walkthrough: Tool Use Flow — Coding Assistant 如何讀取檔案

> [!NOTE]
> 以下演練重現講師在影片中的示範（SRT 33-63）。

| 步驟 | 發生什麼事 | 截圖 |
|------|-----------|------|
| 1 | 純語言模型被要求讀取檔案 — 它回應無法存取檔案系統 | ![LM 限制](../../visual-guide/frames/frame_034.jpg) |
| 2 | Coding assistant 在使用者的請求後附加工具指令，告訴模型有哪些工具可用 | ![附加工具指令](../../visual-guide/frames/frame_045.jpg) |
| 3 | 模型以結構化工具呼叫回應：`ReadFile: main.go`，而非自然語言回答 | ![ReadFile 工具呼叫](../../visual-guide/frames/frame_050.jpg) |
| 4 | Coding assistant 攔截工具呼叫，從磁碟讀取實際檔案，並將內容傳回模型 | ![檔案內容傳回](../../visual-guide/frames/frame_056.jpg) |
| 5 | 模型提供最終回答，現在基於真實的檔案內容 | ![包含內容的最終回答](../../visual-guide/frames/frame_060.jpg) |

**結果**：模型現在能透過精心格式化的文字回應來有效地「讀取檔案」，編排層負責攔截並執行這些回應。

## Instructor Tips

> [!TIP]
> 「Coding assistant 不僅僅是一個寫程式碼的工具」— 講師強調要理解底層發生了什麼，而不是把它當成黑盒子。

> [!TIP]
> 講師逐步演練 tool use 流程，強調模型的「ReadFile」回應並不是模型真的在讀取任何東西 — coding assistant（編排層）才是做實際工作的。

## Key Takeaways

1. Coding assistant 使用語言模型來完成複雜的程式設計任務
2. 語言模型需要工具才能執行真實世界的程式設計任務（讀取檔案、執行命令、寫程式碼）
3. 並非所有語言模型的 tool use 能力都相同 — 品質差異很大
4. Claude 強大的 tool use 能力帶來更好的安全性、客製化能力和平台長期性

---

# PART 2: Study Aids

> [!NOTE]
> 補充學習材料，非來自官方課程。

## Familiar Analogies

- **「手腳」比喻** — 沒有工具的語言模型就像一個雙手被綁住的天才工程師。他能完美地思考解決方案，但無法打字、開檔案或跑測試。Tool use 給了模型「手和腳」。
- **Middleware 模式** — Coding assistant 的角色類似 web stack 中的 middleware。它位於使用者（client）和語言模型（backend）之間，攔截回應、執行工具呼叫、將結果路由回去 — 類似 Express middleware 攔截請求並在傳遞給 route handler 前進行豐富化。
- **Unix 哲學** — 每個工具做好一件事（`ReadFile`、`WriteFile`、`RunCommand`）。Coding assistant 負責組合它們，就像在 shell 中 pipe `grep | sort | uniq` 一樣。

## CCA Exam Connection

> [!TIP]
> **考試提示**：本單元建立了整個 CCA 考試的基礎心智模型。預期會考：
> - 理解三步驟循環（蒐集上下文、制定計畫、採取行動）
> - 知道語言模型無法直接存取檔案/命令（需要 tool use）
> - 識別五步驟 tool use 流程以及各參與者的角色
> - 理解 Claude 的 tool use 優勢為何重要（安全性、可擴展性、更困難的任務）
> - 區分語言模型和 coding assistant（編排層 vs. 模型）

## Anti-Patterns

| 反模式 | 為什麼是錯的 | 正確理解 |
|--------|-------------|---------|
| 認為 LM 直接「讀取」檔案 | 模型只處理文字；編排層讀取檔案並以文字傳遞內容 | Coding assistant 讀取檔案並將內容發送給模型 |
| 假設所有 LM 的 tool use 能力一樣好 | Tool use 品質在不同模型間差異很大 | Claude 在 tool use 方面特別強 — 能創造性地組合工具並使用未見過的工具 |
| 相信 coding assistant 必須為程式碼庫建立索引 | 建立索引是一種方法但不是唯一的 | Claude 的 tool-use 方法按需讀取檔案，避免將程式碼庫發送到外部伺服器 |
| 把 coding assistant 當成只是「自動完成」 | 自動完成是狹隘的、單步驟的功能 | Coding assistant 執行代理式循環：蒐集上下文、計畫、行動 — 可能經過多次迭代 |

## Practice Questions

**Q1.** 在 tool use 互動中，語言模型回應了 `ReadFile: main.go`。接下來會發生什麼？

- A) 語言模型直接從檔案系統開啟檔案
- B) Coding assistant 攔截回應，從磁碟讀取檔案，並將內容傳回模型
- C) 使用者必須手動將檔案內容複製貼上到聊天中
- D) 模型從遠端儲存庫下載檔案

> [!NOTE]
> **答案：B。** 語言模型無法存取檔案系統。Coding assistant（編排層）攔截結構化的工具呼叫，讀取實際檔案，並以文字形式將內容傳回給模型處理。

**Q2.** 以下哪一項不是 Claude 強大 tool use 能力的好處？

- A) 能透過創造性地組合工具來處理更困難的任務
- B) 比其他語言模型更快的推論速度
- C) 更好的安全性，因為不需要建立程式碼庫索引
- D) 可擴展平台 — 容易新增 Claude 能適應的工具

> [!NOTE]
> **答案：B。** 列出的三個好處是：處理更困難的任務、可擴展平台和更好的安全性。推論速度並未被提及為 Claude tool use 優勢的好處。
