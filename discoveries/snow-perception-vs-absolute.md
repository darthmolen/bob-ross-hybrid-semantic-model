# Snow: perceived colour vs absolute colour

**Date:** 2026-08-30
**Source:** mid-episode still, canvas on the easel at the underpainting stage
**Images:** `discoveries/images/s31e05-gesso-stage.jpg` — the ground, before any oil
`discoveries/images/s31e05-underpainting-still.jpg` — the same oval one stage later
**Episode:** **S31E05 — "Cabin in the Hollow"**, `painting_index` 403 — confirmed by the
person who took the photo

---

## The question

> How can Bob make trees purple in a winter scene, yet they still look right and so
> pleasing? It's literal space magic.

## The short answer

It isn't stylisation. It is one of the few places where the physically correct answer and
the beautiful answer are the same answer.

**Snow has no local colour.** It is close to a perfect diffuse reflector, so it does not
have a colour of its own to report — it reports whatever is illuminating it. Sunlit snow
returns warm direct sunlight. Snow *in shadow* is not lit by the sun at all; it is lit by
the sky, and the sky is blue because the atmosphere scatters short wavelengths. A snow
shadow is being illuminated by an enormous blue lamp. Add a low winter sun reddening the
direct light, and the shadow drifts from blue toward violet.

Most painters render snow shadows grey. Grey is the wrong answer that feels safe, because
it is the answer *memory* gives. Bob paints the measurement.

## Perceived vs absolute — why this cuts both ways

The title of this note is the distinction, and it runs in two directions at once.

**1. Absolute is not what you think it is.** "Snow is white" is a claim about an object's
reflectance, not about the light reaching your eye. The absolute measurement of a snow
shadow at golden hour genuinely is blue-violet. What feels like artistic licence is the
literal reading.

**2. Perceived is not what the measurement says either.** Colour vision is relative. A
shadow surrounded by warm sunlit snow reads far more violet than a colorimeter would
report, because the visual system computes colour against its surroundings rather than
absolutely. Bob paints the perceived value, which is *further* from grey than the absolute
one. Simultaneous contrast does the last stretch of the work unpaid.

So the purple is simultaneously more accurate than grey **and** more exaggerated than
accurate. Both, at once. That is the whole trick.

## Why it looks *right* — the structural half

Hue gets the credit; value does the work.

The visual system judges "is this correct?" mostly from lightness relationships and edge
quality, not from hue. Put the trees at the correct *darkness* against the snow and the
sky, and the hue can wander a very long way before anyone objects. The lavender is never
challenged because it is not fighting the structure it sits in.

## Why it looks *pleasing* — the palette half

This part is arithmetic rather than taste, and the dataset shows it outright.

```text
every pigment name across all 403 episodes:
  Alizarin Crimson, Bright Red, Burnt Umber, Cadmium Yellow, Dark Sienna,
  Indian Yellow, Midnight Black, Phthalo Blue, Phthalo Green, Prussian Blue,
  Sap Green, Titanium White, Van Dyke Brown, Yellow Ochre
  (+ Black Gesso, Liquid Black, Liquid Clear — canvas treatments, not pigments)
```

**There is no purple on the palette. Not one tube, in 403 episodes.** Every purple in the
series is Alizarin Crimson mixed into Prussian or Phthalo Blue.

| measurement | value |
| --- | ---: |
| winter-tagged episodes | 98 |
| ...carrying Alizarin Crimson **and** a blue | 84 (85%) |
| ...carrying a dedicated purple or violet tube | **0** |

Because he has no purple, his purple is *made of* the sky. The violet in the trees
literally contains the same Prussian Blue as the sky and the same Alizarin Crimson as the
sunset. Every colour on the canvas shares pigment ancestry with every other colour.

That is why it harmonises, and it is not a matter of taste: **you cannot mix a discordant
colour from a palette that small.** Painters spend careers learning to fake the harmony a
restricted palette hands you for free.

## Corroboration from his own mouth

Recovered from the S17E11 *Morning Walk* captions (see `intake/WORKLIST.md` §D):

> *"For the transparent color, we've just used a mixture of Alizarin Crimson and a little
> Phthalo Blue in it to make, sort of, a **Lavender** color. I've covered the entire dark
> area with that Lavender."*

Not inferred from an image. Stated on air, then confirmed against the palette data.

## The cognitive kicker

You *know* trees are brown. That is memory colour — a label, not what lands on the retina.
So the lavender produces a small split: the perceptual system says *yes, correct* while the
verbal system says *hang on, purple?* Being shown something true that you would never have
said out loud is a genuinely pleasant sensation, and it is a large part of why these
paintings land.

---

## Identifying the episode

