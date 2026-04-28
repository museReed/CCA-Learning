# Enhancements with MCP Servers — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D3 — Claude Code Configuration (20%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 3.2（Claude Code MCP 整合）、2.3（MCP primitives）、1.1（Claude Code 擴充模型） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 76 |

---

## 一句話總結

MCP server 是 Claude Code 的「app store」—— 讓 PM 能用模組化能力（Sentry、Jira、Slack、Figma、內部自訂 API）組合 agent，不用拜託 Anthropic 或工程師開發，只要一條指令：`claude mcp add`。

---

## 心智模型：Agent 的外掛架構

把 Claude Code 想成延長線、MCP server 想成你插上去的電器：

| 延長線比喻 | Claude Code 實際對應 |
|-----------|---------------------|
| 延長線本體 | Claude Code 與它內建的檔案、shell、web 工具 |
| 每個插座 | 一個 MCP client 連線 |
| 插上去的電器 | MCP server（sentry-mcp、playwright-mcp、內部自建 server） |
| 新增電器 | `claude mcp add [name] [command]` |

關鍵洞察：延長線從設計上就是要你能插任何東西。你不用把延長線寄回工廠才能加新電器。

---

## 為什麼這 lesson 對 PM 重要

Lesson 75 為止，Claude Code 看起來像 coding assistant。Lesson 76 揭露它實際是什麼 —— **workflow orchestration 平台**。有了 MCP server，Claude Code 能橫跨你整條工具鏈：

| 沒 MCP 之前 | 有 MCP 之後 |
|------------|------------|
| 讀寫 code | 讀 Jira ticket、寫 code、查 Sentry、更新 Slack |
| 侷限在終端機 | 橫跨整個 SaaS stack |
| 幫個人 | 能驅動整個團隊的 workflow |

對 PM 評估 Claude Code 在組織中的定位來說，這是它從「不錯的開發工具」升級為「平台決策」的關鍵 moment。

---

## 產品使用情境

### 何時投資 MCP server

| 情境 | 要加的 MCP server |
|------|------------------|
| 生產環境 bug triage | sentry-mcp + mcp-atlassian + slack-mcp |
| Spec-driven 功能開發 | mcp-atlassian + figma-context-mcp |
| QA 自動化 | playwright-mcp +（內部 fixture server） |
| 研究與爬蟲 | firecrawl-mcp-server |
| 內部系統存取 | 為你的 API 自建 MCP server |

### 何時 MCP server 是過度工程

| 情境 | 替代方案 |
|------|---------|
| 一次性呼叫你 API 的腳本 | 請 Claude 寫 Python 腳本跑一次 |
| 唯讀文件 | 用 Claude Code 內建 web fetch |
| 一個月才做一次的動作 | 手動仍比建整合便宜 |

好的判斷原則：只有每週都會用或是關鍵安全流程，才值得建或裝 MCP server。

---

## 六個生態 Server（PM 必記）

PM 要能快速回答「生態裡已經有這個了嗎？」的問題：

| Server | 商業用例 | 決策框架 |
|--------|---------|---------|
| **sentry-mcp** | 自動發現與修復 bug | 「接 Claude 到我們的監控平台」 |
| **playwright-mcp** | 瀏覽器自動化做測試 | 「讓 Claude 跑 end-to-end 測試」 |
| **figma-context-mcp** | Claude 讀設計檔 | 「讓 Claude 實作設計稿」 |
| **mcp-atlassian** | Claude 讀 Jira/Confluence | 「讓 Claude 看 spec 和 ticket」 |
| **firecrawl-mcp-server** | Claude 爬網頁 | 「讓 Claude 做競品研究」 |
| **slack-mcp** | Claude 發 Slack 訊息 | 「讓 Claude 跟團隊溝通」 |

利害關係人問「Claude 能不能做 X？」時，先查這份清單，再談自建。

---

## PM 決策框架

團隊提議「加一個 MCP server」時，問：

1. **生態裡已經有了嗎？** 先查上面六個加廣義的 MCP ecosystem。
2. **這個 workflow 實際需要哪種 primitive？** Tool（動作）、prompt（模板）還是 resource（資料）？多半是 tool。
3. **信任邊界在哪？** 每個 MCP server 是獨立 process —— 整合會觸及生產環境嗎？要加核准步驟。
4. **誰擁有這個 server？** 內部 server 要有 owner team。外部 server 要 pin 版本並有更新計畫。
5. **Server 掛掉時的 fallback 是什麼？** Claude Code 的 agent loop 會退化 —— 要預先規劃。

