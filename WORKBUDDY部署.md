# 在腾讯 WorkBuddy 上部署

本副本在原 `zhengxi-views` Skill 的基础上，补了一个 WorkBuddy 清单文件 `skill.yml`，用于在腾讯 WorkBuddy 里部署。

> ⚠️ 字段说明：腾讯官方目前**没有完整公开 `skill.yml` 的字段规范**（它更鼓励"描述需求→自动生成 skill 文件"的交互式创建）。`skill.yml` 里的键名是按通用约定写的尽力版本，导入后如提示字段不符，照 WorkBuddy 的实际 schema 微调即可——**行为逻辑全在 `SKILL.md`，不受影响**。

## 为什么 WorkBuddy 适合跑这个 Skill

WorkBuddy 是**本地运行**的 AI 工作台，能跑脚本、能联网。所以不像 ChatGPT/Gemini 的云端沙箱只能用"自带数据"，它**理论上能跑全部功能**，包括：
- ✅ 溯源问答 / 讲方法 / 风格点评（读语料）
- ✅ 郑希 8 只基金言行对照（读自带快照）
- ✅ **全市场任意基金实时抓取 / 评分**（本地 python + 联网，这是云端工具做不到的）

## 准备：装好脚本依赖

抓取/评分类脚本需要第三方库，先在本机装：

```bash
pip install -r requirements.txt   # requests / beautifulsoup4 / lxml
```

（纯语料检索不需要联网和第三方库。）

## 方式一：作为自定义 Skill 放入 WorkBuddy（推荐）

WorkBuddy 的自定义 Skill 约定是：**Markdown/YAML 清单 + 实现文件（scripts）+ README**，放进它的 `skills/` 目录。本副本已按此结构组织：

```
zhengxi-views/
├── skill.yml        # WorkBuddy 清单（本副本新增）
├── SKILL.md         # 行为指令（WorkBuddy 以此为系统指令）
├── README.md        # 文档
├── references/      # 知识：语料 / 方法 / 评分卡 / 基金数据 / 全市场列表
└── scripts/         # 实现：检索 / 抓取 / 评分脚本
```

步骤：
1. 把整个文件夹放进 WorkBuddy 的 **`skills/` 技能目录**（具体路径见 WorkBuddy「创建自定义 Skill」文档）。
2. 在 WorkBuddy 里**启用/导入**该 Skill；如它读取的是 `skill.yml`，确认字段与其 schema 一致（不一致就按提示改键名）。
3. 用触发词测试，例如："郑希怎么看光通信""用郑希的标准给招商中证白酒打个分"。

## 方式二：用 WorkBuddy 的"创建 Skill"流程包装（最稳，绕开格式差异）

如果方式一的 `skill.yml` 字段对不上 WorkBuddy 的 schema，用它自带的交互式创建：
1. 在 WorkBuddy 里发起"创建自定义 Skill"，把 **`SKILL.md` 正文**作为这个 Skill 的指令/描述贴进去（其中"运行脚本的方式"那段是 Claude Code 专属，可改为"运行本 Skill 目录下 scripts/ 里的对应 python 脚本"）。
2. 把 `references/` 与 `scripts/` 作为该 Skill 的资源/实现文件一起提供。
3. 让 WorkBuddy 生成它自己的 `skill.yml`，安装、测试。

这样由 WorkBuddy 自己产出符合其规范的清单，我们只提供"指令 + 知识 + 脚本"，最省心。

## 调用脚本的注意点（沿用原则）

让 WorkBuddy 的 agent 调脚本时，**用单条命令、脚本绝对路径，不要 `cd … &&`、不要管道/重定向**——脚本内部已用绝对路径定位数据、并自带输出上限。示例：

```
python "<本skill目录>/scripts/score_fund.py" 招商中证白酒
```

## 行为约束（务必保留）

无论哪种方式，`SKILL.md` 里这些底线都要带上：可溯源、不杜撰、原话与推演分开、语料外话题首句加粗声明非郑希本人观点、不构成投资建议。
