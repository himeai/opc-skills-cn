---
name: cn-angel
description: 中国天使轮融资副驾驶（本地规则版）：BP 10 页骨架生成、4 法估值平均与稀释表、Term Sheet 关键条款解读、投资人画像匹配、12 周融资时间表与 SLA 告警。完全本地推理，不替代律师 / FA / 投资顾问，不提供具体投资人联系方式，不构成投资意见。Use when 用户提到融资、天使轮、Pre-A、BP、商业计划书、估值、Term Sheet、TS、对赌、回购、反稀释、优先清算、投资人对接、FA、cap table、稀释、SPA、SHA、ODI、加速器。
---

# 中国天使轮融资副驾驶（cn-angel）

> 给 OPC / 一人公司 / 早期创业团队一个**本地可跑、不依赖任何融资 SaaS 账号**的融资工具箱：
> 出 BP 骨架、估算估值、解读 Term Sheet、匹配投资人画像、列融资时间表。
>
> **本 skill 不替代专业律师 / FA / 投资顾问**；估值仅作教学和谈判参考；Term Sheet 解读不构成法律意见；投资人匹配仅给类型与画像，**不提供具体机构 / 个人的联系方式**。

> 合规边界：本 skill 不爬抓 IT 桔子 / 36Kr / 烯牛数据等任何商业数据库；不替用户群发 BP；不替用户对接具体投资人；涉及对赌 / 个人无限连带 / 回购等高风险条款时主动给 ⚠️ 提示。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/cn-angel

# 1. 出 10 页 BP 骨架
python3 scripts/bp.py "industry=SaaS|stage=天使|model=订阅|north_star_metric=MRR|company=酱油科技|one_liner=AI Agent 客户成功平台|round_size_cny_w=600"

# 2. 估值（4 法平均 + 稀释表）
python3 scripts/valuation.py "stage=天使|industry=SaaS|round_size_cny_w=600|sc_team=1.3|sc_opportunity=1.2|sc_product=1.1|sc_competition=0.9|sc_channel=1.0|sc_extra=1.0|annual_rev_cny_w=120"

# 3. 解读 TS 单条款 / 全部条款
python3 scripts/ts.py "term=对赌"
python3 scripts/ts.py "term=all"

# 4. 投资人画像匹配
python3 scripts/match.py "industry=SaaS|stage=天使|round_size_cny_w=600|prefer=usd"

