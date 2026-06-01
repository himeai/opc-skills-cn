---
name: add-new-skill
description: 返回在 opc-skills-cn 仓库中新增一个 skill 的完整 checklist 与校验步骤。Use when 用户提到新增 skill、创建 skill、贡献 skill、补齐注册表、更新 marketplace、添加 logo、运行校验脚本。
---

# 新增 Skill 流程助手

> 这是给 contributor 和 coding agent 用的流程型 skill，用于把“新增一个 skill”拆成可执行清单，避免遗漏目录、注册表、校验命令与合规边界。

## Prerequisites

### 环境变量
无需额外环境变量。

### 账号要求
- 对仓库有写权限
- 能运行 Python 3 与仓库内校验脚本

## Quick Start

当用户提出“新增一个 skill”时，返回以下最小清单：

1. 读取 `README.md` 与 `AGENTS.md`
2. 复制 `template/SKILL.md` 到 `skills/<skill-name>/SKILL.md`
3. 创建 `scripts/credential.py` 与业务脚本
4. 添加 `skill-logos/<skill-name>.svg`
5. 更新 `skills.json`、`.claude-plugin/marketplace.json`、`README.md`、`CHANGELOG.md`
6. 运行 frontmatter、注册一致性、lint 等校验

## Commands

| 命令 | 说明 |
|---|---|
| `python3 scripts/new_skill.py <skill-name>` | 生成目录骨架与占位 `credential.py` |
| `python3 scripts/validate_skill_md.py skills/<skill-name>/SKILL.md` | 校验 frontmatter |
| `python3 scripts/check_registry_consistency.py` | 校验注册一致性 |

## Checklist

### 1. 命名检查
- 确认 skill 名符合 `AGENTS.md` 第 2 节三档命名规约
- 使用 kebab-case，小写，长度不超过 24

### 2. 结构创建
- `skills/<skill-name>/SKILL.md`
- `skills/<skill-name>/scripts/credential.py`
- 至少一个业务脚本
- 视需要补 `examples/`、`references/`

### 3. 文档与注册
- `skill-logos/<skill-name>.svg`
- `skills.json`
- `.claude-plugin/marketplace.json`
- `README.md` Skills 表格
- `CHANGELOG.md`

### 4. 合规复核
- 不包含爬虫、群发、协议逆向、刷量逻辑
- 凭证全部来自环境变量
- 涉及个人信息时说明 PIPL 边界

### 5. 提交前校验
```bash
python3 scripts/validate_skill_md.py skills/<skill-name>/SKILL.md
python3 scripts/check_registry_consistency.py
python3 -m pylint skills/<skill-name>/scripts/*.py --disable=C0114,C0115,C0116
```

## Notes

- 本 skill 不直接修改仓库文件，只返回新增 skill 的完整执行清单。
- 若仓库尚无 `scripts/check_registry_consistency.py` 或 `scripts/validate_skill_md.py`，应先创建这两个基础设施脚本。
