---
name: opc-plan-b
description: 一人公司「下车—回血—再上路」副驾驶（本地规则版）：注销公司、跑外卖、摆摊、续社保、领失业金、半年后再上路，让你亲眼看见——人生的容错率大得可怕。Use when 用户提到破产、关门、注销、停业、下车、回血、外卖、摆摊、网约车、Plan B、东山再起、复业、失业金、社保断缴、个独注销、灵活就业、地摊。
---

# 一人公司 Plan B 副驾驶（opc-plan-b）

> 公司没了不等于你没了。
>
> 一人公司创业失败之后你会发现——**人生的容错率大得可怕**：外卖能跑、摊能摆、网约车能开、灵活就业社保能续、失业金能领、半年后照样能再开一家。
>
> 这个 skill 帮你把「下车—回血—再上路」每一步落到清单上。本地规则推理，不替代律师 / 税务师 / 心理咨询师，更不替你给爸妈打电话。

> 本 skill 不做心态鸡汤、不做黑色幽默、不嘲讽用户；不推荐 P2P / 网贷 / 高利贷；不做「逃废债」/「征信修复」攻略；不爬抓任何招聘 / 平台数据。所有数据为本地静态规则，最终以当地工商 / 税务 / 人社 / 城管窗口为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-plan-b

# 1. 公司体面下车清单（个体 / 个独 / 一人有限 / 有限公司）
python3 scripts/shutdown.py "entity=个独|location=杭州|has_employees=no|has_debt=no"

# 2. 个人现金流体检 + 失业金 + 灵活就业社保
python3 scripts/runway.py "city=杭州|monthly_cost=8000|cash=30000|debt=0|has_house_loan=yes|prev_contribution_years=3|was_employee=no"

# 3. 零工平台匹配（外卖 / 网约车 / 跑腿 / 众包 / 家政）
python3 scripts/gig.py "city=杭州|wheels=电动车|hours_per_day=8|need_insurance=yes|prefer=外卖"

# 4. 摆摊选品 ROI + 城市政策
python3 scripts/stall.py "city=成都|budget_cny=3000|category=小吃热食|night_or_day=night"

# 5. 复业决策树（建议先做完前 4 步再来）
python3 scripts/restart.py "runway_months=8|burnout=5|asset=技术能力|family=条件支持|gap_months=3|prev_industry=SaaS"
```

## Usage Examples

### 1. 个独刚关门，想知道注销要走多少步
```bash
python3 scripts/shutdown.py "entity=个独|location=杭州|has_employees=no|has_debt=no|has_abnormal=no"
```
输出：简易注销路径、5 步清单、典型 2-3 周完成、园区核定征收常见卡点。

### 2. 跑道还剩多少？要不要立即上零工
```bash
python3 scripts/runway.py "city=杭州|monthly_cost=8000|cash=24000|debt=0|has_house_loan=yes|was_employee=no|prev_contribution_years=0"
```
输出：runway 3 个月（橙色警告）、个独投资人不可领失业金、灵活就业养老 1300-6500 元 / 月、医保 350-900 元 / 月、必砍支出与必保支出清单、立即 action list。

### 3. 短期上外卖回血
```bash
python3 scripts/gig.py "city=杭州|wheels=电动车|hours_per_day=8|need_insurance=no|prefer=外卖"
```
输出：美团 / 蜂鸟 / 达达 排序、估算日入 200-360 元、入门门槛、押金风险提示。

### 4. 周末摆摊试试夜市
```bash
python3 scripts/stall.py "city=成都|budget_cny=3000|category=饮品冷食|night_or_day=night"
```
输出：成都开放夜市清单、饮品冷食毛利 60-80%、设备清单、健康证 + 备案卡要求、回本周期估算。

### 5. 半年后了，要不要再创业
```bash
python3 scripts/restart.py "runway_months=10|burnout=3|asset=技术能力|family=条件支持|gap_months=6|prev_industry=SaaS"
```
输出：「可以复业 / 并行模式 / 暂缓复业」决策、自由职业 / 一人 SaaS / 代运营 三条推荐路径、必须设的 4 项退出红线。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/shutdown.py "<input>"` | 公司注销路径与清单 | `entity=<个体/个独/一人有限/有限公司>\|...` | JSON |
| `python3 scripts/runway.py "<input>"` | 个人现金流体检 + 失业金 + 灵活就业社保 | `city=...\|monthly_cost=...\|cash=...\|...` | JSON |
| `python3 scripts/gig.py "<input>"` | 零工平台匹配排序 | `city=...\|wheels=...\|hours_per_day=...\|...` | JSON |
| `python3 scripts/stall.py "<input>"` | 摆摊选品 ROI + 政策 | `city=...\|budget_cny=...\|category=...\|...` | JSON |
| `python3 scripts/restart.py "<input>"` | 复业决策树 + 6 类轻资产复业方向 | `runway_months=...\|burnout=...\|asset=...\|...` | JSON |

