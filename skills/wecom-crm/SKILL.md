---
name: wecom-crm
description: 企业微信客户运营（WeCom CRM）：客户联系、客户标签、客户群、欢迎语、合规群发、企业朋友圈。仅包装企业微信官方 OpenAPI，禁止批量加好友 / 群发骚扰 / 协议逆向。Use when 用户提到企业微信、wecom、企微、客户联系、外部联系人、external_contact、客户标签、客户群、群发、企业朋友圈、moments、欢迎语、CRM、私域。
---

# 企业微信客户运营（wecom-crm）

> 给 OPC / 一人公司 / 微型 SaaS / 课程顾问一个最小可运行的「企业微信私域」工具箱：
> 客户联系、标签、客户群、欢迎语、合规群发、企业朋友圈，**仅包装企业微信官方 OpenAPI**。

> PIPL 合规边界：所有客户 `external_userid` 由企业微信平台分配，本 skill 不收集 / 不存储 / 不外发任何客户原始联系方式（手机号、微信号）。
> 红线：禁止批量加好友、私信群发骚扰、刷量、协议逆向；群发频率必须遵守企业微信平台规则（每个客户每自然月最多 1 条主动群发）。

## Prerequisites

### 账号要求
- 已注册并完成认证的「企业微信」企业（https://work.weixin.qq.com）
- 在「我的企业 → 应用管理」启用对应模块：
  - 「客户联系」（外部联系人 API、客户群、欢迎语、群发、朋友圈）
  - 自建应用（如需消息推送、菜单管理）
- 在「客户联系 → API → 配置可调用接口的应用 / Secret」分别拷贝各模块的 Secret

### 环境变量
```bash
export WECOM_CORP_ID="ww1234567890abcdef"

# 不同业务模块使用不同 corpsecret（按需配置，不需要的模块可以不配）
export WECOM_SECRET_EXTERNAL_CONTACT="<客户联系 secret>"   # contact / tag / group / welcome / mass
export WECOM_SECRET_CUSTOMER_GROUP="<客户群 secret>"       # 部分接口与 external_contact 共用
export WECOM_SECRET_MOMENTS="<企业朋友圈 secret>"          # moments
export WECOM_SECRET_APP="<自建应用 secret>"                # 应用消息推送（选配）

export WECOM_AGENT_ID="1000002"                            # 自建应用 agent_id（选配）
export WECOM_TOKEN_CACHE_DIR="./.wecom_tokens"             # 默认即此，可选
```

### 依赖
仅 stdlib（`urllib.request` / `json`），无第三方依赖。

## Quick Start

```bash
# 1) 列出配置了「客户联系」的成员
python3 scripts/contact.py "action=list_followers"

# 2) 列出某成员的外部客户
python3 scripts/contact.py "action=list_external|userid=zhangsan"

# 3) 给客户打标签（external_userid 来自上一步）
python3 scripts/tag.py "action=mark|userid=zhangsan|external_userid=woAJ2Gxxx|add=etxxxA,etxxxB"

# 4) 创建一条客户群发任务（合规群发：1 个月只能给同一客户发 1 条）
python3 scripts/mass.py "action=create|sender=zhangsan|text=本月限时优惠详情|external_userids=woAJ2Gxxx,woAJ2Gyyy"

# 5) 创建一条企业朋友圈
python3 scripts/moments.py "action=create|text=新课程上线|sender_userids=zhangsan,lisi|image_media_ids=MEDIA_ID_1"
```

## Usage Examples

### 场景 1：盘点全员客户资产
```bash
# 先列出有「客户联系」权限的员工
python3 scripts/contact.py "action=list_followers"
# 再循环每个员工拉外部客户列表
python3 scripts/contact.py "action=list_external|userid=zhangsan"
```

