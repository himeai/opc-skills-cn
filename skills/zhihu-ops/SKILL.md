---
name: zhihu-ops
description: 知乎内容生产副驾驶（本地规则版）：长回答结构化生成（科普/干货/经验/对比/反驳）、专栏长文骨架、问题选题工厂、领域 tag 推荐。完全本地推理，不爬抓不刷量。Use when 用户提到知乎、zhihu、回答、长答、专栏、知乎选题、知乎话题、领域 tag、盐选、好评率、高赞回答、知乎 SEO。
---

# 知乎内容生产副驾驶（zhihu-ops）

> 给 OPC / 一人公司 / 行业从业者一个**本地可跑、不依赖知乎账号**的内容生产工具箱：
> 出长回答骨架、出专栏长文骨架、出问题选题、推荐领域 tag。
>
> 本 skill **不爬抓**任何知乎数据、**不发**任何内容、**不刷**任何指标，仅做内容生产辅助。

## Prerequisites

### 账号要求
无。

### 环境变量
无。

### 依赖
仅 stdlib。

## Quick Start

```bash
# 1) 给一个具体问题出长回答骨架（科普向）
python3 scripts/answer.py "question=如何评价 AI Agent 在客服场景的真实落地效果？|style=科普|industry=AI|years=4"

# 2) 给一个话题出专栏长文骨架（深度分析）
python3 scripts/column.py "topic=AI Agent 商业化|style=深度分析|industry=AI|year=2026|n=5"

# 3) 给一个领域生成一批选题
python3 scripts/topic.py "domain=AI / 大模型|target=AI Agent|year=2026|n=5|scene=客服"

# 4) 给一篇内容推荐 tag
python3 scripts/tag.py "domain=AI / 大模型|keywords=AI Agent,Prompt,SaaS|max=5"
```

## Usage Examples

### 场景 1：刷到一个高热新问题，30 分钟出一个高质量长回答
1. 用 `answer.py` 选 `style=干货` 拿到结构化骨架
2. 按 outline 逐段填充自己的真实经验（重点：每段都要有可证伪信息）
3. 用 `tag.py` 给问题选 5 个最贴合的 tag，避免「生活」这种宽泛 tag

```bash
python3 scripts/answer.py "question=如何系统地从 0 学习 AI Agent 开发？|style=干货|industry=AI|years=3"
python3 scripts/tag.py "domain=AI / 大模型|keywords=AI Agent,Prompt,LangGraph"
```

### 场景 2：每周出一篇专栏长文（深度分析）
```bash
python3 scripts/column.py "topic=企微私域是不是被高估了|style=深度分析|industry=SaaS|year=2026|n=5"
```
拿到 7 段骨架（导语 → 现象 → 数据 → 三层归因 → 演化路径 → 启示 → 结尾），照着填即可。

### 场景 3：每月做一次选题盘点
```bash
python3 scripts/topic.py "domain=创业 / 副业|target=独立开发者|year=2026|n=5"
```
预计返回 8 条选题，从中挑 3-4 个落到周更日历里。

### 场景 4：发文前 tag 自检
```bash
python3 scripts/tag.py "domain=职场 / 求职|keywords=面试,简历,大厂,跳槽|max=5"
```
- `tags` 是建议挂上的（按规则去重 + canonical 化）
- `related_tags` 是溢出的，可以放到正文小标题
- `dropped` 是没匹配上词库的，要么补到 `tag_lexicon.json`，要么换个说法

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/answer.py "<kv>"` | 长回答骨架 | `\|` 分隔 | JSON |
| `python3 scripts/column.py "<kv>"` | 专栏长文骨架 | `\|` 分隔 | JSON |
| `python3 scripts/topic.py "<kv>"` | 选题工厂 | `\|` 分隔 | JSON |
| `python3 scripts/tag.py "<kv>"` | tag 推荐 | `\|` 分隔 | JSON |

## Scripts

### `scripts/answer.py`
按 5 种答案体裁（科普 / 干货 / 经验 / 对比 / 反驳）拼装骨架；附 3 个钩子候选 + 2 个结尾互动模板。
模板在 `references/answer_templates.json`。

### `scripts/column.py`
按 4 种专栏体裁（深度分析 / 行业拆解 / 个人成长 / 案例复盘）拼装骨架；附 3 个标题候选。
模板在 `references/column_templates.json`。

### `scripts/topic.py`
按 6 大领域（互联网产品 / AI / 创业 / 职场 / 理财 / 健康）× 多个角度（趋势 / 经验 / 方法 / 对比）批量出选题。
种子库在 `references/topic_seeds.json`。

### `scripts/tag.py`
把自由关键词归一到 canonical tag，并叠加领域默认 tag，按 max=5 截断。
词库在 `references/tag_lexicon.json`。

## API Info
本 skill 不调用任何外部 API。

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `topic.py` 出来的题不够垂直 | 选错了 domain | 在 `topic_seeds.json` 里查可用 domain；或 fork 后追加你的细分领域 |
| `tag.py` 给出泛 tag 太多 | 词库覆盖不全 | 在 `tag_lexicon.json` 的 `tag_clusters` 里补 alias |
| 输出体感像 AI 写的 | 骨架是骨架，肉要你自己长 | 每段必须填一手案例 / 数据 / 截图，不要照模板编造 |

## References

- 配套 skill：`xiaohongshu-ops`（小红书短笔记）、`bilibili-ops`（B 站长视频/专栏）、`cn-content-compliance`（发文前合规自检）、`cn-geo`（让你的回答被 AI 搜索引用）

## Notes

- **不爬抓**任何知乎页面 / 用户 / 问题数据
- **不发布**任何内容（知乎个人账号没有官方开放 API 用于发布）
- 骨架只是骨架，**核心信息密度由你来填**，否则发出来读者一眼能看出是模板
- 选题与 tag 推荐基于本地种子库，需要你按行业 fork 后补充才更精准