---

## 組合故事：把 Server 疊成 Workflow

本 lesson 對 PM 最重要的概念是：你可以組合多個 MCP server 涵蓋完整 workflow。範例 —— 生產環境 bug workflow：

| 步驟 | 發生什麼 | 使用的 MCP server |
|-----|---------|------------------|
| 1. 新 error 進來 | 告訴 Claude：「修最新的 Sentry P1」 | sentry-mcp |
| 2. 讀 ticket | Claude 找出關聯 Jira ticket | mcp-atlassian |
| 3. 讀相關 code | Claude 用內建檔案工具 | （內建） |
| 4. 實作修復 | Claude 改檔、跑 test | （內建） |
| 5. 瀏覽器驗證 | Claude 跑 Playwright 測試 | playwright-mcp |
| 6. 通知團隊 | Claude 在 Slack 貼總結 | slack-mcp |

四個 MCP server 加上 Claude Code 內建工具，就涵蓋整個生產 hotfix workflow。PM 的任務是辨認哪些這類 stack 對組織有價值，然後核准 rollout。

---

## 定價與運維視角

加 MCP server 有真實的運維成本。PM 要編預算：

| 成本 | 說明 |
|------|------|
| Token 成本 | 工具越多，每回合吃的 context window 越大 |
| 延遲 | 每個 MCP server 是子 process —— 慢的 server 拖慢 agent |
| 失敗面 | 任何 server 掛掉都可能在 workflow 中斷 agent |
| 安全審查 | 每個整合都是新資料路徑 —— 要 review |
| 更新 | Server 有版本；過時版本會靜默掛掉 |

這些都不是 deal-breaker，只是 rollout 計畫要涵蓋的項目。

---

## 常見 PM 錯誤

1. **生態已有時還自建** —— 先查六個 named server。
2. **想到什麼 server 都加** —— 每個都耗 context 和延遲；要 curate。
3. **沒定義 owner** —— 沒 owner 的內部 MCP server 會快速腐爛。
4. **忽略信任邊界** —— 能發 Slack 訊息的 server 也能發錯訊息。破壞性動作要加確認步驟。
5. **混淆 MCP server 與 API key** —— MCP 是 protocol，不是憑證。Auth 仍然是你的問題。

> **關鍵洞察**
>
> MCP 把 Claude Code 從開發工具變成 **workflow orchestration 平台**。`claude mcp add` 這條指令是 PM 視角中 agent 從「幫忙寫 code」畢業到「驅動跨系統 workflow」的 moment。把 MCP 採用視為平台決策，不是開發者個人喜好。

---

## CCA 考試重點

- **D3（Claude Code Configuration）**：要記得 `claude mcp add` 指令和 Claude Code 內建 MCP client 的事實。
- **D2（Tool Design & MCP Integration）**：要知道三種 primitive（tool、prompt、resource）。
- **D1（Agentic Coding & Architecture）**：準備好情境題 —— 組合多個 server 成 workflow。
- 對 named server 的辨認題（sentry、playwright、figma、atlassian、firecrawl、slack）機率很高。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 需要核准/文件化、用來加 MCP server 的指令是什麼？ | `claude mcp add [server-name] [command-to-start-server]` |
| MCP server 可暴露的三種 primitive 是什麼？ | Tools（執行動作）、Prompts（可重用模板）、Resources（存取資料） |
| 讓 Claude 自動處理 monitoring 平台記錄的 bug，用哪個 MCP server？ | `sentry-mcp` |
| 讓 Claude 讀 Jira ticket 和 Confluence 頁面用哪個 MCP server？ | `mcp-atlassian` |
| 讓 Claude 在團隊頻道發訊息用哪個 MCP server？ | `slack-mcp` |
| 決定是否自建 MCP server 的 PM 判斷標準？ | 整合是否每週都會用或是關鍵安全流程？是則建；否則延後 |
| 舉一個涵蓋生產 hotfix workflow 的四 server stack。 | sentry-mcp（triage）+ mcp-atlassian（ticket）+ playwright-mcp（驗證）+ slack-mcp（通知），加上 Claude Code 內建工具 |
| 採用 MCP server 時 PM 要編的運維成本有哪些？ | Token 成本、延遲、失敗面、安全審查、版本/更新維護 |
