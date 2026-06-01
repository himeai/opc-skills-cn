---
name: opc-travel
description: 量身定制环球旅行副驾驶（本地规则版）：根据主题 / 时长 / 预算 / 出发月份生成路线，覆盖 80+ 国 200+ 城市，4 档预算（穷游 / 舒适 / 商务 / 奢华）、中国普通护照签证矩阵、月份反查目的地、跨气候打包清单。Use when 用户提到环球旅行、Round the World、长途旅行、签证规划、出行预算、欧洲游、亚洲游、北美游、南美游、非洲游、大洋洲游、极地、南极、北极、米其林之旅、海岛、潜水、极光、行李清单、最佳季节、间隔年、gap year。
---

# 量身定制环球旅行副驾驶（opc-travel）

> 一人公司「成功了」之后，第二件事就是世界。
>
> 这个 skill 帮你把模糊的「想环球旅行」变成可执行的清单：去哪、什么时候去、签证什么时候办、要花多少钱、要带什么。本地规则推理，不替代签证中心 / 持牌旅行社。

> 本 skill 不推荐具体航空公司 / 酒店 / 旅行社；不爬抓任何机票 / 酒店 / 签证数据；不绕过任何外汇 / 出入境规则。所有数据为公开静态规则，签证 / 季节 / 预算请以官方与实地为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-travel

# 1. 生成 30 天环球路线（自然 + 海岛 主题，4 月出发，舒适档，亚欧两洲）
python3 scripts/route.py "themes=自然,海岛|days=30|start_month=4|tier=comfort|continents=亚洲,欧洲"

# 2. 一段欧洲行的预算估算（商务档 20 天）
python3 scripts/budget.py "cities=巴黎,罗马,巴塞罗那|days=20|tier=business"

# 3. 签证办理矩阵（按办理 leadtime 倒排）
python3 scripts/visa.py "countries=日本,法国,美国,巴西,肯尼亚|order=date"

# 4. 11 月去哪（红叶 + 海岛主题）
python3 scripts/season.py "month=11|themes=红叶,海岛"

# 5. 跨气候打包清单（热带 + 高山 + 潜水 + 徒步，21 天）
python3 scripts/pack.py "climates=tropical,alpine|themes=diving,trekking|days=21"
```

## Usage Examples

### 1. 卖了公司想 gap year 来一次真环球

```bash
python3 scripts/route.py "themes=自然,极地,海岛,文化|days=180|start_month=10|tier=business|continents=亚洲,欧洲,北美,南美,非洲,大洋洲,极地"
```

输出：跨 6 大洲 + 极地的 180 天清单，按季节排序，含商务档总预算估算（机票 + 食宿 + 保险 + 签证 + 15% 应急）。

### 2. 米其林三星城市巡礼

```bash
python3 scripts/route.py "themes=美食,城市|days=21|start_month=5|tier=luxury|continents=欧洲"
```

输出：巴黎 / 罗马 / 巴塞罗那 / 伦敦 / 东京等城市筛选，luxury 档 Aman / Six Senses 等酒店建议。

### 3. 蜜月去马代 + 巴厘岛

```bash
python3 scripts/budget.py "cities=马尔代夫,巴厘岛|days=12|tier=luxury"
```

### 4. 本月就走，去哪好

```bash
python3 scripts/season.py "month=2|themes=海岛,极地"
```

输出：2 月推荐目的地（巴塔哥尼亚 / 新西兰 / 马代 / 南极末季 / 里约狂欢节），含半球切换提示。

### 5. 签证集中办

```bash
python3 scripts/visa.py "countries=美国,日本,法国,英国,巴西,肯尼亚,坦桑尼亚,澳大利亚|order=date"
```

输出：按 leadtime 倒序排列的办理时间轴，明确每国出发前几天动手；总签证费估算。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/route.py "<input>"` | 主题 / 时长 / 预算 / 月份生成路线 | `themes=...\|days=...\|start_month=...\|tier=...\|continents=...` | JSON |
| `python3 scripts/budget.py "<input>"` | 单次行程或环球预算估算（4 档） | `cities=...\|days=...\|tier=shoestring/comfort/business/luxury` | JSON |
| `python3 scripts/visa.py "<input>"` | 中国普通护照签证矩阵 + 办理时间轴 | `countries=...\|order=date` | JSON |
| `python3 scripts/season.py "<input>"` | 按月份反查推荐目的地 + 节庆 | `month=1..12\|themes=...\|continents=...` | JSON |
| `python3 scripts/pack.py "<input>"` | 跨气候打包清单 | `climates=...\|themes=...\|days=...` | JSON |

