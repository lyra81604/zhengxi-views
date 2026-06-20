<div align="center">

# 🔎 郑希观点库 Skill

### 可溯源 · 原文为据 · 接入全市场基金 · 跨 AI 平台

*「让任意 AI 读懂易方达郑希——他说过什么、怎么投、实际买了什么」*

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![类型](https://img.shields.io/badge/类型-Agent%20Skill-black)
![数据](https://img.shields.io/badge/数据-真实公开披露-success)
![基金](https://img.shields.io/badge/覆盖-全市场%202.7万只-orange)
![平台](https://img.shields.io/badge/平台-Claude%20·%20ChatGPT%20·%20Gemini%20·%20Cursor-7c3aed)

[安装](#安装) · [它能做什么](#它能帮你做什么) · [在其他 AI 里用](#在其他-ai-工具里使用) · [目录结构](#目录结构) · [数据来源](#数据来源与真实性) · [边界](#边界)

</div>

---

很多关于"某基金经理怎么看 X"的回答，听起来头头是道，其实是模型凭印象编的——查无此言。这个 skill 解决的就是这个问题：它的根基是**郑希（易方达权益投资管理部副总经理、基金经理）本人留下的原始文本**，任何结论都能追溯到"哪一年、哪一篇、原话是什么"。

它有**三块根基**，都来自公开内容、可溯源：

1. **原文语料**（`references/corpus/`）——2012–2026 年郑希的全部公开观点：定期报告中的投资运作分析（季报 / 中报 / 年报）、基金经理手记、媒体采访报道，外加基金经理简介、在任 / 曾任基金清单。
2. **投资方法**（`references/method.md`）——从上面的语料**蒸馏**出来的方法框架，**每一条都有他本人原话佐证**。它让 skill 在语料没直接谈过的话题上，也能用郑希自己的方法去推演，而不是一句"查无此言"。
3. **真实基金数据**（`references/fund_data/`）——他全部 8 只基金（4 在任 + 4 曾任）的真实数据快照：每季前十大重仓股、净值/业绩/规模/资产配置/任职回报。再加上 `references/all_funds/` 里**全市场约 2.7 万只基金**列表，可按需抓取任意基金做对比与评分。

## 它能帮你做什么

| 你想做的 | 怎么问 | skill 会怎么做 |
|---|---|---|
| 查清他对某方向的真实看法 | `郑希怎么看光通信？他什么时候开始看好的？` | 检索语料，给**带原文出处的引用**，并梳理观点演变 |
| 了解他的投资方法 | `郑希的选股逻辑是什么？为什么偏好低 ROE？` | 用有原话佐证的方法框架作答，可回原文展开 |
| 用他的思路做前瞻判断 | `用郑希的思路看看创新药值不值得关注` | 语料有就引原文；**没有就用他的方法推演**，并在首句声明非他本人观点 |
| 用他的口吻写点评 | `模仿郑希季报的风格写一段 2026 二季度科技展望` | 参照他季报的结构与笔法成文，不捏造数字持仓，声明为风格化模拟 |
| 言行对照 / 查业绩持仓 | `郑希说看好光通信，持仓真印证了吗？业绩如何？` | 把语料里的表态和真实逐季持仓对照，并给净值/收益/回撤等真实数据 |
| 查 / 对比全市场任意基金 | `把郑希和葛兰的中欧医疗比一比` | 全市场 2.7 万只里查代码 → 实时抓取 → 与郑希的基金并列对比 |
| 用郑希框架给基金打分 | `用郑希的标准给招商中证白酒打个分，他会买吗？` | 一条命令备好数据，按六维评分卡给总分/评级/理由（衡量"多像郑希会买的"，非基金优劣） |

## 和"投资框架/方法论"类 skill 的区别

|  | 方法论 / 框架类 skill | 本项目（郑希观点库） |
|---|---|---|
| 根基 | 抽象出的投资"方法"，**不引原文** | 郑希**本人原话语料** + **有原话佐证的方法蒸馏** |
| 朝向 | 前瞻——把方法套到任意标的去选股 | 以**溯源**为根，前瞻与方法都锚定他原话 |
| 产出 | 选股清单 / 评分 | 带出处的引用 / 观点演变 / 有据可查的前瞻与点评 |
| 核心约束 | —— | **不杜撰**：语料有就引原文，没有就标明"按他的方法推演" |

## 它是 Agent Skill 吗？

**是。** 它符合 Agent Skill 规范：根目录有 `SKILL.md`（YAML frontmatter 含 `name` + `description`）+ 渐进式加载的 `references/`、`scripts/` 资源，能通过官方工具校验并打成 `.skill` 包。

- **Claude Code / Claude.ai** 原生支持 Agent Skill，放进技能目录即自动加载。
- 在 **ChatGPT / Gemini / Cursor** 等没有"技能自动加载器"的工具里，用"自定义指令 + 知识文件"的方式复刻，见 [在其他 AI 工具里使用](#在其他-ai-工具里使用)。

## 目录结构

```text
zhengxi-views/
├── SKILL.md
├── README.md
├── references/
│   ├── method.md
│   ├── scorecard.md
│   ├── corpus_index.json
│   ├── corpus/
│   │   ├── 定期报告/
│   │   ├── 基金经理手记/
│   │   ├── 媒体报道/
│   │   ├── 简介.md
│   │   ├── 管理基金_在任.md
│   │   └── 管理基金_曾任.md
│   ├── fund_data/
│   │   ├── _index.md
│   │   ├── 001513_易方达信息产业混合/
│   │   └── …（共 8 只基金，每只含 季度持仓.md 与 净值业绩规模.md）
│   └── all_funds/
│       └── fund_list.json
└── scripts/
    ├── search_corpus.py
    ├── build_index.py
    ├── fetch_fund_data.py
    ├── build_fund_list.py
    ├── fund_lookup.py
    ├── fetch_any_fund.py
    └── score_fund.py
```

## 安装

### Claude Code（原生，推荐）

macOS / Linux：

```bash
mkdir -p "$HOME/.claude/skills/zhengxi-views"
cp -R SKILL.md README.md references scripts "$HOME/.claude/skills/zhengxi-views"/
```

Windows PowerShell：

```powershell
$dst = "$HOME\.claude\skills\zhengxi-views"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse SKILL.md,README.md,references,scripts $dst
```

装好后**完整重启** Claude Code，问一句"郑希怎么看光通信"即可触发。

### 依赖（仅"抓取基金数据 / 评分"需要）

纯语料检索不依赖第三方库；要用 `fetch_*` / `score_fund` 抓全市场数据时，先装：

```bash
pip install -r requirements.txt   # requests / beautifulsoup4 / lxml
```

### 减少每步确认（Claude Code，可选）

skill 会运行 python 脚本。Claude Code 默认每次运行都要确认。想免确认，在 `~/.claude/settings.json` 的 `permissions.allow` 里加 python 放行规则：

```json
{
  "permissions": {
    "allow": ["Bash(python:*)", "Bash(python3:*)"]
  }
}
```

（会放行所有 python 命令，仅建议在个人机器上使用，随时可删。脚本调用本身已设计为单条命令、无 `cd`/重定向，以避免安全确认。）

## 在其他 AI 工具里使用

本项目是 Agent Skill，**Claude 系原生支持**；其他工具靠"指令 + 知识文件"复刻。能用的功能取决于该工具**能否运行 Python 并联网**：

| 功能 | 所需能力 | Claude Code | Cursor | Claude.ai | ChatGPT | Gemini |
|---|---|:---:|:---:|:---:|:---:|:---:|
| 溯源问答 / 方法讲解 / 风格点评 | 读文件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 郑希 8 只基金言行对照（自带快照） | 读文件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 全市场任意基金实时抓取 / 评分 | Python + 联网 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ |

> ⚠️ = 沙箱通常**无外网**，实时抓取多半失败；但可以在本地先用 `fetch_any_fund.py` 把目标基金抓好，再把生成的数据文件一起上传，离线评分照常работает。

**通用思路（任何支持自定义指令 + 文件上传的 AI）**：
- **指令**：把 `SKILL.md` 正文粘进"系统提示 / 自定义指令"。其中"运行脚本的方式"那段是 Claude Code 专属，可删或改为"用代码解释器运行上传的脚本"；务必保留行为约束（溯源、不杜撰、推演与原话分开、语料外首句加粗声明非原话）。
- **知识**：上传 `references/` 全部内容（`method.md`、`scorecard.md`、`corpus/`、`fund_data/`、`all_funds/fund_list.json`）；要跑脚本的再上传 `scripts/`。

### Cursor（IDE，功能最全，接近 Claude Code）

1. 把整个 `zhengxi-views/` 文件夹放进工作区。
2. 新建 `.cursor/rules/zhengxi.mdc`，把 `SKILL.md` 正文粘进去作为 Rule。
3. Cursor 的 Agent 有本机终端，能跑 python + 联网——检索、实时抓取、评分全部可用，用法与 Claude Code 一致。

### ChatGPT（自定义 GPT）

1. 新建一个 GPT（My GPTs → Create）。
2. **Instructions**：粘贴 `SKILL.md` 正文（按上面"通用思路"调整脚本相关措辞）。
3. **Knowledge**：上传 `method.md`、`scorecard.md`、`corpus/`（可打包成 zip）、`fund_data/`、`all_funds/fund_list.json`，以及 `scripts/*.py`。
4. 打开 **Code Interpreter（数据分析）**。
- 可用：溯源问答、方法、风格点评、郑希基金数据，以及对上传数据用脚本检索 / 评分。
- 受限：全市场**实时抓取**（Code Interpreter 无外网）——改为本地先抓好再上传。

### Gemini（Gem / Google AI Studio）

1. 新建一个 Gem。
2. 指令栏粘贴 `SKILL.md` 正文；知识栏上传 `method.md`、`scorecard.md`、`corpus/`、`fund_data/`。
3. 主要支持读类功能（问答 / 方法 / 点评 / 已打包数据对照）；无代码 + 外网，实时抓取与脚本评分请在本地跑好再带结果提问。

### Claude.ai（网页 / 桌面）

- 若你的账号支持上传 Skill，直接上传打包好的 `.skill`；或新建一个 Project，把 `SKILL.md` 与 `references/`、`scripts/` 作为项目知识上传。
- 网页沙箱可能无外网，实时抓取或受限；自带语料与郑希基金数据正常。

## 脚本速查

```text
search_corpus.py "光通信"                  在语料里检索，返回命中段落 + 出处（新→旧）
search_corpus.py "ROE" "弹性" --any        命中任一关键词
fund_lookup.py 中欧医疗                      全市场按名称/代码/类型查基金代码
fetch_any_fund.py 003095                    按需抓取任意基金的持仓/净值/业绩到缓存
score_fund.py 招商中证白酒                   郑希框架评分一键入口（找代码+备数据+算指标）
build_index.py / build_fund_list.py        语料 / 全市场列表更新后重建
```

> 在 Claude Code / Cursor 里，AI 会自己调用这些脚本，你通常不必手动敲。

## 数据来源与真实性

语料、投资方法佐证、基金数据，全部来自郑希及其管理基金的**公开披露内容**——易方达官网的定期报告、基金经理手记、媒体报道，以及天天基金的公开基金数据。均为真实材料、可追溯原文，skill 只检索引用、不编造、不杜撰。

## 边界

研究与学习辅助，**不构成投资建议**，不预测涨跌、不给买卖指令、不承诺收益。引用须忠于原文；最大的禁区是**编造他没说过的话**或**改写原文冒充原话**——拿不准就回到语料，或如实说"未见"。

## License

MIT
