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

| 資料類型 | 說明 | 數量 |
|----------|------|------|
| **課程文字稿** | 每堂課的完整講稿（Markdown） | 125 份 |
| **英文字幕** | 影片 SRT 字幕檔 | 108 個 |
| **影片截圖** | 講師投影片截圖（PNG/JPG） | 各課附帶 |
| **影音檔** | MP4 影片（108 支） | [GitHub Release v1.0.0](https://github.com/museReed/CCA-Learning/releases/tag/v1.0.0)（1.7 GB） |

### 自製學習筆記（6 版本 × 106 堂）

每堂課都有 **6 個版本**的學習筆記：

| 維度 | 選項 | 說明 |
|------|------|------|
| **角色** | `eng` / `pm` | 工程師版（含完整 code）vs PM 版（商業類比，無 code） |
| **語言** | `en` / `zh-TW` / `zh-CN` | 英文 / 繁體中文 / 簡體中文 |

**工程師版** — 完整 Python 範例、iOS 類比、BUILD 實作、Feynman 驗收題
**PM 版** — 職場情境類比、架構判斷、PRD Checklist、模擬追問

### 雙語字幕 & 翻譯

| 資料類型 | 說明 | 數量 |
|----------|------|------|
| **翻譯 JSON** | 逐句 EN → zh-TW / zh-CN 字幕翻譯 | 108 個 |
| **雙語 SRT** | EN + ZH 雙行字幕檔（可搭配影片播放） | 216 個（108 zh-TW + 108 zh-CN） |

### SVG 圖表

每個核心概念都有 **EN + 繁中** 雙語向量圖（流程圖、架構圖、序列圖）：
- 統一色彩系統：藍 `#3B82F6` / 綠 `#22C55E` / 紅 `#EF4444` / 紫 `#8B5CF6`
- 共 187 個 SVG

### 影片逐幀學習指南（Visual Guides）

從 108 支教學影片自動截取每段字幕的關鍵幀，並燒入雙語字幕：
- 共 **7,658 幀**（每幀 = 影片截圖 + EN/ZH 字幕疊加）
- 每支影片一個 Markdown 學習指南，可離線翻閱

### HTML 學習入口

預建的 HTML 頁面（637 頁），可直接在瀏覽器中閱讀，支援角色 × 語言切換。

---

## 🗺️ 學習路線建議

### 第一階段：核心基礎（建議 2-3 週）

**從這裡開始 👇**

#### 1️⃣ [Claude Code in Action](courses/claude-code-in-action/INDEX.md)（CCA 主課程）
> 涵蓋 D1 + D3 + D4，佔考試 62%

| 章節 | 主題 | CCA 領域 |
|------|------|---------|
| Ch01 Intro | Agentic loop、coding assistant 本質 | D1 |
| Ch02 Getting Started | 安裝、first project、configuration | D3 |
| Ch03 Context & Commands | CLAUDE.md、memory、slash commands | D3 |
| Ch04 Integrations | Git、GitHub、CI/CD、headless mode | D3, D5 |
| Ch05 Hooks | Permission model、hook types、safety | D3, D4 |
| Ch06 SDK & Wrap Up | SDK entry points、course review | D3, D5 |

---

### 第二階段：MCP 深入（建議 1-2 週）

#### 2️⃣ [Introduction to MCP](courses/introduction-to-model-context-protocol/INDEX.md)（MCP 入門）
> 核心 D2 內容

| 章節 | 主題 |
|------|------|
| Ch01 MCP Basics | MCP 架構、Client/Server 角色 |
| Ch02 Tools & Inspector | `@mcp.tool()` 裝飾器、Inspector 測試 |
| Ch03 Resources & Prompts | 三大 primitive 的定義與使用 |
| Ch04 Review | Tools vs Resources vs Prompts 決策指南 |

#### 3️⃣ [MCP Advanced Topics](courses/model-context-protocol-advanced-topics/INDEX.md)（MCP 進階）
> D2 進階 + 部署考量

| 章節 | 主題 |
|------|------|
| Ch01 Sampling & Notifications | Server 借用 Client 的 AI、progress 回報 |
| Ch02 Roots & Messages | 檔案存取權限、JSON 訊息分類 |
| Ch03 Transports | STDIO vs StreamableHTTP、SSE、scaling trade-off |

---

### 第三階段：API 與進階（建議 2-3 週）

#### 4️⃣ [Building with the Claude API](courses/building-with-the-claude-api/INDEX.md)（API 大課程）
> 涵蓋 D1 + D2 + D4 + D5

| 章節 | 主題 |
|------|------|
| Ch01 API Fundamentals | Models、Messages API、streaming、temperature |
| Ch02 Prompt Evaluation | 評估策略、code-based / model-based grading |
| Ch03 Prompt Engineering | 系統化 prompt 設計 |
| Ch04 Tool Use | Tool schema、forced tool use |
| Ch05 RAG | 文件檢索增強生成 |
| Ch06 Extended Features | Vision、PDF、caching、extended thinking |
| Ch07 MCP（與 MCP 課程重疊） | 完整 MCP 入門覆蓋 |
| Ch08 Agents & Workflows | Agent 架構模式 |
| Ch09 Assessment | 綜合評量 |

---

### 官方課程連結

| 課程 | 官方連結 | 本 repo 目錄 | 狀態 |
|------|---------|-------------|------|
| Claude Code in Action | [Skilljar](https://anthropic.skilljar.com/claude-code-in-action) | `courses/claude-code-in-action/` | ✅ 完整 |
| Introduction to MCP | [Skilljar](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | `courses/introduction-to-model-context-protocol/` | ✅ 完整 |
| MCP Advanced Topics | [Skilljar](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) | `courses/model-context-protocol-advanced-topics/` | ✅ 完整 |
| Building with the Claude API | [Skilljar](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | `courses/building-with-the-claude-api/` | ✅ 完整 |
| Claude 101 | [Skilljar](https://anthropic.skilljar.com/claude-101) | `courses/claude-101/` | ⏭️ 入門（可跳過） |
| Introduction to Agent Skills | [Skilljar](https://anthropic.skilljar.com/introduction-to-agent-skills) | `courses/introduction-to-agent-skills/` | ⏭️ 簡介 |
| Introduction to Subagents | [Skilljar](https://anthropic.skilljar.com/introduction-to-subagents) | `courses/introduction-to-subagents/` | ⏭️ 簡介 |

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
官方影片 → 原始文字稿 → 學習筆記 → SVG 圖表 → 逐幀指南 → Flashcard 自測
    ↑                                                         ↓
    └───────────────── 不熟的部分回去複習 ←───────────────────┘
```

---

## 🔧 建置 HTML 學習入口

HTML 已經預建好了，直接打開即可：

```bash
open html/index.html
```

如需重新建置：

```bash
pip3 install markdown
python3 scripts/build_html.py
```

---

## 📁 檔案結構

```
CCA-Learning/
├── README.md                              ← 你在這裡
├── courses/
│   ├── building-with-the-claude-api/      ✅ 9 章 68 課
│   │   ├── INDEX.md                       ← 課程目錄（每門課都有）
│   │   ├── translations/                  ← 74 翻譯 JSON
│   │   └── 01-api-fundamentals/           ← 章節目錄
│   │       ├── 04-accessing-the-api.md    ← 原始課程文字稿
│   │       ├── 04-accessing-the-api/      ← 課堂目錄
│   │       │   ├── study-notes/universal/ ← 6 個學習筆記
│   │       │   └── visuals/               ← SVG 圖表
│   │       ├── images/                    ← 講師截圖（文字稿引用）
│   │       ├── screenshots/               ← Skilljar 頁面截圖
│   │       ├── srt/                       ← 英文 + 雙語字幕
│   │       │   └── bilingual/             ← EN+ZH 雙語 SRT
│   │       ├── videos/                    ← MP4 教學影片
│   │       └── visual-guides/             ← 逐幀截圖+雙語字幕疊加
│   │
│   ├── claude-code-in-action/             ✅ 6 章 15 課
│   │   ├── INDEX.md
│   │   ├── translations/                  ← 15 翻譯 JSON
│   │   └── 01-intro/
│   │       └── 02-introduction/           ← 每堂課獨立目錄
│   │           ├── source/                ← 課程文字稿+截圖
│   │           ├── study-notes/universal/ ← 6 個學習筆記
│   │           ├── srt/bilingual/         ← 雙語 SRT
│   │           ├── visual-guide/          ← 逐幀截圖
│   │           └── visuals/               ← SVG 圖表
│   │
│   ├── introduction-to-model-context-protocol/  ✅ 4 章 11 課
│   ├── model-context-protocol-advanced-topics/  ✅ 4 章 8 課
│   ├── claude-101/                        ⏭️ 單堂入門
│   ├── introduction-to-agent-skills/      ⏭️ 單堂簡介
│   └── introduction-to-subagents/         ⏭️ 單堂簡介
│
├── html/                                  🌐 預建 HTML（637 頁）
├── scripts/                               🔧 翻譯、建置、管線腳本
│   ├── bilingual_pipeline.py              ← 雙語字幕+逐幀指南管線
│   ├── fill_translations.py              ← 翻譯核心工具
│   ├── build_html.py                     ← HTML 建置腳本
│   ├── translate_*.py                    ← 各課程翻譯腳本
│   └── internal/                         ← 內部工具（非讀者用）
└── references/                            📚 CCA 考試參考資料
```

---

## 📊 數量統計

| 項目 | 數量 |
|------|------|
| 課程 | 7 門（4 門完整，3 門大綱） |
| 已完成課堂 | 106 堂 |
| 學習筆記 | 636 份（106 課 × eng/pm × en/zh-TW/zh-CN） |
| SVG 圖表 | 187 個（含 EN 原版 + zh-TW 版） |
| 翻譯 JSON | 108 個（108 支影片 × 逐句 EN/zh-TW/zh-CN） |
| 雙語 SRT | 216 個（108 × zh-TW/zh-CN） |
| 逐幀學習指南 | 7,658 幀 + 108 個 Markdown 導覽 |
| HTML 頁面 | 637 頁 |
| 原始課程文字稿 | 125 份 |
| 教學影片 | 108 支（1.7 GB，見 Release） |

---

## ⚠️ 注意事項

- 影片檔（108 支 MP4，共 1.7 GB）存放於 [GitHub Release](https://github.com/museReed/CCA-Learning/releases/tag/v1.0.0)，按課程分 4 個 zip
- 學習筆記為 AI 輔助產出，建議搭配官方教材交叉驗證
- 本 repo 為**個人學習用途**，課程內容版權屬 Anthropic

---

*Last updated: 2026-04-28*
