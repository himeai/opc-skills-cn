# 化妆品笔记自检示例

输入：

```bash
python3 scripts/check.py "敏感肌亲测：这款国家级精华，30 天根治痘印，全网最低价 100% 有效|cosmetics|xiaohongshu"
```

输出（节选）：

```json
{
  "summary": {"total_hits": 6, "highest_severity": "high"},
  "hits": [
    {"phrase": "国家级",   "category": "ad_law_extreme",  "severity": "high", "law_ref": "广告法第9条"},
    {"phrase": "全网最低", "category": "ad_law_extreme",  "severity": "high", "law_ref": "广告法第9条"},
    {"phrase": "100%",     "category": "ad_law_extreme",  "severity": "high", "law_ref": "广告法第9条"},
    {"phrase": "根治",     "category": "ad_law_medical",  "severity": "high", "law_ref": "广告法第16-17条"}
  ]
}
```

## 处理建议

- 这类高危词在小红书 + 化妆品双重红线里几乎必定限流
- 用 `rewrite.py` 拿到改写建议后，再让真人审一遍
- 化妆品功效宣称需要在国家药监局备案才能用，未备案禁用 "美白/祛斑/防脱"
