"""One-off: extract seed content from the prototype HTML into seed/*.json (A-03 §7).

Converts the prototype's notes HTML into the notes/v1 block schema (ADR-012), so no raw
HTML reaches the database.

Usage:  python scripts/extract_prototype.py
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Documentation" / "01_Product" / "Karan_Sir_Classes_Platform_Demo.html"
OUT = ROOT / "seed"

CALLOUT = {"ex": "example", "wo": "watch_out", "fx": "formula", "fun": "fun"}


def js_unescape(s: str) -> str:
    return s.replace("\\'", "'").replace('\\"', '"')


class NotesParser(HTMLParser):
    """Small, strict converter for the limited HTML used in the prototype notes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict] = []
        self.stack: list[str] = []
        self.inline: list[dict] | None = None
        self.bold = 0
        self.list_items: list | None = None
        self.table: dict | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.callout: dict | None = None
        self.in_label = False
        self.heading: list[str] | None = None
        self.wf: list[dict] | None = None
        self.wf_row: dict | None = None
        self.wf_part: str | None = None
        self.wf_depth = 0

    def _cls(self, attrs) -> list[str]:
        return (dict(attrs).get("class") or "").split()

    def handle_starttag(self, tag, attrs):
        cls = self._cls(attrs)
        a = dict(attrs)
        self.stack.append(tag)
        if self.wf is not None and tag == "div":
            self.wf_depth += 1
        if tag == "div" and "wf" in cls:
            self.wf, self.wf_depth = [], 1
        elif self.wf is not None and tag == "div" and "row" in cls:
            self.wf_row = {"label": "", "text": "", "pct": 100}
        elif self.wf_row is not None and tag == "span":
            self.wf_part = "label"
        elif self.wf_row is not None and tag == "div" and "b" in cls:
            m = re.search(r"--w:(\d+)%", a.get("style", ""))
            self.wf_row["pct"] = int(m.group(1)) if m else 100
            self.wf_part = "text"
        elif tag == "div" and "box" in cls:
            variant = next((CALLOUT[c] for c in cls if c in CALLOUT), "note")
            self.callout = {"type": "callout", "variant": variant, "title": "", "inline": []}
            self.inline = self.callout["inline"]
        elif tag == "div" and "lb" in cls and self.callout is not None:
            self.in_label = True
        elif tag == "p":
            self.inline = []
        elif tag in ("h3", "h4"):
            self.heading = []
        elif tag == "ul":
            self.list_items = []
        elif tag == "li" and self.list_items is not None:
            self.inline = []
        elif tag == "table":
            self.table = {"type": "table", "header": [], "rows": []}
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag == "b":
            self.bold += 1
        elif tag == "br" and self.inline is not None:
            self._text(" ")
            self.stack.pop()

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()
        if self.wf is not None:
            if tag == "span":
                self.wf_part = None
            elif tag == "div":
                self.wf_depth -= 1
                if self.wf_part == "text" and self.wf_row is not None:
                    self.wf.append(self.wf_row)
                    self.wf_row, self.wf_part = None, None
                elif self.wf_depth == 0:
                    alt = "Priority of claims: " + ", then ".join(r["label"] for r in self.wf)
                    self.blocks.append({"type": "infographic", "kind": "waterfall", "data": self.wf, "alt": alt})
                    self.wf = None
            return
        if tag == "div" and self.in_label:
            self.in_label = False
        elif tag == "div" and self.callout is not None:
            self._trim(self.callout["inline"])
            self.blocks.append(self.callout)
            self.callout, self.inline = None, None
        elif tag == "p" and self.inline is not None:
            self._trim(self.inline)
            if self.inline:
                if self.callout is not None:
                    self.callout["inline"].extend(self.inline)
                else:
                    self.blocks.append({"type": "paragraph", "inline": self.inline})
            self.inline = self.callout["inline"] if self.callout else None
        elif tag in ("h3", "h4") and self.heading is not None:
            self.blocks.append({"type": "heading", "level": 3, "text": "".join(self.heading).strip()})
            self.heading = None
        elif tag == "li" and self.list_items is not None:
            self._trim(self.inline)
            self.list_items.append(self.inline)
            self.inline = None
        elif tag == "ul" and self.list_items is not None:
            self.blocks.append({"type": "list", "ordered": False, "items": self.list_items})
            self.list_items = None
        elif tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if not self.table["header"] and self.row and self.table["rows"] == [] and self._row_is_header:
                self.table["header"] = self.row
            else:
                self.table["rows"].append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            if not self.table["header"] and self.table["rows"]:
                self.table["header"] = self.table["rows"].pop(0)
            self.blocks.append(self.table)
            self.table = None
        elif tag == "b":
            self.bold = max(0, self.bold - 1)

    _row_is_header = True

    def handle_data(self, data):
        if self.wf_part and self.wf_row is not None:
            self.wf_row[self.wf_part] += data.strip()
        elif self.in_label and self.callout is not None:
            self.callout["title"] += data.strip()
        elif self.cell is not None:
            self.cell.append(data)
        elif self.heading is not None:
            self.heading.append(data)
        elif self.inline is not None:
            self._text(data)

    def _text(self, data: str) -> None:
        data = re.sub(r"\s+", " ", data)
        if not data:
            return
        if self.inline and bool(self.inline[-1].get("b")) == bool(self.bold):
            self.inline[-1]["t"] += data
        else:
            self.inline.append({"t": data, **({"b": True} if self.bold else {})})

    @staticmethod
    def _trim(inl: list[dict] | None) -> None:
        if not inl:
            return
        inl[0]["t"] = inl[0]["t"].lstrip()
        inl[-1]["t"] = inl[-1]["t"].rstrip()
        inl[:] = [i for i in inl if i["t"]]


