# Code Execution and the Files API — PM Perspective（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.4（server-side tools）、2.1（tool schema 設計） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 59 |

---

## One-Liner

Files API 和 Code Execution 合起來，能讓你的產品上線「把檔案丟給 Claude」型的功能——使用者上傳檔案、用自然語言提問、拿回含圖表的分析結果——而你的團隊不用自建資料管線、沙盒或圖表渲染器。

---

## PM 為什麼要在意

在這個功能之前，上線「上傳 CSV 拿到分析」代表要擁有整條管線：檔案儲存、沙盒 runtime、繪圖函式庫、結果 UI，以及任何一環壞掉時的值班工程師。Code Execution 把這些壓縮成：**宣告一個 server-side tool、把 Files API 接起來做上傳／下載**。分析工作、圖表生成、迭代——全由 Claude 在 Anthropic 操作的沙盒裡搞定。

這是「把計算委派給 Claude」的模式，可以解鎖原本要幾季才能做出來的產品功能：資料分析、圖像處理、文件轉換、數學建模。你的 roadmap 只要有任何「上傳 X 拿回 Y」類型的功能，這堂課就是最短的上線路徑。

---

## Mental Model：可信任承包商的封閉工坊

把 Code Execution 想像成僱用一個在封閉工坊裡工作的承包商：

| 承包商比喻 | API 對應 |
|------------|----------|
| 你在工坊門口交給承包商原料 | 用 Files API 上傳檔案，並用 `container_upload` 送進沙盒 |
| 工坊沒有電話、沒有網路——不受外界干擾 | Docker 容器沒有網路——安全、隔離 |
| 承包商可以在裡面建造、迭代、嘗試不同做法 | Claude 可以在單次回應中多次執行 Python |
| 你在門口領取完成的產品 | 你透過 Files API 下載生成檔案 |
| 你不用提供工具——承包商自帶 | Code Execution 是 server-side tool，無需 client 實作 |

封閉工坊不是限制——它就是**你能放心把真正 runtime 交給 Claude 的理由**。

---

## Product Use Cases

### 課程點出的高價值模式

| 使用情境 | 使用者做什麼 | Claude 做什麼 |
|----------|--------------|----------------|
| 資料分析（流失、銷售、實驗） | 上傳 CSV、用自然語言提問 | 清理、分析、繪圖、總結 |
| 圖像處理 | 上傳圖片、描述要做的轉換 | 在容器中跑圖像庫，回傳處理後的圖 |
| 文件解析與轉換 | 上傳 PDF、要求格式或遮蔽 | 擷取、轉換、重新輸出文件 |
| 數學建模 | 描述問題、上傳參數 | 建立並執行模型，回傳圖和數字 |
| 自訂報表生成 | 上傳原始資料、描述版型 | 生成格式化的 HTML／PDF 輸出 |

### 不適用的情境

| 情境 | 為什麼不行 |
|------|------------|
| 需要即時外部 API 的功能 | 沙盒沒有網路 |
| 需要跨 session 持久狀態的功能 | 容器是 ephemeral——狀態要靠 Files API |
| 試算表就能算的微小運算 | 額外成本不划算；Claude 原生推理就夠便宜 |
| 高安全性資料不能離開你的 infra | 沙盒是 Anthropic hosted——要先跑合規審查 |

---

## PM Decision Framework

為「Claude 做計算」的功能 scope 時：

| 問題 | 為什麼重要 |
|------|------------|
| 功能需要處理、繪圖、解析或轉換資料嗎？ | 答是就可能適合 code execution |
| 輸入是檔案（CSV、PDF、圖片）嗎？ | 答是就用 Files API 上傳 |
| 輸出包含生成的 artifact（圖表、報表）嗎？ | 答是就要透過 `code_execution_output` block 接下載路徑 |
| 功能需要對外網路嗎？ | 答是就不適合——沙盒沒網路 |
| 計算工作量有限（秒到分鐘）嗎？ | 迭代分析會如此；UX 要設計 streaming 或進度指示器 |
| 檔案離開 infra 有合規顧慮嗎？ | 上線前要審查 |

