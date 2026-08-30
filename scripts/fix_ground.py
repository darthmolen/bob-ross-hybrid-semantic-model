#!/usr/bin/env python3
"""
fix_ground.py — repair Section 8 for episodes whose ground is not Liquid White.

Worklist rule: the ground is deterministic and belongs to the CSV, never to a vision
pass. A vision pass cannot tell a black gesso ground from very dark paint over Liquid
White, so it answers "Liquid White" and is wrong on exactly the episodes where the
ground carries the painting.

This is deliberately conservative. It only replaces Section 8 when that section either
asserts a Liquid White ground over a CSV black ground, or names no dark ground at all.
Sections that already state the ground correctly are left alone even when they mention
Liquid White — plenty of them say "black gesso instead of Liquid White", which is right,
and some name a secondary tone this script could not reconstruct.

It never touches sections 1-7. An affirmative Liquid White claim elsewhere in the prose
is reported by lint_index.py and adjudicated by hand, because those sentences are a mix
of genuinely wrong, correctly hedged, and legitimate references to Liquid White used as
a highlight rather than as a ground.

    python scripts/fix_ground.py --check
    python scripts/fix_ground.py --report artifacts/ground_fixed.csv
"""

from __future__ import annotations

import argparse
import ast
import csv
import glob
import os
import re
import sys

FILE_RE = re.compile(r"s(\d{2})e(\d{2})-")
LW = re.compile(r"[Ll]iquid [Ww]hite")

# An affirmative claim that Liquid White is the ground. Deliberately narrow: many
# entries mention Liquid White correctly, and those must survive untouched.
LW_GROUND = re.compile(
    r"(?:canvas\s+(?:was|is|received|begins?|start(?:s|ed)?|prepared)"
    r"|prepared\s+with|begins?\s+with|start(?:s|ed)?\s+(?:out\s+)?with"
    r"|coat(?:ed|ing)?\s+(?:of|with)|base(?:d)?\s+(?:of|on|with)|foundation\s+of"
    r"|covered\s+(?:in|with)|application\s+of|treated\s+with)"
    r"[^.\n]{0,60}[Ll]iquid\s+[Ww]hite"
    r"|[Ll]iquid\s+[Ww]hite[^.\n]{0,40}"
    r"(?:base|foundation|ground|undercoat|coating|treatment|"
    r"across the entire canvas|over the entire canvas|throughout the canvas)",
    re.I)

# Phrases that turn a Liquid White mention into a correct statement.
NEGATED = re.compile(
    r"(?:\bno\b|\bnot\b|without|instead\s+of|rather\s+than|never|absence\s+of|"
    r"avoided|in\s+place\s+of)[^.\n]{0,60}[Ll]iquid\s+[Ww]hite", re.I)

# Vocabulary that shows the entry already knows the ground is dark.
DARK_VOCAB = re.compile(
    r"black gesso|dark ground|black ground|black canvas|dark canvas|toned canvas|"
    r"liquid black|dark base|dark underpainting|dark foundation|gessoed|"
    r"dark-toned|dark toned|black base", re.I)

GROUND_PROSE = {
    "Black Gesso": (
        "**Black gesso** brushed over the canvas and allowed to **dry completely** before any "
        "oil is applied. This is a dry acrylic ground, not a wet one: the oils above it cannot "
        "be pulled back into it, and every light value in the painting has to be added rather "
        "than lifted."),
    "Liquid Black": (
        "**Liquid Black** worked thin into the canvas as a **wet** black ground. Unlike dried "
        "gesso it stays in contact with the oils laid over it, so darks can be pulled back "
        "into the ground and edges softened into it."),
}

CLOSER = {
    "Black Gesso": (
        "The black ground carries the value structure of the whole painting. Read the light in "
        "this entry as light recovered from darkness, not as shadow laid over white."),
    "Liquid Black": (
        "The wet black ground is what keeps the darks deep without mixing them muddy, and what "
        "lets the lit passages be pulled straight out of the ground."),
}


GROUND_TERM = {
    "Black Gesso": re.compile(r"black\s+gesso|gessoed", re.I),
    "Liquid Black": re.compile(r"liquid\s+black", re.I),
}