**S31E05 "Cabin in the Hollow"**, `painting_index` 403. Confirmed.

```text
Black_Gesso = 1   Liquid_Black = 0   Liquid_Clear = 0
tags   Forest, Winter, Sunset/Sunrise, Cloudy, Landscape, Cabin, Fence,
       Path, Stream, Bare Tree, Conifer Tree, Bushes
colors Alizarin Crimson, Black Gesso, Dark Sienna, Midnight Black,
       Phthalo Blue, Prussian Blue, Titanium White, Van Dyke Brown
video  https://www.youtube.com/watch?v=KYlM2zJnNWY
```

The palette is this note's own argument in miniature: **Alizarin Crimson + Phthalo Blue +
Prussian Blue, and no purple tube.** The lavender in this painting is exactly that mix.

### The four features that identify it

Named by the person who shot the still, and all four are legible in the frame:

1. **The blue river** — the teal band descending to the lower right, with a second pool at
   centre-left
2. **The fence posts** — the small dark marks to the right of the cabin, at two levels
3. **The cabin, set facing left** — blocked in high in the opening, with a crisp white
   knife stroke below it
4. **Lavender foliage** — the masses ringing the vignette, heaviest top and bottom

The vignette edge looks soft and feathered in the still, which led me to call it a
fan-brush vignette rather than a mask. **Wrong** — it is oval contact paper, confirmed by
watching the episode. What softens the edge is the sponge, not the absence of a mask. The
CSV's missing `Contact Paper` tag reinforced the mistake; see below.

### How it was found, and the wrong turn in the middle

Worth recording because the failure is more instructive than the success.

| method | result |
| --- | --- |
| tag filter `Winter` + `Cabin` (46 episodes) | nothing matched by eye |
| **corner-brightness vignette detector** (below) | 38 vignette-format paintings — **the step that mattered** |
| hue-histogram similarity, all 403 | **correct**: S31E05 ranked 1st among vignettes, 5th overall |
| value-structure correlation, hue-independent | wrong; correlation only ~0.6, dominated by the oval shape rather than the composition |

The hue match plus the vignette format was right the first time. I then talked myself out
of it by reading fine structural detail off the still — I decided the cabin's orientation
disagreed with the finished painting — and retracted a correct identification. The cabin
does face left. I misread both the still and the finished work.

**The lesson: do not read fine orientation off an underpainting.** A blocked-in shape at
this stage is a placeholder that gets rebuilt; it is not the finished form. Coarse signals
— palette, format, the position of the light opening — survive the stage change. Fine ones
do not, and a confident reading of one is worth less than a coarse agreement of three.

The secondary error was assuming hue can never survive the stage change. Usually it does
not, because opaque white covers the transparent tone. S31E05 is one of the paintings where
it *does*: the finished work stays lavender and teal, which is precisely why hue matching
found it. The rule is not "ignore colour" but "ignore colour unless the finished painting
keeps the underpainting's colour" — and a lavender vignette is a good sign that it will.

### The corner-brightness vignette detector — worth keeping

Sample the four corners of every image, keep those where all four are bright (mean > 150)
and agree with each other (spread < 70). That returns **38 vignette-format paintings** out
of 403.

Its value is that it finds vignettes the `Contact Paper` tag misses, because a feathered
vignette needs no mask. S31E05 and S04E04 are both untagged vignettes, and S31E05 would
not have been in the candidate set without it.

### RESOLVED — the ground, from watching the episode

The suspicion below was right in direction and far short in substance. Watched and
confirmed, 2026-08-30:

1. **Oval contact paper**, burnished down. The scene is worked inside it; the canvas
   outside stays bare, which is the white surround in the finished painting.
2. **Grey gesso, tapped in with a sponge** — not brushed. Broken, granular texture that
   already reads as distant winter scrub.
3. **Liner brush twigging** into the wet grey gesso, drawing branch structure while the
   ground is still workable.
4. **Black gesso, same sponge, graded across the oval** — heavy at the sides, light
   through the middle.

`discoveries/images/s31e05-gesso-stage.jpg` catches it before a drop of oil is applied.
The sponge stipple is unmistakable, the oval sits on bare white canvas with a clean
boundary, and the palette bug is still running **PRUSSIAN BLUE** across the bottom of
frame — which places it inside the opening minute.

**The gradient, measured off that frame:**

| sampled region | luminance (0–255) |
| --- | ---: |
| bare canvas above the oval | 176 |
| light centre of the oval | **178** |
| dark, lower middle | 51 |
| heaviest dark, right side | **24** |

Two things fall out of those numbers.

The oval spans **24 to 178** — very nearly the full usable value range of the finished
painting — and every bit of it is acrylic gesso, laid before any oil.

