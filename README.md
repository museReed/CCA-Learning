# CCA Learning — Claude Certified Associate 學習資料庫

> 本 repo 包含 Anthropic Academy 課程的**原始教材**與**自製學習筆記**，
> 專為準備 [Claude Certified Associate (CCA)](https://www.anthropic.com/claude-certified-associate) 考試而設計。

---

## 📋 目錄

- [考試概覽](#-考試概覽)
- [本 repo 包含什麼](#-本-repo-包含什麼)
- [學習路線建議](#-學習路線建議)
- [課程詳細說明](#-課程詳細說明)
- [如何使用學習筆記](#-如何使用學習筆記)
- [建置 HTML 學習入口](#-建置-html-學習入口)
- [檔案結構](#-檔案結構)

---

## 🎯 考試概覽

CCA 考試涵蓋五大領域：

| 領域 | 比重 | 核心主題 |
|------|------|---------|
| **D1** Agentic Coding Fundamentals | 22% | Agentic loop、stop reasons、multi-turn orchestration |
| **D2** Tool Design & MCP Integration | 18% | MCP server/client、tools/resources/prompts、transports |
| **D3** Claude Code Configuration | 20% | CLAUDE.md、hooks、permissions、headless mode、SDK |
| **D4** AI Safety & Responsible Development | 20% | Prompt injection、jailbreak、PII handling、human-in-the-loop |
| **D5** Enterprise Deployment Patterns | 20% | Extended thinking、prompt caching、multi-model routing |

---

## 📦 本 repo 包含什麼

### 原始教材（官方課程內容）

| 資料類型 | 說明 | 位置 |
|----------|------|------|
| **課程文字稿** | 每堂課的完整講稿（Markdown） | `courses/*/[ch]/[lesson].md` |
| **影片截圖** | 講師投影片截圖（PNG/JPG） | `courses/*/[ch]/images/` |
| **英文字幕** | 影片 SRT 字幕檔（134 個） | `courses/*/[ch]/*.srt` |
| **影音檔** | MP4 影片（108 支）| 📦 [GitHub Release v1.0.0](https://github.com/museReed/CCA-Learning/releases/tag/v1.0.0)（1.7 GB，按課程分 4 個 zip）|

### 自製學習筆記

每堂課都有 **6 個版本**的學習筆記：

| 維度 | 選項 | 說明 |
|------|------|------|
| **角色** | `eng` / `pm` | 工程師版（含完整 code）vs PM 版（商業類比，無 code） |
| **語言** | `en` / `zh-TW` / `zh-CN` | 英文 / 繁體中文 / 簡體中文 |

**工程師版特色：**
- 完整 Python 程式碼範例
- iOS 概念類比（RunLoop ↔ Agentic Loop）
- 動手實作練習（BUILD 段落）
- Feynman 驗收題（TEACH 段落）

**PM 版特色：**
- 職場情境類比（新員工報到、部門經理指派任務）
- 架構判斷練習（不寫 code，判斷設計好壞）
- PRD Checklist
- 模擬追問對話

### SVG 圖表

每個核心概念都有 **EN + 繁中** 雙語向量圖：
- 流程圖、架構圖、序列圖、比較表
- 統一色彩系統：藍 `#3B82F6` / 綠 `#22C55E` / 紅 `#EF4444` / 紫 `#8B5CF6`
- 存放於 `courses/*/[ch]/[lesson]/visuals/`

### HTML 學習入口

預建的 HTML 頁面，可直接在瀏覽器中閱讀：
- 首頁 `html/index.html`：依角色 × 語言切換的導航頁
- 自動記住上次瀏覽的筆記（localStorage）

---

## 🗺️ 學習路線建議

### 第一階段：核心基礎（建議 2-3 週）

**從這裡開始 👇**

#### 1️⃣ [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action)（CCA 主課程）
> 涵蓋 D1 + D3 + D4，佔考試 62%

| 章節 | 主題 | CCA 領域 | 建議用時 |
|------|------|---------|---------|
| Ch01 Intro | Agentic loop、coding assistant 本質 | D1 | 2h |
| Ch02 Getting Started | 安裝、first project、configuration | D3 | 2h |
| Ch03 Context & Commands | CLAUDE.md、memory、slash commands | D3 | 3h |
| Ch04 Integrations | Git、GitHub、CI/CD、headless mode | D3, D5 | 3h |
| Ch05 Hooks | Permission model、hook types、safety | D3, D4 | 3h |
| Ch06 SDK & Wrap Up | SDK entry points、course review | D3, D5 | 2h |

**學習方式：**
1. 先看官方影片或讀 `courses/claude-code-in-action/[ch]/[lesson].md` 原始文字稿
2. 讀對應的學習筆記（選你的角色 + 語言）
3. 看 SVG 圖表加深印象
4. 用 Flashcard 自測

---

### 第二階段：MCP 深入（建議 1-2 週）

#### 2️⃣ [Introduction to MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol)（MCP 入門）
> 核心 D2 內容

| 章節 | 主題 | 重點 |
|------|------|------|
| Ch01 MCP Basics | MCP 架構、Client/Server 角色 | 必讀 |
| Ch02 Tools & Inspector | `@mcp.tool()` 裝飾器、Inspector 測試 | 必讀 |
| Ch03 Resources & Prompts | 三大 primitive 的定義與使用 | 必讀 |
| Ch04 Review | Tools vs Resources vs Prompts 決策指南 | 必讀 |

#### 3️⃣ [MCP Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)（MCP 進階）
> D2 進階 + 部署考量

| 章節 | 主題 | 重點 |
|------|------|------|
| Ch01 Sampling & Notifications | Server 借用 Client 的 AI、progress 回報 | 重要 |
| Ch02 Roots & Messages | 檔案存取權限、JSON 訊息分類 | 重要 |
| Ch03 Transports | STDIO vs StreamableHTTP、SSE、scaling trade-off | 考試常考 |

---

### 第三階段：API 與進階（建議 2-3 週）

#### 4️⃣ [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api)（API 大課程）
> 涵蓋 D1 + D2 + D4 + D5

| 章節 | 主題 |
|------|------|
| Ch01 API Fundamentals | Models、Messages API、streaming、temperature |
| Ch02 Prompt Evaluation | 評估策略 |
| Ch03 Prompt Engineering | 系統化 prompt 設計 |
| Ch04 Tool Use | Tool schema、forced tool use |
| Ch05 RAG | 文件檢索增強生成 |
| Ch06 Extended Features | Vision、PDF、caching、batches |
| Ch07 MCP（重疊） | 與 MCP 課程部分重疊 |
| Ch08 Agents & Workflows | Agent 架構模式 |
| Ch09 Assessment | 綜合評量 |

⚠️ 此課程尚未產出學習筆記，目前僅有原始文字稿與截圖。

---

### 官方課程連結

| 課程 | 官方連結 | 本 repo 對應 |
|------|---------|-------------|
| Claude Code in Action | [anthropic.skilljar.com/claude-code-in-action](https://anthropic.skilljar.com/claude-code-in-action) | `courses/claude-code-in-action/` |
| Introduction to MCP | [anthropic.skilljar.com/introduction-to-model-context-protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | `courses/introduction-to-model-context-protocol/` |
| MCP Advanced Topics | [anthropic.skilljar.com/model-context-protocol-advanced-topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) | `courses/model-context-protocol-advanced-topics/` |
| Building with the Claude API | [anthropic.skilljar.com/claude-with-the-anthropic-api](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | `courses/building-with-the-claude-api/` |
| Claude 101 | [anthropic.skilljar.com/claude-101](https://anthropic.skilljar.com/claude-101) | `courses/claude-101/`（可跳過） |
| Introduction to Agent Skills | [anthropic.skilljar.com/introduction-to-agent-skills](https://anthropic.skilljar.com/introduction-to-agent-skills) | `courses/introduction-to-agent-skills/`（可跳過） |
| Introduction to Subagents | [anthropic.skilljar.com/introduction-to-subagents](https://anthropic.skilljar.com/introduction-to-subagents) | `courses/introduction-to-subagents/`（可跳過） |

### 官方補充資源

| 資源 | 網址 | 用途 |
|------|------|------|
| Anthropic Academy | https://anthropic.skilljar.com | 官方線上課程入口 |
| CCA 考試指南 | 見 repo 內 PDF | 30 Task Statements + Sample Questions |
| Claude Code 文檔 | https://docs.anthropic.com/en/docs/claude-code | 官方 CLI 文檔 |
| MCP 規範 | https://modelcontextprotocol.io | MCP 官方規範 |
| Building Effective Agents | https://www.anthropic.com/research/building-effective-agents | 5 大 Agent 架構模式 |

---

## 📖 如何使用學習筆記

### 找到你的筆記

```
courses/{課程名}/{章節}/{課堂}/study-notes/universal/
├── {lesson}-eng-en.md      ← 工程師版・英文
├── {lesson}-eng-zh-TW.md   ← 工程師版・繁中
├── {lesson}-eng-zh-CN.md   ← 工程師版・簡中
├── {lesson}-pm-en.md       ← PM 版・英文
├── {lesson}-pm-zh-TW.md    ← PM 版・繁中
└── {lesson}-pm-zh-CN.md    ← PM 版・簡中
```

### 每份筆記的結構

1. **One-Liner** — 一句話摘要
2. **核心概念** — 搭配 SVG 圖表
3. **程式範例**（eng）/ **情境類比**（pm）
4. **CCA 考試關聯** — 對應到哪個 Task Statement
5. **Flashcards** — 5-8 張記憶卡

### 建議學習流程

```
官方影片 → 原始文字稿 → 學習筆記 → SVG 圖表 → Flashcard 自測
    ↑                                              ↓
    └──────────── 不熟的部分回去複習 ←──────────────┘
```

---

## 🔧 建置 HTML 學習入口

如果你想在瀏覽器中閱讀（推薦），HTML 已經預建好了：

```bash
# 直接打開
open html/index.html
```

如果需要重新建置：

```bash
# 1. 安裝 markdown 套件
pip3 install markdown

# 2. 建置 HTML
python3 scripts/build_html_multi.py

# 3. 重建首頁
python3 scripts/rebuild_index_multi.py
```

---

## 📁 檔案結構

```
CCA-Learning/
├── README.md
├── .gitignore
├── courses/
│   ├── claude-code-in-action/          ✅ 6 章 19 課（114 筆記 + 90 SVG）
│   │   ├── 01-intro/
│   │   │   ├── 03-what-is-a-coding-assistant/
│   │   │   │   ├── study-notes/universal/   ← 6 個筆記檔
│   │   │   │   └── visuals/                 ← SVG 圖表
│   │   │   └── ...
│   │   └── ...
│   ├── introduction-to-model-context-protocol/  ✅ 4 章 10 課（60 筆記 + 10 SVG）
│   ├── model-context-protocol-advanced-topics/  ✅ 3 章 8 課（48 筆記 + 12 SVG）
│   ├── building-with-the-claude-api/            📝 9 章 87 課（原始教材，待產筆記）
│   ├── claude-101/                              ⏭️ 單堂入門（可跳過）
│   ├── introduction-to-agent-skills/            ⏭️ 單堂簡介（可跳過）
│   └── introduction-to-subagents/               ⏭️ 單堂簡介（可跳過）
└── html/                                        🌐 預建 HTML（222 頁）
    ├── index.html                               ← 學習入口首頁
    ├── claude-code-in-action/
    ├── introduction-to-model-context-protocol/
    └── model-context-protocol-advanced-topics/
```

---

## 📊 數量統計

| 項目 | 數量 |
|------|------|
| 課程 | 7 門（4 門已產筆記） |
| 學習筆記 | 222 份 |
| SVG 圖表 | 112 個（56 EN + 56 zh-TW） |
| HTML 頁面 | 222 頁 |
| 原始課堂文字稿 | 240 份 |
| 英文字幕 | 134 個 .srt |
| 影片截圖 | 393 張 |

---

## ⚠️ 注意事項

- 影片檔（108 支 MP4，共 1.7 GB）存放於 [GitHub Release](https://github.com/museReed/CCA-Learning/releases/tag/v1.0.0)，按課程分為 4 個 zip 下載
- 學習筆記為 AI 輔助產出，建議搭配官方教材交叉驗證
- 本 repo 為**個人學習用途**，課程內容版權屬 Anthropic

---

*Last updated: 2026-04-08*
