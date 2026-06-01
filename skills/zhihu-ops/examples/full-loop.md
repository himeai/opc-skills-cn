# 例：从选题 → 长回答 → tag 全链路

## 场景
你今天在 AI / 大模型领域要更一篇知乎长回答，目标是被算法推荐到时间线。

## 步骤

### 1) 用 topic.py 选题
```bash
python3 scripts/topic.py "domain=AI / 大模型|target=AI Agent|year=2026|n=5|scene=客服"
```
从返回的 `topics` 里挑一条最贴合你专长的，比如「把 AI Agent 落地到客服的 5 个真实坑」。

### 2) 用 answer.py 出骨架
```bash
python3 scripts/answer.py "question=把 AI Agent 落地到客服场景有哪些真实的坑？|style=干货|industry=AI|years=3|column_name=AI Agent 周记"
```
拿到 `outline` 后逐段填：
- TLDR 步骤总览：把 5 个坑用编号一句话列出来
- Step 1-5：每个坑配一段真实场景 + 一段你的解决方法
- 工具/模板：把你用的 prompt 模板或评估表直接放出来
- 常见问题：3-5 个 Q&A
- 结尾：用一个 closing_candidates 收束

### 3) 用 tag.py 推 tag
```bash
python3 scripts/tag.py "domain=AI / 大模型|keywords=AI Agent,客服,Prompt,LLM,SaaS|max=5"
```
预期返回：
```json
{
  "tags": ["AI Agent", "Prompt Engineering", "大语言模型", "人工智能", "SaaS"],
  "dropped": ["客服"]
}
```
其中 `客服` 没有匹配 canonical tag，可以人工挂个 "客服" 自由标签，或者把它写进正文小标题。

## 提示
- 同一篇答案里 `style` 不要混；选 `干货` 就一干到底，避免半干货半经验
- 钩子（hook_candidates）选一个就好，不要把 3 个全用上
- 真正决定回答能否破圈的是**第一屏的信息密度** + **可证伪的细节**，骨架只是脚手架
