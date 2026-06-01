# 6 镜分镜表示例

输入：

```bash
python3 scripts/storyboard.py "我用 ChatGPT 1 小时干完一周活|效率|职场新人"
```

输出（节选）：

```json
{
  "duration_sec": 60,
  "shot_count": 6,
  "subtitle_color": "#FFE600",
  "subtitle_bg": "#1A1A1A",
  "bgm_keyword": "uplifting-electronic",
  "shots": [
    {"index": 1, "duration": 10, "voiceover": "...", "visual": "正脸口播 / 桌面后景"},
    {"index": 2, "duration": 10, "voiceover": "...", "visual": "屏幕录制 / 操作 demo"},
    {"index": 3, "duration": 10, "voiceover": "...", "visual": "时间对比图 / before-after"},
    {"index": 4, "duration": 10, "voiceover": "...", "visual": "工具截图 / 高亮按钮"},
    {"index": 5, "duration": 10, "voiceover": "...", "visual": "总结字卡 / 三步骤"},
    {"index": 6, "duration": 10, "voiceover": "...", "visual": "字卡 + CTA / 评论区扣 1"}
  ]
}
```

## 用法

把 `shots` 表打印出来，交给摄影师 / 自己拍摄。每镜对应：

- voiceover：录音稿
- visual：画面提示
- subtitle：字幕（默认与 voiceover 一致，可手动收紧）
