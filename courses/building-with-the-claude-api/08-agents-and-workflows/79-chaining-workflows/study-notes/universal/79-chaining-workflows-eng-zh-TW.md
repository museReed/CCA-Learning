# Chaining Workflows — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.2(agentic 模式 — chaining)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 79 |

---

## 一句話總結

Chaining 是最簡單也最實用的 workflow 模式:把複雜任務拆成循序的 LLM 呼叫序列,每一步的輸出餵給下一步 — 與 parallelization 相反,用在後續步驟*依賴*前面步驟的情境。

---

## 什麼是 Prompt Chaining

出自 Anthropic「Building Effective Agents」部落格,**prompt chaining** 把任務拆成一系列步驟,每次 LLM 呼叫處理前一次的輸出。當你能乾淨地拆解任務,而且每一步都依賴前一步的結果時,這個模式最適合。

你需要 chaining 的關鍵訊號:步驟可以依序列出,而且步驟 N+1 真的需要步驟 N 的輸出。

---

## 課程中的社群媒體範例

課程示範一個自動生成並發布影片的社群媒體行銷工具:

```
1. 從 Twitter 找相關熱門主題       (非 LLM)
2. 選出最吸引人的主題                (Claude)
3. 研究該主題                        (Claude)
4. 寫短影片腳本                      (Claude)
5. 用 AI 虛擬人 + TTS 產生影片       (非 LLM)
6. 發布到社群媒體                    (非 LLM)
```

重點觀察:
- **不是每步都是 LLM 呼叫。** Chain 可以混搭 LLM 與非 LLM 處理(步驟 1 是 Twitter API、步驟 5 是影片 pipeline、步驟 6 是發布 API)。
- **每個 LLM 步驟都聚焦。** Claude 在步驟 2 挑主題、步驟 3 研究、步驟 4 寫腳本 — 從不在同一 prompt 裡做三件事。
- **輸出往後傳。** 選好的主題變成研究步驟的輸入;研究結果變成腳本步驟的輸入。

---

## 為什麼要 chain 而不是一個大 prompt

Chaining 給你:

1. **每步都聚焦。** Claude 專心做好一件事,而不是同時應付全部。
2. **非 LLM 處理的 hook。** 步驟之間,你的程式碼可以驗證、轉換、抓資料、或短路流程。
3. **可測試。** 每一步有乾淨的 input/output contract,容易 unit test 和 eval。
4. **可觀測。** 失敗被定位到特定步驟,而不是埋在巨型 prompt 裡。
5. **部分重跑。** 5 步裡第 3 步失敗時,可以從第 3 步重跑,不用整個重來。

---

## 長 Prompt 問題(課程的核心動機)

即便你的限制寫得很清楚,Claude 有時還是會在長 prompt 中忽略規則。課程範例是寫一篇技術文章,要:

- 不能提到是 AI 寫的
- 不能用 emoji
- 不能有過時或過於隨意的語言
- 要專業、技術語氣

單一 prompt 想一邊生好內容、一邊滿足四個限制,常常產出違反其中一個以上的結果。

### Chaining 解法

拆成兩步:

**步驟 1 — 初稿**
```python
draft = claude.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user",
               "content": f"寫一篇關於 {topic} 的技術文章。"}]
).content[0].text
```

**步驟 2 — 聚焦修訂**
```python
final = claude.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"""
請修訂下方文章。

依照以下步驟重寫:
1. 找出任何指明作者是 AI 的地方,刪除
2. 找出並刪除所有 emoji
3. 找出任何尷尬用語,替換為技術寫作者會用的語氣

<article>
{draft}
</article>
"""}]
).content[0].text
```

步驟 2 中,Claude 不是同時在*建立*好文章*並*滿足限制 — 它只是在已寫好的文章上執行限制。聚焦任務能完成組合任務失敗的事。

---

## 標準 Python 實作

```python
from anthropic import Anthropic

client = Anthropic()

def call_claude(system: str, user: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text

def social_media_chain(keyword: str) -> str:
    # Step 1: 非 LLM — 抓趨勢
    trends = twitter_api.fetch_trends(keyword)

    # Step 2: LLM — 挑最佳主題
    topic = call_claude(
        system="你負責挑選最吸引人的趨勢。",
        user=f"趨勢:\n{trends}\n\n回傳單一最佳主題。",
    )

    # Step 3: LLM — 研究主題(帶錯誤檢查)
    research = call_claude(
        system="你是精簡的研究員。",
        user=f"研究這個主題:{topic}",
    )
    if len(research) < 100:
        raise RuntimeError("研究步驟回傳內容過少")

    # Step 4: LLM — 用研究內容寫腳本
    script = call_claude(
        system="你寫 60 秒影片腳本。",
        user=f"用這份研究寫腳本:\n{research}",
    )

    # Step 5: 非 LLM — 合成影片
    video = video_pipeline.synthesize(script)

    # Step 6: 非 LLM — 發布
    return social_media.post(video)
```

