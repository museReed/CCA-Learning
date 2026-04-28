# Web Search Tool — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D4 — AI Safety & Alignment (20%) |
| Task Statements | 2.3（built-in server tools）、4.2（grounding 與 citation） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 43 |

---

## One-Liner

為產品加上 web search 現在是一行設定的決策：Anthropic 處理搜尋、解析、citation，你的團隊只要把 result block 渲染到 UI。

---

## Mental Model：擁有圖書證的研究助理

Server tool 出現前，要給 AI 搜尋網路能力意味著建 search pipeline、scrape、清資料、排序、citation 抽取——就像僱一個研究員還要幫他架一整間圖書館。Web search tool 就像發給研究助理一張圖書證：他知道怎麼用、會帶來源回來、每一個論點都有 footnote。

| 能力 | 自己做 | 用 Web Search Tool |
|------|------|--------------------|
| 搜尋基礎設施 | 幾週工程 | 今天就上 |
| 內容解析 | 依來源自定義 | 已處理 |
| Citation 格式化 | 自訂邏輯 | 內建 block |
| Domain 限制 | 自訂 allowlist | `allowed_domains` 欄位 |
| 持續維護 | 你的團隊一直扛 | Anthropic |

上市時間通常快 10-100 倍。

---

## 為什麼 Citation 是產品功能

Web search tool 不只是回傳搜尋結果——它還回傳**引用支撐每個陳述的具體來源文字**。對產品而言，這改變一切：

- **信任**：使用者看到答案出處，不只是原生生成
- **合規**：受規管產業要求來源可追溯
- **稽核**：內部使用者可驗證 Claude 的推理
- **責任降低**：「Claude 說的」變成「這個可驗證來源說的」

沒 grounding 的 LLM 輸出在醫療、法律、金融、政府很難賣。帶 citation 的 grounded 輸出能解鎖這些市場。

---

## Product Use Cases

### Web Search Tool 的明顯贏面

| 產品 | 價值 |
|------|-----|
| 時事型助手 | 模型 cutoff 之後的新資訊 |
| 醫療資訊產品 | NIH/PubMed 限制 + citation 保證安全 |
| 法律研究 copilot | `.gov` / `.edu` 限制 + 可驗證引用 |
| 競爭情報 | 當前市場資料而非訓練舊資料 |
| 財經分析助手 | 即時股票 / 總經資料附來源 |
| 快速變動文件的客服 | 永遠最新的答案 |

### 什麼時候不用

| 情境 | 更好的替代 |
|------|-----------|
| 訓練資料就能完全回答的問題 | 跳過這個 tool——省成本與延遲 |
| 私有 / 專屬資訊 | 用你自己的 document 建自訂檢索 tool |
| 離線 / 無網路環境 | Web search 需要連到 Anthropic 後端 |
| 高流量、對延遲敏感的 endpoint | 每次搜尋都加時間，請抓好預算 |

---

## PM 的關鍵設定槓桿

### 1. `max_uses`——成本與延遲的天花板

Claude 可能會發追蹤搜尋以精煉答案，`max_uses` 就是上限。

- **1-2**：便宜、快，可能漏細節
- **3-5**：研究類使用情境的標準區間
- **10+**：深度研究；預算要抓好

### 2. `allowed_domains`——內容品質的槓桿

這是 PM 最被低估的控制：

- 限定 PubMed 會把泛用健康 bot 變成實證醫療助手
- 限定 SEC filings 會把 chatbot 變成合規的財經工具
- 限定自家文件會變成有 grounding 的內部知識庫

Domain 限制就是你把**信任**建進產品的方式。

### 3. Console Privacy 設定

Web search 必須在 Anthropic console 的 privacy 設定中以 organization 層級啟用。PM 要把它放進環境 setup checklist。

---

## PM Decision Framework

| 問題 | 如果 Yes | 行動 |
|------|---------|------|
| 使用者會問時事 / 最新資訊嗎？ | Yes | 啟用 web search |
| 內容品質與信任很關鍵嗎？ | Yes | `allowed_domains` 抓緊 |
| 答案需要 citation 符合合規嗎？ | Yes | 突出渲染 citation block |
| 這是對延遲敏感的 endpoint 嗎？ | Yes | 降 `max_uses`；考慮 cache |
| 資料是私有 / 內部嗎？ | Yes | 改建自訂檢索 tool |

---

## 渲染很重要

Response 會回傳幾種 block——text、search result、citation。這些不能互換：

1. **Web search result** 以「來源」清單呈現（信任訊號、一眼可見）
2. **Citation block** 以行內連結嵌入答案（每個論點的佐證）
3. **Text block** 作為主答案內容

把一切合併成純字串的產品會失去信任優勢。區分渲染的產品可測量到真實的信任與點擊提升。

---

## Common PM Mistakes

1. **把 web search 當成後端問題** — Citation 渲染是核心 UX 決策，請自己掌握。
2. **敏感主題把 `allowed_domains` 留空** — 醫療、法律、金融產品從第一天就需要 domain 限制。
3. **沒量測 citation 點擊率** — 這是關鍵信任指標，請儀表化。
4. **「以防萬一」把 `max_uses` 設太高** — 成本與延遲會隨每次追蹤搜尋累積。
5. **忘了 console privacy 開關** — 如果 org 設定是關的，staging / production 會靜默失敗。

> **Key Insight**
>
> Web search 是完全託管的 server tool：Anthropic 擁有執行，你擁有渲染。產品價值是**grounded、有 citation、新鮮的答案**，幾乎不需要工程投入。把省下來的時間投在優秀的 citation UI，因為那裡才是信任真正贏來的地方。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：Web search 是典型的「server tool」——由 Anthropic 完全執行。要知道它與 text editor（本地執行）的對比。
- **D4 (AI Safety & Alignment)**：Citation 與 grounding 是信任機制；題目可能問哪個 tool 內建 citation。
- 情境題常比較自建搜尋 vs. server tool——除非資料是私有，server tool 幾乎永遠是正解。

---

## Flashcards

| Front | Back |
|-------|------|
| 誰執行 web search tool？ | Anthropic——是完全託管的 server tool，你不用寫任何本地 code |
| 哪個欄位限制每請求的搜尋次數？ | `max_uses` |
| 哪個欄位限定搜尋到特定網域？ | `allowed_domains` |
| Citation block 帶來什麼產品價值？ | Grounded、可驗證的答案——使用者可以點到每個陳述的來源 |
| 使用 web search 前必須在 Anthropic console 啟用什麼？ | Organization privacy 設定中的 web search tool |
| 為什麼 `allowed_domains` 對受規管產業重要？ | 它把 Claude 限縮到權威來源（醫療限 NIH、法律限 `.gov`），提升信任與合規 |
| 列出兩個不該用 web search 的產品情境。 | 私有 / 專屬資料；離線環境 |
| 使用 web search 時信任的主要 UX 槓桿是什麼？ | 突出渲染 citation block——行內與來源清單並用 |
