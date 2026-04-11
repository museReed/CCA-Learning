# Citations — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D4 — AI Safety & Alignment (20%) — 主要；D2 — Tool Design & MCP Integration (18%) — 次要 |
| Task Statements | 4.2（grounded outputs）、2.2（content blocks）、5.4（信任與可驗證性） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 55 |

---

## One-Liner

Citations 是任何使用者需要知道「這個答案哪來的？」的 Claude 功能的信任層——它把 Claude 從黑盒變成會攤開工作過程的研究助理。

---

## Mental Model：會拿出收據的研究助理

想像你請一個研究助理讀一疊合約、做摘要。兩種情境：

- **沒有 citations**：助理交給你一份摘要然後說「相信我」。你沒辦法驗證，若摘要出錯你也不知道是哪份文件誤導了他。
- **有 citations**：摘要裡每句話都有註腳，指向某份合約裡某條具體條款。你可以在幾秒內抽檢任何一項。

Citations 就是 Claude 的註腳。代價是稍微複雜的回應處理；收益是使用者願意用這個功能做真實決策。

---

## PM 為什麼該在意

Citations 是讓高代價文件功能能夠上線的關鍵功能。沒有它：

- 法務團隊不會用 AI 合約審查器。
- 合規不會批准政策 QA 工具。
- 醫師不會依賴臨床參考助理。
- 金融分析師不會信任從 10-K 擷取出的資料。

有了它，上述所有功能突然都能過關。使用者可以在採取行動前驗證任何陳述。稽核員有可追溯軌跡。面向客戶的產品可以說「這是來源」而不是「請相信我們的 AI」。

如果你的產品在受管制、高代價或企業環境裡，citations 幾乎從來不是可選項。

---

## Product Use Cases

### Citations 必備的情境

| 產品情境 | 為何強制要有 citations |
|---------|----------------------|
| 法律研究、合約審查 | 律師對每個主張都要引用原條款 |
| 臨床決策支援 | 臨床醫師採取行動前需驗證來源指引 |
| 金融分析 | 稽核員要求可追溯的證據鏈 |
| 法規 / 合規 QA | 監管機關要求證明答案來自政策原文 |
| 企業知識搜尋 | 內部使用者想從答案跳到來源文件 |
| 學術或研究工具 | 研究者無法引用指不出的來源 |

### Citations 可選的情境

| 產品情境 | 原因 |
|---------|------|
| 閒聊 / 創意寫作 | 沒有依據型的來源 |
| 用 Claude 一般知識做 brainstorming | 來源是訓練資料，不可引用 |
| 對使用者口述內容做摘要 | 沒有書面文件可引用 |
| 無出貨承諾的內部原型 | 只在「信任是需求」時才付複雜度 |

---

## PM 決策框架

設計以文件為依據的功能時要問：

| 問題 | 若答 Yes | 意涵 |
|------|---------|------|
| 使用者會基於 Claude 的答案做決策嗎？ | Yes | 幾乎一定要有 citations。 |
| Workflow 是受管制的（法律、醫療、金融、合規）？ | Yes | Citations 強制要有——第一個 release 就要上。 |
| 內部稽核或外部審查者會看到 Claude 的輸出？ | Yes | Citations 會產生他們需要的軌跡。 |
| 使用者能容忍 citation 標記帶來的一點 UI 複雜度嗎？ | Yes | 建 hover-to-verify pattern。 |
| 單一 request 用多份文件嗎？ | Yes | `document_index` 和 `document_title` 很重要，UI 要追蹤。 |
| 我們用的是純文字 RAG chunks 而不是 PDF？ | Yes | Citations 仍然能用，只是回的是字元位置不是頁碼。 |

---

## Cost、Complexity、UX 權衡

Citations 是 API 裡最便宜、最高影響力的功能之一。成本：

- **回應處理稍微複雜。** 工程端要迭代 content blocks 並把 citation metadata 拉到 UI。
- **每次呼叫有少許 token 開銷**，因為 Claude 會在文字旁邊吐 citation metadata。
- **UX 設計工作**，要做 hover-and-verify pattern。

效益：

