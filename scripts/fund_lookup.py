# -*- coding: utf-8 -*-
"""在全市场基金列表里查找基金（按代码 / 名称关键词 / 类型）。
用于把基金名解析成代码、找同类基金、确认代码对应的基金。

用法:
  python scripts/fund_lookup.py 中际旭创          # 关键词（名称/拼音/代码）
  python scripts/fund_lookup.py 易方达 --type 混合 # 名称含“易方达”且类型含“混合”
  python scripts/fund_lookup.py 005827            # 直接按代码
  python scripts/fund_lookup.py 光伏 --max 30
依赖 references/all_funds/fund_list.json（先跑 build_fund_list.py 生成）。
"""
import os, sys, json, argparse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIST = os.path.join(ROOT, "references", "all_funds", "fund_list.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*", help="名称/拼音/代码关键词（可多个，需全部命中名称）")
    ap.add_argument("--type", default=None, help="按类型过滤（子串匹配，如 混合 / 指数 / QDII / 债券）")
    ap.add_argument("--max", type=int, default=40)
    args = ap.parse_args()

    if not os.path.exists(LIST):
        print("缺少 fund_list.json，请先运行：python scripts/build_fund_list.py")
        return
    data = json.load(open(LIST, encoding="utf-8"))
    funds = data["funds"]
    q = [s for s in args.query]

    def hit(f):
        if args.type and args.type not in f["type"]:
            return False
        if not q:
            return True
        # 纯代码精确/前缀匹配
        for kw in q:
            up = kw.upper()
            in_code = kw in f["code"]
            in_name = kw in f["name"]
            in_abbr = up in f["abbr"]
            in_py = up in f["pinyin"]
            if not (in_code or in_name or in_abbr or in_py):
                return False
        return True

    res = [f for f in funds if hit(f)]
    print(f"全市场 {data['count']} 只基金（更新 {data['updated']}），命中 {len(res)} 只：\n")
    for f in res[:args.max]:
        print(f"  {f['code']}  {f['name']}  [{f['type']}]")
    if len(res) > args.max:
        print(f"\n(还有 {len(res)-args.max} 只未显示，用 --max 或加更具体的关键词/--type)")
    if res:
        print(f"\n提示：拿到代码后，用 python scripts/fetch_any_fund.py <代码> 抓它的持仓/净值/业绩。")


if __name__ == "__main__":
    main()
