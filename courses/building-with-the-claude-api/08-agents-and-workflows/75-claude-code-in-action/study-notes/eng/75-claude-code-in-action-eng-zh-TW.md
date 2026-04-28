# Claude Code in Action — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 設定與指令）、3.3（CLAUDE.md memory）、1.2（agentic workflow patterns） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 75 |

---

## 一句話總結

Claude Code 最有效的 workflow 是「context → plan → implement」：先載入相關檔案，請 Claude 擬計畫（明確不要寫 code），再請它實作；`/init` 則會產生 `CLAUDE.md` memory file，跨 session 保留專案 context。

---

## `/init` 指令與 CLAUDE.md

開始新專案時，先跑 `/init`。這會觸發 Claude Code：

1. 掃描整個 codebase
2. 推斷專案結構、相依性、coding style 與架構
3. 把總結寫入一個特殊檔案 `CLAUDE.md`

`CLAUDE.md` 在該專案之後的每一場對話中自動帶入為 context，是讓 agent 跨 session「記得」你專案的持續 memory。

### CLAUDE.md 的三種 scope

| Scope | 用途 | 會 commit 進 git 嗎？ |
|-------|------|--------------------|
| **Project** | 整個專案團隊共享 | 會 |
| **Local** | 你個人的筆記 | 不會 |
| **User** | 套用到你所有專案 | 不會（user-global） |

跑 `/init` 時可以加上特別指示，告訴 Claude 要聚焦哪些區域。產生的檔案通常包含 build 指令、coding guideline、專案特定的 pattern。

### `#` 快捷鍵新增筆記

你不用打開檔案就能附加筆記到任一 `CLAUDE.md`。輸入：

```
# 永遠使用描述性的變數名稱
```

…Claude Code 會問你要加到哪個 scope（project / local / user），然後自動附加。

---

## 標準 Workflow：Context → Plan → Implement

Lesson 的核心主張：Claude Code 只有在你提供足夠 context 與結構時，才能成為 effort multiplier。三步建議流程：

### Step 1 —— 餵 context 給 Claude

在請它寫任何 code 之前，先找出能展示你 pattern 的現有檔案，請 Claude 讀。這樣 agent 就有你 coding style 和現有功能的範例可參考。

```
> 讀 math.py 和 document.py 這兩個檔案
```

### Step 2 —— 請 Claude 擬計畫（明確不要寫 code）

請 Claude 思考問題並寫出計畫。**明確告訴它先不要寫 code** —— 只給方法與步驟。

```
> 請計畫實作 document_path_to_markdown tool：
1. 建立一個 function：
   - 接受檔案路徑參數
   - 驗證檔案存在
   - 從副檔名判斷檔案類型
   - 讀取檔案 binary 資料
   - 利用既有的 binary_document_to_markdown function
   - 回傳 markdown 字串
2. 加上適當的 documentation
3. 向 MCP server 註冊這個 tool
4. 加入 tests
```

### Step 3 —— 請 Claude 實作計畫

等計畫談好了，才請它實作：

```
> 實作上面的計畫
```

Claude 會根據前面累積的 context 與 plan 寫 code、更新相關檔案、加 test、跑測試套件驗證。

這個三步 pattern 呼應了考試會測驗的 agent 設計原則「think then act」—— 它不只是 Claude Code 的 idiom，是一般 agent 的 best practice。

---

## 測試驅動開發 Workflow

Lesson 介紹的 TDD 變體能產出更穩健的 code：

1. **餵 context** —— 同上
2. **請 Claude 列出 test cases** —— 這個功能要哪些 test 才算驗證完成？
3. **請 Claude 實作 test** —— 選最相關的那些請它寫出來
4. **請 Claude 寫出能通過 test 的 code** —— 它會反覆迭代直到全綠

這招有效的原因：test 給了 Claude 一個具體的成功標準。不是「寫一個做 X 的 function」，而是有可驗證的目標（全綠的 test），agent 會持續迭代直到達成。

---

## 附加指令列表

除了 workflow 之外，考試還要記這些指令：

