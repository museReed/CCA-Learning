# Citations — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D4 — AI Safety & Alignment (20%) — 主要；D2 — Tool Design & MCP Integration (18%) — 次要 |
| Task Statements | 4.2（grounded outputs）、2.2（content blocks）、5.4（信任與可驗證性） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 55 |

---

## One-Liner

Citations 把 Claude 基於文件的答案從不透明文字變成可驗證的軌跡——對每一個陳述，你都能拿到支撐它的原文、出自哪份文件、以及在文件裡的位置。

---

## Citations 解決的信任問題

當 Claude 對著你提供的文件回答問題時，使用者光看文字沒辦法分辨答案是來自你的文件還是模型的訓練資料。這個曖昧性對任何「來源很重要」的功能都是信任殺手：法律研究、金融分析、醫療資訊、合規 QA。

Citations 的修法是為 Claude 回應裡的每一個陳述建立一條明確、機器可讀的軌跡，指回支撐它的原文。模型不只回答——它把收據一起拿出來。

---

## 啟用 Citations

啟用 citations 需要在 `document` content block 上加兩件事：一個人類可讀的 `title` 和一個 `citations.enabled` 旗標。

```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": file_bytes,
    },
    "title": "earth.pdf",
    "citations": { "enabled": True }
}
```

兩個欄位很重要：

- **`title`**——文件的可讀名稱。這是使用者在 UI 上看到 citation 時顯示的名字；Claude 也用它在同一個 request 的多份文件之間做區分。
- **`citations.enabled`**——告訴 Claude 為每一個陳述追蹤來源的開關。

Document block 的其他部分和 PDF support 的 pattern 完全一樣。

---

## 開啟 Citations 後的回應結構

關閉 citations 時，Claude 的回應是一個簡單的 text block。開啟後，Claude 回傳一個更豐富的結構，文字片段附帶 citation metadata。每個 citation 包含：

- **`cited_text`**——文件裡支撐該陳述的原文，逐字元對應。這是模型指向的 ground truth。
- **`document_index`**——Claude 參考的是哪一份文件，單一 request 裡有多份文件時很有用。
- **`document_title`**——你指給文件的 title（和 document block 裡那個字串一樣）。
- **`start_page_number`**——被引用文字的起始位置。
- **`end_page_number`**——被引用文字的結束位置。

PDF 的 `start_page_number` / `end_page_number` 是頁碼。純文字來源則把這兩個欄位換成**字元位置**，精確指向文字裡的某個 span。

---

## 對純文字來源的 Citations

