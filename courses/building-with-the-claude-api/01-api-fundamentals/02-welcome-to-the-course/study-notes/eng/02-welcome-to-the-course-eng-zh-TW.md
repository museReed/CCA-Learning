# Welcome to the Course — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D1 — Agentic Coding Fundamentals (22%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 1.1（對 Claude 能力的基礎理解）、5.1（模型選擇與部署準備） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 02 |

---

## One-Liner

這堂導覽課程勾勒出完整學習路徑——從 API 存取、提示工程、工具使用、RAG、MCP、Claude Code 到代理工作流——並設定先決條件：Python、Notebook 及 Anthropic API 金鑰。

---

## 課程拓撲結構

課程遵循明確的相依鏈。每個模組都建立在前一個模組之上：

```
API 基礎 → 提示評估 → 提示工程 → 工具使用 → RAG → MCP → Claude Code / Computer Use → 工作流與代理
```

| 模組 | 你會建構什麼 | CCA 考試對應 |
|------|------------|-------------|
| API 基礎 | 第一次請求、多輪對話、串流 | D5：每個生產應用都從這裡開始 |
| 提示評估 | 評估框架、測試資料集 | D1：無法衡量就無法改進 |
| 提示工程 | 清晰度、具體性、XML 結構 | D1：提示設計是核心代理技能 |
| 工具使用 | 工具 schema、多工具編排 | D2：MCP 和工具設計的基礎 |
| RAG | 分塊、嵌入向量、檢索 | D5：企業級知識接地 |
| MCP | Server、Client、Resource、Prompt | D2：連接 Claude 與外部世界的協定 |
| Claude Code + Computer Use | 終端代理、瀏覽器代理 | D1/D3：代理式編碼的實踐 |
| 工作流與代理 | 平行化、串聯、路由 | D1：代理架構模式 |

---

## 先決條件清單

在撰寫任何程式碼之前，確認以下環境就緒：

```bash
# 1. 支援 Notebook 的 Python 環境
python3 --version          # 建議 3.10+
pip install jupyter anthropic

# 2. Anthropic API 金鑰
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. 驗證存取
python3 -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-sonnet-4-5', max_tokens=50, messages=[{'role':'user','content':'ping'}]).content[0].text)"
```

上述任何一步失敗，就先修好再繼續。整門課程都在 Notebook 中執行，環境壞掉等於學習速度歸零。

---

## 成功策略（工程視角）

| 講師建議 | 工程解讀 |
|---------|---------|
| 跟著我一起寫程式碼 | 每段程式碼都自己打一遍；肌肉記憶能鞏固 API 模式 |
| 加快播放速度 | 1.5x–2x 先掃概念，再暫停實作 |
| 擴展 / 修改 Notebook | 最好的學習發生在你故意把東西弄壞的時候 |
| 遇到問題就問 Claude | 用 Claude 來除錯 Claude API 程式碼——這是元學習 |

最後一點常被低估：用 Claude 除錯 Claude API 程式碼是一個緊密的回饋迴路，完美映射了真實的代理式編碼工作流。

---

## 常見錯誤

1. **跳過環境設置** —— 所有 API 課程中一半的「卡住」時刻都是 import 錯誤和缺少金鑰，而非概念性問題。
2. **只看不寫** —— 被動觀看影片對 API 模式的記憶留存率接近零。
3. **直接跳到代理** —— 相依鏈是真實存在的；沒有提示工程知識就使用工具會導致脆弱的 schema。
4. **忽略提示評估** —— 講師稱之為「最重要的實踐」。跳過評估的工程師寫出的提示在自己機器上能用，但在生產環境中失敗。

> **核心洞察**
>
> 這不是一門「看了就會」的課程——而是「邊做邊破」的課程。相依鏈意味著每個模組會產出成品（Notebook、提示、工具 schema），作為下一個模組的輸入。跳過任何一個模組等於漏掉一個相依項，而不只是錯過內容。

---

## CCA 考試相關性

- **D1（代理式編碼基礎）**：課程拓撲結構就是 CCA 技能地圖——API → 提示 → 工具 → 代理，映射考試的預期進程。
- **D5（企業部署模式）**：先決條件（API 金鑰管理、環境設置）是企業部署的第一天必備。
- 預期考試會假設你對此處列出的每個模組都有實作經驗；這堂課就是整個路線圖。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 這門課程的三個先決條件是什麼？ | 基礎 Python 知識、Notebook 環境、Anthropic API 金鑰 |
| 課程模組順序是什麼？ | API 基礎 → 提示評估 → 提示工程 → 工具使用 → RAG → MCP → Claude Code/Computer Use → 工作流與代理 |
| 為什麼講師強調要跟著寫程式碼？ | 被動觀看對 API 模式的記憶留存接近零；打字能建立肌肉記憶 |
| 講師稱哪個模組為「最重要的實踐」？ | 提示評估——唯一能在規模化驗證提示有效性的方法 |
| 課程涵蓋哪兩個 Anthropic 自建的代理？ | Claude Code（終端代理）和 Computer Use（瀏覽器代理） |
| 為什麼模組順序是相依鏈？ | 每個模組的產出（Notebook、schema、提示）是下一個模組的輸入 |
| 卡住時的建議策略是什麼？ | 問 Claude 求助——用 Claude 除錯 Claude API 程式碼是一個元學習迴路 |
