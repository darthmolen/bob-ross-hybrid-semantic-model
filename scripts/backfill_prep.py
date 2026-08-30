#!/usr/bin/env python3
"""
backfill_prep.py — write the `canvas_preparation` block into every episode entry.

The `ground` field is deterministic: it comes straight from the CSV one-hot columns
and the `Contact Paper` tag. It is never generated from the image, because a vision
pass cannot tell a black gesso ground from very dark paint over Liquid White and
falls back on the modal answer — wrong on exactly the episodes that matter.

`secondary_tone` is NOT deterministic. It is the transparent colour laid over the
Clear before painting starts; it is spoken aloud in the opening minute and invisible
in the finished painting. This script never invents one, and never overwrites one
that is already in the file. Use extract_prep.py + apply_tone.py for that field.

    python scripts/backfill_prep.py --csv .cache/bob_ross_paintings.csv
    python scripts/backfill_prep.py --check      # report only, write nothing
"""

from __future__ import annotations

import argparse
import ast
import csv
import glob
import os
import re
import sys

BLOCK_RE = re.compile(r"(?m)^canvas_preparation:\n(?:[ \t]+[^\n]*\n)*")
FILE_RE = re.compile(r"s(\d{2})e(\d{2})-")
KEY_RE = re.compile(r"^  (\w+):(.*)$")
KNOWN = ("ground", "secondary_tone", "liquid_clear", "liquid_white", "contact_paper")
OVERRIDE_KEY = "csv_override"   # set true to freeze a hand-adjudicated block


def ground_of(row: dict, tags: list) -> tuple[str, bool, bool, bool]:
    """Return (ground, liquid_clear, liquid_white, contact_paper) from the CSV alone."""
    if row.get("Black_Gesso") == "1":
        ground = "Black Gesso"
    elif row.get("Liquid_Black") == "1":
        ground = "Liquid Black"
    else:
        ground = "Liquid White"
    return (ground,
            row.get("Liquid_Clear") == "1",
            ground == "Liquid White",
            "Contact Paper" in tags)


def load_csv(path: str) -> dict:
    out = {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                tags = ast.literal_eval(row["tags"]) if row.get("tags") else []
            except (ValueError, SyntaxError):
                tags = []
            out[(int(row["season"]), int(row["episode"]))] = (row, tags)
    return out


def split_keys(block: str) -> dict:
    """Split a canvas_preparation block into {key: raw value text}, keeping
    multi-line scalars intact."""
    body = block.split("\n", 1)[1] if "\n" in block else ""
    out, key, buf = {}, None, []
    for line in body.split("\n"):
        m = KEY_RE.match(line)
        if m:
            if key is not None:
                out[key] = "\n".join(buf)
            key, buf = m.group(1), [m.group(2)]
        elif key is not None:
            buf.append(line)
    if key is not None:
        out[key] = "\n".join(buf)
    return {k: v.rstrip("\n") for k, v in out.items()}


def existing_tone(block: str) -> str | None:
    """Preserve a hand-recovered secondary_tone, including multi-line scalars."""
    val = split_keys(block).get("secondary_tone")
    if val is None or val.strip() in ("", "null", "~"):
        return None
    return val


def extra_keys(block: str) -> str:
    """Preserve any hand-added keys the deterministic backfill does not own."""
    lines = [f"  {k}:{v}" for k, v in split_keys(block).items() if k not in KNOWN]
    return ("\n".join(lines) + "\n") if lines else ""


def render(ground, clear, white, paper, tone_raw, extra="") -> str:
    tone = tone_raw if tone_raw is not None else " null"
    return (f"canvas_preparation:\n"
            f"  ground: \"{ground}\"\n"
            f"  secondary_tone:{tone}\n"
            f"  liquid_clear: {str(clear).lower()}\n"
            f"  liquid_white: {str(white).lower()}\n"
            f"  contact_paper: {str(paper).lower()}\n"
            f"{extra}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=".cache/bob_ross_paintings.csv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    data = load_csv(args.csv)
    files = sorted(glob.glob(os.path.join(args.root, "season-*", "s[0-9]*.md")))

    wrote = skipped = kept_tone = no_meta = unmatched = overridden = 0
    for path in files:
        m = FILE_RE.search(os.path.basename(path))
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        if key not in data:
            print(f"  no CSV row: {path}", file=sys.stderr)
            unmatched += 1
            continue
        row, tags = data[key]
        ground, clear, white, paper = ground_of(row, tags)

        text = open(path, encoding="utf-8").read()
        if "```yaml" not in text:
            no_meta += 1
            continue

        old = BLOCK_RE.search(text)
        if old and split_keys(old.group(0)).get("csv_override", "").strip() == "true":
            # A hand-adjudicated block that deliberately departs from the CSV, normally
            # because the episode narration contradicts it. Leave it alone.
            overridden += 1
            continue
        tone = existing_tone(old.group(0)) if old else None
        extra = extra_keys(old.group(0)) if old else ""
        if tone is not None:
            kept_tone += 1
        block = render(ground, clear, white, paper, tone, extra)

        if old:
            new = text[:old.start()] + block + text[old.end():]
        else:
            # insert immediately before the colors list inside the yaml fence
            cm = re.search(r"(?m)^colors:\n", text)
            if not cm:
                no_meta += 1
                continue
            new = text[:cm.start()] + block + "\n" + text[cm.start():]

        if new == text:
            skipped += 1
            continue
        if not args.check:
            open(path, "w", encoding="utf-8", newline="").write(new)
        wrote += 1

    print(f"{'would write' if args.check else 'wrote'}: {wrote}", file=sys.stderr)
    print(f"unchanged: {skipped}   tones preserved: {kept_tone}   csv_override: {overridden}", file=sys.stderr)
    print(f"no metadata block: {no_meta}   no CSV row: {unmatched}", file=sys.stderr)


if __name__ == "__main__":
    main()
