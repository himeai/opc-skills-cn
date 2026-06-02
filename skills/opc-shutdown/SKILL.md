---
name: opc-shutdown
description: 一人公司「失败篇·公司体面注销」副驾驶（本地规则版）：4 类主体（个体 / 个独 / 一人有限 / 有限公司）注销路径，简易 vs 普通 vs 破产清算的判定，详细步骤 + 典型周数 + 常见卡点 + 异常状态处理。Use when 用户提到注销、关公司、关门、停业、个体注销、个独注销、一人有限注销、简易注销、普通注销、破产清算、解散、吊销、清算、税务注销、工商注销。
---

# 一人公司体面注销副驾驶（opc-shutdown）

> 失败篇第一步：体面下车。
>
> 公司没了不丢人，关不干净才丢人。这个 skill 把 4 类主体（个体 / 个独 / 一人有限 / 有限公司）的注销路径——简易 vs 普通 vs 破产清算——按你的实际情况（有员工没员工 / 有债务没债务 / 是否进了异常名录）拍下推荐路径，列出每步要跑的窗口与典型周数，以及最容易卡壳的几个坑。

> 本 skill 不替代律师 / 税务师；不教「逃废债」/「失联跑路」；不爬抓任何工商 / 税务窗口数据。所有数据为本地静态规则，最终以当地工商 / 税务窗口为准。

## Prerequisites

### 账号要求
无外部账号；本地规则推理。

### 环境变量
无。

### 系统依赖
仅 Python 3.10+ 标准库。

## Quick Start

```bash
cd skills/opc-shutdown

# 个独刚关门，无员工无债务，想知道简易注销怎么走
python3 scripts/shutdown.py "entity=个独|location=杭州|has_employees=no|has_debt=no|has_abnormal=no"

# 一人有限，有员工有未结贷款，问普通注销路径
python3 scripts/shutdown.py "entity=一人有限|location=深圳|has_employees=yes|has_debt=yes|has_abnormal=no"

# 已被列入经营异常名录，先解除异常再注销
python3 scripts/shutdown.py "entity=个体|location=北京|has_employees=no|has_debt=no|has_abnormal=yes"
```

## Usage Examples

### 1. 个独干净退出（最常见）
```bash
python3 scripts/shutdown.py "entity=个独|location=杭州|has_employees=no|has_debt=no|has_abnormal=no"
```
输出：简易注销路径 + 5 步清单 + 典型 2-3 周完成 + 园区核定征收常见卡点。

### 2. 一人有限带员工带债务
```bash
python3 scripts/shutdown.py "entity=一人有限|location=上海|has_employees=yes|has_debt=yes|has_abnormal=no"
```
输出：必须走普通注销 / 清算路径 + 必须先结清工资与社保 + 必须先处理债务 + 典型 2-4 个月。

### 3. 进了异常名录
```bash
python3 scripts/shutdown.py "entity=个体|location=广州|has_abnormal=yes"
```
输出：先解除异常状态（公示信息补报 / 罚款补缴）才能注销，附常见解除路径。

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/shutdown.py "<input>"` | 主体注销路径与详细步骤 | `entity=<个体/个独/一人有限/有限公司>\|location=...\|has_employees=...\|has_debt=...\|has_abnormal=...` | JSON |

## Scripts

### `scripts/shutdown.py`
- **职责**：根据主体类型 + 是否有员工 / 债务 / 异常状态，返回简易 / 普通 / 破产清算路径与详细步骤
- **输入**：`entity` / `location` / `has_employees` / `has_debt` / `has_abnormal`
- **输出**：JSON `{entity, recommended_path, all_paths, simple_eligible, steps, typical_weeks, common_blockers, extra_warnings}`

### `scripts/credential.py`
本 skill 不需要任何凭证。

## API Info

无外部 API。所有数据来自本地 JSON：
- `references/entity_shutdown.json` — 4 类主体注销流程 + 触发简易→普通切换的条件 + 常见卡点

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `error: bad field 'xxx'` | 未用 `key=value` 格式 | 用 `\|` 分隔多个字段，每个字段 `key=value` |
| 主体类型未匹配 | 用了非「个体/个独/一人有限/有限公司」之外的字 | 模糊匹配兜底为「个人独资企业」，建议显式写明 |
| `simple_eligible` 始终为 false | 任一 `has_employees` / `has_debt` / `has_abnormal` 为 yes | 简易注销互斥这三项，先解决再来 |

## References

- 国家市场监督管理总局《市场主体登记管理条例》
- 国家税务总局公告 2018 年第 149 号《关于深化「放管服」改革更大力度推进优化税务注销办理程序》
- 各地市场监督管理局公开公告

## Notes

- 本 skill **完全本地推理，不调用任何外部 API、不爬抓任何窗口数据**
- 数据来自公开政策口径，最新流程请以当地工商 / 税务窗口为准
- 涉及破产清算 / 司法纠纷 / 跨境股东的复杂场景，请聘请律师
- 已知限制：未覆盖港澳台地区主体；未覆盖外资主体注销
- See also（注销之后下一步）：[opc-dagong](../opc-dagong/SKILL.md)（先打工补现金流）、[opc-baitan](../opc-baitan/SKILL.md)（轻成本摆摊）、[opc-tangping](../opc-tangping/SKILL.md)（彻底躺平：失业金 / 灵活就业社保 / 跑道体检）
