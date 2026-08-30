# Correction worklist

Pending changes to the semantic index, recovered from chat sessions that were never
persisted to the repository. Each item names the exact file and the exact change.

Ground truth throughout is `bob_ross_paintings.csv` (twoinchbrush) via `MASTER_DATA.md`.
Where a semantic entry disagrees with those columns, **the entry is wrong**, not the CSV.

Tick items off as they land. Delete the file when the queue is empty.

> **Status.** A–C and E are done. D is blocked on YouTube (see below). F is the only
> substantial work left: 396 of 403 entries still have no `searchable_features`.
> Run `python scripts/lint_index.py` for the live queue.

---

## A. Drop-in replacements — ready to apply

These two files are complete rewrites. Replace wholesale.

- [x] `season-17/s17e11-morning-walk.md` ← `s17e11-morning-walk.md`
- [x] `season-28/s28e04-golden-rays-of-sunshine.md` ← `s28e04-golden-rays-of-sunshine.md`

Both contain first-hand observations made while watching the episodes that exist in no
dataset. Do not regenerate them from the CSV — that would lose the content.

**S17E11 Morning Walk** — two figures (red shirt, gold shirt), not one. Five straight
birch trunks forming a colonnade. Warm-cool trunk modelling, Phthalo Blue on the shadow
side. Canvas is **Black Gesso**, not Liquid White.

> An earlier correction of this file fixed the figures but left Section 8 saying
> "Liquid White base." The foundation error survived a correction pass. Worth assuming
> that happened elsewhere too.

That assumption was right. The lint found **81** entries asserting Liquid White over a
CSV black ground, not four. See E.

The intake file's guess of "transparent violet (unverified)" for the secondary tone has
since been replaced with what Bob actually says on air: a transparent **lavender**,
Alizarin Crimson with a little Phthalo Blue, over a small amount of Liquid Clear. See D.

**S28E04 Golden Rays of Sunshine** — dual-canvas teaching episode. Bob builds the gesso
underpainting live, swaps to a dried twin, glazes Indian Yellow low and Phthalo Blue high
over Liquid Clear, pulls Titanium White rays, then finishes with transparent Alizarin
Crimson and Sap Green over the central path.

---

## B. Confirmed bad entries — need regeneration in repo

Four entries where the prose contradicts or omits the defining feature. All four were
found by hand; assume there are more.

- [x] **`season-16/s16e08-high-tide.md`** — S16E08, index 91
  - Rewritten. Black gesso ground, no Liquid Clear, two palm trunks, colours corrected
    to the CSV set, `searchable_features` added.

- [x] **`season-30/s30e02-woodgrain-view.md`** — S30E02, index 387
  - Rewritten. The painting is a rounded-corner rectangular panel masked out of a painted
    woodgrain board, with a knothole upper right, a bare birch on the panel edge and two
    cardinals on a fence rail breaking the frame. `searchable_features` added.

- [x] **`season-17/s17e12-natures-splendor.md`** — S17E12, index 82
  - Black gesso ground added to Section 6, Section 8 and the colours list.

- [x] **`season-27/s27e04-wilderness-falls.md`** — S27E04, index 350
  - Rewritten with Liquid Black + Liquid Clear and the water features restored.
  - The "wrong image" theory was wrong. `painting350.png` matches both twoinchbrush and
    the jwilber repo byte for byte. It is a **mid-episode still**: the mountain and mist
    are finished, the frame is cropped above the foreground, and the falls sit below its
    lower edge. Only the pale channel descending between the foothills is visible. The
    entry now says so explicitly rather than describing "no visible water features."

### Also found and fixed while here

- **`season-13/s13e13-winter-mountain.md`** carried S12E13's title. Index 136 is
  **Lost Lake**. Renamed to `s13e13-lost-lake.md`, title corrected, and the invented
  "circular vignette" removed — painting 136 runs to all four edges and has no mask.
  `INDEX.md` and `season-13/SOURCE_IMAGES.md` updated.
