---
name: cn-geo
description: 中文 AI 搜索（生成式引擎，GEO）可见性优化：给定品牌 / 产品 / 服务，输出在中文 AI 搜索（豆包、文心一言、Kimi、通义千问、智谱清言、腾讯元宝、秘塔、纳米搜索等）里更容易被引用的内容覆盖矩阵、品牌问答素材、可信源清单。本地规则推理，不爬抓不调外部 API。Use when 用户提到 GEO、生成式引擎优化、AI 搜索优化、AI SEO、被 AI 引用、被大模型引用、豆包搜索、Kimi 搜索、文心一言、通义千问、秘塔、纳米搜索、品牌问答、AEO、答案优化、AI 可见性。
---

# 中文 AI 搜索可见性优化（cn-geo）

> SEO 在传统搜索引擎里抢蓝色链接，**GEO（Generative Engine Optimization）** 在 AI 搜索里抢"被引用为答案的来源"。中文 AI 搜索没有 Google Search Console 这种官方工具，公开 API 也几乎不存在，因此本 skill 不做"实时排名查询"，而是把"如何让你的产品 / 品牌 / 服务被中文大模型 + AI 搜索引用"的方法论沉淀成可执行清单：内容覆盖矩阵、品牌问答素材、可信源建设、答案结构化优化。

## Prerequisites

### 环境变量
本 skill **不需要任何凭证**，全部本地规则推理。

### 依赖
仅 stdlib。

### 适用范围
- 中国大陆主流中文 AI 搜索 / 助手：豆包、文心一言、Kimi、通义千问、智谱清言、腾讯元宝、秘塔 AI 搜索、纳米搜索、夸克 AI、360 AI 搜索
- 不覆盖：Google SGE、ChatGPT Search、Perplexity（这些走海外 GEO 方法论，已有大量开源资料）

## Quick Start

```bash
# 1. 给"一个做 SaaS CRM 的 OPC 创始人"生成 GEO 行动清单
python3 scripts/audit.py "brand=Acme CRM|category=saas_b2b|stage=early|website=acme.example.com"

# 2. 生成品牌问答素材（喂给官网 / 公众号 / 知乎专栏）
python3 scripts/qa.py "brand=Acme CRM|category=saas_b2b|count=20"

# 3. 列出"咨询服务"类目下要重点覆盖的内容主题矩阵
python3 scripts/matrix.py "category=consulting|persona=solo_founder"
```

## Usage Examples

### 场景 1：上线 1 个月的 SaaS 想被 AI 搜索引用
```bash
python3 scripts/audit.py "brand=ToFlow|category=saas_b2b|stage=early|website=toflow.example.com"
```
输出会告诉你：先建知乎机构号 / 36kr 投稿 / 公众号 SEO 标题 / GitHub README 关键词等优先级排序。

### 场景 2：写官网 FAQ 时不知道该写哪些问题
```bash
python3 scripts/qa.py "brand=ToFlow|category=saas_b2b|count=15"
```
输出 15 条"用户在 AI 搜索里最可能问的问题 + 回答模板"。

