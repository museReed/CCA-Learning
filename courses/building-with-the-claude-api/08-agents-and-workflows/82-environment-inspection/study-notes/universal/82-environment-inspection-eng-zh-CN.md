# Environment Inspection — Engineering 深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架构)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 选型) |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 82 |

---

## 一句话总结

Claude 默认是"盲"的——有效的 agent 必须提供让它 **在行动前观察环境当前状态** 的 tools,而且每次变更后要重新观察,否则 Claude 会根据过时或想象出来的世界做决策。

---

## 为什么 Environment Inspection 重要

Agent 在自己看不见的 state 上做决策。LLM 没长眼睛看不到你的文件系统、没 hook 进数据库、也不知道按了按钮后到底发生什么事。没有 inspection tool,Claude 就是在猜现实。

Computer Use 是教科书级别的例子:**每次** Claude 执行动作(打字、点按钮),Anthropic runtime 立刻返回一张 screenshot。那个 screenshot 不是装饰——它是 Claude 把下一步"接地"到屏幕实际状态的方法。点一下可能开了 modal、可能切页、可能出错、也可能什么都没发生。没有 screenshot,Claude 根本没 signal。

这个 pattern 可以推广:如果你的 agent 对任何 state 做动作,它就必须有能力读到那个 state。

---

## 铁律:Read Before Write

Claude 变更任何东西之前,必须先读当前状态。听起来很明显,但一直有人违反。

**例子:在 Python 文件加一条 route**

```python
# BAD — Claude 凭空猜结构
edit_file("app.py", replace="last_line", with="@app.route('/new')...")

# GOOD — Claude 先读再编辑
current = read_file("app.py")
# Claude 推理:"这是 FastAPI,routes 在 20-45 行,imports 在最上面"
edit_file("app.py", old_string="...existing_route_block...", new_string="...with new route...")
```

Claude Code 把这条规则写进设计里:`Edit` tool 拒绝对"本次 session 没 `Read` 过的文件"操作。这不是礼貌——这是防止 Claude 用可能错误的假设去改文件。

---

## System Prompt Pattern for Inspection

你通过明确的 system prompt 指令引导 Claude 去做 inspection。以 video generation agent 为例:

```python
system_prompt = """
你是 video production agent。把任务视为完成前,你 **必须** 验证你的输出:

1. 用 `bash` 执行 whisper.cpp 对生成的视频产出带时间戳的 caption 文件。确认对白出现在预期时间点。
2. 用 `ffmpeg` 从视频每秒截一张图。逐张检查视觉元素是否符合 spec。
3. 把截图和 caption 对比原始需求。
4. 任何元素缺漏或错误,回去重生成该段再重新验证。

未完成这些验证步骤,绝对不能宣告任务完成。
"""
```

System prompt 把"验证输出"从模糊建议变成强制的 tool-calling 协议。没有这个,Claude 会按它 **预期** tool 产出什么就宣告成功。

---

## Inspection 的四大好处

| 好处 | 带来什么 |
|------|---------|
| **Progress tracking** | Claude 能衡量距离目标还有多远,而不只是执行步骤 |
| **Error handling** | 非预期输出当轮就能侦测并修正 |
| **Quality assurance** | Agent 在宣告"完成"前自我验证,抓出静默失败 |
| **Adaptive behavior** | Claude 根据观察到的结果调整策略,不只是按原计划走 |

没有 inspection = 盲眼执行器。有 inspection = feedback 驱动的 agent。

---

## 实作 Checklist

设计任何 agent tool 时,问:**"Claude 怎么知道这个动作成功了?"**

| 动作类型 | Inspection Tool |
|----------|-----------------|
| 文件写入/编辑 | 写入后 `read_file`;diff 对照预期输出 |
| UI 点击 / Computer Use | 每次动作自动 screenshot |
| HTTP API 调用 | 返回完整 response body + status code,不要只回 "ok" |
| 数据库写入 | Insert/update 后 read-back query |
| Shell 命令 | 返回 stdout + stderr + exit code |
| 影音生成 | Metadata 抽取 + keyframe screenshot + 转文字 |

Rule of thumb:**每个会变更状态的 tool 都该搭配一个观察 tool**,而且 system prompt 要明确叫 agent 两个都用。

---

## Code Pattern:Before and After Inspection

```python
system = """
你是 code refactoring agent。每次改文件都要:

1. 调用 `read_file` 加载当前内容。
2. 分析结构,找出该改什么。
3. 调用 `edit_file`,提供精确的 old_string / new_string。
4. **再次** 调用 `read_file` 验证改动应用正确。
5. 调用 `run_tests` 确认没弄坏东西。

步骤 4 或 5 失败就不要继续下一个改动——先把 regression 修好。
"""

tools = [read_file, edit_file, run_tests]
```

现在这个 agent 是 **grounded** 的——每个决策都基于新鲜的观察,不是基于三轮前对文件内容的假设。

---

## 常见错误

1. **Write-only tool** — 只给 `edit_file` 不给 `read_file`。Claude 没办法对看不到的文件做推理。
2. **Tool 响应过于精简** — API call 只回 `"ok"` 不回 response body。Claude 没数据可以用。
3. **依赖计划而非观察** — Claude 把自己之前的计划当成 ground truth。System prompt 必须强迫重新观察。
4. **变更后没 inspection** — Tool 没抛 exception 就当成功,用过时 state 继续跑。
5. **Computer Use 关掉 screenshot** — 为了省 cost 关掉自动截图,等于让 Computer Use 蒙眼操作。

> **Key Insight**
>
> Environment inspection 是把 Claude 从盲眼执行器变成 grounded agent 的关键。每个变更 tool 都要搭配观察 tool,system prompt 要让 inspection 变成强制而非可选。"Read before write, verify after write"是 agentic 系统里单一杠杆最高的可靠度 pattern。

---

## CCA 考试关联

- **D1 (Agentic Coding & Architecture)**:会考"为什么 Claude Code 改文件前要先读"、"为什么 Computer Use 自动回 screenshot"。答案是 grounding。
- **D5 (Enterprise Deployment)**:Production agent 的可靠度和 error handling 靠 inspection 内建在 tool set 里,而不是事后补。
- 考题关键字:"grounding""verify""observe""blindly execute"都指向 environment inspection。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 为什么 Computer Use 每次动作后都回 screenshot? | Claude 对环境是盲的—— screenshot 是它观察自己动作结果、把下一步接地的方法。 |
| Agent 变更 state 时该遵守什么规则? | Read before write——变更前先检视当前状态,变更后再检视一次验证。 |
| 为什么 Claude Code 要求 `Edit` 前先 `Read`? | 防止 Claude 根据假设改文件——它必须先观察真实内容。 |
| 举三个支持 environment inspection 的 tool response pattern。 | 返回完整 HTTP response + status、返回 stdout + stderr + exit code、DB 变更后 read-back query(任三)。 |
| 怎么在 agent 里强制 environment inspection? | 用 system prompt 指令明确要求每次变更动作前后都要调用特定 inspection tool。 |
| Environment inspection 的四大好处是什么? | Progress tracking、error handling、quality assurance、adaptive behavior。 |
| 设计 agent tool 时该问的唯一设计问题是什么? | "Claude 怎么知道这个动作成功了?" |
| 为什么 API tool 只回 `"ok"` 是烂设计? | Claude 没数据可以用——agent 没办法验证或调整,没有实际 response 内容。 |
