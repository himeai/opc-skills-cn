# 直播带货 30 分钟话术示例

输入：

```bash
python3 scripts/live.py "9.9 元应季水果|生鲜|宝妈"
```

输出（节选）：

```json
{
  "duration_min": 30,
  "phases": [
    {"id": "warmup",  "label": "暖场", "minutes": 3, "lines": ["..."]},
    {"id": "intro",   "label": "讲解", "minutes": 6, "lines": ["..."]},
    {"id": "pain",    "label": "痛点", "minutes": 5, "lines": ["..."]},
    {"id": "benefit", "label": "福利", "minutes": 5, "lines": ["..."]},
    {"id": "urgency", "label": "逼单", "minutes": 6, "lines": ["..."]},
    {"id": "closing", "label": "收尾", "minutes": 5, "lines": ["..."]}
  ],
  "compliance_reminders": [
    "禁用『最』『第一』『国家级』『绝对』等绝对化用语",
    "化妆品/保健品/医疗器械严禁宣称疗效",
    "价格/赠品承诺必须真实可兑现"
  ]
}
```

## 注意

- 本输出**不含**夸大/绝对化用语，但主播自己临场发挥时仍需自查广告法合规
- 库存/赠品/售后承诺必须可兑现，否则触发平台违规与消费者权益问题
- 化妆品/保健品/医疗器械直播请额外查阅相关行业规则
