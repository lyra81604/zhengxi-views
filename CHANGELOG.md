# 更新日志

本项目遵循语义化版本（SemVer）。

## [1.1.0] - 2026-06

### 新增
- 腾讯 **WorkBuddy** 部署支持：新增 `skill.yml` 清单与 `WORKBUDDY部署.md` 指南（方式一：放入 `skills/` 目录导入，已实测可用）。本地运行可用全部功能（含实时抓取/评分）。
- README 增加 WorkBuddy 平台徽章、兼容性表格列与部署小节。

## [1.0.0] - 2026-06

首个公开版本。

### 语料与方法
- 收录郑希 2012–2026 年全部公开观点原文：定期报告投资运作分析、基金经理手记、媒体采访，以及简介、在任/曾任基金清单。
- `references/method.md`：从语料蒸馏的投资方法框架，每条配本人原话佐证。
- `references/scorecard.md`：郑希框架六维评分卡。

### 基金数据
- `references/fund_data/`：郑希全部 8 只基金（4 在任 + 4 曾任）的真实数据快照（逐季前十大持仓、净值/业绩/规模/资产配置/任职回报）。
- `references/all_funds/`：全市场约 2.7 万只基金列表，支持按需抓取任意基金做查询、对比与评分。

### 脚本
- `search_corpus.py` 语料检索、`fund_lookup.py` 基金查找、`fetch_fund_data.py` / `fetch_any_fund.py` 数据抓取、`score_fund.py` 评分一键入口、`build_index.py` / `build_fund_list.py` 重建索引。

### 行为约束
- 一切结论可溯源、不杜撰；原话与推演分开；语料外话题首句加粗声明非本人观点。
- 脚本调用设计为单条命令、无 `cd`/重定向，避免权限确认弹窗。
