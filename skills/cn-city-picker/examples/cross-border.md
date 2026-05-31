# 跨境电商独立站选址

## 输入

跨境电商独立站，月预算 1.5 万，已婚无娃，怕冷不爱辣，户籍山东，倾向南方非一线。

## 命令

```bash
python3 scripts/pick.py "跨境电商独立站，月预算 1.5 万，已婚无娃，怕冷不爱辣，户籍山东，倾向南方非一线"
```

## 输出截断

```json
{
  "status": "ok",
  "parsed_preferences": {
    "budget_cny": 15000,
    "industries": ["跨境电商"],
    "prefer_south": true,
    "fear_cold": true,
    "avoid_spicy": true,
    "prefer_non_tier1": true,
    "hukou_province": "山东"
  },
  "top_recommendations": [
    {"city": "厦门", "score": 90.2},
    {"city": "杭州", "score": 89.7},
    {"city": "宁波", "score": 88.9}
  ]
}
```

## 解读

这类用户需要同时满足跨境电商产业、南方气候、非一线成本和不辣饮食。厦门、杭州、宁波通常会优先进入候选；惠州也会作为靠近深圳且成本更低的扩展选项进入比较池。
