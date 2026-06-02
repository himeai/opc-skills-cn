---
name: opc-tangping
description: 一人公司「失败篇·彻底躺平」副驾驶（本地规则版）：个人现金流跑道 4 档红绿灯（绿/黄/橙/红）+ 失业金估算（10 城）+ 灵活就业养老 / 医疗社保金额 + 征信保护清单（must_do / avoid）+ 必保支出 / 可砍支出。Use when 用户提到躺平、彻底躺平、摆烂、失业金、低保、灵活就业社保、社保断缴、医保断缴、征信保护、个人现金流、跑道、月支出、降本、待业、空窗。
---

# 一人公司彻底躺平副驾驶（opc-tangping）

> 失败篇第四步：什么都不干，先把 6 个月跑道铺出来。
>
> 「人生的容错率大得可怕」不是鸡汤——你真的可以什么都不干，靠 灵活就业社保 + 失业金（如符合条件）+ 必砍支出 + 征信保护 撑半年到一年。这个 skill 把跑道月数算清楚，给出 4 档红绿灯，并对接 10 城失业金 / 灵活就业养老 / 医疗社保的实际金额范围。

> 本 skill 不做心态鸡汤、不嘲讽用户；不推荐 P2P / 网贷 / 高利贷；不做「逃废债」/「征信修复」/「断缴公积金套现」攻略；不爬抓任何招聘 / 平台数据。所有数据为本地静态规则，最终以当地人社 / 银行 / 司法窗口为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-tangping

# 杭州、月支出 8000、现金 30000、有房贷、雇员缴过 3 年
python3 scripts/runway.py "city=杭州|monthly_cost=8000|cash=30000|debt=0|has_house_loan=yes|was_employee=yes|prev_contribution_years=3"

# 上海、月支出 12000、现金 50000、有 5 万信用卡欠款、个独投资人
python3 scripts/runway.py "city=上海|monthly_cost=12000|cash=50000|debt=50000|has_house_loan=no|was_employee=no"

# 二三线、月支出 4000、现金 60000、想看灵活就业社保
python3 scripts/runway.py "city=西安|monthly_cost=4000|cash=60000|was_employee=no"
```

## Usage Examples

### 1. 跑道还剩多少？要不要立即上零工
```bash
python3 scripts/runway.py "city=杭州|monthly_cost=8000|cash=24000|debt=0|has_house_loan=yes|was_employee=no|prev_contribution_years=0"
```
输出：runway 3 个月（橙色警告）、个独投资人不可领失业金、灵活就业养老 1300-6500 元 / 月、医保 350-900 元 / 月、必砍支出与必保支出清单、立即 action list。

### 2. 之前是雇员，缴过失业保险
```bash
python3 scripts/runway.py "city=北京|monthly_cost=10000|cash=80000|debt=0|has_house_loan=no|was_employee=yes|prev_contribution_years=6"
```
输出：跑道 8 个月（黄色）+ 失业金每月约 1500-2500 元 + 最长可领 18-24 个月 + 灵活就业身份切换路径。

### 3. 真·躺平，月支出极低
```bash
python3 scripts/runway.py "city=西安|monthly_cost=4000|cash=60000|debt=0|has_house_loan=no|was_employee=no"
```
输出：跑道 15 个月（绿色）、二三线灵活就业养老 / 医疗参考、不需要立即上零工、长期建议。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/runway.py "<input>"` | 跑道 + 失业金 + 灵活就业社保 + 征信保护 | `city=...\|monthly_cost=...\|cash=...\|debt=...\|has_house_loan=<yes/no>\|was_employee=<yes/no>\|prev_contribution_years=...` | JSON |

## Scripts

### `scripts/runway.py`
- **职责**：跑道月数 + 4 档红绿灯（绿 ≥ 12 / 黄 6-12 / 橙 3-6 / 红 < 3）+ 失业金估算（10 城）+ 灵活就业养老 / 医疗社保金额 + 必保 / 可砍支出清单 + 征信保护 must_do / avoid
- **输入**：`city` / `monthly_cost` / `cash` / `debt` / `has_house_loan` / `was_employee` / `prev_contribution_years`
- **输出**：JSON `{runway_months, threshold, unemployment_benefit, flexible_insurance, credit_protection, must_keep, can_cut, action_list}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/personal_finance.json` — 10 城失业金 + 灵活就业养老 / 医疗 + 征信保护清单 + 跑道阈值

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad number` | `monthly_cost` / `cash` / `debt` 不是数字 | 传纯数字（不要带「元」「万」等单位） |
| 失业金 `eligible=false` | `was_employee=no` 或 `prev_contribution_years<1` | 个独 / 个体投资人本人通常不缴失业保险，不可领；建议改走灵活就业社保 |
| 城市未匹配 → 二三线参考 | 城市未列入 10 城清单 | 数据来自当地公开政策口径，未列入的统一走「二三线参考」近似值 |

## References

- 人社部《失业保险条例》
- 人社部《关于深入推进社会保险关系转移接续工作的通知》
- 中国人民银行《征信业务管理办法》
- 各地人社局公开政策

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何平台数据**
- 数据为公开政策口径，金额随社保基数 / 个人选择档次 / 城市动态变化，最终以当地人社窗口为准
- 涉及房贷断供 / 信用卡逾期 / 司法纠纷的复杂场景，请咨询持牌财务规划师 / 律师
- 主基调：**躺得心安理得**，不做黑色幽默
- See also：先注销公司见 [opc-shutdown](../opc-shutdown/SKILL.md)；想跑外卖回血见 [opc-dagong](../opc-dagong/SKILL.md)；想低成本试错见 [opc-baitan](../opc-baitan/SKILL.md)
