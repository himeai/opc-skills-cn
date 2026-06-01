---
name: wechatpay
description: 微信支付 V3 商户接入：JSAPI / Native / H5 / APP 下单、查询、关单、退款、回调验签 + AES-GCM 解密、平台证书管理。仅调用微信支付商户官方 API V3。Use when 用户提到微信支付、wxpay、wechatpay、收款、扫码支付、JSAPI、Native、商户号、mch_id、APIv3、退款、对账、回调、notify、商户证书、平台证书。
---

# 微信支付 V3 商户接入（wechatpay）

> 给 OPC / 微型 SaaS / 课程与咨询服务商一个最小可运行的微信支付商户接入。只覆盖**官方商户 API V3**，不做营销、不做代收代付、不做服务商分账。私钥与 APIv3 密钥全部从环境变量读取，回调验签与解密**全部本地完成**。

> 资金安全提示：本 skill 涉及真实资金流转，请先在沙箱或使用小额测试，确认链路正确后再切到生产；**任何情况下都不要把私钥 / APIv3 密钥贴进对话或日志**。

## Prerequisites

### 账号要求
- 已开通微信支付商户号（普通商户即可，服务商需自行调整 mchid 字段）
- 已在 https://pay.weixin.qq.com 商户后台「API 安全」里：
  - 申请 **API 证书**（得到 `apiclient_key.pem` 私钥 + 证书序列号）
  - 设置 **APIv3 密钥**（32 字节字符串，回调解密用）

### 环境变量
```bash
export WECHATPAY_MCH_ID="<10 位商户号>"
export WECHATPAY_APIV3_KEY="<32 字节 APIv3 密钥>"
export WECHATPAY_CERT_SERIAL_NO="<API 证书序列号>"

# 私钥二选一：路径或 inline PEM
export WECHATPAY_PRIVATE_KEY_PATH="/secure/path/to/apiclient_key.pem"
# 或：
# export WECHATPAY_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

# 关联公众号 / 小程序 appid（jsapi 必填，其它支付方式可在命令行覆盖）
export WECHATPAY_APP_ID="<wx... appid>"

# 默认回调地址（也可在 order.py 命令行覆盖）
export WECHATPAY_NOTIFY_URL="https://your.example.com/wxpay/notify"
export WECHATPAY_REFUND_NOTIFY_URL="https://your.example.com/wxpay/refund-notify"

# 平台证书存放路径（cert.py download 后自动写入；notify.py 验签需要）
export WECHATPAY_PLATFORM_CERT_PATH="./platform_certs/<serial>.pem"
```

### 依赖
```bash
pip install cryptography
```
仅用于 RSA-SHA256 签名 / 验签 与 AES-GCM 解密；HTTP 走 stdlib `urllib.request`。

## Quick Start

```bash
# 1) 第一次部署：拉取并保存平台证书（每月跑一次防止到期）
python3 scripts/cert.py "action=download|out_dir=./platform_certs"

# 2) JSAPI 下单（公众号支付）
python3 scripts/order.py "type=jsapi|out_trade_no=ORDER20260601001|amount=12.50|description=咨询服务|openid=oABC123XYZ"

# 3) 查订单
python3 scripts/query.py "action=get|out_trade_no=ORDER20260601001"

# 4) 退款
python3 scripts/refund.py "out_trade_no=ORDER20260601001|out_refund_no=REFUND20260601001|refund=12.50|total=12.50|reason=客户取消"

# 5) 处理回调（在 web 框架 controller 里调）
echo '{"headers":{"Wechatpay-Signature":"...","Wechatpay-Timestamp":"...","Wechatpay-Nonce":"..."},"body":"{...}"}' \
  | python3 scripts/notify.py "stdin=1"
```

## Usage Examples

### 场景 1：Native 扫码支付（PC 收银台）
```bash
python3 scripts/order.py "type=native|out_trade_no=PC202606010001|amount=199|description=年度订阅"
# 取响应中的 code_url 生成二维码即可
```

### 场景 2：H5 支付（移动浏览器）
```bash
python3 scripts/order.py "type=h5|out_trade_no=H5202606010001|amount=29.9|description=单次咨询|client_ip=1.2.3.4"
# 取响应中的 h5_url 跳转
```

### 场景 3：APP 支付
```bash
python3 scripts/order.py "type=app|out_trade_no=APP202606010001|amount=99|description=会员开通|appid=wx_app_appid"
```

### 场景 4：商户号订单号 vs 微信订单号查询
```bash
python3 scripts/query.py "action=get|out_trade_no=ORDER20260601001"
python3 scripts/query.py "action=get|transaction_id=4200001234202606011234567890"
```

