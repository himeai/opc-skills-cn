# BOOTSTRAP.md — 给 Coding Agent 的启动指令

> **用法**：在 Claude Code / Cursor / Codex 等任意 coding agent 中，把本文件第二部分（### START PROMPT 之后的全部内容）作为 system / first message 粘贴进去即可。Agent 会自动按顺序完成 Phase 0 → Phase 1 → Phase 2。
>
> 你提供：本文件 + README.md + AGENTS.md + template/SKILL.md + skills/cn-city-picker/SKILL.md
> Agent 输出：一个可直接 `git init && git push` 的完整 opc-skills-cn 仓库骨架，以及第一个可运行的 skill（`cn-city-picker`）。

---

## 一、人类操作步骤（你做的事）

```
1. 新建一个本地空目录                   →  mkdir opc-skills-cn && cd opc-skills-cn
2. 把下面 4 个文件放进去                →  README.md / AGENTS.md / template/SKILL.md
                                            skills/cn-city-picker/SKILL.md
3. 启动 coding agent，复制 START PROMPT  →  agent 开始执行
4. 验收 Phase 0 产出，再放行 Phase 1     →  逐阶段把关
5. git init + 推送到 GitHub             →  收工
```

---

## 二、START PROMPT

### START PROMPT

你现在是 `opc-skills-cn` 项目的初始化 coding agent。本仓库定位、规范、命名规则已经在 `README.md` 和 `AGENTS.md` 中明确说明。请你严格按以下三个 Phase 顺序执行，每个 Phase 完成后**停下来**等我确认，再进入下一个 Phase。

#### 全局约束（任何 Phase 都不许违反）
1. 严格遵循 `AGENTS.md` 第 1-8 节所有规则
2. 严格遵循 `AGENTS.md` 第 2 节的三档命名规约
3. Python 3 + stdlib 优先，禁止引入 Node.js / TypeScript
4. 禁止硬编码任何 token / API key
5. 禁止实现爬虫、群发、协议逆向类逻辑
6. 每完成一个文件就提交一个 commit，commit message 用中文 + 约定式提交格式（`feat:` / `chore:` / `docs:`）

---

#### Phase 0：仓库基础设施（预计 30 分钟）

**目标**：搭出一个能跑 CI、能被 `npx skills add` 安装、能通过校验脚本的空骨架。

按顺序产出以下文件：

1. **`LICENSE`** — Apache License 2.0 标准文本，Copyright 占位写 `Copyright 2026 opc-skills-cn contributors`
2. **`.gitignore`** — Python + Node + macOS + IDE 标准忽略 + 额外加 `.env` / `.env.local` / `references/policy_cache/`
3. **`.gitattributes`** — `* text=auto eol=lf`
4. **`CHANGELOG.md`** — Keep-a-Changelog 格式，初始版本 `## [0.0.1] - 2026-05-31`，Added 一条 "项目初始化"
5. **`ROADMAP.md`** — 把 README 路线图表格扩展成详细版，每个 skill 列：目标用户、核心场景、依赖的外部 API、预计工期（人日）、风险点
6. **`skills.json`** — 空注册表，schema 头部加注释说明字段含义，初始 `skills: []`
7. **`.claude-plugin/marketplace.json`** — Claude Code 插件 marketplace 空骨架，参照上游 opc-skills 的 schema
8. **`scripts/validate_skill_md.py`** — 校验单个 SKILL.md 的 frontmatter 是否只含 name + description，文件名作为参数传入
9. **`scripts/check_registry_consistency.py`** — 校验 `skills/` 目录、`skills.json`、`.claude-plugin/marketplace.json` 三方 skill 列表完全一致
10. **`scripts/new_skill.py`** — 半自动脚手架：输入 skill 名，自动从 `template/SKILL.md` 复制并初始化目录结构 + 占位 `credential.py`
11. **`.github/workflows/ci.yml`** — GitHub Actions：在 push / PR 时跑 pylint + 上述两个校验脚本
12. **`.github/ISSUE_TEMPLATE/`** — bug_report.md + feature_request.md + new_skill_proposal.md（中文模板）
13. **`.github/PULL_REQUEST_TEMPLATE.md`** — 提交清单照搬 `AGENTS.md` 第 7 节
14. **`CODE_OF_CONDUCT.md`** — Contributor Covenant 2.1 中文版
15. **`SECURITY.md`** — 漏洞报告流程，邮箱占位 `security@<待填>`

**Phase 0 验收**：
```bash
python3 scripts/validate_skill_md.py template/SKILL.md
python3 scripts/check_registry_consistency.py
python3 -c "import json; json.load(open('skills.json')); json.load(open('.claude-plugin/marketplace.json'))"
```
三个命令全部退出码 0，Phase 0 通过。**输出一份 Phase 0 完成报告（文件树 + 校验结果），停下来等我说"继续"。**

---

#### Phase 1：cn-city-picker MVP（预计 1-2 天）

**目标**：把 `skills/cn-city-picker/SKILL.md` 里设计的 skill 落地成可运行 MVP。