# 5. 12 周融资时间表
python3 scripts/timeline.py "start_date=2026-06-01|target_close_weeks=12"
```

## Usage Examples

### 1. 一个 SaaS 创始人准备首次出去融天使轮
1. `bp.py` 出骨架 → 拿到 SaaS 行业差异化要点（North Star = MRR、关键指标 NRR / Payback）
2. `valuation.py` 用 Scorecard + 行业倍数法估算 → 建议投前 800-1200 万
3. `match.py` → 推荐 美元 SaaS VC + 个人天使（KOL）+ CVC 三类
4. `timeline.py` → 12 周从首轮接触到 close

### 2. 拿到一份 TS，看不懂条款
- `ts.py "term=优先清算"` → 解释 1x 非参与是市场标准，超过 1.5x 应拒绝
- `ts.py "term=对赌"` → ⚠️ danger 级别，天使轮原则上拒绝
- `ts.py "term=all"` → 一次性导出 12 条核心条款逐项解读

### 3. 硬科技项目想找国资基金
- `match.py "industry=硬科技|stage=天使|round_size_cny_w=2000"` → 国资 / 政府引导 / 人民币 VC
- 输出含每类 persona 的关注点（落地纳税 / 产业目录 / 返投比例）

### 4. 估值落差较大想看不同稀释下的金额
- `valuation.py` 输出 `dilution_table`，给出投资人占 5%/8%/10%/12%/15%/18%/20% 时的 implied 投前估值

## Commands

| 命令 | 用途 |
|---|---|
| `python3 scripts/bp.py "<kv>"` | 生成 10 页 BP 骨架 + 行业差异化要点 |
| `python3 scripts/valuation.py "<kv>"` | 4 法估值平均 + 稀释表 + 阶段合理性 |
| `python3 scripts/ts.py "<kv>"` | TS 条款解读，市场标准 vs 激进 vs 谈判空间 |
| `python3 scripts/match.py "<kv>"` | 投资人画像匹配（仅类型 + 接洽建议） |
| `python3 scripts/timeline.py "<kv>"` | 12 周融资时间表 + SLA 告警 |

## Scripts

### `scripts/bp.py`

输入字段（`|` 分隔，`=` 键值）：

| 字段 | 说明 | 默认 |
|---|---|---|
| `industry` | SaaS / 消费 / 硬科技 / 文娱 / 教育 / 医疗 / 出海 / AI 应用 | `AI 应用` |
| `stage` | 种子 / 天使 / Pre-A | `天使` |
| `company` | 公司中文名 | `<公司中文名>` |
| `one_liner` | 一句话定位（≤ 25 字） | `<X 行业的 Y>` |
| `north_star_metric` | 北极星指标 | 由行业默认 |
| `round_size_cny_w` | 本轮金额（万元） | `<本轮金额>` |

输出：10 页 deck 骨架 + 每页 must_have / common_pitfalls + 行业差异化建议 + extra_pages 提示。

### `scripts/valuation.py`

支持四种估值法（提供任一法的输入即可，自动跳过未填法）：

- **Berkus**：5 项 0-1 打分，最高 1000 万
- **Scorecard**：6 项 0.5-1.5 加权，baseline = 800 万
- **VC 反推**：用 `projected_exit_cny_w` 反推
- **行业倍数**：用 `annual_rev_cny_w` × 行业 multiple

输出：每法估值 + 平均值 + 投后估值 + 稀释表（5%/8%/10%/12%/15%/18%/20%）+ 阶段合理性检查 + dilution_alert（healthy/caution/warning/danger）。

### `scripts/ts.py`

支持解读 12 条核心条款：优先清算 / 反稀释 / 回购 / 对赌 / 董事会席位 / 保护性条款 / ROFR_共同出售 / 拖售权 / 信息权 / 员工期权池 / 竞业限制 / 独家锁定期。

每条返回：market_standard / aggressive / negotiation_room / warn_level (low/medium/high/danger)。

### `scripts/match.py`

8 类投资人画像：美元 VC / 人民币 VC / CVC / 国资 / 个人天使 / FA / 加速器 / 盈利型小生意天使。

按 stage / industry / round_size 评分排序，**仅给类型 + ticket 区间 + 决策周期 + 关注点 + 接洽建议 + 红 flags**，不给具体机构 / 个人联系方式。

### `scripts/timeline.py`

12 周融资时间表（材料 → 接触 → 约见 → 深度访谈 → IC → TS → DD → SPA → 工商 → 打款 → close）。支持按 `target_close_weeks` 等比缩放。每节点有 deliverables + common_blockers + SLA 告警阈值。

## API Info

无外部 API。

## Troubleshooting

- **估值偏离阶段典型区间**：valuation.py 的 `sanity_check.in_typical_range = false` 时，意味着估值超出该阶段常见区间，需要更强 milestone 支撑。
- **稀释 alert = warning / danger**：本轮稀释超过 25% 后续融资会被卡，建议缩小本轮金额或上调估值。
- **match.py 无推荐**：检查 industry / stage 拼写是否在支持列表内。

## References

- `references/bp_templates.json`：10 页 deck skeleton + 8 大赛道差异
- `references/valuation_models.json`：4 估值法 + 阶段区间 + 稀释阈值
- `references/ts_clauses.json`：12 条 TS 关键条款
- `references/investor_personas.json`：8 类投资人画像
- `references/timeline_milestones.json`：12 周融资节点 + SLA

## Notes

- 本 skill 不替代律师起草 SPA / SHA / 章程；不替代税务师 / FA 服务
- 涉及个人无限连带责任 / 现金对赌 / Full-ratchet 反稀释 等条款，请务必由律师审查后再签
- 投资人匹配仅作类型导向，不替代真实尽调和合作判断
- 估值法假设来自公开经验数值，市场行情变化会导致区间漂移
