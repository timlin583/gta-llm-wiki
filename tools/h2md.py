"""Minimal HTML -> Markdown converter (stdlib only).
usage: h2md.py in.html out.md source_url fetched root_kind root_value
root_kind: id | tag | class  -- extract only the first matching element subtree.
Keeps text verbatim; drops scripts/styles/nav chrome, inline citation markers and [edit] links.
"""
import sys, re
from html.parser import HTMLParser

SKIP_TAGS = {"script", "style", "noscript", "svg", "template", "button", "form", "nav", "footer", "iframe", "figure_skip"}
SKIP_CLASSES = {"reference", "mw-editsection", "navbox", "navbox-styles", "reflist-skip", "noprint",
                "mw-empty-elt", "shortdescription", "hatnote-skip", "sistersitebox", "metadata",
                "mw-jump-link", "printfooter", "catlinks", "ambox", "vector-body-before-content"}
VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
BLOCK = {"p", "div", "section", "article", "main", "header", "blockquote", "figure", "figcaption", "dl", "dd", "dt", "caption"}


class Conv(HTMLParser):
    def __init__(self, kind, val):
        super().__init__(convert_charrefs=True)
        self.kind, self.val = kind, val
        self.depth = 0          # depth inside root (0 = not inside)
        self.done = False
        self.skip = 0           # depth inside skipped subtree
        self.out = []
        self.cur = []
        self.list_stack = []
        self.table = None       # list of rows
        self.row = None
        self.cell = None
        self.heading = None

    def is_root(self, tag, attrs):
        a = dict(attrs)
        if self.kind == "id":
            return a.get("id") == self.val
        if self.kind == "tag":
            return tag == self.val
        if self.kind == "class":
            return self.val in (a.get("class") or "").split()
        return False

    def flush(self):
        text = re.sub(r"[ \t\r\n]+", " ", "".join(self.cur)).strip()
        self.cur = []
        if text:
            self.out.append(text)

    def handle_starttag(self, tag, attrs):
        if self.done:
            return
        if self.depth == 0:
            if self.is_root(tag, attrs):
                self.depth = 1
            return
        if tag not in VOID:
            self.depth += 1
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        cls = set((dict(attrs).get("class") or "").split())
        style = (dict(attrs).get("style") or "").replace(" ", "")
        if tag in SKIP_TAGS or cls & SKIP_CLASSES or "display:none" in style:
            if tag not in VOID:
                self.skip = 1
            return
        if self.table is not None:
            if tag == "tr":
                self.row = []
            elif tag in ("td", "th"):
                self.cell = []
            elif tag == "br" and self.cell is not None:
                self.cell.append(" ")
            return
        if tag == "table":
            self.flush()
            self.table = []
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush()
            self.heading = int(tag[1])
        elif tag in ("ul", "ol"):
            self.flush()
            self.list_stack.append(tag)
        elif tag == "li":
            self.flush()
            indent = "  " * (len(self.list_stack) - 1)
            self.cur.append(indent + "- ")
        elif tag == "br":
            self.cur.append("\n")
        elif tag in BLOCK:
            self.flush()

    def handle_endtag(self, tag):
        if self.done or self.depth == 0:
            return
        if tag in VOID:
            return
        self.depth -= 1
        if self.depth == 0:
            self.flush()
            self.done = True
            return
        if self.skip:
            self.skip -= 1
            return
        if self.table is not None:
            if tag in ("td", "th") and self.cell is not None and self.row is not None:
                self.row.append(re.sub(r"\s+", " ", "".join(self.cell)).strip().replace("|", "\\|"))
                self.cell = None
            elif tag == "tr" and self.row is not None:
                if any(self.row):
                    self.table.append(self.row)
                self.row = None
            elif tag == "table":
                self.emit_table()
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self.heading:
            text = re.sub(r"\s+", " ", "".join(self.cur)).strip()
            self.cur = []
            if text:
                self.out.append("#" * self.heading + " " + text)
            self.heading = None
        elif tag in ("ul", "ol"):
            self.flush()
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "li" or tag in BLOCK:
            self.flush()

    def emit_table(self):
        rows = self.table
        self.table = None
        if not rows:
            return
        w = max(len(r) for r in rows)
        rows = [r + [""] * (w - len(r)) for r in rows]
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        self.out.append("\n".join(lines))

    def handle_data(self, data):
        if self.done or self.depth == 0 or self.skip:
            return
        if self.table is not None:
            if self.cell is not None:
                self.cell.append(data)
            return
        self.cur.append(data)


def main():
    src, dst, url, fetched, kind, val = sys.argv[1:7]
    with open(src, encoding="utf-8", errors="replace") as f:
        html = f.read()
    c = Conv(kind, val)
    c.feed(html)
    c.flush()
    # preserve list item line breaks: items were flushed separately, join list items with single newline
    blocks, prev_li = [], False
    for b in c.out:
        is_li = b.lstrip().startswith("- ")
        if is_li and prev_li:
            blocks[-1] += "\n" + b
        else:
            blocks.append(b)
        prev_li = is_li
    body = "\n\n".join(blocks).strip()
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"---\nsource_url: {url}\nfetched: {fetched}\n---\n\n{body}\n")
    print(dst, "blocks:", len(blocks))


if __name__ == "__main__":
    main()
