# Code Execution and the Files API — Engineering Deep Dive（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.4（server-side tools）、2.1（tool schema 設計）、1.2（multi-turn tool loop） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 59 |

---

## One-Liner

Files API 讓你把檔案上傳一次、之後用 ID 引用；Code Execution 是一個 server-side Python 沙盒（隔離 Docker 容器、沒有網路），Claude 可以直接驅動——兩者組合起來，你就能把真正的運算工作交給 Claude，而不用自己架執行環境。

---

## Files API — 上傳一次，多次引用

平常你把檔案（圖片、PDF）以 base64 嵌在 message 裡。Files API 是另一條路：單獨上傳檔案，拿到一份 file metadata object 和一個獨特的 **file ID**，之後的 message 就用這個 ID 引用。

流程：

1. 透過專用 API 呼叫上傳檔案（圖片、PDF、文字、CSV 等）。
2. 拿到一份 file metadata object，內含 **file ID**。
3. 之後的 message 用 file ID 引用，不再嵌入原始 bytes。

為什麼重要：

- 不用每次 request 都重送檔案——一次上傳，多次引用。
- 大檔案變得可以便宜重用——不用在每個 request 塞 base64。
- 它是把資料**送進／取出** Code Execution 沙盒的主要管道，因為沙盒沒有網路。

---

## Code Execution Tool — Server-Side Python 沙盒

Code Execution 是一個 **server-side tool**。不像一般 client-side tool，你不用自己實作——只要在 request 裡宣告預設的 tool schema，Claude 就可以在隔離環境中執行 Python。

執行環境的性質相當刻意：

| 性質 | 細節 |
|------|------|
| **Runtime** | 隔離 Docker 容器中的 Python。 |
| **網路存取** | **沒有**。容器不能打對外 API。 |
| **Iteration** | Claude 可以在單次對話中多次執行 code，隨分析進展迭代。 |
| **整合** | 結果被捕捉、由 Claude 解讀，產出最終回應。 |
| **需要實作** | **Client 端不用**——這是 Anthropic 提供的 server-side tool。 |

隔離是特性，不是限制：它讓你能安全地讓 Claude 跑 code，不用暴露你的 infra、金鑰或網路。

---

## 結合 Files API + Code Execution

因為 Docker 容器**沒有網路**，Files API 自然成為橋樑：它是把資料**送進**、把生成的 artifact **取出**的主要管道。

典型 workflow：

1. 用 Files API 上傳資料檔（例如 CSV）。
2. 在 message 裡放一個 `container_upload` block 帶 file ID，讓沙盒收到檔案。
3. 要 Claude 分析資料。
4. Claude 在容器裡寫 Python 並執行來處理檔案。
5. Claude 可以生成輸出（圖表、報告）並透過 Files API 提供下載。

這是乾淨的委派模式：你控制輸入輸出，Claude 處理 code。

---

## 實務範例：流失分析

課程示範一份 streaming service 資料集（`streaming.csv`），包含使用者資訊——訂閱方案、觀看習慣、流失標籤。

先用 helper function 上傳：

```python
file_metadata = upload('streaming.csv')
```

然後建一則 message，把文字指令和一個 `container_upload` block 配在一起引用上傳的檔案，並啟用 code execution tool：

```python
messages = []
add_user_message(
    messages,
    [
        {
            "type": "text",
            "text": """Run a detailed analysis to determine major drivers of churn.
            Your final output should include at least one detailed plot summarizing your findings."""
        },
        {"type": "container_upload", "file_id": file_metadata.id},
    ],
)

chat(
    messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)
```

關鍵：

- `container_upload` block 是把上傳檔案注入沙盒的方式。
- `tools` list 只有一項，`type: "code_execution_20250522"`——預設 server-side tool schema，你不用實作。
- Claude 收到指令和檔案引用後，就能跑 Python 分析。

---

## 回應結構

Claude 使用 code execution 時，response 會含多種 block 型態交錯出現：

| Block 類型 | 內容 |
|-----------|------|
| **Text blocks** | Claude 的分析、推理、自然語言說明。 |
| **Server tool use blocks** | Claude 決定要跑的實際 Python code。 |
| **Code execution tool result blocks** | 跑 code 的輸出（stdout、錯誤、檔案 handle）。 |

Claude 可以在單次回應中**多次**執行 code，逐步建立分析（讀入 → 檢視 → 清理 → 繪圖 → 總結）。每個執行 cycle 以一個 `server tool use` block 接一個 `code execution tool result` block 呈現。

---

## 下載生成的檔案

最強大的特性之一是 Claude 可以生成檔案（圖表、報告、轉換後的 CSV）並讓你下載。當 Claude 在容器裡建出一張視覺化圖，它會儲存在容器中，你可以透過 Files API 取回。

