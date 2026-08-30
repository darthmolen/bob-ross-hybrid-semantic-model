# Caption Tone Recovery

**Status:** Backlog
**Track:** main
**Date:** 2026-08-29
**Date Discovered:** 2026-08-29
**Author:** Claude (Opus 5)
**Discovered During:** `intake/WORKLIST.md` §D — run of `scripts/extract_prep.py`

## Context

`canvas_preparation.secondary_tone` is the one field in the schema that no dataset
contains. It is the transparent colour laid over the Clear before painting starts: Bob
names it aloud in the opening minute and it is invisible in the finished painting, so
neither the CSV nor a vision pass can recover it. `scripts/extract_prep.py` reads it out
of YouTube captions.

The first run over the 65 `Underpainting` episodes returned **5 recovered, 60 blocked**.
YouTube IP-blocks bulk transcript requests in practice after about six. Worse, the script
was caching those transient blocks as "this video has no captions" — permanently — so the
run reported 60/65 `no-captions` and every one of those 60 was a false negative that would
have been skipped forever on the next run.

That bug is fixed and the poisoned cache is purged. `Blocked` is now a distinct exception,
never cached, with exponential backoff and a summary line stating that a blocked run is
not a result.

What remains is the rate limit itself, and the first run established that **it cannot be
outrun inside a single session**. Raising `--sleep` from 0.6s to 10s and adding backoff to
a 300s ceiling did not help: a second attempt over the same 60 episodes, run after the
first had already blocked, recovered nothing. The block is a per-IP budget measured over
hours, not a per-request spacing problem. Once tripped it stays tripped for a while, and
retrying into it spends budget for nothing.

So this job has to be **trickled** — a handful of episodes per run, many runs spread over
days, stopping the moment a block appears rather than pushing through it. The transcript
cache makes that free: fetched episodes are never re-fetched, so every run resumes exactly
where the last one stopped and costs only the episodes it actually pulls.

The five that came through paid for the exercise:

| episode | what Bob says |
|---|---|
| S17E11 Morning Walk | black gesso, dried; a little Liquid Clear; transparent **lavender** = Alizarin Crimson + a little Phthalo Blue |
| S11E10 Sunset over the Waves | black gesso, dried; **Indian Yellow** sky, **Alizarin Crimson** below; masking tape as a horizon straight-edge |
| S12E08 Evening Waterfall | black gesso, dried; **Phthalo Blue + Sap Green**, thin, left wet |
| S04E07 Cabin in the Woods | black canvas; thin coat of **Phthalo Blue + Sap Green** |
| S07E03 Evergreens at Sunset | dried opaque **acrylic yellow** ground, taped circle for the sun, **Liquid Black** over the top |

Two produced new ground truth the CSV contradicts or cannot express, and both now carry
`csv_override: true`:

- **S17E11** uses Liquid Clear; the CSV records `Liquid_Clear = 0`.
- **S07E03** uses an opaque dried acrylic yellow ground with a taped circular mask. The
  schema has no field for it — it is recorded in `acrylic_underground` and `mask_shape`.
  The sun in that painting was never painted; it is bare ground where the tape was.

Both were caught by the `disagreement` column, which is the script's real payload. At a
5/65 sample it has already found two dataset errors. Finishing the run is the only way to
know how many more there are.

## Objective

Recover `secondary_tone` for every episode whose captions carry it, by trickling the
fetches slowly enough that YouTube never blocks, and adjudicate every dataset
disagreement the run surfaces.

## Success Criteria

- [ ] All 403 episodes have a cached transcript or a confirmed genuine `no-captions`
- [ ] **No run in the campaign ends with rows in `blocked` status** — a blocked run means
      the rate was too high and the pacing needs to drop, not that the work is done
- [ ] Every `high` confidence row adjudicated; tone written to the entry with the quote
      that produced it and a `secondary_tone_source` field
- [ ] Every `disagreement` flag adjudicated — `csv_override` where the narration wins,
      a caption variant added where the script misheard
- [ ] `tone-unrecovered` rows either resolved by a wider `--window` or listed as a
      genuinely-unrecoverable residue with a reason
