# Environment Inspection — Engineering 深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架構)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 選型) |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 82 |

---

## 一句話總結

Claude 預設是「盲」的——有效的 agent 必須提供讓它 **在行動前觀察環境目前狀態** 的 tools,而且每次變更後要重新觀察,否則 Claude 會根據過時或想像出來的世界做決策。

---

## 為什麼 Environment Inspection 重要

Agent 在自己看不見的 state 上做決策。LLM 沒長眼睛看不到你的檔案系統、沒 hook 進資料庫、也不知道按了按鈕後到底發生什麼事。沒有 inspection tool,Claude 就是在猜現實。

Computer Use 是教科書等級的例子:**每次** Claude 執行動作(打字、點按鈕),Anthropic runtime 立刻回傳一張 screenshot。那個 screenshot 不是裝飾——它是 Claude 把下一步「接地」到螢幕實際狀態的方法。點一下可能開了 modal、可能換頁、可能出錯、也可能什麼都沒發生。沒有 screenshot,Claude 根本沒 signal。

這個 pattern 可以推廣:如果你的 agent 對任何 state 做動作,它就必須有能力讀到那個 state。

---

## 鐵律:Read Before Write

Claude 變更任何東西之前,必須先讀目前狀態。聽起來很明顯,但一直有人違反。

**範例:在 Python 檔案加一條 route**

```python
# BAD — Claude 憑空猜結構
edit_file("app.py", replace="last_line", with="@app.route('/new')...")

# GOOD — Claude 先讀再編輯
current = read_file("app.py")
# Claude 推理:「這是 FastAPI,routes 在 20-45 行,imports 在最上面」
edit_file("app.py", old_string="...existing_route_block...", new_string="...with new route...")
```

Claude Code 把這條規則寫進設計裡:`Edit` tool 拒絕對「本次 session 沒 `Read` 過的檔案」操作。這不是禮貌——這是防止 Claude 用可能錯誤的假設去改檔案。

---

## System Prompt Pattern for Inspection

你透過明確的 system prompt 指令引導 Claude 去做 inspection。以 video generation agent 為例:

```python
system_prompt = """
你是 video production agent。把任務視為完成前,你 **必須** 驗證你的輸出:

1. 用 `bash` 執行 whisper.cpp 對生成的影片產出帶時間戳的 caption 檔。確認對白出現在預期時間點。
2. 用 `ffmpeg` 從影片每秒取一張截圖。逐張檢查視覺元素是否符合 spec。
3. 把截圖和 caption 對比原始需求。
4. 任何元素缺漏或錯誤,回去重生成該段再重新驗證。

未完成這些驗證步驟,絕對不能宣告任務完成。
"""
```

System prompt 把「驗證輸出」從含糊建議變成強制的 tool-calling 協議。沒有這個,Claude 會依照它 **預期** tool 產出什麼就宣告成功。

---

## Inspection 的四大好處

| 好處 | 帶來什麼 |
|------|---------|
| **Progress tracking** | Claude 能衡量距離目標還有多遠,而不只是執行步驟 |
| **Error handling** | 非預期輸出當回合就能偵測並修正 |
| **Quality assurance** | Agent 在宣告「完成」前自我驗證,抓出靜默失敗 |
| **Adaptive behavior** | Claude 根據觀察到的結果調整策略,不只是照原計畫走 |

沒有 inspection = 盲眼執行器。有 inspection = feedback 驅動的 agent。

---

## 實作 Checklist

設計任何 agent tool 時,問:**「Claude 怎麼知道這個動作成功了?」**

| 動作類型 | Inspection Tool |
|----------|-----------------|
| 檔案寫入/編輯 | 寫入後 `read_file`;diff 對照預期輸出 |
| UI 點擊 / Computer Use | 每次動作自動 screenshot |
| HTTP API 呼叫 | 回傳完整 response body + status code,不要只回 "ok" |
| 資料庫寫入 | Insert/update 後 read-back query |
| Shell 指令 | 回傳 stdout + stderr + exit code |
| 影音生成 | Metadata 抽取 + keyframe screenshot + 轉文字 |

Rule of thumb:**每個會變更狀態的 tool 都該搭配一個觀察 tool**,而且 system prompt 要明確叫 agent 兩個都用。

---

## Code Pattern:Before and After Inspection

```python
system = """
你是 code refactoring agent。每次改檔案都要:

1. 呼叫 `read_file` 載入目前內容。
2. 分析結構,找出該改什麼。
3. 呼叫 `edit_file`,提供精確的 old_string / new_string。
4. **再次** 呼叫 `read_file` 驗證改動套用正確。
5. 呼叫 `run_tests` 確認沒弄壞東西。

步驟 4 或 5 失敗就不要繼續下一個改動——先把 regression 修好。
"""

tools = [read_file, edit_file, run_tests]
```

現在這個 agent 是 **grounded** 的——每個決策都基於新鮮的觀察,不是基於三回合前對檔案內容的假設。

---

## 常見錯誤

1. **Write-only tool** — 只給 `edit_file` 不給 `read_file`。Claude 沒辦法對看不到的檔案做推理。
2. **Tool 回應過於精簡** — API call 只回 `"ok"` 不回 response body。Claude 沒資料可以用。
3. **依賴計畫而非觀察** — Claude 把自己之前的計畫當成 ground truth。System prompt 必須強迫重新觀察。
4. **變更後沒 inspection** — Tool 沒丟 exception 就當成功,用過時 state 繼續跑。
5. **Computer Use 關掉 screenshot** — 為了省 cost 關掉自動截圖,等於讓 Computer Use 蒙眼操作。

> **Key Insight**
>
> Environment inspection 是把 Claude 從盲眼執行器變成 grounded agent 的關鍵。每個變更 tool 都要搭配觀察 tool,system prompt 要讓 inspection 變成強制而非可選。「Read before write, verify after write」是 agentic 系統裡單一槓桿最高的可靠度 pattern。

---

## CCA 考試關聯

- **D1 (Agentic Coding & Architecture)**:會考「為什麼 Claude Code 改檔案前要先讀」、「為什麼 Computer Use 自動回 screenshot」。答案是 grounding。
- **D5 (Enterprise Deployment)**:Production agent 的可靠度和 error handling 靠 inspection 內建在 tool set 裡,而不是事後補。
- 考題關鍵字:「grounding」「verify」「observe」「blindly execute」都指向 environment inspection。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 為什麼 Computer Use 每次動作後都回 screenshot? | Claude 對環境是盲的——screenshot 是它觀察自己動作結果、把下一步接地的方法。 |
| Agent 變更 state 時該遵守什麼規則? | Read before write——變更前先檢視目前狀態,變更後再檢視一次驗證。 |
| 為什麼 Claude Code 要求 `Edit` 前先 `Read`? | 防止 Claude 根據假設改檔案——它必須先觀察真實內容。 |
| 舉三個支援 environment inspection 的 tool response pattern。 | 回傳完整 HTTP response + status、回傳 stdout + stderr + exit code、DB 變更後 read-back query(任三)。 |
| 怎麼在 agent 裡強制 environment inspection? | 用 system prompt 指令明確要求每次變更動作前後都要呼叫特定 inspection tool。 |
| Environment inspection 的四大好處是什麼? | Progress tracking、error handling、quality assurance、adaptive behavior。 |
| 設計 agent tool 時該問的唯一設計問題是什麼? | 「Claude 怎麼知道這個動作成功了?」 |
| 為什麼 API tool 只回 `"ok"` 是爛設計? | Claude 沒資料可以用——agent 沒辦法驗證或調整,沒有實際 response 內容。 |
