#!/usr/bin/env python3
"""
lint_index.py — check every episode entry against the CSV ground truth.

Four bad entries were found by hand. This finds the rest in about a second. Every rule
here exists because a real entry broke it.

    python scripts/lint_index.py                    # all rules, all seasons
    python scripts/lint_index.py --season 16
    python scripts/lint_index.py --rule ground-contradiction
    python scripts/lint_index.py --quiet            # counts only

Exit code is 1 if anything failed, so it drops straight into CI.
"""

from __future__ import annotations

import argparse
import ast
import csv
import glob
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_ground   # noqa: E402  — shared ground-claim predicate

FILE_RE = re.compile(r"s(\d{2})e(\d{2})-")

GESSO_VOCAB = re.compile(
    r"black gesso|dark ground|black ground|black canvas|dark canvas|toned canvas|"
    r"dark background|dark base|dark underpainting|dark toned|dark-toned|gessoed|"
    r"liquid black|black base|acrylic ground|dry acrylic", re.I)
MASK_VOCAB = re.compile(
    r"contact paper|mask|masked|masking|shaped|vignette|border|stencil|taped|tape\b|"
    r"cut the shape|frame line", re.I)
CLEAR_VOCAB = re.compile(r"liquid clear", re.I)
LIQUID_WHITE = re.compile(r"liquid white", re.I)


def prose_of(text: str) -> str:
    """Everything outside the trailing yaml fence."""
    return text.split("```yaml")[0]


def yaml_of(text: str) -> str:
    parts = text.split("```yaml")
    return parts[1].split("```")[0] if len(parts) > 1 else ""


def listed_colors(block: str) -> list[str]:
    m = re.search(r"(?m)^colors:\n((?:  - .*\n)*)", block)
    if not m:
        return []
    return [ln.strip()[2:].strip() for ln in m.group(1).splitlines() if ln.strip()]


def scalar(block: str, key: str) -> str | None:
    m = re.search(rf"(?m)^(?:  |)({re.escape(key)}):[ \t]*(.*)$", block)
    return m.group(2).strip().strip('"') if m else None


def load_csv(path: str) -> dict:
    out = {}
    for row in csv.DictReader(open(path, encoding="utf-8")):
        try:
            tags = ast.literal_eval(row["tags"]) if row.get("tags") else []
            cols = ast.literal_eval(row["colors"]) if row.get("colors") else []
        except (ValueError, SyntaxError):
            tags, cols = [], []
        out[(int(row["season"]), int(row["episode"]))] = (row, tags, cols)
    return out


def exceptions(block: str) -> set[str]:
    """Rules this entry has been adjudicated out of, e.g.

        lint_exceptions:
          - rule: ground-contradiction
            reason: split ground, Liquid Black below and Liquid White above

    Use sparingly and always with a reason. It exists for facts the CSV one-hot
    columns cannot express, not for entries nobody wants to fix.
    """
    m = re.search(r"(?ms)^lint_exceptions:\n((?:\s+.*\n)*)", block)
    if not m:
        return set()
    return set(re.findall(r"(?m)^\s*-?\s*rule:\s*(\S+)", m.group(1)))


