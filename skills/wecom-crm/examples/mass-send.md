# 例：合规客户群发（每月限频）

## 场景
本月最后 3 天给「高意向」客户发一条限时优惠提醒。受企业微信平台规则约束：
**每个客户每自然月最多收到 1 条主动群发**。本 skill 只负责把内容投出去，频率自查由你的业务系统保证。

## 步骤

### 1) 拉「高意向」客户的 external_userid 列表
应用层根据上月或本月已发记录过滤掉本月已经触达过的客户：
```bash
python3 scripts/mass.py "action=list|chat_type=single|start_time=1716998400|end_time=1719676800"
```
拿到本月已触达客户后做差集，得到本次允许触达的 `external_userids`。

### 2) 创建群发任务
```bash
python3 scripts/mass.py "action=create|sender=zhangsan|chat_type=single|text=本月最后 3 天，老客户专属 8 折|external_userids=woAJ2Gxxx,woAJ2Gyyy,woAJ2Gzzz|allow_select=0"
```

### 3) 创建后会返回 `msgid`，跟踪发送结果
```bash
# 该员工对所有客户的执行明细
python3 scripts/mass.py "action=get_result|msgid=msgGCxxx|userid=zhangsan"

# 该群发任务下所有 sender 的概览
python3 scripts/mass.py "action=get_task|msgid=msgGCxxx"
```

## 输出（节选）
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "fail_list": [],
  "msgid": "msgGC123abc"
}
```

## 关键约束
- **频率**：同一客户每自然月只能收到 1 条主动群发（命中会返回 `errcode=45033`）
- **附件**：可同时携带 `text` + `image_media_id` + `link_url` + `miniprogram_appid`
- **chat_type=group** 时为「群主名义群发到客户群」，无需 `external_userids`
- **allow_select=1** 时员工可在企业微信侧手动确认每个客户后再发；`=0` 直接由系统投递
