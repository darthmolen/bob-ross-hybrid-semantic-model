# Copilot Code Review Instructions

This repository contains a **Bob Ross Hybrid Semantic Model** - a structured catalog of all 403 Bob Ross "Joy of Painting" episodes with semantic metadata for natural language querying.

## Primary Data Source

All episode data should be cross-referenced against the authoritative CSV:
**https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv**

This CSV contains:
- `painting_index`: Unique global identifier (1-403) - **NOT sequential by season**
- `season` and `episode` numbers
- `title`: Official episode title
- `colors`: Comma-separated list of colors used
- `youtube_src`: YouTube video URL

## Critical Validation Rules

### 1. Painting Index Verification

**CRITICAL**: The `painting_index` in YAML metadata must match the CSV data exactly.

- There is **NO FORMULA** to calculate painting_index from season/episode
- Season 1, Episode 1 → painting_index: 282 (not 1)
- Season 3, Episode 1 → painting_index: 256 (not 27)
- The mapping is non-sequential and unpredictable

**IMPORTANT**: Do NOT flag painting_index issues based on assumptions or guesses. You MUST:

1. **Actually fetch the CSV** from: `https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv`
2. **Find the exact row** where `season` and `episode` columns match the file being reviewed
3. **Compare the `painting_index` value** from that CSV row against the file's YAML metadata
4. **Only flag an issue** if there is a verified mismatch between the CSV data and the file

If you cannot fetch or parse the CSV data, do NOT flag painting_index issues - skip this validation instead of guessing.

### 2. Episode Title Verification

Episode titles must match the CSV exactly. Use web search to verify titles against:
- The CSV data source
- Bob Ross official databases
- Wikipedia's Bob Ross episode lists

### 3. Required Semantic Tags

Every episode file must include these 5 semantic identity tags in the YAML section:
- `composition_archetype`
- `palette_identity`
- `depth_style`
- `lighting_type`
- `motion_profile`

Flag any episode missing these tags.

### 4. Color Validation

Colors in the YAML `colors` list must be from the Bob Ross standard palette:
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

Plus base coatings: Liquid White, Liquid Clear, Black Gesso, Grey Gesso

Flag any non-standard color names.

### 5. Section Completeness

Each episode must have all 8 sections:
1. Composition
2. Palette
3. Mood & Atmosphere
4. Structural Layout
5. Motion
6. Technique
7. Narrative Layer
8. Initial Canvas Treatment

## Web Search Cross-Checking

When reviewing semantic model changes, use web search to verify:

1. **Episode Details**: Search for "Bob Ross Season X Episode Y" to confirm:
   - Episode title accuracy
   - Air date/year
   - General painting description matches the semantic analysis

2. **Color Accuracy**: Search for "Bob Ross [episode title] colors" to verify the color palette used

3. **Technique Verification**: Search for specific Bob Ross techniques mentioned to ensure accuracy

4. **Painting Index**: Fetch the CSV data to verify painting_index values

## Markdown Formatting Standards

### Identity Label Formatting

Each section ends with an identity label that summarizes the key characteristic. The **CORRECT format** is:

```
Label: **value**
```

The label is in Title Case, followed by a colon and space, then the value wrapped in bold (`**...**`).

**CORRECT examples:**
```markdown
Palette identity: **golden autumn palette with warm yellow-dominant foliage**
Lighting: **dappled sunlight** filtering through autumn canopy with soft background glow.
Depth style: **tunnel-like pathway depth with atmospheric luminosity**
Motion profile: **gentle forward flow with vertical-horizontal interplay**
Signature technique: **fan brush autumn foliage with layered warm-over-cool color application**
```

**INCORRECT examples (DO NOT USE):**
```markdown
❌ **Palette identity: "value"**          (bold wrapping everything, quotes)
❌ **Palette identity**: value            (bold on label only)
❌ - **palette_identity**: value          (list item with snake_case)
❌ **palette_identity**: value            (snake_case, bold on label)
❌ Palette identity: "value"              (quotes around value)
```

### Identity Labels by Section

| Section | Label Format |
|---------|--------------|
| 1. Composition | (Summary prose paragraph, no label) |
| 2. Palette | `Palette identity: **value**` |
| 3. Mood & Atmosphere | `Lighting: **type** optional additional text.` |
| 4. Structural Layout | `Depth style: **value**` |
| 5. Motion | `Motion profile: **value**` |
| 6. Technique | `Signature technique: **value**` |
| 7. Narrative Layer | (Quoted narrative, no label) |
| 8. Initial Canvas Treatment | (Summary prose, no label) |

### Key Formatting Rules

1. **Bold goes on the VALUE, not the label** - `Label: **value**` not `**Label**: value`
2. **No quotes inside the bold** - `**golden autumn**` not `**"golden autumn"**`
3. **Use Title Case for labels** - `Palette identity:` not `palette_identity:`
4. **Standalone lines** - Identity labels should be on their own line, not inline within paragraphs
5. **No list items** - Identity labels are standalone lines, not bullet points

### Colors in YAML vs Prose

**In the `colors` YAML array:**
- List ONLY the paint colors actually applied during painting
- Do NOT include Liquid White, Liquid Clear, Black Gesso, or Grey Gesso here (these are canvas treatments, not applied colors)

**In the prose sections:**
- Mention Liquid White/Clear/Black Gesso/Grey Gesso in Section 8 (Initial Canvas Treatment) and Section 6 (Technique)
- These are valid to discuss as techniques but should NOT be in the final `colors` YAML list unless they were used as an actual applied color (rare)

## File Naming Convention

Episode files must follow: `s{SS}e{EE}-{slug-title}.md`
- Example: `s01e01-a-walk-in-the-woods.md`
- Season and episode numbers are zero-padded to 2 digits
- Title is lowercase, hyphenated

## SOURCE_IMAGES.md Manifests

Each season folder should have a `SOURCE_IMAGES.md` documenting:
- Episode to painting_index mapping
- Image source (local vs GitHub fallback)
- Verification that indices match CSV data
