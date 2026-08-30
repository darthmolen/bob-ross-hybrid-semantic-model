#!/usr/bin/env python3
"""
fix_colors.py — make every entry's `colors` list a subset of the CSV colors column.

Ground truth is `bob_ross_paintings.csv`. Where an entry lists a colour the CSV does not,
the entry invented it — most often Prussian Blue or Phthalo Green, the two most
"expected" Bob Ross colours, or Liquid White, which is a canvas treatment and never
belongs in the colours array.

This only ever REMOVES. It never adds a colour the entry did not claim, because the
CSV column is the full palette put out for the episode and not everything on the palette
reaches the canvas. Omissions are reported, not fixed.

    python scripts/fix_colors.py --check
    python scripts/fix_colors.py --report artifacts/colors_fixed.csv
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
LIST_RE = re.compile(r"(?m)^colors:\n((?:  - [^\n]*\n)*)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=".cache/bob_ross_paintings.csv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", help="write a CSV of every change")
    args = ap.parse_args()

    truth = {}
    for row in csv.DictReader(open(args.csv, encoding="utf-8")):
        try:
            cols = ast.literal_eval(row["colors"]) if row.get("colors") else []
        except (ValueError, SyntaxError):
            cols = []
        truth[(int(row["season"]), int(row["episode"]))] = cols

    changed, rows = 0, []
    for path in sorted(glob.glob(os.path.join(args.root, "season-*", "s[0-9]*.md"))):
        m = FILE_RE.search(os.path.basename(path))
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        if key not in truth:
            continue
        text = open(path, encoding="utf-8").read()
        lm = LIST_RE.search(text)
        if not lm:
            continue

        listed = [ln.strip()[2:].strip() for ln in lm.group(1).splitlines() if ln.strip()]
        valid = truth[key]
        kept = [c for c in listed if c in valid]
        dropped = [c for c in listed if c not in valid]
        missing = [c for c in valid if c not in kept]
        if not dropped:
            continue

        rel = os.path.relpath(path, args.root).replace(os.sep, "/")
        rows.append([rel, "S%02dE%02d" % key, "; ".join(dropped), "; ".join(missing)])
        changed += 1
        if args.check:
            continue
        block = "colors:\n" + "".join("  - %s\n" % c for c in kept)
        open(path, "w", encoding="utf-8", newline="").write(
            text[:lm.start()] + block + text[lm.end():])

    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["file", "episode", "removed_invented", "still_absent_from_entry"])
            w.writerows(rows)
        print(f"report: {args.report}", file=sys.stderr)

    print(f"{'would fix' if args.check else 'fixed'}: {changed} entries", file=sys.stderr)


if __name__ == "__main__":
    main()
