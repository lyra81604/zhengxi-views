# -*- coding: utf-8 -*-
"""一键：给任意基金准备好"郑希框架评分"所需的全部材料。
自动完成：解析代码（名称→代码）→ 备齐数据（郑希精编快照/缓存/实时抓取）→ 计算机械指标
→ 打印一份完整证据档案。随后请按 references/scorecard.md 逐维打分。

用法:
  python scripts/score_fund.py 005827
  python scripts/score_fund.py 中欧医疗健康
  python scripts/score_fund.py 001513          # 郑希自己的基金，用精编快照

设计目的：把"查找→抓取→读多个文件"合并成一条命令，少点几次确认，输出即可直接打分。
研究与学习辅助，非投资建议。
"""
import os, sys, json, glob
import fetch_fund_data as F
import fetch_any_fund as A

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZX_DIR = os.path.join(ROOT, "references", "fund_data")          # 郑希精编快照
CACHE = os.path.join(ROOT, "references", "fund_data_cache")     # 任意基金缓存
LIST = os.path.join(ROOT, "references", "all_funds", "fund_list.json")


def resolve(arg):
    """把代码或名称解析成 (code, name, type)。名称多命中时取最短名（通常是母基金/主代码）。"""
    if not os.path.exists(LIST):
        return arg, arg, ""
    funds = json.load(open(LIST, encoding="utf-8"))["funds"]
    if arg.isdigit():
        for f in funds:
            if f["code"] == arg:
                return f["code"], f["name"], f["type"]
        return arg, arg, ""
    cands = [f for f in funds if arg in f["name"] or arg.upper() in f["abbr"] or arg.upper() in f["pinyin"]]
    if not cands:
        return None, arg, ""
    cands.sort(key=lambda f: len(f["name"]))
    return cands[0]["code"], cands[0]["name"], cands[0]["type"]


def find_data_dir(code):
    """优先郑希精编快照，其次缓存。返回目录或 None。"""
    for base in (ZX_DIR, CACHE):
        hit = glob.glob(os.path.join(base, f"{code}_*"))
        if hit and os.path.exists(os.path.join(hit[0], "季度持仓.json")):
            return hit[0], (base == ZX_DIR)
    return None, False


def turnover_proxy(quarters):
    """季度间换手代理：相邻季度前十大重叠越低→换手越高。返回 平均(1-重叠率)%。"""
    qs = sorted(quarters, key=lambda q: (q["year"], q["quarter"]))
    qs = qs[-5:]  # 近5个季度
    diffs = []
    for a, b in zip(qs, qs[1:]):
        sa = {h["股票代码"] for h in a["holdings"]}
        sb = {h["股票代码"] for h in b["holdings"]}
        if sa and sb:
            overlap = len(sa & sb) / max(len(sb), 1)
            diffs.append(1 - overlap)
    return round(sum(diffs) / len(diffs) * 100, 1) if diffs else None


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/score_fund.py <基金代码或名称>")
        return
    arg = sys.argv[1]
    code, name, ftype = resolve(arg)
    if not code:
        print(f"没找到“{arg}”。试试 python scripts/fund_lookup.py {arg}")
        return

    d, is_zx = find_data_dir(code)
    if not d:
        print(f"本地无 {code} 数据，实时抓取中 ...")
        A.fetch_one(code)
        d, is_zx = find_data_dir(code)
    if not d:
        print(f"抓取失败，无法评分 {code} {name}")
        return

    quarters = json.load(open(os.path.join(d, "季度持仓.json"), encoding="utf-8"))
    pzp = os.path.join(d, "净值业绩规模.json")
    pz = json.load(open(pzp, encoding="utf-8")) if os.path.exists(pzp) else {}

    print("=" * 70)
    print(f"郑希框架评分 · 证据档案")
    print(f"基金：{name}（{code}）  类型：{ftype}")
    print(f"数据来源：{'郑希精编快照' if is_zx else '全市场实时缓存'}（{os.path.relpath(d, ROOT)}）")
    print("=" * 70)

    # 最新一季前十大
    if quarters:
        latest = sorted(quarters, key=lambda q: (q["year"], q["quarter"]))[-1]
        conc = sum(float(h["占净值比"].rstrip("%")) for h in latest["holdings"] if h["占净值比"].rstrip("%").replace(".", "").isdigit())
        print(f"\n【最新前十大持仓】{latest['year']}年第{latest['quarter']}季度  (前十大合计约 {round(conc,1)}% 净值)")
        for i, h in enumerate(latest["holdings"], 1):
            print(f"  {i:2d}. {h['股票名称']}（{h['股票代码']}） {h['占净值比']}")
        print(f"\n【集中度】前十大合计 ≈ {round(conc,1)}%（越高越集中）")
        tp = turnover_proxy(quarters)
        print(f"【换手代理】近5季相邻重叠外的平均换手 ≈ {tp}%（越高=调仓越频繁=越像周期拼接）")
        print(f"【披露季度数】{len(quarters)} 个季度（可看历史主线如何切换）")

    # 业绩/规模/配置
    if pz:
        ac = [p for p in (pz.get("累计净值走势") or []) if p and len(p) >= 2 and p[1] is not None]
        if ac:
            print(f"\n【业绩（按累计净值估算）】")
            print(f"  今年以来 {F.year_return(ac)}% | 近1年 {F.window_return(ac,365)}% | "
                  f"近3年 {F.window_return(ac,365*3)}% | 成立以来 {round((ac[-1][1]/ac[0][1]-1)*100,2)}%")
            print(f"  成立以来最大回撤 {F.max_drawdown(ac)}%")
        gt = pz.get("累计收益率走势") or []
        if gt and gt[0].get("data"):
            rng = gt[0]["data"]
            print(f"  区间对比（{F.fmt_ts(rng[0][0])}~{F.fmt_ts(rng[-1][0])}）：" +
                  " | ".join(f"{s['name']} {s['data'][-1][1]}%" for s in gt if s.get("data")))
        fs = pz.get("规模变动") or {}
        if isinstance(fs, dict) and fs.get("series"):
            last = fs["series"][-1]
            print(f"【规模】最新 {last.get('y')} 亿元（{fs['categories'][-1]}）")
        aa = pz.get("资产配置") or {}
        if isinstance(aa, dict) and aa.get("series"):
            parts = [f"{s['name']} {s['data'][-1]}%" for s in aa["series"] if s.get("data") and "占" in (s.get("name") or "")]
            if parts:
                print(f"【资产配置】{aa['categories'][-1]}：" + "；".join(parts))
        fm = pz.get("基金经理") or []
        for m in (fm if isinstance(fm, list) else []):
            prof = m.get("profit") or {}
            ser = (prof.get("series") or [{}])[0].get("data") if prof.get("series") else None
            if prof.get("categories") and ser:
                print(f"【现任经理任职回报】{m.get('name')}：" +
                      "；".join(f"{c} {x.get('y')}%" for c, x in zip(prof["categories"], ser)))
        pe = pz.get("业绩评价") or {}
        if isinstance(pe, dict) and isinstance(pe.get("data"), list):
            print("【天天基金五维(满分100)】" + "；".join(f"{c}{v}" for c, v in zip(pe.get("categories", []), pe["data"])))

    print("\n" + "=" * 70)
    print("下一步：用 references/scorecard.md 的六维逐项打分，给总分、评级、理由。")
    print("提醒：本评分衡量“与郑希风格的契合度”，非基金优劣，亦非投资建议；")
    print("      个股 ROE / 流动性等无数据项请标“需核实”，不要臆造。")
    print("=" * 70)


if __name__ == "__main__":
    main()