- [ ] Section 8 of each corrected entry quotes the narration, matching the five already
      done

## Approach

### The trickle is the plan

Treat the per-IP budget as unknown and let the block calibrate it. The only hard number
we have is that **six consecutive fetches tripped it**, so start well under that and
adjust from evidence.

Starting parameters, to be tuned:

| knob | start at | why |
|---|---|---|
| episodes per run | **4** | comfortably under the six that tripped it |
| gap between runs | **2 hours** | ≈48/day; the whole 403 in ~9 days |
| `--sleep` within a run | 10s | spacing inside a run is cheap insurance, not the fix |
| `--retries` | **0** | retrying into a block spends budget for nothing and may extend it |

Adaptation rule, applied by whoever or whatever drives the campaign:

- A run that **blocks on its first fetch** → the IP is still cold. Skip the next two slots
  entirely, then resume at half the episodes-per-run.
- A run that blocks **partway through** → drop episodes-per-run by one and carry on.
- **Ten consecutive clean runs** → raise episodes-per-run by one, up to a ceiling of 8.

Never push through a block. Stop, wait out the slot, come back. The cache means a stopped
run has lost nothing.

### Driving it

This is a long unattended campaign, not a sitting. Two options:

- `/loop 2h` with a prompt that runs one batch and reports the count — simplest, and the
  session stays live to adjudicate as results land.
- A scheduled cloud agent (`/schedule`) if the machine will not be up for nine days.

Either way, progress is measurable without parsing anything:

```bash
ls .cache/.transcript_cache/*.json | wc -l          # episodes fetched, out of 403
```

### Proxy, as a fallback only

If the trickle turns out to be blocked even at 4-per-2-hours, route through a residential
proxy per the `youtube-transcript-api` README section on IP bans. Demoted from the
original plan: a proxy is a dependency to acquire and pay for, and the trickle costs
nothing but patience. Try patience first.

### Adjudication

Manual and fast — the script's own estimate of five seconds a row held up. Sort
`prep_review.csv` by `confidence` descending and read the `quote` column.

Adjudication does **not** need to wait for the campaign to finish. Every batch produces
rows worth reading, and reading them early is what feeds the variants table.

Expect false positives in `said_tone`. Bob reads the palette aloud in the first thirty
seconds of most episodes, so colour names near a prep cue are not always the tone —
S04E07 reported "Titanium White + Phthalo Blue + Sap Green" when only the last two were
the ground tone. The quote column settles it.

The colour-variants table is the maintenance surface, and every variant added improves all
403 retroactively because transcripts are cached — re-analysing costs nothing, only
re-fetching is rationed. This is the reason to adjudicate continuously rather than at the
end: a variant added on day two improves every batch from day one onward *and* every batch
still to come. Variants added from the first five: `black canvas`/`black canvases` (Bob
says "black gesso" once and then never again), `duct tape`/`masking tape`/`piece of
tape`/`made a circle`, `acrylic … paint`/`painted it yellow`, and prep cues `transparent
color`, `layers of color`, `even coat`, `on top of that`, `onto that`, `mixture of`,
`still wet`. The `black canvas` variant alone lifted S04E07 from a false `gesso-not-heard`
flag to high confidence.

## Phases

### Phase 1 — Give the script a rate budget

`extract_prep.py` currently has `--sleep`, `--retries` and `--max-backoff` but no way to
cap a run or to stop cleanly on a block. Add:

- `--limit N` — fetch at most N **uncached** episodes this run, then stop. Cached ones
  are free and must not count against the budget.
- `--stop-on-block` — abandon the run at the first `Blocked` and exit non-zero, so a
  scheduler can tell "rate too high" from "batch complete".
- `--remaining` — print how many episodes still lack a cached transcript and exit. The
  progress meter and the loop's termination check.

Verify with `--limit 1` that the budget counts uncached fetches only.

### Phase 2 — Calibrate  [ASYNC]

Run three or four batches at the starting parameters over a day. If all come back clean,
the pacing holds; if any blocks, apply the adaptation rule before committing to a
schedule. Do not start the long campaign until a full day has passed without a block.

