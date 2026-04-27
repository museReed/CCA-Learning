# Building with the Claude API — 教材產出計畫

> 68 課 × 6 變體 = 408 份學習筆記 + ~60 SVG 圖表
> 預計 7 天完成，每天 ~10 課

---

## 排程總覽

| 天 | 日期 | 章節 | 課數 | 筆記數 | SVG | CCA 領域 | 優先級 |
|----|------|------|------|--------|-----|----------|--------|
| D1 | 04-09 | Ch04 Tool Use | 11 | 66 | 10 | D1+D2 | 🔴 最高 |
| D2 | 04-10 | Ch08 Agents & Workflows | 11 | 66 | 10 | D1+D5 | 🔴 最高 |
| D3 | 04-11 | Ch01 API Fundamentals | 9 | 54 | 8 | D1+D5 | 🟠 高 |
| D4 | 04-12 | Ch07 MCP | 10 | 60 | 8 | D2 | 🟠 高 |
| D5 | 04-13 | Ch05 RAG + Ch06 前半 | 7+4=11 | 66 | 10 | D5 | 🟡 中 |
| D6 | 04-14 | Ch06 後半 + Ch02 Eval + Ch09 | 4+6+1=11 | 66 | 8 | D5 | 🟡 中 |
| D7 | 04-15 | Ch03 Prompt Engineering | 5 | 30 | 6 | D5 | 🟢 補充 |
| | | **合計** | **68** | **408** | **~60** | | |

---

## 優先級說明

按 CCA 考試權重排序：

1. **Ch04 Tool Use** — Tool schema、forced tool use、multi-turn（D1 22% + D2 18% = 40%）
2. **Ch08 Agents & Workflows** — Agent 架構模式、parallelization、routing（D1 22% + D5 20%）
3. **Ch01 API Fundamentals** — Messages API、streaming、temperature（D1+D5 基礎）
4. **Ch07 MCP** — 與已有 MCP 課程互補，API 視角的 MCP 實作（D2 18%）
5. **Ch05 RAG** — 檢索增強生成完整流程（D5 20%）
6. **Ch06 Extended Features** — Extended thinking、caching、vision（D5 20%）
7. **Ch02 Prompt Evaluation** — Eval workflow、grading（D5 20%）
8. **Ch03 Prompt Engineering** — Prompt 技巧（D5，與其他領域重疊較少）

---

## 每日執行流程

每天開一個 Claude Code session，執行以下步驟：

### Step 1: 建立目錄
```bash
# 為當天的課建立 study-notes/universal/ 和 visuals/ 目錄
```

### Step 2: 平行產出筆記（4-6 個 subagent）
- 每個 agent 處理 2-3 課 × 6 變體
- Agent prompt 包含：原始文字稿 + 筆記模板 + CCA domain mapping

### Step 3: 平行產出 SVG（1-2 個 subagent）
- 每章 ~8-10 個核心概念圖
- EN + zh-TW 雙語版
- 色彩系統：藍 `#3B82F6` / 綠 `#22C55E` / 紅 `#EF4444` / 紫 `#8B5CF6`

### Step 4: 後處理
```bash
# 1. 插入 SVG 引用到筆記
python3 scripts/insert_images_api.py

# 2. 建置 HTML
python3 scripts/build_html_multi.py

# 3. 重建首頁
python3 scripts/rebuild_index_multi.py
```

### Step 5: 推送
```bash
git add courses/building-with-the-claude-api/{chapters}
git commit -m "feat(cca): add study notes for Ch0X - {topic}"
git push
```

---

## 各天詳細內容

