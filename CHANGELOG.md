# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.7] - 2026-06-01

### Added

- cn-geo v0.1.0：中文 AI 搜索（GEO）可见性优化——给定品牌 / 品类 / 阶段，输出在豆包 / Kimi / 文心 / 元宝 / 秘塔等中文 AI 搜索里被引用的行动清单、品牌问答素材、内容覆盖矩阵（本地规则推理，无外部 API）
- cn-tax v0.1.0：中国小微纳税人税务助手——个体 / 个独 / 小规模 / 一般纳税人四种身份下的季度申报清单、税负近似测算、合规风险提醒（本地规则推理，不替代税务师，不自动提交申报）
- icp-domain-cn v0.1.0：中国大陆上线前置流程清单——给定主体 / 域名 / 服务器位置，判断 ICP 备案 + 公安备案 + 域名实名 + 行业前置许可的需求，输出分步指引（本地规则推理，不替代律师 / 备案专员）

## [0.0.6] - 2026-06-01

### Added

- cn-festival-calendar v0.1.0：中国节日 / 节气 / 电商大促 / 监管敏感期内容决策引擎——给定日期或节日，输出 5 大平台（小红书/抖音/快手/B站/公众号）的发布角度、错峰排期、敏感期警告（本地数据，覆盖 2024–2030 年农历对照）

## [0.0.6] - 2026-06-01

### Added

- wechatpay v0.1.0：微信支付 V3 商户接入（JSAPI/Native/H5/APP 下单、查询、关单、退款、回调验签 + AES-GCM 解密、平台证书管理；仅 stdlib + cryptography）
- alipay v0.1.0：支付宝 OpenAPI 商户接入（当面付 / PC / WAP / APP 下单、查询、关单、退款、异步通知 RSA2 验签；不依赖支付宝官方 SDK）
- cn-einvoice v0.1.0：中国电子发票开具（诺诺 / 百望双供应商，普票 / 专票开具、查询、红冲；可被 wechatpay / alipay 复用）

## [0.0.5] - 2026-06-01

### Added

- cn-content-compliance v0.1.0：中国内容合规自检——广告法极限词 + 医疗/食品/化妆品/金融/教培行业红线 + 各主流平台禁用词的本地匹配与改写建议（不构成法律意见）

## [0.0.4] - 2026-06-01

### Added

- kuaishou-ops v0.1.0：快手老铁口播脚本、3 段式分镜、30 分钟直播带货话术（本地模板 + 规则模型，不爬抓不刷量）
- bilibili-ops v0.1.0：B 站 12 分钟三段式长视频脚本、6 章节大纲与时间码、动态/专栏文案与 tag 推荐（本地模板 + 规则模型，不爬抓不刷量）

## [0.0.3] - 2026-06-01

### Added

- xiaohongshu-ops v0.1.0：小红书选题工厂、笔记结构化生成、关键词与 tag 推荐（本地种子库 + 规则模板，不爬抓不刷量）
- douyin-ops v0.1.0：抖音/视频号 60 秒口播脚本、6 镜分镜表、剪映工程 JSON 骨架（本地模板 + 规则模型，不爬抓不刷量）

## [0.0.2] - 2026-06-01

### Added

- wechat-ops v0.1.0：微信公众号 access_token 缓存、图文草稿、自定义菜单、客服文本回复（仅官方开放 API）

## [0.0.1] - 2026-05-31

### Added

- cn-city-picker v0.1.0
- 项目初始化
