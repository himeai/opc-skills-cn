# 跑道 6 个月 + 灵活就业社保 + 申领失业金（杭州 / 35 岁）

## 场景

之前做雇员 6 年缴过失业保险，后来开公司 2 年（个独）。今年决定彻底躺平，账上有 60000 元，月固定支出 8000 元（含房贷 4000 元）。

## Step 1：跑道体检

```bash
cd skills/opc-tangping

python3 scripts/runway.py "city=杭州|monthly_cost=8000|cash=60000|debt=0|has_house_loan=yes|was_employee=yes|prev_contribution_years=6"
```

输出（节选）：
- runway_months: 7.5 → 黄色警告（6-12 个月）
- threshold.advice: 建议立即开始零工 / 摆摊补贴
- unemployment_benefit:
  - eligible: true
  - estimated_monthly_cny_range: [1500, 2400]（杭州标准）
  - max_duration: 缴 5-10 年 → 最多 18 个月
- flexible_insurance:
  - pension_monthly_range_cny: [1300, 6500]（按缴费档次）
  - medical_monthly_range_cny: [350, 900]
  - registration_path: 持身份证 / 户口本 / 解除劳动关系证明 至社保经办处办理灵活就业身份切换
- credit_protection.must_do:
  - 房贷优先保障还款
  - 信用卡最低还款保住征信
  - 医保不要断缴 3 个月以上

## Step 2：6 个月行动清单

| 月 | 动作 |
|---|---|
| M1 | 申领失业金（户籍 / 居住地人社局）；办灵活就业身份；医保转灵活就业医保不断缴 |
| M1 | 砍订阅 / 健身 / 外食，月支出从 8000 → 5500 |
| M2-3 | 失业金 + 跑道月余约 1800 元，可用于一次性消化生活成本压力 |
| M3-6 | 持续观察心力恢复；不强迫自己「重新创业」；跑道可延长至 10 个月 |

## Step 3：可砍 / 必保支出

- **必保**：房贷、医保灵活就业、基础水电网、最低生活费
- **可砍**：奢侈品订阅、健身房、外食、非必要电子产品分期、车辆（如非通勤必需）

## 6 个月后

- 心力恢复，想重启 → 视情况看重新创业 / 找工作
- 跑外卖回血 → [opc-dagong](../../opc-dagong/SKILL.md)
- 低成本试错 → [opc-baitan](../../opc-baitan/SKILL.md)
- 想继续躺 → 没事，跑道还在，社保还在，征信还在

## 风险与免责

- 数据为公开政策口径，金额随社保基数 / 个人选择档次 / 城市动态变化
- 涉及房贷断供 / 信用卡逾期 / 司法纠纷的复杂场景，请咨询持牌财务规划师 / 律师
- 不推荐 P2P / 网贷 / 高利贷；不做「逃废债」/「征信修复」攻略
- 主基调：**躺得心安理得**，人生的容错率大得可怕
