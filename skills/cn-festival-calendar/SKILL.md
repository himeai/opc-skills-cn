---
name: cn-festival-calendar
description: 中国节日 / 节气 / 大促 / 监管敏感期内容决策引擎：给定日期或节日，输出 5 大平台（小红书/抖音/快手/B站/公众号）的发布角度、错峰排期、敏感期警告。本地数据，不爬抓不调外部 API。Use when 用户提到节日营销、节气、电商大促、618、双 11、年货节、春节、中秋、节日选题、内容排期、错峰发布、两会、清明、烈士纪念日、敏感期、过节发什么、节日日历。
---

# 中国节日内容决策引擎（cn-festival-calendar）

> 看日历只能告诉你"今天是几号"，但一个跑 5 个平台的内容创作者真正需要知道：今天是不是内容机会、什么时候开始铺、哪个平台用什么角度、什么时候要避开敏感期。本 skill 把节日 / 节气 / 大促 / 监管敏感期整理成本地决策引擎，覆盖 5 个主流平台。

## Prerequisites

### 环境变量
本 skill **不需要任何凭证**，全部本地推理。

### 依赖
仅 stdlib。

### 数据范围
- 公历节日：18 个（元旦、315、五一、国庆、双 11 等）
- 农历节日：11 个（春节、端午、中秋、重阳等），覆盖 **2024–2030 年公历对应日期**
- 24 节气：全部，按公历近似落点
- 电商大促：6 个（年货节、38 节、618、双 11、双 12 等），含预热与转化窗口
- 监管 / 平台敏感期：两会、高考、清明、烈士纪念日、教培专项、医疗常态、金融常态等
- 地方节日：泼水节、火把节、那达慕、苗年、藏历新年

> 农历对应日期超出 2024–2030 范围时，请补充 `references/dates.json`。

## Quick Start

```bash
# 1. 查今天对一个跨多平台、医疗行业的创作者意味着什么
python3 scripts/today.py "2026-06-01|general|all"

# 2. 给端午节生成 3 个平台的错峰发布排期
python3 scripts/plan.py "duanwu|general|xiaohongshu,douyin,bilibili"

# 3. 检查 2026-03-08 对金融行业是否处于敏感期
python3 scripts/blackout.py "2026-03-08|finance"
```

预期 `today.py` 输出节选：
```json
{
  "date": "2026-06-01",
  "festivals": [
    {"name": "六一儿童节", "type": "solar", "tier": "A"},
    {"name": "618 年中大促（预热期）", "type": "ecommerce_warmup", "tier": "A"}
  ],
  "content_opportunities": [
    {"festival": "六一儿童节", "platform": "xiaohongshu",
     "angles": ["亲子穿搭", "玩具", "童年回忆杀"], "post_by": "2026-05-11"}
  ],
  "blackout_alerts": [],
  "upcoming_14d": [...]
}
```

## Usage Examples

### 场景 1：每日例会问"今天该发什么"
```bash
python3 scripts/today.py "today|general|xiaohongshu,douyin,wechat_mp"
```

### 场景 2：为下一次大促排期
```bash
python3 scripts/plan.py "shuang_shi_yi|cosmetics|all"
```

### 场景 3：金融号写稿前避雷
```bash
python3 scripts/blackout.py "today|finance"
```

### 场景 4：教培号在高考前后的内容禁区
```bash
python3 scripts/blackout.py "2026-06-08|education"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/today.py "<date>\|<industry>\|<platforms>"` | 给定日期的节日 + 内容机会 + 敏感期一站式报告 | `\|` 分隔 | JSON |
| `python3 scripts/plan.py "<festival_id>\|<industry>\|<platforms>"` | 给定节日的多平台错峰排期 | `\|` 分隔 | JSON |
| `python3 scripts/blackout.py "<date>\|<industry>"` | 给定日期是否在监管 / 平台敏感期 | `\|` 分隔 | JSON |

`date`：`YYYY-MM-DD` 或 `today`
`industry`：`general` / `finance` / `medical` / `cosmetics` / `food` / `education`
`platforms`：`xiaohongshu` / `douyin` / `kuaishou` / `bilibili` / `wechat_mp`，逗号分隔，或 `all`
`festival_id`：见 `references/festivals.json`，例：`chunjie` / `duanwu` / `zhongqiu` / `618` / `shuang_shi_yi` / `nianhuojie`

## Scripts

### `scripts/credential.py`
本 skill 无凭证需求，仅占位以保持目录结构一致。

### `scripts/today.py`
- **职责**：根据公历日期，汇总当日所有节日 / 节气 / 大促窗口 + 未来 14 天预告 + 各平台对应内容角度 + 该行业的敏感期警告
- **输入**：`date|industry|platforms`
- **输出**：`{date, festivals, content_opportunities, blackout_alerts, upcoming_14d}`

### `scripts/plan.py`
- **职责**：以一个节日为锚点，按各平台 lead-time（小红书 21 天 / B 站 10 天 / 抖音 7 天等）生成错峰发布表
- **输入**：`festival_id|industry|platforms`
- **输出**：`{festival, festival_date, days_to_go, schedule: [{platform, post_by, angles, best_post_types, windows}], earliest_action}`

### `scripts/blackout.py`
- **职责**：判断给定日期对该行业是否处于监管 / 平台敏感期；命中即返回 `level`（high/medium/low）+ 禁忌话题 + 替代角度 + 法规依据
- **输入**：`date|industry`
- **输出**：`{date, industry, alerts: [...], safe, highest_level}`

## 数据架构

```
references/
├── festivals.json          # 节日 / 节气 / 电商大促 / 地方节日
├── blackout_periods.json   # 监管 + 平台敏感期
├── platform_timing.json    # 各平台最佳发布时段 + 节日角度映射
└── dates.json              # 农历→公历对照表（2024-2030）
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **数据版本**：见各 JSON 顶部 `version` 字段
- **更新频率**：每年初（春节前）必须 PR 更新农历对应日期，敏感期跟随重大法规变动手动更新

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `unknown festival id` | 节日 ID 不在词典 | 见 `references/festivals.json` 取 `id` 字段，或新增 |
| `could not resolve date for festival` | 农历对照表年份缺失 | 在 `references/dates.json` 追加目标年份 |
| 节气日期偏差 1 天 | 用了近似落点 | 节气真实日期需查询授时中心；本 skill 不追求绝对准确，仅作内容排期参考 |
| 母亲节 / 父亲节日期不准 | 这两个节日是"5 月第二个周日 / 6 月第三个周日" | 当前用近似日期占位；需绝对准确请扩展 solar 配置增加 `weekday_anchor` |

## References

- 公开节日数据：法定节假日通知 + 中科院授时中心
- 平台运营时段：抖音创作者中心 / 小红书蒲公英 / B 站创作中心 / 视频号助手 / 快手磁力金牛公开白皮书
- 敏感期依据：《广告法》《互联网广告管理办法》《关于进一步减轻义务教育阶段学生作业负担和校外培训负担的意见》《英雄烈士保护法》

## Notes

- 本 skill **不爬抓任何平台**，节日 / 时段 / 敏感期数据全部静态收录
- 与 `cn-content-compliance` 互补：合规 skill 管"这句话能不能说"，本 skill 管"这个时间点能不能发这个话题"
- 与 `xiaohongshu-ops` / `douyin-ops` / `kuaishou-ops` / `bilibili-ops` / `wechat-ops` 配合使用：本 skill 给排期 + 角度，再交给对应平台 skill 生成具体文案
