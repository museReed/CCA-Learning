# Being Clear and Direct — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 設計與迭代）、1.1（指令遵循） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 26 |

---

## 一句話總結

Prompt 的第一行是 heavy lifting 的關鍵——用祈使動詞開頭、直接描述任務，讓 Claude 對你要什麼完全沒有模糊空間。

---

## 第一行原則

課程直接斷言：prompt 的第一行是整個 request 最重要的部分。後面所有的東西——context、constraints、examples——都是環繞這個開頭指令的鷹架。第一行寫對，Claude 立刻對齊意圖；第一行寫錯，後面再多 context 也救不完全。

管住第一行的兩個原則：**clarity（清楚）** 和 **directness（直接）**。

---

## Clarity：prompt 怎麼用字

「清楚」關於選字與明確性：

- 用任何人都看得懂的簡單語言。
- 直接說你要什麼，不要繞路、不要清嗓子。
- 開頭就用一句直白描述 Claude 的任務。

像「我需要知道那種人家放在屋頂上、用太陽的東西——我想叫太陽能板的那種」這種模糊開頭，逼 Claude 猜主題、格式、深度都要猜。清楚改寫——「Write three paragraphs about how solar panels work.」——一句話鎖定全部三項。

---

## Directness：prompt 怎麼結構化

「直接」關於語法形式：

- **用指令，不要用問句**。
- 用 action verb 開頭：Write、Create、Generate、Identify、Summarize、Extract、List。

像「我在看再生能源，地熱聽起來很酷。有哪些國家在用？」這種問句會讓 Claude 用對話語氣回答、沒有結構。直接改寫——「Identify three countries that use geothermal energy. Include generation stats for each.」——指定了數量（3）、限制（用地熱）、必要輸出（每國附統計）。

語法從問句變命令是有實際作用的。問句引出回答，祈使句引出產出。

---

## 貫穿範例

套用到 Lesson 25 的餐單 prompt：

**弱 baseline：**

```
What should this person eat?
```

**Clear and direct 改寫：**

```
Generate a one-day meal plan for an athlete that meets their dietary restrictions.
```

改寫版一句話告訴 Claude 三件事：

| 元素 | 值 |
|------|-----|
| 動作 | Generate |
| 對象 | 一份餐單 |
| 限制 | 一日份、給運動員、符合飲食限制 |

問句版本這三個元素全都缺。

---

## 量測結果

課程給了跑 evaluator 的具體數字：

| 版本 | 分數 (/10) |
|------|-----------|
| "What should this person eat?" | 2.32 |
| "Generate a one-day meal plan for an athlete that meets their dietary restrictions." | 3.92 |

單單改一行就 **+1.60 的絕對進步**。這不是終點——後面的技巧（specificity、examples、structure）還會繼續往上推——但證明了光第一行就值好幾分。

---

## 為什麼這在機制上有效

Claude 被訓練成遵循指令。看到祈使句開頭時，模型的 next-token 機率分佈會往「服從、產出要求的 artifact」這類 response pattern 靠攏。看到模糊問句時，分佈會散到多種可能的 response style：對話、澄清、推測、保留。祈使句把分佈 collapse 到你要的模式。

所以課程提的「把 Claude 當成需要明確指引的能幹助理」比「正在聊天的朋友」好用。前者把互動 framing 成任務執行，後者邀請閒聊。

---

## 常見錯誤

1. **開頭先給 context** — 「我在看 X……」把指令延後又稀釋。指令先、context 後。
2. **把任務寫成問句** — 問句看起來禮貌但結構模糊。
3. **用模糊名詞** — 「那些東西」「一些」「合理就好」都把詮釋 push 給 Claude。
4. **以為後面指令會修好爛第一行** — 後文能 refine 但不能 retro-frame 一個糊的開頭。
5. **疊加保留語** — 「如果可以的話，可不可以也許……」把祈使句弱化成選配。

> **Key Insight**
>
> 祈使句開頭是 prompt engineering 裡最便宜、最快的勝利。在加 examples、加結構、加 XML tag 之前，先把第一行重寫成 action verb 開頭的命令句。課程範例中這個改動在 10 分制上貢獻 +1.6 分——每個字元的投報率比其他任何技巧都高。

---

## CCA 考試相關性

- **D3 (Evaluation & Iteration)**：「問句 → 祈使句」是 prompt 改進 playbook 的第一招，也是最便宜的一招。
- **D1 (Agentic Architecture)**：agent 的 system prompt 同一個原則——先寫 agent 的核心祈使，不要先寫前言。
- 題目可能給一個弱 prompt，要你選改進版——祈使句改寫幾乎永遠是答案。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Prompt 哪一行最重要？ | 第一行。它為後續一切定調，決定 Claude 怎麼 framing 回應。 |
| 寫好第一行的兩個原則？ | Clarity（簡單無歧義）和 Directness（用指令不用問句、action verb 開頭）。 |
| 太陽能板弱 vs 清楚開頭各一例？ | 弱：「屋頂上那個用太陽的東西」；清楚：「Write three paragraphs about how solar panels work.」 |
| Prompt 該用什麼語法形式？ | 祈使句（命令）用 Write、Create、Generate、Identify 這類 action verb 開頭，不用問句。 |
| 課程量到光靠 clarity + directness 的分數進步？ | 2.32 → 3.92，改一行的 +1.6 分進步。 |
| 為什麼祈使句比問句對 Claude 更有效？ | 它把 response 分佈 collapse 到任務執行，而不是對話或澄清模式。 |
| 改寫後餐單開頭告訴 Claude 哪三件事？ | 動作（generate）、對象（meal plan）、限制（一日、運動員、符合飲食限制）。 |
