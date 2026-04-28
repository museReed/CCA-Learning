# 定義 Prompts — PM 視角

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.6 (prompt template design), 1.3 (prompt engineering for tools) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 12 |

---

## 一句話摘要

MCP prompts 就像團隊打包進產品的專家腳本 — 使用者不需要成為 prompt 工程專家，就能獲得一致、高品質的 AI 互動。

---

## 為什麼 PM 應該關心 Prompts

Prompts 解決了一個根本的產品問題：**專家使用者與新手使用者之間的品質差距**。

| 使用者類型 | 沒有 MCP Prompts | 有 MCP Prompts |
|-----------|-------------------|-----------------|
| 專家使用者 | 寫出好 prompt，得到好結果 | 同樣好的結果，速度稍快 |
| 一般使用者 | 寫出普通 prompt，得到普通結果 | 透過預建模板獲得專家級結果 |
| 新使用者 | 不知道該問什麼，結果差 | 透過 slash commands 發現工作流程 |

這與 email 範本、Notion 範本庫或 Figma 元件庫是相同的原理 — 封裝專業知識以供重複使用。

---

## 心智模型：餐廳菜單

把 MCP primitives 想像成與餐廳互動的不同方式：

| 互動 | MCP Primitive | 誰決定 | 餐廳類比 |
|-------------|---------------|-------------|-------------------|
| 主廚即興發揮 | **Tool** | 主廚（Claude） | 「主廚推薦 — 給我驚喜」 |
| 服務生送水 | **Resource** | 餐廳（app） | 水自動出現在桌上 |
| 顧客從菜單點餐 | **Prompt** | 顧客（使用者） | 「我要 7 號套餐」 |

Prompts 就是菜單。廚房（MCP server 開發者）精心設計了每道菜（prompt 模板）。顧客（使用者）從測試過的選項中挑選，得到可預測的高品質結果。

---

## 產品使用場景

### 何時使用 Prompts

| 場景 | 為什麼 Prompts 有效 |
|----------|-----------------|
| 「把這份文件轉成 markdown」 | 測試過的模板比使用者的臨時請求更能處理邊界案例 |
| 「從我的筆記生成週報摘要」 | 使用者難以自己撰寫的複雜指令 |
| 「分析這個資料集並建立報告」 | 含多個步驟的領域專屬工作流程 |
| 「翻譯這份文件並保留格式」 | 需要精心 prompt engineering 的細膩指令 |

### 何時不該用 Prompts

| 場景 | 更好的替代方案 |
|----------|--------------------|
| 使用者提出自由問題 | 讓 Claude 直接處理 — 不需要模板 |
| App 需要預載 context | 用 **resource** — app-controlled |
| Claude 需要決定何時行動 | 用 **tool** — model-controlled |

---

## Slash Command UX 模式

Prompts 天然對應 Slack、Notion、Discord 等工具中熟悉的 slash command 模式：

1. **使用者輸入 `/`** — 可用 prompts 作為命令選單出現
2. **使用者選擇命令**（如 `/format`）— 被提示輸入必要參數
3. **使用者提供參數**（如選擇文件）— prompt 模板被填入
4. **模板發送給 Claude** — Claude 收到精心設計的指令
5. **Claude 執行** — 使用可用的 tools 來完成 prompt 的指令

從使用者角度，這感覺像「工作流程按鈕」— 一鍵（或命令）觸發複雜、可靠的操作。

---

## 產品四大好處

1. **一致性** — 每個使用者得到相同品質的指令，消除「prompt 樂透」
2. **專業知識編碼** — 開發者的領域知識烘焙進模板中
3. **可重用性** — 多個 client 應用可共享同一 server 的 prompts
4. **集中維護** — 在 server 上更新 prompt，所有 clients 自動獲得改進

---

## PM 常見錯誤

1. **不投資 prompt 品質** — 把 prompts 當簡單字串而非需要迭代的測試模板
2. **太多 prompts** — 用選擇淹沒使用者；策展一組聚焦的高價值工作流程
3. **PRD 中沒有指定 prompt 參數** — 使用者需要清楚的參數描述；列入驗收標準
4. **混淆 prompts 和 system instructions** — prompts 是使用者觸發的工作流程，不是永遠開啟的行為規則

> **Key Insight**
>
> Prompts 是 **user-controlled** primitive。使用者明確決定何時使用，不同於 tools（Claude 決定）或 resources（app 決定）。對 PM 來說，這直接對應到「工作流程功能」— 使用者啟動結構化、可重複流程的功能。CCA 考試中，控制模型區分（model / app / user）是 D1 和 D2 中最常考的概念。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：知道何時建議用 prompts vs. tools vs. resources。觸發條件是：「預定義工作流程」+「使用者啟動」= prompt。
- **D1 (Agentic Architecture)**：Prompts 屬於使用者控制層。
- 注意考題中的「workflow」或「slash command」— 這些幾乎都指向 prompts。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 誰控制 MCP prompts 的觸發時機？ | 使用者（user-controlled）— 透過 slash commands、按鈕或選單 |
| MCP prompts 解決什麼產品問題？ | 專家與新手使用者之間的品質差距 — prompts 將專業知識封裝為可重用模板 |
| MCP prompts 的餐廳類比是什麼？ | 菜單 — 廚房設計每道菜（模板），顧客（使用者）從測試過的選項中挑選 |
| PM 何時該選 prompt 而非 tool？ | 工作流程是預定義的、可重複的、且由使用者明確觸發時 |
| Prompts 天然對應什麼 UX 模式？ | Slash commands（`/format`、`/summarize`）— 從 Slack、Notion、Discord 熟悉的模式 |
| MCP prompts 的四大產品好處是什麼？ | 一致性、專業知識編碼、可重用性、集中維護 |
| Prompts 和 system instructions 有什麼不同？ | Prompts 是使用者觸發的工作流程；system instructions 是永遠開啟的行為規則 |
| 使用者選擇 prompt 並提供參數後會發生什麼？ | 模板填入參數後作為精心設計的指令發送給 Claude |