### 场景 2：客户分层 → 打标签
```bash
# 先看现有标签组
python3 scripts/tag.py "action=list"

# 新增一个标签组
python3 scripts/tag.py "action=add_group|group_name=客户阶段|order=1"

# 给标签组加标签
python3 scripts/tag.py "action=add_tag|group_id=etGROUP_ID|tag_name=高意向|tag_order=1"

# 给客户打标签 / 取消标签
python3 scripts/tag.py "action=mark|userid=zhangsan|external_userid=woAJxxx|add=etTAGA,etTAGB|remove=etTAGC"
```

### 场景 3：客户群运营看板
```bash
python3 scripts/group.py "action=list|status_filter=0|limit=100"
python3 scripts/group.py "action=get|chat_id=wrCxxxxxxx"
python3 scripts/group.py "action=stats|day_begin=2026-05-01|day_end=2026-05-31"
```

### 场景 4：欢迎语模板与回调发送
```bash
# 配置「入群欢迎语」模板
python3 scripts/welcome.py "action=add_template|text=欢迎加入，回复1领取资料"

# 在「客户添加事件」回调里拿到 welcome_code 后实时发欢迎语
python3 scripts/welcome.py "action=send|welcome_code=CALLBACK_CODE_xxx|text=欢迎，先认识一下吧"
```

### 场景 5：合规群发（限频 / 留痕 / 可追踪）
```bash
# 创建群发任务
python3 scripts/mass.py "action=create|sender=zhangsan|text=本月限时|external_userids=woAJxxx"

# 查询某员工执行情况
python3 scripts/mass.py "action=get_result|msgid=msgGCxxx|userid=zhangsan"

# 列出指定时间窗口的群发记录
python3 scripts/mass.py "action=list|chat_type=single|start_time=1717200000|end_time=1719792000"
```

### 场景 6：企业朋友圈批量投放
```bash
python3 scripts/moments.py "action=create|text=新课程预告|sender_userids=zhangsan,lisi|image_media_ids=MEDIA_ID_1,MEDIA_ID_2|visible_range=ALL"

# 查询任务结果
python3 scripts/moments.py "action=get_task|jobid=jobxxxxx"

# 查看朋友圈互动
python3 scripts/moments.py "action=comments|moment_id=mom_xxx|userid=zhangsan"
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/contact.py "action=list_followers"` | 列「客户联系」配置员工 | `\|` 分隔 | JSON |
| `python3 scripts/contact.py "action=list_external\|userid=..."` | 列员工的外部客户 | `\|` 分隔 | JSON |
| `python3 scripts/contact.py "action=get\|external_userid=..."` | 查客户详情 | `\|` 分隔 | JSON |
| `python3 scripts/tag.py "action=list"` | 列标签 / 标签组 | `\|` 分隔 | JSON |
| `python3 scripts/tag.py "action=add_group\|group_name=..."` | 新建标签组 | `\|` 分隔 | JSON |
| `python3 scripts/tag.py "action=add_tag\|group_id=...\|tag_name=..."` | 新建标签 | `\|` 分隔 | JSON |
| `python3 scripts/tag.py "action=mark\|userid=...\|external_userid=...\|add=...\|remove=..."` | 打 / 取消标签 | `\|` 分隔 | JSON |
| `python3 scripts/group.py "action=list"` | 列客户群 | `\|` 分隔 | JSON |
| `python3 scripts/group.py "action=stats\|day_begin=...\|day_end=..."` | 客户群统计 | `\|` 分隔 | JSON |
| `python3 scripts/welcome.py "action=add_template\|text=..."` | 新增欢迎语模板 | `\|` 分隔 | JSON |
| `python3 scripts/welcome.py "action=send\|welcome_code=...\|text=..."` | 回调即时发欢迎语 | `\|` 分隔 | JSON |
| `python3 scripts/mass.py "action=create\|sender=...\|text=..."` | 创建客户群发 | `\|` 分隔 | JSON |
| `python3 scripts/moments.py "action=create\|text=...\|sender_userids=..."` | 创建企业朋友圈 | `\|` 分隔 | JSON |

