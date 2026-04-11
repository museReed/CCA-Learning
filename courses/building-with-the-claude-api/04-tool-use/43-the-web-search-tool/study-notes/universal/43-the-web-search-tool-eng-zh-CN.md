# Web Search Tool — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D4 — AI Safety & Alignment (20%) |
| Task Statements | 2.3（built-in server tools）、2.1（tool schema）、4.2（grounding 与 citation） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 43 |

---

## One-Liner

Web search tool 是 Anthropic 完全托管的 server tool:你只需要给一个很小的 schema stub,Anthropic 会在他们的服务器上处理整个搜索、结果抓取、citation 生成——完全不需要你的本地实现。

---

## 关键区分：Server Tool vs. Client-Executed Tool

不同于自定义 tool（schema 与实现都你写）或 text editor tool（Claude 知 schema、你执行指令）,web search tool 是 **server tool**：

| Tool 类型 | 谁定义 Schema | 谁执行 |
|-----------|---------------|-------|
| 自定义 tool | 你 | 你 |
| Text editor（built-in） | Anthropic | 你 |
| Web search（server tool） | Anthropic | **Anthropic** |

Runtime 你什么都不用做。Claude 向 Anthropic 的 web search 后端发出调用,结果通过 API response 回来。

---

## 前置条件：在 Console 启用

使用 web search 前,你的 Anthropic 组织必须在 privacy 设置启用它：

```
https://console.anthropic.com/settings/privacy
```

这是 org level 的 opt-in。若设置是关的,包含 web search tool 的请求会失败。PM 请把它视为任何会用到此 tool 的环境 deployment checklist 的一项。

---

## 声明 Tool

Schema stub 有三个必填字段：

```python
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
}
```

| 字段 | 含义 |
|------|------|
| `type` | Versioned 的 server tool 标识符,必须对应你使用的模型版本 |
| `name` | 固定为 `web_search` |
| `max_uses` | 每个请求的搜索次数上限 |

`max_uses` 上限很重要,因为 Claude 可能会根据初步结果发**后续搜索**。一个用户问题可能随着 Claude 精炼理解而变成三、四次查询。`max_uses` 就是你的成本与延迟天花板。

---

## 限制搜索域名

可以用 `allowed_domains` 限制哪些域名可搜索：

```python
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["nih.gov"],
}
```

使用场景：

- **医疗建议** → 限 PubMed / NIH 获得循证来源
- **法律研究** → 限 `.gov` 或 `.edu` 域名
- **公司专属数据** → 限公司官网
- **学术** → 限同行评审来源

Domain 限制不只是过滤搜索,更是你控制**内容质量与信任**的主要杠杆。

---

## Response Block 类型

启用 web search 的 response 除了一般 text,还会包含几种新的 block：

| Block 类型 | 用途 |
|------------|-----|
| `text` | Claude 的普通解释文本 |
| `ServerToolUseBlock` | 显示 Claude 实际下的搜索 query |
| `WebSearchToolResultBlock` | 包含完整搜索结果 |
| `WebSearchResultBlock` | 单条结果（title + URL + snippet） |
| Citation block | 来自来源、支撑 Claude 陈述的逐字引用 |

因为执行是 server-side 的,`ServerToolUseBlock` 与 `WebSearchToolResultBlock` 会在同一个 response 中一并返回——不需要做第二次 round trip。

```python
for block in response.content:
    if block.type == "text":
        render_text(block.text)
    elif block.type == "server_tool_use":
        log_query(block.input["query"])
    elif block.type == "web_search_tool_result":
        render_source_list(block.content)
```

---

## Citation 与 Grounding

Claude 会用 **citation block** 标注文本输出,内容包括：

- 来源域名与页面标题
- 来源 URL
- 支撑该陈述的具体引用文字

这让 grounded generation 真正可行:用户可以点击到来源验证任何陈述。它也给你一个产品界面——"来源"面板——相较于没有 grounding 的 LLM 回应,信任感大幅提升。

