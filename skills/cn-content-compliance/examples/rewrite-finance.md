# 金融号合规改写示例

输入：

```bash
python3 scripts/rewrite.py "我们家产品保本，100% 稳赚不赔，年化 15%|finance|wechat_mp"
```

输出（节选）：

```json
{
  "original": "我们家产品保本，100% 稳赚不赔，年化 15%",
  "rewritten": "我们家产品历史表现稳定（不构成投资建议），高比例 ...",
  "changes": [
    {"from": "保本",   "to": "历史表现稳定（不构成投资建议）", "category": "finance"},
    {"from": "100%",   "to": "高比例",                          "category": "ad_law_extreme"},
    {"from": "稳赚",   "to": "存在收益可能（不构成投资建议）", "category": "ad_law_misleading"},
    {"from": "稳赚不赔", "to": null, "note": "未提供改写建议，建议人工删除或重写"}
  ]
}
```

## 处理建议

- 金融营销宣传管理办法对"保本/稳赚"几乎是零容忍，强烈建议删除
- 自动改写仅供参考，最终文案务必由合规/法务审核
- 公众号金融类账号还需要持牌资质，未持牌不要做投资建议
