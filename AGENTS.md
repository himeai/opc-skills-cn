# AGENTS.md — opc-skills-cn 开发者代理总指南

> 这个文件是给 **coding agent**（Claude Code / Cursor / Codex / Droid 等）读的。
> 用户在本仓库里让你"新增一个 skill" / "实现某个 skill"时，**先完整读这份文件**，再开始动手。

---

## 0. 仓库使命

为中国一人公司（OPC）用户提供可装入任何 AI agent 的、覆盖**内容/流量/私域/收款/合规/协作**全链路的 Skills。规范完全对齐上游 [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills)，让两个 repo 的 skill 可以并存安装。

## 1. 接到新增 skill 任务时的标准流程

```
1) 读 README.md「工程规范」章节
2) 读本文件第 2-4 节（命名 / 结构 / 凭证 / 合规红线）
3) 复制 template/SKILL.md → skills/<skill-name>/SKILL.md
4) 实现 scripts/credential.py（必须）+ 业务脚本
5) 添加 skill-logos/<skill-name>.svg
6) 追加 skills.json + .claude-plugin/marketplace.json + README 表格行 + CHANGELOG 条目
7) 运行第 6 节的本地校验命令
8) 自检第 7 节的提交清单
9) 提 PR 到 develop 分支
```

**关键原则**：每一步都要落到文件改动，不要"假装完成"。所有 9 步缺一不可。

## 2. 命名与目录

### 仓库命名
本仓库名 `opc-skills-cn`（国别后缀，对标上游 opc-skills）。**禁止**把 `-cn` 后缀传染到单个 skill 名。

### Skill 命名规约（四档，选其一，禁止混用）
| 场景 | 命名风格 | 例子 |
|---|---|---|
| 中国平台专属能力 | 平台名直接做前缀 | `wechat-mp` / `xiaohongshu-ops` / `douyin-ops` / `bilibili-zhihu` / `wecom-crm` |
| 中国通用/跨平台能力 | `cn-` 语义前缀 | `cn-city-picker` / `cn-tax` / `cn-geo` / `cn-recruit` / `cn-legal` |
| OPC 生命周期专属能力 | `opc-` 语义前缀 | `opc-plan-b`（创业失败下车回血） |
| 海外/全球通用 | 无前缀 | `feishu-ops`（飞书海外即 Lark） / `stripe-paddle` |

判定规则：
1. **能用一个明确的中文平台名命名？** → 用平台前缀（`wechat-*` / `xiaohongshu-*` / `douyin-*` …）
2. **是"中国特色"但不绑定单一平台？** → 用 `cn-` 前缀
3. **绑定一人公司生命周期场景（下车 / 重启 / 复盘等），不强中国特色？** → 用 `opc-` 前缀
4. **海外也能用、产品方也面向海外？** → 不加任何前缀

### 通用约束
- Skill 名一律 **kebab-case**，长度 ≤ 24 字符，全小写
- 一个 skill = `skills/<name>/` 一个目录，禁止跨目录共享代码
- 目录里允许的子目录只有：`scripts/`、`examples/`、`references/`。其它一律不要
- 禁止以 `-skill` / `-skills` 结尾命名单个 skill（那是仓库级后缀）

## 3. SKILL.md 硬约束

frontmatter **只有两个字段**，多写会破坏 marketplace 解析：
```yaml
---
name: <kebab-case，和目录名完全一致>
description: <一句话讲清楚做什么 + 「Use when ...」触发词>
---
```

description 必须包含中文触发关键词的自然语言列举（例："Use when 用户提到公众号、推文、图文消息"）——这是 agent 路由该 skill 的唯一线索。

正文章节顺序见 README，**最少必须有** `## Prerequisites` `## Quick Start` `## Commands`。

## 4. 凭证与合规（红线）

### 凭证规则
- **每个 skill 必须有 `scripts/credential.py`**，统一从 `os.environ` 读取
- 环境变量命名：`<SKILL_NAME_UPPER>_<FIELD>`，例：`WECHAT_MP_APP_ID`
- 在 SKILL.md `## Prerequisites` 用 `export XXX=...` 形式列出所有变量
- **严禁** 把 token / app_secret 写进任何 .py / .md / .json
- **严禁** 提交 `.env` / `.env.local`（已在 .gitignore）

