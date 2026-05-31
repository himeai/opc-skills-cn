## 提交清单

- [ ] `skills/<name>/SKILL.md` 存在且 frontmatter 合规
- [ ] `skills/<name>/scripts/credential.py` 存在
- [ ] 至少 1 个业务脚本，且 `python3 scripts/xxx.py --help` 可运行
- [ ] `skill-logos/<name>.svg` 存在（24x24 像素风）
- [ ] `skills.json` 已追加条目，`color` 与 logo 主色一致
- [ ] `.claude-plugin/marketplace.json` 已追加条目
- [ ] `README.md` Skills 表格已更新（含 logo / 状态）
- [ ] `CHANGELOG.md` 已追加 `### Added` 条目
- [ ] 至少 1 个 `examples/*.md`
- [ ] 凭证全部走环境变量，无硬编码
- [ ] 不包含爬虫 / 群发 / 协议逆向逻辑
- [ ] 第 6 节所有校验命令通过

## 变更说明

请说明本次 PR 的主要变更。

## 验证结果

请粘贴本地校验命令与输出。
