# Project Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (project context prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

設定一個範例 Node.js + SQLite UI 生成專案，讓你在後續課程中有真實的 codebase 可以搭配 Claude Code 一起探索。

## Core Concepts

### 為什麼需要一個專案

搭配專案使用 Claude Code 會更有趣。課程提供了一個範例 UI 生成應用程式（與先前影片中展示的相同）。你不一定要跑這個專案 — 如果你想的話，可以用自己的 codebase 跟著做。

### 前置需求

- 本機必須安裝 **Node.js**
- 安裝指引：https://nodejs.org/en/download

### 設定步驟

| 步驟 | 指令 / 動作 | 功能說明 |
|------|------------|---------|
| 1 | 安裝 Node.js | 執行環境前置需求 |
| 2 | 下載並解壓縮 `uigen.zip`（附在該課程單元中） | 取得範例專案檔案 |
| 3 | `npm run setup` | 安裝相依套件並建立本機 SQLite 資料庫 |
| 4 | *（選擇性）* 將 Anthropic API key 放入 `.env` 檔案 | 啟用即時 Claude API 呼叫以生成 UI |
| 5 | `npm run dev` | 啟動開發伺服器 |

> [!NOTE]
> 步驟 4 是選擇性的。如果沒有提供 API key，應用程式仍會生成一些靜態假資料。若要完整測試，可至 https://console.anthropic.com/ 取得 API key。

### 專案架構（從上下文推斷）

- **Frontend + Backend**：Node.js 專案，附帶 dev server（`npm run dev`）
- **Database**：本機 SQLite（由 `npm run setup` 建立）
- **AI Integration**：透過 Anthropic API 使用 Claude 生成 UI 元件
- **Graceful Degradation**：無 API key 時降級為靜態假資料

## Key Takeaways

1. 範例專案是選擇性的 — 你可以改用自己的 codebase
2. `npm run setup` 一個指令同時處理相依套件安裝與資料庫建立
3. Anthropic API key 是選擇性的；應用程式在沒有 key 的情況下仍可正常降級運作
4. 這個專案提供一個真實的多檔案 codebase，讓你練習 Claude Code 互動
5. `.env` 檔案用來存放密鑰（API key）— 這是常見的 Node.js 模式

---

# PART 2: Study Aids

> 💡 補充學習材料，非官方課程內容。

## Familiar Analogies

- **`npm run setup`** — 類似 Rails 的 `rails db:setup` 或 Django 的 `python manage.py migrate`。一個指令同時搞定相依套件和資料庫。
- **`.env` 檔案放 API key** — 與 Next.js、Vite 及大多數現代 Node.js 框架相同的模式。環境變數讓密鑰不進版控。
- **Graceful degradation** — 就像天氣 app 在斷網時顯示快取資料。沒有 API key 應用程式仍能運作，只是內容是靜態的。
- **SQLite 做本機開發** — 類似 Java 的 H2 或 Python 的 sqlite3。檔案型資料庫，零伺服器設定。

## CCA Exam Connection

> [!TIP]
> 這個單元建立了後續課程使用的專案背景。預期考試會測試：
> - 理解 Claude Code 可以在既有 codebase 上運作（不只是新專案）
> - 知道 `npm run setup` 是專案特有的 script（不是 Claude Code 的指令）
> - 區分 Claude Code（CLI 工具）與 Anthropic API（範例 app 使用的服務）

## Anti-Patterns

| Anti-Pattern | 為什麼是錯的 | 正確做法 |
|-------------|------------|---------|
| 將含有 API key 的 `.env` 檔案 commit 進版控 | 在版本控制中暴露密鑰 | 將 `.env` 加入 `.gitignore`；專案應該已經這樣做了 |
| 在 `npm run setup` 之前就跑 `npm run dev` | 資料庫還不存在，app 會 crash | 一定要先跑 `npm run setup` |
| 以為 API key 是必要的 | 課程明確說明這是選擇性的 | 沒有 key 時 app 會生成靜態假資料作為 fallback |
| 混淆專案的 Anthropic API 使用與 Claude Code 本身 | 兩者是分開的：專案呼叫 API；Claude Code 是你用來開發專案的 CLI | 理解 Claude Code 分析程式碼，而專案在 runtime 使用 Claude API |

## Practice Questions

**Q1.** 下載並解壓縮範例專案後，應該先執行什麼指令？

- A) `npm install`
- B) `npm run dev`
- C) `npm run setup`
- D) `node setup.js`

> [!NOTE]
> **答案：C。** `npm run setup` 會安裝相依套件並建立本機 SQLite 資料庫。在 setup 之前就跑 `npm run dev` 會失敗，因為資料庫尚未建立。

**Q2.** 學生沒有 Anthropic API key。執行範例專案時會發生什麼？

- A) 應用程式完全無法啟動
- B) 應用程式啟動但在生成 UI 元件時 crash
- C) 應用程式啟動並生成靜態假資料，而非呼叫 Claude
- D) 應用程式啟動時提示輸入 API key

> [!NOTE]
> **答案：C。** 課程明確說明如果沒有提供 API key，app 仍會生成一些靜態假資料。API key 對於跟著課程學習來說是選擇性的。

**Q3.** Anthropic API key 應該放在範例專案的哪裡？

- A) `config.json` 檔案中
- B) `.env` 檔案中
- C) 作為 `npm run dev` 的命令列參數
- D) 在 `package.json` 的 `scripts` 區塊中

> [!NOTE]
> **答案：B。** 課程指示將 API key 放入 `.env` 檔案，這是 Node.js 中環境特定設定的標準模式。