## Scripts

### `scripts/shutdown.py`
- **职责**：根据主体类型 + 是否有员工 / 债务 / 异常状态，返回简易 / 普通注销路径与详细步骤
- **输入**：`entity` / `location` / `has_employees` / `has_debt` / `has_abnormal`
- **输出**：JSON `{entity, recommended_path, steps, typical_weeks, common_blockers, extra_warnings}`

### `scripts/runway.py`
- **职责**：跑道月数 + 4 档危险阈值（绿/黄/橙/红）+ 失业金估算 + 灵活就业社保金额 + 必保 / 可砍支出清单 + 征信保护清单
- **输入**：`city` / `monthly_cost` / `cash` / `debt` / `has_house_loan` / `was_employee` / `prev_contribution_years`
- **输出**：JSON `{runway_months, threshold, unemployment_benefit, flexible_insurance, credit_protection, action_list}`

### `scripts/gig.py`
- **职责**：根据交通工具 / 五险需求 / 偏好类目，对 10 家主流平台按 5 维加权打分排序
- **维度权重**：earn 35% · barrier 20% · insurance 20% · vehicle_fit 15% · stability 10%
- **输出**：JSON `{ranked: [{name, score, estimated_daily_cny, fit_reasons, warnings}]}`

### `scripts/stall.py`
- **职责**：10 城地摊政策 + 5 大品类（小吃热食 / 饮品冷食 / 文创手作 / 二手好物 / 轻服务）选品 + ROI 估算 + 设备清单 + 备案要求
- **输出**：JSON `{city_policy, category_overview, roi_estimate_low, roi_estimate_mid, equipment_checklist, license_required}`

### `scripts/restart.py`
- **职责**：4 维决策树（跑道 / 心力 / 资产 / 家庭）→「可以复业 / 并行模式 / 暂缓复业」3 档判断 + 6 类轻资产复业方向 + 退出红线
- **输出**：JSON `{decision, recommended_paths, exit_red_lines, action_list}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/entity_shutdown.json` — 4 类主体注销流程
- `references/gig_platforms.json` — 10 家主流零工平台
- `references/stall_policies.json` — 10 城地摊政策 + 5 大品类
- `references/personal_finance.json` — 失业金 + 灵活就业社保数据
- `references/comeback_paths.json` — 6 类轻资产复业方向 + 决策树

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 未用 `key=value` 格式 | 用 `\|` 分隔多个字段，每个字段 `key=value` |
| `error: bad number` | `monthly_cost` / `cash` / `runway_months` 不是数字 | 传入纯数字（不要带「元」「万」等单位） |
| 城市未匹配 → 二三线参考 | 城市未列入 10 城清单 | 数据来自当地公开政策口径，未列入的统一走「二三线参考」近似值 |

## References

- 国务院《关于推动「夜经济」高质量发展的指导意见》
- 人社部《失业保险条例》
- 国家税务总局《市场主体登记管理条例》
- 各地市监 / 城管 / 人社局公开政策

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何平台数据**
- 数据来自公开政策与平台公告，最新口径请以当地窗口为准
- 涉及个人征信 / 债务 / 司法纠纷的复杂场景，请聘请律师 / 持牌财务规划师
- 主基调：**体面下车 + 快速回血**，不是黑色幽默
- 已知限制：未覆盖港澳台地区主体注销路径；未覆盖跨境网约车 / 海外零工平台