### Phase 3 — Trickle the 65 `Underpainting` episodes  [ASYNC]

60 remaining. At 4 per run every 2 hours, roughly a day and a half. Highest value first —
these are the episodes where the tone is known to exist.

### Phase 4 — Adjudicate the 65

Write tones into `canvas_preparation.secondary_tone` and into Section 8 with the
supporting quote. Add caption variants for anything misheard and re-analyse — free
against the cache.

### Phase 5 — Trickle the remaining 338  [ASYNC]

About a week at the same pacing. The full run's value is the `tone-not-tagged` flag:
episodes where Bob describes a tone the `Underpainting` tag missed. That is new ground
truth the dataset does not have, and there is no way to find it except by listening.

### Phase 6 — Adjudicate the disagreements

Work the `disagreement` column, not the tone column:

| flag | action |
|---|---|
| `tone-not-tagged` | new ground truth — record it, note the CSV omission |
| `tone-unrecovered` | try `--window 240`; if still empty, list as residue |
| `gesso-not-heard` | widen variants, or record the CSV as wrong |
| `tone-off-palette` | usually a mis-hearing — add the variant |
| `clear-not-in-csv` | CSV is wrong — `csv_override: true` plus a note, as on S17E11 |

### Phase 7 — Close out

Re-run `lint_index.py` (must stay clean), tick §D in `intake/WORKLIST.md`, and record two
numbers: how many dataset errors the full run found, and what pacing the campaign settled
at. The first is the argument for applying this technique elsewhere; the second is what
the next person needs so they do not have to rediscover the rate limit.

## Dependencies / Prerequisites

- `pip install youtube-transcript-api`
- `.cache/bob_ross_paintings.csv` fetched (gitignored; command in `intake/WORKLIST.md`)
- **A way to run unattended over ~9 days** — `/loop`, a scheduled agent, or a person
  willing to fire a batch a few times a day. This is the real prerequisite; the work per
  batch is seconds.
- **The IP must have cooled off.** As of 2026-08-29 this machine's address was still
  blocked. Check with a single-episode fetch before starting:
  `python scripts/extract_prep.py --season 16 --episode 8 --out .cache/probe.csv`
- **Partially conflicts with `feature_searchable-features-backfill`.** The conflict is
  narrower than it first looks, and the trickle is what makes it so:

  | phase | writes to | can share the clock with the features backfill? |
  |---|---|---|
  | 1 tooling | `scripts/extract_prep.py` | yes |
  | 2, 3, 5 fetching | `.cache/` and `artifacts/prep_review.csv` only | **yes** |
  | 4, 6 adjudication | `season-*/s*.md` | **no — serialise** |

  The fetching phases are nine days of waiting that touch no entry file. Blocking the
  features backfill behind them would waste the wall clock for nothing. Run the trickle in
  the background and do features work in the foreground; stop the features work only for
  the adjudication windows, which are hours, not days.

  If the two are given separate tracks on that basis, the adjudication phases must still
  hold `Track: main` and take the features plan out of `in-progress/` first — their file
  sets genuinely overlap and the guardrail applies.

## Files Expected to Change

- `scripts/extract_prep.py` — `--limit`, `--stop-on-block`, `--remaining`; plus caption
  variants as they are found
- `season-*/s[0-9]*.md` — `canvas_preparation.secondary_tone` and Section 8 for every
  episode with a recovered tone; up to 65 in phase 4, unknown in phase 6
- `intake/WORKLIST.md` — §D ticked off, and the settled pacing recorded next to it
- `artifacts/prep_review.csv` — new; the adjudicated review sheet, worth committing as
  the record of what was heard

## Trigger for Promotion

Promote when someone can leave a loop or a scheduled agent running for a week or two. The
active work is small and spread thin; the constraint is wall-clock patience, not effort.

Promote immediately and in isolation if a **specific** episode needs its tone:
`--season N --episode M` is a single request and will usually get through even from a
rate-limited address, which is how S17E11 was recovered in the first place.