def html_to_blocks(html: str) -> dict:
    p = NotesParser()
    p.feed(html)
    return {"schema": "notes/v1", "blocks": p.blocks}


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    bank = json.loads(re.search(r"const BANK=(\[.*?\]);const SUBJ", src, re.S).group(1))

    subj_block = re.search(r"const SUBJ=\[(.*?)\n\];", src, re.S).group(1)
    subjects = []
    for m in re.finditer(r"\{id:'(\w+)',n:'([^']+)',ic:'([^']+)',m:\[(.*?)\]\}", subj_block):
        lms = [js_unescape(x) for x in re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(4))]
        subjects.append({"code": m.group(1), "name": m.group(2), "icon": m.group(3), "lms": lms})

    wf = re.search(r"const WF=`(.*?)`;", src, re.S).group(1)
    auth_src = re.search(r"const AUTH=\{(.*?)\n\};\nfunction genContent", src, re.S).group(1)
    notes = []
    for key_m in re.finditer(r"'(\w+):(\d+)':\{", auth_src):
        start = key_m.end()
        nxt = re.search(r"\n'(\w+):(\d+)':\{", auth_src[start:])
        chunk = auth_src[start: start + nxt.start()] if nxt else auth_src[start:]
        sid, lm_index = key_m.group(1), int(key_m.group(2))
        topics = []
        for t in re.finditer(r"\{t:'((?:[^'\\]|\\.)*)',h:`(.*?)`\}", chunk, re.S):
            topics.append({"title": js_unescape(t.group(1)), "body": html_to_blocks(t.group(2).replace("${WF}", wf))})
        extra = {}
        for name, kind in (("rev", "revision_sheet"), ("info", "infographic")):
            m = re.search(name + r":`(.*?)`", chunk, re.S)
            if m:
                extra[kind] = html_to_blocks(m.group(1).replace("${WF}", wf))
        vids = [{"title": js_unescape(a), "duration": b, "topic": js_unescape(c)}
                for a, b, c in re.findall(r"\['((?:[^'\\]|\\.)*)','([\d:]+)','((?:[^'\\]|\\.)*)'\]", chunk)]
        notes.append({"subject": sid, "lm_index": lm_index, "topics": topics, "extra": extra,
                      "planned_videos": vids})

    cards_src = re.search(r"const CARDS=\{(.*?)\n\};", src, re.S).group(1)
    cards = {}
    for line in cards_src.strip().splitlines():
        m = re.match(r"(\w+):\[(.*)\],?$", line.strip())
        if m:
            pairs = re.findall(r"\['((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'\]", m.group(2))
            cards[m.group(1)] = [{"front": js_unescape(a), "back": js_unescape(b)} for a, b in pairs]

    for name, data in (("subjects", subjects), ("notes", notes), ("questions", bank), ("flashcards", cards)):
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"subjects={len(subjects)} lms={sum(len(s['lms']) for s in subjects)} note_lms={len(notes)} "
          f"topics={sum(len(n['topics']) for n in notes)} questions={len(bank)} "
          f"cards={sum(len(v) for v in cards.values())}")


if __name__ == "__main__":
    sys.exit(main())
