# -*- coding: utf-8 -*-
"""抓取郑希全部基金的真实数据（持仓 / 净值业绩 / 规模 / 基本信息），生成快照到
references/fund_data/。这是“快照 + 可刷新”模式：要更新数据时重跑本脚本即可。

  python scripts/fetch_fund_data.py            # 抓全部基金
  python scripts/fetch_fund_data.py 001513     # 只抓指定代码

数据来源：
  - 基金清单：易方达官网 manager 接口（拿到郑希在任/曾任全部主基金及任职区间）
  - 净值/业绩/规模/经理：天天基金 pingzhongdata/{code}.js
  - 季度前十大持仓：天天基金 FundArchivesDatas.aspx?type=jjcc
全部为公开披露数据。研究与学习辅助，非投资建议。
"""
import os, re, sys, json, time, datetime
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "references", "fund_data")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
THIS_YEAR = datetime.date.today().year

S = requests.Session()
S.headers.update({"User-Agent": UA})
S.verify = False


def safe(s):
    return re.sub(r'[\\/:*?"<>|\s]+', "_", (s or "").strip())[:80]


def get(url, referer=None, tries=3):
    h = {"Referer": referer} if referer else {}
    for i in range(tries):
        try:
            r = S.get(url, headers=h, timeout=40)
            r.encoding = "utf-8"
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(f"   重试({i+1}) {url[:70]}: {e}")
        time.sleep(1.5)
    return None


# ---------- 1. 郑希基金清单（含任职区间） ----------
def fund_list():
    api = "https://api.efunds.com.cn/xcowch/front/efund/fundmanager/fundlist"
    h = {"Content-Type": "application/json; charset=utf-8",
         "Referer": "https://www.efunds.com.cn/manager/462.shtml"}
    funds = []
    for flag, role in [("Y", "在任"), ("N", "曾任")]:
        r = S.post(api, data=json.dumps({"managerCode": "zhengxi", "isPreview": False,
                   "pageIndex": 0, "pageSize": "50", "siteID": "1", "isOnWork": flag},
                   ensure_ascii=False).encode("utf-8"), headers=h, timeout=40)
        d = json.loads(r.content.decode("utf-8"))
        seen = set()
        for f in d["data"]["fundList"]:
            main = f.get("mainFundName") or f.get("fundName")
            if main in seen:
                continue
            seen.add(main)
            funds.append({"code": f.get("fundCode"), "name": main, "role": role,
                          "start": f.get("startDate"), "end": f.get("endDate"),
                          "type": "/".join(f.get("type") or [])})
    return funds


# ---------- 2. pingzhongdata：净值/业绩/规模/经理 ----------
def parse_pingzhong(code):
    txt = get(f"https://fund.eastmoney.com/pingzhongdata/{code}.js")
    if not txt:
        return None

    def var(name, default=None):
        m = re.search(r"var\s+" + re.escape(name) + r"\s*=\s*(.*?);\s*(?:/\*|var\s|function|$)", txt, re.S)
        if not m:
            return default
        raw = m.group(1).strip()
        try:
            return json.loads(raw)
        except Exception:
            return raw.strip('"')

    return {
        "fS_name": var("fS_name"),
        "fS_code": var("fS_code"),
        "费率": var("fund_Rate"),
        "起购": var("fund_minsg"),
        "单位净值走势": var("Data_netWorthTrend"),       # [{x:ts, y:nav, equityReturn, unitMoney}]
        "累计净值走势": var("Data_ACWorthTrend"),        # [[ts, acworth]]
        "累计收益率走势": var("Data_grandTotal"),         # [{name, data:[[ts,pct]]}]  本基金 vs 同类 vs 沪深300
        "同类排名走势": var("Data_rateInSimilarType"),
        "规模变动": var("Data_fluctuationScale"),
        "持有人结构": var("Data_holderStructure"),
        "资产配置": var("Data_assetAllocation"),
        "业绩评价": var("Data_performanceEvaluation"),
        "基金经理": var("Data_currentFundManager"),
    }


