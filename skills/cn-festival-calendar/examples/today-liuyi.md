# 例：每日选题决策（六一儿童节当天）

## 输入
```bash
python3 scripts/today.py "2026-06-01|general|xiaohongshu,douyin,wechat_mp"
```

## 输出（节选）
```json
{
  "date": "2026-06-01",
  "festivals": [
    {"name": "六一儿童节", "tier": "A", "themes": ["亲子穿搭", "玩具", "童年回忆杀"]},
    {"name": "618 年中大促（预热期）", "tier": "A"},
    {"name": "京东 618 / 抖音 618", "tier": "S"}
  ],
  "content_opportunities": [
    {
      "festival": "六一儿童节", "platform": "xiaohongshu",
      "angles": ["攻略", "穿搭", "送礼"],
      "post_by": "2026-05-11",
      "best_windows": [{"start": "07:00", "end": "09:00"}]
    },
    {
      "festival": "六一儿童节", "platform": "douyin",
      "angles": ["短视频", "直播", "话题挑战"],
      "post_by": "2026-05-25"
    }
  ],
  "blackout_alerts": [],
  "upcoming_14d": [
    {"name": "芒种", "date": "2026-06-06", "in_days": 5},
    {"name": "夏至", "date": "2026-06-21", "in_days": 20}
  ]
}
```

## 怎么用

1. 早会先跑一次，确认今天有几条赛道可吃
2. `post_by` 已经过去 → 当天发应景内容；没过去 → 下次该提前到这一天发
3. `upcoming_14d` 用来做下周内容排期
4. 结合 `cn-content-compliance` check 一遍最终文案