按顺序产出：

1. **`skills/cn-city-picker/scripts/credential.py`** — 按 `AGENTS.md` 第 4 节模板
2. **`skills/cn-city-picker/references/cities.json`** — 种子数据，**先收录 20 个核心城市**（北上广深 + 杭州、苏州、成都、重庆、武汉、长沙、西安、南京、厦门、佛山、宁波、青岛、合肥、郑州、无锡、东莞），每城填充 `AGENTS.md` 引用的 schema 全部字段。**数据可基于公开常识填充合理范围**，并在每条记录加 `"data_source_note"` 字段标注"种子数据，待人工核校"
3. **`skills/cn-city-picker/references/industry_city_matrix.json`** — 20 个 OPC 行业 × 20 城市的 0-100 契合度矩阵
4. **`skills/cn-city-picker/references/sources.md`** — 数据来源清单（政府站、统计年鉴、行业报告）
5. **`skills/cn-city-picker/scripts/pick.py`** — 主入口，按 SKILL.md 设计的"偏好解析规则"实现：
   - 解析自然语言偏好 → 提取约束（预算/气候/医疗/行业/户籍/城市等级偏好）
   - 应用过滤规则
   - 按八维加权 + 行业矩阵加权打分
   - 输出 Top 3-5 JSON
6. **`skills/cn-city-picker/scripts/profile.py`** — 单城市档案查询
7. **`skills/cn-city-picker/scripts/compare.py`** — 多城市对比，输出 Markdown 表 + 雷达图原始数据
8. **`skills/cn-city-picker/scripts/refresh_policy.py`** — 占位实现：标注 TODO，先返回"功能待接入"，确保 import 不报错
9. **`skills/cn-city-picker/examples/`** — 至少 3 个 `*.md`，每个走完一个完整使用场景（输入 → 命令 → 输出截断 → 解读）
10. **`skill-logos/cn-city-picker.svg`** — 24x24 像素风，主色取 `#2E7CF6`（地图蓝），元素含中国地图轮廓 + 选中标记
11. **同步更新**：
    - `skills.json` 追加 `cn-city-picker` 注册项
    - `.claude-plugin/marketplace.json` 追加插件项
    - `README.md` Skills 表格把状态从 📝 改为 ✅
    - `CHANGELOG.md` 追加 `### Added: cn-city-picker v0.1.0`

**Phase 1 验收**：
```bash
python3 scripts/validate_skill_md.py skills/cn-city-picker/SKILL.md
python3 scripts/check_registry_consistency.py
python3 -m pylint skills/cn-city-picker/scripts/*.py --disable=C0114,C0115,C0116
cd skills/cn-city-picker
python3 scripts/pick.py "跨境电商独立站，月预算 1.5 万，已婚无娃，怕冷不爱辣，户籍山东，倾向南方非一线"
python3 scripts/profile.py 厦门
python3 scripts/compare.py 厦门 杭州 成都
```
全部成功，**输出 Phase 1 完成报告 + 三条命令的真实输出截图（文本）**，停下来等我说"继续"。

---

#### Phase 2：贡献者文档与新 skill 引导（预计 30 分钟）

**目标**：让后续 contributor（人或 agent）能"一键"开发新 skill。

按顺序产出：

1. **`.factory/AGENTS.md`** — 把根目录 `AGENTS.md` 软链/复制到此（对齐上游约定）
2. **`.factory/skills/add-new-skill/SKILL.md`** — 把"新增 skill 流程"本身做成一个 skill（这是上游 opc-skills 的精妙设计），调用时返回完整 checklist
3. **`docs/quickstart.md`** — 5 分钟新手教程：从安装到第一次调用
4. **`docs/skill-authoring.md`** — 长版 skill 开发手册（AGENTS.md 是给 agent 的简版，这份是给人看的扩展版）
5. **`docs/compliance.md`** — 中国合规边界详解（PIPL / 数据出境 / 平台协议）
6. **`README.md` 增补**：
   - 顶部加 badge 区（CI / License / Skills 数量 / Star）
   - 增加"快速贡献"小节，链到 docs/skill-authoring.md
   - 增加"路线图"快照链接

**Phase 2 验收**：
- 整个仓库可被 `npx skills add <YOUR_ORG>/opc-skills-cn --skill cn-city-picker` 模拟安装命令成功（先在本地用 file:// 测试）
- 所有 markdown 链接 `markdown-link-check` 通过
- `git log --oneline` 显示清晰的提交序列

**输出最终交付报告**：文件树 + skills 数 + 测试结果 + 下一步建议。

---

#### 你（agent）的注意事项
- **遇到歧义先停下来问**，不要自作主张扩大范围
- **每个 Phase 之间必须等我说"继续"**，不要连贯执行
- 校验命令失败时,**先分析错误**,不要盲目重试
- 任何"种子数据"必须显式标注 `data_source_note`,不要伪造来源链接
- 提交信息全中文,符合约定式提交格式
- 不要在本仓库里生成任何 emoji 装饰文字

### END PROMPT