def fmt_ts(ms):
    try:
        return datetime.datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d")
    except Exception:
        return str(ms)


def window_return(ac, days):
    """从累计净值序列 [[ts,val]] 计算最近 days 天的区间收益%。"""
    if not ac or len(ac) < 2:
        return None
    last_ts, last_v = ac[-1]
    target = last_ts - days * 86400 * 1000
    base = None
    for ts, v in ac:
        if ts >= target:
            base = v
            break
    if not base:
        base = ac[0][1]
    if not base:
        return None
    return round((last_v / base - 1) * 100, 2)


def max_drawdown(ac):
    if not ac:
        return None
    peak = -1e9
    mdd = 0
    for _, v in ac:
        peak = max(peak, v)
        if peak > 0:
            mdd = min(mdd, v / peak - 1)
    return round(mdd * 100, 2)


def year_return(ac):
    """今年以来收益%。"""
    if not ac:
        return None
    last_ts, last_v = ac[-1]
    jan1 = datetime.datetime(THIS_YEAR, 1, 1).timestamp() * 1000
    base = None
    for ts, v in ac:
        if ts >= jan1:
            base = v
            break
    if not base or not base:
        return None
    return round((last_v / base - 1) * 100, 2)


# ---------- 3. 季度前十大持仓 ----------
def parse_holdings(code, year):
    url = (f"https://fundf10.eastmoney.com/FundArchivesDatas.aspx?"
           f"type=jjcc&code={code}&topline=10&year={year}&month=")
    txt = get(url, referer="https://fundf10.eastmoney.com/")
    if not txt:
        return []
    m = re.search(r'content:"(.*)",arryear:', txt, re.S)
    if not m:
        return []
    html = m.group(1).encode().decode("unicode_escape", errors="ignore") if "\\u" in m.group(1) else m.group(1)
    soup = BeautifulSoup(m.group(1), "lxml")
    quarters = []
    for box in soup.select(".boxitem"):
        h = box.select_one("h4 .left")
        title = h.get_text(" ", strip=True) if h else ""
        qm = re.search(r"(\d{4})年(\d)季度", title)
        if not qm:
            continue
        rows = []
        for tr in box.select("table tbody tr"):
            tds = [td.get_text(strip=True) for td in tr.select("td")]
            a = tr.select_one("td a")
            if len(tds) < 4:
                continue
            # 列：序号 代码 名称 [相关资讯...] 占净值比 持股数 持仓市值
            code_ = tds[1]
            name_ = tds[2]
            pct = next((t for t in tds if t.endswith("%")), "")
            rows.append({"股票代码": code_, "股票名称": name_, "占净值比": pct,
                         "_raw": tds})
        if rows:
            quarters.append({"year": int(qm.group(1)), "quarter": int(qm.group(2)),
                             "title": title, "holdings": rows})
    return quarters