### D1 — Ch04 Tool Use（11 課）

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 32 | introducing-tool-use | Tool use 概念與流程 | tool-use-flow |
| 33 | project-overview | Weather app 專案架構 | — |
| 34 | tool-functions | Python 工具函數定義 | — |
| 35 | tool-schemas | JSON Schema 定義工具 | tool-schema-anatomy |
| 36 | handling-message-blocks | Content block 類型處理 | message-block-types |
| 37 | sending-tool-results | tool_result 回傳格式 | tool-result-flow |
| 38 | multi-turn-conversations-with-tools | 多輪工具呼叫對話 | multi-turn-tool-loop |
| 39 | implementing-multiple-turns | Agentic loop 實作 | agentic-loop |
| 40 | using-multiple-tools | 多工具協作 | — |
| 41 | fine-grained-tool-calling | tool_choice 精細控制 | tool-choice-modes |
| 42 | the-text-edit-tool | 內建文字編輯工具 | — |
| 43 | the-web-search-tool | 內建網頁搜尋工具 | — |

**Agent 分配：**
- Agent A: 32-35（4 課 × 6 = 24 筆記）
- Agent B: 36-39（4 課 × 6 = 24 筆記）
- Agent C: 40-43（3 課 × 6 = 18 筆記）* 注意：38 在 Ch01 目錄下但屬於 Tool Use 主題

---

### D2 — Ch08 Agents & Workflows（11 課）

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 73 | anthropic-apps | Anthropic 產品生態 | — |
| 74 | claude-code-setup | Claude Code 安裝設定 | — |
| 75 | claude-code-in-action | Claude Code 實戰演示 | — |
| 76 | enhancements-with-mcp-servers | MCP server 整合 | — |
| 77 | agents-and-workflows | Agent vs Workflow 定義 | agent-vs-workflow |
| 78 | parallelization-workflows | 平行化工作流 | parallelization-pattern |
| 79 | chaining-workflows | 鏈式工作流 | chaining-pattern |
| 80 | routing-workflows | 路由工作流 | routing-pattern |
| 81 | agents-and-tools | Agent 工具使用 | agent-tool-loop |
| 82 | environment-inspection | 環境感知與檢查 | environment-inspection |
| 83 | workflows-vs-agents | 工作流 vs Agent 決策指南 | workflow-agent-decision |

**Agent 分配：**
- Agent A: 73-76（4 課 × 6 = 24 筆記）
- Agent B: 77-80（4 課 × 6 = 24 筆記）
- Agent C: 81-83（3 課 × 6 = 18 筆記）

---

### D3 — Ch01 API Fundamentals（9 課）

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 04 | accessing-the-api | API 存取方式 | api-access-methods |
| 05 | getting-an-api-key | API Key 取得 | — |
| 06 | making-a-request | 第一個 API 請求 | request-anatomy |
| 07 | multi-turn-conversations | 多輪對話 | multi-turn-flow |
| 09 | system-prompts | 系統提示詞 | system-prompt-role |
| 11 | temperature | Temperature 參數 | temperature-spectrum |
| 13 | response-streaming | 串流回應 | streaming-flow |
| 14 | structured-data | 結構化資料輸出 | — |

**Agent 分配：**
- Agent A: 04-07（4 課 × 6 = 24 筆記）
- Agent B: 09,11,13,14（4 課 × 6 = 24 筆記）

---

### D4 — Ch07 MCP（10 課）

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 61 | introducing-mcp | MCP 介紹（API 視角） | — |
| 62 | mcp-clients | MCP Client 實作 | mcp-client-architecture |
| 63 | project-setup | CLI chatbot 專案設定 | — |
| 64 | defining-tools-with-mcp | MCP 工具定義 | — |
| 65 | the-server-inspector | Server Inspector 測試 | — |
| 66 | implementing-a-client | Client 完整實作 | client-server-flow |
| 67 | defining-resources | Resource 定義 | resource-types |
| 68 | accessing-resources | Resource 存取 | — |
| 69 | defining-prompts | Prompt template 定義 | three-primitives-api |
| 70 | prompts-in-the-client | Client 端 prompt 使用 | — |

**Agent 分配：**
- Agent A: 61-65（5 課 × 6 = 30 筆記）
- Agent B: 66-70（5 課 × 6 = 30 筆記）

---

