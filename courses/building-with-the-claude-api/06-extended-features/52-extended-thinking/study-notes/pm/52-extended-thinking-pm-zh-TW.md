# Extended Thinking — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 1.1（推理深度）、1.2（agentic loop）、5.2（latency/cost 權衡） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 52 |

---

## One-Liner

Extended thinking 是當 prompt engineering 在難推理任務上走到盡頭時，產品經理可以拉的那根調節桿——多花錢、多等幾秒，換一個更聰明的答案。

---

## Mental Model：西洋棋選手與時鐘

想像一位西洋棋大師在兩種不同賽制下下棋。

- **Bullet chess（急速對弈）**：時鐘只有三十秒。他憑直覺飛快下，大多能贏，但有些該贏的會輸。
- **Classical chess（正式對弈）**：時鐘有數小時。他靠在椅背上，在腦中推演各種變化、評估風險，下出明顯更強的棋。

標準 Claude 就是 bullet chess——快、流暢、通常正確。Extended thinking 是 classical chess——你買的是模型在草稿紙上思考的時間。棋是同一盤棋，差別在選手有多少時間想。

沒有人會為了點一份咖啡用 classical chess。同樣的，也不應該為了 prompt engineering 就能解決的問題付 extended thinking 的錢。

---

## PM 為什麼該在意

Extended thinking 是少數能把**成本與延遲**直接換**準確度**的產品槓桿。這正是 PM 每天在處理的取捨：

- 使用者抱怨 Claude 對某個難問題五次裡錯一次。
- 工程團隊已經調了兩週 prompt，eval 分數停滯。
- CFO 在問為什麼 AI 功能有延遲尖峰。
- 沒人知道該拉哪根桿。

Extended thinking 給你一個有名字、可量測的選項帶到那場對話裡——測試成本很低（翻旗標重跑 eval），限制明確到可以寫進 PRD。

---

## Product Use Cases

### Extended thinking 該打開的時機

| 使用者需求 | 為什麼 thinking 有幫助 |
|-----------|---------------------|
| 難推理（數學、邏輯、多步規劃） | 模型真的需要思考 token 來走完每一步 |
| 高代價的答案，準確度比延遲更重要 | 使用者願意多等幾秒換一個正確答案 |
| 多約束的複雜文件分析 | 思考空間讓模型能協調互相衝突的條件 |
| 需要「想清楚」而不是「查一下」的研究型問題 | 任務形狀本身就是推導答案，不是檢索 |

### 不該打開的時機

| 使用者需求 | 更好的選擇 |
|-----------|-----------|
| 簡單改寫、摘要、翻譯 | Base model；thinking 加成本但不加準確度 |
| 需要快速回應、延遲即 UX 的聊天 | Extended thinking 會明顯拖慢 |
| 要抓即時資料 | 用 tools 而不是 thinking——再怎麼深思熟慮也變不出訓練資料裡沒有的事實 |
| 短結構化擷取 | 這是 prompt/格式的問題，不是推理問題 |

---

## PM 決策框架

當團隊有人說「我們來打開 extended thinking」時，要問：

| 問題 | 若答 Yes | 意涵 |
|------|---------|------|
| 我們對著 eval set 優化過 prompt 了嗎？ | No | 先做這件事。Thinking 修不了壞掉的 prompt。 |
| 準確度差距明顯是推理深度問題嗎？ | No | 問題可能在 tools、RAG 或結構——不是 thinking。 |
| 使用者能容忍這個互動多等幾秒嗎？ | No | Thinking 會傷 UX。考慮非同步或進度提示。 |
| 每次呼叫的成本增加在當前量級下可接受嗎？ | No | Thinking tokens 規模化後是真金白銀，先算清楚再決定。 |
| 這個 flow 依賴 assistant 預填或自訂 temperature 嗎？ | Yes | 與 thinking 不相容，必須重設計 prompt 策略。 |

以上全綠就打開 thinking 跑 eval，看差距是否收斂。若收斂就出貨，並在 PRD 裡寫下成本與延遲預算。

---

## Cost、Latency、UX 權衡

Extended thinking 不是無聲升級。它改變三件使用者會感覺到的事：

- **等待時間上升。** 模型真的會花較長的實際時間在思考。互動 UI 需要能容忍多幾秒的 loading state。
- **每次呼叫成本上升。** Thinking tokens 要計費。每天 10 萬次呼叫、budget 1024 token，月帳單上看得到。
- **回應處理變複雜。** 工程端要迭代 content blocks，還要決定要不要把推理攤給使用者看。這是設計決策，不只是程式決策。

PM 的衛生習慣：任何啟用 thinking 的功能，PRD 裡必含：