And the light centre measures *the same as bare canvas*. The grey gesso there is scumbled
so thin it returns canvas value. He is not painting a light centre; he is **leaving** one,
and sponging darkness in around it. The vignette is made by subtraction.

That fourth step is why the underpainting still looks the way it does. The dark-to-light
falloff of the vignette is **already in the ground**, sponged in and dried, before any oil
is touched. Bob normally builds a vignette's dark edges in oil working inward; here the
value scaffold is pre-built in acrylic and the oil sits on top of it. Not just a dark
ground — a *graded* one.

It also settles what the underpainting still is showing. Put the two frames side by side
and they are the same oval, one stage apart: the light-valued violet and teal centre is
transparent oil over the **light middle** of that gradient, and the near-black ring at the
perimeter is the heavy black gesso at the sides showing through — not paint. The reading
was right; the mechanism behind it was richer than a guess at a "shaped ground."

### Two things that appear nowhere else in 403 episodes

| fact | how the index currently handles it |
|---|---|
| **Grey gesso** | 17 entries mention it; **all 17 are negations** — "No grey gesso", "Grey gesso: Not used". This is the first recorded use. The CSV has no column for it. |
| **Sponge application** | The word "sponge" appears in **zero** of the 403 entries. The technique is absent from the index entirely. |

The CSV tracks exactly three preparation facts — `Black_Gesso`, `Liquid_Black`,
`Liquid_Clear` — plus a `Contact Paper` tag. Grey gesso, sponging, and a graded ground all
fall outside that schema, which is the same shape of problem as S07E03's dried acrylic
yellow underground.

### The Contact Paper tag under-reports

S31E05 carries **no `Contact Paper` tag**, yet the oval mask is used on air. Measuring the
tag against the corner-brightness detector:

| | count |
|---|---:|
| tagged `Contact Paper` in the CSV | 60 |
| detected as vignette format | 38 |
| **detected as vignette, not tagged** | **7** |
| tagged, not a vignette | 29 |

The seven the tag misses: S04E04 Winter Sawscape, S08E07 Winter Hideaway, S10E07 Winter
Solitude, S12E12 **Mountain in an Oval**, S25E06 Oriental Falls, S30E07 Through the
Window, S31E05 Cabin in the Hollow. One of them has "Oval" in its title.

The 29 in the other direction are not errors — a mask is not always a vignette; it can be
a straight horizon edge or a shaped border. The two concepts are independent, and the
index should carry both.

### What was changed as a result

`season-31/s31e05-cabin-in-the-hollow.md` — Section 8 rewritten from observation, with
`csv_override: true` so the deterministic backfill will not revert it, and a
`lint_exceptions` entry because the mask rule cannot fire from a tag the CSV does not have:

```yaml
canvas_preparation:
  ground: "Black Gesso over Grey Gesso, sponged"
  contact_paper: true
  mask_shape: "oval"
  application: "sponge"
  csv_override: true
```

---

## Follow-ups

- [x] ~~Settle the shaped-ground question~~ — resolved by watching the episode, above
- [ ] File the seven untagged vignettes as CSV corrections, and check whether any other
      episode uses grey gesso or a sponge — nothing in the index records either, so the
      only way to know is to watch
- [ ] Promote the corner-brightness vignette detector into `scripts/` — it is currently
      only described in this note, and it earned its keep
- [ ] Consider a `vignette: true` field derived from that detector. `Contact Paper` is not
      a synonym for vignette in either direction, and "oval vignette" is exactly the kind
      of lay phrase `searchable_features` is supposed to answer to
- [ ] Write S31E05's `searchable_features` from both the still and the finished painting —
      the underpainting stage is itself a memorable cue. This note already holds them:
      *oval vignette*, *lavender trees*, *purple woods*, *blue river*, *teal stream*,
      *cabin facing left*, *snow roof*, *fence posts in the snow*, *white canvas around
      the oval*

## Provenance

Still photographed off a screen and supplied on 2026-08-30, committed alongside this note.
Everything above was read from that file. The episode identification was confirmed by the
person who took the photo, not derived — see the wrong turn recorded above.

## Related

- `intake/WORKLIST.md` §D — the caption recovery that produced the *Morning Walk* quote
- `season-17/s17e11-morning-walk.md` — `secondary_tone: "Lavender — transparent Alizarin
  Crimson with a little Phthalo Blue"`
- `season-31/s31e05-cabin-in-the-hollow.md` — the entry this note questions
- `season-04/s04e01-purple-splendor.md` — the same lavender effect at full canvas with no
  vignette; the closest sibling to this painting in the corpus
- `planning/backlog/feature_searchable-features-backfill_2026-08-29.md` — the retrieval
  work this note keeps bumping into
