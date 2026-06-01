# 章节大纲示例

输入：

```bash
python3 scripts/chapters.py "Mac mini M4 一年使用复盘|测评|程序员"
```

输出（节选）：

```json
{
  "topic": "Mac mini M4 一年使用复盘",
  "duration_min": 12,
  "chapter_count": 6,
  "chapters": [
    {"index": 1, "start_sec": 0,   "start_tc": "00:00", "title": "开场",                "duration_sec": 120},
    {"index": 2, "start_sec": 120, "start_tc": "02:00", "title": "测评维度与评分规则",  "duration_sec": 120},
    {"index": 3, "start_sec": 240, "start_tc": "04:00", "title": "外观与基础参数",      "duration_sec": 120},
    {"index": 4, "start_sec": 360, "start_tc": "06:00", "title": "性能/体验实测",       "duration_sec": 120},
    {"index": 5, "start_sec": 480, "start_tc": "08:00", "title": "总分与购买建议",      "duration_sec": 120},
    {"index": 6, "start_sec": 600, "start_tc": "10:00", "title": "总结与三连",          "duration_sec": 120}
  ]
}
```

## 使用建议

- 把 chapters 数组直接复制到稿件后台的"分 P 与时间章节"区域
- 时间码格式 `MM:SS` 与必剪、剪映的章节点格式一致
- 默认 6 章 = 1 开场 + 4 主章节 + 1 总结，需要调整章数请改 `references/chapter_meta.json`
