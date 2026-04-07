# Project Setup — 工程深度筆記

| 項目 | 細節 |
|------|--------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 2.5 (built-in tools — awareness), 3.5 (iterative refinement — intro) |
| 來源 | claude-code-in-action / 02-getting-started / Lesson 06（純文字課程） |

---

## 一句話總結

課程示範專案是一個以 Anthropic API 和 SQLite 為後端的 Node.js UI 生成應用 — 用來探索 Claude Code 的 built-in tools 和迭代工作流的實作沙箱。

---

## 專案架構

示範專案（`uigen`）透過 Anthropic API 使用 Claude 生成 UI 元件：

```
uigen/
├── package.json          # Node.js 專案設定
├── .env                  # Anthropic API key（選用）
├── prisma/
│   └── schema.prisma     # SQLite 資料庫 schema
├── src/
│   ├── server/           # 後端 API 路由
│   └── client/           # 前端 UI
└── node_modules/         # 相依套件（npm run setup 後產生）
```

**關鍵設定步驟：**
1. 安裝 Node.js
2. 解壓 `uigen.zip` 並執行 `npm run setup`（安裝相依套件 + 建立 SQLite DB）
3. 選擇性在 `.env` 中加入 Anthropic API key
4. 以 `npm run dev` 啟動

> [!TIP]
> **關鍵洞察**
>
> API key 是選用的。沒有它，應用程式會生成靜態假資料而非呼叫 Claude。這代表即使沒有 Anthropic API key 也能跟著課程學習。

---

## Built-in Tools 預覽（Task 2.5）

本專案設定介紹了 Claude Code built-in tools 運作的情境。在後續課程中，你會使用：

| 工具 | 在此專案中的用途 |
|------|------------------------------|
| **Read** | 檢視 `schema.prisma`、`package.json`、路由檔案 |
| **Write / Edit** | 修改 UI 元件、新增 API 路由 |
| **Bash** | 執行 `npm run dev`、`npm run setup`、跑測試 |
| **Glob / Grep** | 在 `src/` 中搜尋特定模式 |

Claude Code 會根據你的請求自動選擇合適的工具。你不需要手動呼叫工具。

---

## Iterative Refinement 預覽（Task 3.5）


![Iterative Refinement Cycle](../../visuals/iterative-refinement-cycle-zh-TW.svg)
*圖：迭代精煉循環 — 請求、建構、檢視、回饋。*

此專案旨在展示與 Claude Code 的迭代開發：

1. 請 Claude 生成一個 UI 元件
2. 在瀏覽器中查看結果
3. 提供回饋（截圖、文字描述或兩者皆有）
4. Claude 改進實作

這個引入-迭代-改進循環是高效使用 Claude Code 的基礎，在 Lesson 07 和 08 中深入探討。

---

## 考試重點

| 考試概念 | 本課教了什麼 |
|-------------|-------------------------|
| **Built-in tool selection (2.5)** | 認識 Claude Code 有 Read、Write、Bash、Glob、Grep 等工具，且會自動選擇 |
| **Iterative refinement (3.5)** | 介紹 generate-review-refine 循環 |

---

## 反模式

| 反模式 | 為何失敗 |
|-------------|-------------|
| 跳過 `npm run setup` | SQLite 資料庫不會存在，導致執行時錯誤 |
| 將含有 API key 的 `.env` commit 到版本控制 | 安全風險 — `.env` 應在 `.gitignore` 中 |
| 以為 API key 是必需的 | 應用程式在沒有它的情況下使用靜態備用資料正常運作 |
