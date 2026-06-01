# 同城 6 镜分镜表示例

输入：

```bash
python3 scripts/storyboard.py "本地 9.9 早餐铺测评|同城|本地老铁"
```

输出（节选）：

```json
{
  "duration_sec": 60,
  "shot_count": 6,
  "subtitle_color": "#FFFFFF",
  "subtitle_bg": "#CC0000",
  "bgm_keyword": "city-walk",
  "shots": [
    {"index": 1, "duration": 10, "visual": "门店外景 / 招牌特写"},
    {"index": 2, "duration": 10, "visual": "店内走动 / 第一视角"},
    {"index": 3, "duration": 10, "visual": "试吃试用 / 反应镜头"},
    {"index": 4, "duration": 10, "visual": "价格标签 / 特写"},
    {"index": 5, "duration": 10, "visual": "总结字卡 / 推荐榜"},
    {"index": 6, "duration": 10, "visual": "门店地址字卡 / CTA"}
  ]
}
```

## 用法

把 `shots` 表打印出来直接交给摄影师；同城本地视频以"真实门店镜头 + 反应特写"为主，避免摆拍痕迹。
