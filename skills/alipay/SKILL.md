---
name: alipay
description: 支付宝 OpenAPI 商户接入：当面付（条码/扫码）、PC 网站支付、手机网站支付、APP 支付、查询、关单、退款、异步通知验签。RSA2 签名，仅 stdlib + cryptography。Use when 用户提到支付宝、alipay、当面付、扫码支付、pc 支付、wap 支付、APP 支付、退款、对账、return_url、notify_url、RSA2、应用私钥、支付宝公钥。
---

# 支付宝 OpenAPI 商户接入（alipay）

> 给 OPC / 微型 SaaS / 课程与电商订阅服务商一个最小可运行的支付宝商户接入。覆盖**当面付 / PC / WAP / APP** 四种场景的下单、查询、关单、退款，与异步通知验签。所有签名验签**本地完成**，不依赖支付宝官方 SDK（避免巨型依赖）。

> 资金安全提示：本 skill 涉及真实资金。建议先用沙箱（`ALIPAY_SANDBOX=1`）联调，确认 `notify_url` 公网可达且验签通过后再切生产；**任何情况下都不要把应用私钥贴进对话或日志**。

## Prerequisites

### 账号要求
1. 在 https://open.alipay.com 创建应用（自研应用即可）
2. 在「开发设置 - 接口加签方式」选择 RSA2，本地生成密钥对，把**应用公钥**上传给支付宝，把**支付宝公钥**复制下来
3. 申请并通过：当面付 / 电脑网站支付 / 手机网站支付 / APP 支付 中你需要的能力

### 环境变量
```bash
export ALIPAY_APP_ID="<2021xxxxxxxxxxxx>"

# 应用私钥（你自己生成的）— 二选一
export ALIPAY_APP_PRIVATE_KEY_PATH="/secure/path/to/app_private_key.pem"
# 或：
# export ALIPAY_APP_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

# 支付宝公钥（从 open.alipay.com 拷贝，用于验签）— 二选一
export ALIPAY_PUBLIC_KEY_PATH="/secure/path/to/alipay_public_key.pem"
# 或：
# export ALIPAY_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"

# 默认回调（也可在命令行覆盖）
export ALIPAY_NOTIFY_URL="https://your.example.com/alipay/notify"
export ALIPAY_RETURN_URL="https://your.example.com/alipay/return"

# 可选
export ALIPAY_SIGN_TYPE="RSA2"   # 默认 RSA2，不建议用 RSA
export ALIPAY_SANDBOX="0"        # 1 = 走沙箱网关
```

### 依赖
```bash
pip install cryptography
```

## Quick Start

```bash
# 1) PC 网站支付：拿到一个跳转 URL，浏览器打开就跳到支付宝收银台
python3 scripts/order.py "type=page|out_trade_no=ORD20260601P001|amount=199|subject=年度订阅"

# 2) 当面付（扫码）：返回 qr_code，由你的前端生成二维码
python3 scripts/order.py "type=precreate|out_trade_no=ORD20260601Q001|amount=29.9|subject=咖啡一杯"

# 3) 查询订单
python3 scripts/query.py "action=query|out_trade_no=ORD20260601P001"

# 4) 退款
python3 scripts/refund.py "action=refund|out_trade_no=ORD20260601P001|out_request_no=REFUND001|amount=199|reason=客户取消"

# 5) 处理异步通知（在 web 框架 controller 里调）
echo "out_trade_no=ORD...&trade_no=...&trade_status=TRADE_SUCCESS&...&sign_type=RSA2&sign=..." \
  | python3 scripts/notify.py "stdin=1"
```

## Usage Examples

### 场景 1：手机网站支付（公众号外的 H5）
```bash
python3 scripts/order.py "type=wap|out_trade_no=H5202606010001|amount=29.9|subject=单次咨询"
# response.redirect_url 直接 302 给客户端
```

### 场景 2：当面付—条码支付（用户出示付款码）
```bash
python3 scripts/order.py "type=face_to_face|out_trade_no=POS202606010001|amount=29.9|subject=门店消费|auth_code=283892323456789012"
```

### 场景 3：APP 支付（生成 orderString 给客户端 SDK）
```bash
python3 scripts/order.py "type=app|out_trade_no=APP202606010001|amount=99|subject=会员开通"
# response.alipay_trade_app_pay_response 里取 trade_no / 整个 form 串
```

### 场景 4：关单（避免长时间未支付占位）
```bash
python3 scripts/query.py "action=close|out_trade_no=ORD20260601P001"
```

