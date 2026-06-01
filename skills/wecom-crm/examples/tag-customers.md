# 例：客户分层打标签

## 场景
按客户阶段（高意向 / 待跟进 / 老客户）做分层管理，用「客户标签」组织私域客户。

## 步骤

### 1) 看现有标签
```bash
python3 scripts/tag.py "action=list"
```

### 2) 新增「客户阶段」标签组
```bash
python3 scripts/tag.py "action=add_group|group_name=客户阶段|order=1"
```
输出里会返回新建组的 `group_id`（如 `etGROUP_xxx`）。

### 3) 在该组下加 3 个标签
```bash
python3 scripts/tag.py "action=add_tag|group_id=etGROUP_xxx|tag_name=高意向|tag_order=1"
python3 scripts/tag.py "action=add_tag|group_id=etGROUP_xxx|tag_name=待跟进|tag_order=2"
python3 scripts/tag.py "action=add_tag|group_id=etGROUP_xxx|tag_name=老客户|tag_order=3"
```
拿到 3 个 `tag_id`（如 `etTAG_HIGH` / `etTAG_FU` / `etTAG_OLD`）。

### 4) 给客户打 / 取消标签
```bash
# 升级：把客户从「待跟进」升到「高意向」
python3 scripts/tag.py "action=mark|userid=zhangsan|external_userid=woAJ2Gxxx|add=etTAG_HIGH|remove=etTAG_FU"
```

## 输出（节选）
```json
{"errcode": 0, "errmsg": "ok"}
```

## 提示
- `userid`：企业微信成员；`external_userid`：客户在该成员下的标识，由 `contact.py list_external` 拿到
- 一次 `mark` 可同时 `add` 多个标签（逗号分隔）和 `remove` 多个标签
- 客户不会感知到被打了什么标签
