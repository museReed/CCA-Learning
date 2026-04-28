# Environment Inspection — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架構)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 選型) |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 82 |

---

## 一句話總結

AI agent 預設是盲的——它需要明確的「眼睛」去看你 App 的 state 才能可靠地交付結果。PM 必須從第一天就把 inspection 能力寫進預算,不能當成 nice-to-have。

---

## PM 為什麼該在意

Production AI 功能大部分的失敗不是 model「幻覺」——是 model 在它實際看不到的 state 上做動作。使用者的檔案因為錯誤假設被改掉、按鈕被宣告點擊成功但其實什麼都沒發生、資料庫 row 用過時 context 被更新。

解法不是「用更聰明的 model」,而是給 agent **觀察能力**,並且強制它在每個動作前後都用。這是 PM 的決策,因為它會出現在你的 PRD 裡:tool 需求、成本預算、可靠度 SLO。

| 沒有 Inspection | 有 Inspection |
|----------------|--------------|
| Agent 憑空猜現實 | Agent 每個決策都接地在觀察到的 state |
| 靜默失敗傳到使用者 | 失敗在同一回合就被抓到並修正 |
| 「AI 看起來不太可靠」 | 「AI 穩定地交付它承諾的東西」 |
| 錯誤編輯引發客服 ticket | 使用者信任隨時間累積 |

---

## 心智模型:沒看 X 光就動刀的外科醫師

想像一個外科醫師,靠教科書背下人體解剖,但拒絕在開刀前看你實際的 X 光片。每個病人都略有不同——器官位置會偏、血管分支不盡相同——教科書的平均值不是你的身體。

沒有 environment inspection 的 agent 就是那個醫師。他們知道程式碼、檔案、資料庫、UI 「通常」長什麼樣,然後根據平均值動作。Environment inspection 就是 X 光:它讓 Claude 看到面前這個 **特定的** 病人,不是教科書。

產品版本的心法:**agent 動刀前要先看,縫合後要再看一次。**

---

## 產品使用情境

### 什麼時候 Inspection 是關鍵

| 情境 | Inspection 給你什麼 |
|------|---------------------|
| AI 寫程式助手編輯使用者檔案 | 防止覆蓋「上次讀取之後」才發生的變更 |
| Agent 操作網頁 UI(Computer Use) | 每次點擊後的 screenshot 確認點擊成功 |
| AI 客服 agent 更新 CRM 紀錄 | Read-back 確認更新有存進去 |
| AI 內容生成器產出多媒體 | 抽 frame/字幕驗證輸出符合 brief |
| AI 操作團隊共享資料 | 抓出 race condition 和 stale-state bug |

### 什麼時候 Inspection 是過度工程

| 情境 | 為什麼可以跳過 |
|------|---------------|
| 一次性文字摘要 | 沒有 state 被變更——沒東西可 inspect |
| 固定輸入的翻譯 | 輸出就是唯一 artifact;沒有下游 state |
| 分類或評分 | Pure function——沒有環境可 inspect |

**Rule**:任何會寫入東西(檔案、DB、API、UI)的功能都該有 inspection。只讀取並回傳文字的功能通常不需要。

---

## 「不做 Inspection」的隱藏成本

團隊跳過 inspection 是因為感覺像工程 overhead。這個省法實際上買到什麼:

| 跳過省下 | 後來付的代價 |
|----------|-------------|
| 每個動作少 2 次 tool call | 客服 ticket 變 10 倍 |
| 每次請求 cost 少 ~20% | 一次錯誤編輯就失去使用者信任 |
| 回應稍快 | 工程團隊好幾個月在救 edge case |
| PRD 比較簡單 | Production 有不可知的失敗模式 |

這是典型的短期 vs 長期 trade-off。為了趕 demo date 跳過 inspection 的 PM 通常會付 5 倍回去補客服負擔。

---

## PM 決策框架

對每個 AI 功能問:

| 問題 | 為什麼重要 |
|------|-----------|
| Agent 變更了什麼 state? | 任何變更的東西都必須可觀察 |
| Agent 怎麼知道動作成功? | 答不出來 = 你有個盲 agent |
| 靜默失敗長什麼樣? | Inspection 是你即時抓靜默失敗的方法 |
| 如果 state 在 agent 上次讀取後變了會怎樣? | 答案是「資料遺失」= 寫入前強制重新 inspect |
| 怎麼衡量結果符合意圖? | 動作後的 inspection 是你的 in-band quality gate |

如果團隊說「直接相信 tool result 就好」,推回去。Claude 分不出「我做了」跟「我以為我做了」的差別,沒有證據它真的不知道。

---

## PM 常見錯誤

1. **把 inspection 當成要優化掉的 cost** — 每次 inspection 省下的客服和復原成本是它自己的好幾倍。
2. **PRD 裡沒列 inspection tool** — 你不寫,工程團隊就會做 write-only 版本。
3. **Computer Use 為了「省錢」關掉 screenshot** — 這會讓下游每個 agent 決策都靜默劣化。
4. **說「model 應該自己知道」** — Environment inspection 關心的是 model 面前的 **具體** state,訓練資料給不了這個。
5. **用「tool call 次數」當成功指標** — 你要的是「verified success rate」不是「tool call success rate」。

> **Key Insight**
>
> Environment inspection 是任何 agentic 產品裡單一槓桿最高的可靠度功能。把它寫進 PRD、把它列進 acceptance criteria——這就分開了「使用者信任的 AI 產品」跟「製造客服 ticket 的 AI 產品」。心法:「Agent 動作前看到什麼?動作後怎麼確認成功?」

---

## CCA 考試關聯

- **D1 (Agentic Coding & Architecture)**:會出情境題「agent 改錯檔案,哪裡出問題?」答案通常是「沒先檢視目前 state」。
- **D5 (Enterprise Deployment)**:Production agent 的可靠度、error handling、使用者信任都是 inspection 的下游。
- 考題關鍵字:「grounding」「observe environment」「verify output」「read before write」。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Environment inspection 為什麼對 agent 很關鍵? | Claude 預設是盲的——它需要 tool 來觀察真實 state,否則只能根據假設行動。 |
| Environment inspection 的外科醫師類比是什麼? | 一個拒絕看你 X 光的醫師——他懂一般解剖但不懂你這個病人;inspection 就是 X 光。 |
| PM 什麼時候該在 PRD 裡要求 environment inspection? | 只要 agent 會變更任何 state 就要——檔案、資料庫、UI、API。 |
| 列出三個 inspection 很關鍵的產品情境。 | AI 程式編輯器、Computer Use agent、CRM 更新 agent、內容生成器、共享資料 agent(任三)。 |
| 跳過 inspection 的隱藏成本是什麼? | 靜默失敗傳到使用者、客服 ticket 爆掉、使用者信任崩盤——通常比 inspection 本身的 cost 貴 5 倍。 |
| PM 在 PRD 裡對每個 AI 動作該問的單一問題是什麼? | 「Agent 怎麼知道這個動作成功了?」 |
| 為什麼「model 應該自己知道」是錯的 PM 直覺? | 訓練資料給的是平均值,inspection 關心的是此刻 model 面前的具體 state。 |
| 比「tool call 成功率」更重要的 success metric 是什麼? | Verified outcome success rate——觀察到的 state 是否真的符合使用者意圖。 |
