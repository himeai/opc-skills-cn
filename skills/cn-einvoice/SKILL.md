---
name: cn-einvoice
description: 中国电子发票开具：诺诺 / 百望 OpenAPI 双供应商支持，覆盖电子普票 / 专票开具、查询、红冲、状态回调。可被 wechatpay / alipay 等收款 skill 直接调用，作为「收款 → 开票」链路最后一公里。Use when 用户提到开发票、电子发票、普票、专票、红冲、抬头、税号、发票回调、诺诺、百望、纸票电子化、税控、销项发票。
---

# 中国电子发票（cn-einvoice）

> 一人公司收完款后绕不开的最后一步：开票。本 skill 抽象了**诺诺发票 / 百望发票**两家最主流的服务商，提供同一套 CLI；你只需切换 `CN_EINVOICE_PROVIDER` 环境变量即可在两家之间迁移。

> 资金 / 税务合规提示：电子发票一经开出即进入税务系统，红冲不可撤销。本 skill **不替你做抬头校验**（重名 / 税号反查），请在业务系统里加确认环节；不替代税务师判断税目与税率。

## Prerequisites

### 账号要求
二选一即可（也可以两家同时开通、按业务量切换）：

#### 诺诺发票
1. 在 https://www.nuonuo.com 开通商家账号并完成税控接入
2. 进入「开放平台」获取 `appKey` / `appSecret` 与 `accessToken`
3. 把销项发票模板审批好

#### 百望发票
1. 在 https://www.baiwang.com 开通账号并完成「云票」接入
2. 在开放平台拿到 `app_key` / `app_secret`
3. 申请「发票开具」「查询」「红冲」三个接口的权限

### 环境变量
```bash
# 选择服务商：nuonuo（默认）或 baiwang
export CN_EINVOICE_PROVIDER="nuonuo"

# 诺诺凭据（provider=nuonuo 时必填）
export CN_EINVOICE_NUONUO_APP_KEY="<appKey>"
export CN_EINVOICE_NUONUO_APP_SECRET="<appSecret>"
export CN_EINVOICE_NUONUO_TAX_NUM="<销方 18 位税号>"
export CN_EINVOICE_NUONUO_TOKEN="<accessToken，可选>"

# 百望凭据（provider=baiwang 时必填）
export CN_EINVOICE_BAIWANG_APP_KEY="<app_key>"
export CN_EINVOICE_BAIWANG_APP_SECRET="<app_secret>"
export CN_EINVOICE_BAIWANG_TAX_NUM="<销方 18 位税号>"

# 通用可选
export CN_EINVOICE_DEFAULT_DRAWER="开票员姓名"
export CN_EINVOICE_NOTIFY_URL="https://your.example.com/einvoice/callback"
export CN_EINVOICE_SANDBOX="0"  # 1 = 走沙箱
```

### 依赖
仅 stdlib（HMAC / MD5 签名 + `urllib.request`）。无需第三方包。

## Quick Start

```bash
# 1) 开一张普票
python3 scripts/issue.py "order_no=ORD20260601A001|amount=99|tax_rate=0.06|buyer_name=北京某某科技有限公司|buyer_tax_num=91110000XXXXXXXXXX|buyer_email=ap@buyer.com|item_name=技术咨询服务|invoice_type=normal"

# 2) 查这张票出了没（异步）
python3 scripts/query.py "order_no=ORD20260601A001"

# 3) 红冲
python3 scripts/redflush.py "invoice_code=011001900111|invoice_no=12345678|reason=客户要求重开"
```

预期 `issue.py` 响应（节选）：
```json
{
  "provider": "nuonuo",
  "order_no": "ORD20260601A001",
  "items_count": 1,
  "response": {"code": "E0000", "describe": "处理成功", "result": {"serialNo": "..."}}
}
```

## Usage Examples

### 场景 1：和 wechatpay 串联——支付成功立即开票
```bash
# 1. wechatpay/notify.py 校验回调拿到 out_trade_no + 金额
# 2. 业务层调本 skill 的 issue.py：
python3 scripts/issue.py "order_no=$OUT_TRADE_NO|amount=$AMOUNT_YUAN|tax_rate=0.06|buyer_name=$BUYER|item_name=咨询服务"
# 3. 把回执 invoice_no / serialNo 存入订单表
```

