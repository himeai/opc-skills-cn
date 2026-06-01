# 5 分钟快速开始

本指南面向第一次使用 `opc-skills-cn` 的贡献者与使用者，帮助你在几分钟内完成安装、调用和本地验证。

## 1. 前置环境

- Python 3.10+（本仓库脚本以 Python 3 + stdlib 为默认运行环境）
- Node.js 与 `npx`（用于 `skills` CLI 安装测试）
- Git

## 2. 获取仓库

```bash
git clone <your-fork-or-repo-url>
cd opc-skills-cn
```

## 3. 本地检查当前已实现 skill

当前仓库已实现并注册的 skill 为：

- `cn-city-picker`

可查看注册表：

```bash
python3 -c "import json; print([skill['name'] for skill in json.load(open('skills.json'))['skills']])"
```

## 4. 直接运行 cn-city-picker

```bash
cd skills/cn-city-picker
python3 scripts/pick.py "跨境电商独立站，月预算 1.5 万，怕冷不爱辣，倾向南方非一线"
python3 scripts/profile.py 厦门
python3 scripts/compare.py 厦门 杭州 成都
```

返回结果分别为：

- `pick.py`：JSON 推荐结果
- `profile.py`：单城市档案 JSON
- `compare.py`：Markdown 对比表与雷达图原始数据

## 5. 运行仓库校验

在仓库根目录执行：

```bash
python3 scripts/validate_skill_md.py skills/cn-city-picker/SKILL.md
python3 scripts/check_registry_consistency.py
python3 -m pylint skills/cn-city-picker/scripts/*.py --disable=C0114,C0115,C0116
```

## 6. 模拟安装 skill

若本机已安装 `skills` CLI，可用本地仓库路径做模拟安装：

```bash
npx skills add file:///ABSOLUTE/PATH/TO/opc-skills-cn --skill cn-city-picker -y --copy
```

如需安装到特定 agent，可追加 `-a claude-code` 或其它 agent 名称。

## 7. 下一步

- 如果你准备新增一个 skill，推荐先打开 [`.factory/skills/add-new-skill/SKILL.md`](../.factory/skills/add-new-skill/SKILL.md)，按里面的 checklist 执行。
- 如果你需要核对注册表格式，先看 [skills.json 字段说明](./skills-json-schema.md)。
- 想开发新 skill：看 [skill-authoring.md](./skill-authoring.md)
- 想理解合规边界：看 [compliance.md](./compliance.md)
- 想查看路线图：看 [../ROADMAP.md](../ROADMAP.md)
