---
name: skill-name-here
description: 一句话讲清楚这个 skill 做什么。Use when 用户提到关键词1、关键词2、关键词3，或者用户的意图涉及具体场景描述。
---

# Skill 中文名

> 一段话介绍这个 skill 的价值主张：为谁解决什么问题，凭什么这么解决。

## Prerequisites

### 环境变量
```bash
export SKILL_NAME_API_KEY="<your-key>"          # 必需，xxx 平台申请
export SKILL_NAME_OPTIONAL_FIELD="<value>"       # 可选，默认 xxx
```

### 账号要求
- xxx 平台已开通 xxx 权限（链接：https://...）
- 已完成 xxx 认证 / 备案

### 依赖（如有第三方库）
```bash
pip install xxx     # 仅当 stdlib 无法完成时
```

## Quick Start

最小可运行示例（30 秒上手）：

```bash
python3 scripts/main.py "请帮我做一件具体的事情"
```

预期输出：
```json
{"status": "ok", "result": "..."}
```

## Usage Examples

### 场景 1：xxx
用户输入："..."

执行：
```bash
python3 scripts/xxx.py "..."
```

### 场景 2：xxx
（同上结构）

### 场景 3：xxx
（同上结构）

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/main.py "<query>"` | 主入口 | 自然语言指令 | JSON |
| `python3 scripts/xxx.py --help` | 子命令 | 见 --help | ... |

## Scripts

### `scripts/main.py`
- **职责**：xxx
- **输入**：单个字符串参数
- **输出**：stdout JSON，stderr 日志
- **退出码**：0=成功，2=凭证缺失,1=其它失败

### `scripts/credential.py`
统一从环境变量读取凭证，禁止硬编码。

## API Info

- **Base URL**: `https://api.xxx.com/v1`
- **Auth**: API Key（Header: `Authorization: Bearer xxx`）
- **Rate Limits**: xxx QPS / xxx 次每天
- **Docs**: https://...

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: missing credential` | 未配置环境变量 | 参考 Prerequisites 配置 |
| `429 Too Many Requests` | 触发限流 | 脚本会自动重试；持续失败请升级套餐 |

## References

- 官方 API 文档：https://...
- 相关 skill：`other-skill-name`

## Notes

- 本 skill **仅调用平台官方 / 开放 API**，不包含任何爬虫、协议逆向、批量行为
- 涉及用户数据时遵循 PIPL：xxx
- 已知限制：xxx
