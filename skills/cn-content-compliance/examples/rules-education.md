# 教培 + 抖音规则查看示例

输入：

```bash
python3 scripts/rules.py "education|douyin"
```

输出（节选）：

```json
{
  "industry": "education",
  "platform": "douyin",
  "category_count": 4,
  "categories": {
    "ad_law_extreme":    {"severity": "high",   "pattern_count": 51, "law_ref": "广告法第9条"},
    "ad_law_misleading": {"severity": "medium", "pattern_count": 19, "law_ref": "广告法第28条"},
    "education":         {"severity": "high",   "pattern_count": 16, "law_ref": "双减政策、广告法第24条"},
    "platform:douyin":   {"severity": "medium", "pattern_count": 12}
  }
}
```

## 用法

- 适合在做新行业/新平台前，先 dump 词表给法务/合规组人看
- `category_count = 4` 即"广告法极限词 + 广告法误导词 + 教培行业 + 抖音平台"四叠加
- 想新增词条直接编辑 `references/rules.json` 提 PR
