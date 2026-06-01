# 例：从 JD → 候选人评分 → 面试题 全链路

## 场景
你刚开了一个「中级后端工程师」岗位，5 分钟内要：
1. 出一份能直接挂到内推群的 JD
2. 把 3 个简历快速筛一筛
3. 给一面面试官出一份结构化面经

## 步骤

### 1) 生成 JD
```bash
python3 scripts/jd.py "role=后端工程师|family=工程|seniority=中级|primary_stack=Go|product_line=客户成功平台|industry=SaaS|location=远程|salary=25-40k*15|tone=活泼|hr_email=hr@example.com|company_short_desc=面向 OPC 的 AI Agent 工具团队"
```
拿输出里的 `must_have` 列表（前 6 项）做后续筛选关键词：
```
Go, 微服务, 高并发, K8s, 单元测试, owner
```

### 2) 给 3 位候选人打分
```bash
python3 scripts/score.py '{
  "must_have_keywords": ["Go", "微服务", "高并发", "K8s"],
  "candidate": {
    "skills": ["Go", "微服务", "K8s"],
    "years": 4,
    "target_band": "中级",
    "industry": "SaaS",
    "target_industry": "SaaS",
    "tenures_years": [2.5, 3.1, 1.8],
    "highlights": ["开源贡献者", "技术博客", "曾带 3 人小组"]
  }
}'
```
预期返回 `total_score ~ 85+`，`verdict: 强推`，加急约面。

对另一位"履历跳来跳去"的候选人：
```bash
python3 scripts/score.py '{
  "must_have_keywords": ["Go", "微服务", "高并发", "K8s"],
  "candidate": {
    "skills": ["Go"],
    "years": 4,
    "target_band": "中级",
    "tenures_years": [0.6, 0.8, 0.7, 0.9],
    "highlights": []
  }
}'
```
预期返回 `red_flags` 里命中 `frequent_jobhop`，`verdict` 通常会是「电话沟通」或「暂不合适」。

### 3) 一面面试官的题包
```bash
python3 scripts/interview.py "family=工程|dimensions=技术深度,项目经验,解决问题|primary_stack=Go|product_line=客户成功平台"
```
直接把输出的 `dimensions[].questions` 贴到 Notion 面评模板里，每题留一行写候选人回答 + STAR 评分。

## 提示
- 评分是**初筛信号**，不要拿它当最终判定；总分 70+ 进一面，50-70 电话 30 分钟看动机
- 面试题里的 `look_for` 是给面试官**自己看**的，不要在面试中念给候选人听
- 红旗（red_flags）只是提示，不要因此拒绝候选人，要在面试中带着追问验证