每一步都有清楚的 contract、錯誤處理 hook,可以獨立替換。

---

## Chain 中的錯誤傳遞

因為每一步依賴前一步,chain 必須刻意處理錯誤:

| 策略 | 說明 | 使用時機 |
|------|------|---------|
| **Fail fast** | 一失敗就拋例外 | 早期 prototype、簡單流程 |
| **Retry step** | 失敗步驟用 backoff 重試 | 短暫 API 錯誤 |
| **Validate then branch** | 檢查步驟輸出,選下一步 | 輸出品質有變動(例如空研究)|
| **Graceful degradation** | 跳過非關鍵步驟 | 選用的豐富化步驟 |
| **Replay from checkpoint** | 持久化步驟輸出,重試時接續 | 長 chain、昂貴呼叫 |

Production chain 通常五種都混用,每一步都包 retry + validation。

---

## Chaining vs Parallelization vs Agent

| 面向 | Chaining | Parallelization | Agent |
|------|----------|-----------------|-------|
| 步驟相依性 | 有(循序)| 無(獨立)| 執行期決定 |
| Control flow | 程式碼 | 程式碼 | LLM |
| 延遲 | 步驟延遲總和 | 步驟延遲最大值 | 變動 |
| 成本 | 步驟成本總和 | 步驟成本總和 | 變動 |
| 最適合 | 有依賴的多步複雜任務 | 跨獨立準則的複雜決策 | 開放式任務 |

---

## 常見錯誤

1. **該 chain 卻做成 agent。** 如果你能列出步驟,chain 比把流程交給 Claude 更簡單可靠。
2. **Chain 太長。** 每步都是失敗點。如果 LLM 呼叫超過 10 次,考慮拆成多個 chain 加 checkpoint。
3. **忘了在步驟間傳遞 context。** 步驟 4 需要步驟 3 的輸出 — 不要以為 Claude 會記得,要明確注入。
4. **步驟間沒錯誤處理。** 一個壞步驟可以把垃圾傳到最後。要在步驟間驗證。
5. **把該用單一呼叫的任務做成 chain。** 不是每個任務都該 chain。如果一個 prompt 可靠就用一個 prompt。

---

> **關鍵洞察**
>
> Chaining 是「長 prompt 問題」的解法模式。當 Claude 在巨型 prompt 中忽略限制時,拆開任務:一個呼叫負責生,另一個負責執行限制。這個「聚焦注意力」原則延伸到任何下一步需要前一步輸出的多步任務。考試記住:**chaining 有序列依賴,parallelization 沒有。**

---

## CCA 考試關聯

- **D1(22%)主要**: Chaining 是四大 workflow 模式之一,預期有情境題要你與 parallelization 和 routing 區分。
- **D5(20%)次要**: Production chain 需要錯誤處理、checkpoint、步驟間驗證。
- Chaining 訊號字:「sequential」、「output of step N feeds step N+1」、「focus on one aspect at a time」、「break down into steps」。
- 關鍵區分:chaining = 序列依賴;parallelization = 獨立子任務。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 什麼是 prompt chaining? | 把任務拆成循序 LLM 呼叫,每一步輸出餵下一步 |
| Chaining 和 parallelization 的差別? | Chaining 有序列依賴;parallelization 是並行獨立子任務 |
| Chaining 解決的「長 prompt 問題」是什麼? | Claude 在巨型 prompt 中忽略限制;拆成「生成 + 修訂」步驟可靠地強制執行 |
| Chain 可以包含非 LLM 步驟嗎? | 可以 — chain 常常混搭 LLM 呼叫與 API、驗證、資料轉換 |
| 強制限制的兩步 chaining 解法? | 步驟 1:生初稿。步驟 2:專門修訂執行每條規則 |
| 列出 chain 的四種錯誤處理策略。 | Fail-fast、retry-step、validate-then-branch、graceful degradation、replay-from-checkpoint |
| Chaining 和 parallelization 的權衡? | Chaining 延遲總和(較慢)但支援依賴;parallelization 延遲最大值但需獨立 |
| 什麼時候*不*該用 chaining? | 當單一 prompt 可靠或子任務可獨立執行時(改用 parallelization)|
