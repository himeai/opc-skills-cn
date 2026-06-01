---
name: icp-domain-cn
description: 在中国大陆上线网站 / 小程序 / H5 前的域名 + ICP 备案 + 公安备案 + 行业前置许可清单生成器：给定主体类型 / 域名 / 服务器位置 / 行业，输出本次必须办什么、不必办什么、踩过最多的坑。本地规则推理，不爬抓不调外部 API。Use when 用户提到 ICP 备案、公安备案、网站备案、域名备案、上线流程、域名注册、服务器选型、个人备案、企业备案、备案号、beian、视听许可证、ICP 经营许可证、网络文化经营许可证、域名实名。
---

# 中国大陆上线前置流程清单（icp-domain-cn）

> 一个 OPC 创始人想上线一个网站 / 小程序 / H5，最容易踩坑的不是写代码，而是：域名要不要实名、服务器选境内还是香港、ICP 备案怎么走、要不要做公安备案、做电商 / 视频 / 教培是不是还要前置许可。本 skill 把"备案 + 域名 + 服务器选择 + 行业资质"沉淀成本地决策引擎，输入主体 + 业务类型 → 输出本次需要办的清单。

## 风险提示

- 本 skill **仅作流程参考**，不替代律师 / 备案专员 / 通信管理局意见
- 备案规则按**省份**与**主体类型**差异显著；最终以各地通信管理局与云厂商备案系统为准
- 不替你提交备案：所有上传材料、人脸核验、负责人短信确认必须本人完成
- 不规避备案：本 skill 拒绝输出"如何不备案上线"的方案

## Prerequisites

### 环境变量
本 skill **不需要任何凭证**，全部本地规则推理。

### 依赖
仅 stdlib。

## Quick Start

```bash
# 1. 个人 + .com + 阿里云境内 服务器：是否需要 ICP / 公安备案
python3 scripts/check.py "subject=individual|domain=example.com|hosting=cn_mainland"

# 2. 拿到 ICP 备案分步指引
python3 scripts/steps.py "filing=icp"

# 3. 一个做"在线视频教育"的公司，需要哪些前置许可证
python3 scripts/qualifications.py "industry=education,live_audio_video"
```

## Usage Examples

### 场景 1：个人博客准备上线
```bash
python3 scripts/check.py "subject=individual|domain=myblog.cn|hosting=cn_mainland"
```
输出：必须 ICP + 必须公安备案 + .cn 域名实名 + 个人备案不能做电商。

### 场景 2：想上线快但不接受境内备案的 SaaS
```bash
python3 scripts/check.py "subject=company|domain=mysaas.com|hosting=overseas"
```
输出：免备案 + 但用了国内 CDN 仍需备案 + 推荐方案。

### 场景 3：公安备案具体怎么做
```bash
python3 scripts/steps.py "filing=psb"
```
输出 4 步分步指引 + 平台链接 + 关键陷阱。

### 场景 4：教培 / 视频 / 游戏行业资质自查
```bash
python3 scripts/qualifications.py "industry=education,publication"
```
输出每个行业需要的许可证清单。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/check.py "subject=X\|domain=X\|hosting=X"` | 综合判断本次上线要办什么 | k=v | JSON |
| `python3 scripts/steps.py "filing=icp\|psb"` | 分步流程 | k=v | JSON |
| `python3 scripts/qualifications.py "industry=id1,id2"` | 行业前置许可清单 | k=v | JSON |

`subject`：`individual` / `individual_business` / `company`
`hosting`：`cn_mainland` / `hk_macao` / `overseas`
`industry`（多选逗号分隔）：`ecommerce` / `live_audio_video` / `news` / `publication` / `medical` / `education` / `finance` / `game`

## Scripts

### `scripts/credential.py`
本 skill 无凭证需求，仅占位。

### `scripts/check.py`
- **职责**：综合主体类型 / 域名后缀 / 服务器位置，判断 ICP / 公安备案是否必需，给出推荐方案
- **输入**：`subject=...|domain=...|hosting=...`
- **输出**：`{decisions: {icp_required, psb_required, real_name_required}, advice: [...], common_rejections: [...]}`

### `scripts/steps.py`
- **职责**：返回指定备案类型的分步操作指引
- **输入**：`filing=icp|psb`
- **输出**：`{filing, steps: [{id, label, items}]}`

### `scripts/qualifications.py`
- **职责**：返回多个行业的前置许可清单
- **输入**：`industry=id1,id2,...`
- **输出**：`{industries: [{id, label, requirements: [...]}]}`

## 数据架构

```
references/
└── rules.json   # 主体类型 / 域名后缀 / 服务器选择 / 备案步骤 / 行业资质 / 常见拒绝原因
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **更新频率**：建议每年 PR 复核（备案规则会跟随《网络安全法》《数据安全法》《电信条例》修订）

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `unknown subject / hosting` | 输入不在词典 | 见 Commands 部分支持的取值 |
| 输出与某省实际要求不一致 | 规则按通用口径，省份差异未建模 | 以所在省通信管理局公告为准 |
| 上线急 → 选海外服务器 | 想跳过备案 | 国内访问体验差且如要用国内 CDN 仍需备案；权衡后再决定 |

## References

- 工信部 ICP 备案系统：https://beian.miit.gov.cn/
- 全国互联网安全管理服务平台：https://beian.mps.gov.cn/
- 主流云厂商备案入口：阿里云 / 腾讯云 / 华为云 / 火山引擎备案系统
- 协同 skill：与本 skill 互补的有 `cn-tax`（税务）、`wechatpay` / `alipay`（收款）、`cn-content-compliance`（上线后内容合规）

## Notes

- 本 skill **不爬抓任何政府 / 厂商系统**，无外部 API 调用
- **不替代律师 / 备案专员**：复杂主体（外资 / VIE / 多主体）请咨询专业服务