### 场景 5：退款查询（确认是否真的退到账）
```bash
python3 scripts/refund.py "action=query|out_trade_no=ORD20260601P001|out_request_no=REFUND001"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/order.py "type=page\|out_trade_no=...\|amount=...\|subject=..."` | PC 网站支付（返回 redirect_url） | `\|` 分隔 | JSON |
| `python3 scripts/order.py "type=wap\|..."` | 手机网站支付 | `\|` 分隔 | JSON |
| `python3 scripts/order.py "type=app\|..."` | APP 支付 | `\|` 分隔 | JSON |
| `python3 scripts/order.py "type=precreate\|..."` | 当面付扫码 | `\|` 分隔 | JSON |
| `python3 scripts/order.py "type=face_to_face\|...\|auth_code=..."` | 当面付条码 | `\|` 分隔 | JSON |
| `python3 scripts/query.py "action=query\|out_trade_no=..."` | 查询 | `\|` 分隔 | JSON |
| `python3 scripts/query.py "action=close\|out_trade_no=..."` | 关单 | `\|` 分隔 | JSON |
| `python3 scripts/query.py "action=cancel\|out_trade_no=..."` | 撤销（当面付） | `\|` 分隔 | JSON |
| `python3 scripts/refund.py "action=refund\|out_trade_no=...\|out_request_no=...\|amount=..."` | 退款 | `\|` 分隔 | JSON |
| `python3 scripts/refund.py "action=query\|out_trade_no=...\|out_request_no=..."` | 退款查询 | `\|` 分隔 | JSON |
| `python3 scripts/notify.py "stdin=1"` | 异步通知验签 | stdin form | JSON |

输入约定：键值对 `|` 分隔；金额单位**元**（保留两位小数）；金额字段可写 `amount=12.50` 或 `amount_yuan=12.50`。

## Scripts

### `scripts/credential.py`
统一从环境变量读取 `ALIPAY_*`；私钥与支付宝公钥都支持 inline / 路径双形式。

### `scripts/alipay_http.py`
- 唯一接触私钥的模块
- 拼接公共参数（`app_id` / `method` / `timestamp` / `version` / `biz_content` …）
- 按 `ALIPAY_SIGN_TYPE` 用 RSA2（默认）或 RSA 签名
- `call()` 做 POST + JSON 解析
- `build_redirect_url()` 给 `page.pay` / `wap.pay` 用，直接拼成签名好的跳转 URL
- `verify_callback()` 用支付宝公钥验签异步通知

### `scripts/order.py` / `query.py` / `refund.py`
按场景装配 `biz_content` 后转给 `alipay_http`，不做业务侧补单逻辑。

### `scripts/notify.py`
读取 `application/x-www-form-urlencoded` 通知体（stdin 或 base64），验签后输出标准化结果。

## API Info

- **Gateway (prod)**: `https://openapi.alipay.com/gateway.do`
- **Gateway (sandbox)**: `https://openapi-sandbox.dl.alipaydev.com/gateway.do`
- **Auth**: 应用私钥 RSA2 签名 + `app_id`；通知用支付宝公钥验签
- **Rate Limits**: 视接口而定，常规 100-1000 QPS
- **Docs**: https://opendocs.alipay.com/open/02e7gq

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `missing credentials: ALIPAY_APP_PRIVATE_KEY_PATH or ALIPAY_APP_PRIVATE_KEY` | 没配应用私钥 | 任选一种环境变量；inline 形式记得保留换行 |
| `Invalid sign / 40004 ACQ.SIGN_ERROR` | 签名失败 | 1) 确认 sign_type=RSA2 与 open.alipay.com 配置一致 2) 确认上传的是「应用公钥」不是「支付宝公钥」 |
| `Insufficient SCOPE` | 未签约对应支付能力 | 在 open.alipay.com 应用详情页申请 `alipay.trade.page.pay` 等能力 |
| 通知 `verified=false` | 支付宝公钥不对 / sign_type 不匹配 | 重新从 open.alipay.com 拷贝支付宝公钥；确保 RSA2 一致 |
| `redirect_url` 太长 | 浏览器拒收 | 把 GET 跳转改成「表单 POST 自动提交」，把 params 拆成 hidden input |

## References

- 支付宝开放文档：https://opendocs.alipay.com/open/02e7gq
- 当面付：https://opendocs.alipay.com/open/02emkp
- PC 网站支付：https://opendocs.alipay.com/open/270/105898
- 手机网站支付：https://opendocs.alipay.com/open/203/107090
- APP 支付：https://opendocs.alipay.com/open/204/105465
- 配套 skill：`wechatpay`、`cn-einvoice`

## Notes

- **仅调用**支付宝官方 OpenAPI；不做爬虫、不做协议逆向、不做未授权代收代付
- 不打印任何凭据；HTTP 错误会原样返回响应体，请自行屏蔽日志
- 不做业务侧幂等（你的订单系统应自己保证 `out_trade_no` 不重复，退款侧保证 `out_request_no` 不重复）
- 不持久化任何业务数据，所有状态通过环境变量 + 命令行参数传入
