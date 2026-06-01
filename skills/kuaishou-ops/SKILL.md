---
name: kuaishou-ops
description: 快手短视频内容生产副驾驶：从一句话主题生成"老铁文化"风格的口播脚本、3 段式分镜、本地工程 JSON、同城/老铁话题候选，全部基于本地模板与规则模型，不爬抓也不刷量。Use when 用户提到快手、老铁、同城、短视频、口播、脚本、分镜、磁力金牛、电商直播带货、ks。
---

# 快手脚本工厂（kuaishou-ops）

> 快手生态的核心是"老铁文化 + 同城信任 + 直播带货"。本 skill 把"主题 → 老铁口播 → 分镜 → 直播带货话术"前几步结构化输出，后续拍摄、直播留给真人。

## Prerequisites

### 环境变量
```bash
# 全部可选，未配置时仅本地推理
export KUAISHOU_OPS_OPEN_TOKEN=""    # 可选：快手开放平台 access_token，未配置则跳过实时数据查询
```

### 账号要求
无强制。本 skill 主功能为**本地内容生成**，不需要登录快手账号。

### 依赖
仅 stdlib。

### 合规边界
- 不爬抓快手任何页面、用户内容、推荐流、直播间
- 不做批量发布、刷赞、刷评、互关、群发私信、刷直播间人气
- "爆款"措辞仅作结构参考，不保证流量
- 直播带货话术仅作脚本参考，主播需对货品质量与广告合规自行负责

## Quick Start

```bash
# 1. 主题 → 60 秒老铁口播脚本
python3 scripts/script.py "县城超市利润真相|老铁|普通人"

# 2. 把脚本扩成分镜表（每镜文案/画面/时长）
python3 scripts/storyboard.py "县城超市利润真相|老铁|普通人"

# 3. 输出直播带货话术（30 分钟）
python3 scripts/live.py "9.9 元应季水果|生鲜|宝妈"
```

预期输出（节选）：
```json
{
  "duration_sec": 60,
  "shots": [
    {"index": 1, "duration": 5, "voiceover": "老铁们看好...", "visual": "...", "subtitle": "..."}
  ]
}
```

## Usage Examples

### 场景 1：每周 3 条老铁口播主题排期
```bash
python3 scripts/script.py "县城开店选品的 3 条铁律|老铁|创业者"
```

### 场景 2：把口播扩成分镜表
```bash
python3 scripts/storyboard.py "县城开店选品的 3 条铁律|老铁|创业者"
```

### 场景 3：直播带货 30 分钟话术
```bash
python3 scripts/live.py "9.9 元应季水果|生鲜|宝妈"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/script.py "<topic>\|<style>\|<audience>"` | 60 秒老铁口播脚本 | `\|` 分隔 | JSON：开场/正文/收尾 |
| `python3 scripts/storyboard.py "<topic>\|<style>\|<audience>"` | 分镜表（默认 6 镜） | `\|` 分隔 | JSON：shots[] |
| `python3 scripts/live.py "<product>\|<category>\|<audience>"` | 直播带货 30 分钟话术 | `\|` 分隔 | JSON：phases[] |

## Scripts

### `scripts/credential.py`
读取可选 `KUAISHOU_OPS_OPEN_TOKEN`。无强制。

### `scripts/script.py`
- **职责**：基于 `references/script_templates.json` 的老铁式 5 段（喊话/共情/事实/反转/CTA）输出口播
- **输入**：`topic|style|audience`
- **输出**：JSON：opening、empathy、fact、twist、cta

### `scripts/storyboard.py`
- **职责**：把脚本映射为 6 个镜头（默认 60s / 6 镜 ≈ 每镜 10s），每镜含 voiceover、visual、subtitle、duration

### `scripts/live.py`
- **职责**：基于 `references/live_templates.json`，输出 30 分钟直播 6 阶段话术骨架（暖场/讲解/痛点/福利/逼单/收尾），不带任何虚假宣传话术

## 数据架构

```
references/
├── script_templates.json   # 风格 × 段式 × 老铁钩子模板
├── style_meta.json         # 风格定义（口吻 / BGM / 字幕）
└── live_templates.json     # 直播话术骨架（6 阶段）
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **可选实时源**：快手开放平台 https://open.kuaishou.com（用户自行配置 token 后启用）

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| 脚本风格不对 | 风格名不在种子库 | 在 `references/style_meta.json` 提 PR 增加 |
| 直播话术无效 | 类目不在种子库 | 在 `references/live_templates.json` 补充类目 |

## References

- 快手开放平台：https://open.kuaishou.com
- 磁力金牛（电商）：https://niu.e.kuaishou.com
- 相关 skill：`douyin-ops`、`xiaohongshu-ops`、`bilibili-ops`

## Notes

- 本 skill **不爬取快手**，所有输出基于本地模板 + 规则
- "老铁文化"模板仅是结构参考，真实信任来自主播本人长期输出
- 直播带货话术不包含夸大/绝对化表述，主播仍需对广告法合规自行负责
- 严禁用本 skill 实现刷量、批量发布、机器人评论、刷直播间人气
