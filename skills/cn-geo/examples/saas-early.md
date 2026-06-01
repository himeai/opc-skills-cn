# 例：SaaS 早期上线，给 GEO 行动清单

## 输入
```bash
python3 scripts/audit.py "brand=ToFlow|category=saas_b2b|stage=early|website=toflow.example.com"
```

## 输出（节选）
```json
{
  "brand": "ToFlow",
  "category": "saas_b2b",
  "stage": "early",
  "dimensions": [
    {"name": "credible_source", "actions": [
      {"id": "media_pr", "label": "向 36 氪 / 创业邦 / 钛媒体投稿一次产品 / 融资 PR"},
      {"id": "zhihu_org", "label": "开通知乎机构号，每月至少 4 条优质内容"}
    ]},
    {"name": "structured_content", "actions": [
      {"id": "site_faq", "label": "官网建立 FAQ 页（至少 15 条 Q&A，每条短于 200 字）"}
    ]},
    {"name": "brand_qa", "actions": [
      {"id": "qa_skeleton", "label": "用 cn-geo qa.py 生成 20 条品牌问答素材"}
    ]}
  ],
  "top_3_next_actions": [
    {"dimension": "credible_source", "id": "media_pr", "priority": 1},
    {"dimension": "credible_source", "id": "zhihu_org", "priority": 1},
    {"dimension": "structured_content", "id": "site_faq", "priority": 1}
  ]
}
```

## 怎么用

1. 先把 `top_3_next_actions` 当本周 OKR
2. 跑 `qa.py` 生成 20 条品牌问答，按 publish_to 顺序铺
3. 跑 `matrix.py` 拿到主题矩阵，按主题排内容日历
4. 一个月后手动在豆包 / Kimi / 文心 / 元宝 / 秘塔搜一次品牌名，看 AI 怎么描述你
