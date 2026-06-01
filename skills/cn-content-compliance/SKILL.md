---
name: cn-content-compliance
description: 中国市场内容发布前的合规自检：广告法极限词、医疗 / 食品 / 化妆品 / 金融 / 教培行业红线、小红书 / 抖音 / B 站 / 公众号 / 快手平台禁用词，全部本地规则匹配，附改写建议。Use when 用户提到合规、违禁词、极限词、广告法、敏感词、审核、过审、风险词、内容自检、发布前检查、改写、降级、平替词。
---

# 中国内容合规自检（cn-content-compliance）

> 一人公司发内容最容易踩三类坑：广告法极限词、行业红线（医疗/食品/化妆品/金融/教培）、平台社区公约。本 skill 把这些公开规则整理成本地词库 + 行级检测器，发布前先过一遍，再让真人决定要不要改。

## Prerequisites

### 环境变量
本 skill **不需要任何凭证**，全部本地推理。

### 依赖
仅 stdlib。

### 法律免责
- 本 skill 词库来自公开法规与平台公开规则，**仅作辅助参考**，不构成法律意见
- 真实发布前请由法务/合规人员复核，尤其医疗、金融、教培等强监管行业
- 词库会持续更新，但不保证完备

## Quick Start

```bash
# 1. 检查一段文案，含广告法 + 平台双重维度
python3 scripts/check.py "我们家护肤品全网最低价，100% 美白祛斑|cosmetics|xiaohongshu"

# 2. 让 skill 把命中的极限词替换为合规改写建议
python3 scripts/rewrite.py "我们家护肤品全网最低价，100% 美白祛斑|cosmetics|xiaohongshu"

# 3. 查看某行业 / 平台的完整规则
python3 scripts/rules.py "cosmetics|xiaohongshu"
```

预期 `check.py` 输出（节选）：
```json
{
  "summary": {"total_hits": 4, "highest_severity": "high"},
  "hits": [
    {"phrase": "全网最低", "category": "ad_law_extreme", "severity": "high", ...},
    {"phrase": "100%",     "category": "ad_law_extreme", "severity": "high", ...},
    {"phrase": "美白",     "category": "cosmetics",      "severity": "high", ...},
    {"phrase": "祛斑",     "category": "cosmetics",      "severity": "high", ...}
  ]
}
```

## Usage Examples

### 场景 1：小红书化妆品笔记发布前自检
```bash
python3 scripts/check.py "敏感肌亲测：这款国家级精华，30 天根治痘印|cosmetics|xiaohongshu"
```

### 场景 2：抖音直播脚本反极限词
```bash
python3 scripts/check.py "全网最低价，全国包邮，秒杀 9 块 9|food|douyin"
```

### 场景 3：金融号合规改写
```bash
python3 scripts/rewrite.py "保本理财，稳赚不赔，年化 15%|finance|wechat_mp"
```

### 场景 4：查看某行业 / 平台完整词表
```bash
python3 scripts/rules.py "education|douyin"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/check.py "<text>\|<industry>\|<platform>"` | 全维度敏感词扫描 | `\|` 分隔 | JSON：summary + hits[] |
| `python3 scripts/rewrite.py "<text>\|<industry>\|<platform>"` | 命中词替换为合规改写建议 | `\|` 分隔 | JSON：rewritten、changes[] |
| `python3 scripts/rules.py "<industry>\|<platform>"` | 列出指定行业 + 平台的完整规则 | `\|` 分隔 | JSON：categories、severity |

`industry` 可选：`general` / `medical` / `cosmetics` / `food` / `finance` / `education`
`platform` 可选：`general` / `xiaohongshu` / `douyin` / `bilibili` / `wechat_mp` / `kuaishou`

## Scripts

### `scripts/credential.py`
本 skill 无凭证需求，仅占位以保持目录结构一致。

### `scripts/check.py`
- **职责**：从 `references/rules.json` 加载规则，扫描文案，命中即上报短语、分类、严重度、法律依据
- **入参**：`text|industry|platform`
- **输出**：`{summary: {total_hits, highest_severity}, hits: [...]}`

### `scripts/rewrite.py`
- **职责**：基于 `rewrite_hints` 把高危词降级为合规表达；未命中改写表的词原样保留并提示
- **入参**：`text|industry|platform`
- **输出**：`{rewritten, changes: [{from, to, category}]}`

### `scripts/rules.py`
- **职责**：导出某 `industry × platform` 组合的完整词表，便于 PR / 法务复核
- **入参**：`industry|platform`
- **输出**：`{industry, platform, categories: {...}}`

## 数据架构

```
references/
└── rules.json     # 广告法 + 行业红线 + 平台禁用词 + 改写建议
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **词库版本**：见 `references/rules.json` 顶部 `version` 字段
- **更新频率**：跟随重大法规变动手动更新（PR 欢迎）

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| 命中词漏报 | 词库未覆盖、变形/谐音 | 在 `references/rules.json` 提 PR 增加 |
| 误报多 | 上下文意义不同（如"治愈系" vs "治愈"） | 当前为子串匹配，会有少量误报；改写建议仅作参考 |
| `industry`/`platform` 不识别 | 拼写错误 | 见上文可选值；未识别时按 `general` 处理 |

## References

- 《中华人民共和国广告法》
- 《化妆品监督管理条例》
- 《食品安全法》第 73 条
- 《金融营销宣传管理办法》
- "双减"政策与教培广告管理要求
- 各平台公开社区公约 / 商业化规则

## Notes

- 本 skill **不爬抓任何平台**，规则全部静态收录
- 词库与改写建议仅供参考，**不构成法律意见**
- 与 `wechat-ops` / `xiaohongshu-ops` / `douyin-ops` / `kuaishou-ops` / `bilibili-ops` 配合使用：发布前用本 skill 过一遍
