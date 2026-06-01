# 剪映工程 JSON 骨架示例

输入：

```bash
python3 scripts/capcut.py "我用 ChatGPT 1 小时干完一周活|效率|职场新人"
```

输出结构（节选）：

```json
{
  "schema": "douyin-ops-capcut-skeleton-v1",
  "project": {
    "name": "我用 ChatGPT 1 小时干完一周活-效率",
    "duration": 60000,
    "fps": 30,
    "resolution": {"width": 1080, "height": 1920}
  },
  "tracks": [
    {"type": "video_placeholder", "items": [...]},
    {"type": "subtitle", "items": [...]}
  ]
}
```

## 注意

本 JSON **仅作骨架参考**，剪映 / CapCut 闭源格式可能版本变更：

- `video_placeholder` 是占位轨，需要在剪映里替换为真实素材
- 字幕轨可直接复制 `subtitle.items[].text` 到剪映"文本"功能
- 正式工程导出请以剪映客户端为准
