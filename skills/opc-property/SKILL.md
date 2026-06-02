---
name: opc-property
description: 一人公司「成功篇·置业」副驾驶（本地规则版）：1000 万起步的高净值置业决策——国内顶豪盘（汤臣一品 / 深圳湾一号 / 钓鱼台七号院 / 翠湖天地等）、海外 10 大豪宅市场（纽约 / 伦敦 / 巴黎 / 悉尼 / 新加坡 / 迪拜 / 东京 / 洛杉矶 / 温哥华 / 葡萄牙）、5 年持有成本测算、跨境资金合规清单。本地推理，不构成投资 / 移民 / 税务建议，不推荐任何具体楼盘 / 中介。Use when 用户提到置业、买房、豪宅、顶豪、神盘、汤臣一品、深圳湾一号、钓鱼台七号院、海外置业、买房送身份、Golden Visa、迪拜金签、伦敦买房、纽约公寓、第二居所、家族信托、CRS、ODI、外汇额度、5 万美元、跨境资金。
---

# 一人公司置业副驾驶（opc-property）

> 一个人靠 AI 把公司做起来了，下一步就是把钱搬到一些「过 50 年还在那里」的资产上。
>
> 这个 skill 不是给你「劝买」的——它是给你**算账**的：
> 看清「值不值得 / 能不能买 / 持有要花多少 / 钱能不能合规出去」四个核心问题。
>
> 1000 万人民币是入场券。这个 skill 默认你已经过了那一关。

> 本 skill 不构成投资 / 移民 / 税务 / 法律建议；不推荐任何具体楼盘、中介、私行、移民顾问；不教任何规避外汇管制的办法。所有数据来自公开市场信息整理，时效性以当地最新公告为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-property

# 1. 综合匹配：给我国内外 Top 3 候选
python3 scripts/match.py "budget_cny=3000w|purpose=自住|family=有学龄子女|residency=希望第二身份|risk_pref=中"

# 2. 国内城市排序
python3 scripts/cn_city.py "budget_cny=2000w|priority=学区"

# 3. 海外市场对照
python3 scripts/global_market.py "budget_cny=5000w|residency=希望第二身份|tax_pref=低税|family=有学龄子女"

# 4. 5 年持有成本测算
python3 scripts/holding_cost.py "city=纽约|total_cny=5000w|hold_years=5|rent_out=yes"

# 5. 跨境资金合规检查
python3 scripts/compliance.py "amount_cny=5000w|target_country=美国|use=境外购房|family_size=3"
```

预算可以写 `1000w` / `1.2 亿` / `30000000`，工具会自动解析。

## Usage Examples

### 1. 三千万级买家：自住 + 子女教育
```bash
python3 scripts/match.py "budget_cny=3000w|purpose=自住|family=有学龄子女|residency=希望第二身份|risk_pref=中"
```
输出：识别为「三千万级」段位，国内推 A/S 级标的（前滩天悦、华润润府、深圳湾一号等），海外推迪拜 / 新加坡 / 悉尼 / 温哥华 / 洛杉矶。

### 2. 亿级买家：以伦敦 / 纽约为目标的旗舰资产
```bash
python3 scripts/global_market.py "budget_cny=1.2 亿|residency=希望第二身份|tax_pref=中|family=有学龄子女"
```
输出：纽约 / 伦敦 / 巴黎核心区核心楼盘清单 + 17% 印花税 / Mansion Tax 等关键税费。

### 3. 进出场成本对比：迪拜 vs 伦敦
```bash
python3 scripts/holding_cost.py "city=迪拜|total_cny=3000w|hold_years=5|rent_out=yes"
python3 scripts/holding_cost.py "city=伦敦|total_cny=3000w|hold_years=5|rent_out=yes"
```
输出：迪拜零税 + 6.5% 租金收益率 vs 伦敦 17% SDLT + 28% Non-resident CGT 的 5 年总成本对比。

### 4. 把钱搬出去这件事
```bash
python3 scripts/compliance.py "amount_cny=5000w|target_country=美国|use=境外购房|family_size=3"
```
输出：明确 5 万美元额度不可用于购房、ODI 房地产敏感行业受限、推荐「先解决身份再解决资产」路径。

### 5. 国内学区豪宅怎么选
```bash
python3 scripts/cn_city.py "budget_cny=2000w|priority=学区"
```
输出：上海 / 北京 / 深圳 学区维度排序 + 各城市预算内匹配的顶豪盘清单。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/match.py "<input>"` | 国内外综合 Top 3 推荐 | `budget_cny=...\|purpose=...\|family=...\|residency=...\|risk_pref=...` | JSON |
| `python3 scripts/cn_city.py "<input>"` | 国内 10 城 7 维加权排序 | `budget_cny=...\|priority=...` | JSON |
| `python3 scripts/global_market.py "<input>"` | 海外 10 市场对照 + 推荐 | `budget_cny=...\|residency=...\|tax_pref=...\|family=...` | JSON |
| `python3 scripts/holding_cost.py "<input>"` | 5 年持有成本 + 隐含年化 | `city=...\|total_cny=...\|hold_years=...\|rent_out=...` | JSON |
| `python3 scripts/compliance.py "<input>"` | 跨境合规清单 + 红线 | `amount_cny=...\|target_country=...\|use=...\|family_size=...` | JSON |

