# Prompt Evaluation — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.1（eval 設計）、3.2（測試資料集）、3.3（eval 執行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 17 |

---

## 一句話摘要

Prompt evaluation 是 AI 功能的「產品品質版 A/B 測試」— 它讓團隊改 prompt 時能帶著「量測出來的信心」上線，而不是祈禱上次那個小調整沒把真實用戶搞壞。

---

## PM 為什麼要在意

每一個 AI 功能背後都有一個 prompt。沒有 evaluation pipeline，「這個 prompt 好不好？」就只是工程師的意見，不是產品的事實。這個落差會直接造成商業後果。

| 症狀 | 根因 | 商業衝擊 |
|------|------|----------|
| 客戶反映「AI 答錯了」 | Prompt 從沒在真實流量上測過 | 客戶流失、品牌信任受損 |
| 工程師爭論哪版 prompt「比較好」 | 沒有客觀指標終結辯論 | 迭代變慢、變成政治決策 |
| 不敢改現有 prompt | 沒有安全網抓 regression | 功能停滯、prompt tech debt |
| 無法跟高層報一個品質數字 | 根本沒有 eval 分數 | 沒辦法設 AI 品質 OKR |

Prompt evaluation 把上面每一個「意見」和「恐懼」變成一個數字。PM 就是靠數字管產品的。

---

## 心智模型：餐廳廚房

把 prompt 想成食譜，prompt evaluation 想成試菜團隊。

| 廚房概念 | Prompt 概念 |
|----------|-------------|
| 食譜卡 | Prompt template |
| 主廚調整食譜 | Prompt engineer 調整 prompt |
| 主廚試一次就出菜 | 選項 1 — 測一次就上 |
| 主廚試五次、補一點調味 | 選項 2 — 測幾次、補邊角案例 |
| 試菜小組對 20 道菜打分，主廚據此迭代 | 選項 3 — 跑 eval pipeline |

選項 3 是唯一能讓你擁有米其林等級廚房的路。選項 1 和 2 感覺快，但做出來的晚餐品質不穩定。

---

## 三條路 — PM 視角

| 選項 | 工程師實際做了什麼 | PM 看得到的風險 |
|------|--------------------|----------------|
| 1. 測一次 | 跑一個例子看起來還行就上 | 高：任何不尋常的用戶輸入都可能變成故障 |
| 2. 測幾次補洞 | 跑幾個他想得到的邊角案例 | 中：人類想像力抓不到真實長尾 |
| 3. Eval pipeline | 跑數百、數千個案例進自動化 scorer | 低：regression 在開發機就被抓到，不是客服工單 |

工程師說「prompt 好了」，PM 下一個問題永遠該是：*你剛剛走的是三條路裡的哪一條？*

---

## 產品場景

### Evaluation 不可省

| 場景 | 原因 |
|------|------|
| 面向客戶的 AI 功能 | 失敗對用戶可見，事故代價高 |
| 涉及金錢、健康、法律、安全的 prompt | 正確性是法遵和責任問題 |
| 計畫每月迭代的功能 | 沒有 eval，每次迭代都是 regression 風險 |
| 想比較兩個模型的功能（Haiku vs. Sonnet） | Eval 提供 cost/quality trade-off 所需的客觀比較 |

### 可以短暫延後

| 場景 | 注意事項 |
|------|----------|
| 下週 demo 的內部原型 | 可延後，但沒 eval 就不能正式上線 |
| 一次性拋棄腳本 | 可延後，但要知道你在欠技術債 |

---

## PM 決策框架

批准任何 AI 功能 GA 之前問：

| 問題 | 如果「沒有」 |
|------|-------------|
| 有一份反映真實用戶輸入的 eval 資料集嗎？ | 擋下發佈 — 你根本沒法量品質 |
| 能產出目前 prompt 版本的客觀分數嗎？ | 擋下發佈 — 你沒有 baseline |
| 下個月改 prompt 時 CI 會告訴你品質升降嗎？ | 擋下發佈 — 你沒有 regression 安全網 |
| 能在發佈文件的品質章節引用一個數字嗎？ | 擋下發佈 — 你的品質敘事全靠感覺 |

---

## PM 常見錯誤

1. **把「看起來還不錯」當品質訊號** — GA 前應該要求的是一個數字，不是感覺。
2. **因時程壓力讓工程師跳過 eval** — 每跳過一次 eval 就是未來要付的 production 故障。
3. **沒把 eval 的 API 花費算進預算** — Eval 要錢，從第一天起就應該納入功能成本模型。
4. **把一次好 demo 當成 production 準備度** — 一次 demo 就是選項 1，而選項 1 是陷阱。
5. **沒把 eval 資料集當成 PM 的產出物** — 資料集編碼了「什麼才叫好」，那是 PM 的決策，不是 junior eng 的決定。

---

> **Key Insight**
>
> PM 的工作就是把「品質」變成一個數字。Prompt evaluation 就是那個機制，把 AI 品質從主觀論戰變成能寫進 OKR、發佈文件、事故回顧的客觀指標。CCA 考題只要問「我們怎麼知道這個 prompt 可以上 production 了？」那就是 D3 題，答案永遠是：跑 eval pipeline。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：區分 prompt engineering（怎麼寫）與 prompt evaluation（怎麼量）；知道三條路和為什麼選項 3 贏。
- **D5（Enterprise Deployment）**：Prompt eval 是 production 發佈的前置條件 — 沒 eval 就不上線。
- 考題常見話術：「怎麼比較 prompt 版本」「怎麼抓 regression」「怎麼回報品質」都是 D3/D5，都指向 eval pipeline。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt evaluation 解決的 PM 問題是什麼？ | 把「這 prompt 好不好？」這種主觀判斷，變成能寫進發佈文件、OKR 與事故回顧的客觀分數。 |
| Prompt evaluation 的餐廳比喻是什麼？ | 試菜小組按評分表給菜打分，主廚帶著信心迭代，而不是只靠一次試吃。 |
| Prompt 寫好後 PM 該問哪三條路？ | 1) 測一次、2) 測幾個邊角案例、3) 跑 eval pipeline — 只有 3 才適合 GA。 |
| PM 在批准 GA 前必須要求什麼？ | 資料集、客觀分數、regression 安全網，以及能寫進發佈文件的數字。 |
| 為什麼「demo 看起來不錯」不夠？ | Demo 就是選項 1 — 一個例子不是真實流量的隨機抽樣，會隱藏失敗模式。 |
| 什麼情況下可以延後做 eval pipeline？ | 只有內部原型或一次性腳本 — 面向客戶的功能絕對不行。 |
| Eval 資料集歸誰擁有？ | 這是 PM 級別的產出，因為它編碼了「什麼才叫好」，不是純工程決策。 |
| Prompt evaluation 對應哪個 CCA domain？ | D3 Evaluation & Iteration（主要）、D5 Enterprise Deployment（次要，作為 production 閘門）。 |