- **Seasons 7 and 8** (25 entries) had no metadata block at all — no episode number, no
  `painting_index`, no colours. Backfilled by `scripts/backfill_metadata.py`.
- Five entries in seasons 10 and 13 had a metadata block with no opening ` ```yaml `
  fence, so every script skipped them silently. Fixed.

---

## C. Schema change — split the preparation field

Section 8 currently conflates two independent facts. Split them everywhere:

- **Ground** — Black Gesso / Liquid Black / Liquid White / Contact Paper.
  Deterministic, already in the CSV. Should be template-filled from the one-hot
  columns, never generated from the image. A vision pass cannot distinguish a black
  gesso ground from very dark paint over Liquid White, so it falls back on the modal
  answer (Liquid White) and is wrong exactly on the episodes that matter.

- **Secondary tone** — the transparent colour laid over the Clear before painting
  begins. Flagged by the `Underpainting` tag (65 of 403 episodes), but the *value*
  is not in any dataset. It is spoken aloud in the opening minute of the episode and
  is invisible in the finished painting.

```yaml
canvas_preparation:
  ground: "Black Gesso"
  secondary_tone: "Phthalo Blue"
  liquid_clear: true
  liquid_white: false
  contact_paper: false
```

- [x] Add `canvas_preparation` to the template — `TEMPLATE.md` now documents the split,
      `searchable_features`, and the colours-are-a-subset-of-the-CSV rule
- [x] Backfill `ground` for all 403 from the CSV one-hot columns —
      `scripts/backfill_prep.py`, idempotent, 401 entries carry the block
- [~] Backfill `secondary_tone` from transcripts — 5 recovered, 60 blocked. See D

Two escape hatches were needed and are honoured by the tooling:

- `csv_override: true` inside `canvas_preparation` freezes a block the narration
  contradicts, so `backfill_prep.py` will not revert it. Used on S17E11 (Liquid Clear
  used on air, `Liquid_Clear = 0` in the CSV) and S07E03.
- `lint_exceptions:` with a `rule:` and a `reason:` waives a lint rule for facts the
  one-hot columns cannot express. Used on the two **split-ground** episodes, S18E13 and
  S21E01, where black covers the lower canvas and white or clear the upper.

---

## D. Recover the secondary tone from captions

`../scripts/extract_prep.py` pulls the opening ~150 seconds of YouTube captions for each episode
and extracts what Bob actually says about the preparation, then diffs it against the
dataset.

```
pip install youtube-transcript-api
python extract_prep.py --underpainting-only    # the 65 that matter, start here
python extract_prep.py                          # all 403 once it looks right
```

- [~] Run on the 65 underpainting episodes — **5 recovered, 60 blocked by YouTube**
- [x] Adjudicate, add caption variants as needed
- [ ] Run on all 403
- [~] Backfill `secondary_tone` — done for all 5 that came back

### What came back

| episode | ground heard | secondary tone heard |
|---|---|---|
| S04E07 Cabin in the Woods | black canvas | **Phthalo Blue + Sap Green**, thin coat |
| S07E03 Evergreens at Sunset | dried **acrylic yellow**, then Liquid Black | — (inverted: the tone is *under* the black) |
| S11E10 Sunset over the Waves | black gesso, dried | **Indian Yellow** sky, **Alizarin Crimson** below |
| S12E08 Evening Waterfall | black gesso, dried | **Phthalo Blue + Sap Green**, left wet |
| S17E11 Morning Walk | black gesso + Liquid Clear | **lavender** = Alizarin Crimson + a little Phthalo Blue |

All five are now in their entries, in Section 8, with the quote that produced them and a
`secondary_tone_source` field. Two produced new ground truth:

- **S07E03** uses a preparation that appears nowhere else and that the CSV schema cannot
  represent: an opaque **acrylic yellow ground**, dried, with a **taped circle** masking
  what becomes the sun, and Liquid Black brushed over the top. The sun in that painting
  was never painted — it is bare ground where the tape was.
- **S17E11** uses Liquid Clear, which the CSV denies.

### Why the other 60 failed

YouTube IP-blocks bulk transcript requests, in practice after about six. The first run
came back 60/65 `no-captions`, and **all 60 were false** — the script was caching
transient block failures as "this video has no captions", permanently. That cache is
purged and the bug is fixed: `Blocked` is now a distinct exception, never cached, with
exponential backoff and a summary line that says a blocked run is not a result.

To finish D: rerun from an unblocked IP, or route through a residential proxy per the
`youtube-transcript-api` README on IP bans. Transcripts already fetched are cached, so
reruns only cost the missing ones.

The colour-variants table in the script is the maintenance surface. Auto-captions render
"Phthalo" as "thalo", "gesso" as "jesso", "Alizarin Crimson" as "lizard in crimson".
Every variant added improves all 403 retroactively, since transcripts are cached.
Variants added from the five recovered transcripts:

- `black canvas` / `black canvases` — Bob says "black gesso" once and then never again
- `duct tape`, `masking tape`, `piece of tape`, `made a circle` — the tape is the
  workshop reality behind the `Contact Paper` tag
- `acrylic … paint`, `painted it yellow` — the S07E03 ground, new to the vocabulary
- prep cues: `transparent color`, `layers of color`, `even coat`, `on top of that`,
  `onto that`, `mixture of`, `still wet`

The `black canvas` variant alone lifted S04E07 from a false `gesso-not-heard` flag to
high confidence.

---

## E. Lint pass — catch the rest automatically

`scripts/lint_index.py`. Exits 1 on any failure, so it drops into CI.

- [x] `Black_Gesso = 1` → text must contain gesso / dark ground vocabulary,
      and must **not** contain "Liquid White"
- [x] `Contact Paper` in tags → must contain mask / shaped / vignette / border vocabulary
- [x] `Liquid_Clear = 1` → must appear in technique or canvas treatment
- [x] Colours in the entry must be a **subset** of the CSV colours column
- [x] `painting_index` in the entry must match the CSV for that season/episode
- [x] Title in the entry must match the CSV title
- [x] plus: `canvas_preparation` present and agreeing with the CSV;
      `searchable_features` present **and non-empty**

The Liquid White rule needed care. A flat "prose must not contain Liquid White" flagged
81 entries, but around a third of those were right — "black gesso **instead of** Liquid
White" is correct, and Liquid White used for a sky band or a highlight over a black
ground is a real thing Bob does. The rule now looks for an un-negated claim that Liquid
White is the *ground*, and `lint_index.py` imports that predicate from `fix_ground.py`
so the linter and the fixer can never disagree.

### What the first clean run found, and what fixed it

| rule | before | after | fixed by |
|---|---:|---:|---|
| `colors-invented` | 214 | 0 | `scripts/fix_colors.py` |
| `ground-contradiction` | 81 | 0 | `fix_ground.py` (76) + `fix_prose_ground.py` (26 edits) + 2 waivers |
| `ground-unstated` | 42 | 0 | `fix_ground.py` |
| `clear-unstated` | 25 | 0 | `fix_prep_prose.py` |
| `colors/index/title/prep-missing` | 25 each | 0 | `backfill_metadata.py` |
| `mask-unstated` | 8 | 0 | `fix_prep_prose.py`, shapes read off the paintings |
| `title-mismatch` | 1 | 0 | S13E13 renamed to Lost Lake |
| `features-missing` + `features-empty` | 396 | 396 | **open — see F** |

The invented colours were not random. Across 214 entries the top three were **Prussian
Blue (81)**, **Phthalo Green (52)** and **Liquid White (41)** — the two most
stereotypically Bob Ross pigments, plus a canvas treatment that is not a pigment at all.
The generator was reaching for what a Bob Ross palette is *supposed* to look like.

`fix_ground.py` only replaces Section 8 when that section fails to name the real ground.
Sections that already say "black gesso applied and dried, Alizarin Crimson over it
instead of Liquid White" are better than any template and are left alone. Reports of
every change are in `artifacts/`.

---

## F. Searchable features — the retrieval half

**This is the remaining work: 396 of 403 entries have no `searchable_features`.**

Twenty paintings have been successfully identified across sessions. Fourteen of the
twenty are specialty preparations — a far higher rate than the series baseline, because
those are the episodes that stick in visual memory. They are also the episodes whose
entries most often omit the preparation. The retrieval problem and the bad-entry
problem are the same problem.

The cues that actually found them were almost never technique words. They were shape,
colour and position:

> "three trees breaking the vignette on the right" · "green in the water itself" ·
> "reddish-brown mountain on the right" · "held up instead of on the easel" ·
> "five straight trees he's giving bark to"

- [ ] `searchable_features` blocks should answer to that register, not to archetype
      language. Structural descriptors outperform thematic ones: "split canvas",
      "vertical dividing line" and "dual frame" retrieve reliably; "seasonal duality"
      retrieves nothing.
- [ ] Include lay synonyms: teal, pink, woods, oval vignette, breaking the frame,
      board, plank, knothole.

Written so far, as worked examples of the register: S16E08, S17E11, S27E04, S28E04,
S30E02, S07E03, and the seven mask descriptions in `fix_prep_prose.py`.

This cannot be scripted. A regex over the prose reproduces the prose's vocabulary, which
is the thing that fails at retrieval in the first place — it needs the painting. The 25
season 7–8 entries carry a `# TODO` placeholder marking where the block goes.

