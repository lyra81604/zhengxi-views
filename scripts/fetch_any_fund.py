# -*- coding: utf-8 -*-
"""按需抓取【全市场任意基金】的真实数据（季度持仓 / 净值业绩 / 规模），存入缓存
references/fund_data_cache/{code}_{name}/，供 skill 回答任意基金的问题、做同类对比。

用法:
  python scripts/fetch_any_fund.py 005827              # 抓单只
  python scripts/fetch_any_fund.py 005827 161725 110011 # 抓多只（如做对比）
  python scripts/fetch_any_fund.py 005827 --force      # 忽略缓存重新抓

说明:
  - 复用 fetch_fund_data.py 的解析与渲染逻辑，数据源同为天天基金公开数据。
  - 基金名/类型从 references/all_funds/fund_list.json 解析（先跑 build_fund_list.py）。
  - 默认 7 天内抓过的直接用缓存；--force 强制刷新。
  - 郑希自己的 8 只基金已有精编快照在 references/fund_data/，无需用本脚本。
研究与学习辅助，非投资建议。
"""
import os, sys, json, time, datetime
import fetch_fund_data as F  # 复用 parse_pingzhong / parse_holdings / render_* / THIS_YEAR

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "references", "fund_data_cache")
LIST = os.path.join(ROOT, "references", "all_funds", "fund_list.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_LIST = None


def lookup(code):
    global _LIST
    if _LIST is None:
        _LIST = {f["code"]: f for f in json.load(open(LIST, encoding="utf-8"))["funds"]} if os.path.exists(LIST) else {}
    f = _LIST.get(code)
    return {"code": code, "name": f["name"] if f else code, "type": f["type"] if f else "", "role": ""}


def fresh(d, days=7):
    p = os.path.join(d, "净值业绩规模.md")
    if not os.path.exists(p):
        return False
    age = time.time() - os.path.getmtime(p)
    return age < days * 86400


def fetch_one(code, force=False):
    meta = lookup(code)
    d = os.path.join(CACHE, f"{code}_{F.safe(meta['name'])}")
    if fresh(d) and not force:
        print(f"  {code} {meta['name']}：缓存仍新鲜，跳过（--force 可强制刷新）")
        return d
    os.makedirs(d, exist_ok=True)
    print(f"=== {code} {meta['name']} [{meta['type']}] ===")
    print("  抓 净值/业绩/规模 ...")
    pz = F.parse_pingzhong(code)
    if pz:
        with open(os.path.join(d, "净值业绩规模.json"), "w", encoding="utf-8") as f:
            json.dump(pz, f, ensure_ascii=False)
    with open(os.path.join(d, "净值业绩规模.md"), "w", encoding="utf-8") as f:
        f.write(F.render_fund_md(meta, pz))
    print("  抓 季度持仓 ...")
    quarters = []
    for y in range(2003, F.THIS_YEAR + 1):
        qs = F.parse_holdings(code, y)
        quarters += qs
        time.sleep(0.4)
    uniq = {}
    for q in quarters:
        uniq[(q["year"], q["quarter"])] = q
    quarters = list(uniq.values())
    with open(os.path.join(d, "季度持仓.json"), "w", encoding="utf-8") as f:
        json.dump(quarters, f, ensure_ascii=False)
    with open(os.path.join(d, "季度持仓.md"), "w", encoding="utf-8") as f:
        f.write(F.render_holdings_md(meta, quarters))
    print(f"  完成：{len(quarters)} 个季度持仓 → {os.path.relpath(d, ROOT)}")
    return d


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if not args:
        print("用法: python scripts/fetch_any_fund.py <基金代码> [更多代码...] [--force]")
        print("找代码: python scripts/fund_lookup.py <关键词>")
        return
    os.makedirs(CACHE, exist_ok=True)
    for code in args:
        try:
            fetch_one(code, force=force)
        except Exception as e:
            print(f"  !! {code} 抓取失败：{e}")
        time.sleep(0.8)


if __name__ == "__main__":
    main()
