---
name: cn-city-picker
description: 中国创业城市智能选址。根据用户行业、预算、家庭、户籍、生活偏好，从 300+ 地级市中按八维评分（税收/生活成本/气候/创业政策/产业生态/人才供给/数字基建/行政效率）筛选 Top 3-5 推荐城市，输出对比报告、政策清单与落地 checklist。Use when 用户提到选城市、创业去哪、注册公司选哪个城市、个独注册地、园区落户、城市对比、税收洼地、宜居创业、人才补贴、园区返税、跨境电商综试区。
---

# 中国创业城市选址（cn-city-picker）

> 一人公司的"第 0 步决策"。选错城市每年损失 5-20 万（税负 + 房租 + 错失补贴）。
> 本 skill 把行业/预算/家庭/户籍/偏好 → 转化为八维加权评分 → 输出 Top 3-5 推荐 + 落地 checklist。

## Prerequisites

### 环境变量
```bash
# 全部可选 - 用于实时抓取最新政策；未配置时降级到静态数据底库
export TIANYANCHA_API_KEY=""        # 可选：拉产业链上下游聚集度
export AMAP_API_KEY=""              # 可选：拉房租/通勤实时数据
```

### 账号要求
无强制。**未配置任何 key 时，仍可使用静态底库给出报告**（数据按季度更新）。

### 依赖
仅 stdlib。

## Quick Start

```bash
python3 scripts/pick.py "我做跨境电商独立站，月预算 1.5 万，已婚无娃，
老婆是医生需要三甲医院，怕冷不爱辣，户籍山东，倾向南方非一线"
```

输出（节选）：
```json
{
  "top_recommendations": [
    {
      "city": "厦门",
      "score": 87,
      "highlights": ["跨境电商综试区一类", "个独核定 0.5-2.1%", "三甲 12 家", "冬均温 12℃"],
      "concerns": ["房价偏高", "梅雨 3-6 月"],
      "monthly_cost_estimate_cny": 13200
    },
    {"city": "佛山", "score": 84, ...},
    {"city": "成都", "score": 81, ...}
  ],
  "next_steps_checklist": [
    "联系厦门软件园三期咨询入驻",
    "在 cn-tax 中选择「厦门个独核定」预设",
    "icp-domain-cn 建议接入商：阿里云华东 2"
  ]
}
```

## Usage Examples

### 场景 1：自由职业 SaaS 开发者，单身，预算紧
```bash
python3 scripts/pick.py "我一个人做 SaaS，月预算 8000，单身，喜欢有 livehouse 和咖啡馆，不要太热"
```
预期推荐方向：长沙 / 成都 / 西安 / 杭州临安。

### 场景 2：跨境电商，看重综试区与园区返税
```bash
python3 scripts/pick.py "跨境电商独立站 + 亚马逊，看重综试区一类、园区返税 ≥ 30%，团队预计 1 人"
```
预期推荐方向：厦门 / 深圳前海 / 杭州 / 宁波。

### 场景 3：自媒体博主，看重内容生态
```bash
python3 scripts/pick.py "小红书 + 视频号美食博主，需要拍摄场景多元，注重美食、消费力"
```
预期推荐方向：成都 / 长沙 / 广州 / 苏州。

### 场景 4：仅查询单一城市的八维档案
```bash
python3 scripts/profile.py 厦门
```

### 场景 5：两两对比
```bash
python3 scripts/compare.py 厦门 杭州 成都
```

## Commands

| 命令 | 说明 |
|---|---|
| `python3 scripts/pick.py "<自然语言偏好>"` | 主入口：偏好 → Top N 推荐 |
| `python3 scripts/profile.py <城市名>` | 单城市八维档案 |
| `python3 scripts/compare.py <城市A> <城市B> [城市C ...]` | 多城市横向对比 |
| `python3 scripts/refresh_policy.py [城市名]` | 强制刷新政策时效字段缓存 |

## Scripts

### `scripts/pick.py`
- **输入**：自然语言偏好字符串
- **流程**：解析偏好 → 加载 `references/cities.json` → 八维加权 → 行业匹配矩阵加权 → Top N
- **输出**：JSON

### `scripts/profile.py`
- **输入**：城市名（中文）
- **输出**：该城市八维原始指标 + 政策清单 + 联动 skill 提示

