---
name: opc-baitan
description: 一人公司「失败篇·摆摊」副驾驶（本地规则版）：10 城（上海 / 北京 / 广州 / 深圳 / 成都 / 杭州 / 重庆 / 武汉 / 西安 / 长沙）夜市政策 + 5 大品类（小吃热食 / 饮品冷食 / 文创手作 / 二手好物 / 轻服务）选品 + ROI 估算 + 设备清单 + 备案要求。Use when 用户提到摆摊、摆地摊、地摊、夜市、烤肠、小吃车、文创、饮品、集市、早市、路边摊、二手、街头创业、夜经济。
---

# 一人公司摆摊回血副驾驶（opc-baitan）

> 失败篇第三步：低成本试错，先把现金流跑起来。
>
> 烤肠、关东煮、咖啡、文创、二手——一辆推车 + 几千块就能开张。这个 skill 把全国 10 城的夜市开放政策（合规摆点 / 备案 / 占道许可）、5 大品类的起步成本与典型毛利率、设备清单、健康证 / 备案卡要求摊在桌上，按你的城市 + 预算 + 品类直接给出能上手的最小可行摊位。

> 本 skill 不教逃避城管 / 占用消防通道 / 黑摊位等违规做法；不爬抓任何平台数据；不替你跑健康证 / 占道许可。所有数据为本地静态规则，最终以当地市集运营方与城管 / 卫健窗口为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-baitan

# 上海、3000 元预算、卖烤肠 / 关东煮
python3 scripts/stall.py "city=上海|budget_cny=3000|category=小吃热食|night_or_day=night"

# 成都、5000 元预算、卖手打柠檬茶
python3 scripts/stall.py "city=成都|budget_cny=5000|category=饮品冷食|night_or_day=night"

# 北京、2000 元预算、卖手作 / 文创
python3 scripts/stall.py "city=北京|budget_cny=2000|category=文创手作|night_or_day=day"
```

## Usage Examples

### 1. 卖烤肠（最低门槛小吃）
```bash
python3 scripts/stall.py "city=上海|budget_cny=3000|category=小吃热食|night_or_day=night"
```
输出：上海开放夜市清单 + 小吃热食典型毛利率 + 起步成本 + 设备清单（不锈钢操作台 + 煤气罐 + 餐厨垃圾签约）+ 必备健康证 + ROI 低 / 中场景对比。

### 2. 周末饮品冷食摊
```bash
python3 scripts/stall.py "city=成都|budget_cny=4000|category=饮品冷食|night_or_day=night"
```
输出：成都夜市开放点位 + 饮品冷食毛利 60-80% + 制冰机 / 搅拌器 / 一次性杯具清单 + 备案卡要求 + 回本周期估算。

### 3. 文创手作走集市
```bash
python3 scripts/stall.py "city=北京|budget_cny=2000|category=文创手作|night_or_day=day"
```
输出：北京周末市集运营方清单 + 文创品类典型客单 + 起步成本最低区间 + 不需要健康证的备案路径。

### 4. 二手好物摊
```bash
python3 scripts/stall.py "city=深圳|budget_cny=500|category=二手好物|night_or_day=day"
```
输出：深圳跳蚤市场 / 二手集市点位 + 起步成本最低 + 客单与定价区间 + 注意事项（避免假货 / 三无产品）。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/stall.py "<input>"` | 摆摊选品 + 城市政策 + ROI | `city=...\|budget_cny=...\|category=<小吃热食/饮品冷食/文创手作/二手好物/轻服务>\|night_or_day=<night/day>` | JSON |

## Scripts

### `scripts/stall.py`
- **职责**：按城市政策匹配开放点位，按品类返回起步成本 / 毛利 / 单量典型值，按预算给出 ROI 低 / 中两档估算
- **输出**：JSON `{city_policy, category_overview, suggested_picks, budget_check, roi_estimate_low, roi_estimate_mid, equipment_checklist, license_required, general_warnings}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/stall_policies.json` — 10 城夜市政策 + 5 大品类（含烤肠、关东煮、煎饼果子等小吃热食示例）+ 起步成本 + 资质要求

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad budget_cny` | 预算字段不是数字 | 传纯数字，不要带「元」/「万」单位 |
| `in_budget=false` | 预算低于该品类起步成本下限 | 选低门槛品类（二手好物 / 轻服务）或加预算 |
| 城市未匹配 | 城市未列入 10 城清单 | 模糊匹配兜底为「成都」，建议显式写明 |

## References

- 国务院《关于推动「夜经济」高质量发展的指导意见》
- 各地《城市道路管理条例》/ 占道经营许可办法
- 各地市集运营方公开招商公告

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何平台数据**
- 数据为公开政策与运营方公告，最新口径请以当地城管 / 市集窗口为准
- 涉及食品安全 / 食材进货 / 健康证的环节请按《食品安全法》合规办理
- 已知限制：未覆盖二线以下城市；未覆盖跨境 / 网红快闪点位
- See also：先注销公司见 [opc-shutdown](../opc-shutdown/SKILL.md)；想跑外卖见 [opc-dagong](../opc-dagong/SKILL.md)；要看跑道与失业金见 [opc-tangping](../opc-tangping/SKILL.md)
