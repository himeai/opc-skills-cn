---
name: bilibili-ops
description: B 站长视频与图文内容生产副驾驶：从一句话主题生成 10-15 分钟三段式脚本、章节大纲、动态/专栏文案、tag 推荐，全部基于本地模板与规则模型，不爬抓也不刷数据。Use when 用户提到 B 站、bilibili、UP 主、长视频、专栏、动态、稿件、章节、必剪、bv、av、三连。
---

# B 站长视频脚本工厂（bilibili-ops）

> 抖音/快手是短视频，小红书是图文，B 站独特的位置是"长视频 + 强章节 + 弹幕互动"。本 skill 为 UP 主把"主题 → 长视频脚本 → 章节大纲 → 动态/专栏文案"这一段流程结构化，把后续录制、剪辑、答弹幕留给真人。

## Prerequisites

### 环境变量
```bash
# 全部可选，未配置时仅本地推理
export BILIBILI_OPS_OPEN_TOKEN=""    # 可选：B 站开放平台 token，未配置则跳过实时数据查询
```

### 账号要求
无强制。本 skill 主功能为**本地内容生成**，不需要登录 B 站。

### 依赖
仅 stdlib。

### 合规边界
- 不爬抓 B 站任何页面、稿件、用户、弹幕、评论
- 不做批量发布、刷三连、刷弹幕、刷评论、机器人互动
- "爆款结构"仅作参考，不保证流量
- 涉及他人作品的二创/搬运请用户自行确认版权与平台规则

## Quick Start

```bash
# 1. 主题 → 12 分钟长视频三段式脚本
python3 scripts/script.py "我用 30 天搭建一人公司|knowhow|创业新人"

# 2. 把脚本扩成章节大纲（含时间码 + 章节标题）
python3 scripts/chapters.py "我用 30 天搭建一人公司|knowhow|创业新人"

# 3. 输出动态 / 专栏文案
python3 scripts/post.py "我用 30 天搭建一人公司|创业|动态"
```

预期输出（节选）：
```json
{
  "duration_min": 12,
  "sections": {"intro": "...", "body": [...], "outro": "..."}
}
```

## Usage Examples

### 场景 1：长视频脚本起手
```bash
python3 scripts/script.py "Mac mini M4 一年使用复盘|测评|程序员"
```

### 场景 2：把脚本切章节
```bash
python3 scripts/chapters.py "Mac mini M4 一年使用复盘|测评|程序员"
```

### 场景 3：稿件配套动态/专栏文案
```bash
python3 scripts/post.py "Mac mini M4 一年使用复盘|测评|动态"
python3 scripts/post.py "Mac mini M4 一年使用复盘|测评|专栏"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/script.py "<topic>\|<style>\|<audience>"` | 三段式长视频脚本 | `\|` 分隔 | JSON：intro/body/outro |
| `python3 scripts/chapters.py "<topic>\|<style>\|<audience>"` | 章节大纲（默认 6 章 + 时间码） | `\|` 分隔 | JSON：chapters[] |
| `python3 scripts/post.py "<topic>\|<category>\|<format>"` | 动态/专栏文案 | `\|` 分隔 | JSON：title、body、tags |

## Scripts

### `scripts/credential.py`
读取可选 `BILIBILI_OPS_OPEN_TOKEN`。无强制。

### `scripts/script.py`
- **职责**：基于 `references/script_templates.json`，把主题扩成 12 分钟三段式脚本（intro 钩子 / body 主章节 / outro 三连引导）
- **输入**：`topic|style|audience`
- **输出**：JSON：intro、body、outro

### `scripts/chapters.py`
- **职责**：基于 `references/chapter_meta.json`，把脚本切为章节大纲（默认 6 章），生成时间码与章节标题，方便剪辑里直接打章节点

### `scripts/post.py`
- **职责**：基于 `references/post_templates.json` 输出 B 站动态或专栏文案，含标题、正文、tag

## 数据架构

```
references/
├── script_templates.json   # 长视频三段式模板（按风格分类）
├── chapter_meta.json       # 章节风格元数据（时长 / 标题模式）
└── post_templates.json     # 动态 / 专栏文案模板
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **可选实时源**：B 站开放平台 https://open.bilibili.com（用户自行配置 token 后启用）

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| 章节时长不平均 | 总时长无法整除 | 余数会自动补到前面章节 |
| 风格不在种子库 | style 名拼写错误 | 在 `references/script_templates.json` 提 PR 增加 |

## References

- B 站开放平台：https://open.bilibili.com
- 创作者中心：https://member.bilibili.com
- 相关 skill：`xiaohongshu-ops`、`douyin-ops`、`kuaishou-ops`

## Notes

- 本 skill **不爬取 B 站**，所有输出基于本地模板 + 规则
- 三段式与章节模板仅是结构参考，UP 主真实输出仍取决于专业度与表达
- 严禁用本 skill 实现刷三连、刷弹幕、刷评论、批量发布
