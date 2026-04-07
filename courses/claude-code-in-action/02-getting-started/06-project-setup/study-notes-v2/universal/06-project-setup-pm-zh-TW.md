# Project Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (project context prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

課程提供了一個範例專案，讓你有一個真實運作的應用程式可以搭配 Claude Code 探索 — 把它想成後續課程的 sandbox 環境。

## Core Concepts

### 為什麼需要一個專案

搭配專案使用 Claude Code 會更有趣。課程提供了一個範例 UI 生成應用程式（與先前影片中展示的相同）。你不一定要跑這個專案 — 如果你想的話，可以用自己的 codebase 跟著做。

### 這個專案做什麼

範例 app 是一個 **UI 生成工具**，透過 Anthropic API 使用 Claude 來建立 UI 元件。把它想成一個接收請求、產出視覺結果的小產品 — 類似許多 AI 驅動的 SaaS 工具底層的運作方式。

### 設定步驟（你的工程團隊會做的事）

| 步驟 | 指令 / 動作 | PM 翻譯 |
|------|------------|---------|
| 1 | 從 https://nodejs.org/en/download 安裝 Node.js | 安裝執行環境 — 類似在開發者機器上安裝 Java 或 Python |
| 2 | 下載並解壓縮 `uigen.zip`（附在課程單元中） | 取得專案檔案 — 類似從 GitHub clone 一個 repo |
| 3 | 執行 `npm run setup` | 一鍵設定 — 安裝相依套件並設定資料庫，類似 SaaS 產品 onboarding 精靈中點擊「Setup」 |
| 4 | *（選擇性）* 將 Anthropic API key 放入 `.env` 檔案 | 設定 AI 整合 — 類似在工具的設定頁面輸入 OpenAI key。至 https://console.anthropic.com/ 取得 |
| 5 | 執行 `npm run dev` | 啟動應用程式 — 類似在 IDE 中點擊「Run」或啟動本機伺服器 |

> 📝
> API key（步驟 4）是選擇性的。如果沒有提供 API key，app 仍會生成一些靜態假資料。這是 **graceful degradation** 模式 — 產品以降低功能的方式運作，而非完全壞掉。

### 關鍵架構決策（PM 視角）

- **本機 SQLite 資料庫**：不需要雲端資料庫設定。開發環境零基礎建設成本。
- **可選 API key**：降低進入門檻。新成員無需等待 API 存取權限即可上手。
- **單一設定指令**：`npm run setup` 將多個步驟打包。良好的開發者體驗（DX）減少 onboarding 摩擦。

## Key Takeaways

1. 範例專案是選擇性的 — 團隊可以用自己的 codebase
2. 一個指令（`npm run setup`）處理整個環境建置
3. API key 是選擇性的，展示了產品設計中的 graceful degradation
4. 專案代表了典型的 AI 整合 web 應用架構
5. 密鑰（API key）儲存在 `.env` 檔案中，不在程式碼裡 — 這是安全最佳實踐

---

# PART 2: Study Aids

> 💡 補充學習材料，非官方課程內容。

## Familiar Analogies

- **`npm run setup`** — 類似企業軟體的「Quick Start」精靈。一鍵（一個指令）環境就緒。降低開發者的「首次產生價值時間」。
- **`.env` 檔案** — 類似 SaaS 產品中輸入 API key 和設定的設定頁面。將密鑰與應用程式程式碼分離。
- **Graceful degradation（無 API key）** — 類似 Spotify 的離線模式：核心功能仍可使用，但進階功能（即時 AI 生成）需要認證。
- **SQLite** — 類似嵌入式資料庫（想像現代版的 MS Access）。適合原型開發，因為不需要獨立的資料庫伺服器。

## CCA Exam Connection

> 💡
> 身為 PM，考試可能測試你對專案設定背景的理解，而非記住精確指令。專注於：
> - 為什麼 Claude Code 需要一個專案（它分析既有程式碼）
> - Claude Code（開發工具）與 Anthropic API（範例 app 在 runtime 使用的服務）的區別
> - 理解設定指令是專案特有的，不是 Claude Code 的功能

## Anti-Patterns

| Anti-Pattern | 為什麼是錯的 | 正確做法 |
|-------------|------------|---------|
| 以為 Claude Code 只能用在範例專案 | Claude Code 可以用在任何 codebase | 範例專案只是一個方便的示範 |
| 以為 API key 是課程必須的 | 課程明確表示這是選擇性的 | 沒有 key 時 app 會 graceful degradation |
| 混淆專案設定與 Claude Code 設定 | 這是兩件不同的事：一個設定 app，另一個設定 AI 工具 | 第 05 單元涵蓋 Claude Code 設定；第 06 單元涵蓋範例專案 |
| 因為「PM 不寫程式」就跳過這個單元 | 理解開發環境有助於與工程團隊溝通 | 至少要理解每個設定步驟完成什麼 |

## Practice Questions

**Q1.** `npm run setup` 在範例專案中完成什麼？

- A) 在開發者機器上安裝 Claude Code
- B) 安裝專案相依套件並建立本機 SQLite 資料庫
- C) 將應用程式部署到雲端伺服器
- D) 設定 Anthropic API key

> 📝
> **答案：B。** `npm run setup` 是專案特有的 script，安裝相依套件並建立本機資料庫。它與 Claude Code 安裝無關（那是第 05 單元的內容）。

**Q2.** 為什麼範例專案在沒有 Anthropic API key 的情況下仍能運作？

- A) 它使用 Claude Code 內建的 API key
- B) SQLite 在本機提供 AI 功能
- C) app 降級為生成靜態假資料
- D) Node.js 內建 AI 生成功能

> 📝
> **答案：C。** 課程說明沒有 API key 時，app 會生成靜態假資料。這是 graceful degradation 模式 — 產品提供降低但可用的輸出，而非完全失敗。

**Q3.** PM 正在評估團隊應該用範例專案還是自己的 codebase 來上課。哪個說法正確？

- A) 認證考試要求必須使用範例專案
- B) 團隊必須在前三個模組使用範例專案，之後才能切換
- C) 兩種都可以 — 課程明確表示你可以用自己的 codebase 跟著做
- D) 只有範例專案具備 Claude Code 需要的正確結構

> 📝
> **答案：C。** 課程明確說明：「You can always follow along with the remainder of the course with your own code base if you wish.」Claude Code 可以用在任何 codebase。
