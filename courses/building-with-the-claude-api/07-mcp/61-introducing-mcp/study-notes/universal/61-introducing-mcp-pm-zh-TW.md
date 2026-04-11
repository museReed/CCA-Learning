# Introducing MCP — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、2.1（tool schemas）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 61 |

---

## 一句話總結

MCP 是 Claude 整合的「不要重造輪子」層：你的團隊不用為每一個想串的 SaaS 都去寫 tool 定義、測試、持續維護，而是直接裝一個現成的 MCP server，就能免費繼承整個 tool 目錄。

---

## 心智模型：Claude 的 App Store

把 Ch04 的 tool use 想像成教 Claude 怎麼使用一個你客製打造的裝置；MCP 就是那個裝置連上去的 **App Store**：

| 沒有 MCP | 有 MCP |
|---------|--------|
| 每個整合都是客製品 | 整合可以「安裝」 |
| 工程團隊擁有每個 tool schema | 服務提供者或社群擁有 |
| 加 GitHub 要寫幾十個 schema | 加 GitHub 只要裝一個 server |
| 每次 API 改版都是你的維護問題 | 上游發新版本 |

「App Store」不是官方說法，但它抓住了最重要的產品真相：MCP 徹底改變了整合工作的經濟學。

---

## 這節課為什麼對 PM 重要

一個產品團隊在評估「我們能不能做一個 AI 助理，讓它回答使用者關於我們 GitHub / Jira / Sentry / Notion 的問題？」歷來答案都是：

> 「可以，但要花 3-6 個月工程來寫和維護這些 tool 整合。」

MCP 把這個時間線大幅壓縮。粗略估計：

| 整合來源 | 大概多久可以「Claude 能用」 |
|---------|---------------------------|
| 為單一 SaaS 客製寫 tools | 數週到數月 |
| 安裝官方 MCP server | 數小時 |
| 安裝社群 MCP server | 數小時（加上 due diligence） |
| 還沒有 MCP server | 回到原本的時間線 |

PM 在評估任何會碰外部系統的 AI 功能時，第一個該問的問題是：「這個服務有沒有現成的 MCP server？」

---

## 用 PM 語言翻譯 GitHub 範例

這節課用 GitHub 當主要範例。PM 應該這樣內化：

> 「讓 Claude 能回答*任何*GitHub 問題，成本是多少？」

沒有 MCP 的話，「任何 GitHub 問題」意味著你要承諾撰寫、測試、維護一個 tool 給使用者可能提到的每個功能：repos、PRs、issues、projects、releases、actions、reviews、members、permissions、search、notifications。那是一個跨季度的專案——還沒輪到 Jira 或 Slack。

有了 MCP，「任何 GitHub 問題」只要連到 GitHub MCP server——tools 都已經寫好了，服務提供者（或可信的社群）會維護它們。

---

## 產品應用場景

### MCP 是對的答案

| 情境 | 為什麼 MCP 合適 |
|------|---------------|
| 橫跨多個 SaaS 工具的 AI 助理 | N 個 install 指令換 N 個生態系 |
| 來自利害關係人的長尾整合需求 | 可以增量加，不用重構架構 |
| 內部「AI 對公司資料」的 pilot | 把內部 API 包成一個 MCP server，所有 Claude 產品都能用 |
| 需要很多小動作的 agent workflow | 每個動作都是現成的 MCP tool |

### MCP 太重了

| 情境 | 改用什麼 |
|------|---------|
| 對簡單內部 endpoint 的一次性查詢 | 直接寫 tool 比裝 server 快 |
| 只需要讀一份靜態文件 | 用 resource 或純 context |
| 還在驗證使用者是否需要這個功能 | 先 hard-code，等到訊號明確再說 |

---

## PM 決策框架

有人提議「我們加 X 整合」時要問：

1. **廠商有沒有官方 MCP server？** 先從這裡開始——品質最高。
2. **有社群 MCP server 嗎？** 可以用，但要做資安和維護的 due diligence。
3. **如果都沒有，這個功能值得自己寫嗎？** 用「每週會用或涉及安全」的標準。
4. **我們真正需要廠商 API 的哪個子集？** 避免 scope creep——如果只要 3 個功能，不要裝 80 個 tools。
5. **MCP server 掛掉時有什麼 fallback？** MCP server 是獨立 process，要規劃失敗情境。

---

## 隱藏的 PM 優勢

Tools/prompts/resources 這三種 primitive 也是 PM 的槓桿點：

| Primitive | PM 真正買到的東西 |
|-----------|------------------|
| Tools | 助理能代替使用者做的動作 |
| Prompts | 預先寫好的 workflow，一鍵載入 |
| Resources | 助理可以讀取的策展過的資料面 |

PM 可以把 MCP 採用 scope 成「裝這個 server 用它的 tools，順便把它的 prompts 開放給 power users」——同一個 server 能交付多層價值。

---

## 生態系定位

PM 也該知道：

| 事實 | 產品意涵 |
|------|---------|
| MCP 是開放協定 | 你沒有被鎖在 Anthropic；整合可以搬到其他 model host |
| 任何人都能寫 server | 廠商、社群、你的內部平台團隊 |
| 服務提供者常釋出官方 server | 評估功能時第一站 |
| 生態系成長很快 | 「還沒有 MCP server」這個回答的半衰期很短 |

---

## 常見 PM 錯誤

1. **把 MCP 當成技術細節** — 它是每一次整合的 *buy vs build* 決策。
2. **沒問使用者實際需要什麼 tools 就裝一堆 server** — tool 氾濫會膨脹 context 拖慢回應。
3. **以為 MCP 解決 auth** — 憑證管理、rate limits、權限還是你產品的問題。
4. **忘了預算 server 的更新** — MCP server 有版本，過期的版本會默默出錯。
5. **把 MCP 和 tool use 搞混** — tool use 是 Claude 協定，MCP tools 還是跑在上面。你不能跳過學 tool use。

> **Key Insight**
>
> MCP 不是技術升級，而是**經濟**升級。它把「讓 AI 功能接觸真實系統」的主要成本（撰寫和維護 tool 整合）交給別人承擔。PM 的工作是注意到：「我們該自己寫這個整合嗎？」的答案已經從「好幾個月的工作」變成「一行 install 指令」——然後重新排優先序。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 MCP 是什麼、誰在寫 MCP servers、三種 primitives。
- **D1（Agentic Architecture）**：了解 MCP 是 agent 插入的可重複使用整合層。
- 考題常問「MCP 解決什麼問題？」——答案是*撰寫/維護 tool 整合的負擔*。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| MCP 一句話 pitch 是什麼？ | 一個讓你「安裝」現成 tool 整合到 Claude 的協定，而不用自己寫。 |
| PM 在評估新 Claude 整合時第一個該問什麼？ | 「這個服務有沒有官方或社群的 MCP server？」 |
| MCP 的三種 primitives 是什麼？ | Tools、Prompts、Resources |
| MCP 取代 tool use 嗎？ | 不——它是分發層，還是跑在 tool use 上面。 |
| 誰常寫 MCP server？ | 服務提供者（官方）、社群維護者、或你自己的內部團隊 |
| PM 採用 MCP server 時該預算什麼？ | Token 成本、延遲、故障面、資安審查、版本維護 |
| MCP 是 Anthropic 專屬嗎？ | 不——它是開放協定，任何 model host 或 application 都能用。 |
| GitHub 範例中呈現的主要問題是什麼？ | 要為單一服務的 API 撰寫和維護幾十個客製 tools。 |