## Scripts

### `scripts/match.py`
- **职责**：根据预算 / 用途 / 家庭 / 身份偏好做国内 + 海外的 Top 3 综合推荐
- **分层**：千万级 / 三千万级 / 亿级 / 超亿级 4 档
- **输出**：JSON `{segment, domestic_picks, overseas_picks, next_steps}`

### `scripts/cn_city.py`
- **职责**：国内 10 城（沪 / 京 / 深 / 杭 / 广 / 蓉 / 苏 / 厦 / 三 / 大）7 维加权评分（限购 / 流动性 / 学区 / 远期供给 / 持有税费 / 租售比 / 文化品牌）
- **输出**：JSON `{ranked: [{city, weighted_score, headline, matching_properties}]}`

### `scripts/global_market.py`
- **职责**：纽约 / 伦敦 / 巴黎 / 悉尼 / 新加坡 / 迪拜 / 东京 / 洛杉矶 / 温哥华 / 葡萄牙 10 市场对照
- **关联**：自动拼接黄金签证 / 投资移民程序信息
- **输出**：JSON `{ranked, tips, outflow_quota_warning}`

### `scripts/holding_cost.py`
- **职责**：一次性税 + 年度税 + 物业 + 净租金 + 退出税 → 5 年总成本与隐含年化
- **输出**：JSON `{one_time, annual, five_year_summary, interpretation}`

### `scripts/compliance.py`
- **职责**：5 万美元额度边界 + ODI / QDII / WMC 等合规通道清单 + 红线（蚂蚁搬家 / 地下钱庄 / 虚假贸易等）
- **输出**：JSON `{annual_quota, recommended_legal_paths, red_lines, must_know}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。数据来自本地 JSON：
- `references/cn_premium_properties.json` — S/A/B 三级国内顶豪盘 + 4 档买家分层
- `references/cn_cities.json` — 10 城 7 维评分参数
- `references/global_markets.json` — 10 大海外市场参数
- `references/policy_residency.json` — 买房 / 投资移民程序对照
- `references/holding_costs.json` — 各市场持有成本参数
- `references/capital_outflow.json` — 跨境资金合规通道与红线

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 未用 `key=value` 格式 | 用 `\|` 分隔多字段，每段 `key=value` |
| `error: empty budget` | 预算字段为空 | 写 `1000w` / `1.2 亿` / `30000000` 都可以 |
| 某城市无匹配标的 | 预算未达 tier 起步价 | 调高预算或换 tier |

## References

- 国家外汇管理局《个人外汇管理办法》及其实施细则
- 发改委 / 商务部《境外投资管理办法》
- CRS（共同申报准则）官方文件
- 各国移民局最新黄金签证 / 投资移民公告
- 链家 / 贝壳 / 中原 / 易居公开成交数据

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何挂牌 / 成交数据**
- 数据为公开整理，最新口径请咨询当地律师 / 持牌中介 / 银行私行
- 对应「失败篇」是 `opc-shutdown` / `opc-dagong` / `opc-baitan` / `opc-tangping`，对应「成功篇」另两个 skill 是 `opc-travel`、`opc-experience`
- 本工具不构成投资 / 移民 / 税务 / 法律建议；不教任何规避外汇管制的办法
- 已知限制：未覆盖港澳台与一带一路沿线国家；未涉及 PE / 不动产基金等机构通道
