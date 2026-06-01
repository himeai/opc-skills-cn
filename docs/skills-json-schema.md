# skills.json 字段说明与固定格式示例

本文件用于说明根目录 `skills.json` 的注册项结构，帮助 contributor 在新增 skill 时保持字段一致、命名统一、安装命令可用。

## 1. 顶层结构

```json
{
  "$schema": "https://example.invalid/opc-skills-cn/skills.schema.json",
  "_comment": {"...": "字段说明"},
  "skills": [
    {
      "name": "your-skill-name",
      "version": "0.1.0",
      "description": "一句话说明用途。",
      "logo": "skill-logos/your-skill-name.svg",
      "icon": "tool",
      "color": "2E7CF6",
      "triggers": ["关键词1", "关键词2"],
      "dependencies": {},
      "auth": {
        "required": true,
        "type": "api_key",
        "keys": []
      },
      "install": {
        "user": {"claude": "npx skills add <YOUR_ORG>/opc-skills-cn --skill your-skill-name -a claude"},
        "project": {"claude": "npx skills add <YOUR_ORG>/opc-skills-cn --skill your-skill-name"}
      },
      "commands": ["python3 scripts/main.py \"{input}\""],
      "links": {"github": "https://github.com/<YOUR_ORG>/opc-skills-cn/tree/main/skills/your-skill-name"}
    }
  ]
}
```

## 2. 字段逐项说明

### `name`
- 类型：字符串
- 要求：与 `skills/<name>/` 目录名完全一致
- 命名：kebab-case，全小写

### `version`
- 类型：字符串
- 要求：语义化版本，例如 `0.1.0`

### `description`
- 类型：字符串
- 要求：一句话说明 skill 做什么
- 建议：与 `SKILL.md` frontmatter 中的用途描述保持一致，但无需重复完整 `Use when`

### `logo`
- 类型：字符串
- 要求：指向 `skill-logos/<name>.svg`

### `icon`
- 类型：字符串
- 要求：简单语义图标名，用于未来 marketplace 展示

### `color`
- 类型：字符串
- 要求：6 位十六进制色值，不带 `#`
- 约束：应与 SVG logo 主色一致

### `triggers`
- 类型：字符串数组
- 要求：写中文触发词，供 agent 路由使用

### `dependencies`
- 类型：对象
- 当前约定：无依赖时使用空对象 `{}`

### `auth`
- 类型：对象
- 常见字段：
  - `required`：是否必须配置凭证
  - `type`：当前常用 `api_key`
  - `keys`：环境变量声明数组

`keys` 中每一项格式：

```json
{"env": "WECHAT_MP_APP_ID", "url": "https://mp.weixin.qq.com", "optional": false}
```

### `install`
- 类型：对象
- 约定：至少提供 `user` 与 `project` 两类安装命令
- 当前 README 示例使用 `claude` 作为 agent 名键

### `commands`
- 类型：字符串数组
- 要求：写 marketplace 可直接执行的命令模板
- 约定：用户输入占位符统一为 `{input}`

### `links`
- 类型：对象
- 当前至少建议包含 `github`

## 3. 固定格式模板

新增 skill 时可以直接复制以下对象并替换字段：

```json
{
  "name": "your-skill-name",
  "version": "0.1.0",
  "description": "一句话说明用途。",
  "logo": "skill-logos/your-skill-name.svg",
  "icon": "tool",
  "color": "2E7CF6",
  "triggers": ["关键词1", "关键词2", "关键词3"],
  "dependencies": {},
  "auth": {
    "required": true,
    "type": "api_key",
    "keys": [
      {"env": "YOUR_SKILL_API_KEY", "url": "https://example.com", "optional": false}
    ]
  },
  "install": {
    "user": {"claude": "npx skills add <YOUR_ORG>/opc-skills-cn --skill your-skill-name -a claude"},
    "project": {"claude": "npx skills add <YOUR_ORG>/opc-skills-cn --skill your-skill-name"}
  },
  "commands": [
    "python3 scripts/main.py \"{input}\""
  ],
  "links": {
    "github": "https://github.com/<YOUR_ORG>/opc-skills-cn/tree/main/skills/your-skill-name"
  }
}
```

## 4. 以 cn-city-picker 为例

参考当前实现：`skills.json:15`

重点可以对照：

- `logo` 对应 `skill-logos/cn-city-picker.svg`
- `color` 为 `2E7CF6`
- `auth.required` 为 `false`
- `commands` 对应 `pick.py` / `profile.py` / `compare.py`

## 5. 提交前检查

修改 `skills.json` 后，至少执行：

```bash
python3 -c "import json; json.load(open('skills.json')); print('skills.json OK')"
python3 scripts/check_registry_consistency.py
```

若新增的是正式 skill，还应继续检查：

```bash
python3 scripts/validate_skill_md.py skills/<skill-name>/SKILL.md
python3 -m pylint skills/<skill-name>/scripts/*.py --disable=C0114,C0115,C0116
```