# ---------- 主流程 ----------
def render_fund_md(meta, pz):
    nm = pz.get("fS_name") if pz else meta["name"]
    L = [f"# {nm}（{meta['code']}） · 净值/业绩/规模", ""]
    if meta.get("role"):
        L.append(f"- 郑希任职：{meta['role']}，{meta['start']} ~ {meta['end']}（类型 {meta.get('type','')}）")
    else:
        L.append(f"- 类型：{meta.get('type','')}")
    if not pz:
        L.append("\n> 未取到天天基金数据。")
        return "\n".join(L)
    ac = [p for p in (pz.get("累计净值走势") or []) if p and len(p) >= 2 and p[1] is not None]
    nwt = [p for p in (pz.get("单位净值走势") or []) if isinstance(p, dict) and p.get("y") is not None]
    if nwt:
        last = nwt[-1]
        L.append(f"- 最新单位净值：{last.get('y')}（{fmt_ts(last.get('x'))}）")
    if ac:
        L.append(f"- 最新累计净值：{ac[-1][1]}（{fmt_ts(ac[-1][0])}）")
    # 收益与回撤（基于累计净值）
    L.append("")
    L.append("## 区间收益与回撤（按累计净值估算）")
    L.append(f"- 今年以来：{year_return(ac)}%")
    L.append(f"- 近1年：{window_return(ac,365)}%")
    L.append(f"- 近3年：{window_return(ac,365*3)}%")
    L.append(f"- 成立以来累计：{round((ac[-1][1]/ac[0][1]-1)*100,2) if ac else None}%")
    L.append(f"- 最大回撤（成立以来）：{max_drawdown(ac)}%")
    # 收益率 vs 同类/沪深300（grandTotal 仅覆盖近 6 个月区间，按实际起止标注）
    gt = pz.get("累计收益率走势") or []
    if gt and (gt[0].get("data")):
        rng = gt[0]["data"]
        L.append("")
        L.append(f"## 区间收益率对比（{fmt_ts(rng[0][0])} ~ {fmt_ts(rng[-1][0])}）")
        for s in gt:
            data = s.get("data") or []
            if data:
                L.append(f"- {s.get('name')}：{data[-1][1]}%")
    # 规模
    fs = pz.get("规模变动") or {}
    cats = fs.get("categories") or [] if isinstance(fs, dict) else []
    series = fs.get("series") or [] if isinstance(fs, dict) else []
    if cats and series:
        last = series[-1]
        y = last.get("y") if isinstance(last, dict) else last
        L.append("")
        L.append(f"## 规模\n- 最新披露规模：{y} 亿元（{cats[-1]}，环比 {last.get('mom') if isinstance(last,dict) else ''}）")
    # 资产配置（最新一期）
    aa = pz.get("资产配置") or {}
    if isinstance(aa, dict) and aa.get("categories"):
        acats = aa["categories"]
        parts = []
        for s in aa.get("series", []):
            data = s.get("data") or []
            if data and "占" in (s.get("name") or ""):
                parts.append(f"{s['name']} {data[-1]}%")
        if parts:
            L.append(f"\n## 资产配置（{acats[-1]}）\n- " + "；".join(parts))
    # 基金经理（含任职回报）
    fm = pz.get("基金经理") or []
    if isinstance(fm, list) and fm:
        L.append("")
        L.append("## 现任基金经理（天天基金口径）")
        for m in fm:
            line = f"- {m.get('name')}：任职 {m.get('workTime')}，在管 {m.get('fundSize')}"
            prof = m.get("profit") or {}
            ser = (prof.get("series") or [{}])[0].get("data") if prof.get("series") else None
            if prof.get("categories") and ser:
                rets = "；".join(f"{c} {d.get('y')}%" for c, d in zip(prof["categories"], ser))
                line += f"\n    - 任职回报：{rets}（截至 {prof.get('jzrq','')}）"
            L.append(line)
        L.append("  > 注：此为该基金“现任”经理数据；郑希若已离任，任职回报不代表其任内表现，请结合上方任职区间判断。")
    # 业绩评价
    pe = pz.get("业绩评价") or {}
    if isinstance(pe, dict) and pe.get("categories") and isinstance(pe.get("data"), list):
        L.append("")
        L.append("## 业绩评价（天天基金五维，满分100）")
        for c, v in zip(pe["categories"], pe["data"]):
            L.append(f"- {c}：{v}")
    return "\n".join(L)