---

## 渲染模式

Response 的 block 类型对应特定 UI 元件：

1. **Text block** → 主回答区的常规内容
2. **Web search result block** → "来源列表",通常放在回答上方或侧边
3. **Citation block** → 行内徽章或 footnote,显示来源域名与页面标题,可外链

把每种 block 视为不同的 UI 槽,不要合并成一个字符串。

---

## 什么时候用 Web Search Tool

Lesson 指出四个主要场景：

- **时事** — 超出模型训练 cutoff 的信息
- **专门信息** — 不在 Claude 训练数据中的
- **事实核查**与权威来源
- **研究工作**需要最新信息

你只要把 schema 加入 tools 数组,Claude 会自动判断是否要搜索。不需要特别指示 Claude 用它,模型会根据问题内容自己决定。

---

## 成本与延迟

- 每次搜索都会增加延迟（服务器要 fetch、parse、返回结果）
- `max_uses` 决定每个请求的搜索次数上限——按使用场景价值设置
- Domain 限制可以缩小搜索面、加快速度
- Streaming 依然可用;search block 会沿同一个事件序列 stream

高流量 production 使用时请埋点：

- 每请求的平均搜索次数（注意是否上漂）
- 启用 search vs. 不启用的首个 text token 时间
- Citation 点击率（用户对来源的信任信号）

---

## Common Mistakes

1. **忘记在 console 启用 web search** — 请求会静默失败或报错;请先检查 org 设置。
2. **`max_uses` 设太高** — 在推测性问题上的失控搜索链会让成本与延迟翻倍。
3. **没渲染 citation** — 失去 server tool 最大的产品优势:可验证、有 grounding 的答案。
4. **敏感主题没用 `allowed_domains`** — 医疗、法律、财务主题从权威来源限制中受益极大。
5. **当 server tool 就够用时还自己实现 web search** — 重新实现意味着更多代码、更差的 citation、也没有内置的 rendering block。

> **Key Insight**
>
> 像 web search 这样的 server tool 是最快把"需要新鲜或权威数据"的 production 级 AI 功能上线的路径。你出一个 schema stub,Anthropic 出整个执行、解析、citation pipeline。你唯一要写的代码是渲染 response block 的 UI。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 web search 是"server tool"——Anthropic 执行调用,你不提供任何本地函数。
- **D4 (AI Safety & Alignment)**：Citation 与 grounding 是关键的信任功能,考题会测"无 grounding 的 LLM 输出"vs."带 citation 的答案"。
- 题目常对比:自定义 tool（两者都要）、text editor（只给 schema）、web search（什么都不用——完全托管）。

---

## Flashcards

| Front | Back |
|-------|------|
| "server tool"与 text editor tool 的差别？ | Server tool 完全由 Anthropic 的基础设施执行——你不提供任何本地函数 |
| Web search schema stub 需要哪些字段？ | `type`（versioned）、`name`（`web_search`）、`max_uses` |
| `max_uses` 控制什么？ | 单一请求中 Claude 能执行的最大搜索次数（控成本 / 延迟） |
| 如何限定搜索到特定域名？ | 在 schema 里设 `allowed_domains`,比如 `["nih.gov"]` |
| 使用 web search 前必须在 Anthropic console 做什么？ | 在 privacy 设置中启用 web search tool |
| 列出 web-search response 中的三种新 block 类型。 | `ServerToolUseBlock`、`WebSearchToolResultBlock`、`WebSearchResultBlock`,以及 citation block |
| Citation block 的目的是什么？ | 引用支撑 Claude 陈述的具体来源文字,实现 grounded、可验证的答案 |
| 什么时候 PM 会选 web search tool 而不是自定义搜索集成？ | 需要新鲜 / 权威数据、又想不自己实现就拿到自动 citation 与 grounding 时 |
