# opc-experience：从「卖了公司」到「去太空」的 5 年路径

> 用户：33 岁，刚把 SaaS 卖给上市公司，到手 5000w，想用 5 年时间解锁人生体验清单。

## 第 1 步：我能做什么 —— 主清单筛选

```bash
python3 scripts/unlock.py "budget_cny=5000w|fitness=4|categories=极地探险,极速极限,飞行航天,顶级美食,体育成就,登山远征,私享包场,文化收藏|age=33|max_lead_months=60"
```

输出：30+ 项可立即启动的体验，按预算 + lead 排序。立刻可做的有：

- 跳伞五大圣地（半年内）
- F1 单座赛车 / Paddock Club（半年）
- KTM 摩托环球（18 个月）
- PPL 私人飞行执照（1 年）
- 米其林三星巡礼 21 餐（9 个月）
- 北极破冰船（1 年）
- 南极包船游艇（1.5 年）
- 温网中央球场会员席（1 年）

中长线的有：

- 马拉松六大满贯（5 年）
- 七大洲最高峰（5-7 年）
- 私人飞机会籍（NetJets / 君联，6 个月起，1500w+）
- 亚轨道太空（Virgin Galactic / Blue Origin，1-3 年）

## 第 2 步：去太空（核心心愿）

```bash
python3 scripts/space.py "tier=suborbital"
```

输出：

- **Virgin Galactic VSS Unity**：90 km，失重 4 分钟，60 万 USD（约 435w CNY），3 天训练，FAA 商业宇航员之翼
- **Blue Origin New Shepard**：107 km，越过卡门线（100 km 国际通用宇航员定义），拍卖 / 邀约制
- 决策清单：体检 → 资金 → 训练 → 保险 → FAA 知情同意书

```bash
python3 scripts/compliance.py "scope=payment,insurance,medical,legal|experience_id=space_suborbital"
```

输出关键提示：

- 太空意外险全球仅 < 5 家承保（Allianz / Lloyd's of London 等），保费约总价 5-15%
- 跨境支付 60w USD：每年 5w 美元购汇 × N 年 + 境外信用卡 + 持牌私行 ODI；任何「换汇 / 蚂蚁搬家 / 地下钱庄」都是违法
- 离心机 4G 训练：健康成人通常可通过；65 岁以上需医师签字

## 第 3 步：5 年长线 —— 马拉松六大满贯

```bash
python3 scripts/train.py "goal=marathon_bmw6|current_fitness=3"
```

输出：

- Y1：完赛任意一场马拉松 sub 5:00
- Y2-3：柏林（最快 PB） + 芝加哥 + 东京 + 伦敦 + 纽约（5 大慈善 / 抽签）
- Y4-5：波士顿 BQ（35-39 岁男子 ≤ 3:00）
- 体能 gap 提示：当前 tier 3 → 目标 tier 4，建议 6-18 个月体能提升

## 第 4 步：长线之巅 —— 七大洲最高峰

```bash
python3 scripts/unlock.py "budget_cny=2500w|fitness=5|categories=登山远征|age=33|max_lead_months=84"
python3 scripts/train.py "goal=everest|current_fitness=4"
python3 scripts/compliance.py "scope=insurance,medical|experience_id=everest_summit"
```

输出：

- 七顶峰预算 80w-250w CNY，5-7 年
- 珠峰：3 年训练（玉珠峰 → 阿玛达布拉姆 → 卓奥友 → 珠峰）
- 8000m 体检：MRI 头颅 + 肺部 CT + 心脏超声
- 风险：珠峰死亡率 ~1%，必须签遗体后送条款

## 第 5 步：每年的「轻体验」 —— 米其林 + 包场 + 拍场

```bash
python3 scripts/unlock.py "budget_cny=500w|fitness=1|categories=顶级美食,私享包场,文化收藏|age=33|max_lead_months=12"
```

输出：每年可循环的体验：

- 米其林三星巡礼（一年走完巴黎 / 罗马 / 东京 / 京都 / 香港 / 纽约）
- 卢浮宫 / 梵蒂冈闭馆夜场私享导览
- 米兰斯卡拉 / 维也纳金色大厅 / 纽约大都会包厢
- F1 摩纳哥游艇 + 温网决赛日 + 勃艮第特级园朝圣
- 佳士得 / 苏富比夜场举牌（KYC + 信托结构）

## 5 年路径汇总

| 年份 | 主线 | 副线 |
|---|---|---|
| Y1 | PPL（1 年）+ 米其林三星巡礼 | 跳伞五大圣地 / F1 单座 |
| Y2 | 北极破冰船 + 第一座 8000m | 马拉松 ×3（柏林 / 芝加哥 / 东京）|
| Y3 | 南极包船 + KTM 摩托环球 | 马拉松 ×2（伦敦 / 纽约）|
| Y4 | 亚轨道太空（Virgin Galactic）| BQ + 波士顿马拉松 |
| Y5 | 珠峰登顶（七顶峰之首）| 米兰斯卡拉 + 佳士得夜场 |

总预算：1500w-3000w 量级，5000w 资产足够 cover + 留 2000w 持续投资。

## 复盘

- 一辈子最多 3-5 个真正会被记住的体验，不必贪多
- 体能不可逆——35 岁能登珠峰，55 岁就难了。优先做体能门槛高的
- 太空 / 顶峰 / 极地都有真实的死亡率，保险 + 体检 + 持牌专业人士不能省
- 这个 skill 帮你做的不是炫耀清单，是「**人生的下一步是清单可执行的**」
- 任何跨境支付都必须走合规渠道；这是底线

边界提醒：

- 工具不推荐具体俱乐部 / 教练 / 中介 / 拍卖行 / 运营商
- 不构成投资 / 法律 / 医疗 / 保险建议
- Titan 深潜（2023）/ 珠峰 / F1 业余赛道事故均为前车之鉴；本工具不替代专业人士