### D5 — Ch05 RAG + Ch06 前半（11 課）

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 45 | introducing-rag | RAG 概念與動機 | rag-overview |
| 46 | text-chunking-strategies | 文本切塊策略 | chunking-strategies |
| 47 | text-embeddings | 文本嵌入 | embedding-space |
| 48 | the-full-rag-flow | 完整 RAG 流程 | full-rag-pipeline |
| 49 | implementing-the-rag-flow | RAG 實作 | — |
| 50 | bm25-lexical-search | BM25 詞彙搜尋 | bm25-vs-semantic |
| 51 | a-multi-index-rag-pipeline | 多索引 RAG | multi-index-rag |
| 52 | extended-thinking | Extended Thinking | extended-thinking-flow |
| 53 | image-support | 圖片支援 | — |
| 54 | pdf-support | PDF 支援 | — |
| 55 | citations | 引用功能 | citation-flow |

**Agent 分配：**
- Agent A: 45-48（4 課 × 6 = 24 筆記）
- Agent B: 49-51（3 課 × 6 = 18 筆記）
- Agent C: 52-55（4 課 × 6 = 24 筆記）

---

### D6 — Ch06 後半 + Ch02 Eval + Ch09（11 課）

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 56 | prompt-caching | Prompt Caching 概念 | caching-concept |
| 57 | rules-of-prompt-caching | Caching 規則 | caching-rules |
| 58 | prompt-caching-in-action | Caching 實戰 | — |
| 59 | code-execution-and-the-files-api | Code Execution + Files API | code-execution-flow |
| 17 | prompt-evaluation | Prompt 評估概論 | eval-overview |
| 18 | a-typical-eval-workflow | 典型評估工作流 | eval-workflow |
| 19 | generating-test-datasets | 測試資料集生成 | — |
| 20 | running-the-eval | 執行評估 | — |
| 21 | model-based-grading | Model-based 評分 | grading-methods |
| 22 | code-based-grading | Code-based 評分 | — |
| 87 | details (Ch09) | Request 五步驟流程 | request-lifecycle |

**Agent 分配：**
- Agent A: 56-59（4 課 × 6 = 24 筆記）
- Agent B: 17-20（4 課 × 6 = 24 筆記）
- Agent C: 21,22,87（3 課 × 6 = 18 筆記）

---

### D7 — Ch03 Prompt Engineering（5 課）+ 收尾

| # | 課 | 主題 | SVG |
|---|-----|------|-----|
| 25 | prompt-engineering | Prompt Engineering 總論 | prompt-engineering-overview |
| 26 | being-clear-and-direct | 清晰直接原則 | — |
| 27 | being-specific | 具體化原則 | specificity-spectrum |
| 28 | structure-with-xml-tags | XML 結構化 | xml-tag-structure |
| 29 | providing-examples | Few-shot 範例 | few-shot-pattern |

**Agent 分配：**
- Agent A: 25-27（3 課 × 6 = 18 筆記）
- Agent B: 28-29（2 課 × 6 = 12 筆記）

**收尾工作：**
1. 全量 HTML 重建（含 API 課程）
2. 更新 `html/index.html` 加入第 4 門課
3. 更新 `README.md` 統計數字
4. 最終 git push

---

## Token 預算追蹤

| 天 | 筆記 | SVG | 預估 tokens | 累計 |
|----|------|-----|------------|------|
| D1 | 66 | 10 | ~350K | 350K |
| D2 | 66 | 10 | ~350K | 700K |
| D3 | 54 | 8 | ~290K | 990K |
| D4 | 60 | 8 | ~310K | 1,300K |
| D5 | 66 | 10 | ~350K | 1,650K |
| D6 | 66 | 8 | ~340K | 1,990K |
| D7 | 30 | 6 | ~180K | **2,170K** |

---

## 注意事項

- **38-multi-turn-conversations-with-tools** 在 Ch01 目錄下但內容屬 Tool Use，D1 處理
- **Ch07 MCP** 與已有的 MCP 兩門課部分重疊，筆記需標註差異點
- **87-details** 在 Ch09 Assessment 目錄但有完整教學內容（Request lifecycle）
- 每天跑完後立即 commit + push，避免進度遺失
- 若當天 quota 不足，優先完成筆記，SVG 可推遲

---

*Created: 2026-04-09*
