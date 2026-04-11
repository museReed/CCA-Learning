# 專案概覽:提醒應用 — PM Perspective

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1(tool schema 設計)、1.2(agentic loop 基礎)、1.1(功能拆解) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 33 |

---

## 一句話總結

三個字的使用者需求(「下週四提醒我」)底下藏著三個不同的產品能力缺口 — 正確的 AI 產品架構是**每個缺口配一個 tool**,而不是做一個「全能魔法函式」。

---

## 「提醒我」的假性簡單

PRD 上可能這樣寫:

> *作為使用者,我可以說「下下個星期四提醒我某件事」,助手會幫我設好提醒。*

所有 stakeholder 點頭。兩句話的 user story。兩天的 ticket 吧?

不是。底層模型不會:

1. 知道此刻精確時間(只知道大概日期)
2. 可靠地做日期運算(LLM 算星期幾出錯頻率超乎想像)
3. 把提醒存到任何地方

每一條都是不同的問題,都要自己的元件。這是 PM 在 scope AI 功能時最常踩的雷:表面是一句話,底下的能力圖是一棵樹。

---

## 心智模型:樂高 vs. 公仔

| 方法 | 比喻 | v1 出貨速度 | 長期槓桿 |
|------|------|-------------|----------|
| 一個「全做完」的大 function | 公仔 — 塑到固定的姿勢 | 快 | 零重用、難修 |
| 小小的原子 tool,由 Claude 組合 | 樂高 — 積木 | 稍慢 | 未來任何功能都能重用 |

Tool use 獎勵樂高派。第一次做 `add_duration_to_datetime` 時你付出成本。之後任何碰到「提醒我 N 天後」「N 週後截止」「下季再訂」的功能都能免費重用同一塊積木。

---

## 三個缺口 → 三個 Tool

| 使用者訊號 | 暴露的缺口 | 該做的 tool |
|-----------|------------|-------------|
| 「現在」 | Claude 不知道精確時間 | Get current datetime |
| 「下下個星期四」 | Claude 日期運算不可靠 | Add duration to datetime |
| 「提醒我」 | Claude 沒有提醒系統 | Set reminder |

每一列都是 PRD 裡的決策點。每個 tool 都有自己的 acceptance criteria、失敗模式、遙測需求。

---

## 為何這對 Roadmap 規劃很重要

因為 tool 可以重用,所以幫提醒功能做 scoping 的同時,你也幫**未來好幾個功能**做了 scoping:

- 生日提醒(三個 tool 全部重用)
- 截止日追蹤(重用其中兩個)
- 週期性會議(重用其中兩個)
- 假期倒數(重用其中兩個)
- 「N 週後是幾號」類的問答(重用其中兩個)

看到這個模式的 PM 可以把功能賣給 stakeholder 說「我們是在打排程系統的地基」,而不是「我們做了個玩具提醒 app」。ROI 算盤完全翻轉。

---

## 把建構順序當作風險管理工具

課程是最簡單的先做:

1. Read-only 先做(get current datetime)— 壞了影響最小。
2. Pure function 第二(add duration)— 決定性、可單測。
3. Write operation 最後(set reminder)— 有真實世界副作用,有真實風險。

對 PM 而言,這也是 dogfood 的順序。先內部出第一個 tool、再第二個,只有兩個依賴都穩了才出寫入型 tool。每個階段都可上線。

---

## PM 決策框架

看到「聽起來很簡單」的 user story 就問:

| 問題 | 若是 | 行動 |
|------|------|------|
| 需要此刻的資料嗎? | 是 | 規劃一個 tool。 |
| 需要 LLM 不擅長的運算(日期、金額、距離)嗎? | 是 | 規劃一個 tool。 |
| 需要把狀態持久化? | 是 | 規劃一個 tool。 |
| 這幾個 tool 在其他功能用得到? | 是 | 提升優先級 — 是地基。 |
| Stakeholder 以為「這很簡單、一個 call 就夠」? | 是 | 跟他一起跑這個 gap 分析。 |

---

## PM 常犯的錯

1. **誤判 scope** — 「提醒我」聽起來兩天的 ticket,實際上是三個 tool 加一個 agent loop。排期要對應調整。
2. **在壓力下 bundling** — stakeholder 會說「做一個全包 function 就好」。抗住,長期成本遠高。
3. **沒行銷重用價值** — 沒把地基工作包裝好,會讓人覺得是過度工程一個小功能。
4. **跳過玩具專案** — 把這個 pattern 直接用在高風險功能上,等於把學習曲線推到生產環境。
5. **沒為 multi-turn loop 設計 loading state** — 三次 tool call 加三次 API call 會疊出好幾秒的延遲,得先設計好。

> **Key Insight**
>
> 提醒專案是 AI 產品管理「冰山」問題最清楚的範例:聽起來瑣碎的 user story 底下坐著多個截然不同的能力缺口。正確的回應是每個缺口配一個 tool — 因為每個 tool 都會變成未來功能的可重用資產。CCA 考試會出「如何把自然語言功能拆成 tool」類型的題目。

---

## CCA 考試重點

- **D1(Agentic Architecture)**:認知一次使用者輸入可能觸發多次 tool call,順序由 Claude 規劃。
- **D2(Tool Design & MCP Integration)**:「一個缺口一個 tool」的設計原則會被直接測。
- 考題常見模式:給一個功能(「提醒我」「摘要今天」「訂會議」),要你辨認出最少需要的 tool 集合。

---

## Flashcards

| Front | Back |
|-------|------|
| AI 產品 scoping 的「冰山」陷阱是什麼? | 一句話的 user story(「下週四提醒我」)底下藏多個不同的能力缺口;正確 scope 是每個缺口配一個 tool。 |
| 為何提醒 app 是好的首個專案? | 它用一個友善的故事示範實際的多 tool 組合,風險逐步升級(read-only → pure function → write)。 |
| 樂高 vs. 公仔的比喻是什麼? | 原子 tool 像樂高積木(跨功能重用);大 function 像公仔(一次性、無重用)。 |
| 提醒 app 的 tool 可以在哪些未來功能被重用? | 生日提醒、截止日追蹤、週期性會議、假期倒數、「N 週後是幾號」問答。 |
| 這個專案建議的 tool 建構順序是? | Read-only 先、pure function 第二、write/有副作用最後 — 風險梯度。 |
| Scoping「提醒我」類功能時 PM 第一個常犯的錯是? | 估錯大小 — 以為是簡單 ticket,實際上是三個 tool 加 multi-turn loop。 |
| 為何要替這類功能預算 loading state? | 多次 tool call 加 API round trip 很容易疊出好幾秒延遲。 |
| 如何把地基 tool 工作賣給 stakeholder? | 包裝成「為一整家族的未來功能打地基」,而不是「做玩具提醒 app」。 |
