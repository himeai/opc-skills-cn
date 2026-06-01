---
name: opc-experience
description: 一人公司「成功篇·体验解锁」副驾驶（本地规则版）：高净值体验全清单——南极游艇 / KTM 摩托环球 / 米其林三星巡礼 / 马拉松六大满贯 / 私人飞行执照 / 去太空（Virgin Galactic / Blue Origin / SpaceX × Axiom）/ 顶豪拍场 / 七大洲最高峰，按预算 + 体能 + 类别 + 年龄筛选；训练路径规划；合规与风险红线。Use when 用户提到高净值体验、人生清单、bucket list、人生体验、解锁、南极、北极、私人飞机、去太空、亚轨道、轨道飞行、Virgin Galactic、Blue Origin、SpaceX、米其林三星、World 50 Best、马拉松六大满贯、BMW6、Ironman、登山、珠峰、七大洲最高峰、F1、自由潜、米兰斯卡拉、佳士得拍场。
---

# 高净值体验解锁副驾驶（opc-experience）

> 一人公司「成功了」之后，第三件事是：不断解锁新的体验。
>
> 房子是壳，旅行是流，**体验才是会被记住一辈子的东西**。这个 skill 把一辈子可能想做的几十个高净值体验摊在桌上，按预算 + 体能 + 时间窗口告诉你——哪些今年就能做、哪些要训练 3-7 年、哪些要排队等飞船。本地规则推理，不替代体育 / 航空 / 法律 / 保险专业人士。

> 本 skill 不推荐具体俱乐部 / 教练 / 中介 / 拍卖行；不爬抓任何预订平台；不绕过任何外汇 / 出入境 / FAA / CCAR 规则。所有数据为公开静态规则，最终以官方 / 持牌专业人士为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-experience

# 1. 按 500w 预算 + 体能 4 + 35 岁筛选可解锁体验
python3 scripts/unlock.py "budget_cny=500w|fitness=4|categories=极地探险,极速极限,飞行航天|age=35|max_lead_months=24"

# 2. 太空旅行专项查询（去太空：亚轨道 / 轨道 / 月球）
python3 scripts/space.py "tier=suborbital"
python3 scripts/space.py "tier=orbital|budget_cny=5亿"
python3 scripts/space.py "tier=all"

# 3. 训练路径规划（六大满贯 / 珠峰 / 私人飞行执照 / 自由潜 / Ironman）
python3 scripts/train.py "goal=marathon_bmw6|current_fitness=3"

# 4. 合规与风险（含支付 / 保险 / 体检 / 法律红线）
python3 scripts/compliance.py "scope=payment,insurance,medical,legal|experience_id=space_suborbital"
```

## Usage Examples

### 1. 35 岁、刚卖了公司、500w 体验预算、想这两年就解锁

```bash
python3 scripts/unlock.py "budget_cny=500w|fitness=4|categories=极地探险,极速极限,飞行航天,顶级美食,体育成就|age=35|max_lead_months=24"
```

输出：南极包船 / 跳伞五大圣地 / F1 单座 / 米其林三星巡礼 / 北极破冰船 / KTM 环球 / PPL 私人飞行执照 等可立即启动项目；按预算 + lead 排序。

### 2. 想去太空（亚轨道）

```bash
python3 scripts/space.py "tier=suborbital"
```

输出：

- Virgin Galactic（VSS Unity，90 km）票价约 60w USD ≈ 435w CNY，3 天训练，FAA 商业宇航员之翼
- Blue Origin（New Shepard，107 km，越过卡门线）拍卖 / 邀约制
- 决策清单：体检 → 资金 → 训练 → 保险 → FAA 知情同意书

### 3. 想去 ISS 国际空间站

```bash
python3 scripts/space.py "tier=orbital"
```

输出：SpaceX × Axiom，单座 5500w USD ≈ 4 亿 CNY，6 个月封闭训练；附 Polaris Dawn / Roscosmos 现状。

### 4. 跑完六大满贯

```bash
python3 scripts/train.py "goal=marathon_bmw6|current_fitness=3"
```

输出：5 年训练路径（Y1 完赛 → Y2-3 抽中柏林 + 芝加哥 + 东京 + 伦敦 + 纽约 → Y4-5 BQ 波士顿）；体能 gap 提示。

### 5. 想登顶珠峰

```bash
python3 scripts/train.py "goal=everest|current_fitness=4"
python3 scripts/compliance.py "scope=insurance,medical|experience_id=everest_summit"
```

输出：3 年训练路径（玉珠峰 → 阿玛达布拉姆 → 卓奥友 → 珠峰）；高海拔保险 + 8000m 体检基线 + 死亡率 1% 风险提示。

### 6. 顶级拍场举牌

```bash
python3 scripts/unlock.py "budget_cny=5000w|fitness=1|categories=文化收藏|age=45"
python3 scripts/compliance.py "scope=legal|experience_id=auction_blue_chip"
```

输出：佳士得 / 苏富比 / 富艺斯 蓝筹艺术 / 当代 / 钟表夜场；KYC + 信托结构 + CRS 提示。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/unlock.py "<input>"` | 按预算 / 体能 / 类别 / 年龄筛选 60+ 体验 | `budget_cny=...\|fitness=1..5\|categories=...\|age=...\|max_lead_months=...` | JSON |
| `python3 scripts/space.py "<input>"` | 太空旅行（去太空）专项：亚轨道 / 轨道 / 月球 | `tier=suborbital/orbital/lunar_deepspace/all\|budget_cny=...` | JSON |
| `python3 scripts/train.py "<input>"` | 训练路径规划（6 个目标） | `goal=everest/ppl_us_faa/marathon_bmw6/freediving_pro/ironman/f1_grid\|current_fitness=1..5` | JSON |
| `python3 scripts/compliance.py "<input>"` | 支付 / 保险 / 医疗 / 法律红线 | `scope=payment,insurance,medical,legal\|experience_id=...` | JSON |

