<div align="center">

# 🔎 基金经理 · 郑希观点库 Skill

### 可溯源 · 原文为据 · 接入全市场基金 · 跨 AI 平台

*「查观点 · 学方法 · 做前瞻 · 仿口吻写点评 · 言行对照 · 全市场基金对比与评分 —— 让任意 AI 读懂易方达郑希」*

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![类型](https://img.shields.io/badge/类型-Agent%20Skill-black)
![数据](https://img.shields.io/badge/数据-真实公开披露-success)
![基金](https://img.shields.io/badge/覆盖-全市场%202.7万只-orange)
![平台](https://img.shields.io/badge/平台-Claude%20·%20WorkBuddy%20·%20ChatGPT%20·%20Gemini%20·%20Cursor-7c3aed)

[安装](#install) · [它能做什么](#features) · [在其他 AI 里用](#other-ai) · [目录结构](#structure) · [数据来源](#sources) · [边界](#limits)

</div>

---

很多关于"某基金经理怎么看 X"的回答，听起来头头是道，其实是模型凭印象编的——查无此言。这个 skill 解决的就是这个问题：它的根基是**郑希（易方达权益投资管理部副总经理、基金经理）本人留下的原始文本**，任何结论都能追溯到"哪一年、哪一篇、原话是什么"。

它有**三块根基**，都来自公开内容、可溯源：

- 📚 **原文语料**（`references/corpus/`）——2012–2026 年郑希的全部公开观点：定期报告中的投资运作分析（季报 / 中报 / 年报）、基金经理手记、媒体采访报道，外加基金经理简介、在任 / 曾任基金清单。
- 🧭 **投资方法**（`references/method.md`）——从上面的语料**蒸馏**出来的方法框架，**每一条都有他本人原话佐证**。它让 skill 在语料没直接谈过的话题上，也能用郑希自己的方法去推演，而不是一句"查无此言"。
- 📊 **真实基金数据**（`references/fund_data/`）——他全部 8 只基金（4 在任 + 4 曾任）的真实数据快照：每季前十大重仓股、净值/业绩/规模/资产配置/任职回报。再加上 `references/all_funds/` 里**全市场约 2.7 万只基金**列表，可按需抓取任意基金做对比与评分。

**⚠️ 仅供研究与学习辅助，不构成投资建议。**

<a id="features"></a>
## 🎯 它能帮你做什么

| 你想做的 | 怎么问 | skill 会怎么做 |
|---|---|---|
| 查清他对某方向的真实看法 | `郑希怎么看光通信？他什么时候开始看好的？` | 检索语料，给**带原文出处的引用**，并梳理观点演变 |
| 了解他的投资方法 | `郑希的选股逻辑是什么？为什么偏好低 ROE？` | 用有原话佐证的方法框架作答，可回原文展开 |
| 用他的思路做前瞻判断 | `用郑希的思路看看创新药值不值得关注` | 语料有就引原文；**没有就用他的方法推演**，并在首句声明非他本人观点 |
| 用他的口吻写点评 | `模仿郑希季报的风格写一段 2026 二季度科技展望` | 参照他季报的结构与笔法成文，不捏造数字持仓，声明为风格化模拟 |
| 言行对照 / 查业绩持仓 | `郑希说看好光通信，持仓真印证了吗？业绩如何？` | 把语料里的表态和真实逐季持仓对照，并给净值/收益/回撤等真实数据 |
| 查 / 对比全市场任意基金 | `把郑希和葛兰的中欧医疗比一比` | 全市场 2.7 万只里查代码 → 实时抓取 → 与郑希的基金并列对比 |
| 用郑希框架给基金打分 | `用郑希的标准给招商中证白酒打个分，他会买吗？` | 一条命令备好数据，按六维评分卡给总分/评级/理由（衡量"多像郑希会买的"，非基金优劣） |

## 💬 示例 · 看看它怎么答

下面是 skill 的**真实输出**（稍作精简）。

<details>
<summary><b>① 溯源问答 —— “郑希怎么看光通信？什么时候开始看好的？”</b></summary>

<br>

> 他在 **2026 年 6 月接受中国证券报采访**时把逻辑讲得很清楚：
>
> > “全球 AI 资本开支已经来到万亿美元级别。AI 产业链中，数据传输是重要一环，而光通信则是远距离传输的关键路径。叠加我国在光通信领域的全球比较优势，未来光通信市场规模有望进一步提升。”
>
> 时间点上，他说对“光”的重仓**可追溯到 2025 年二季度**。对照他管理的 **易方达信息产业（001513）持仓**：2025Q2 起，中际旭创、新易盛、源杰科技、光库科技等光通信标的确实集体进入前十大——**言行一致**。

</details>

<details>
<summary><b>② 语料里没谈过的方向 —— “用郑希的思路看看创新药？”</b></summary>

<br>

> **郑希没有公开谈过创新药这个方向，下面是按他一贯的投资方法做的推演，不代表他本人的观点。**
>
> 在他全部公开材料里，“创新药”基本只是季报复盘里“顺带提一句”的角色，从没专门展开。所以把他的方法搬过来看：
> - **第 1 关·有没有“供给端创造的需求”**：创新药靠新靶点/新疗法创造原本不存在的需求，属于他偏爱的“科技型通胀”，这一关最对味；
> - **第 2 关·中国比较优势在哪**：原始创新策源地在海外，中国更占优的是 CXO / 出海 BD 这类“卖水人”环节；
> - **第 3 关·低 ROE 弹性**：未盈利 Biotech 是典型“预先研发型低 ROE”，符合他的偏好；但**流动性**这关会筛掉一批日成交清淡的小票。
>
> *（涉及具体公司/估值标“需核实”；非投资建议。）*

</details>

<details>
<summary><b>③ 郑希框架评分 —— “用郑希的标准给招商中证白酒打个分，他会买吗？”</b></summary>

<br>

> # 用郑希框架给【招商中证白酒指数（012414）】打分：**21 / 100 · 不契合**
>
> 一句话：这是一只合格的行业指数工具，但几乎不像“郑希会买的基金”。**低分 ≠ 差基金**，只是风格和他几乎相反。
>
> | 维度 | 得分 | 一句话依据 |
> |---|---|---|
> | 景气方向 / 通胀属性 | 4 / 25 | 前十大清一色高端白酒，当前处于去库存**下行周期**，是“被压价”而非“在涨价” |
> | ROE 低位弹性 | 6 / 20 | 全是 ROE 长期高位的白酒白马，非他要的“低位待修复” |
> | 全球视野 / 中国比较优势 | 2 / 15 | 纯内需消费，与全球技术周期无关 |
> | 流动性 | 7 / 10 | 重仓全是流动性最好的大盘龙头（唯一亮点） |
> | 集中度与周期拼接 | 2 / 15 | 集中度 85.8% 但**被动躺平**，近 5 季换手代理仅 ~5%，与他“周期拼接/高换手”相反 |
> | 业绩与回撤印证 | 0 / 15 | 近 1 年 −23.9%、最大回撤 −63.2%，大幅跑输 |
>
> **他会买吗？几乎不会**——一只被动锁定单一传统行业的指数基金，和他“自上而下找通胀、偏科技成长、买低 ROE 弹性、动态周期拼接”的方法全对不上。

</details>

<details>
<summary><b>④ 全市场对比 —— “把郑希的信息产业和葛兰的中欧医疗比一比”</b></summary>

<br>

> | | 郑希 · 信息产业 001513 | 葛兰 · 中欧医疗 003095 |
> |---|---|---|
> | 赛道 | 科技（光通信·算力·半导体） | 医药（CXO·创新药） |
> | 风格 | 自上而下、产业链轮动、**高换手** | 核心资产**长持**、低换手 |
> | 近 1 年 | **+290%** | −5.4% |
> | 最大回撤 | −46.3% | −63.9% |
>
> 一句话：两人都是高仓位单赛道选手，但郑希靠“踩对当下景气 + 动态轮动”把弹性变成收益，葛兰靠“长拿核心资产”在医药下行期完整承接了更深回撤。
> *（数据为公开季度快照，截至 2026-06；非投资建议。）*

</details>

## ⚖️ 和"投资框架/方法论"类 skill 的区别

|  | 方法论 / 框架类 skill | 本项目（郑希观点库） |
|---|---|---|
| 根基 | 抽象出的投资"方法"，**不引原文** | 郑希**本人原话语料** + **有原话佐证的方法蒸馏** |
| 朝向 | 前瞻——把方法套到任意标的去选股 | 以**溯源**为根，前瞻与方法都锚定他原话 |
| 产出 | 选股清单 / 评分 | 带出处的引用 / 观点演变 / 有据可查的前瞻与点评 |
| 核心约束 | —— | **不杜撰**：语料有就引原文，没有就标明"按他的方法推演" |

## 🧩 它是 Agent Skill 吗？

**是。** 它符合 Agent Skill 规范：根目录有 `SKILL.md`（YAML frontmatter 含 `name` + `description`）+ 渐进式加载的 `references/`、`scripts/` 资源，能通过官方工具校验并打成 `.skill` 包。

- **Claude Code / Claude.ai** 原生支持 Agent Skill，放进技能目录即自动加载。
- **腾讯 WorkBuddy** 用 `skill.yml` 清单组织 Skill，本仓库已附一份，放进它的 `skills/` 目录即可（已实测可用）。
- 在 **ChatGPT / Gemini / Cursor** 等没有"技能自动加载器"的工具里，用"自定义指令 + 知识文件"的方式复刻，见 [在其他 AI 工具里使用](#other-ai)。

<a id="structure"></a>
## 🗂️ 目录结构

```text
zhengxi-views/
├── SKILL.md
├── skill.yml                       # 腾讯 WorkBuddy 清单（Claude 用法可忽略）
├── WORKBUDDY部署.md
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

<a id="install"></a>
## ⚙️ 安装

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

<a id="other-ai"></a>
## 🌐 在其他 AI 工具里使用

本项目是 Agent Skill，**Claude 系原生支持**；其他工具靠"指令 + 知识文件"复刻。能用的功能取决于该工具**能否运行 Python 并联网**：

| 功能 | 所需能力 | Claude Code | WorkBuddy | Cursor | Claude.ai | ChatGPT | Gemini |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 溯源问答 / 方法讲解 / 风格点评 | 读文件 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 郑希 8 只基金言行对照（自带快照） | 读文件 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 全市场任意基金实时抓取 / 评分 | Python + 联网 | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ❌ |

> 腾讯 **WorkBuddy** 本地运行、能跑脚本联网，因此可用**全部功能**（含实时抓取）；它用 `skill.yml` 作清单，本仓库已附一份，详见 [腾讯 WorkBuddy](#腾讯-workbuddy)。

> ⚠️ = 沙箱通常**无外网**，实时抓取多半失败；但可以在本地先用 `fetch_any_fund.py` 把目标基金抓好，再把生成的数据文件一起上传，离线评分照常进行。

**通用思路（任何支持自定义指令 + 文件上传的 AI）**：
- **指令**：把 `SKILL.md` 正文粘进"系统提示 / 自定义指令"。其中"运行脚本的方式"那段是 Claude Code 专属，可删或改为"用代码解释器运行上传的脚本"；务必保留行为约束（溯源、不杜撰、推演与原话分开、语料外首句加粗声明非原话）。
- **知识**：上传 `references/` 全部内容（`method.md`、`scorecard.md`、`corpus/`、`fund_data/`、`all_funds/fund_list.json`）；要跑脚本的再上传 `scripts/`。

### 腾讯 WorkBuddy

WorkBuddy 是本地运行的 AI 工作台，自定义 Skill 约定为 **`skill.yml` 清单 + 实现文件（scripts）+ README**。本仓库已附 `skill.yml`，可直接用：

1. 把整个文件夹放进 WorkBuddy 的 **`skills/` 技能目录**，按 `skill.yml` 导入启用（**已实测可用**）。
2. 先 `pip install -r requirements.txt` 装好脚本依赖；因本地运行，**实时抓取/评分等全部功能均可用**。
3. 触发词示例："郑希怎么看光通信""用郑希的标准给招商中证白酒打个分"。

> `skill.yml` 字段按通用约定编写；若 WorkBuddy 提示字段不符，对照其 schema 微调即可（行为逻辑都在 `SKILL.md`）。完整步骤与备选方案见 [`WORKBUDDY部署.md`](WORKBUDDY部署.md)。

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

## 🛠️ 脚本速查

```text
search_corpus.py "光通信"                  在语料里检索，返回命中段落 + 出处（新→旧）
search_corpus.py "ROE" "弹性" --any        命中任一关键词
fund_lookup.py 中欧医疗                      全市场按名称/代码/类型查基金代码
fetch_any_fund.py 003095                    按需抓取任意基金的持仓/净值/业绩到缓存
score_fund.py 招商中证白酒                   郑希框架评分一键入口（找代码+备数据+算指标）
build_index.py / build_fund_list.py        语料 / 全市场列表更新后重建
```

> 在 Claude Code / Cursor 里，AI 会自己调用这些脚本，你通常不必手动敲。

<a id="sources"></a>
## ✅ 数据来源与真实性

语料、投资方法佐证、基金数据，全部来自郑希及其管理基金的**公开披露内容**——易方达官网的定期报告、基金经理手记、媒体报道，以及天天基金的公开基金数据。均为真实材料、可追溯原文，skill 只检索引用、不编造、不杜撰。

<a id="limits"></a>
## 🚧 边界

研究与学习辅助，**不构成投资建议**，不预测涨跌、不给买卖指令、不承诺收益。引用须忠于原文；最大的禁区是**编造他没说过的话**或**改写原文冒充原话**——拿不准就回到语料，或如实说"未见"。

## 📄 License

MIT