### 场景 5：关单（避免长时间未支付被自动支付）
```bash
python3 scripts/query.py "action=close|out_trade_no=ORDER20260601001"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/cert.py "action=download\|out_dir=..."` | 下载并保存平台证书 PEM | `\|` 分隔 | JSON |
| `python3 scripts/order.py "type=jsapi\|out_trade_no=...\|amount=...\|description=..."` | 创建订单 | `\|` 分隔 | JSON |
| `python3 scripts/query.py "action=get\|out_trade_no=..."` | 查询订单 | `\|` 分隔 | JSON |
| `python3 scripts/query.py "action=close\|out_trade_no=..."` | 关闭订单 | `\|` 分隔 | JSON |
| `python3 scripts/refund.py "out_trade_no=...\|out_refund_no=...\|refund=...\|total=..."` | 申请退款 | `\|` 分隔 | JSON |
| `python3 scripts/notify.py "stdin=1"` | 校验回调 + 解密 resource | stdin JSON | JSON |

输入约定：键值对用 `|` 分隔，键值用 `=` 分隔；金额支持 `amount=<元>` 或 `amount_fen=<分>`。

## Scripts

### `scripts/credential.py`
统一从 env 读取 `WECHATPAY_*` 凭据，私钥支持 inline 与路径两种形式；`assert_ready()` 会在缺失时给出明确错误。

### `scripts/wxpay_http.py`
唯一接触私钥的模块。封装 V3 鉴权 header（`WECHATPAY2-SHA256-RSA2048`）、RSA-SHA256 签名、`urllib.request` 调用与错误解码；所有业务脚本通过 `request_v3(method, path, payload)` 发请求。

### `scripts/order.py` / `query.py` / `refund.py`
分别对应下单 / 查单关单 / 退款，仅做参数装配 + 转发；不做业务侧补单逻辑（你的应用层应该自己幂等）。

### `scripts/notify.py`
回调验签 + AES-GCM 解密：
- 用本地缓存的平台证书 PEM 校验 `Wechatpay-Signature`
- 用 `WECHATPAY_APIV3_KEY` 解密 `resource.ciphertext`
- 输出 `{verified, event_type, summary, decrypted}`，由你的应用层根据 `event_type` 入账

### `scripts/cert.py`
下载平台证书。微信支付平台证书会**轮换**，建议加到月度 cron 里。

## API Info

- **Base URL**: `https://api.mch.weixin.qq.com`
- **Auth**: 商户私钥 RSA-SHA256 签名 + 商户 API 证书序列号；回调用平台证书验签
- **Rate Limits**: 视接口而定，常见接口 600 QPM；超过返回 `429`，本 skill 不做重试，由你的应用层退避
- **Docs**: https://pay.weixin.qq.com/docs/merchant/products/native-payment/introduction.html

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `missing credentials: WECHATPAY_PRIVATE_KEY_PATH or WECHATPAY_PRIVATE_KEY` | 没配置私钥 | 任选一种环境变量；inline 形式记得保留换行 |
| `HTTP 401: SIGN_ERROR` | 签名失败 | 检查 `WECHATPAY_CERT_SERIAL_NO` 是否与私钥配对、商户号是否匹配 |
| `HTTP 400: PARAM_ERROR amount` | 金额单位错误 | API 接受**分**为整数；本 skill 已自动 `元 * 100`，但小心浮点累积误差，建议传 `amount_fen` |
| 回调 `verified=false` | 平台证书过期 / 缺失 | 重新跑 `cert.py download`，更新 `WECHATPAY_PLATFORM_CERT_PATH` |
| 解密 `InvalidTag` | APIv3 密钥不对 | 商户后台重新拷贝 32 字节 APIv3 密钥 |

## References

- 微信支付 V3 接入指南：https://pay.weixin.qq.com/docs/merchant/development/interface-rules/introduction.html
- API 字典（JSAPI / Native / H5 / APP / 退款）：https://pay.weixin.qq.com/docs/merchant/apis/jsapi-payment/direct-jsons/jsapi-prepay.html
- 平台证书：https://pay.weixin.qq.com/docs/merchant/development/interface-rules/wechatpay-certificates.html
- 配套 skill：`cn-einvoice`（开票）、`alipay`（同账户支付宝收款）

## Notes

- 仅调用**微信支付商户官方 API V3**，不做爬虫、不做协议逆向、不做未授权代收代付
- 不打印任何凭据；HTTP 错误会原样返回响应体，请自行屏蔽日志
- 不做业务侧幂等（你的订单系统应自己保证 `out_trade_no` 不重复）
- 不持久化任何业务数据，所有状态通过环境变量 + 命令行参数传入
