#!/usr/bin/env python3
"""
fix_prose_ground.py — repair the 21 hand-adjudicated Liquid White claims that survive
outside Section 8.

fix_ground.py owns Section 8 and only rewrites it wholesale. These are single sentences
and bullets in Sections 2, 6 and 8 that assert a Liquid White base for an episode whose
CSV ground is black. Each was read before being listed here, and each replacement names
the real ground while keeping whatever the original sentence was actually about.

Two further entries — S18E13 Rippling Waters and S21E01 Valley View — describe a *split*
ground, Liquid Black or Black Gesso on the lower canvas and Liquid White or Clear above.
That is a real technique the CSV one-hot columns cannot express, so those two are not
edited; they carry a `lint_exceptions` key instead.

Idempotent: a replacement that is already applied is skipped.

    python scripts/fix_prose_ground.py --check
    python scripts/fix_prose_ground.py
"""

from __future__ import annotations

import argparse
import sys

# (path, exact old text, replacement)
EDITS = [
    ("season-03/s03e08-night-light.md",
     "- **Liquid white or black foundation** allowing for dark nocturnal base with light emergence",
     "- **Dry black gesso foundation** giving the dark nocturnal base out of which the light emerges"),

    ("season-04/s04e12-autumn-days.md",
     "- Liquid White/Clear base enables smooth sky-to-mist gradient",
     "- Thin transparent colour over the dry black gesso ground carries the sky-to-mist gradient"),

    ("season-05/s05e10-the-windmill.md",
     "- Liquid White or Liquid Clear base allows color blending in sky",
     "- Sky colours scumbled thin over the dry black gesso ground, which darkens them as they thin out"),

    ("season-06/s06e01-blue-river.md",
     "- Liquid White base for smooth blending",
     "- Dry black gesso ground; blending done in thin oil over it rather than into a wet white base"),

    ("season-06/s06e05-secluded-forest.md",
     "- Liquid White or light blue base for atmospheric effect",
     "- Dry black gesso ground with a thin transparent blue over it for the atmospheric effect"),
    ("season-06/s06e05-secluded-forest.md",
     "- Liquid White base",
     "- Dry black gesso ground, no Liquid White"),

    ("season-06/s06e12-marshlands.md",
     "- Liquid White base for bright blending",
     "- Dry black gesso ground; the bright passages are built up over it, not blended out of white"),

    ("season-09/s09e13-mountain-hideaway.md",
     "- Liquid White base for bright, blendable foundation",
     "- Dry black gesso ground; the bright passages are added over it rather than lifted out of white"),

    ("season-13/s13e06-hidden-creek.md",
     "**Liquid White/Black base**: The canvas likely received a darker base treatment "
     "(possibly thinned Midnight Black or dark blue-green) to establish the overall cool, "
     "shadowed forest tone, with Liquid White reserved for areas requiring luminosity and "
     "atmospheric blending.",
     "**Black gesso base**: The canvas carries a dry black gesso ground, which establishes the "
     "cool, shadowed forest tone directly. Luminous passages are added on top of it; there is no "
     "Liquid White underneath them."),

    ("season-15/s15e10-forest-down-oval.md",
     "- Liquid White or Liquid Clear for the wet canvas base allowing seamless blending",
     "- Dry black gesso ground; blending done in thin oil over it, with no wet white base"),

    ("season-18/s18e07-golden-morning-mist.md",
     "- Liquid White or Liquid Clear base for extensive wet-on-wet blending",
     "- Dry black gesso ground; the wet-on-wet blending happens in the oil laid over it"),
    ("season-18/s18e07-golden-morning-mist.md",
     "- Liquid White base for smooth wet-on-wet blending",
     "- Dry black gesso ground, no Liquid White"),

    ("season-18/s18e09-seascape-fantasy.md",
     "- **Liquid White**: Applied as base for smooth wet-on-wet blending in sky and water",
     "- **Black gesso**: Applied as the ground and dried; sky and water are worked thin over it"),
    ("season-18/s18e09-seascape-fantasy.md",
     "A traditional Liquid White foundation enabling smooth atmospheric blending and luminous "
     "color transitions throughout the oceanscape.",
     "A dry black gesso foundation. The luminous colour transitions across this oceanscape are "
     "built up out of that dark ground rather than blended down into a white one."),

    ("season-19/s19e02-quiet-mountain-lake.md",
     "A classic Liquid White foundation enabling seamless sky-to-mountain transitions and smooth "
     "reflective water surfaces.",
     "A dry black gesso foundation with Liquid Clear over it. The Clear supplies the slip for the "
     "sky-to-mountain transitions and the reflective water without lightening the ground."),

    ("season-19/s19e08-scenic-seclusion.md",
     "- Liquid White base for blendable sky and atmospheric effects",
     "- Wet Liquid Black ground; sky and atmosphere are blended down into it"),

    ("season-19/s19e10-after-the-rain.md",
     "- Liquid White or Liquid Clear base for blending",
     "- Dry black gesso ground; blending done in thin oil directly over it"),

    ("season-25/s25e09-downstream-view.md",
     "- **Liquid White**: Applied across the entire canvas for smooth blending and wet-on-wet technique",
     "- **Black gesso**: Applied across the entire canvas and dried; the wet-on-wet work happens "
     "in the oil above it"),
    ("season-25/s25e09-downstream-view.md",
     "A traditional Liquid White foundation supporting bright, vibrant colors and seamless blending "
     "throughout the composition.",
     "A dry black gesso foundation. The bright colours read as vivid because they are the only "
     "light on an otherwise black canvas."),

    ("season-25/s25e11-fishermans-paradise.md",
     "- Selective application of Liquid White or Liquid Clear for atmospheric blending areas",
     "- Dry black gesso ground throughout; atmospheric passages thinned over it rather than "
     "floated on a wet white base"),

    ("season-27/s27e01-twilight-beauty.md",
     "- **Liquid White**: Applied to upper canvas for sky blending and smooth color transitions",
     "- **Black gesso**: The ground for the whole canvas, applied and dried before any oil"),
    ("season-27/s27e01-twilight-beauty.md",
     "A Liquid White base with contact paper oval masking and dark vignette framing, allowing for "
     "both smooth sky gradients and the dramatic oval presentation style.",
     "A dry black gesso ground with Liquid Clear over it, a contact paper oval mask, and dark "
     "gesso framing around the outer edge — giving both the smooth sky gradients inside the oval "
     "and the dramatic vignette presentation."),

    ("season-27/s27e02-anglers-haven.md",
     "- Liquid White base for sky and mountain highlights",
     "- Wet Liquid Black ground under Liquid Clear; sky and mountain highlights are pulled out of it"),

    ("season-27/s27e11-splendor-of-a-snowy-winter.md",
     "- Liquid White base for smooth blending in sky and snow",
     "- Wet Liquid Black ground under Liquid Clear; sky and snow are blended over that, not over white"),

    ("season-27/s27e12-forest-river.md",
     "- Liquid White or Liquid Clear base for the luminous background effect",
     "- Liquid Clear over a dry black gesso ground gives the luminous background effect"),

    ("season-31/s31e10-balmy-beach.md",
     "A traditional Liquid White base across the entire canvas, allowing for seamless wet-on-wet "
     "blending of the complex sunset gradient and smooth atmospheric color",
     "A dry black gesso ground with Liquid Clear over it, allowing seamless wet-on-wet blending of "
     "the complex sunset gradient and smooth atmospheric color"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    applied = missing = already = 0
    for path, old, new in EDITS:
        text = open(path, encoding="utf-8").read()
        if new in text:
            already += 1
            continue
        if old not in text:
            print(f"  NOT FOUND in {path}: {old[:70]}...", file=sys.stderr)
            missing += 1
            continue
        applied += 1
        if not args.check:
            open(path, "w", encoding="utf-8", newline="").write(text.replace(old, new, 1))

    verb = "would apply" if args.check else "applied"
    print(f"{verb}: {applied}   already done: {already}   not found: {missing}",
          file=sys.stderr)
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