### `scripts/compare.py`
- 多城市横向对比，输出 Markdown 表 + 雷达图数据

### `scripts/refresh_policy.py`
- 抓取政府公开政策页（白名单域名），LLM 摘要后写入 `references/policy_cache/<city>.json`
- 默认缓存 7 天

### `scripts/credential.py`
读取可选环境变量。

## 数据架构

```
references/
├── cities.json              # 50 重点城市八维静态指标（季度更新）
├── industry_city_matrix.json # 20 行业 × 50 城市契合度（0-100）
├── policy_cache/            # 时效性政策缓存（脚本自动管理）
└── sources.md               # 每个数据点的来源链接与采集日期
```

### `cities.json` 单条 schema
```json
{
  "city": "厦门",
  "tier": "新一线",
  "province": "福建",
  "dimensions": {
    "tax_policy":      {"score": 88, "indv_tax_min": 0.005, "park_rebate_max": 0.4},
    "living_cost":     {"score": 65, "rent_1b1b_median": 4500, "meal_index": 38},
    "startup_policy":  {"score": 85, "register_subsidy": 5000, "social_insurance_relief": true},
    "climate":         {"score": 82, "avg_temp": 21, "pm25_avg": 28, "rainy_season": "3-6"},
    "digital_infra":   {"score": 90, "gigabit_coverage": 0.95, "cross_border_bw": "good"},
    "industry":        {"score": 87, "cluster": ["跨境电商", "软件", "文旅"]},
    "talent":          {"score": 78, "college_count": 16, "retention_rate": 0.62},
    "admin_efficiency":{"score": 86, "register_days": 1, "icp_days": 7}
  },
  "policy_links": [
    {"title": "厦门软件园企业入驻指南", "url": "..."},
    {"title": "跨境电商综试区扶持政策", "url": "..."}
  ],
  "next_steps_template": [
    "联系厦门软件园三期咨询入驻",
    "在 cn-tax 选择「厦门个独核定」预设"
  ]
}
```

## 偏好解析规则（pick.py 内置）

| 用户表达 | 加权 |
|---|---|
| "预算紧 / 便宜" | `living_cost` ×1.5 |
| "三甲医院 / 老人 / 孩子" | `living_cost` ×0.8 + 强制过滤医疗资源 ≥ 阈值 |
| "怕冷 / 南方" | 过滤年均温 < 15℃ |
| "不爱辣" | 排除川渝湘鄂（弱过滤，可被其它维度反超） |
| "跨境电商" | 行业矩阵 ×2 + `tax_policy.park_rebate_max` ×1.3 |
| "户籍 XX" | XX 同省候选 ×1.1（落户/社保友好度） |
| "非一线 / 慢生活" | 过滤一线城市 |

## 与其它 skill 的联动（dependencies）

本 skill 输出会在 `next_steps_checklist` 中显式提示用户继续调用：
- `cn-tax` —— 加载所选城市的税收预设
- `icp-domain-cn` —— 建议接入商区域
- `wepay-alipay` —— 提示对公账户所在地要求
- `cn-recruit` —— 切换本地招聘平台权重

## API Info

- **静态底库**：随 skill 一同分发，无外部 API
- **可选实时源**：
  - 天眼查 API（产业链）：`https://open.tianyancha.com`
  - 高德 API（房租/通勤）：`https://lbs.amap.com`

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| 推荐结果偏一线 | 用户未表达预算约束 | 显式加 "月预算 X 元" 重新调用 |
| 政策链接过期 | 政府站定期改版 | 运行 `refresh_policy.py <city>` 重新抓取 |
| 城市未收录 | 不在 50 重点城市列表 | 在 `cities.json` 提 PR 补充 |

## References

- 国务院"一网通办"评估报告 https://www.gov.cn
- 中国气象局月报 http://www.cma.gov.cn
- 各地税务局公告（按需检索）
- 仲量联行《中国创业城市活力指数》年度报告

## Notes

- 本 skill **不构成法律/税务建议**，最终落户决策请咨询当地代账机构
- 数据底库每季度更新一次，时效字段（最新补贴）走缓存抓取
- 行业矩阵默认覆盖 20 个 OPC 主流行业，缺失行业请提 issue
- 严格 PIPL 合规：不收集用户输入的家庭/户籍信息到 skill 目录外
