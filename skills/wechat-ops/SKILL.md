---
name: wechat-ops
description: 微信公众号（订阅号/服务号）日常运营自动化：access_token 缓存、图文草稿与群发、自定义菜单同步、客服文本回复、素材管理。Use when 用户提到公众号、推文、图文消息、菜单配置、客服回复、群发、素材上传、access_token、订阅号、服务号、mp.weixin.qq.com。
---

# 微信公众号运营（wechat-ops）

> 一人公司的内容主阵地。本 skill 把"草稿 → 发布 → 菜单 → 客服回复"这几件高频公众号操作做成 stdlib-only 的脚本，全部走 [微信公众平台官方接口](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)，不爬抓、不刷量、不替你登录他人账号。

## Prerequisites

### 环境变量
```bash
export WECHAT_MP_APP_ID="<wx 开头的 AppID>"           # 必需，公众号后台「设置与开发 → 基本配置」
export WECHAT_MP_APP_SECRET="<32 位 AppSecret>"        # 必需，同上
export WECHAT_MP_TOKEN_CACHE="./.wechat_mp_token.json" # 可选，access_token 本地缓存路径，默认同此值
```

### 账号要求
- 已认证的公众号（订阅号或服务号），未认证账号无法调用群发与自定义菜单
- 在公众平台「设置与开发 → 基本配置」中将本机 / 服务器出口 IP 加入「IP 白名单」
- 群发图文：服务号需「群发接口」权限；订阅号需用「群发接口」或「发表接口」（draft → publish）

### 依赖
仅 stdlib（`urllib.request` / `json` / `os` / `time` / `argparse`）。

### 合规边界（PIPL & 平台规则）
- 仅调用公众平台官方开放 API，不模拟登录、不抓取后台 HTML
- 客服消息仅在用户 48 小时内主动交互过的会话中发送，禁止主动骚扰
- 不存储用户的 OpenID 到 skill 目录之外
- 单日群发次数受公众平台规则限制，本 skill 不绕过

## Quick Start

```bash
# 1. 获取并缓存 access_token
python3 scripts/mp_token.py

# 2. 把一篇 markdown 文章建为草稿
python3 scripts/publish.py "标题|作者|./article.md|./cover.jpg"

# 3. 同步自定义菜单
python3 scripts/menu.py ./references/menu.example.json

# 4. 给最近 48 小时内交互的用户回复一条文本
python3 scripts/reply.py "<openid>|你好，已收到你的咨询"
```

预期输出（节选）：
```json
{"status": "ok", "media_id": "MEDIA_ID", "draft_id": "DRAFT_ID"}
```

## Usage Examples

### 场景 1：把本地 Markdown 文章建成图文草稿
用户输入："把 ./posts/2026-06-01-opc.md 用《一人公司的第一个月》当标题，封面 cover.jpg，建草稿"

执行：
```bash
python3 scripts/publish.py "一人公司的第一个月|opc-skills-cn|./posts/2026-06-01-opc.md|./cover.jpg"
```

### 场景 2：同步自定义菜单
用户输入："把菜单换成：左『最新文章』跳官网，中『加我』跳客服，右『关于』跳介绍页"

执行：
```bash
python3 scripts/menu.py ./references/menu.example.json
```

### 场景 3：客服文本回复（48 小时窗口内）
用户输入："给 oABCD12345 回一句『资料已发邮件』"

执行：
```bash
python3 scripts/reply.py "oABCD12345|资料已发邮件"
```

### 场景 4：检查当前 access_token 是否有效
```bash
python3 scripts/mp_token.py --check
```

## Commands

| 命令 | 说明 | 输入 | 输出 |
|---|---|---|---|
| `python3 scripts/mp_token.py` | 取/刷新 access_token，写入缓存 | 无 | JSON |
| `python3 scripts/mp_token.py --check` | 校验缓存中的 token 是否仍有效 | 无 | JSON |
| `python3 scripts/publish.py "<title>\|<author>\|<md_path>\|<cover_path>"` | 上传封面 → 建图文草稿 | `\|` 分隔字符串 | JSON |
| `python3 scripts/menu.py <menu.json>` | 覆盖式同步自定义菜单 | 菜单 JSON 路径 | JSON |
| `python3 scripts/reply.py "<openid>\|<text>"` | 客服文本回复 | `\|` 分隔字符串 | JSON |

## Scripts

### `scripts/credential.py`
统一从环境变量读取 `WECHAT_MP_APP_ID` / `WECHAT_MP_APP_SECRET` / `WECHAT_MP_TOKEN_CACHE`。禁止硬编码。

### `scripts/mp_token.py`
- **职责**：调用 `cgi-bin/token` 获取 access_token，缓存到 `WECHAT_MP_TOKEN_CACHE`，剩余有效期 < 5 分钟时自动刷新
- **退出码**：0=成功，2=凭证缺失，1=其它失败

### `scripts/publish.py`
- **职责**：上传封面图为永久图片素材 → 建图文草稿（`draft/add`）
- **输入**：`title|author|md_path|cover_path`
- **输出**：`{"status":"ok","media_id":"...","draft_id":"..."}`

### `scripts/menu.py`
- **职责**：覆盖式同步自定义菜单（先 `menu/delete` 再 `menu/create`）
- **输入**：菜单 JSON 文件路径，schema 见 `references/menu.example.json`

### `scripts/reply.py`
- **职责**：发送客服文本消息（`message/custom/send`）
- **输入**：`openid|text`
- **限制**：仅在 48 小时主动交互窗口内有效，错误码 45015 = 超出窗口

## API Info

- **Base URL**：`https://api.weixin.qq.com`
- **Auth**：URL 参数 `access_token=<token>`（由 `token.py` 注入）
- **Rate Limits**：access_token 默认 2000 次/日刷新；群发受公众平台等级限制
- **Docs**：
  - 总览：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
  - 草稿箱：https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
  - 自定义菜单：https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Creating_Custom-Defined_Menu.html
  - 客服消息：https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html

## Troubleshooting

| 现象 | 错误码 | 解决 |
|---|---|---|
| `error: missing credential` | - | 按 Prerequisites 配置 `WECHAT_MP_APP_ID` / `WECHAT_MP_APP_SECRET` |
| `40164 invalid ip ...` | 40164 | 把当前出口 IP 加入公众平台 IP 白名单 |
| `45015 response out of time limit` | 45015 | 超出 48 小时客服窗口，无法主动发送 |
| `40001 invalid credential` | 40001 | AppSecret 错误或被重置；删除缓存重试 |
| `48001 api unauthorized` | 48001 | 当前公众号类型/认证状态没有该接口权限 |

## References

- 公众平台官方接口文档：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
- 错误码总表：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Global_Return_Code.html
- 相关 skill：`wecom-crm`（企业微信 SCRM）、`xiaohongshu-ops`、`douyin-ops`

## Notes

- 本 skill **仅调用公众平台官方 API**，不包含任何爬虫、协议逆向、批量加好友、群发骚扰逻辑
- access_token 仅缓存到本机由 `WECHAT_MP_TOKEN_CACHE` 指定的文件，建议加入 `.gitignore`
- 已知限制：
  - 不支持视频号（视频号有独立 API，归 `douyin-ops` 视频号子模块或后续独立 skill）
  - 不实现一键群发：群发涉及触达大量用户，需在公众平台后台手工二次确认
