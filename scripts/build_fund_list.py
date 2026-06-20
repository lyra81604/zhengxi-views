# -*- coding: utf-8 -*-
"""下载全市场公募基金代码列表，生成 references/all_funds/fund_list.json（可打包、可检索）。
全市场约 2.7 万只基金。刷新重跑：  python scripts/build_fund_list.py
来源：天天基金 fundcode_search.js（公开数据）。
"""
import os, re, json, datetime
import requests

requests.packages.urllib3.disable_warnings()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "references", "all_funds")


def main():
    os.makedirs(OUT, exist_ok=True)
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60, verify=False)
    r.encoding = "utf-8"
    m = re.search(r"=\s*(\[.*\]);?\s*$", r.text, re.S)
    arr = json.loads(m.group(1))
    funds = [{"code": x[0], "abbr": x[1], "name": x[2], "type": x[3], "pinyin": x[4]}
             for x in arr if len(x) >= 5]
    data = {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": "天天基金 fundcode_search.js（公开数据）",
        "count": len(funds),
        "funds": funds,
    }
    with open(os.path.join(OUT, "fund_list.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    # 类型清单（便于按类型筛选时知道有哪些类型名）
    types = sorted({f["type"] for f in funds})
    with open(os.path.join(OUT, "_types.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(types))
    print(f"已写入 {len(funds)} 只基金 → references/all_funds/fund_list.json")
    print(f"类型共 {len(types)} 种，见 references/all_funds/_types.txt")


if __name__ == "__main__":
    main()
