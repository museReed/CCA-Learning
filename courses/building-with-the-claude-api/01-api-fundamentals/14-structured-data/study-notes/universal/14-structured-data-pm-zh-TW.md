# Structured Data — PM 視角

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design & MCP Integration (18%) 次要 |
| Task Statements | 5.3（production 模式）、1.3（prompt engineering）、2.1（結構化輸出） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 14 |

---

## 一句話總結

當你的產品需要 raw data——一個 JSON object、code snippet、條列清單——不要閒聊前言時，你用兩件一組的技巧（prefill + stop sequence）讓 Claude 交回乾淨輸出，使用者可以直接 copy-paste 或下游系統可以直接 parse 而不用額外處理。

---

## 心智模型：販賣機 vs 親切咖啡師

想兩種買咖啡的方式：

| 互動 | 類比 | 輸出 |
|------|------|------|
| 親切咖啡師 | 預設 Claude | 「來，你的拿鐵！今天多加了一點奶泡，希望你喜歡。有需要隨時說！」+ 咖啡 |
| 販賣機 | Prefilled Claude | *click* → 咖啡 |

兩者都交出咖啡。但如果你是把咖啡接進管線（下游系統）的產品，咖啡師的閒聊會塞住管線。結構化資料技巧把 Claude 變成販賣機，用於閒聊是摩擦而非友善的情境。

---

## 產品問題

想像一個 AWS EventBridge 規則產生器：使用者輸入描述、按產生、預期按「複製」拿到乾淨 JSON，直接貼到 AWS console。如果 Claude 回傳：

````
```json
{ ... }
```
This rule captures EC2 instance state changes when instances start running.
````

那「複製」按鈕會：

1. 複製太多——使用者把 markdown fences 和一句英文貼進 AWS，被拒絕
2. 需要 client 端 custom parsing 邏輯——當 Claude 用不同方式寫解釋就失敗

兩種結果都是產品品質 bug。結構化資料技巧完全消除這類 bug。

---

## 產品使用情境

### 什麼時候需要結構化輸出

| 產品 | 需要什麼 |
|------|---------|
| API 回應產生器 | 純 JSON body |
| Code 產生器 / snippet 工具 | 乾淨 code 無評論 |
| 設定檔建立器（YAML、JSON、TOML）| 可直接存檔的檔案內容 |
| 從非結構化文字抽資料 | 可 parse 的 JSON 進 database |
| CSV / 試算表 row 產生器 | 可匯入的 rows |
| SQL query 建立器 | 可執行的 SQL，別無其他 |

### 什麼時候閒聊輸出沒問題

| 產品 | 原因 |
|------|------|
| 對話式 chat | 使用者*想要* context 和友善 |
| 家教 app | 解釋本身就是產品 |
| Summarizer | 散文就是輸出 |
| 創意寫作 | 評論可以是聲音的一部分 |

測試：是人類要讀這個輸出，還是機器要 parse？如果是後者，你需要結構化輸出。

---

## Copy-Paste 測試

這是簡單的 PM 測試：如果你的 feature 有「複製」按鈕，輸出應該不用編輯就能貼。如果 Claude 產生的輸出在可用前需要任何手動清理，你的產品就壞了。

設計審查時跑這個測試：

1. 用當前 prompt 從 Claude 產生真實回應
2. 按「複製」
3. 貼到目標環境（AWS console、code editor、試算表）
4. 能用嗎？不能的話，你需要結構化資料技巧

這是五分鐘的測試，能在上線前抓住最常見的 AI 產品 bug 之一。

---

## PM 決策框架

| 問題 | 如果 Yes | 意涵 |
|------|---------|------|
| 輸出會餵給下游 parser 或自動 pipeline 嗎？ | Yes | 必須用結構化輸出 |
| UI 有「複製」按鈕嗎？ | Yes | 必須用結構化輸出 |
| 使用者會把回應跟規格（AWS rule、JSON schema）比對嗎？ | Yes | 必須用結構化輸出 |
| 輸出只給人類閱讀嗎？ | No | 預設 Claude 可以 |
| 使用者能忍受自己清理輸出嗎？ | No | 必須用結構化輸出 |