找 response 裡 `type: "code_execution_output"` 的 block——裡面有生成內容的 file ID。用 Files API 下載：

```python
download_file("file_id_from_response")
```

這完成了整個來回：CSV 進（透過 Files API），圖表出（透過 Files API），中間 Claude 做完所有 pandas／matplotlib 的工作。

---

## 不只資料分析

雖然流失分析是標準例子，這組合還能做很多其他委派模式：

- **圖片處理與操作** — 縮放、格式轉換、特徵擷取。
- **文件解析與轉換** — PDF 擷取、格式轉換、遮蔽處理。
- **數學運算與建模** — 模擬、優化、統計測試。
- **報表生成** — 從原始資料生成 HTML 或 PDF 輸出。

底層模式相同：Files API 控制*資料邊界*，Code Execution 處理*運算*，Claude 用自然語言協調兩者。

---

## Common Mistakes

1. **忘記沙盒沒有網路** — 寫出 `requests.get(...)` 的 code 一定失敗；資料必須透過 Files API 進去。
2. **可以用 file ID 卻把大檔 inline** — 每個 request 都 base64 嵌入大 CSV，浪費 token 和成本；上傳一次、用 ID 引用。
3. **以為必須自己實作 code execution tool** — 它是 server-side。你只宣告 schema，Anthropic 跑 Python。
4. **漏掉生成的輸出** — 沒掃 response 找 `code_execution_output` block，就看不到 Claude 產出的圖表和報告。
5. **以為沙盒會跨 session 保留** — 容器是 ephemeral；Files API 的 file ID 才是耐久的 handle，不是容器狀態。
6. **沒準備迭代** — Claude 可以在單次回應中多次跑 code；handler 只期待一個 execution block 會漏掉後面的資料。

---

> **Key Insight**
>
> Code Execution 是**完全不用 client 實作的 server-side tool**——你宣告 schema、Claude 在隔離容器跑 Python、你讀結果 block。Files API 是補上容器沒網路這個缺口的資料邊界。兩者一起讓你把整條運算 workflow 委派給 Claude：資料上傳進去，拿回分析和 artifact，完全不用自己架執行 infra。

---

## CCA Exam Relevance

- **D2（Tool Design）** — Code Execution 是 **server-side tool** 的典型範例。要知道你不用實作；只要在 `tools` list 裡宣告 `{"type": "code_execution_20250522", "name": "code_execution"}`，Claude 就會替你跑 Python。
- **D1（Agentic Architecture）** — 多次執行 code（Claude 在單次回應多次執行）是一個完全跑在 server side 的 agentic loop。
- 記住沙盒性質：隔離 Docker 容器、沒有網路、Python runtime、ephemeral。
- 記住 Files API 是進／出橋樑：檔案靠 `container_upload` 進去，artifact 靠 `code_execution_output` → `download_file(file_id)` 出來。

---

## Flashcards

| Front | Back |
|-------|------|
| Files API 讓你做什麼？ | 上傳檔案（圖片、PDF、CSV 等）一次、拿到 file ID，之後的 message 用該 ID 引用，不用再嵌入原始資料。 |
| Code Execution 是 client-side 還 server-side tool？ | Server-side——你不用實作；你宣告預設 schema，Claude 就在隔離容器中跑 Python。 |
| Code Execution 使用什麼 runtime 和環境？ | 隔離 Docker 容器中的 Python，**沒有網路**。 |
| 為什麼用 Code Execution 時 Files API 不可或缺？ | 沙盒沒網路，唯一把資料送進去、把 artifact 取出來的方式就是透過 Files API 上傳／下載。 |
| 哪個 block 型態把上傳的檔案注入沙盒？ | `container_upload`，帶著 Files API 上傳回來的 `file_id`。 |
| 要啟用 code execution，tool schema 要填什麼？ | 在 `tools` list 裡放 `{"type": "code_execution_20250522", "name": "code_execution"}`。 |
| Claude 可以在單次回應中多次執行 code 嗎？ | 可以——迭代進行，把 text、server tool use block、code execution result block 交錯。 |
| Code execution 回應裡會出現哪三種 block？ | Text block（Claude 的解釋）、server tool use block（Python code）、code execution tool result block（輸出）。 |
| 怎麼取回 Claude 在容器中生成的檔案？ | 找 `code_execution_output` block 裡的 file ID，然後用 Files API 呼叫 `download_file(file_id)`。 |
| 說出三個 Code Execution + Files API 的非資料分析用途。 | 圖片處理、文件解析與轉換、數學運算與建模、報表生成。 |
