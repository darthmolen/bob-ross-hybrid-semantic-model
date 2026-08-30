#!/usr/bin/env python3
"""
fix_prep_prose.py — add the two preparation facts the prose kept dropping.

Two lint rules kept firing on entries whose ground was otherwise fine:

  clear-unstated   Liquid_Clear = 1 but Liquid Clear is never mentioned
  mask-unstated    tags include Contact Paper but no mask vocabulary appears

The Liquid Clear bullet is generic and generated from the CSV. The contact paper
bullets are not: the *shape* of the mask is the thing people actually remember and
search for — an oval, a triptych, a border, a tree escaping the frame — so each was
read off the painting and written by hand. A generated "contact paper was used" line
would satisfy the linter and help no one find anything.

Appends to Section 8. Idempotent.

    python scripts/fix_prep_prose.py --check
    python scripts/fix_prep_prose.py
"""

from __future__ import annotations

import argparse
import sys

CLEAR_BULLET = (
    "- **Liquid Clear** over the ground, giving a wet, transparent working surface "
    "without lightening it.")

CLEAR_FILES = [
    "season-05/s05e09-anatomy-of-a-wave.md",
    "season-10/s10e10-ocean-sunset.md",
    "season-11/s11e03-daisy-delight.md",
    "season-11/s11e11-golden-glow.md",
    "season-17/s17e05-country-time.md",
    "season-24/s24e13-snowbound-cabin.md",
    "season-27/s27e05-winter-at-the-farm.md",
    "season-27/s27e09-island-paradise.md",
    "season-28/s28e05-the-magic-of-fall.md",
    "season-29/s29e12-auroras-dance.md",
    "season-30/s30e05-a-copper-winter.md",
]

# Read off the painting, one at a time. The shape is the searchable fact.
MASK_BULLETS = {
    "season-08/s08e09-majestic-pine.md": (
        "- **Contact paper** masking an irregular rectangular panel with a stepped notch cut "
        "out of the lower right corner. The pine on the left is painted past the mask edge so "
        "its trunk and canopy break out of the frame onto the bare canvas."),
    "season-10/s10e11-triple-view.md": (
        "- **Contact paper** laid in two vertical strips, dividing the canvas into a "
        "**triptych** — three tall panels separated by clean white gaps, each carrying part of "
        "the same continuous landscape. The mask is lifted at the end and the gaps stay bare."),
    "season-14/s14e09-riverside-escape-oval.md": (
        "- **Contact paper** cut as an **oval** and burnished down, so the scene is painted "
        "only inside it. The birches on the left are carried past the oval edge and break out "
        "of the frame."),
    "season-17/s17e08-view-from-the-park.md": (
        "- **Contact paper** cut as a free-form **apple silhouette** — the Big Apple — masking "
        "the whole scene. The lettering **NEW YORK** runs vertically down the bare canvas on "
        "the right, outside the mask."),
    "season-20/s20e05-divine-elegance.md": (
        "- **Contact paper** masking a rectangular panel set inside a wide, even **border** of "
        "bare pale canvas on all four sides, giving the painting a mounted, matted look."),
    "season-21/s21e05-cabin-at-trails-end.md": (
        "- **Contact paper** cut as a large **oval** on a white ground. The trees at the upper "
        "right are painted past the oval edge and break out of the frame."),
    "season-29/s29e03-seasonal-progression.md": (
        "- **Contact paper** laid as vertical strips, splitting the canvas into panels divided "
        "by clean **vertical dividing lines** — a split canvas carrying the same scene across "
        "separate frames."),
}


def append_to_section8(text: str, bullet: str) -> str | None:
    """Insert a bullet at the end of Section 8's bullet list, or after its first
    paragraph if it has no bullets. Returns None if already present."""
    if bullet in text:
        return None
    start = text.find("## 8. Initial Canvas Treatment")
    if start < 0:
        return None
    end = text.find("\n```yaml", start)
    end = len(text) if end < 0 else end
    rule = text.rfind("\n---\n", start, end)
    end = rule if rule > start else end
    body = text[start:end]

    lines = body.rstrip("\n").split("\n")
    last_bullet = max((i for i, ln in enumerate(lines) if ln.startswith("- ")),
                      default=None)
    if last_bullet is None:
        lines.append("")
        lines.append(bullet)
    else:
        lines.insert(last_bullet + 1, bullet)
    return text[:start] + "\n".join(lines) + "\n" + text[end:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    jobs = [(p, CLEAR_BULLET) for p in CLEAR_FILES] + list(MASK_BULLETS.items())
    done = skipped = 0
    for path, bullet in jobs:
        text = open(path, encoding="utf-8").read()
        new = append_to_section8(text, bullet)
        if new is None:
            skipped += 1
            continue
        done += 1
        if not args.check:
            open(path, "w", encoding="utf-8", newline="").write(new)

    verb = "would append" if args.check else "appended"
    print(f"{verb}: {done}   already present: {skipped}", file=sys.stderr)


if __name__ == "__main__":
    main()
