# Skill 开发手册

本手册是给人类 contributor 看的长版说明；若你是 coding agent，还应先读根目录 [AGENTS.md](../AGENTS.md)。

## 1. 开发目标

每个 skill 都应满足以下要求：

- 可被 `npx skills add` 安装
- 目录独立，不跨 skill 共享代码
- 以 Python 3 + stdlib 为默认实现方式
- 凭证全部从环境变量读取
- 不触碰仓库规定的合规红线

## 2. 命名规约

命名只允许三档：

1. 中国平台专属能力：平台名前缀，如 `wechat-mp`
2. 中国通用能力：`cn-` 前缀，如 `cn-tax`
3. 海外或全球通用能力：不加前缀，如 `feishu-ops`

补充要求：

- 全小写 kebab-case
- 长度不超过 24
- 禁止以 `-skill` 或 `-skills` 结尾

## 3. 标准目录结构

```text
skills/<skill-name>/
├── SKILL.md
├── scripts/
│   ├── credential.py
│   └── *.py
├── examples/
└── references/
```

允许的子目录只有 `scripts/`、`examples/`、`references/`。

## 4. SKILL.md 写法

frontmatter 只能有两个字段：

```yaml
---
name: your-skill-name
description: 一句话说明 skill 做什么。Use when 用户提到触发关键词1、触发关键词2。
---
```

正文最少要有：

- `## Prerequisites`
- `## Quick Start`
- `## Commands`

建议参考：

- [template/SKILL.md](../template/SKILL.md)
- [skills/cn-city-picker/SKILL.md](../skills/cn-city-picker/SKILL.md)

## 5. 脚本规范

- 使用 `#!/usr/bin/env python3`
- 默认从 skill 根目录调用
- 入口脚本接收单个字符串参数
- stdout 输出结构化结果，JSON 优先
- stderr 输出错误或日志
- 非成功退出时返回非 0

## 6. 凭证规范

每个 skill 必须有 `scripts/credential.py`，例如：

```python
import os

def get_credentials() -> dict[str, str | None]:
    return {
        "app_id": os.environ.get("WECHAT_MP_APP_ID"),
        "app_secret": os.environ.get("WECHAT_MP_APP_SECRET"),
    }
```

禁止：

- 把 token 写进 `.py`、`.md`、`.json`
- 提交 `.env` 或 `.env.local`

## 7. 注册位置

新增 skill 时必须同步更新：

- [`skills.json`](../skills.json)
- [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)
- [`README.md`](../README.md)
- [`CHANGELOG.md`](../CHANGELOG.md)

## 8. Logo 规范

- 放在 `skill-logos/<skill-name>.svg`
- 24x24 像素风
- 主色与 `skills.json` 的 `color` 字段一致

## 9. 本地校验流程

```bash
python3 scripts/validate_skill_md.py skills/<skill-name>/SKILL.md
python3 scripts/check_registry_consistency.py
python3 -m pylint skills/<skill-name>/scripts/*.py --disable=C0114,C0115,C0116
```

## 10. 推荐工作流

1. 复制模板或运行 `python3 scripts/new_skill.py <skill-name>`
2. 补齐 `SKILL.md`
3. 实现 `credential.py` 与业务脚本
4. 加 logo
5. 更新注册表与 README
6. 跑校验
7. 自检合规边界

## 11. 参考资料

- [AGENTS.md](../AGENTS.md)
- [5 分钟快速开始](./quickstart.md)
- [中国合规边界详解](./compliance.md)
- [ROADMAP.md](../ROADMAP.md)
