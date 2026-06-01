# 例：两会期间金融号写稿前避雷

## 输入
```bash
python3 scripts/blackout.py "2026-03-08|finance"
```

## 输出
```json
{
  "date": "2026-03-08",
  "industry": "finance",
  "alerts": [
    {
      "id": "lianghui",
      "name": "全国两会期间",
      "level": "high",
      "industries": ["finance", "medical", "education", "general"],
      "blackout_topics": ["政策解读", "金融预测", "医疗效果对比", "教培营销", "境外政经议题"],
      "safe_alternatives": ["产品使用教程", "用户故事", "幕后日常", "知识科普"],
      "law_ref": "《互联网信息服务管理办法》+ 平台两会期间运营公告"
    },
    {
      "id": "jinrong_changtai",
      "name": "金融行业宣传常态收紧",
      "level": "medium",
      "blackout_topics": ["保本", "稳赚", "收益承诺", "无风险", "比较其他平台"],
      "safe_alternatives": ["理财知识科普", "风险测评", "资产配置思路"]
    }
  ],
  "safe": false,
  "highest_level": "high"
}
```

## 怎么用

- `safe: false` + `highest_level: high` → 当天直接停发金融政策解读类内容
- 改用 `safe_alternatives` 里的角度（产品教程、用户故事），保持账号活跃但避开雷区
- 用 `law_ref` 给老板/法务解释为什么要停发
- 同时把 `blackout_topics` 喂给 `cn-content-compliance` 做发布前最后一次自检