## Scripts

### `scripts/unlock.py`
- **职责**：从 60+ 体验主清单中按预算（含 1000w / 1 亿 / 50 亿区间）、体能 1-5、年龄窗口、最大 lead 月数过滤
- **输入**：`budget_cny` / `fitness` / `categories` / `age` / `max_lead_months`
- **输出**：JSON `{matched_count, by_category, tier_legend, fitness_legend, warnings}`

### `scripts/space.py`
- **职责**：太空旅行（去太空）专项；3 个层级（亚轨道 / 轨道 / 月球深空）+ 6 家提供商（Virgin Galactic / Blue Origin / SpaceX × Axiom / Polaris / Roscosmos / Boeing Starliner）
- **输入**：`tier` / `budget_cny`
- **输出**：JSON `{tiers, providers, decision_checklist, regulatory_notes, warnings}`

### `scripts/train.py`
- **职责**：6 个高净值目标的多年训练路径（珠峰 / PPL / 六大满贯 / 自由潜专业 / Ironman / F1 单座）
- **输入**：`goal` / `current_fitness`
- **输出**：JSON `{training, gap, gap_advice, current_baseline, target_baseline, license_table}`

### `scripts/compliance.py`
- **职责**：支付（5w 美元购汇 + 5 类违法方法红线）/ 保险（极地 / 高山 / 潜水 / F1 / 太空 6 类专项）/ 医疗（4 个高度梯度体检基线）/ 法律（信托 / CRS / 免责书）
- **输入**：`scope` / `experience_id`
- **输出**：JSON `{payment_compliance, insurance_required, medical_baseline, exit_entry, legal_redlines, ethics_caution, specific_insurance}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/experiences.json` — 8 大类 60+ 高净值体验主清单
- `references/space_travel.json` — 太空旅行专项数据（去太空）
- `references/training.json` — 6 个目标训练路径 + 资格证矩阵 + 5 档体能基线
- `references/compliance.json` — 支付 / 保险 / 医疗 / 法律 / 伦理红线

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 未用 `key=value` 格式 | 用 `\|` 分隔多个字段，每个字段 `key=value` |
| `error: bad number` | `budget_cny` / `fitness` / `age` 不是数字 | 数字 + 可带 `w/万/亿`（如 `500w` / `5亿`） |
| `matched_count` 为 0 | 预算 / 体能 / 类别过严 | 放宽 fitness 或扩大 categories 列表 |
| `goal '...' 未匹配` | training.json 未列入该目标 | 当前覆盖 6 个目标，可见 train.py 提示 |

## References

- 国家外汇管理局《个人外汇管理办法》—— 5 万美元年度购汇额度
- FAA 商业宇航员之翼标准（飞行高度 ≥ 80 km）
- 国际航空联合会 FAI 卡门线定义（100 km）
- IAATO 南极旅游运营商协会
- UIAA 国际登山协会高山向导认证
- abbottwmm.com 马拉松六大满贯认证

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何平台数据**
- 数据为静态参考；价格 / 排队 / 训练时长以官方公告为准
- 涉及私人飞机 / 太空旅行 / 顶豪艺术品 / 七顶峰的所有权 + 信托 + CRS + 遗产税请由家族办公室 + 持牌涉外律师设计
- 极限项目死亡率与风险真实存在（珠峰 ~1% / Titan 深潜事故 / F1 业余赛道事故）；本工具不替代体育 / 航空 / 医疗专业人士
- 主基调：**人生体验是可清单化的事情**，本地规则帮你把模糊的「想做」变成可执行的下一步
