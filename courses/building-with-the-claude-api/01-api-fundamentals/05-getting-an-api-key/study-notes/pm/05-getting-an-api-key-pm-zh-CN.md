# Getting an API Key — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Claude Code Configuration (20%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 3.1（API key lifecycle）、3.2（workspace 策略）、5.3（生产环境 secret 卫生） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 05 |

---

## One-Liner

Anthropic API key 就是你 Claude feature 的信用卡——把创建、workspace 选择、rotation 当成产品问题（不只是 devops 的事），才不会在凌晨三点收到爆表账单或安全事故通知。

---

## Mental Model：银行保险箱的钥匙

Anthropic API key 就像银行保险箱的钥匙：

| 特性 | 保险箱钥匙 | Anthropic API Key |
|------|----------|-------------------|
| 只给一次 | 从银行拿回家 | 创建时只显示一次 |
| 不能恢复 | 丢了就钻开箱子换新的 | 丢了就删了重建 |
| 银行能验证但不能复制 | 银行只存 hash，不存钥匙 | Anthropic 只存 hash，不存明文 |
| 谁有谁就能用 | 进箱子不验身份 | 谁有 key 谁就能花你的预算 |

PM 的启示：**把 key 当现金处理**。你不会把实体现金放 repo 里——API key 也一样。

---

## 为什么 PM 该关心 key

| 关切点 | PM 影响 |
|------|--------|
| 成本归属 | 没有 workspace 纪律，你无法回答"Feature X 花了多少钱" |
| 安全事故 | Key 泄漏是真金白银的敞口，会出现在下个月的账单 |
| Launch 卡关 | 合规团队在企业 launch 前会问"key 存哪里" |
| 团队 onboarding | 新工程师需要 key，流程必须文档化且可审计 |
| 供应商审查 | 企业客户在采购阶段会问你的 key 管理 |

**没有 key 管理计划就推 Claude feature，等于推了一个伪装成 feature 的成本与安全负债。**

---

## Product Use Cases：Workspace 策略就是产品决策

### 一个产品一个 workspace

多个产品共用一个 Anthropic 账号、需要干净的产品级计费时用。

| 好处 | 代价 |
|------|------|
| "Product A 花了多少 Claude 钱"一目了然 | 工程师要在 console 切 workspace |
| 每产品配额可以防止互相抢资源 | 管理负担略增 |

### 一个环境一个 workspace

运营安全很重要时用（生产几乎都要）。

| 好处 | 代价 |
|------|------|
| Dev 失控的 loop 抽不到生产配额 | 要 rotate 的 key 变多 |
| 事故时 blast radius 很清楚 | 要监控的审计面更多 |

### 共用 Default workspace

只有 prototype 和教学才用。

| 好处 | 代价 |
|------|------|
| 零设置 | 没有成本归属；任何事故影响一切 |

---

## Key 生命周期：PM 检查清单

```
     创建
      │
      ▼
     复制一次 → 存 secret manager
      │
      ▼
     文档化：名字、所有者、用途
      │
      ▼
     用在 service → 监控用量/成本
      │
      ▼
     定期 rotate（季度）
      │
      ▼
     Service 退役时删掉
```

每一步都是产品问题：

| 步骤 | PM 责任 |
|------|--------|
| 创建 | 确保命名惯例存在并被遵守 |
| 存储 | PRD 里规定用 secret manager |
| 文档化 | 维护 key 库存（谁拥有什么） |
| 监控 | 不寻常开销的 dashboard |
| Rotate | 把每季 rotate 排成工程 ticket |
| 删除 | Feature 退役时有 decommission checklist |

---

## PM Decision Framework

新的 Claude feature 提案时跑这份问卷：

| 问题 | 默认答案 |
|------|---------|
| 这把 key 要放哪个 workspace？ | 专属的 per-feature 或 per-env workspace |
| 谁是这把 key 的人类所有者？ | Feature team 里指名的工程师，不是"整个 team" |
| 生产环境这把 key 存哪？ | Secret manager（不要放裸机器的环境变量） |
| 怎么 rotate？ | 每季，排定 ticket |
| 泄漏怎么知道？ | 账单异常告警 + GitHub secret scanning |
| 事故 playbook 是什么？ | Console 删掉 → 建新 → redeploy → post-mortem |

---

## Common PM Mistakes

1. **把 key 管理当成纯 devops 的事** —— 它是产品问题，因为它驱动成本归属、安全姿态、launch 就绪度。
2. **跳过命名惯例** —— 第一个事故打来时，"My Key 3"会让你花好几个小时当侦探。
3. **没排 rotation 的工时** —— Rotation 没排进 roadmap 就不会发生，排成每季。
4. **Dev 跟 prod 共用一个 workspace** —— 今天省十分钟，之后被失控账单打回来。
5. **没有事故 playbook** —— Key 泄漏时，team 在压力下临时想 rotate 步骤，浪费时间。

> **Key Insight**
>
> Key 管理不是小事——它是伪装成水电的产品设计决策。为 Claude feature 失眠的 PM，通常都是那些把 API key 当成"工程师的事"的人，然后被一个 4 万美金的 dev 失控账单或 public repo 泄漏事件狠狠教训。**把"workspace + key 计划"加进 feature launch checklist，就放在"隐私审查"旁边。**

---

## CCA Exam Relevance

- **D3（Claude Code Configuration）**：创建流程、存储模式、恢复路径（不能恢复，只能 rotate）。
- **D5（Enterprise Deployment）**：Workspace 作为计费/配额边界；key 卫生作为生产需求。
- 情境触发："Key 泄漏到 public repo" → Console 删掉、建新、redeploy、检讨怎么泄漏的。

---

## Flashcards

| Front | Back |
|-------|------|
| 为什么 PM 该关心 API key 管理？ | 它驱动成本归属、安全事故、企业 launch 就绪度 |
| Anthropic API key 的心智模型是什么？ | 保险箱钥匙——只给一次、不能恢复、银行只存 hash |
| "workspace 要选哪个"PM 默认答案是什么？ | 专属的 per-feature 或 per-env workspace，不是共用 Default |
| Key 库存要记什么？ | 名字、所有者（指名的人）、用途、workspace、rotation 日期 |
| Key 泄漏的正确事故处理是什么？ | Console 删掉 → 建新 → redeploy → post-mortem |
| 为什么季度 rotate 需要 PM 背书？ | 因为 rotation 没排进 roadmap 就不会发生 |
| Dev 跟 prod 共用一个 workspace 有什么问题？ | Dev 失控 loop 会抽干生产配额，造成客户事故 |
| PM 该在 feature launch checklist 加什么？ | Workspace + key 计划，和隐私与安全审查放一起 |
