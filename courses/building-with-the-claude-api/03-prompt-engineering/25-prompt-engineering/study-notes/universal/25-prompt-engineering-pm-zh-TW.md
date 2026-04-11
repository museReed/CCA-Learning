# Prompt Engineering — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 設計與迭代）、1.1（指令遵循） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 25 |

---

## 一句話總結

Prompt engineering 是有計分板的產品迭代——建 baseline、打分、改一件事、再打分——讓每次發版都靠數據，不是靠感覺。

---

## PM 為什麼該在乎

大多數 AI 功能上線後就把 prompt 丟著不再量測。這等同於你上線一個 landing page 卻從來不看轉換率。這堂課把 prompt 視為**一個值得自己的 CI、自己的 regression test、自己的 KPI 的產品工件**——evaluator 字面上就是一個 10 分制的分數。

沒有 eval loop 會發生：

- **漂移**——模型升級悄悄讓輸出品質退步。
- **各說各話**——RD 說「有用」，客服說「用戶在抱怨」，沒人指得出一個數字。
- **不敢動**——沒人敢碰 prompt，因為沒人能證明改動是安全的。

有了 eval loop，prompt 改動就跟其他產品改動一樣：看得到 delta、勝的就上、退步就 roll back。

---

## 心智模型：健身追蹤器

把 prompt engineering 當成用健身追蹤器訓練：

| 活動 | 沒追蹤器 | 有追蹤器 |
|------|----------|----------|
| 開始新菜單 | 「感覺有變強」 | Baseline 臥推 = 60 kg |
| 試新技巧 | 「比較累應該有用」 | 技巧 A → 62 kg (+2) |
| 再試另一招 | 「剛剛哪一招比較好？」 | 技巧 B → 70 kg (+10)，採用 |

Evaluator 就是追蹤器，prompt 是訓練菜單，各種技巧是不同運動。你只有在每次單獨量體重後才知道哪個動作真的有效。

---

## 五步驟迴圈（翻譯成 PM 語言）

| 步驟 | 做什麼 | PM 翻譯 |
|------|--------|---------|
| 1 | 設目標 | 「好」長什麼樣？定 acceptance criteria。 |
| 2 | 寫初版 prompt | 就算知道很爛也先出 v0。 |
| 3 | 評估 | 跑測試、拿一個分數。 |
| 4 | 套用一個技巧 | 只改一件事。一件。 |
| 5 | 重新評估 | 分數上去？留下。下去？回滾。 |

這就是 Lean Startup 的 build-measure-learn 套用在 prompt 粒度上。

---

## 產品應用場景

### 什麼時候值得建 eval loop

| 場景 | 為什麼重要 |
|------|------------|
| 品質主觀的用戶功能（摘要、推薦） | 人對「品質」看法不同，你需要共同計分板 |
| 受監管或高風險領域（醫療、金融、法務） | 必須能證明 prompt 行為一致 |
| 會被多位工程師在幾個月內修改的 prompt | Regression safety，改動得可證明無害 |
| 餵給下游 pipeline 的 prompt（prompt → tool call → DB 寫入） | 上游品質退步在沒有分數時很難察覺 |

### 什麼時候是 overkill

| 場景 | 更好的做法 |
|------|------------|
| 一次性內部腳本 | 手動 spot-check 就好 |
| PMF 前的丟棄型 prototype | 優先迭代速度，不是 prompt 品質 |
| 只上給五個內部用戶的 prompt | 用戶本身就是 eval |

---

## 計分板思維

課程給了具體數字：baseline 2.3/10 很正常。PM 該內化幾個錨點：

| 分數 (/10) | 代表什麼 | 可以發嗎 |
|-----------|----------|----------|
| 2-3 | 初版 baseline | 絕對不行 |
| 5-6 | 套了 clarity + specificity | 內部試吃 |
| 7-8 | 加了 examples + 結構 | Beta |
| 9+ | Edge case 都硬化了 | 正式上 |

這是有立場的——課程示範 2.3 → 3.92 → 7.86 連跳兩個技巧。PM 的重點是：**把分數門檻綁到每個發版 gate**，不是模糊的「看起來 OK」。

---

## PM 決策框架

準備發 AI 功能時問：

| 問題 | 如果是，你需要 |
|------|---------------|
| 這個 prompt 上線後會被改超過一次嗎？ | Eval loop + regression tracking |
| 不同利害關係人對品質有分歧嗎？ | 用 `extra_criteria` 把 rubric 寫死 |
| 品質是主觀的（tone、格式、完整度）嗎？ | Model-graded evaluator，不是只跑 unit test |
| 未來模型升級會影響這個功能嗎？ | 固定 baseline 分數，讓升級自己證明 |
| 我們在乎 p95 品質還是只在乎平均值？ | 最終驗證跑大一點的資料集 |

---

## 常見 PM 錯誤

1. **「在我的範例上有用」** — 一個 happy path 不是 eval，那是 demo。
2. **跳過 baseline** — 上線時就用一個「好」prompt，結果你永遠無法證明下一版更好。
3. **改動 rubric** — 在迭代中途改 `extra_criteria`，前後分數失去可比性。Rubric 凍結、迭代 prompt。
4. **太早投資** — 還沒發 baseline 就去蓋 500 case 的 eval harness 是燒 runway。先從 2-3 case 開始。
5. **只看分數不看報告** — PM 只盯數字就錯過 grader 的推理，那才是產品洞察的來源。

> **Key Insight**
>
> Prompt engineering 把一個主觀的產品工件變成可量測的。對 PM 來說這就是「靠感覺發版」和「靠數據發版」的差距。一旦有分數，你就能擁有它、保衛它、回滾退步、推動改進——這會把 AI 功能從魔法變成工程。

---

## CCA 考試相關性

- **D3 (Evaluation & Iteration)**：要認得出 eval-driven loop 是「怎麼改善一個 prompt？」的標準答案。
- **D1 (Agentic Architecture)**：同一套 loop 也用來調 agent system prompt。題目可能把 agent 行為錯誤包裝成 prompt 調校問題。
- 題目會問：「團隊 prompt 得 2.3/10，下一步？」答案永遠是「套一個技巧再評估」，不是「重寫」。
- 要知道迭代早期用小資料集（2-3 case）是刻意設計，不是缺陷。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 這堂課 prompt engineering 的核心概念？ | 可迭代的 loop：baseline → 評估 → 套技巧 → 重新評估。可量測，不是靠感覺。 |
| PM 為什麼要幫每次 prompt 發版綁分數？ | 沒分數就不知道改動是進步還是退步，分數把 prompt 變成可管理的產品工件。 |
| 典型 baseline 分數是多少？PM 該怎麼反應？ | 約 2.3/10，把它當起點不是警報。 |
| 為什麼每次迭代只套一個技巧？ | 才能歸因分數變化，建立可靠的未來 playbook。 |
| `extra_criteria` 翻譯成 PM 語言？ | Rubric，grader 要評分的必備項清單，是把業務需求編碼進 eval 的方式。 |
| 「健身追蹤器」類比是什麼？ | Evaluator 是體重計/追蹤器，prompt 是訓練菜單，每個技巧是一個動作，每次單獨量。 |
| 什麼時候建 eval loop 是 overkill？ | 一次性腳本、PMF 前 prototype、只上給少數內部用戶的 prompt。 |
| 這堂課支持什麼樣的發版 gate 模式？ | 把每個發版階段（內部、beta、GA）綁到最低分數門檻。 |
