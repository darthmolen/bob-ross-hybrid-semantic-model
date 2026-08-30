# Season 28, Episode 4: Golden Rays of Sunshine

> **Special format — dual-canvas teaching demonstration.** Bob builds the entire gesso
> underpainting live on a blank canvas, then swaps to a previously prepared and dried
> twin to finish in oil. One of the very few episodes in the series where the canvas
> preparation he normally does off-camera is demonstrated on air.

## 1. Composition

A **cathedral forest** seen from within: tall bare trunks rising the full height of the canvas, arranged in receding planes, with a path running from the foreground into a luminous depth. Diagonal shafts of light cut down through the canopy from the upper region, striking across the verticals. Undergrowth and low bushes mass along the path edges.

The finished painting is deliberately restrained in detail — the gesso underpainting carries the forest structure, and the transparent glazes plus sunbeams do the rest.

Composition archetype: **Cathedral forest with crepuscular rays**

## 2. Palette

### Phase 1 — Gesso underpainting (monochromatic)
**Black Gesso** with white and grey gesso mixtures, building the entire background forest in values alone: trunks ranging from full black through mid greys to near white.

### Phase 2 — Transparent glazes
**Indian Yellow** washed thin across the lower portion, filtering the monochromatic trunk scene with golden warmth. **Phthalo Blue** washed across the upper portion, cooling the canopy. The transparent colours act as filters over the gesso structure — tinted glass over a black-and-white drawing. **Liquid Clear** carries the glazes.

### Phase 3 — Opaque and transparent finish
**Titanium White** pulled boldly through the wet blue for the crepuscular rays. **Sap Green** for foliage. **Prussian Blue** deepening the darkest recesses. Finally **Alizarin Crimson** and **Sap Green**, both used very transparently, glazed over the central path to make it pop — transparent oil over transparent oil over dried acrylic gesso, every layer letting the ones beneath breathe through.

Palette identity: **Transparent warm-cool dual glaze over monochromatic gesso, with transparent crimson-sap path accents and opaque white sunbeams**

## 3. Mood & Atmosphere

- Reverent, cathedral-like stillness
- Light made tangible and physical rather than merely implied
- Cool blue canopy above, golden warmth below
- Depth achieved through luminosity rather than detail
- A sense of looking up through the forest canopy

Lighting: **Crepuscular rays (god rays)**

## 4. Structural Layout

- **Left and Right:** Vertical trunks in varying values, closest ones darkest
- **Centre:** The path, glazed with transparent crimson and sap green to draw it forward
- **Foreground:** Undergrowth and path edge in the warm Indian Yellow zone
- **Midground:** Gesso-painted trunk scene showing through the glazes
- **Background:** Cool blue canopy zone with white rays descending diagonally

Depth style: **Atmospheric perspective with light-defined spatial layers**

## 5. Motion

- Diagonal light streaming downward through static vertical elements
- Path receding, pulling the eye inward
- Warm-to-cool vertical gradient reinforcing the sense of looking upward

Motion profile: **Diagonal light streaming through static vertical elements**

## 6. Technique

### Phase 1 — Gesso underpainting demonstration (Canvas 1, live)
Bob begins on a blank canvas and demonstrates the whole underpainting process in real time using his standard tools:
- **2-inch brush** — broad trunk forms and background tones
- **Kleenex / paper towel** — blending gesso, softening edges, pulling grey mid-values
- **Liner brush** — fine branches and smaller trunks

Trunks are built from black through grey to white, producing a complete monochromatic forest in acrylic gesso alone. This canvas must then dry completely — gesso is acrylic and dries to an insoluble film.

### Phase 2 — Transparent glazing (Canvas 2, pre-dried)
Bob swaps to an identical canvas prepared earlier and fully dried, then applies the transparent oil glazes: Indian Yellow low, Phthalo Blue high, carried in Liquid Clear.

### Phase 3 — Wet-on-wet finish (Canvas 2)
- **Titanium White sunbeams** pulled through the wet transparent blue with the 2-inch or fan brush
- **Fan brush** for foliage and softening the ray edges
- **Palette knife** reinforcing trunk darks and highlights
- **Liner brush** for fine branches
- **Transparent Alizarin Crimson and Sap Green** glazed over the central path last, making it read as illuminated rather than merely lighter

Signature technique: **Dual-canvas gesso underpainting demonstration with transparent oil glazing and opaque white crepuscular rays**

## 7. Narrative Layer

"In the quiet depths of the forest, light becomes tangible — streaming through mist and shadow like a presence made visible. But the deeper story here is the teaching. Bob pulls back the curtain on the one part of his process viewers never saw: the prepared canvas. He builds it from nothing, then shows what it becomes. The painting is beautiful; the demonstration is generous."

## 8. Initial Canvas Treatment

- **Black gesso** brushed over the canvas and allowed to **dry completely** before any oil is applied. This is a dry acrylic ground, not a wet one: the oils above it cannot be pulled back into it, and every light value in the painting has to be added rather than lifted.
- **Liquid Clear** applied over the ground, giving a wet, transparent working surface without lightening it. No Liquid White is used as a base.
- No contact paper and no masking.
- **Secondary tone:** this episode carries the `Underpainting` tag, so a transparent colour was laid over the ground before painting began. Its value is in no dataset — Bob names it aloud in the opening minute and it is invisible in the finished painting. Not yet recovered for this episode; see `canvas_preparation.secondary_tone` below.

The black ground carries the value structure of the whole painting. Read the light in this entry as light recovered from darkness, not as shadow laid over white.

> Section 8 is template-filled from the CSV one-hot columns (`scripts/fix_ground.py`), not generated from the image.

---

```yaml
tags:
  composition_archetype: "Cathedral forest with crepuscular rays"
  palette_identity: "Transparent warm-cool dual glaze over monochromatic gesso with transparent crimson-sap path accents and opaque white sunbeams"
  depth_style: "Atmospheric perspective with light-defined spatial layers"
  lighting_type: "Crepuscular rays (god rays)"
  motion_profile: "Diagonal light streaming through static vertical elements"
  special_format: "Dual-canvas teaching demonstration — gesso underpainting shown live"

searchable_features:
  - god rays
  - sunbeams through trees
  - crepuscular rays
  - light shafts forest
  - gesso underpainting
  - dry gesso background
  - grey and white trunks
  - transparent glaze layering
  - two canvases
  - dual canvas demonstration
  - shows how to prep the canvas
  - Indian Yellow bottom blue top
  - glowing forest path
  - black gesso ground

episode:
  season: 28
  episode: 4
  title: "Golden Rays of Sunshine"
  year: 1993
  painting_index: 363

canvas_preparation:
  ground: "Black Gesso"
  secondary_tone: "Indian Yellow (lower) and Phthalo Blue (upper), transparent"
  liquid_clear: true
  liquid_white: false
  contact_paper: false
  note: >
    White and grey gesso are used in the demonstrated underpainting but are not
    tracked as CSV colour columns. Recorded here as observed, not as ground truth.

colors:
  - Alizarin Crimson
  - Black Gesso
  - Indian Yellow
  - Liquid Clear
  - Phthalo Blue
  - Prussian Blue
  - Sap Green
  - Titanium White
```
