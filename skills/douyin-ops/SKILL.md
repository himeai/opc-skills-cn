---
name: douyin-ops
description: 抖音/视频号短视频副驾驶：从一句话主题生成口播脚本、3 段式分镜、本地剪映工程 JSON、热点话题候选，全部基于本地模板与规则模型，不爬抓也不刷量。Use when 用户提到抖音、视频号、短视频、口播、脚本、分镜、剪映、capcut、热点话题、tag、爆款视频。
---

# 抖音/视频号脚本工厂（douyin-ops）

> 一人公司主理人最高 ROI 的短视频流程不是"全自动剪辑"，而是"主题 → 口播脚本 → 分镜 → 拍摄拍清楚 → 剪映里堆字幕 BGM"。本 skill 把前三步结构化输出，把后两步留给真人。

## Prerequisites

### 环境变量
```bash
# 全部可选，未配置时仅本地推理
export DOUYIN_OPS_OPEN_TOKEN=""    # 可选：抖音开放平台 access_token，未配置则跳过实时热点查询
```

### 账号要求
无强制。本 skill 主功能为**本地内容生成**，无需登录抖音。

### 依赖
仅 stdlib。

### 合规边界
- 不爬抓抖音/视频号任何页面、用户内容、推荐流
- 不做批量发布、刷赞、刷评、互关、群发私信
- 所谓"爆款结构"仅是结构参考，不保证流量
- 涉及他人作品的二创需用户自行确认版权与平台规则

## Quick Start

```bash
# 1. 主题 → 60 秒口播脚本
python3 scripts/script.py "副业搞钱方向选择|knowhow|新手"

# 2. 把脚本扩成分镜表（每镜文案/画面/时长）
python3 scripts/storyboard.py "副业搞钱方向选择|knowhow|新手"

# 3. 输出剪映可导入的工程 JSON 骨架
python3 scripts/capcut.py "副业搞钱方向选择|knowhow|新手"
```

预期输出（节选）：
```json
{
  "duration_sec": 60,
  "shots": [
    {"index": 1, "duration": 5, "voiceover": "...", "visual": "...", "subtitle": "..."}
  ]
}
```

## Usage Examples

### 场景 1：每周 3 条口播主题排期
```bash
python3 scripts/script.py "我用 ChatGPT 1 小时干完一周活|效率|职场新人"
```

### 场景 2：把口播扩成分镜表，交给摄影师
```bash
python3 scripts/storyboard.py "我用 ChatGPT 1 小时干完一周活|效率|职场新人"
```

### 场景 3：剪映工程 JSON 骨架（仅含字幕轨与时间码）
```bash
python3 scripts/capcut.py "我用 ChatGPT 1 小时干完一周活|效率|职场新人"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/script.py "<topic>\|<style>\|<audience>"` | 60 秒口播脚本 | `\|` 分隔 | JSON：开场/正文/收尾 |
| `python3 scripts/storyboard.py "<topic>\|<style>\|<audience>"` | 分镜表（默认 6 镜） | `\|` 分隔 | JSON：shots[] |
| `python3 scripts/capcut.py "<topic>\|<style>\|<audience>"` | 剪映工程 JSON 骨架 | `\|` 分隔 | JSON：tracks/字幕 |

## Scripts

### `scripts/credential.py`
读取可选 `DOUYIN_OPS_OPEN_TOKEN`。无强制。

### `scripts/script.py`
- **职责**：基于 `references/script_templates.json` 的 5 段式开场/钩子/反转/结论/CTA，按风格输出口播
- **输入**：`topic|style|audience`
- **输出**：JSON：opening、body、closing

### `scripts/storyboard.py`
- **职责**：把 `script.py` 的内容映射为 6 个镜头（默认 60s / 6 镜 ≈ 每镜 10s），每镜含 voiceover、visual、subtitle、duration

### `scripts/capcut.py`
- **职责**：基于分镜，输出剪映 (CapCut) 可作为参考的工程 JSON 骨架（仅字幕轨 + 时间码 + 镜头切点），用户自行在剪映里导入素材

## 数据架构

```
references/
├── script_templates.json   # 风格 × 段式 × 钩子模板
├── style_meta.json         # 风格定义（口吻 / BGM 倾向 / 字幕风格）
└── hot_topics.example.json # 用户自维护的热点话题示例
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **可选实时源**：抖音开放平台 https://developer.open-douyin.com（用户自行配置 token 后启用，本 skill 不替用户登录）

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| 脚本风格不对 | 风格名不在种子库 | 在 `references/style_meta.json` 提 PR 增加 |
| 剪映打不开 JSON | 剪映版本字段不兼容 | 当前 JSON 仅作骨架参考，正式导入需用户对齐自己版本 |

## References

- 抖音开放平台：https://developer.open-douyin.com
- 微信视频号：https://channels.weixin.qq.com
- 相关 skill：`wechat-ops`、`xiaohongshu-ops`、`cn-geo`

## Notes

- 本 skill **不爬取抖音**，所有输出基于本地模板 + 规则
- 剪映工程 JSON 仅作骨架参考，剪映闭源格式可能版本变更，请以剪映官方为准
- 严禁用本 skill 实现刷量、批量发布、机器人评论、二创洗稿
