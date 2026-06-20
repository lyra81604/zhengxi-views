# -*- coding: utf-8 -*-
"""在郑希语料中按关键词检索，返回带出处（标题+日期+来源+文件）的段落片段。

用法:
  python scripts/search_corpus.py "AI算力"
  python scripts/search_corpus.py "光通信" "ROE" --any        # 命中任一关键词
  python scripts/search_corpus.py "新能源" --type 定期报告 --context 2
  python scripts/search_corpus.py "周期拼接" --max 15

说明:
  - 默认: 段落需命中“全部”关键词(AND)；--any 改为命中任一(OR)。
  - --type 限定类型(定期报告/基金经理手记/媒体报道)，可重复。
  - --context N: 命中段落额外带上前后各 N 个段落，便于看上下文。
  - 输出每条片段都附 [类型 | 日期 | 标题 | 来源 | 文件路径]，可直接用于溯源引用。
"""
import os, re, sys, glob, argparse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "references", "corpus")
TYPES = ["定期报告", "基金经理手记", "媒体报道"]


def load_doc(path):
    text = open(path, encoding="utf-8").read()
    title = (re.search(r"^#\s+(.+)$", text, re.M) or [None, ""])[1].strip() if re.search(r"^#\s+(.+)$", text, re.M) else ""
    date = (re.search(r"日期[:：]\s*([0-9\-]+)", text) or [None, ""])
    date = date.group(1).strip() if hasattr(date, "group") else ""
    src = re.search(r"来源[:：]\s*(.+)", text)
    src = src.group(1).strip() if src else ""
    body = text.split("---", 1)[-1] if "---" in text else text
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    return title, date, src, paras


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", nargs="+")
    ap.add_argument("--any", action="store_true", help="命中任一关键词即可(默认要求全部命中)")
    ap.add_argument("--type", action="append", choices=TYPES, help="限定文档类型(可重复)")
    ap.add_argument("--context", type=int, default=0, help="命中段落附带前后各 N 段")
    ap.add_argument("--max", type=int, default=20, help="最多返回片段数")
    args = ap.parse_args()

    kws = args.keywords
    types = args.type or TYPES
    hits = []
    for t in types:
        for path in sorted(glob.glob(os.path.join(CORPUS, t, "*.md"))):
            title, date, src, paras = load_doc(path)
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            for i, p in enumerate(paras):
                matched = [k for k in kws if k in p]
                ok = (len(matched) > 0) if args.any else (len(matched) == len(kws))
                if ok:
                    lo = max(0, i - args.context)
                    hi = min(len(paras), i + args.context + 1)
                    snippet = "\n".join(paras[lo:hi])
                    hits.append((date, t, title, src, rel, matched, snippet))

    hits.sort(key=lambda h: h[0], reverse=True)  # 新→旧
    if not hits:
        print(f"未命中：{kws}（类型 {types}）。可换近义词或加 --any 放宽。")
        return
    print(f"命中 {len(hits)} 段，显示前 {min(args.max,len(hits))} 段（新→旧）：\n")
    for date, t, title, src, rel, matched, snippet in hits[:args.max]:
        cite = f"[{t} | {date} | {title}" + (f" | 来源:{src}" if src else "") + f" | {rel}]"
        print(cite)
        print(f"命中: {', '.join(matched)}")
        print(snippet)
        print("\n" + "-" * 80 + "\n")
    if len(hits) > args.max:
        print(f"(还有 {len(hits)-args.max} 段未显示，用 --max 调整)")


if __name__ == "__main__":
    main()