def render_holdings_md(meta, quarters):
    nm = meta["name"]
    L = [f"# {nm}（{meta['code']}） · 季度前十大重仓股", ""]
    if meta.get("role"):
        L.append(f"- 郑希任职：{meta['role']}，{meta['start']} ~ {meta['end']}")
    else:
        L.append(f"- 类型：{meta.get('type','')}")
    L.append(f"- 共 {len(quarters)} 个季度披露\n")
    for q in sorted(quarters, key=lambda x: (x["year"], x["quarter"]), reverse=True):
        L.append(f"## {q['year']}年第{q['quarter']}季度")
        for i, h in enumerate(q["holdings"], 1):
            L.append(f"{i}. {h['股票名称']}（{h['股票代码']}） 占净值 {h['占净值比']}")
        L.append("")
    return "\n".join(L)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(OUT, exist_ok=True)
    funds = fund_list()
    if only:
        funds = [f for f in funds if f["code"] == only]
    index = []
    for meta in funds:
        code = meta["code"]
        print(f"\n=== {code} {meta['name']} ({meta['role']}) ===")
        try:
            _process_fund(meta, index)
        except Exception as e:
            print(f"  !! {code} 处理失败，跳过：{e}")
        time.sleep(1)
    _write_index(index)


def _process_fund(meta, index):
        code = meta["code"]
        d = os.path.join(OUT, f"{code}_{safe(meta['name'])}")
        os.makedirs(d, exist_ok=True)

        print("  抓 净值/业绩/规模/经理 ...")
        pz = parse_pingzhong(code)
        if pz:
            with open(os.path.join(d, "净值业绩规模.json"), "w", encoding="utf-8") as f:
                json.dump(pz, f, ensure_ascii=False)
        with open(os.path.join(d, "净值业绩规模.md"), "w", encoding="utf-8") as f:
            f.write(render_fund_md(meta, pz))

        print("  抓 季度持仓 ...")
        start_year = int((meta["start"] or "2012")[:4])
        quarters = []
        for y in range(start_year, THIS_YEAR + 1):
            quarters += parse_holdings(code, y)
            time.sleep(0.5)
        # 去重
        uniq = {}
        for q in quarters:
            uniq[(q["year"], q["quarter"])] = q
        quarters = list(uniq.values())
        with open(os.path.join(d, "季度持仓.json"), "w", encoding="utf-8") as f:
            json.dump(quarters, f, ensure_ascii=False)
        with open(os.path.join(d, "季度持仓.md"), "w", encoding="utf-8") as f:
            f.write(render_holdings_md(meta, quarters))
        print(f"  完成：{len(quarters)} 个季度持仓")

        index.append({**meta, "fund_name_em": pz.get("fS_name") if pz else None,
                      "quarters": len(quarters),
                      "dir": os.path.relpath(d, ROOT).replace("\\", "/")})


def _write_index(index):
    # 与已有索引按代码合并（单只刷新时不丢其它基金）
    merged = {}
    idx_path = os.path.join(OUT, "_index.json")
    if os.path.exists(idx_path):
        try:
            for it in json.load(open(idx_path, encoding="utf-8")).get("funds", []):
                merged[it["code"]] = it
        except Exception:
            pass
    for it in index:
        merged[it["code"]] = it
    index = sorted(merged.values(), key=lambda x: (x["role"] != "在任", x["code"]))
    with open(os.path.join(OUT, "_index.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                   "source": "天天基金/易方达官网（公开数据）", "funds": index},
                  f, ensure_ascii=False, indent=2)
    # 索引 md
    L = [f"# 郑希基金数据快照", f"", f"更新时间：{datetime.datetime.now():%Y-%m-%d %H:%M}　数据来源：天天基金（公开数据）", ""]
    for it in index:
        L.append(f"- **{it['name']}**（{it['code']}，{it['role']}，{it['start']}~{it['end']}）"
                 f"— {it['quarters']} 个季度持仓，详见 `{it['dir']}/`")
    L.append("\n> 公开披露数据，研究与学习辅助，非投资建议。")
    with open(os.path.join(OUT, "_index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"\n全部完成，共 {len(index)} 只基金。索引：references/fund_data/_index.md")
    return index


if __name__ == "__main__":
    main()
