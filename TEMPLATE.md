# Bob Ross Episode Template

Use this template to analyze and document each Bob Ross "Joy of Painting" episode. Each entry must contain all eight sections in the order shown below.

---

## Episode Header

```markdown
# Season {X}, Episode {Y} — "{Title}" ({Year})
```

---

## 1. Composition

Describe the physical layout of the painting:

- **Landforms**: Mountains, hills, valleys, cliffs
- **Water features**: Lakes, rivers, oceans, waterfalls, streams
- **Trees and vegetation**: Forest density, tree types, ground cover
- **Sky conditions**: Clear, cloudy, sunset, atmospheric effects
- **Structures**: Cabins, barns, fences, bridges (if any)
- **Overall compositional archetype**: Forest corridor, mountain reflection, oceanscape, etc.

End with a one-sentence summary of the compositional archetype.

**Example:**
```
- Narrow river flowing toward the viewer
- Dense dark forest on both sides
- Soft distant tree line
- Subtle background glow
- No mountains
- No structures

A dark-toned forest-and-river corridor composition.
```

---

## 2. Palette

List the dominant colors and their functional roles:

- **Primary colors used**: Specific Bob Ross palette colors
- **Warm vs cool**: Overall temperature bias
- **High-contrast vs low-contrast**: Value relationships
- **Signature color relationships**: Key color interactions

End with a **palette identity phrase**.

**Example:**
```
- Deep blacks and dark blues (underpainting)
- Earthy browns
- Cool greens for foliage
- Titanium white for water highlights
- Soft yellow-white glow in the distance

Palette identity: **dark woodland palette with luminous water highlights**
```

**Bob Ross Standard Colors:**
- Alizarin Crimson
- Bright Red
- Cadmium Yellow
- Dark Sienna
- Indian Yellow
- Midnight Black
- Phthalo Blue
- Phthalo Green
- Prussian Blue
- Sap Green
- Titanium White
- Van Dyke Brown
- Yellow Ochre

---

## 3. Mood & Atmosphere

Capture the emotional and atmospheric qualities:

- **Tone**: Peaceful, dramatic, mysterious, serene, energetic
- **Lighting type**: Diffuse, backlit, glowing, stormy, dappled, sunset
- **Emotional resonance**: What feelings the painting evokes

End with a **lighting type** statement.

**Example:**
```
- Mysterious
- Quiet
- Slightly dramatic
- Cool and shaded
- Depth emerging from darkness

Lighting: **backlit glow** illuminating the river and distant trees.
```

---

## 4. Structural Layout

Break down the spatial arrangement:

- **Left**: Elements on the left side
- **Right**: Elements on the right side
- **Center**: Central focal elements
- **Foreground**: Front elements closest to viewer
- **Midground**: Middle-distance elements
- **Background**: Distant elements

End with a **depth style** statement.

**Common Depth Styles:**
- Atmospheric fade
- Tunnel depth
- Silhouette depth
- Layered planes
- Radial depth

**Example:**
```
- **Left:** Dense trees leaning inward
- **Right:** Matching forest mass
- **Center:** River reflecting distant light
- **Foreground:** Grassy banks and water highlights
- **Background:** Soft glow behind distant trees

Depth style: **tunnel-like depth with strong value contrast**
```

---

## 5. Motion

Identify any implied or explicit motion:

- **Water flow**: River current, waterfall movement, ocean waves
- **Wave direction**: Breaking patterns, foam streaks
- **Cloud drift**: Wind direction, atmospheric movement
- **Compositional flow lines**: Visual paths that guide the eye
- **Atmospheric motion**: Mist, fog, light rays

End with a **motion profile** statement.

**Example:**
```
- Gentle river flow toward the viewer
- Subtle foam streaks
- Faint upward atmospheric glow
- Compositional flow: **center-pull perspective**
```

---

## 6. Technique

List the technical methods Bob Ross used:

- **Brush types**: Fan brush, liner brush, script liner, oval brush
- **Knife work**: Palette knife mountains, trees, structures
- **Blending methods**: Criss-cross, circular, feathering
- **Reflection techniques**: Pull-down, mirror, ripple effects
- **Special effects**: Mist, glow, translucency, scratching, scraping

End with a **signature technique** statement.

**Example:**
```
- Dark toned canvas (early black-gesso-style approach)
- Fan-brush evergreens and bushes
- Knife-scraped tree trunks
- Pull-down reflections for water
- Horizontal smoothing strokes
- Liner brush twigs and grasses

Signature technique: **light water highlights over a dark river base**
```

---

## 7. Narrative Layer

Provide a short interpretive description (2-4 sentences):

- What story the painting suggests
- Emotional or symbolic meaning
- How the elements interact to create the overall impression

Use quotation marks around the narrative.

**Example:**
```
"A quiet, shadowed river winding through a dark forest.
The distant glow adds mystery and depth, while the water catches the faintest hints of light."
```

---

## 8. Initial Canvas Treatment

Document the foundation Bob Ross prepared before painting:

- **Liquid White**: Smooth, wet surface for blending
- **Liquid Clear**: Transparent wet surface for glazing
- **Black gesso**: Dark underpainting for dramatic contrast
- **Grey gesso**: Mid-tone foundation
- **Contact paper**: Masking for sharp edges
- **Textured gesso**: Special surface preparation

End with a one-sentence summary of the foundational approach.

**Example:**
```
- Dark toned canvas
- Liquid White applied selectively for glow and water
- No contact paper
- No masking
- No textured gesso

A foundational dark-base woodland scene emphasizing contrast and atmospheric depth.
```

---

## Metadata Section (REQUIRED)

Add structured metadata for programmatic access. **This section is mandatory for all episode entries:**

```yaml
tags:
  composition_archetype: "forest corridor"
  palette_identity: "dark woodland palette with luminous water highlights"
  depth_style: "tunnel depth"
  lighting_type: "backlit glow"
  motion_profile: "center-pull perspective"

episode:
  season: 2
  episode: 6
  title: "Black River"
  year: 1984
  youtube_url: "https://www.youtube.com/watch?v=..."

colors:
  - Midnight Black
  - Prussian Blue
  - Van Dyke Brown
  - Sap Green
  - Titanium White
  - Yellow Ochre
```

---

## Style Requirements

- Use concise bullet lists for structured fields
- Use short descriptive paragraphs for narrative sections
- Maintain consistent terminology across episodes
- Avoid subjective critique; focus on semantic clarity
- Keep each episode self-contained and searchable
- No conversational language
- No references to the indexing process
- Use bold for key identity phrases (palette identity, lighting type, depth style, etc.)

---

## Complete Example

See `.claude/context/bob-ross-semantic-index-context.md` Section "Example Entry: Season 2, Episode 6 — 'Black River' (1984)" for a full working example.
