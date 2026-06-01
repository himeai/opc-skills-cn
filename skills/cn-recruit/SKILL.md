---
name: cn-recruit
description: 中国小公司招聘助手（本地规则版）：JD 生成、候选人筛选评分、结构化面试题库、招聘看板与 SLA 告警。完全本地推理，不爬抓简历库、不替代专业 HR / 律师判断。Use when 用户提到招聘、JD、岗位描述、候选人筛选、简历评分、面试题、面试评估、招聘看板、pipeline、HR、用人需求、社招、校招、内推。
---

# 中国小公司招聘助手（cn-recruit）

> 给 OPC / 一人公司 / 早期小团队一个**本地可跑、不依赖任何招聘 SaaS 账号**的招聘工具箱：
> 写 JD、给候选人打分、出结构化面试题、维护招聘看板。
>
> **本 skill 不替代专业 HR / 不替代用人经理判断**；评分模型是先验规则，仅供初筛参考；面试题库不构成法律或心理学测评。

## Prerequisites

### 账号要求
无。完全本地规则推理，不调用任何外部 API。

### 环境变量
无。

### 依赖
仅 stdlib。

## Quick Start

```bash
# 1) 生成一份后端工程师 JD
python3 scripts/jd.py "role=后端工程师|family=工程|seniority=中级|primary_stack=Go|product_line=客户成功平台|industry=SaaS|location=远程|salary=25-40k*15|tone=活泼|hr_email=hr@example.com|company_short_desc=AI Agent 创业团队"

# 2) 给候选人打分
python3 scripts/score.py '{
  "must_have_keywords": ["Go", "微服务", "K8s", "高并发"],
  "candidate": {
    "skills": ["Go", "K8s", "微服务"],
    "years": 4,
    "target_band": "中级",
    "industry": "SaaS",
    "target_industry": "SaaS",
    "tenures_years": [2.5, 3.1, 1.8],
    "highlights": ["开源贡献者", "技术博客"]
  }
}'

# 3) 出一份面试题包
python3 scripts/interview.py "family=工程|dimensions=技术深度,项目经验,解决问题|primary_stack=Go|product_line=客户成功平台"

# 4) 看板汇总 + 告警
python3 scripts/board.py '{
  "positions": [
    {"id": "P-001", "title": "后端工程师", "open_days": 18,
     "candidates": [
       {"name": "A", "stage": "screening", "days_in_stage": 4},
       {"name": "B", "stage": "tech1", "days_in_stage": 7},
       {"name": "C", "stage": "offer", "days_in_stage": 9}
     ]
    }
  ]
}'
```

## Usage Examples

### 场景 1：5 分钟出一份 JD 草稿
```bash
python3 scripts/jd.py "role=内容运营|family=运营|seniority=初级|industry=SaaS|product_line=AI Agent 工具|channel=小红书|tone=活泼|hr_email=hr@example.com|company_short_desc=面向 OPC 的 AI 工具品牌"
```
拿输出里的 `responsibilities` / `must_have` / `nice_to_have` 直接贴去拉勾 / Boss / 内推群。

### 场景 2：批量初筛（1 个 JD vs N 个简历）
1. 用 `jd.py` 输出的 `must_have` 提炼成关键词数组
2. 把每个候选人结构化字段塞进 `score.py`
3. 拿 `total_score >= 70` 的进电话沟通

### 场景 3：用人经理面试前 30 分钟
```bash
python3 scripts/interview.py "family=产品|dimensions=项目经验,技术深度,沟通协作|product_line=AI 客服"
```
得到结构化题库 + STAR 追问模板，直接贴进 Notion 当面评纪要。

### 场景 4：每周一早上招聘站会
```bash
python3 scripts/board.py "$(cat ./pipeline.json)"
```
重点看 `warnings` 里的 `stage_overdue` / `pipeline_too_thin` / `offer_long_silence`，对症做下一步动作。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/jd.py "<kv>"` | 生成 JD | `\|` 分隔 | JSON |
| `python3 scripts/score.py '<json>'` | 候选人打分 | JSON 字符串 | JSON |
| `python3 scripts/interview.py "<kv>"` | 面试题包 | `\|` 分隔 | JSON |
| `python3 scripts/board.py '<json>'` | 看板 + 告警 | JSON 字符串 | JSON |

## Scripts

### `scripts/jd.py`
按 `role_family`（工程 / 产品 / 设计 / 运营 / 销售 / 通用）+ `seniority`（实习/初级/中级/高级/专家）+ `tone`（正式/活泼/极简）拼装 JD。
模板池在 `references/jd_templates.json`。

### `scripts/score.py`
5 维加权评分：技能匹配（35）+ 经验年限（20）+ 行业相关（15）+ 履历稳定性（15）+ 亮点（15）。
阈值与红旗规则在 `references/score_rules.json`。仅做**初筛信号**，不替代用人经理判断。

### `scripts/interview.py`
按 `family × dimension` 出结构化题，每题附追问与 look_for；自带 STAR 通用追问模板。
题库在 `references/interview_bank.json`。

### `scripts/board.py`
聚合 pipeline，按 8 个标准阶段（sourcing → onboard）分桶，套 SLA 与三类告警（stage_overdue / pipeline_too_thin / offer_long_silence）。
配置在 `references/board_config.json`。

## API Info
本 skill 不调用任何外部 API。

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 输入没用 `key=value\|key=value` 格式 | 检查分隔符；值里有 `=` / `\|` 时考虑改用 JSON 输入 |
| `score.py` 总分偏低但人感觉合适 | 关键词没命中 | `must_have_keywords` 里加上候选人简历里的同义词；或人工覆盖 |
| `board.py` 报 `pipeline_too_thin` | 候选人池过薄 | 扩展渠道（内推 / 行业群 / 招聘平台同时挂） |

## References

- 配套 skill：`wecom-crm`（用企微沉淀候选人触达）、`feishu-ops`（飞书任务跟进 pipeline）、`cn-content-compliance`（招聘文案合规自检）
- 内置数据：`references/jd_templates.json`、`references/score_rules.json`、`references/interview_bank.json`、`references/board_config.json`

## Notes

- 评分规则是**先验规则**，不构成对候选人的最终评价；最终判断必须由用人经理结合面试与背调
- 题库不构成法律 / 心理学测评，避免使用与岗位无关的家庭、宗教、生育等问题
- PIPL 合规边界：本 skill 不收集、不存储、不外发任何候选人简历；所有数据仅在调用方进程内
- 不爬抓任何招聘平台数据；候选人结构化字段由调用方自行整理