### 合规红线（违反 = PR 直接关闭）
- 拒绝实现：**爬虫绕过登录、批量加好友、私信群发、刷量、虚假评论、协议逆向**
- 只包装**平台官方/开放 API**（微信开放平台、抖音开放平台、小红书蒲公英、企微 API、飞书 OpenAPI 等）
- 涉及个人数据的 skill 必须在 SKILL.md 顶部声明 PIPL 合规边界
- 涉及收款/开票/税务的 skill 必须在 README 顶部加风险提示

## 5. 实现规范

### 语言与依赖
- Python 3.10+，shebang `#!/usr/bin/env python3`
- **优先只用 stdlib**：`urllib.request` / `json` / `argparse` / `os` / `re` / `base64` / `time` / `hashlib` / `hmac`
- 必须引入第三方库时：
  - 在 SKILL.md `## Prerequisites` 写 `pip install <pkg>`（不要 requirements.txt）
  - 在脚本顶部 try/except 给出友好提示

### 脚本契约
- 入口脚本接收 **单个字符串参数**（marketplace 注入 `{input}`）
- 输出：stdout 打印结构化结果（JSON 优先），stderr 打印日志
- 退出码：0 成功，非 0 失败
- 平铺导入，无 package：`from credential import get_xxx`
- 工作目录 = skill 根目录（不是 scripts/）

### 错误处理
- 凭证缺失 → 友好提示如何配置，退出码 2
- API 限流 → 自动指数退避，最多重试 3 次
- 网络失败 → 给出原始错误 + 重试建议

## 6. 本地校验（提交前必跑）

```bash
# JSON 合法性
python3 -c "import json; json.load(open('skills.json')); print('skills.json OK')"
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('marketplace OK')"

# 注册一致性：skill 目录 ↔ skills.json ↔ marketplace.json 三方对齐
python3 scripts/check_registry_consistency.py

# Lint（仅你新增/修改的 skill）
python3 -m pylint skills/<skill-name>/scripts/*.py

# Skill frontmatter 校验
python3 scripts/validate_skill_md.py skills/<skill-name>/SKILL.md
```

`scripts/check_registry_consistency.py` 与 `scripts/validate_skill_md.py` 是仓库级工具脚本，如果不存在，**第一步先创建它们**（这是合理的基础设施工作）。

## 7. 提交清单（PR 描述模板自动生成）

- [ ] `skills/<name>/SKILL.md` 存在且 frontmatter 合规
- [ ] `skills/<name>/scripts/credential.py` 存在
- [ ] 至少 1 个业务脚本，且 `python3 scripts/xxx.py --help` 可运行
- [ ] `skill-logos/<name>.svg` 存在（24x24 像素风）
- [ ] `skills.json` 已追加条目，`color` 与 logo 主色一致
- [ ] `.claude-plugin/marketplace.json` 已追加条目
- [ ] `README.md` Skills 表格已更新（含 logo / 状态）
- [ ] `CHANGELOG.md` 已追加 `### Added` 条目
- [ ] 至少 1 个 `examples/*.md`
- [ ] 凭证全部走环境变量，无硬编码
- [ ] 不包含爬虫 / 群发 / 协议逆向逻辑
- [ ] 第 6 节所有校验命令通过

## 8. 你（agent）的自我约束

- **不要**问用户"我应该用什么语言" — 答案永远是 Python 3
- **不要**问"要不要加 requirements.txt" — 答案永远是不加
- **不要**自作主张引入 Node.js / TypeScript（仓库不接受）
- **不要**用 emoji 装饰 SKILL.md（影响 marketplace 渲染）
- **不要**在 SKILL.md frontmatter 加 README 没列的字段
- **可以**主动创建缺失的基础设施脚本（如 `scripts/check_registry_consistency.py`）
- **可以**在评论里指出原 opc-skills 规范的不合理之处，但不要单方面改

## 9. 速查表

| 我要... | 看哪里 |
|---|---|
| 新增 skill 的完整步骤 | 本文件第 1 节 + README「贡献新 Skill」 |
| SKILL.md 怎么写 | `template/SKILL.md` |
| 凭证 / credential.py 怎么写 | 本文件第 4 节 |
| 注册到哪几个地方 | 本文件第 7 节 |
| 合规边界 | 本文件第 4 节红线 |
| 当前 skill 路线图 | `ROADMAP.md` |
| 各 skill 的设计文档 | `skills/<name>/SKILL.md` + `references/` |
