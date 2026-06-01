# 例：PC 网站支付（年度订阅 199 元）

## 场景
用户在你的 SaaS 控制台点「升级到 Pro」按钮，后端拼一条跳转 URL，前端 302 即可跳到支付宝收银台。

## 输入
```bash
python3 scripts/order.py "type=page|out_trade_no=ORD20260601P001|amount=199|subject=Pro 年度订阅"
```

## 输出（节选）
```json
{
  "type": "page",
  "out_trade_no": "ORD20260601P001",
  "amount_yuan": "199.00",
  "redirect_url": "https://openapi.alipay.com/gateway.do?app_id=...&method=alipay.trade.page.pay&...&sign=..."
}
```

## 怎么集成
1. 后端把 `redirect_url` 直接写进 302 Location 头返回给前端
2. 用户在支付宝收银台付完后，浏览器跳回 `ALIPAY_RETURN_URL`（你设置的同步回跳地址）
3. 同时支付宝服务器异步 POST 到 `ALIPAY_NOTIFY_URL`，你的 controller 把 body 喂给 `notify.py "stdin=1"`
4. `verified=true` 且 `trade_status=TRADE_SUCCESS` → 应用层幂等更新订单
