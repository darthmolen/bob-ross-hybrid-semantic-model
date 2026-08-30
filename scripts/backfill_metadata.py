#!/usr/bin/env python3
"""
backfill_metadata.py — give every entry a metadata block.

Seasons 7 and 8 were generated before the metadata block existed, so 25 entries carry
prose only: no episode number, no painting_index, no colors, no canvas_preparation.
They are invisible to every script in this directory and to any structured query.

Everything factual comes from the CSV. The five identity tags are lifted out of the
prose, which already states them — in one of two formats, since the two generation
passes disagreed:

    Palette identity: **Dawn mist with warm earthen accents**
    **Lighting Type: Soft Diffused Overcast**

A tag that cannot be found is left out rather than invented. `searchable_features` is
never generated here: it has to answer to what someone remembers seeing, and that comes
from the image, not from a regex.

    python scripts/backfill_metadata.py --check
    python scripts/backfill_metadata.py
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

# "Palette identity: **value**"  and  "**Palette Identity: value**"
LABELS = {
    "composition_archetype": ["composition archetype", "compositional archetype", "archetype"],
    "palette_identity": ["palette identity"],
    "depth_style": ["depth style"],
    "lighting_type": ["lighting type", "lighting"],
    "motion_profile": ["motion profile", "compositional flow"],
}


def find_label(prose: str, names: list[str]) -> str | None:
    for name in names:
        n = re.escape(name)
        for pat in (rf"(?i){n}\s*:\s*\*\*(.+?)\*\*",
                    rf"(?i)\*\*{n}\s*:\s*(.+?)\*\*"):
            m = re.search(pat, prose)
            if m:
                val = " ".join(m.group(1).split()).strip(' .*"')
                if val:
                    return val
    return None


def ground_of(row, tags):
    if row.get("Black_Gesso") == "1":
        ground = "Black Gesso"
    elif row.get("Liquid_Black") == "1":
        ground = "Liquid Black"
    else:
        ground = "Liquid White"
    return (ground, row.get("Liquid_Clear") == "1",
            ground == "Liquid White", "Contact Paper" in tags)


YEARS = {7: 1986, 8: 1986}


def block(row, tags, cols, prose, season, episode) -> str:
    out = ["", "---", "", "## Metadata", "", "```yaml", "tags:"]
    found = 0
    for key, names in LABELS.items():
        val = find_label(prose, names)
        if val:
            out.append(f'  {key}: "{val}"')
            found += 1
    if not found:
        out.append('  # no identity labels found in the prose')
    ground, clear, white, paper = ground_of(row, tags)
    out += [
        "",
        "searchable_features:",
        "  # TODO — write from the painting: shape, colour and position, plus lay",
        "  # synonyms. See TEMPLATE.md. Not generated, because a regex over the prose",
        "  # reproduces the prose's vocabulary, which is the thing that fails at retrieval.",
        "",
        "episode:",
        f"  season: {season}",
        f"  episode: {episode}",
        f'  title: "{row["painting_title"]}"',
        f"  year: {YEARS.get(season, '')}".rstrip(),
        f"  painting_index: {row['painting_index']}",
        f'  youtube_url: "{row["youtube_src"]}"',
        "",
        "canvas_preparation:",
        f'  ground: "{ground}"',
        "  secondary_tone: null",
        f"  liquid_clear: {str(clear).lower()}",
        f"  liquid_white: {str(white).lower()}",
        f"  contact_paper: {str(paper).lower()}",
        "",
        "colors:",
    ]
    out += [f"  - {c}" for c in cols]
    out += ["```", ""]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=".cache/bob_ross_paintings.csv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    truth = {}
    for row in csv.DictReader(open(args.csv, encoding="utf-8")):
        try:
            tags = ast.literal_eval(row["tags"]) if row.get("tags") else []
            cols = ast.literal_eval(row["colors"]) if row.get("colors") else []
        except (ValueError, SyntaxError):
            tags, cols = [], []
        truth[(int(row["season"]), int(row["episode"]))] = (row, tags, cols)

    added = 0
    for path in sorted(glob.glob(os.path.join(args.root, "season-*", "s[0-9]*.md"))):
        m = FILE_RE.search(os.path.basename(path))
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        if key not in truth:
            continue
        text = open(path, encoding="utf-8").read()
        if "```yaml" in text:
            continue
        row, tags, cols = truth[key]
        new = text.rstrip("\n") + "\n" + block(row, tags, cols, text, *key)
        rel = os.path.relpath(path, args.root).replace(os.sep, "/")
        print(f"  + {rel}", file=sys.stderr)
        added += 1
        if not args.check:
            open(path, "w", encoding="utf-8", newline="").write(new)

    print(f"{'would add' if args.check else 'added'}: {added} metadata blocks", file=sys.stderr)


if __name__ == "__main__":
    main()