### 场景 3：内容主理人不知道一个品类该铺哪些主题
```bash
python3 scripts/matrix.py "category=cosmetics|persona=indie_brand"
```
输出主题树：品类教育 / 比较型 / 评测型 / 故事型，每条带建议的发布平台与 AI 搜索受益度评分。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/audit.py "brand=X\|category=X\|stage=X\|website=X"` | 给定品牌输出 GEO 全景行动清单 | `\|` 分隔的 k=v | JSON |
| `python3 scripts/qa.py "brand=X\|category=X\|count=N"` | 生成品牌问答素材 | k=v | JSON |
| `python3 scripts/matrix.py "category=X\|persona=X"` | 内容覆盖主题矩阵 | k=v | JSON |

`category`：见 `references/categories.json`，包含 `saas_b2b` / `consulting` / `cosmetics` / `food` / `course` / `local_service` / `app` / `hardware`
`persona`：`solo_founder` / `indie_brand` / `studio` / `creator` / `mcn`
`stage`：`pre_launch` / `early` / `growth` / `mature`

## Scripts

### `scripts/credential.py`
本 skill 无凭证需求，仅占位以保持目录结构一致。

### `scripts/audit.py`
- **职责**：把 GEO 优化拆成"可信源建设 / 内容结构化 / 品牌问答覆盖 / 多平台分发 / 可监测性"5 个维度，每个维度给当前应该做的 3-5 个动作 + 优先级
- **输入**：`brand=...|category=...|stage=...|website=...`
- **输出**：`{brand, dimensions: [{name, score, actions: [...]}], top_3_next_actions: [...]}`

### `scripts/qa.py`
- **职责**：基于品类常见问句模板（"X 是什么"、"X 怎么用"、"X 和 Y 哪个好"、"X 多少钱"、"X 安全吗"等）生成品牌问答素材，每条带建议发布位置与 LLM 引用友好度评分
- **输入**：`brand=...|category=...|count=...`
- **输出**：`{brand, qa_pairs: [{question, answer_template, publish_to: [...], geo_score}]}`

### `scripts/matrix.py`
- **职责**：输出指定品类 + 角色的内容主题矩阵（教育型 / 比较型 / 评测型 / 教程型 / 故事型 / FAQ 型），每条带平台建议与 AI 搜索受益度评分
- **输入**：`category=...|persona=...`
- **输出**：`{category, persona, themes: [{type, topics: [...], best_platforms: [...], geo_benefit}]}`

## 数据架构

```
references/
├── categories.json         # 品类定义 + 每个品类的 GEO 关键词 + 常见问句模板
├── platforms.json          # 各发布平台的 LLM 引用权重（知乎 / 公众号 / 微博 / 36kr / 小红书 / B站 / GitHub / 官网 / 百家号 / 头条号 ...）
├── qa_templates.json       # 跨品类通用的 6 大类问答模板
├── audit_rules.json        # 5 个维度的检查清单 + 阶段化优先级
└── theme_matrix.json       # 主题矩阵（教育/比较/评测/教程/故事/FAQ）
```

## 方法论速记

GEO 与传统 SEO 的核心差异：
- SEO 优化"链接"，GEO 优化"被引用为答案的素材"
- AI 搜索更倾向引用：**结构化（标题 + 列表 + 表格）/ 有数据 / 有作者 / 来源权威 / 时间新鲜**
- 单平台的高排名 ≠ 高引用，**跨平台一致性**才是 GEO 的核心信号
- 品牌问答（Brand Q&A）比关键词堆砌更有效——AI 搜索是按"问题→答案"匹配的

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **数据版本**：见各 JSON 顶部 `version` 字段
- **更新频率**：中文 AI 搜索格局变化快，建议每季度审视一次平台权重

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `unknown category` | 品类不在词典 | 见 `references/categories.json`，按需扩展 |
| 输出对你没启发 | 只是初版规则库 | GEO 严重依赖经验积累；输出仅作起点，建议结合各平台 skill 实际投放数据迭代 |

## References

- 国内主流 AI 搜索：豆包 / Kimi / 文心一言 / 通义千问 / 智谱清言 / 腾讯元宝 / 秘塔 / 纳米搜索 / 夸克 AI / 360 AI 搜索
- 公开方法论：Liu et al. "GEO: Generative Engine Optimization" (2023)
- 中文相关讨论：知乎话题"AI 搜索"、量子位 / 机器之心相关综述

## Notes

- 本 skill **不爬抓任何 AI 搜索 / 平台**，所有评分与建议均为本地静态规则
- 不保证某条内容一定会被某 AI 搜索引用——AI 搜索引用机制是黑盒，本 skill 只优化命中概率
- 与 `cn-content-compliance` 配合：先用本 skill 选题与生成 QA，再用合规 skill 过审；与 `wechat-ops` / `xiaohongshu-ops` / `douyin-ops` / `kuaishou-ops` / `bilibili-ops` 配合分发