Citations 不是 PDF 獨享。對純文字文件開 citations 的方式是換 `source` block：

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": article_text,
    },
    "title": "earth_article",
    "citations": { "enabled": True }
}
```

和 PDF 情況的差別：

- `source.type` 是 `"text"` 而不是 `"base64"`。
- `source.media_type` 是 `"text/plain"`。
- `source.data` 放原始文章文字，不是 base64 bytes。
- 回傳的 citations 用**字元位置**（start_index / end_index）而不是頁碼。

這對 RAG 管線意義很大：當你的檢索步驟抓出一段純文字 chunk，你可以把它當成一份可引用的文件送進去，拿回精確的字元 span，用來做 hover-over UI 或 highlight 工具非常乾淨。

---

## 用 Citations 做 UI

Citations 的真正產品槓桿在 UI 層。典型 pattern：

1. Claude 的回應帶著 citation 註解的片段送回來。
2. UI 照常渲染答案文字，但每個被引用的 span 加上標記（一個小數字、反白背景、或內嵌 icon）。
3. Hover 或點擊標記會打開一個 popover，顯示 `cited_text`、`document_title`，並提供跳到某頁或某字元位置的動作。
4. 使用者可以就地驗證陳述，不用離開答案畫面。

這把 Claude 從「回答的黑盒」變成「會把工作過程攤開的研究助理」。需要信任輸出的使用者可以兩下點擊驗證；不在意的使用者可以忽略標記。

---

## 何時該用 Citations

課程點名四個 citations 值得花成本與複雜度的情境：

- **使用者需要驗證資訊的正確性。** 高代價答案——法律、醫療、金融——需要證據。
- **你處理的是權威文件。** 若文件是 source of truth（合約、法規、臨床指引），使用者應該能指向它。
- **來源透明度對產品至關重要。** 有些產品——企業搜尋、研究工具、知識庫——靠來源透明度活著。
- **使用者可能想探索特定事實周圍的脈絡。** Citations 是往下鑽的 UX 鉤子；使用者可以從答案跳到周圍段落再跳到整份文件。

---

## Common Mistakes

1. **忘了 `title` 欄位。** Citations 在回應裡用 title 當文件識別字。沒寫，使用者看到空白或通用標籤，無法區分文件。
2. **啟用 citations 卻沒顯示。** 旗標打開卻把答案渲染成純文字，token 成本照付、信任效益為零。
3. **以為純文字來源用頁碼。** 純文字的 citations 回傳字元位置，不是頁碼。你的 UI 必須依 source 類型分支。
4. **沒處理更豐富的回應結構。** 開 citations 的回應比單一 text block 複雜。Content-block handler 必須迭代並正確拉出 citation metadata。
5. **在同一個 request 裡混用有引用和沒引用的文件卻沒追蹤。** `document_index` 告訴你 citation 指向哪一份——要用它。
6. **以為 citations 等於正確性保證。** Citation 證明原文存在、Claude 讀過它——不證明 Claude 的解讀正確。Citations 是來源證據，不是準確度保證。

---

> **Key Insight**
>
> Citations 是把 Claude 的文件答案轉成可驗證陳述的依據層。API 表面很小——一個 `title` 欄位加一個 `citations.enabled` 旗標——但產品衝擊巨大：對每一個高代價文件 workflow（法律、醫療、金融、合規），citations 就是「能出貨」和「不能出貨」的差別。把 citations 和 PDF support 搭配起來，就是企業文件 stack 的標準組合。

---

## CCA Exam Relevance

- **D4 (AI Safety & Alignment)**：Grounded outputs 與可驗證回應是核心 safety 考量。Citations 是產生可驗證、有來源連結答案的標準機制。
- **D2 (Tool Design & MCP Integration)**：Citations 延伸 `document` content block。要知道 `title` 和 `citations.enabled` 欄位，以及 citation metadata 的形狀（`cited_text`、`document_index`、`document_title`、頁碼或字元位置）。
- 情境題：「使用者需要驗證 Claude 的答案來自某個特定來源。」答案是在 document block 上啟用 citations，並在 UI 上顯示 `cited_text` 和 `document_title`。

---

## Flashcards

| Front | Back |
|-------|------|
| 啟用 citations 要在 document block 加哪兩個欄位？ | 一個 `title` 欄位（可讀文件名）加 `"citations": {"enabled": True}`。 |
| Citation 物件裡有哪五項資訊？ | `cited_text`、`document_index`、`document_title`、`start_page_number`、`end_page_number`。 |
| PDF 和純文字來源的 citations 差在哪？ | PDF citations 回傳頁碼；純文字 citations 回傳字元位置。 |
| 純文字可引用文件用什麼 `source.type` 和 `media_type`？ | `source.type: "text"` 和 `media_type: "text/plain"`，`data` 放原始文章文字。 |
| 什麼時候該用 citations？ | 使用者需要驗證資訊、處理權威文件、來源透明度關鍵、或使用者可能想探索脈絡時。 |
| 為什麼啟用 citations 時 `title` 欄位是必要的？ | 它是每個 citation 回傳的文件識別字，也是使用者在 UI 看到的標籤；沒有它，多文件回應會曖昧。 |
| Citation 和正確性保證的差別？ | Citation 證明原文存在、Claude 讀過它；不證明 Claude 的解讀正確。 |
| Citations 的標準 UX pattern？ | 在被引用的 span 加行內標記，hover 顯示 `cited_text` 與 `document_title`，並提供跳到來源的動作。 |
| 為什麼 citations 對法律、醫療、金融產品至關重要？ | 這些領域的使用者必須先驗證來源才敢採取行動；citations 提供讓這些功能能出貨的可稽核軌跡。 |
