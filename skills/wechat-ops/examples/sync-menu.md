# 示例：覆盖式同步自定义菜单

## 步骤

1. 编辑 `references/menu.example.json`（或自己拷一份），结构：
```json
{
  "button": [
    {"type": "view", "name": "最新文章", "url": "https://example.com/latest"},
    {
      "name": "联系我们",
      "sub_button": [
        {"type": "view", "name": "加微信", "url": "https://example.com/wechat"},
        {"type": "click", "name": "在线咨询", "key": "ASK_NOW"}
      ]
    },
    {"type": "view", "name": "关于", "url": "https://example.com/about"}
  ]
}
```

2. 同步：
```bash
python3 scripts/menu.py ./references/menu.example.json
```

3. 输出：
```json
{"status":"ok","buttons":3}
```

> 该脚本会先 `menu/delete` 再 `menu/create`，因此每次同步都是覆盖式更新。
