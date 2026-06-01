# 例：从交回公章到摆摊出第一单的 30 天

> 假设你是一位上一次创业失败的 OPC 创始人，杭州，个独主体，没员工，没外债，房贷在缴，跑道 3 个月。
> 这里没有鸡汤，只有清单。

## Day 0：体检 — 我现在到底什么状态

```bash
python3 scripts/runway.py "city=杭州|monthly_cost=8000|cash=24000|debt=0|has_house_loan=yes|was_employee=no|prev_contribution_years=0"
```

输出关键值：
- `runway_months`: 3.0 → **橙色警告**「必须立即降本 + 上零工，不要犹豫」
- `unemployment_benefit.eligible`: false → 个独投资人本人通常未缴失业保险，不可领
- `flexible_insurance.medical_monthly_range_cny`: 350-900 → 医保不能断
- `action_list`: 立即开始零工 / 把外食 + 订阅砍光 / 优先保住房贷

## Day 1-3：把公司体面送走

```bash
python3 scripts/shutdown.py "entity=个独|location=杭州|has_employees=no|has_debt=no|has_abnormal=no"
```

输出：
- `recommended_path`: 简易注销
- `typical_weeks`: 2-3 周
- `steps`: 5 步（清税 → 工商注销 → 公章缴销 → 银行销户 → 社保切换灵活就业）
- `common_blockers`: 园区核定征收要先拿无欠税证明、对公余额转出涉个税

> 同时去社区医院办健康证（30-50 元，1-2 天出证），后面跑外卖 / 摆摊都用得上。

## Day 4-10：先把外卖跑起来，把房贷月供锁住

```bash
python3 scripts/gig.py "city=杭州|wheels=电动车|hours_per_day=8|need_insurance=no|prefer=外卖"
```

输出 Top 3：
1. 美团骑手（专送）→ 估算日入 280 元 / 月入 7000 元
2. 饿了么蜂鸟（专送）→ 估算日入 250 元
3. 达达快送 → 估算日入 240 元

> 第一周先专送（站点合作商缴五险），等熟悉路线后再切众包灵活时间。
> 房贷 5000 / 月先稳住。

## Day 11-30：周末试摆摊，找回选品的手感

```bash
python3 scripts/stall.py "city=杭州|budget_cny=3000|category=饮品冷食|night_or_day=night"
```

输出：
- `city_policy.open_areas`: 武林夜市 / 胜利河美食街 / 拱宸桥夜市 / 运河夜市
- `category_overview.gross_margin_pct`: [60, 80]
- `roi_estimate_mid.daily_gross_cny`: ~1100 元（按 105 单 × 12 元客单）
- `equipment_checklist`: 折叠摊位 / 灯具 / 收款码 / 保温桶 / 制冰机 / 一次性杯具
- `license_required`: 健康证 + 小食品摊贩备案卡

> 先在杭州武林夜市排队（热门夜市排队 3-6 个月），同时申请二线市集做练手。
> 周末 2 天试摊，验证选品 + 出摊节奏，工作日继续跑专送。

## Day 30：体检一次，看要不要开始想下一步

```bash
python3 scripts/restart.py "runway_months=4|burnout=4|asset=技术能力|family=条件支持|gap_months=1|prev_industry=SaaS"
```

输出：
- `decision.verdict`: **并行模式** — 跑道一般、心力一般，零工 + 复业并行，不要 all in
- `recommended_paths`: 自由职业 / 一人 SaaS / 代运营 三条
- `exit_red_lines.must_set_before_start`: 时间 / 资金 / 心力 / 家庭 4 项硬红线

> 上一次创业的代码 + 客户访谈记录还在，先把它们改写成自由职业 portfolio。
> 周末 2 天用一半接私单（自由职业），一半摆摊。
> 给自己设定：6 个月内私单收入 ≥ 月房贷 → 才考虑回到全职复业。

## 30 天后的状态

- 公司已注销，工商无尾巴
- 医保未断，灵活就业身份切换完成
- 现金流：外卖 7000 + 摆摊 2000 + 接单 3000 ≈ 12000 / 月，跑道从 3 月延长到 6 月+
- 复盘文档已写到 4000 字，开始在小红书发「OPC 失败复盘」系列
- 心情：累，但**人生的容错率确实大得可怕**

## 下一步可以做的

- 6 个月后 burnout 降到 ≤ 3 → 重新跑 `restart.py`，决定是否 all in 复业
- 如果接单收入 ≥ 房贷 + 生活费 → 可以减少零工，扩大自由职业 / 一人 SaaS 投入
- 如果半年后零工依然是主收入 → 也很好，「下车」本来就是一个完整的生活方式选项