- **信任。** 使用者真的會拿輸出來用。
- **法規通過。** 法務與合規能批准原本會擋下來的功能。
- **幻覺事件更少。** Citations 會顯示 Claude 在引文件還是在外推——是自然的 sanity check。
- **更好的深鑽 UX。** 想要更多脈絡的使用者可以跳到來源段落或頁面。

對任何企業文件功能，成本效益幾乎是必贏的選擇。對消費端的一般知識功能，citations 常常不適用。

---

## PDF + Citations 標準 stack

把課程 54（PDF support）和課程 55（citations）配對，就是標準的 Claude 企業文件 stack：

1. 啟用 `citations.enabled: True` 並帶可讀 `title` 的 PDF content block。
2. 精準的擷取或 QA prompt。
3. 渲染答案並在行內放 citation 標記、提供 hover popover 的 UI。
4. 可選：對文件 bytes 做 prompt caching 以支援重複 query。

這是從「我們有一堆 PDF」到「我們有一個可上線、使用者信任的企業功能」的最短路徑。每一份文件 workflow 的 PRD 都應該明確引用這個配對。

---

## Common PM Mistakes

1. **對高代價功能把 citations 當可選項。** 它不是。受管制 workflow 裡的使用者沒有它不會採用。
2. **在 API 打開 citations 卻沒在 UI 顯示。** 付了成本、拿不到信任效益，還讓工程團隊困惑功能的意義。
3. **忘了 `title` 欄位。** 多文件回應變得曖昧，使用者無法分辨 citation 來自哪份文件。
4. **以為 citations 保證正確性。** Citation 證明來源文字存在，不證明 Claude 的改寫忠實。高代價答案仍需人工審查解讀錯誤。
5. **沒處理純文字 RAG chunks。** 若你的管線送的是文字 chunk，citations 仍然能用，但回傳的是字元位置不是頁碼，UI 必須依 source 類型分支。
6. **低估 UX 設計工作。** Citation 標記、hover popover、跳到來源、「無 citation」的 fallback 都需要明確設計。

---

> **Key Insight**
>
> Citations 是任何基於使用者在意的文件的 Claude 功能的最小可行信任機制。啟用便宜、跳過很貴：沒有它，企業和受管制功能很少能過信任門檻，使用者只好自己回去讀原文。把 citations 和 PDF support 配對，一個 request 就能拿到標準的企業文件 stack。

---

## CCA Exam Relevance

- **D4 (AI Safety & Alignment)**：Citations 是 grounded、可驗證輸出的標準機制。預期考信任與來源透明度的題目。
- **D2 (Tool Design & MCP Integration)**：要會 API 形狀——`title` 欄位、`citations.enabled` 旗標、citation metadata 結構（`cited_text`、`document_index`、`document_title`、頁碼或字元位置）。
- 情境題：「使用者需要驗證 Claude 的文件答案。」答案是在 document block 啟用 citations 並在 UI 顯示 `cited_text`。

---

## Flashcards

| Front | Back |
|-------|------|
| Citations 的研究助理類比是什麼？ | 沒 citations 時助理說「相信我」；有 citations 時每句話都有註腳指向某個來源條款，你可以抽檢。 |
| 什麼時候 citations 是強制的？ | 受管制或高代價 workflow：法律、醫療、金融、合規、企業知識、學術或研究工具。 |
| 什麼時候 citations 可選或不適用？ | 閒聊、創意寫作、一般知識 brainstorming、或對使用者口述內容做摘要。 |
| Citations UX 要設計什麼？ | 行內標記、hover popover 顯示 `cited_text` 與 `document_title`、跳到來源、以及無 citation 片段的 fallback。 |
| 最小可行的企業文件 stack 是什麼？ | PDF content block + 啟用 citations + 精準 prompt + 有 citation 標記的 UI +（可選）對重複 query 的 prompt caching。 |
| 為什麼 citations 啟用便宜、跳過很貴？ | 啟用只要少許 token 開銷與中等 UI 工作；跳過代表高代價功能過不了信任與合規門檻。 |
| Citations 保證 Claude 的答案正確嗎？ | 不。它證明 Claude 讀過某段來源原文，不證明 Claude 的解讀準確。具後果的答案仍需人工審查。 |
| Citations PRD 該規格什麼？ | 信任需求（誰要驗證）、標記與 popover 的 UX pattern、多文件處理、純文字 vs PDF source type、缺 citation 的 fallback。 |