任何「yes」條件成立時，把「輸出必須是乾淨、可 parse 的 [格式]」寫進 PRD 驗收標準。

---

## 和 Tool Use 的取捨

課程後面，tool use 提供另一種取得結構化 JSON 的方式——Claude 回傳一個 schema 驗證過的 tool-call object。身為 PM，理解差別：

| 方法 | 優點 | 缺點 |
|------|------|------|
| Prefill + stop sequence | 簡單，任何格式都行（code、CSV、YAML、XML），不需 schema | 無 type 驗證；Claude 還是可能吐 malformed data |
| Tool use + `input_schema` | Schema 驗證、type 安全、agent 式組合性 | 較複雜、只能 JSON |

**PM 經驗法則：** 快速原型和非 JSON 格式用 prefill + stop sequence 就好。下游系統依賴的 production JSON 生成，堅持用有 schema 的 tool use。

---

## 常見 PM 錯誤

1. **假設 Claude「就會回 JSON」**——它預設回 JSON 加解釋。結構化資料技巧是必要
2. **沒在目標環境測試 copy-paste**——bug 只在真實使用者嘗試用輸出時才出現
3. **在 system prompt 寫「輸出乾淨 JSON」就當作完成**——Claude 還是會加評論。你需要 prefill + stop sequence 或 tool use
4. **沒編列 retry 邏輯預算**——就算有 prefill，Claude 偶爾還是會吐 malformed 輸出。Production feature 需要 JSON parse retry
5. **在 API 回應用閒聊輸出**——下游整合者假設契約；評論打破每個 consumer

> **Key Insight**
>
> 結構化資料不是 nice-to-have——它是使用者能真的在下游 workflow 用起來的 AI feature 和「幾乎可用」輸出之間的差別。Prefill + stop sequence 模式是「讓 Claude 閉嘴只回那個東西」最簡單的 PM 面向配方。知道什麼時候伸手用它；知道什麼時候 tool use 才是更好的答案。

---

## CCA 考試重點

- **D5.3（production 模式）**：預期考情境題，問如何讓 Claude 回傳純 JSON 給下游消費
- **D2 (Tool Design)**：tool use 是 production 級 JSON 的替代方案——考試可能要你在兩者間選
- 注意「Claude 把輸出包在 markdown fences 裡並加解釋」這種措辭——答案是 prefill + stop sequence（或 tool use）

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 結構化資料技巧解決什麼產品問題？ | Claude 預設把結構化輸出包在 markdown fences 裡並加英文評論，打破下游 parsing 和 copy-paste UX |
| PM 級的「copy-paste 測試」是什麼？ | 產生真實回應、按複製、貼到目標環境。不能用的話，你的產品需要結構化輸出 |
| 結合起來強制乾淨結構化輸出的兩個技巧是什麼？ | Assistant message prefilling 和 stop sequences |
| 什麼時候閒聊輸出是對的選擇？ | 對話式 chat、家教、summarization、創意寫作——任何人類直接讀輸出的地方 |
| 什麼時候結構化輸出是必須？ | 任何輸出餵給 parser、automation pipeline、copy 按鈕或有 schema 契約的地方 |
| 和 tool use 的取捨是什麼？ | Prefill 對任何格式有效不需 schema；tool use 只能 JSON 但提供 schema 驗證和 type 安全 |
| 為什麼在 system prompt 寫「請只回 JSON」不夠？ | Claude 的 helpful 行為還是會漏評論——你需要結構強制，不只是指令 |
| 販賣機類比是什麼？ | 預設 Claude 是加閒聊的親切咖啡師；prefilled Claude 是只交出產品的販賣機 |
