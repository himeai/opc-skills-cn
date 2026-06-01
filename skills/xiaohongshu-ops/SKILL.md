---
name: xiaohongshu-ops
description: 小红书内容生产副驾驶：选题工厂、笔记结构化生成（标题/封面文案/正文/tag）、关键词与话题推荐，全部基于本地种子库与规则模型，不做爬虫与刷量。Use when 用户提到小红书、笔记、xhs、爆款标题、选题、话题、关键词、tag、种草文案、封面文案、薯队长。
---

# 小红书内容运营（xiaohongshu-ops）

> 一人公司主理人最常见的内容输出场景：每天 1-2 篇小红书。本 skill 用本地种子库 + 规则模板把"选题 → 标题 → 正文 → tag"流程结构化，把博主的精力从找词找选题里救出来，专注于真实经验输出。

## Prerequisites

### 环境变量
```bash
# 全部可选 - 用于将来对接小红书蒲公英开放平台
export XIAOHONGSHU_OPS_DANDELION_TOKEN=""   # 可选：蒲公英 API token，未配置时仅本地推理
```

### 账号要求
无强制。本 skill 主功能为**本地内容生成**，不需要登录小红书账号即可使用。

### 依赖
仅 stdlib。

### 合规边界
- 不爬抓小红书任何页面 / 接口 / 用户内容
- 不做批量发布、刷量、刷评论、互关
- 涉及"爆款"措辞仅作参考，不保证流量结果
- 真实数据指标（在线趋势 / 实时热度）需用户自行从合规渠道补充

## Quick Start

```bash
# 1. 选题工厂：行业 + 受众 → 10 个选题
python3 scripts/topic.py "护肤|25-30 岁敏感肌女性|国货平价"

# 2. 把一个选题生成结构化笔记草稿
python3 scripts/note.py "国货平价精华怎么选|护肤|25-30 岁敏感肌女性|经验分享口吻"

# 3. 关键词 / tag 推荐
python3 scripts/keywords.py "国货平价精华|护肤"
```

预期输出（节选）：
```json
{
  "title_candidates": ["⚠️ 敏感肌别再乱用了！这 3 支国货精华我用了半年", "..."],
  "cover_copy": "敏感肌也能用",
  "body_outline": ["痛点钩子", "成分对比", "用法步骤", "结果对比", "避雷提醒"],
  "tags": ["#敏感肌护肤", "#国货之光", "#精华推荐"]
}
```

## Usage Examples

### 场景 1：每周选题表
```bash
python3 scripts/topic.py "母婴|0-1 岁新手妈妈|辅食工具"
```

### 场景 2：把灵感扩成完整笔记草稿
```bash
python3 scripts/note.py "我用 60 元搞定的婴儿辅食工具|母婴|0-1 岁新手妈妈|测评口吻"
```

### 场景 3：盘点一个产品的关键词矩阵
```bash
python3 scripts/keywords.py "辅食研磨碗|母婴"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/topic.py "<行业>\|<受众>\|<细分>"` | 选题工厂 | `\|` 分隔 | JSON：10 选题 |
| `python3 scripts/note.py "<选题>\|<行业>\|<受众>\|<口吻>"` | 笔记草稿 | `\|` 分隔 | JSON：标题/封面/正文/tag |
| `python3 scripts/keywords.py "<产品/词>\|<行业>"` | 关键词矩阵 | `\|` 分隔 | JSON：核心 + 长尾 + tag |

## Scripts

### `scripts/credential.py`
读取可选 `XIAOHONGSHU_OPS_DANDELION_TOKEN`。无强制。

### `scripts/topic.py`
- **职责**：基于 `references/topic_seeds.json` 的种子模式，结合行业/受众/细分输出 10 个选题
- **输入**：`industry|audience|niche`
- **输出**：JSON `{topics: [{title, angle, hook_type}, ...]}`

### `scripts/note.py`
- **职责**：基于 `references/note_templates.json`，把选题扩成结构化笔记草稿
- **输入**：`topic|industry|audience|tone`
- **输出**：JSON：title_candidates、cover_copy、body_outline、tags

### `scripts/keywords.py`
- **职责**：基于 `references/keyword_seeds.json`，输出核心词、长尾词、tag 候选
- **输入**：`product|industry`

## 数据架构

```
references/
├── topic_seeds.json       # 行业 × 受众 × 角度 选题模板库
├── note_templates.json    # 笔记结构模板库（钩子 / 正文 / 收尾）
└── keyword_seeds.json     # 行业关键词种子库
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **可选实时源**：
  - 小红书蒲公英开放平台：https://pgy.xiaohongshu.com（仅在用户配置 token 后启用）

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| 输出选题过于通用 | 受众/细分填得太宽 | 把"敏感肌"改成"25-30 岁敏感肌泛红泛油" |
| tag 数量过少 | 行业不在种子库 | 在 `references/keyword_seeds.json` 提 PR 补充 |

## References

- 小红书蒲公英官方文档：https://pgy.xiaohongshu.com
- 相关 skill：`wechat-ops`、`douyin-ops`、`cn-geo`

## Notes

- 本 skill **不爬取小红书**，所有输出基于本地种子库 + 规则模板
- 所谓"爆款"模板仅是结构参考，真实流量需要博主真实经验与表达
- 严禁用本 skill 实现刷量、刷评论、批量发布