输入约定：键值对用 `|` 分隔，键值用 `=` 分隔；列表字段（如 `external_userids` / `add` / `remove` / `image_media_ids` / `sender_userids`）用 `,` 分隔。

## Scripts

### `scripts/credential.py`
按模块（external_contact / customer_group / moments / app）分别读取 corpsecret，集中处理 `WECOM_CORP_ID` 与 token 缓存目录。

### `scripts/wecom_token.py`
企业微信 access_token 获取与本地缓存，**按 module 隔离**写入 `./.wecom_tokens/<module>.json`，提前 5 分钟刷新。

### `scripts/wecom_http.py`
唯一接触网络的模块。封装：
- 自动注入 `access_token`
- 40014 / 42001 token 失效自动 force_refresh 重试一次
- KV CLI helper：`run_kv_cli(usage, builder)` 解析 `k1=v1|k2=v2`

### `scripts/contact.py`
客户联系：列员工、列外部客户、查客户详情。

### `scripts/tag.py`
客户标签 CRUD + 给客户打 / 取消标签（支持 `add=tagid1,tagid2` 与 `remove=tagid3`）。

### `scripts/group.py`
客户群：列表、详情、按时间窗口拉统计。

### `scripts/welcome.py`
入群欢迎语模板增删查 + `send_welcome_msg`（用客户添加事件回调里的 welcome_code 即时发）。

### `scripts/mass.py`
客户群发（单聊 / 群聊）：create / list / get_result / get_task；可附带 text / image / link / miniprogram。

### `scripts/moments.py`
企业朋友圈：create / get_task / list / customers / send_result / comments；可视范围支持 ALL / PART_VISIBLE。

## API Info

- **Base URL**: `https://qyapi.weixin.qq.com/cgi-bin`
- **Auth**: corpid + 模块化 corpsecret 换 access_token，URL query 参数透传
- **Rate Limits**: 主动调用 600 QPM；客户群发对单个客户每自然月 1 条；朋友圈每个员工每天 3 条
- **Docs**: https://developer.work.weixin.qq.com/document/path/92556

## Troubleshooting

| 现象 | 原因 | 解决 |
|---|---|---|
| `missing credential env: WECOM_CORP_ID` | 没配置 corp_id | `export WECOM_CORP_ID=ww...` |
| `missing credential env: WECOM_SECRET_EXTERNAL_CONTACT` | 没配置对应模块 secret | 在企业微信后台「客户联系 → API」拷贝 |
| `api error: errcode 60011` | 应用没获得对应客户 / 部门权限 | 在「客户联系 → 可调用应用」里勾选成员范围 |
| `api error: errcode 40014` | access_token 过期 | 本 skill 已自动 force_refresh 重试一次；仍失败请检查 secret 是否被重置 |
| `api error: errcode 45033` | 群发命中频率限制 | 检查同一客户上一次群发是否在本月内 |
| `api error: errcode 95005` | 朋友圈每日条数超限 | 调整 sender_userids 或换天再发 |

## References

- 企业微信开发者文档：https://developer.work.weixin.qq.com/
- 客户联系 API：https://developer.work.weixin.qq.com/document/path/92571
- 客户群 API：https://developer.work.weixin.qq.com/document/path/93414
- 企业朋友圈 API：https://developer.work.weixin.qq.com/document/path/95094
- 配套 skill：`wechat-mp`（公众号）、`wechatpay`（支付）

## Notes

- 仅包装**企业微信官方 OpenAPI**；不做爬虫、协议逆向、批量加好友、群发骚扰
- 不打印任何凭据；HTTP 错误会原样返回响应体，请自行屏蔽日志
- 所有 token 仅在 `./.wecom_tokens` 内本地缓存，**不外发**
- 客户原始联系方式（手机号 / 微信号）由企业微信平台保管，本 skill 全程只接触平台分配的 `external_userid`
