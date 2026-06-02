<div align="center">

# opc-skills-cn

[![CI](https://img.shields.io/badge/CI-passing-brightgreen)](./.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-25-2E7CF6)](./skills.json)
[![Star](https://img.shields.io/badge/Star-welcome-lightgrey)](https://github.com)

**面向中国市场的一人公司（OPC）AI Agent Skills 集合**

让一个人借助 AI，搞定运营一家中国公司所需的全部事情：内容、流量、私域、收款、开票、税务、备案、合规。

[快速开始](#快速开始) · [Skills 列表](#已收录-skills) · [贡献指南](#贡献新-skill) · [路线图快照](#路线图快照) · [Roadmap](./ROADMAP.md)

</div>

---

## 这是什么

`opc-skills-cn` 是 [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) 的中国生态对应物。原 repo 聚焦海外 indie hacker 工具链（Reddit / X / Product Hunt / Google SEO / Gemini），完全没有覆盖中国生态。本项目补齐这块空白：

- **流量端**：微信公众号、小红书、抖音/视频号、B 站、知乎、即刻
- **私域端**：企业微信 SCRM、视频号小店、微信小程序
- **收款端**：微信支付、支付宝、电子发票（诺诺 / 百望）
- **合规端**：个独/小规模税务申报、ICP/公安备案、PIPL 隐私政策
- **AI 搜索 GEO**：豆包、Kimi、元宝、夸克、百度智能答案

与原 repo **保持 100% 工程规范兼容**——同样的 `SKILL.md` frontmatter、同样的 `skills.json` 注册表、同样的 `npx skills add` 分发渠道，方便用户在两个 repo 之间无缝混用。

## 已收录 Skills

> 状态图例：✅ 已上线 · 🚧 开发中 · 📝 设计中 · ⏳ 待排期

<table>
  <thead>
    <tr><th>Logo</th><th>Skill</th><th>描述</th><th>状态</th></tr>
  </thead>
  <tbody>
    <tr><td colspan="4" align="center"><b>🏛️ 创业前置</b></td></tr>
    <tr>
      <td><img src="./skill-logos/cn-city-picker.svg" alt="cn-city-picker" width="24"></td>
      <td><code>cn-city-picker</code></td>
      <td><b>创业城市选择决策</b>：八维评分（税收/生活成本/气候/政策/产业/人才/基建/行政）从重点城市筛 Top 3-5，并给出落地 checklist</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/icp-domain-cn.svg" alt="icp-domain-cn" width="24"></td>
      <td><code>icp-domain-cn</code></td>
      <td><b>中国大陆上线前置流程</b>：给定主体 / 域名 / 服务器位置，判断 ICP 备案 + 公安备案 + 域名实名 + 行业前置许可需求，输出分步指引（本地规则）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>📣 流量内容</b></td></tr>
    <tr>
      <td><img src="./skill-logos/wechat-ops.svg" alt="wechat-ops" width="24"></td>
      <td><code>wechat-ops</code></td>
      <td>微信公众号 access_token 缓存、图文草稿、自定义菜单、客服文本回复（仅官方开放 API）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/xiaohongshu-ops.svg" alt="xiaohongshu-ops" width="24"></td>
      <td><code>xiaohongshu-ops</code></td>
      <td>小红书选题工厂、笔记结构化生成、关键词与 tag 推荐（本地种子库 + 规则模板）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/douyin-ops.svg" alt="douyin-ops" width="24"></td>
      <td><code>douyin-ops</code></td>
      <td>抖音/视频号 60 秒口播脚本、6 镜分镜表、剪映工程 JSON 骨架（本地模板 + 规则）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/kuaishou-ops.svg" alt="kuaishou-ops" width="24"></td>
      <td><code>kuaishou-ops</code></td>
      <td>快手老铁口播脚本、3 段式分镜、30 分钟直播带货话术（本地模板 + 规则）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/bilibili-ops.svg" alt="bilibili-ops" width="24"></td>
      <td><code>bilibili-ops</code></td>
      <td>B 站 12 分钟三段式长视频脚本、6 章节大纲与时间码、动态/专栏文案与 tag 推荐（本地模板 + 规则）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>🧭 内容支撑</b></td></tr>
    <tr>
      <td><img src="./skill-logos/cn-content-compliance.svg" alt="cn-content-compliance" width="24"></td>
      <td><code>cn-content-compliance</code></td>
      <td><b>中国内容合规自检</b>：广告法极限词 + 医疗/食品/化妆品/金融/教培行业红线 + 各平台禁用词，附改写建议（本地词库 + 规则）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/cn-festival-calendar.svg" alt="cn-festival-calendar" width="24"></td>
      <td><code>cn-festival-calendar</code></td>
      <td><b>节日内容决策引擎</b>：节日 / 节气 / 电商大促 / 监管敏感期 → 5 大平台错峰排期、内容角度、敏感期警告（本地数据）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/cn-geo.svg" alt="cn-geo" width="24"></td>
      <td><code>cn-geo</code></td>
      <td><b>中文 AI 搜索 GEO 优化</b>：给定品牌 / 品类 / 阶段，输出在豆包 / Kimi / 文心 / 元宝 / 秘塔等中文 AI 搜索里被引用的行动清单、品牌问答素材、内容覆盖矩阵（本地规则）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>💰 收款开票</b></td></tr>
    <tr>
      <td><img src="./skill-logos/wechatpay.svg" alt="wechatpay" width="24"></td>
      <td><code>wechatpay</code></td>
      <td><b>微信支付 V3 商户接入</b>：JSAPI / Native / H5 / APP 下单、查询、关单、退款、回调验签 + AES-GCM 解密、平台证书管理（仅商户官方 API V3）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/alipay.svg" alt="alipay" width="24"></td>
      <td><code>alipay</code></td>
      <td><b>支付宝 OpenAPI 商户接入</b>：当面付 / PC / WAP / APP 下单、查询、关单、退款、异步通知 RSA2 验签（stdlib + cryptography）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/cn-einvoice.svg" alt="cn-einvoice" width="24"></td>
      <td><code>cn-einvoice</code></td>
      <td><b>中国电子发票开具</b>：诺诺 / 百望双供应商，覆盖普票 / 专票开具、查询、红冲，可被 wechatpay / alipay 复用</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>📊 税务合规</b></td></tr>
    <tr>
      <td><img src="./skill-logos/cn-tax.svg" alt="cn-tax" width="24"></td>
      <td><code>cn-tax</code></td>
      <td><b>中国小微纳税人税务助手</b>：个体 / 个独 / 小规模 / 一般纳税人四种身份下的季度申报清单、税负近似测算、合规风险提醒（本地规则，不替代税务师）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>🤝 私域协作</b></td></tr>
    <tr>
      <td><img src="./skill-logos/wecom-crm.svg" alt="wecom-crm" width="24"></td>
      <td><code>wecom-crm</code></td>
      <td><b>企业微信客户运营</b>：客户联系、客户标签、客户群、欢迎语、合规群发、企业朋友圈，仅包装企业微信官方 OpenAPI（禁止批量加好友/群发骚扰）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>🧑‍💼 招聘内容</b></td></tr>
    <tr>
      <td><img src="./skill-logos/cn-recruit.svg" alt="cn-recruit" width="24"></td>
      <td><code>cn-recruit</code></td>
      <td><b>中国小公司招聘助手</b>：JD 生成、候选人筛选评分、结构化面试题库、招聘看板与 SLA 告警（本地规则推理，无外部 API）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/zhihu-ops.svg" alt="zhihu-ops" width="24"></td>
      <td><code>zhihu-ops</code></td>
      <td><b>知乎内容生产助手</b>：长回答结构化生成（科普/干货/经验/对比/反驳）、专栏长文骨架、问题选题工厂、领域 tag 推荐（本地规则，不爬抓不刷量）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>💸 融资资金</b></td></tr>
    <tr>
      <td><img src="./skill-logos/cn-angel.svg" alt="cn-angel" width="24"></td>
      <td><code>cn-angel</code></td>
      <td><b>中国天使轮融资助手</b>：BP 10 页骨架、4 法估值平均（Berkus / Scorecard / VC / 行业倍数）与稀释表、Term Sheet 12 条关键条款解读、投资人画像匹配、12 周融资时间表与 SLA 告警（本地规则，不替代律师 / FA / 投资顾问，不提供具体投资人联系方式）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>🎉 成功篇</b></td></tr>
    <tr>
      <td><img src="./skill-logos/opc-property.svg" alt="opc-property" width="24"></td>
      <td><code>opc-property</code></td>
      <td><b>一人公司置业助手</b>：1000 万起步的高净值置业决策——国内顶豪盘（汤臣一品 / 深圳湾一号 / 钓鱼台七号院 / 翠湖天地等 S/A/B 三级清单）、海外 10 大豪宅市场（纽约 / 伦敦 / 巴黎 / 悉尼 / 新加坡 / 迪拜 / 东京 / 洛杉矶 / 温哥华 / 葡萄牙）、5 年持有成本测算、跨境资金合规清单（本地规则，不构成投资 / 移民 / 税务建议）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/opc-travel.svg" alt="opc-travel" width="24"></td>
      <td><code>opc-travel</code></td>
      <td><b>一人公司环球旅行助手</b>：80+ 国 200+ 城市路线生成（按主题 / 时长 / 预算 / 出发月份）、4 档预算（穷游 / 舒适 / 商务 / 奢华）、中国普通护照签证矩阵 + 办理时间轴、月份反查目的地（含半球切换 + 节庆日历）、跨气候打包清单（本地规则，不推荐具体航司 / 酒店 / 旅行社，不爬抓任何机票数据）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/opc-experience.svg" alt="opc-experience" width="24"></td>
      <td><code>opc-experience</code></td>
      <td><b>一人公司高净值体验解锁助手</b>：8 大类 60+ 高净值体验（南极游艇 / KTM 摩托环球 / 米其林三星巡礼 / 马拉松六大满贯 / 私人飞行执照 / 去太空 / 顶豪拍场 / 七大洲最高峰）按预算 + 体能 + 年龄筛选；太空旅行专项（Virgin Galactic / Blue Origin / SpaceX × Axiom 等 3 档 6 家提供商）；6 类训练路径规划；支付 / 保险 / 医疗 / 法律红线（本地规则，不推荐具体俱乐部 / 教练 / 中介，不替代体育 / 航空 / 法律 / 保险专业人士）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>💔 失败篇</b></td></tr>
    <tr>
      <td><img src="./skill-logos/opc-shutdown.svg" alt="opc-shutdown" width="24"></td>
      <td><code>opc-shutdown</code></td>
      <td><b>一人公司体面注销助手</b>：4 类主体（个体 / 个独 / 一人有限 / 有限公司）注销路径，简易 vs 普通 vs 破产清算判定，详细步骤 + 典型周数 + 常见卡点 + 异常状态处理（本地规则，不替代律师 / 税务师）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/opc-dagong.svg" alt="opc-dagong" width="24"></td>
      <td><code>opc-dagong</code></td>
      <td><b>一人公司打工回血助手</b>：跑滴滴 / 送外卖 / 送快递 / 跑腿 / 众包；10 家主流零工平台按 5 维加权打分排序（earn 35% · barrier 20% · insurance 20% · vehicle_fit 15% · stability 10%），按城市 / 交通工具 / 五险需求筛选（本地规则，不爬抓任何招聘 / 平台数据，不教刷单 / 套保险）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/opc-baitan.svg" alt="opc-baitan" width="24"></td>
      <td><code>opc-baitan</code></td>
      <td><b>一人公司摆摊回血助手</b>：摆地摊 / 卖烤肠 / 夜市；10 城（上海 / 北京 / 广州 / 深圳 / 成都 / 杭州 / 重庆 / 武汉 / 西安 / 长沙）夜市政策 + 5 大品类（小吃热食 / 饮品冷食 / 文创手作 / 二手好物 / 轻服务）选品 + ROI 估算 + 设备清单 + 备案要求（本地规则，不教逃避城管 / 占用消防通道）</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><img src="./skill-logos/opc-tangping.svg" alt="opc-tangping" width="24"></td>
      <td><code>opc-tangping</code></td>
      <td><b>一人公司彻底躺平助手</b>：领低保 / 领失业金 / 灵活就业社保；个人现金流跑道 4 档红绿灯 + 失业金估算（10 城）+ 灵活就业养老 / 医疗社保金额 + 征信保护清单 + 必保 / 可砍支出（不推荐 P2P / 网贷 / 高利贷；不做「逃废债」/「征信修复」攻略）</td>
      <td>✅</td>
    </tr>
    <tr><td colspan="4" align="center"><b>⏳ 规划中</b></td></tr>
    <tr><td></td><td><code>cn-legal</code></td><td>个独章程、SaaS 服务协议、PIPL 隐私政策（法大大 / e 签宝）</td><td>⏳</td></tr>
    <tr><td></td><td><code>cn-cloud</code></td><td>阿里云 / 腾讯云 / 火山引擎：OSS、CDN、函数计算、解析</td><td>⏳</td></tr>
    <tr><td></td><td><code>cn-requesthunt</code></td><td>跨小红书 / 知乎 / 即刻 / V2EX / 脉脉的需求挖掘</td><td>⏳</td></tr>
  </tbody>
</table>

完整路线图见 [ROADMAP.md](./ROADMAP.md)。

## 快速开始

### 通过 Claude Code Plugin Marketplace
```bash
/plugin marketplace add <YOUR_ORG>/opc-skills-cn
/plugin install wechat-ops@opc-skills-cn
```

### 通过通用 CLI（支持 16+ AI 工具）
```bash
# 安装全部 skills
npx skills add <YOUR_ORG>/opc-skills-cn

# 只安装某一个
npx skills add <YOUR_ORG>/opc-skills-cn --skill wechat-ops

# 指定 AI 工具（claude / cursor / codex / droid / opencode / windsurf …）
npx skills add <YOUR_ORG>/opc-skills-cn -a claude
```

## 工程规范（与 opc-skills 完全对齐）

### 仓库结构
```
opc-skills-cn/
├── skills/                      # 所有 skill 源码，一个目录一个 skill
│   └── <skill-name>/
│       ├── SKILL.md             # 必需：YAML frontmatter + 文档
│       ├── scripts/             # 可选：Python 脚本（stdlib 优先）
│       │   ├── credential.py    # 约定：读取环境变量
│       │   └── *.py
│       ├── examples/            # 推荐：使用示例 *.md
│       └── references/          # 可选：API 文档 / schema
├── skill-logos/                 # 每个 skill 一个 *.svg（像素风）
├── template/SKILL.md            # 新 skill 起手模板
├── .claude-plugin/marketplace.json   # Claude Code 插件注册表
├── .factory/skills/add-new-skill/    # 新增 skill 的 checklist（作为一个 skill）
├── scripts/                     # 仓库级工具脚本
├── skills.json                  # 全局 skill 注册表（单一信息源）
├── CHANGELOG.md
├── LICENSE                      # Apache-2.0
└── README.md
```

### SKILL.md frontmatter（只有两个必需字段）
```yaml
---
name: wechat-mp
description: 微信公众号自动排版、图文生成、定时发布、菜单/客服消息管理。
             Use when 用户提到公众号、推文、图文消息、菜单配置、客服回复、定时群发。
---
```

> ⚠️ 不要在 frontmatter 里写 version / license / tags / requires / env。
> 这些字段统一在根目录 `skills.json` 中声明。

### SKILL.md 正文章节（建议顺序）
```
# <Skill 中文名>
## Prerequisites          ← 环境变量、账号要求
## Quick Start            ← 30 秒最小可运行示例
## Usage Examples         ← 3-5 个真实场景
## Commands               ← 所有可调用脚本
## Scripts                ← 每个脚本的输入/输出契约
## API Info               ← Base URL / Rate Limits / Auth / Docs
## Troubleshooting
## References
## Notes
```

### 运行时与依赖
- **语言**：Python 3.10+，shebang 用 `#!/usr/bin/env python3`
- **依赖**：**优先只用 stdlib**（`urllib.request`、`json`、`argparse`、`os`、`re`、`base64`、`time`）。需要第三方包必须在该 skill 的 SKILL.md `## Prerequisites` 章节显式声明 `pip install xxx`，不写 `requirements.txt`。
- **调用约定**：从 skill 根目录调用，`python3 scripts/<name>.py "{input}"`
- **跨脚本导入**：平铺，无 package：`from credential import get_xxx`
- **凭证**：每个 skill 必须有 `scripts/credential.py`，统一从环境变量读取，**严禁硬编码**

```python
# scripts/credential.py 模板
import os

def get_wechat_mp_credentials() -> dict:
    return {
        "app_id":     os.environ.get("WECHAT_MP_APP_ID"),
        "app_secret": os.environ.get("WECHAT_MP_APP_SECRET"),
    }
```

### skills.json 注册项 schema
```json
{
  "name": "wechat-mp",
  "version": "0.1.0",
  "description": "微信公众号自动排版、图文生成、定时发布。",
  "logo": "https://raw.githubusercontent.com/<YOUR_ORG>/opc-skills-cn/main/skill-logos/wechat-mp.svg",
  "icon": "wechat",
  "color": "07C160",
  "triggers": ["公众号", "推文", "图文消息", "菜单", "客服回复", "群发"],
  "dependencies": {},
  "auth": {
    "required": true,
    "type": "api_key",
    "keys": [
      { "env": "WECHAT_MP_APP_ID",     "url": "https://mp.weixin.qq.com", "optional": false },
      { "env": "WECHAT_MP_APP_SECRET", "url": "https://mp.weixin.qq.com", "optional": false }
    ]
  },
  "install": {
    "user":    { "claude": "npx skills add <YOUR_ORG>/opc-skills-cn --skill wechat-mp -a claude" },
    "project": { "claude": "npx skills add <YOUR_ORG>/opc-skills-cn --skill wechat-mp" }
  },
  "commands": ["python3 scripts/publish.py \"{input}\""],
  "links": { "github": "https://github.com/<YOUR_ORG>/opc-skills-cn/tree/main/skills/wechat-mp" }
}
```

字段解释、固定格式模板与提交前检查见 [`docs/skills-json-schema.md`](./docs/skills-json-schema.md)。

## 贡献新 Skill

> 完整 checklist 见 `.factory/skills/add-new-skill/SKILL.md`（这本身也是一个 skill）。

### 快速贡献

- 第一次参与：先看 [5 分钟快速开始](./docs/quickstart.md)
- 需要长版开发说明：看 [Skill 开发手册](./docs/skill-authoring.md)
- 需要确认中国合规边界：看 [合规说明](./docs/compliance.md)
- 想直接拿到新增 skill 的执行清单：优先查看 [`.factory/skills/add-new-skill/SKILL.md`](./.factory/skills/add-new-skill/SKILL.md)
- 想核对注册表字段：看 [`skills.json` 字段说明](./docs/skills-json-schema.md)

如果你是在和 agent 协作，推荐先把下面这句话直接发给它：

```text
请先使用 .factory/skills/add-new-skill/SKILL.md 中的 checklist，再开始新增 <skill-name>
```

1. 从 `develop` 分支切出 `feature/skill/<skill-name>`（kebab-case）
2. 复制 `template/SKILL.md` 到 `skills/<skill-name>/SKILL.md`，按规范填写 frontmatter
3. 在 `scripts/` 下实现脚本（stdlib 优先，凭证走 `credential.py`）
4. 在 `skill-logos/` 添加 `<skill-name>.svg`（24x24 像素风，主色取自 `skills.json` 的 `color`）
5. 在 `skills.json` 追加注册项
6. 在 `.claude-plugin/marketplace.json` 追加插件项
7. 在 `README.md` 的 Skills 表格新增一行
8. 在 `CHANGELOG.md` 增加条目
9. 校验：
   ```bash
   python3 -c "import json; json.load(open('skills.json')); print('skills.json valid')"
   python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('marketplace.json valid')"
   python3 -m pylint skills/<skill-name>/scripts/*.py
   ```
10. 提交 PR 到 `develop`，CI 通过后合入

### Skill 设计原则（强约束）
- **单一职责**：一个 skill 只解决一类问题；跨域能力拆成多个 skill
- **零云依赖**：除目标平台 API 外，不引入额外 SaaS
- **优雅降级**：未配置凭证时应给出清晰错误，而不是 crash
- **中文优先**：所有 description / examples / 错误信息默认中文；可附英文
- **合规第一**：涉及爬虫、私信群发、批量加好友的能力一律拒绝实现；只做平台**官方/开放 API** 包装
- **不存储用户数据**：所有数据流过 skill 即焚，不落盘到 skill 目录外

## Roadmap

见 [ROADMAP.md](./ROADMAP.md)。

## 路线图快照

- 当前已实现（按主题）：
  - **创业前置**：[`cn-city-picker`](./skills/cn-city-picker/SKILL.md)、[`icp-domain-cn`](./skills/icp-domain-cn/SKILL.md)
  - **流量内容**：[`wechat-ops`](./skills/wechat-ops/SKILL.md)、[`xiaohongshu-ops`](./skills/xiaohongshu-ops/SKILL.md)、[`douyin-ops`](./skills/douyin-ops/SKILL.md)、[`kuaishou-ops`](./skills/kuaishou-ops/SKILL.md)、[`bilibili-ops`](./skills/bilibili-ops/SKILL.md)
  - **内容支撑**：[`cn-content-compliance`](./skills/cn-content-compliance/SKILL.md)、[`cn-festival-calendar`](./skills/cn-festival-calendar/SKILL.md)、[`cn-geo`](./skills/cn-geo/SKILL.md)
  - **收款开票**：[`wechatpay`](./skills/wechatpay/SKILL.md)、[`alipay`](./skills/alipay/SKILL.md)、[`cn-einvoice`](./skills/cn-einvoice/SKILL.md)
  - **税务合规**：[`cn-tax`](./skills/cn-tax/SKILL.md)
  - **私域协作**：[`wecom-crm`](./skills/wecom-crm/SKILL.md)
  - **招聘内容**：[`cn-recruit`](./skills/cn-recruit/SKILL.md)、[`zhihu-ops`](./skills/zhihu-ops/SKILL.md)
  - **融资资金**：[`cn-angel`](./skills/cn-angel/SKILL.md)
  - **失败篇**：[`opc-shutdown`](./skills/opc-shutdown/SKILL.md)、[`opc-dagong`](./skills/opc-dagong/SKILL.md)、[`opc-baitan`](./skills/opc-baitan/SKILL.md)、[`opc-tangping`](./skills/opc-tangping/SKILL.md)
- 下一批优先：`cn-legal`、`cn-cloud`、`cn-requesthunt`
- 详细分期与风险评估：见 [ROADMAP.md](./ROADMAP.md)

| 阶段 | 时间 | 目标 |
|---|---|---|
| **P0** | M1–M2 | `cn-city-picker`（前置决策） · `wechat-mp` · `xiaohongshu-ops` · `douyin-ops` · `kuaishou-ops` · `bilibili-ops` · `cn-geo` |
| **P1** | M3–M4 | `wechatpay` · `alipay` · `cn-einvoice` · `cn-tax` · `icp-domain-cn` |
| **P2** | M5–M6 | `wecom-crm` · `cn-recruit` · `zhihu-ops` · `cn-legal` |
| **P3** | M7+   | `cn-cloud` · `cn-requesthunt` · 出海回流 skill |

## 许可

Apache License 2.0 — 见 [LICENSE](./LICENSE)。

## 致谢

工程规范借鉴自 [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills)，特此致谢。
