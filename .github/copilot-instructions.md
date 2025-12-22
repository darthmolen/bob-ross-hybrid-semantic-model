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
- Always verify against the CSV source

When reviewing changes to episode files, use web search to fetch the CSV and confirm:
```
painting_index matches CSV row where season={X} AND episode={Y}
```

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
