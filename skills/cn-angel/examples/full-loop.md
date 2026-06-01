# 例：天使轮融资全链路（BP → 估值 → TS → 投资人 → 时间表）

## 场景
你是一个 SaaS 创业团队，想出去融天使轮 600 万。从准备 BP 到 close 的全流程演练。

## 步骤

### 1) 出 10 页 BP 骨架
```bash
python3 scripts/bp.py "industry=SaaS|stage=天使|north_star_metric=MRR|company=酱油科技|one_liner=AI Agent 客户成功平台|round_size_cny_w=600"
```
拿到 deck 骨架，开始填实际内容（封面、痛点、产品、数据、团队…）。

### 2) 估值（Scorecard + 行业倍数法）
```bash
python3 scripts/valuation.py "stage=天使|industry=SaaS|round_size_cny_w=600|sc_team=1.3|sc_opportunity=1.2|sc_product=1.1|sc_competition=0.9|sc_channel=1.0|sc_extra=1.0|annual_rev_cny_w=120"
```
输出参考：
- `pre_money_avg_cny_w`: 1140 → 投前估值约 1140 万
- `dilution_table`: 投资人占 5% 对应投前 1.14 亿，占 12% 对应 4400 万…
- `dilution_alert`: `healthy`（投前 1140 + 600 = 投后 1740，本轮稀释 34%，超过 healthy_max 20% → 实际会被警告 `danger`）
- 调整：把 round_size 降到 300，或上调估值

### 3) 投资人画像匹配
```bash
python3 scripts/match.py "industry=SaaS|stage=天使|round_size_cny_w=600|prefer=usd"
```
输出（top 推荐）：
- 美元 VC（ticket 800-5000 万，决策 4-8 周）
- CVC 战略（ticket 1000-8000 万，决策 8-16 周）
- 个人天使（ticket 50-500 万，决策 1-4 周）

按 score 排序后，自己去公开渠道（IT 桔子 / 公众号 / 朋友圈）筛具体名单。

### 4) 拿到一份 TS，逐条解读
```bash
python3 scripts/ts.py "term=优先清算,反稀释,回购,对赌"
```
对每条返回：
- `market_standard`：市场惯例（这一档可签）
- `aggressive`：常见激进版（对创始人不利）
- `negotiation_room`：谈判建议（哪些可让，哪些必须守）
- `warn_level`：low / medium / high / danger（红线条款警告）

如果 TS 出现「现金对赌 + 个人无限连带回购」直接看到 `danger`，建议拒签或重谈。

### 5) 排融资 12 周时间表
```bash
python3 scripts/timeline.py "start_date=2026-06-01|target_close_weeks=12"
```
输出每周的 deliverables、common_blockers 和 SLA 告警阈值（如：到第 4 周还没有 partner 复谈，要复盘 BP）。

## 关键 takeaway

1. **估值不要一次到位**：4 法平均 + 阶段合理性检查；偏离过多投资人会立刻 NO
2. **稀释 ≤ 20% 是健康线**：超过 25% 下一轮就被卡
3. **TS 红线条款优先死守**：对赌、个人无限连带、Full-ratchet 反稀释、3 年回购
4. **投资人匹配先看 ticket size 适配**：本轮 600 万，找单笔 50-200 万的 FA 是浪费时间
5. **时间预算 ≥ 12 周**：DD 阶段经常卡 2-4 周；境外架构 ODI 备案再加 4-8 周

## 合规提醒

- 本 skill **不替代律师 / FA / 税务师**
- 不提供任何具体投资人 / 机构 / 个人联系方式
- TS / SPA / SHA / 章程 必须由专业律师起草和审查
- 涉及对赌 / 个人连带 / 重组等条款，请务必先做法律 + 税务双重审查