### 场景 2：开专票（B2B）
```bash
python3 scripts/issue.py "order_no=ORD20260601B001|amount=10000|tax_rate=0.13|buyer_name=...|buyer_tax_num=...|buyer_address_phone=...|buyer_bank_account=...|item_name=软件订阅服务|invoice_type=special"
```

### 场景 3：多商品开同一张票
```bash
python3 scripts/issue.py 'order_no=ORD20260601C001|buyer_name=客户公司|invoice_type=normal|items_json=[{"name":"咨询费","amount":500,"tax_rate":0.06,"unit":"次","quantity":1},{"name":"差旅费","amount":120,"tax_rate":0.06,"unit":"次","quantity":1}]'
```

### 场景 4：从沙箱切到生产
```bash
export CN_EINVOICE_SANDBOX=1   # 沙箱测全链路
# 验证通过后
export CN_EINVOICE_SANDBOX=0
```

### 场景 5：从诺诺迁到百望
```bash
export CN_EINVOICE_PROVIDER=baiwang
# 切到百望对应的 APP_KEY / APP_SECRET / TAX_NUM 即可，CLI 不变
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/issue.py "order_no=...\|amount=...\|tax_rate=...\|buyer_name=...\|item_name=..."` | 开票（普/专/全电） | `\|` 分隔 | JSON |
| `python3 scripts/query.py "order_no=..."` | 按订单号查发票 | `\|` 分隔 | JSON |
| `python3 scripts/query.py "invoice_no=..."` | 按发票号查 | `\|` 分隔 | JSON |
| `python3 scripts/redflush.py "invoice_no=...\|reason=..."` | 申请红冲 | `\|` 分隔 | JSON |

输入约定：键值对 `|` 分隔，金额单位为**元**；多商品用 `items_json=[...]` 传 JSON 数组。

## Scripts

### `scripts/credential.py`
按 `CN_EINVOICE_PROVIDER` 选择凭据集；缺失时给出明确错误。

### `scripts/einvoice_http.py`
唯一接触签名的模块：
- 诺诺：`HMAC-SHA1(appSecret, sortedParams + body)`，hex
- 百望：`MD5(secret + sorted(k+v) + body + secret)`，upper hex
- 走 stdlib `urllib.request`，无 SDK 依赖

### `scripts/issue.py` / `scripts/query.py` / `scripts/redflush.py`
分别对应开票 / 查询 / 红冲；按 provider 装配请求体后转给 `einvoice_http.call`。

## API Info

- **诺诺**: `https://sdk.nuonuo.com/open/v1/services` ｜ Docs: https://open.nuonuo.com/document
- **百望**: `https://openapi.baiwang.com/router/rest` ｜ Docs: https://open.baiwang.com/doc
- **沙箱**: 两家都提供，受 `CN_EINVOICE_SANDBOX=1` 控制
- **Rate Limits**: 视套餐而定，常规 5-50 QPS；超限服务商会直接返回 `LIMIT_FREQUENCY`，本 skill 不重试

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `missing credentials: CN_EINVOICE_NUONUO_APP_KEY` | provider 与凭据不匹配 | `export CN_EINVOICE_PROVIDER=nuonuo` 或对应换百望凭据 |
| `unsupported provider 'xxx'` | 拼错了 | 仅支持 `nuonuo` / `baiwang` |
| `HTTP 200` 但响应 `code != E0000` | 业务字段不合规（抬头税号长度 / 税率不合法） | 看 `describe` / `message`；常见是税率小数位过多 |
| 异步回执长期不到 | 回调 URL 不可公网访问 | 用 `query.py` 主动轮询；生产环境务必让 `CN_EINVOICE_NOTIFY_URL` 公网可达 |

## References

- 增值税电子普通发票管理办法（国家税务总局）
- 关于在全国范围内推行使用全面数字化的电子发票工作的公告
- 配套 skill：`wechatpay`、`alipay`、`cn-tax`

## Notes

- **仅调用**两家服务商的官方 OpenAPI；不做爬虫、不做协议逆向
- 不替你做抬头反查 / 重复开票去重，请在业务侧自己做幂等
- 不替代税务师判断税目 / 税率 / 是否能开
- 红冲操作不可撤销，本 skill 不做客户端二次确认；请在业务系统加审批环节
- 任何情况下都不要把 `appSecret` / `accessToken` 写进 .py / .md / .json
