# Getting an API Key — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Claude Code Configuration (20%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 3.1（API key lifecycle）、3.2（workspace 与 key 命名）、5.3（生产环境 secret 卫生） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 05 |

---

## One-Liner

Anthropic 的 API key 是一张"写入后只能读一次"的 bearer credential，通过 Console 在指定的 workspace 下创建——它只会显示一次，没看到当下复制就永远拿不回来。

---

## 创建流程五步

```
Console 登录 ─▶ Get API Keys ─▶ Create Key ─▶ Workspace + 命名 ─▶ 只能复制一次
    1              2              3              4                 5
```

| 步骤 | 动作 | 备注 |
|------|------|------|
| 1 | 访问 `https://console.anthropic.com/` 并登录 | 用要负责计费与审计的账号 |
| 2 | 点 **Get API Keys**（dashboard 右上角） | 进到 key 管理页 |
| 3 | 点 **Create Key**（key 页右上角） | 打开创建对话框 |
| 4 | 选 workspace（例如 `Default`）并取名（例如 `Anthropic Course`） | 名字只是给人看的标识；workspace 才是计费/审计边界 |
| 5 | 立刻复制 | **这个值只会显示一次**；对话框关了就只能删了重建 |

"只能复制一次"这个规则不是 UX 小瑕疵，而是安全设计。Anthropic 创建后就不再存储明文 key，只保留 hash。**你丢了没人救得回来，反过来讲也没人能从客服工单把它偷走。**

---

## Workspace：隔离的单位

Workspace 是计费、rate limit、用量报表的边界。选对 workspace 是生产决策，不是装饰。

| Workspace 策略 | 适合谁 | 取舍 |
|---------------|-------|------|
| 一个产品一个 workspace | 干净的产品级计费与配额 | 工程师要切换 |
| 一个环境一个 workspace（dev/staging/prod） | 环境隔离、事故收敛 | 要管的 key 更多 |
| 共用 `Default` workspace | POC / 教学 | 不同项目之间无法归账 |

只要是认真在跑的生产 app，就像管 AWS account 一样管 workspace：**至少 prod/非 prod 分开。**

---

## Key 命名：一个小习惯省你一堆时间

名字是 free-form 的，只用来给人辨识。**早点立规矩：**

```
<env>-<service>-<owner>-<date>
prod-chatbot-backend-2025-04-11
dev-ingest-worker-2025-04-11
```

看到可疑账单或要 rotate key 的时候，名字是你在 console 里唯一的查询键。取成"My Key 3"会在事故时让你多花好几个小时。

---

## Key 在代码中的处理

Anthropic 的 SDK 会自动读环境变量 `ANTHROPIC_API_KEY`。这是 Lesson 06 会用到的 pattern，也是唯一可以接受的起手式：

```bash
# .env（绝对不要 commit）
ANTHROPIC_API_KEY="sk-ant-api03-...your-key..."
```

```python
# Python — SDK 会自己从环境变量抓
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()  # 不用显式传 key
```

Key 在代码中的铁律：

| 规则 | 原因 |
|------|------|
| 绝对不 commit `.env` | Public repo 会触发自动 revoke，private repo 也会从 fork 泄漏 |
| `.env` 一律加进 `.gitignore` | 双保险防止误 commit |
| 生产环境用 secret manager（AWS Secrets Manager、GCP Secret Manager、HashiCorp Vault） | 裸服务器的环境变量 POC 可以，但没审计轨迹 |
| 怀疑泄漏就立刻 rotate | Console 删旧 → 建新 → redeploy |
| 不要通过 chat/email/截图分享 | 必须分享就用密码管理器的 secure share |

---

## "key 丢失"工作流

因为值只会显示一次，恢复路径很明确：**不能恢复，只能 rotate。**

```
                ┌──────────────────┐
                │    key 丢了？     │
                └────────┬─────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    Console 找到                   Console 删掉
    那把 key                       那把丢失的 key
         │                               │
         └───────────────┬───────────────┘
                         ▼
                Console: Create Key
                （新的值，新的"只能复制一次"窗口）
                         ▼
                更新 .env / secret manager
                / redeploy
```

这也是按计划 rotate 的完全相同流程——**没有"拿回现有 key 的值"这个 API。**

---

## 代码示例：显式传 key（只能用在测试）

SDK 允许直接把 key 当参数传，但这只能用在丢弃式的脚本：

```python
from anthropic import Anthropic

# 只有 one-off notebook 或测试可接受，生产环境绝对不要
client = Anthropic(api_key="sk-ant-api03-...")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": "ping"}],
)
print(response.content[0].text)
```

这个 pattern 一旦离开 notebook 就变成地雷——一个手滑的 `git add .` 就把 key 推到 remote。

---

## Common Mistakes

1. **对话框还没复制就关掉** —— 值救不回来，只能删了重建。
2. **Key commit 进 git** —— 即使 private repo 也会从 fork、备份、未来开源泄漏。一律用环境变量。
3. **用"My Key"或"Test"当名字** —— 事故发生时你会不知道哪把 key 归哪个 service。
4. **Dev 和 prod 共用一个 workspace** —— Dev 失控的 job 会把你的生产配额抽干。
5. **从来不 rotate** —— Key 应该按计划过期（季度是合理 default），没用的 key 要删掉。

> **Key Insight**
>
> "只能复制一次"的对话框不是不方便——**它就是 API key 安全的根本原因。** 如果 Anthropic 之后还能给你看这个 key，那被盗号的攻击者也能。把"复制一次、存 secret manager、有怀疑就 rotate"这个循环内化，你 D3 secret hygiene 的考题基本上就过了。

---

## CCA Exam Relevance

- **D3（Claude Code Configuration）**：创建流程、key 放哪、怎么恢复（不能恢复，只能 rotate）、为什么。
- **D5（Enterprise Deployment）**：把 workspace 当成生产环境的考量——计费、审计、rate limit 隔离。
- 考试触发："工程师丢了 API key"→ 答案永远是"在 console 删掉重建"，不是"联系 Anthropic 客服恢复"。

---

## Flashcards

| Front | Back |
|-------|------|
| Anthropic API key 的明文值能看几次？ | 只有一次，创建当下；之后不再显示 |
| 丢了 key 要怎么救？ | 救不回来；要到 console 删掉再建一把新的 |
| 创建 API key 的五个步骤？ | 1) 登录 console.anthropic.com 2) Get API Keys 3) Create Key 4) 选 workspace 并命名 5) 立刻复制那个值 |
| `anthropic` SDK 会自动读哪个环境变量？ | `ANTHROPIC_API_KEY` |
| `.gitignore` 应该加什么来保护 key？ | `.env`（以及其他可能存 key 的文件） |
| 为什么 Anthropic 创建后不保留明文 key？ | 这样谁都没办法事后拿到它，包括 Anthropic 客服和攻击者 |
| Workspace 在 key 管理中的用途？ | 计费、配额、用量报表的边界；按环境或按产品分 |
| 安全的命名惯例？ | `<env>-<service>-<owner>-<date>`，例如 `prod-chatbot-backend-2025-04-11` |
