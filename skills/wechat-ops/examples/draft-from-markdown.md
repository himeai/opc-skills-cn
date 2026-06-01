# 示例：把本地 Markdown 建为公众号图文草稿

## 前置

```bash
export WECHAT_MP_APP_ID="wx0000000000000000"
export WECHAT_MP_APP_SECRET="********************************"
```

> 把本机出口 IP 加入公众平台「设置与开发 → 基本配置 → IP 白名单」。

## 步骤

1. 准备本地文件：
   - `./posts/2026-06-01-opc.md`：正文 Markdown（仅支持 `#` / `##` / `-` / 段落）
   - `./posts/cover.jpg`：封面图（建议 900×500 以上，<= 10 MB）

2. 取/刷新 access_token：
```bash
python3 scripts/mp_token.py
```

3. 上传封面 + 建草稿：
```bash
python3 scripts/publish.py "一人公司的第一个月|opc-skills-cn|./posts/2026-06-01-opc.md|./posts/cover.jpg"
```

4. 输出示例：
```json
{"status":"ok","media_id":"DM_MEDIA_ID","draft_id":"DRAFT_MEDIA_ID"}
```

5. 打开公众平台后台 → 草稿箱 → 二次校对 → 手动点击群发。

> 本 skill 故意不提供"一键群发"：群发会触达全体粉丝，必须由人在公众平台后台二次确认。
