# 例：支付成功后立即开普票

## 场景
你跑了一个咨询业务，客户在公众号支付 99 元后，要给他开「技术咨询服务」普票，抬头是公司，需要邮箱发送。

## 输入
```bash
python3 scripts/issue.py "order_no=ORD20260601A001|amount=99|tax_rate=0.06|buyer_name=北京某某科技有限公司|buyer_tax_num=91110000XXXXXXXXXX|buyer_email=ap@buyer.com|item_name=技术咨询服务|invoice_type=normal"
```

## 输出（节选）
```json
{
  "provider": "nuonuo",
  "order_no": "ORD20260601A001",
  "items_count": 1,
  "response": {
    "code": "E0000",
    "describe": "处理成功",
    "result": {"serialNo": "20260601A001abcd"}
  }
}
```

## 怎么集成
1. 把 `serialNo` 存入订单表
2. 起一个 cron 每隔 30 秒拿这些 `serialNo` 调 `query.py`，拿到 `invoiceCode + invoiceNo + 下载链接`
3. 把下载链接通过邮件 / 公众号客服消息推给客户
4. 整个链路保持幂等：同一个 `order_no` 服务商会拒绝重复开票（返回错误码 E9999 之类，看 describe）
