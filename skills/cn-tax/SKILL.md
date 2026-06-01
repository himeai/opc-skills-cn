---
name: cn-tax
description: 中国个体工商户 / 小规模 / 个独 / 公司制纳税人的季度申报清单、税负近似测算、合规风险提醒。本地规则推理，不替代税务师，不自动提交申报。Use when 用户提到报税、纳税申报、季度申报、年度汇算、增值税、企业所得税、个人经营所得、附加税、税负测算、小规模、一般纳税人、个体工商户、个人独资、税务合规、零申报、风控、虚开发票、电子税务局。
---

# 中国小微纳税人税务助手（cn-tax）

> 一个跑 OPC 的人最怕的不是赚不到钱，是收完款不知道该交多少税、什么时候交、怎么交。本 skill 把"个体 / 个独 / 小规模 / 一般纳税人"四种身份下的常见税种（增值税、附加税、企业所得税、个人经营所得）整理成本地决策引擎，输入一组数字 → 输出近似税负 + 申报清单 + 合规风险提醒。**绝不替代税务师**，所有计算结果必须以电子税务局申报系统为准。

## 风险提示

- 本 skill **仅供内部预估与流程参考**，不出具任何税务意见
- 税收政策按地区、行业、年份频繁变化，本规则库基于 2026 年通用口径
- **绝不自动提交申报**：凡涉及电子税务局、个税 App 的操作，由用户人工完成
- 真实复杂业务（跨境、股权激励、研发加计、关联交易）请咨询税务师
- 政策延续条款（如小规模 1% / 小型微利 5%）请以财政部/税务总局最新通知为准

## Prerequisites

### 环境变量
本 skill **不需要任何凭证**，全部本地规则推理。

### 依赖
仅 stdlib。

## Quick Start

```bash
# 1. 季度税负预估：小规模公司，一季度收款 28 万
python3 scripts/estimate.py "entity=small_scale_company|period=quarter|revenue=280000|cost=120000"

# 2. 看本季度该报哪些表、要准备什么资料
python3 scripts/checklist.py "entity=small_scale_company|period=quarter"

# 3. 检查一组业务行为有没有踩税务红线
python3 scripts/risk.py "scenario=personal_to_business,long_zero_filing"
```

## Usage Examples

### 场景 1：个体工商户季度自查
```bash
python3 scripts/estimate.py "entity=individual_business|period=quarter|revenue=180000|cost=70000"
```
输出：增值税（季度 30 万内免征）+ 附加税 + 经营所得近似税负。

### 场景 2：小型微利企业年度估税
```bash
python3 scripts/estimate.py "entity=small_scale_company|period=year|revenue=1800000|cost=1100000|headcount=4"
```
输出：判断是否符合小型微利、企业所得税近似（实际税负 5%）。

### 场景 3：临近申报截止日的清单
```bash
python3 scripts/checklist.py "entity=individual_business|period=quarter"
```
输出：季度申报清单 + 申报日历（次月 / 次季 15 日）。

### 场景 4：风险自检
```bash
python3 scripts/risk.py "scenario=invoice_split,personal_to_business"
```
输出：每条风险的等级 + 描述 + 整改建议。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/estimate.py "entity=X\|period=X\|revenue=X\|cost=X[\|headcount=X]"` | 税负近似测算 | k=v | JSON |
| `python3 scripts/checklist.py "entity=X\|period=X"` | 申报清单 + 日历 | k=v | JSON |
| `python3 scripts/risk.py "scenario=id1,id2,..."` | 风险自检 | k=v（逗号分隔风险 id） | JSON |

`entity`：`individual_business` / `small_scale_company` / `general_taxpayer_company` / `sole_proprietor`
`period`：`quarter` / `year`

## Scripts

### `scripts/credential.py`
本 skill 无凭证需求，仅占位以保持目录结构一致。

### `scripts/estimate.py`
- **职责**：根据身份 / 期间 / 收入 / 成本，输出增值税 + 附加税 + 所得税的近似税负
- **输入**：`entity=...|period=...|revenue=...|cost=...|[headcount=...]`
- **输出**：`{entity, period, taxes: [{name, base, rate, amount, note}], total_tax, effective_rate, cautions: [...]}`

### `scripts/checklist.py`
- **职责**：返回该身份下该期间应完成的申报清单
- **输入**：`entity=...|period=...`
- **输出**：`{entity, period, filings: [...], deadline_hints: [...]}`

### `scripts/risk.py`
- **职责**：列出指定风险点的等级与说明，或返回全部风险
- **输入**：`scenario=id1,id2`（可选，缺省返回全部）
- **输出**：`{risks: [{id, level, rule}]}`

## 数据架构

```
references/
├── rules.json         # 税种规则（增值税征收率 / 附加税 / 企税 / 个体经营所得累进）
├── checklists.json    # 申报清单与申报日历
└── risk_alerts.json   # 常见税务风险点
```

## API Info

- **本地推理**：随 skill 一同分发，无外部 API
- **数据版本**：见各 JSON 顶部 `version` 字段
- **更新频率**：每年初（财税新政发布后）必须 PR 更新规则

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `unknown entity` | entity 不在词典 | 见 `references/rules.json` 的 `entities` 字段 |
| 计算结果与电子税务局不一致 | 本 skill 未建模进项 / 加计 / 研发 / 减免备案 | 以电子税务局为准；本 skill 仅作毛估 |
| 政策已变 | 规则文件版本旧 | 更新 `references/rules.json` 的对应字段 |

## References

- 国家税务总局：https://www.chinatax.gov.cn/
- 电子税务局：https://etax.chinatax.gov.cn/
- 财政部 / 税务总局公告：通过官方渠道订阅
- 协同 skill：`wechatpay` / `alipay` 提供收款流水，`cn-einvoice` 提供开票数据，是 `cn-tax` 的上游

## Notes

- 本 skill **不爬抓税务局**，无任何外部 API 调用
- **不替代税务师 / 会计师**：复杂业务请咨询专业人士
- 对应的合规边界：本 skill 不会建议任何"如何避税"的违规手段
