# 程式碼評分 Code-Based Grading — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任務聲明 | 3.4（deterministic 評分）、3.3（test runner 整合）、5.4（綜合 eval 指標） |
| 來源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 22 |

---

## 一句話重點

Code-based grading 是你 AI 品質指標中便宜、deterministic 的底層 —— 用微秒時間自動擋下壞掉的輸出，讓團隊不會再上線那些 demo 就能抓到的退化。

---

## 為什麼 PM 要在意

想像一下：你上線了一個 code-generation feature，結果從用戶推文才發現有一半輸出 syntax 錯。這種事不該發生。Code-based grading 讓這類退化**無法上線** —— 每個 test case 在 prompt 改動正式發佈前就自動被 parse 過。

Code grader 能抓、model grader 無法可靠抓的三件事：

- 「這到底能不能 parse 成 JSON / Python / Regex？」
- 「當我要求純 code 時，model 有沒有偷塞 commentary？」
- 「這週我們是不是不小心在 format 紀律上退化了？」

這些退化人類 demo 可能 miss，但跑在每個 prompt PR 上的 CI pipeline 絕對會抓到。

---

## 心智模型：上編輯之前先拼字檢查

把 code grader 和 model grader 想成兩階段編輯 pipeline：

| 階段 | 角色 | 成本 | 抓什麼 |
|------|------|------|--------|
| **拼字檢查**（code grader） | 自動擋下 syntax 壞掉的輸出 | 微秒、免費 | JSON parse 錯誤、Python syntax 錯誤、regex 錯誤 |
| **編輯**（model grader） | 判斷清晰度、有用度、指令遵循 | 每個 case 一次 API | 主觀品質問題 |

每一篇文字在交給真人編輯前都會先過拼字檢查。AI 輸出也一樣 —— 便宜的 deterministic 檢查先跑，過關的才進昂貴的判斷環節。

---

## 產品使用情境

### 何時用 Code Graders

| 情境 | 為什麼 code grader 適合 |
|------|-------------------------|
| 要上線 JSON API、AI 必須回合法 JSON | Parseable 是不可協商的，而且檢查免費 |
| Code-generation 功能（SQL、Python、regex） | 無效 syntax 會立刻讓產品壞掉 |
| 「只要 raw output、不要 commentary」的指令 | 用嚴格 parser 很好驗 |
| 長度或格式限制 | 是布林檢查，不是判斷題 |
| 每個 prompt PR 上 CI/CD eval gate | 微秒延遲讓它可以到處跑 |

### 何時**不要**用 Code Graders

| 情境 | 更好的替代 |
|------|-----------|
| 「這個回應有沒有幫上忙？」 | 用 model grader —— 這是主觀題 |
| 「輸出符不符合品牌語氣？」 | 用 model grader |
| 「答案對不對？」 | 除非你有 ground-truth 字串可比對，否則用 model grader |

---

## 綜合分數才是 feature

來源最後一步是把 model grader 和 code grader 分數取平均：

```
score = (model_score + syntax_score) / 2
```

這個綜合指標才是 PM 該追蹤的。它獎勵同時在形式（syntax）和內容（quality）都對的 prompt，並懲罰任一軸作弊的 prompt。

一個關鍵 PM 決策：**權重**。預設是 50/50。純 code-generation 產品可能要把 syntax 拉到 70%。客服語氣功能可能要把 quality 拉到 80%，code grader 只當硬底線。這個權重是**產品決策**，不是工程決策 —— 明確寫在 PRD 裡。

---

## PM 決策框架

| 問題 | 若答 Yes | 行動 |
|------|---------|------|
| 輸出有 deterministic 結構（JSON、code、regex）嗎？ | Yes | 加 code grader —— 免費又 deterministic |
| test case 有 `format: "python"` 這類格式欄位嗎？ | Yes | 很好 —— runner 可以自動 route |
| Eval pipeline 有 gate 在 CI 嗎？ | Yes | Code graders 是最便宜、最適合每個 PR 跑的 gate |
| 我們也在乎內容品質嗎？ | Yes | 和 model grader 合併取平均分數 |
| 有某個維度比另一個重要很多嗎？ | Yes | 在 PRD 裡調權重 —— 不要永遠預設 50/50 |

---

## 常見 PM 錯誤

1. **因為「model grader 什麼都能做」就跳過 code grader** —— 在 deterministic 檢查上浪費 token，還引入不該有的 variance。
2. **CI 沒 gate code grader** —— 壞掉的 JSON 退化會上線，沒任何東西在 review 前擋它。
3. **永遠預設 50/50 權重** —— 不是每個產品都平等看重 syntax 和品質。要刻意調。
4. **把 test case format 當成工程獨占** —— `format` 欄位是產品決策（我們對用戶承諾什麼？），該在 PRD 裡擁有。
5. **把分數當目標** —— 來源講得很清楚：分數本身無所謂好壞。重點是 prompt 迭代能不能把它往對的方向推。

> **關鍵洞察**
>
> Code graders 存在是因為某些品質屬性是二元的：JSON 不是能 parse 就是不能，Python 不是能編譯就是不能。花 model grader 去檢查這些就像花錢請書籍編輯做拼字檢查。便宜的 deterministic 檢查放前面，model grader 的 token 只花在真的需要判斷的地方。

---

## CCA 考試相關性

- **D3（Evaluation）**：Code graders 是混合 eval pipeline 的 deterministic 那一半。要知道哪些任務屬 code grader（format、syntax、長度）vs model grader（品質、helpfulness）。
- **D5（Enterprise Deployment）**：Deterministic 評分讓 eval 自動化便宜到可以 gate CI。
- 注意：「你要驗證 AI 產的 JSON / Python / Regex」→ 答案永遠是 code grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Code graders 解決了 model graders 無法可靠處理的什麼產品問題？ | 在上線前抓出壞掉的 deterministic 輸出（無效 JSON、不能 parse 的 Python、壞 regex）。 |
| Code graders 的兩大優勢？ | Deterministic（同輸入同分數）和極便宜（微秒、無 API 成本）。 |
| Code grader + model grader 的心智模型？ | 拼字檢查（code grader）先跑，真人編輯（model grader）後跑。 |
| 合併 model 和 code grader 分數的預設方式？ | 非加權平均：`(model_score + syntax_score) / 2`。 |
| Model 和 code grader 分數的權重該由誰擁有？ | PM —— 這是關於功能「哪一軸更重要」的產品決策。 |
| test case 必須帶哪個欄位，runner 才能 route 到正確 validator？ | `format` —— 值像 `"python"`、`"json"`、`"regex"`。 |
| 為什麼絕對分數無所謂好壞？ | 因為重點是 prompt 迭代能不能移動它 —— 看 delta，不看絕對值。 |
| 什麼時候應完全跳過 code grader？ | 當輸出沒有 deterministic 結構可驗（例如自由格式的有用回應）。 |
