# opc-travel：30 岁卖了公司，gap year 来一次真环球

> 这是一个完整的从「想环球」到「拎包出发」的 5 步示例。
> 用户：32 岁，刚把一家做了 4 年的 SaaS 卖给一家上市公司，扣完税到手 1800w，想拿出 100w 走半年环球。

## 第 1 步：路线生成（180 天，6 大洲）

```bash
python3 scripts/route.py "themes=自然,极地,海岛,城市,文化|days=180|start_month=10|tier=business|continents=亚洲,欧洲,北美,南美,非洲,大洋洲,极地"
```

输出（节选）：

```json
{
  "tier": "商务",
  "tier_remark": "绝大部分体验顶配 + 商务舱，30 天约 30-50w / 人",
  "total_days": 180,
  "used_days": 175,
  "stops_count": 16,
  "by_continent": {
    "亚洲": ["京都", "巴厘岛", "马尔代夫", "尼泊尔加德满都 / EBC"],
    "欧洲": ["巴黎", "罗马", "威尼斯", "瑞士因特拉肯 / 少女峰"],
    "北美": ["纽约", "黄石公园", "夏威夷"],
    "南美": ["巴塔哥尼亚", "马丘比丘 / 库斯科"],
    "非洲": ["肯尼亚 / 坦桑尼亚迁徙", "开普敦"],
    "大洋洲": ["新西兰皇后镇"],
    "极地": ["南极半岛"]
  },
  "budget_breakdown_cny": {
    "lodging_food_local": 540000,
    "intl_flight": 35000,
    "insurance": 4800,
    "visa_estimate": 8000,
    "contingency_15pct": 86250
  },
  "total_cny": 674050
}
```

> 67w，落在预算 100w 内，留 33w 当缓冲 / 升级 / 应急。

## 第 2 步：节奏调整 —— 10 月出发对不对

```bash
python3 scripts/season.py "month=10|themes=红叶,文化,城市"
```

输出：京都红叶前段 / 纽约秋叶 / 卡帕多奇亚热气球 / 雅典 / 马德里全部命中。10 月出发是对的。

继续：

```bash
python3 scripts/season.py "month=2|themes=极地,海岛"
```

> 2 月正好是南极末季 + 巴塔哥尼亚 + 新西兰盛夏，刚好可以从北半球冬天逃到南半球夏天。

## 第 3 步：签证集中办（路线敲定后立刻办）

```bash
python3 scripts/visa.py "countries=日本,法国,意大利,瑞士,美国,墨西哥,秘鲁,智利,阿根廷,肯尼亚,坦桑尼亚,南非,新西兰|order=date"
```

输出：

- 美国 30 天 leadtime → 出发前 37 天动手
- 申根（任一国可代办）15 天 → 出发前 22 天
- 新西兰 / 阿根廷 / 肯尼亚 / 坦桑 / 南非 电子签 / 落地签 → 出发前 1 周
- 日本 5 天 → 出发前 12 天
- 总签证费估算约 **6500-7500 元**

> 工具会按 leadtime 倒排出时间轴，避免临行前手忙脚乱。

## 第 4 步：南极那段单独算钱（升级到 luxury）

```bash
python3 scripts/budget.py "cities=南极半岛|days=14|tier=luxury"
```

输出：14 天约 **150w 量级**（含国际机票 + 邮轮 + 保险 + 应急）。

> 想环游一辈子 1 次的事，单独升档不亏。

## 第 5 步：分段打包

冬装段（瑞士 + 南极 + 巴塔哥尼亚）：

```bash
python3 scripts/pack.py "climates=alpine,polar|themes=ski|days=45"
```

夏装段（马代 + 巴厘 + 大堡礁）：

```bash
python3 scripts/pack.py "climates=tropical|themes=diving|days=20"
```

萨法里段（肯尼亚 / 坦桑）：

```bash
python3 scripts/pack.py "climates=temperate_summer|themes=safari|days=10"
```

> 输出每段的基础包 + 气候模块 + 主题模块 + TSA 红线。中途回家一次或在中转地寄存 / 邮寄是常见做法。

## 复盘

5 步走完，原来需要找 3 家旅行社、咨询 5 个朋友、自己刷 30 个攻略、纠结一个月的事情，半小时搞定一个清单。

边界提醒：

- 工具不替代签证中心 / 律师 / 银行私行；不推荐具体航司酒店；不爬抓任何数据
- 境外消费请走合规外汇渠道（年度 5 万美元购汇 + 境外信用卡刷卡），任何「换汇 / 蚂蚁搬家 / 地下钱庄」都是违法的
- 申根 90 / 180 规则在长期环游必须算清；停超会被拉黑名单
- 数据是静态参考，最终以中国领事服务网 + 目的国使馆官网为准