| 指令 | 功能 |
|------|------|
| `/init` | 掃描 codebase 並產生 `CLAUDE.md` |
| `/clear` | 清空對話歷史並重置 context |
| `#` | 附加筆記到 `CLAUDE.md`（會問 scope） |

這就是本 lesson 教的全部指令面。`/init`、`/clear`、`#` —— 預期會考直接記憶題。

---

## Claude Code 處理的日常任務

進入 session 後，Claude 還能處理本來要在編輯器和終端機之間切換的日常開發事務：

- 把改動 stage 並 commit 到 git
- 跑測試
- 管理相依套件
- 執行臨時 shell 指令

設計目標：你專注在大圖像（要做什麼、spec 長怎樣），Claude 負責 glue work。

---

## 為什麼「先計畫再寫 code」有效

這部分是超出來源的 WHY：

- **注意力預算** —— 先要求計畫，model 的推理會集中在架構上，不是語法。之後實作時，架構和語法都會分到模型注意力。
- **錯誤成本** —— 計畫修起來便宜，code 改起來貴。在計畫階段抓到方向錯誤，比重寫 code 便宜 10 倍。
- **人類 review** —— 計畫很短，code diff 很長。Review 計畫只要幾秒，review diff 要幾分鐘。
- **Context 錨定** —— 對話中談定的計畫會變成 agent 生 code 時回頭參考的基準。

這就是為什麼考試把「context → plan → implement」當成標準 agent workflow，而不是只是 Claude Code 的小技巧。

---

## 常見錯誤

1. **專案開始時沒跑 `/init`** —— 失去持續 context，每場 session agent 都得重新學你的專案。
2. **沒擬計畫就開始要 code** —— 拿掉了最便宜的錯誤修正步驟。
3. **忘了餵 context** —— Claude 會猜你的慣例，產出跟 codebase 打架的 code。
4. **把 `#` 當 Markdown heading** —— 在 Claude Code 裡，訊息開頭的 `#` 是 memory append 快捷鍵，不是 Markdown 格式。
5. **想跑 `/init` 卻打成 `/clear`** —— `/clear` 清現況對話；`/init` 建立專案記憶。效果相反。

> **關鍵洞察**
>
> 核心 workflow —— **context → plan → implement** —— 是唯一能讓 Claude Code（以及一般 agent）發揮 10x 價值的 pattern。任何一步被跳過，產出品質都會顯著劣化。考試可能直接問「建議的 Claude Code workflow 是什麼」或給情境問「少了哪一步」。

---

## CCA 考試重點

- **D3（Claude Code Configuration）**：直接記憶 `/init`、`/clear`、`#`、`CLAUDE.md` scope 的題目機率很高。
- **D1（Agentic Coding & Architecture）**：「context → plan → implement」workflow 對應一般 agent best practice。
- 預期至少一題問 CLAUDE.md 三種 scope（project / local / user）。
- 預期有一題對比 `/init` 與 `/clear` —— 很容易搞混。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| `/init` 指令在 Claude Code 做什麼？ | 掃描 codebase 以理解結構、相依、風格與架構，並把總結寫入 `CLAUDE.md` |
| `CLAUDE.md` 是什麼？ | 自動在後續 Claude Code 對話中帶入的 memory 檔，保存專案相關資訊 |
| `CLAUDE.md` 的三種 scope 是什麼？ | Project（共享、進 git）、Local（個人、不進 git）、User（跨所有專案） |
| `#` 指令在 Claude Code 做什麼？ | 附加筆記到 `CLAUDE.md`，並詢問要用 project、local 還是 user scope |
| 標準 Claude Code workflow 的三步是什麼？ | 1) 讀相關檔案餵 context、2) 請 Claude 擬計畫不寫 code、3) 請 Claude 實作計畫 |
| `/clear` 做什麼？ | 清除當前 session 的對話歷史並重置 context |
| Claude Code 的 TDD 變體 workflow 是什麼？ | 餵 context → 請 Claude 發想 test cases → 實作 test → 寫出能通過 test 的 code |
| 為什麼要先擬計畫再實作？ | 計畫修改便宜、review 快、能讓 model 先專注架構再顧語法 —— 及早抓錯 |
