# 个独 14 天简易注销路径（杭州）

## 场景

一个 SaaS 独立开发者，2 年前在杭州未来科技城注册了「XX 软件工作室」（个人独资企业），核定征收。今年决定关停，没员工没债务也没进异常名录。

## 步骤

```bash
cd skills/opc-shutdown

python3 scripts/shutdown.py "entity=个独|location=杭州|has_employees=no|has_debt=no|has_abnormal=no"
```

## 输出（节选）

- recommended_path: 简易注销
- typical_weeks: 2-3
- steps:
  1. 登录国家企业信用信息公示系统提交简易注销公告（公示 20 天）
  2. 同步前往税务窗口办理税务注销（清税证明）
  3. 公示期满后，到工商窗口领《注销通知书》
  4. 注销对公账户、销毁公章 / 财务章 / 法人章
  5. 注销园区注册地址托管协议
- common_blockers:
  - 园区核定征收尾期未结清
  - 对公账户里还有余额未划走
  - 增值税普通发票未缴销

## 14 天时间线

| Day | 动作 |
|---|---|
| Day 1 | 公示系统提交简易注销公告 |
| Day 1-2 | 税务窗口办理清税；带上税控盘 / 普票 / 营业执照 |
| Day 3-4 | 银行办对公销户（划走余额） |
| Day 5-21 | 等公示 20 天 |
| Day 22 | 工商窗口领注销通知书 + 销毁三章 |

## 失败篇下一步

注销完成后，你有 3 条岔路：

- 继续打工补现金流 → [opc-dagong](../../opc-dagong/SKILL.md)
- 低成本试错摆摊 → [opc-baitan](../../opc-baitan/SKILL.md)
- 彻底躺平算跑道 → [opc-tangping](../../opc-tangping/SKILL.md)

## 免责

本 example 不构成法律 / 税务建议；具体流程以当地工商 / 税务窗口为准。复杂案例（有员工 / 有债务 / 异常名录）建议聘请律师或注销代办。
