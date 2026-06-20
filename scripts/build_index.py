# -*- coding: utf-8 -*-
"""扫描 references/corpus，生成 corpus_index.json（语料目录索引）。
语料更新后重新运行即可：  python scripts/build_index.py
"""
import os, re, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "references", "corpus")

TYPE_DIR = {
    "定期报告": "定期报告",
    "基金经理手记": "基金经理手记",
    "媒体报道": "媒体报道",
}


def parse_md(path):
    text = open(path, encoding="utf-8").read()
    title = ""
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
    date = ""
    m = re.search(r"日期[:：]\s*([0-9\-]+)", text)
    if m:
        date = m.group(1).strip()
    source = ""
    m = re.search(r"来源[:：]\s*(.+)", text)
    if m:
        source = m.group(1).strip()
    link = ""
    m = re.search(r"原文链接[:：]\s*(\S+)", text)
    if m:
        link = m.group(1).strip()
    # body = 去掉头部元数据后的正文
    body = text.split("---", 1)[-1] if "---" in text else text
    return title, date, source, link, len(body)


def main():
    docs = []
    for tdir, ttype in TYPE_DIR.items():
        for path in sorted(glob.glob(os.path.join(CORPUS, tdir, "*.md"))):
            title, date, source, link, blen = parse_md(path)
            docs.append({
                "type": ttype,
                "title": title,
                "date": date,
                "source": source,
                "link": link,
                "body_chars": blen,
                "path": os.path.relpath(path, ROOT).replace("\\", "/"),
            })
    docs.sort(key=lambda d: (d["type"], d["date"] or ""), reverse=False)
    out = {
        "manager": "郑希",
        "manager_id": "462",
        "home": "https://www.efunds.com.cn/manager/462.shtml",
        "counts": {t: sum(1 for d in docs if d["type"] == t) for t in TYPE_DIR},
        "date_range": {
            "min": min((d["date"] for d in docs if d["date"]), default=""),
            "max": max((d["date"] for d in docs if d["date"]), default=""),
        },
        "documents": docs,
    }
    dst = os.path.join(ROOT, "references", "corpus_index.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"索引已生成: {dst}")
    print(f"共 {len(docs)} 篇 | {out['counts']} | {out['date_range']}")


if __name__ == "__main__":
    main()