Suggested order, highest retrieval value first: the 65 `Underpainting` episodes, then
the `Contact Paper` and `Dark Background` ones, then the rest by season.

---

## Tooling

All scripts take `--check` for a dry run and are idempotent.

| script | does |
|---|---|
| `extract_prep.py` | pulls opening captions, writes `prep_review.csv` |
| `backfill_prep.py` | writes `canvas_preparation` from the CSV; preserves tones and `csv_override` |
| `backfill_metadata.py` | adds a whole metadata block to entries that have none |
| `fix_colors.py` | intersects `colors` with the CSV column; only ever removes |
| `fix_ground.py` | rewrites Section 8 where it fails to name the real ground |
| `fix_prose_ground.py` | 26 hand-written repairs to Liquid White claims outside Section 8 |
| `fix_prep_prose.py` | adds missing Liquid Clear and contact-paper facts to Section 8 |
| `lint_index.py` | all of E; exit 1 on failure |

The CSV is not vendored. Fetch it to `.cache/bob_ross_paintings.csv`, which is
gitignored along with the transcript cache:

```
curl -o .cache/bob_ross_paintings.csv \
  https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv
```

`INDEX.md` was patched for the S13E13 rename only. It has not been regenerated since the
403 entries changed — run `/rebuild-index` when F is far enough along to be worth it.

---

## Known-good reference data

- Image URL: `https://raw.githubusercontent.com/darthmolen/bob-ross-hybrid-semantic-model/main/images/painting{index}.png`
- `painting_index` is authoritative for image mapping. Verify from metadata, never infer.
  A fabricated index once displayed an entirely wrong painting (S21E08, 113 vs the real 24).
- Some catalogue stills are **mid-episode frames**, not the finished painting — S27E04 is
  one. An element named in the title but absent from the still is a cropping artefact
  before it is a mapping error.
- The Twitch marathon does not run episodes in order. Sequential assumptions are invalid.
- `tags` and `colors` in the CSV are Python list strings — parse with `ast.literal_eval()`.
- The CSV `colors` column includes `Black Gesso`, `Liquid Clear` and `Liquid Black`
  alongside the pigments. Entry colour lists must be a subset of it, so those belong in
  the list when the CSV has them.
- Year fields in the index are internally inconsistent (S16 stamped 1988, S17 1989–1990,
  S18 1988). Unresolved; do not trust them for chronology.
