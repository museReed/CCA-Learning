# Getting an API Key — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Claude Code Configuration (20%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 3.1（API key lifecycle）、3.2（workspace 與 key 命名）、5.3（生產環境 secret 衛生） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 05 |

---

## One-Liner

Anthropic 的 API key 是一張「寫入後只能讀一次」的 bearer credential，透過 Console 在指定的 workspace 底下建立——它只會顯示一次，沒看到當下複製就永遠拿不回來。

---

## 建立流程五步驟

```
Console 登入 ─▶ Get API Keys ─▶ Create Key ─▶ Workspace + 命名 ─▶ 只能複製一次
    1              2              3              4                  5
```

| 步驟 | 動作 | 備註 |
|------|------|------|
| 1 | 瀏覽 `https://console.anthropic.com/` 並登入 | 用要負責計費與稽核的帳號 |
| 2 | 點 **Get API Keys**（dashboard 右上） | 會進到 key 管理頁 |
| 3 | 點 **Create Key**（key 頁右上） | 打開建立對話框 |
| 4 | 選 workspace（例如 `Default`）並取名（例如 `Anthropic Course`） | 名字只是給人看的識別；workspace 才是計費/稽核邊界 |
| 5 | 立刻複製 | **這個值只會顯示一次**；對話框關掉就只能刪了重建 |

「只能複製一次」這個規則不是 UX 小瑕疵，而是安全設計。Anthropic 建立後就不再儲存明文 key，只保留 hash。**你掉了沒人救得回來，反過來講也沒人能從客服工單把它偷走。**

---

## Workspace：隔離的單位

Workspace 是計費、rate limit、用量報表的邊界。選對 workspace 是生產決策，不是裝飾。

| Workspace 策略 | 適合誰 | 取捨 |
|---------------|-------|------|
| 一個產品一個 workspace | 乾淨的產品級計費與配額 | 工程師要切來切去 |
| 一個環境一個 workspace（dev/staging/prod） | 環境隔離、事故圍堵 | 要管的 key 比較多 |
| 共用 `Default` workspace | POC / 教學 | 不同專案之間無法歸帳 |

只要是認真在跑的生產 app，就像管 AWS account 一樣管 workspace：**至少 prod/非 prod 分開。**

---

## Key 命名：一個小習慣省你一堆時間

名字是 free-form 的，只用來給人辨識。**早點立規矩：**

```
<env>-<service>-<owner>-<date>
prod-chatbot-backend-2025-04-11
dev-ingest-worker-2025-04-11
```

看到可疑帳單或要 rotate key 的時候，名字是你在 console 裡唯一的查詢鍵。取成「My Key 3」會在事故時讓你多花好幾小時。

---

## Key 在程式碼中的處理

Anthropic 的 SDK 會自動讀取環境變數 `ANTHROPIC_API_KEY`。這是 Lesson 06 會用到的 pattern，也是唯一可以接受的起手式：

```bash
# .env（絕對不要 commit）
ANTHROPIC_API_KEY="sk-ant-api03-...your-key..."
```

```python
# Python — SDK 會自己從環境變數抓
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()  # 不用顯式傳 key
```

Key 在程式碼中的鐵律：

| 規則 | 原因 |
|------|------|
| 絕對不 commit `.env` | Public repo 會觸發自動 revoke，private repo 也會從 fork 洩漏 |
| `.env` 一律加進 `.gitignore` | 雙保險防止誤 commit |
| 生產環境用 secret manager（AWS Secrets Manager、GCP Secret Manager、HashiCorp Vault） | 裸 server 的環境變數 POC 可以，但沒稽核軌跡 |
| 懷疑洩漏就立刻 rotate | Console 刪舊 → 建新 → redeploy |
| 不要透過 chat/email/截圖分享 | 真的必須分享就用密碼管理器的 secure share |

---

## 「key 遺失」工作流

因為值只會顯示一次，恢復路徑很明確：**不能恢復，只能 rotate。**

```
                ┌──────────────────┐
                │    key 掉了？     │
                └────────┬─────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    Console 找到                  Console 刪掉
    那把 key                      那把遺失的 key
         │                               │
         └───────────────┬───────────────┘
                         ▼
                Console: Create Key
                （新的值，新的「只能複製一次」視窗）
                         ▼
                更新 .env / secret manager
                / redeploy
```

這也是排程 rotate 的完全相同流程——**沒有「拿回既有 key 的值」這個 API。**

---

## 程式碼範例：顯式傳 key（只能用在測試）

SDK 允許直接把 key 當參數傳，但這只能用在丟棄式的腳本：

```python
from anthropic import Anthropic

# 只有 one-off notebook 或測試可接受，生產環境絕對不要
client = Anthropic(api_key="sk-ant-api03-...")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": "ping"}],
)
print(response.content[0].text)
```

這個 pattern 一旦離開 notebook 就變成地雷——一個手滑的 `git add .` 就把 key 推到 remote。

---

## Common Mistakes

1. **對話框還沒複製就關掉** —— 值救不回來，只能刪了重建。
2. **Key commit 進 git** —— 即使是 private repo 也會從 fork、備份、之後開源洩漏。一律用環境變數。
3. **用「My Key」或「Test」當名字** —— 事故發生時你會不知道哪把 key 歸哪個 service。
4. **Dev 和 prod 共用一個 workspace** —— Dev 失控的 job 會把你的生產配額抽乾。
5. **從來不 rotate** —— Key 應該排程過期（季度是合理 default），沒用的 key 要刪掉。

> **Key Insight**
>
> 「只能複製一次」的對話框不是不方便——**它就是 API key 安全的根本原因。** 如果 Anthropic 之後還能給你看這個 key，那被盜號的攻擊者也能。把「複製一次、存 secret manager、有懷疑就 rotate」這個迴圈內化，你 D3 secret hygiene 的考題基本上就過了。

---

## CCA Exam Relevance

- **D3（Claude Code Configuration）**：建立流程、key 放哪、怎麼恢復（不能恢復，只能 rotate）、為什麼。
- **D5（Enterprise Deployment）**：把 workspace 當成生產環境的考量——計費、稽核、rate limit 隔離。
- 考試觸發：「工程師弄丟了 API key」→ 答案永遠是「在 console 刪掉重建」，不是「聯絡 Anthropic 客服救回」。

---

## Flashcards

| Front | Back |
|-------|------|
| Anthropic API key 的明文值能看幾次？ | 只有一次，建立當下；之後不會再顯示 |
| 弄丟 key 要怎麼救？ | 救不回來；要到 console 刪掉再建一把新的 |
| 建立 API key 的五個步驟？ | 1) 登入 console.anthropic.com 2) Get API Keys 3) Create Key 4) 選 workspace 並命名 5) 立刻複製那個值 |
| `anthropic` SDK 會自動讀哪個環境變數？ | `ANTHROPIC_API_KEY` |
| `.gitignore` 應該加什麼來保護 key？ | `.env`（以及其他可能放到 key 的檔案） |
| 為什麼 Anthropic 建立後不保存明文 key？ | 這樣誰都沒辦法事後拿到它，包括 Anthropic 客服和攻擊者 |
| Workspace 在 key 管理中的用途？ | 計費、配額、用量報表的邊界；按環境或按產品分 |
| 安全的命名慣例？ | `<env>-<service>-<owner>-<date>`，例如 `prod-chatbot-backend-2025-04-11` |
