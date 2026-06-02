---
name: opc-dagong
description: 一人公司「失败篇·打工」副驾驶（本地规则版）：10 家主流零工平台（外卖 / 网约车 / 跑腿 / 众包 / 家政）按 5 维加权打分排序，按城市 / 交通工具 / 五险需求 / 偏好类目筛选；估算日入；列出押金与门槛风险。Use when 用户提到打工、跑滴滴、送外卖、送快递、跑腿、众包、闪送、美团骑手、饿了么、达达、网约车、滴滴司机、副业打工、灵活用工、零工。
---

# 一人公司打工回血副驾驶（opc-dagong）

> 失败篇第二步：跑滴滴、送外卖、送快递。
>
> 没人会因为你跑过外卖看不起你。这个 skill 把美团 / 蜂鸟 / 达达 / 滴滴 / T3 / 曹操 / 闪送 / UU 跑腿 / 众包数据标注 / 58 天鹅家政 共 10 家主流平台，按 5 维（earn 35% · barrier 20% · insurance 20% · vehicle_fit 15% · stability 10%）加权打分，结合你的城市 / 交通工具 / 是否需要五险，给出排序后的可上手清单。

> 本 skill 不爬抓任何招聘 / 派单数据；不绕过任何平台规则；不教刷单 / 套保险等违规操作。所有数据为本地静态规则，最终以平台公告为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-dagong

# 杭州、电动车、想跑外卖、需要五险
python3 scripts/gig.py "city=杭州|wheels=电动车|hours_per_day=8|need_insurance=yes|prefer=外卖"

# 上海、私家车、想开网约车
python3 scripts/gig.py "city=上海|wheels=私家车|hours_per_day=10|need_insurance=no|prefer=网约车"

# 北京、无车、想做众包数据标注
python3 scripts/gig.py "city=北京|wheels=无车|hours_per_day=6|prefer=众包"
```

## Usage Examples

### 1. 短期上外卖
```bash
python3 scripts/gig.py "city=杭州|wheels=电动车|hours_per_day=8|need_insurance=no|prefer=外卖"
```
输出：美团骑手 / 饿了么蜂鸟 / 达达 排序、估算日入 200-360 元、入门门槛、押金风险提示。

### 2. 私家车开网约车
```bash
python3 scripts/gig.py "city=深圳|wheels=私家车|hours_per_day=10|need_insurance=yes|prefer=网约车"
```
输出：滴滴 / T3 / 曹操 排序、双证（人证 + 车证）门槛提示、平台抽成区间、合规警告（不允许刷单 / 套保险）。

### 3. 没有交通工具
```bash
python3 scripts/gig.py "city=北京|wheels=无车|hours_per_day=6|prefer=众包"
```
输出：众包数据标注 / 58 天鹅家政 等不依赖交通工具的选项，附时薪估算与备案要求。

### 4. 不限类目看全量打分
```bash
python3 scripts/gig.py "city=成都|wheels=电动车|hours_per_day=8|need_insurance=yes"
```
输出：10 家平台全量按综合分排序，附「为什么适合你」标签 + 警告标签。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/gig.py "<input>"` | 零工平台匹配排序 | `city=...\|wheels=<电动车/私家车/摩托车/无车>\|hours_per_day=...\|need_insurance=<yes/no>\|prefer=<外卖/网约车/跑腿/众包/家政>` | JSON |

## Scripts

### `scripts/gig.py`
- **职责**：按你的交通工具 / 五险需求 / 偏好类目，对 10 家主流平台按 5 维加权打分排序
- **维度权重**：earn 35% · barrier 20% · insurance 20% · vehicle_fit 15% · stability 10%
- **输出**：JSON `{ranked: [{name, score, estimated_daily_cny, entry_barrier, social_insurance, fit_reasons, warnings}], general_notes}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/gig_platforms.json` — 10 家主流零工平台 + 5 维评分权重 + 通用注意事项

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 未用 `key=value` 格式 | 用 `\|` 分隔多个字段，每个字段 `key=value` |
| 排序结果不带「适合你的交通工具」 | `wheels` 与平台要求的车型不匹配 | 切换交通工具或选 `prefer=众包/家政` 这类不依赖车的类目 |
| 「⚠️ 你需要五险但此平台不提供」 | `need_insurance=yes` 而平台只给意外险 | 切换 `prefer=家政` 或考虑灵活就业社保（见 opc-tangping） |

## References

- 人社部《新就业形态劳动者职业伤害保障管理办法》
- 各平台公开骑手 / 司机招募政策
- 国务院《关于支持多渠道灵活就业的意见》

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何平台数据**
- 估算时薪 / 抽成数据来自平台公告 + 公开报道，随地区 / 时段 / 单量动态变化
- 不推荐冲单刷量、不推荐套取意外险，平台违规直接封号
- See also：先注销公司见 [opc-shutdown](../opc-shutdown/SKILL.md)；想换轻资产创业见 [opc-baitan](../opc-baitan/SKILL.md)；要看跑道与失业金见 [opc-tangping](../opc-tangping/SKILL.md)
