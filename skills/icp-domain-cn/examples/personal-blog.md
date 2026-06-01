# 例：个人博客 + .cn + 阿里云境内服务器

## 输入

```bash
python3 scripts/check.py "subject=individual|domain=myblog.cn|hosting=cn_mainland"
```

## 输出（节选）

```json
{
  "subject": "individual",
  "domain": "myblog.cn",
  "domain_suffix": "cn",
  "hosting": "cn_mainland",
  "decisions": {
    "icp_filing_required": true,
    "psb_filing_required": true,
    "domain_real_name_required": true
  },
  "advice": [
    "主体类型：个人。个人备案站点严禁经营性内容（含电商、付费内容、广告联盟），违规将被注销备案",
    "服务器：境内服务器（阿里云 / 腾讯云 / 华为云 / 火山引擎等）。优点：国内访问速度快, 部分企业 / 教育 / 政务必须境内；缺点：首次备案 20 工作日左右, 网站内容需符合大陆法律",
    "域名后缀 .cn：.cn 域名要求实名认证；接入境内服务器必须 ICP 备案",
    "→ 必须完成 ICP 备案；详见 steps.py filing=icp",
    "→ 必须完成公安备案（拿到 ICP 备案号后 30 天内）；详见 steps.py filing=psb",
    "→ 域名必须实名认证（注册商后台办理）",
    "→ 个人主体备案站点严禁经营性内容（电商 / 付费内容 / 广告联盟）"
  ]
}
```

## 怎么用

1. 看 `decisions` 决定要不要做备案
2. 跑 `steps.py filing=icp` / `steps.py filing=psb` 拿分步指引
3. 内容上线后用 `cn-content-compliance` 过一次合规
4. 收款 + 开票场景用 `wechatpay` / `alipay` / `cn-einvoice` 串起来