1. 以 eval 為基礎的理由（開啟前後的準確度）。
2. 每次呼叫成本估算與月度預測。
3. Loading state 與可選的「顯示推理」toggle 的 UX 規格。
4. 當 thinking 與其他依賴功能不相容時的 fallback 路徑。

---

## Safety 故事：Signatures 與 Redacted Blocks

Extended thinking 帶兩個 safety 特性。PM 應該知道它們存在，因為它們同時影響信任訊息和技術設計。

- **Signatures**——每個 thinking block 都有加密簽章。如果開發者（或攻擊者）試圖在對話中段改寫推理、把 Claude 引到不安全的地方，簽章驗證會失敗、history 會被拒絕。這是你可以對客戶說「我們怎麼知道推理沒被竄改」時指得出來的保證。
- **Redacted blocks**——有時 Claude 自家的 safety 系統會對推理亮紅燈，並以加密形式回傳。你的 app 讀不出 redacted 內容，但必須原樣傳回去以保留上下文。產品意涵：你的「顯示推理」UI 偶爾會在某一輪沒東西可顯示，必須準備一個優雅的 fallback，而不是丟錯誤畫面。

---

## Common PM Mistakes

1. **Prompt 還沒優化就先開 thinking。** 結果就是把推理槓桿疊在一個壞掉的 prompt 上，準確度幾乎不動。
2. **把 thinking 當成「Claude 免費變聰明」。** 它是成本與延遲的權衡。假裝不是，就會在上線時嚇到財務與 UX。
3. **把原始推理文字直接渲染給使用者。** 推理軌跡又長又偏內部，使用者預設不會想看一整牆的思考過程。
4. **忽略功能不相容性。** 若你現在的 prompt 策略用了 assistant 預填或自訂 temperature，打開 thinking 會整個壞掉。
5. **忘記 thinking budget 必須嚴格小於 max_tokens。** API 會強制這條限制。第一次在 production 出包，就是一次本來可以在 review 時攔截的故障。
6. **沒為 redacted 情境更新「顯示推理」UI。** 使用者會看到空白面板，以為功能壞了。

---

> **Key Insight**
>
> Extended thinking 是 Claude API 第一個乾淨、可被產品經理管理的權衡——一邊是準確度，另一邊是成本加延遲。PM 的工作是知道什麼時候拉它：在 prompt 優化之後、有 eval 證據支持、並且只用在那些使用者寧願等久一點也要正確答案的難推理任務上。

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**：把 extended thinking 認成 agentic loop 內推理深度的標準槓桿，並分辨它 vs. prompt / tools 各自的適用場景。
- **D5 (Enterprise Deployment)**：成本與延遲的權衡、以 eval 驅動的採用決策、以及 `thinking_budget` / `max_tokens` 的限制都是 production 級的考點。
- 可能的情境題：「Prompt engineering 在一個難推理任務上碰到天花板——下一步該怎麼做？」預期答案是 extended thinking，且要 eval-driven。

---

## Flashcards

| Front | Back |
|-------|------|
| Extended thinking 的西洋棋類比是什麼？ | 標準 Claude 是 bullet chess——快、通常正確。Extended thinking 是 classical chess——買模型在草稿紙上思考的時間，在難題上給更強的答案。 |
| 什麼時候 extended thinking 是錯的工具？ | 快速簡單任務（改寫、翻譯、閒聊）或真正問題是缺資料（該用 tools/RAG）而不是推理深度時。 |
| PM 在一個功能上打開 thinking 前必須先完成什麼？ | 針對 eval set 的 prompt 優化，且證據顯示剩下的差距是 prompt 單獨解不掉的推理深度問題。 |
| Extended thinking 對使用者體驗改變哪三件事？ | 等待時間、每次呼叫成本、以及回應複雜度（推理軌跡出現在 content blocks）。 |
| 啟用 thinking 的功能 PRD 該包含什麼？ | 以 eval 為基礎的準確度理由、成本預測、UX loading states、以及相容性 fallback。 |
| Thinking signature 保證什麼？ | 推理軌跡在對話 turn 之間沒被竄改，防止開發者偽造 chain-of-thought 把模型引到不安全的地方。 |
| 什麼是 redacted thinking block？app 該怎麼處理？ | 因為內部 safety 系統標記而被加密的 thinking block。App 讀不到內容但必須原樣傳回以保留上下文。 |
| 為什麼 extended thinking 與某些功能不相容？ | 出於模型設計原因——特別是 pre-filled assistant 訊息與自訂 temperature 會和 thinking 機制衝突，啟用 thinking 時那部分 prompt 策略必須重做。 |
