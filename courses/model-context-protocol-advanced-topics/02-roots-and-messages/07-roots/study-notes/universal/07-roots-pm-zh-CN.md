# Roots — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.2 (MCP security model), 2.3 (MCP server capabilities) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 07 |

---

## One-Liner

Roots 是 MCP 告诉 server「你可以看这里，只有这里」的方式 — 同时解决文件发现的易用性问题和无限制访问的安全问题。

---

![Roots Access](../../visuals/roots-access-zh-TW.svg)


## 心智模型：大楼门禁卡

把 roots 想成办公大楼的门禁卡：

| 概念 | 大楼类比 | MCP 对应 |
|------|---------|----------|
| Root | 门禁卡授权进入 3 楼和 7 楼 | Client 说「你可以访问 /projects 和 /data」 |
| 有 roots 的 Server | 持卡员工 | Server 知道要搜索哪些目录 |
| 没有 roots 的 Server | 没卡的访客 | 必须询问确切房号（完整文件路径） |
| Enforcement | 每层楼的闸门 | `is_path_allowed()` 函数（必须自建） |

关键洞察：**门禁卡本身不锁门** — 闸门才锁。同样地，roots 告诉 server 该去哪里，但 enforcement 必须另外实现。

---

## Roots 解决的两个问题

### 问题 1：易用性

没有 roots 时，用户必须提供确切路径：
- 「读取 `/Users/reed/Documents/projects/my-app/src/components/Header.tsx`」

有 roots 时，用户只需说：
- 「读取 Header.tsx」

Server 知道要在核准的目录内搜索。

### 问题 2：安全性

没有 roots 时，MCP server 可能访问系统上任何文件：
- 个人文档、SSH key、含密码的环境文件

有 roots 时，server 的范围被限制在核准的目录。

> **Key Insight**
> Roots 解决的问题和 Google Drive 或 Dropbox 的「文件夹权限」相同 — 定义工具可以看到的边界。作为 PM，如果你的产品处理文件，roots 就是实现最小权限访问的机制。

---

## 流程说明（无代码）

1. **Client 声明 roots**：「这个 server 可以访问我的项目文件夹和数据文件夹」
2. **Server 发现 roots**：「我有两个目录的访问权 — 让我在那里搜索」
3. **用户发出请求**：「找到配置文件」
4. **Server 在 roots 内搜索**：先看项目文件夹，再看数据文件夹
5. **Server 找到并使用文件**：返回配置文件内容

用户从不需要打完整路径。Server 从不看核准目录以外的地方。

---

## 关键安全缺口

这是 PM 必须传达给工程团队的最重要细节：

**MCP SDK 不会自动强制 root 边界。**

SDK 提供核准 roots 的清单。但技术上没有任何机制阻止 server 忽略清单而访问其他文件。你的工程团队必须自建 enforcement。

| SDK 提供的 | 团队必须建的 |
|-----------|------------|
| Root 发现机制 | 访问控制验证 |
| 核准目录清单 | Path traversal 防护 |
| 标准 URI 格式 | Symlink 解析 |

**PM 行动项**：在 PRD 中明确要求访问文件的 tool 必须实现路径验证。不要假设 SDK 会处理。

---

## 产品情境

### 情境 1：Code Review 工具

Code review MCP server 需要读取源代码。没有 roots 时：
- 用户必须为每个文件贴上完整路径
- Server 可能意外读取含 API key 的 `.env` 文件

有 roots 时：
- Client 将 server 指向 repository root
- Server 在 repo 内自然搜索
- Repo 外的文件不可访问（有 enforcement 时）

### 情境 2：多项目工作空间

开发者同时做三个项目。Client 配置三个 roots：
- `/projects/frontend`（React app）
- `/projects/backend`（Python API）
- `/projects/shared`（共用库）

Server 可以跨三个项目搜索，用户不需切换上下文。

---

## PM 安全检查清单

审查访问文件的 MCP tool 设计时，确认：

- [ ] Server 在访问文件前调用 `list_roots()`
- [ ] 路径验证函数存在（`is_path_allowed()`）
- [ ] Path traversal 攻击有处理（解析 `..` 和 symlinks）
- [ ] 被拒绝的访问尝试有记录
- [ ] 用户可以查看和修改 root 配置

---

## CCA Exam Relevance

- **D2 Task 2.2**：MCP 安全模型 — roots 是文件系统安全机制
- **D2 Task 2.3**：Server capabilities — 理解 `list_roots()` 如何启用文件发现
- 预期情境题：「Server 访问了核准 roots 外的文件。哪里出了问题？」答：enforcement 未实现
- 核心考试哲学：**Validation > Trust** — SDK 默认信任 server；你的代码必须加上验证

---

## Flashcards

| Front | Back |
|-------|------|
| MCP roots 解决哪两个问题？ | 易用性（不需完整路径）和安全性（限制 server 访问核准的目录） |
| MCP SDK 会自动阻止 server 访问 roots 外的文件吗？ | 不会 — SDK 提供 root 清单但不强制边界；开发者必须实现验证 |
| PM 对 roots 的关键行动项是什么？ | 在 PRD 中明确要求路径验证 — 不要假设 SDK 会处理 |
| Roots 的安全类比是什么？ | 大楼门禁卡 — 告诉你可以去哪，但闸门（enforcement code）必须另外建 |
| Roots 如何改善用户体验？ | 用户说「找配置文件」而非打完整路径 — server 在核准目录内搜索 |
| Client 可以配置多个 roots 吗？ | 可以 — 例如同时指向多个项目目录 |
| Roots 最大的安全风险是什么？ | Server 收到 roots 但不验证路径 — path traversal 攻击可逃出 root 边界 |
| 哪个考试哲学适用于 roots？ | Validation > Trust — 不要假设 server 会自我限制；加上程序化 enforcement |