前三題是、後三題答案可接受，就是好下注。

---

## UX 含義

Code execution 改變了「簡單功能」能做到的事。單一 prompt 可以產出：

- 含多個圖表輸出的分析。
- 多步驟推理（讀入 → 檢視 → 清理 → 繪圖 → 總結），由 Claude 旁白。
- 不需額外使用者操作的迭代精修。

對使用者來說，這像隨時有一個資深資料分析師在線。對產品來說，你可以承諾以前需要 services 團隊或複雜 UI 才能交付的結果——透過一個文字框加一個檔案上傳就能做到。

---

## Common PM Mistakes

1. **承諾即時資料分析** — 沙盒沒網路，「取得最新股價並畫圖」開箱即用不可行。要先在自己的 code 抓資料，上傳結果，再呼叫 code execution。
2. **改用自建管線** — 團隊常低估 code execution 的能力，建一套自家沙盒——結果更慢、更不穩、更難維護。
3. **忘記把生成 artifact 露出在 UI** — 如果 UI 從不顯示 Claude 產出的檔案，使用者只會看到文字說明，感覺功能沒完成。要把 `code_execution_output` 檔案渲染出來。
4. **低估迭代** — Claude 可能在單次回應跑 code 三到五次。UX 和 log 要接得住，不能假設只執行一次。
5. **跳過合規審查** — 只要檔案離開你的 infra，法務和安全團隊就要介入。企業客戶上線前這關不能省。
6. **沒有同時規劃 Files API** — 沒 Files API 的 code execution 像沒有出貨門的工坊。要一起規劃。

---

> **Key Insight**
>
> Code Execution + Files API 是**產品捷徑**：把「我們要建一條沙盒運算管線」變成「我們要宣告一個 tool、接好檔案上下傳」。Roadmap 上任何「使用者上傳 X、我們分析並回傳 Y」的項目，這組合能把幾個月的工程壓成一個 sprint。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）** — 要知道區別：server-side tool（如 code execution）不需 client 實作，client-side tool 則要。考題常問「什麼時候你要自己實作 tool，什麼時候是 Claude 在 server 端跑」。
- 記住沙盒性質：隔離 Docker 容器、沒有網路、Python。
- 記住 Files API 是資料進（`container_upload`）、出（`download_file(file_id)`）的管道。
- 題目若出現「把某個運算任務委派給 Claude」的情境，正確答案通常是 Code Execution + Files API 模式。

---

## Flashcards

| Front | Back |
|-------|------|
| Code Execution + Files API 解鎖哪類產品功能？ | 使用者上傳檔案、用自然語言請求分析／轉換／報表，而你的團隊不用自建沙盒或管線。 |
| Files API 為產品做什麼？ | 提供「上傳一次、用 ID 引用」的檔案模式，同時作為 Code Execution 沙盒進／出的橋樑。 |
| Code Execution 是 server-side 還是 client-side tool？ | Server-side——無需 client 實作；Claude 替你在隔離容器跑 Python。 |
| 為什麼沙盒沒有網路？ | 那是隔離／安全特性——容器不能打對外 API，執行環境因此安全。 |
| 說一個這個模式不適合的功能。 | 需要即時對外 API 的東西（沙盒沒網路），或需要跨 session 持久狀態的東西。 |
| 哪個 mental model 能很好地描述這個模式？ | 可信任承包商的封閉、離線工坊——你在門口交原料，他在裡面工作，你在門口領產品。 |
| 為什麼 PM 不該改用自建沙盒？ | 因為 server-side tool 把幾個月的工作壓成一次 tool 宣告加 Files API 接線，團隊也省下維護自家 runtime 的成本。 |
| 哪種 block 把生成檔案交還給你？ | 帶 file ID 的 `code_execution_output` block，透過 Files API 取回。 |
