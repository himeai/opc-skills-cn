# 例：处理微信支付回调

## 场景
微信支付 V3 异步回调到 `WECHATPAY_NOTIFY_URL`，你需要：
1. 验签（用平台证书）
2. 解密 resource（用 APIv3 密钥）
3. 拿到 `out_trade_no` / `transaction_id` 入账

## 输入
你的 web 框架 controller 把请求头与 body 拼成一个 JSON 喂给脚本：

```bash
echo '{
  "headers": {
    "Wechatpay-Signature": "lwc...",
    "Wechatpay-Timestamp": "1748761200",
    "Wechatpay-Nonce": "abc123",
    "Wechatpay-Serial": "<platform-cert-serial>"
  },
  "body": "{\"id\":\"...\",\"event_type\":\"TRANSACTION.SUCCESS\",\"resource\":{\"ciphertext\":\"...\",\"nonce\":\"...\",\"associated_data\":\"transaction\"}}"
}' | python3 scripts/notify.py "stdin=1"
```

## 输出
```json
{
  "verified": true,
  "event_type": "TRANSACTION.SUCCESS",
  "summary": "支付成功",
  "decrypted": {
    "out_trade_no": "ORD20260601A001",
    "transaction_id": "4200001234202606011234567890",
    "trade_state": "SUCCESS",
    "amount": {"total": 19900, "currency": "CNY", "payer_total": 19900}
  }
}
```

## 怎么集成
- `verified=false` → 直接返回 `{"code":"FAIL","message":"INVALID_SIGN"}` 给微信
- `verified=true` → 应用层根据 `decrypted.out_trade_no` 幂等更新订单；返回 `{"code":"SUCCESS"}`
- 如果 `decrypted` 为空说明 body 没有 `resource` 字段，常见于退款回调；用同一脚本处理也可以（事件类型 `REFUND.SUCCESS`）
