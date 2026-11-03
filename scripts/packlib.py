"""Shared helpers for subject content packs (seed/packs/<code>.json), loaded by backend/scripts/seed.py.

Original wording throughout (C-06): notes, revision sheets, LOS paraphrases, MCQs and flashcards.
"""

import json
import re
from pathlib import Path

PACKS = Path(__file__).resolve().parents[1] / "seed" / "packs"


def inl(text: str) -> list[dict]:
    """'plain **bold** plain' -> notes/v1 inline runs."""
    runs = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            runs.append({"t": part, "b": True} if i % 2 else {"t": part})
    return runs


def P(t): return {"type": "paragraph", "inline": inl(t)}
def H(t): return {"type": "heading", "level": 3, "text": t}
def L(*items): return {"type": "list", "ordered": False, "items": [inl(x) for x in items]}
def OL(*items): return {"type": "list", "ordered": True, "items": [inl(x) for x in items]}
def T(header, *rows): return {"type": "table", "header": header, "rows": [list(r) for r in rows]}
def EX(t): return {"type": "callout", "variant": "example", "title": "Worked example", "inline": inl(t)}
def WO(t): return {"type": "callout", "variant": "watch_out", "title": "Watch out", "inline": inl(t)}
def FX(t, title="Formula"): return {"type": "callout", "variant": "formula", "title": title, "inline": inl(t)}
def FUN(t): return {"type": "callout", "variant": "fun", "title": "Funny use case", "inline": inl(t)}
def doc(*blocks): return {"schema": "notes/v1", "blocks": list(blocks)}
def topic(title, *blocks): return {"title": title, "body": doc(*blocks)}
def sheet(formula, *rows): return doc(FX(formula, "Revision sheet · 1 page"), T(["Remember", "Point"], *rows))
def q(d, stem, opts, a, e, los): return {"d": d, "q": stem, "o": opts, "a": a, "e": e, "los": los}
def fc(front, back): return {"front": front, "back": back}


def _rotate_key(x: dict, target: int) -> dict:
    """Rotate the options (keeping their cyclic order) so the correct answer sits at `target`."""
    k = (x["a"] - target) % 3
    return {**x, "o": x["o"][k:] + x["o"][:k], "a": target}


def write_pack(code: str, name: str, lms: list[dict], retag_proto: dict[str, int] | None = None,
               balance_keys: bool = False) -> None:
    """balance_keys: cycle the correct answer through A, B, C within each LM (§8.1 answer balance)."""
    out_lms = []
    for lm in lms:
        lm = dict(lm)
        if balance_keys:
            lm["questions"] = [_rotate_key(x, (i + lm["lm_no"]) % 3) for i, x in enumerate(lm["questions"])]
        lm["los"] = [{"code": c, "command_word": w, "statement": s} for c, w, s in lm["los"]]
        codes = {o["code"] for o in lm["los"]}
        for i, x in enumerate(lm["questions"]):
            where = f"{code} LM{lm['lm_no']} Q{i + 1}"
            assert len(x["o"]) == 3 and len(set(x["o"])) == 3 and 0 <= x["a"] <= 2, where
            assert x["d"] in "EMH" and x["los"] in codes, where
        assert len(lm["questions"]) >= 3, f"{code} LM{lm['lm_no']}: chapter quiz needs at least 3 questions"
        out_lms.append(lm)
    nos = [lm["lm_no"] for lm in out_lms]
    assert nos == list(range(1, len(nos) + 1)), f"{code}: LM numbers must run 1..n"
    pack = {"subject": code, "name": name, "lms": out_lms, "retag_proto": retag_proto or {}}
    PACKS.mkdir(parents=True, exist_ok=True)
    out = PACKS / f"{code}.json"
    out.write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Wrote {out.name}: {len(out_lms)} LMs, {sum(len(x['questions']) for x in out_lms)} questions, "
          f"{sum(len(x['flashcards']) for x in out_lms)} flashcards, {sum(len(x['los']) for x in out_lms)} LOS")
