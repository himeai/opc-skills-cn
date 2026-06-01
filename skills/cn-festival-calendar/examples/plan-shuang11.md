# 例：双 11 多平台错峰排期

## 输入
```bash
python3 scripts/plan.py "shuang_shi_yi|cosmetics|all"
```

## 输出（节选）
```json
{
  "festival": "双 11",
  "festival_date": "2026-11-11",
  "days_to_go": 163,
  "tier": "S",
  "themes": ["全品类大促", "囤货", "比价"],
  "schedule": [
    {
      "platform": "xiaohongshu",
      "post_by": "2026-10-21",
      "lead_time_days": 21,
      "angles": ["全年最全攻略", "好物清单", "凑单笔记"],
      "best_post_types": ["图文笔记", "生活方式", "种草"]
    },
    {
      "platform": "bilibili",
      "post_by": "2026-11-01",
      "lead_time_days": 10,
      "angles": ["双 11 跨年盘点", "数码深评"]
    },
    {
      "platform": "douyin",
      "post_by": "2026-11-04",
      "lead_time_days": 7,
      "angles": ["双 11 直播", "限时秒杀", "比价"]
    },
    {
      "platform": "kuaishou",
      "post_by": "2026-11-06",
      "lead_time_days": 5,
      "angles": ["工厂直播", "老铁专属价"]
    },
    {
      "platform": "wechat_mp",
      "post_by": "2026-11-08",
      "lead_time_days": 3,
      "angles": ["双 11 长文指南", "理性消费"]
    }
  ],
  "earliest_action": "2026-10-21"
}
```

## 怎么用

- `earliest_action` 是整个项目的 deadline 起点：从这天开始排选题、约拍摄、写脚本
- 不同平台 lead time 不一样：小红书要提前 21 天种草、公众号长文 3 天就够
- 每平台 `angles` 不互相重复——同一品 5 个平台讲 5 个故事
- 配合 `cn-content-compliance` 检查每条文案，化妆品类高发"美白""祛斑"等极限词