def section8_is_wrong(body: str, ground: str) -> str | None:
    """Return a reason string if Section 8 needs replacing, else None.

    The bar for replacing is deliberately high: the section has to fail to name the
    actual ground. A section that names it is kept even when it also mentions Liquid
    White, because those are usually right — Liquid White used for a sky band or a
    highlight over a black ground is a real thing Bob does, and the hand-written
    sections that describe it carry detail no template can reconstruct. Those are
    reported by lint_index.py for human adjudication instead.
    """
    if GROUND_TERM[ground].search(body):
        return None
    if DARK_VOCAB.search(body):
        return "dark ground implied but %s never named" % ground
    for m in LW.finditer(body):
        window = body[max(0, m.start() - 110):m.end() + 70]
        if NEGATED.search(window):
            continue
        if LW_GROUND.search(window):
            return "asserts a Liquid White ground"
    return "no ground stated"


def section8(ground, clear, paper, underpainting, had_lw) -> str:
    lines = ["## 8. Initial Canvas Treatment", "", "- " + GROUND_PROSE[ground]]
    if clear:
        lines.append("- **Liquid Clear** applied over the ground, giving a wet, transparent "
                     "working surface without lightening it. No Liquid White is used as a base.")
    else:
        lines.append("- No Liquid Clear and no Liquid White base — the oils are carried thin "
                     "directly over the ground.")
    if paper:
        lines.append("- **Contact paper** cut to shape and applied as a mask, so the area it "
                     "covers stays clean while the surround is painted, and is lifted before "
                     "that area is worked.")
    else:
        lines.append("- No contact paper and no masking.")
    if underpainting:
        lines.append("- **Secondary tone:** this episode carries the `Underpainting` tag, so a "
                     "transparent colour was laid over the ground before painting began. Its "
                     "value is in no dataset — Bob names it aloud in the opening minute and it "
                     "is invisible in the finished painting. Not yet recovered for this "
                     "episode; see `canvas_preparation.secondary_tone` below.")
    lines += ["", CLOSER[ground], "",
              "> Section 8 is template-filled from the CSV one-hot columns "
              "(`scripts/fix_ground.py`), not generated from the image."]
    if had_lw:
        lines.append("> The text it replaced named the wrong ground for this episode. "
                     "See `artifacts/ground_fixed.csv` for what it said.")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=".cache/bob_ross_paintings.csv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report")
    args = ap.parse_args()

    truth = {}
    for row in csv.DictReader(open(args.csv, encoding="utf-8")):
        try:
            tags = ast.literal_eval(row["tags"]) if row.get("tags") else []
        except (ValueError, SyntaxError):
            tags = []
        truth[(int(row["season"]), int(row["episode"]))] = (row, tags)

    changed, rows = 0, []
    for path in sorted(glob.glob(os.path.join(args.root, "season-*", "s[0-9]*.md"))):
        m = FILE_RE.search(os.path.basename(path))
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        if key not in truth:
            continue
        row, tags = truth[key]
        gesso, lblack = row["Black_Gesso"] == "1", row["Liquid_Black"] == "1"
        if not (gesso or lblack):
            continue
        ground = "Black Gesso" if gesso else "Liquid Black"

        text = open(path, encoding="utf-8").read()
        start = text.find("## 8. Initial Canvas Treatment")
        if start < 0:
            rows.append([os.path.relpath(path, args.root).replace(os.sep, "/"),
                         "S%02dE%02d" % key, ground, "SKIPPED - no section 8"])
            continue
        # Section 8 runs to the metadata fence, or to a '---' rule before it.
        end = text.find("\n```yaml", start)
        end = len(text) if end < 0 else end
        rule = text.rfind("\n---\n", start, end)
        end = rule if rule > start else end
        body = text[start:end]

        # A hand-adjudicated section that quotes the episode narration is better than
        # anything this script can write. Leave it alone.
        if "Recovered from the episode narration" in body:
            continue

        reason = section8_is_wrong(body, ground)
        if reason is None:
            continue

        new = section8(ground, row["Liquid_Clear"] == "1", "Contact Paper" in tags,
                       "Underpainting" in tags, bool(LW.search(body)))
        rows.append([os.path.relpath(path, args.root).replace(os.sep, "/"),
                     "S%02dE%02d" % key, ground, reason])
        changed += 1
        if not args.check:
            open(path, "w", encoding="utf-8", newline="").write(
                text[:start] + new + text[end:])

    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["file", "episode", "csv_ground", "reason"])
            w.writerows(rows)
        print(f"report: {args.report}", file=sys.stderr)
    print(f"{'would rewrite' if args.check else 'rewrote'}: {changed} sections", file=sys.stderr)


if __name__ == "__main__":
    main()