def check(path, row, tags, cols, text) -> list[tuple[str, str]]:
    """Return a list of (rule, message)."""
    out = []
    prose, block = prose_of(text), yaml_of(text)
    waived = exceptions(block)
    gesso = row.get("Black_Gesso") == "1"
    lblack = row.get("Liquid_Black") == "1"
    lclear = row.get("Liquid_Clear") == "1"
    paper = "Contact Paper" in tags
    override = scalar(block, "csv_override") == "true"

    # --- rule 1: a black ground must be described, and must not be called Liquid White.
    # The Liquid White check reuses fix_ground's predicate so the linter and the fixer
    # never disagree: a mention that is negated ("black gesso instead of Liquid White")
    # or that describes a highlight rather than a base is correct and is not flagged.
    if gesso or lblack:
        ground_name = "Black Gesso" if gesso else "Liquid Black"
        if not GESSO_VOCAB.search(prose):
            out.append(("ground-unstated",
                        f"CSV ground is {ground_name} but the prose never says so"))
        if not override:
            for m in fix_ground.LW.finditer(prose):
                window = prose[max(0, m.start() - 110):m.end() + 70]
                if fix_ground.NEGATED.search(window):
                    continue
                if fix_ground.LW_GROUND.search(window):
                    out.append(("ground-contradiction",
                                f"CSV ground is {ground_name} but the prose asserts a "
                                f"Liquid White base: ...{window.strip()[:120]}..."))
                    break

    # --- rule 2: a contact-paper episode must describe the mask
    if paper and not MASK_VOCAB.search(prose):
        out.append(("mask-unstated",
                    "tags include Contact Paper but the prose has no mask vocabulary"))

    # --- rule 3: Liquid Clear must appear where the CSV says it was used
    if lclear and not CLEAR_VOCAB.search(prose):
        out.append(("clear-unstated", "Liquid_Clear = 1 but Liquid Clear is never mentioned"))

    # --- rule 4: colors must be a subset of the CSV colors column
    listed = listed_colors(block)
    if not listed:
        out.append(("colors-missing", "no colors list in the metadata block"))
    else:
        invented = [c for c in listed if c not in cols]
        if invented:
            out.append(("colors-invented",
                        f"not on the CSV palette: {', '.join(sorted(invented))}"))

    # --- rule 5: painting_index must match the CSV
    idx = scalar(block, "painting_index")
    if idx is None:
        out.append(("index-missing", "no painting_index in the metadata block"))
    elif idx != row["painting_index"]:
        out.append(("index-mismatch",
                    f"entry says {idx}, CSV says {row['painting_index']}"))

    # --- rule 6: title must match the CSV
    title = scalar(block, "title")
    if title is None:
        out.append(("title-missing", "no title in the metadata block"))
    elif title.strip().lower() != row["painting_title"].strip().lower():
        out.append(("title-mismatch",
                    f"entry says {title!r}, CSV says {row['painting_title']!r}"))

    # --- rule 7: the canvas_preparation block must exist and agree with the CSV
    if not re.search(r"(?m)^canvas_preparation:", block):
        out.append(("prep-missing", "no canvas_preparation block"))
    elif not override:
        want_ground = "Black Gesso" if gesso else "Liquid Black" if lblack else "Liquid White"
        got = scalar(block, "ground")
        if got != want_ground:
            out.append(("prep-ground", f"ground is {got!r}, CSV implies {want_ground!r}"))
        for key, want in (("liquid_clear", lclear), ("contact_paper", paper)):
            got = scalar(block, key)
            if got != str(want).lower():
                out.append((f"prep-{key.replace('_', '-')}",
                            f"{key} is {got}, CSV implies {str(want).lower()}"))

    # --- rule 8: searchable_features, the retrieval half. A block with only a TODO
    # comment in it does not count — an empty list retrieves exactly nothing.
    fm = re.search(r"(?m)^searchable_features:\n((?:(?:  [-#].*)?\n)*)", block)
    if not fm:
        out.append(("features-missing", "no searchable_features block"))
    elif not [ln for ln in fm.group(1).splitlines() if ln.strip().startswith("- ")]:
        out.append(("features-empty", "searchable_features has no entries"))

    return [(rule, msg) for rule, msg in out if rule not in waived]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=".cache/bob_ross_paintings.csv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--season", type=int)
    ap.add_argument("--rule", action="append", help="only report these rules")
    ap.add_argument("--quiet", action="store_true", help="counts only")
    args = ap.parse_args()

    data = load_csv(args.csv)
    files = sorted(glob.glob(os.path.join(args.root, "season-*", "s[0-9]*.md")))

    tally, failing, checked = Counter(), set(), 0
    for path in files:
        m = FILE_RE.search(os.path.basename(path))
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        if args.season and key[0] != args.season:
            continue
        if key not in data:
            print(f"{path}: no CSV row")
            continue
        checked += 1
        row, tags, cols = data[key]
        text = open(path, encoding="utf-8").read()

        for rule, msg in check(path, row, tags, cols, text):
            if args.rule and rule not in args.rule:
                continue
            tally[rule] += 1
            failing.add(path)
            if not args.quiet:
                rel = os.path.relpath(path, args.root).replace(os.sep, "/")
                print(f"{rel}: [{rule}] {msg}")

    print(f"\n{checked} entries checked, {len(failing)} failing", file=sys.stderr)
    for rule, n in tally.most_common():
        print(f"  {n:>4}  {rule}", file=sys.stderr)
    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    main()