## Scripts

### `scripts/route.py`
- **职责**：从 200+ 城市中按主题命中 + 季节匹配 + 大洲过滤打分排序，按建议天数塞进总时长，给出预算分项与大洲分组
- **输入**：`themes` / `days` / `start_month` / `tier` / `continents`
- **输出**：JSON `{stops, by_continent, budget_breakdown_cny, total_cny, tips}`

### `scripts/budget.py`
- **职责**：按 4 档（穷游 / 舒适 / 商务 / 奢华）估算行程总预算 = 食宿 + 机票 + 保险 + 签证 + 15% 应急
- **输入**：`cities` / `days` / `tier`
- **输出**：JSON `{daily_cost_cny, breakdown_cny, total_cny, per_person_per_day_cny}`

### `scripts/visa.py`
- **职责**：中国 PRC 普通护照对 40+ 主流国家的签证类型 / 停留天数 / 大致费用 / 办理周期；可按 leadtime 倒排出"出发前几天动手"时间轴
- **输入**：`countries` / `order`
- **输出**：JSON `{schedule, total_fee_cny_est, earliest_apply_before_departure_days, warnings}`

### `scripts/season.py`
- **职责**：按月份反查目的地，含半球冷暖提示、当月节庆、`avoid` 提醒
- **输入**：`month` / `themes` / `continents`
- **输出**：JSON `{month_name, recommended_curated, all_matched, festivals_this_month, hemisphere_swap_tip}`

### `scripts/pack.py`
- **职责**：基础包 + 6 类气候模块 + 6 类主题模块 + 行李策略 + TSA 红线
- **输入**：`climates`（tropical / desert / alpine / polar / temperate_summer / temperate_winter）/ `themes`（diving / trekking / safari / michelin_tour / self_drive / ski）/ `days`
- **输出**：JSON `{base_kit, climate_modules, theme_modules, luggage_strategy, tsa_redlines}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/destinations.json` — 7 大洲 80+ 国 200+ 城市基础信息
- `references/visa_cn.json` — 中国普通护照签证矩阵
- `references/seasons.json` — 12 个月份索引 + 节庆日历
- `references/budgets.json` — 4 档预算结构 + 辅助成本
- `references/packing.json` — 跨气候 / 跨主题打包清单 + TSA 红线

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 未用 `key=value` 格式 | 用 `\|` 分隔多个字段，每个字段 `key=value` |
| `error: bad number` | `days` / `month` 不是数字 | 传入纯数字（不要带「天」「月」单位） |
| `not_found` 包含某国 | visa_cn.json 未列入 | 该国不在 40+ 主流目的地清单内，请直接查中国领事服务网 |
| 推荐目的地很少 | themes / continents 过严 | 放宽其中一项，或参考 destinations.json 的 themes 列表 |

## References

- 中国领事服务网（cs.mfa.gov.cn）—— 签证 / 出入境 / 安全提示
- 国家外汇管理局《个人外汇管理办法》—— 5 万美元年度购汇额度
- TSA / IATA 国际通用安检与行李规则
- 各国驻华使馆官网 —— 签证最终口径
- 申根 90/180 规则、申根保险 30 万欧元医疗保额要求

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何机票 / 酒店数据**
- 数据为静态参考，签证 / 季节 / 预算请以官方与实地为准
- 涉及外汇 / 移民 / 长期居留的场景，请咨询持牌律师 / 银行私行 / 持牌出入境中介
- 高风险国家（叙利亚 / 也门 / 阿富汗 / 朝鲜等）默认不做攻略
- 主基调：**让世界变成可清单化的事情**，不是炫耀也不是攀比
