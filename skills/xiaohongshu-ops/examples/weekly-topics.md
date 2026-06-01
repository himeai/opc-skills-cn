# 示例：一周选题表

## 输入

行业：母婴；受众：0-1 岁新手妈妈；细分：辅食工具

```bash
python3 scripts/topic.py "母婴|0-1 岁新手妈妈|辅食工具"
```

## 输出（节选）

```json
{
  "topics": [
    {"title": "0-1 岁新手妈妈总在 辅食工具难选 上踩坑？", "angle": "痛点直击", "hook_type": "pain_point"},
    {"title": "5 款 辅食工具，我用半年挑出这 3 支", "angle": "横向对比", "hook_type": "compare"},
    {"title": "100 元搞定 辅食工具难选，比 进口品牌 还省", "angle": "平价解决", "hook_type": "cheap_solve"}
  ]
}
```

## 用法

将 10 个选题导入到 Notion / 飞书多维表格，按周排发布节奏即可。
