# Searchable Features Backfill

**Status:** Backlog
**Track:** main
**Date:** 2026-08-29
**Date Discovered:** 2026-08-29
**Author:** Claude (Opus 5)
**Discovered During:** `intake/WORKLIST.md` §F, surfaced by `scripts/lint_index.py`

## Context

Worklist §F is the last open item and the largest. **396 of 403 entries have no
`searchable_features` block.** Seven do: S07E03, S16E08, S17E11, S27E04, S28E04, S30E02,
S29E03 — all written by hand during the §A–§E correction pass.

This is the retrieval half of the index. Twenty paintings have been found across
sessions; fourteen of the twenty were specialty preparations, and the cues that actually
found them were never technique words. They were shape, colour and position:

> "three trees breaking the vignette on the right" · "green in the water itself" ·
> "reddish-brown mountain on the right" · "held up instead of on the easel" ·
> "five straight trees he's giving bark to"

The bad-entry problem and the retrieval problem turned out to be the same problem, and
§A–§E fixed only the first half. An entry can now state its ground correctly and still be
unfindable — S30E02 Woodgrain View was located only by querying the one-hot prep columns
directly, because nothing in its prose said *board*, *plank* or *knothole*.

## Objective

Every episode entry carries a `searchable_features` block written in the register people
actually remember, so `lint_index.py` exits clean.

## Success Criteria

- [ ] `python scripts/lint_index.py` reports 0 `features-missing` and 0 `features-empty`
- [ ] Every block is written from the painting, not from the entry's own prose
- [ ] Every specialty preparation appears in plain words in its entry's block —
      "black gesso ground", "board background", "contact paper mask", "oval vignette"
- [ ] Counted things are counted: "two palm trunks", "five straight birch trees"
- [ ] Lay synonyms present alongside painter's vocabulary: teal, pink, woods, plank,
      knothole, breaking the frame
- [ ] `INDEX.md` regenerated once the backfill is complete

## Approach

**This cannot be scripted, and that is the whole point.** A regex over the entry's prose
reproduces the prose's vocabulary, which is exactly what fails at retrieval. Each block
needs the image at `images/painting{index}.png`.

Work season by season, reading the painting and writing 10–15 features per entry. Use the
seven existing blocks as the register reference; `TEMPLATE.md` documents the rules.

Do **not** reuse the composition archetype or palette identity as features. Those are
thematic labels and they retrieve nothing — "seasonal duality" found no episode, while
"split canvas" and "vertical dividing line" found it immediately.

### Prioritisation

Ordered by retrieval value, not by season number. Specialty preparations are the episodes
people remember and the ones whose entries most often omitted the defining feature.

| bucket | total | have | missing |
|---|---:|---:|---:|
| A — `Underpainting` tag | 65 | 5 | 60 |
| B — `Contact Paper` tag | 50 | 0 | 50 |
| C — other dark ground / `Dark Background` | 74 | 2 | 72 |
| D — everything else | 214 | 0 | 214 |

Buckets A–C are 189 entries and carry most of the value. Bucket D is the long tail.

Seven mask shapes are already described in prose, in `scripts/fix_prep_prose.py` — lift
those into the corresponding `searchable_features` blocks rather than re-deriving them:
S08E09 stepped-notch panel, S10E11 triptych, S14E09 oval, S17E08 apple silhouette with
NEW YORK lettering, S20E05 wide border, S21E05 oval, S29E03 vertical split.

## Phases

### Phase 1 — Harness and register

Write `scripts/features_report.py`: list entries missing a block, grouped by bucket, with
`painting_index` and image path, so a session can pick up a batch without re-deriving the
queue. Confirm the register against the seven existing blocks.

### Phase 2 — Bucket A, the 60 remaining `Underpainting` episodes  [ASYNC]

Highest value. These overlap the caption-recovery plan, so run one or the other, never
both — see Dependencies.

### Phase 3 — Bucket B, the 50 `Contact Paper` episodes  [ASYNC]

Shape is the searchable fact here: oval, triptych, border, panel, silhouette, and which
elements break the frame.

### Phase 4 — Bucket C, the 72 remaining dark-ground episodes  [ASYNC]

### Phase 5 — Bucket D, the 214 remaining episodes  [ASYNC]

Batch by season, 13 at a time.

### Phase 6 — Close out

Run `lint_index.py` to zero, then `/rebuild-index`, then delete `intake/WORKLIST.md`
if §D is also done.

## Dependencies / Prerequisites

- `.cache/bob_ross_paintings.csv` fetched (gitignored; command in `intake/WORKLIST.md`)
- `images/painting{index}.png` — all 403 present locally
- **Partially conflicts with `feature_caption-tone-recovery`.** That plan is now a
  trickle — roughly nine days of paced YouTube fetches to stay under the rate limit — and
  its fetching phases touch only `.cache/` and `artifacts/`, not entry files. So this plan
  does **not** have to wait nine days behind it. Run the trickle in the background and
  this backfill in the foreground.

  The two do collide during that plan's adjudication phases (its 4 and 6), which write
  `secondary_tone` and Section 8 into the same entries this plan is editing. Those windows
  are hours. Pause this plan for them rather than sequencing the whole thing behind the
  campaign.

## Files Expected to Change

- `season-*/s[0-9]*.md` — 396 entries gain a `searchable_features` block
- `scripts/features_report.py` — new; the work queue
- `INDEX.md` — regenerated at the end
- `intake/WORKLIST.md` — §F ticked off

## Trigger for Promotion

Promote when there is appetite for a long, image-by-image pass — this is 396 paintings and
does not compress. Promote a single bucket instead if the appetite is smaller: bucket A or
B alone is a coherent, shippable unit and each is worth more than the same effort spread
thinly across all four.
