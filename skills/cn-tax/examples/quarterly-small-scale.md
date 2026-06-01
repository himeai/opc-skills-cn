# 例：小规模公司一季度估税

## 输入

```bash
python3 scripts/estimate.py "entity=small_scale_company|period=quarter|revenue=280000|cost=120000"
```

## 输出（节选）

```json
{
  "entity": "small_scale_company",
  "entity_label": "小规模纳税人（公司制）",
  "period": "quarter",
  "revenue": 280000.0,
  "cost": 120000.0,
  "profit": 160000.0,
  "taxes": [
    {"name": "vat", "label": "增值税（小规模）",
     "base": 280000.0, "rate": 0.0, "amount": 0.0,
     "note": "销售额 280000.00 ≤ 免征额度 300000，假设全部为普票..."},
    {"name": "additional_tax", "label": "附加税费（城建 7% + 教育费 3% + 地方 2%）",
     "base": 0.0, "rate": 0.12, "amount": 0.0,
     "note": "假设市区税率 7%；县/镇为 5%，其它 1%。小规模 / 小微减半计征"},
    {"name": "corporate_income", "label": "企业所得税（小型微利综合 5%）",
     "base": 160000.0, "rate": 0.05, "amount": 8000.0,
     "note": "小型微利企业 2027 年底前减按 25% 计入应纳税所得额，按 20% 税率，综合实际税负 5%"}
  ],
  "total_tax": 8000.0,
  "effective_rate": 0.0286,
  "cautions": [
    "结果为本地近似计算，实际以电子税务局申报系统为准",
    "未建模：进项发票 / 研发加计 / 残保金 / 印花税 / 房产税等"
  ]
}
```

## 怎么用

1. 跑 `estimate.py` 拿到本季度近似税负 → 现金流预留
2. 跑 `checklist.py` 拿到申报清单 → 按清单准备资料
3. 真实申报：登录电子税务局，**人工**完成
4. 复杂业务（跨境 / 股权 / 研发加计）请咨询税务师，不要照搬本 skill 输出
