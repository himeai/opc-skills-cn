# 例：JSAPI 下单（公众号场景）

## 场景
微信公众号内一键购买 199 元年度订阅，需要在前端拿到 `prepay_id` 唤起 `chooseWXPay`。

## 输入
```bash
python3 scripts/order.py "type=jsapi|out_trade_no=ORD20260601A001|amount=199|description=年度订阅|openid=oABC123XYZ"
```

## 输出（节选）
```json
{
  "type": "jsapi",
  "out_trade_no": "ORD20260601A001",
  "amount_fen": 19900,
  "response": {
    "prepay_id": "wx2026060112345678..."
  }
}
```

## 接下来你要做什么
1. 后端拿到 `prepay_id`，按官方文档对 `appId|timeStamp|nonceStr|package=prepay_id=...|signType=RSA` 再次签名给前端
2. 前端 `WeixinJSBridge.invoke('getBrandWCPayRequest', ...)` 唤起支付
3. 用户支付成功 → 微信回调 `WECHATPAY_NOTIFY_URL` → 你的服务器把 body + headers 喂给 `notify.py "stdin=1"` 完成验签 + 入账
