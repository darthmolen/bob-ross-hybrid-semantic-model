---
applyTo:
  - "season-**/s??e??-*.md"
  - "**/SOURCE_IMAGES.md"
---

# Semantic Model Episode Review Instructions

When reviewing Bob Ross episode semantic model files, perform these validations:

## CSV Cross-Reference (REQUIRED)

The authoritative data source is:
`https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv`

### Mandatory Checks:

1. **painting_index**: Must match CSV exactly for this season/episode combination

   **⚠️ DO NOT GUESS - VERIFY FIRST**: The painting_index mapping is non-sequential and cannot be calculated. Before flagging ANY painting_index issue:

   1. **Fetch the actual CSV** from the URL above
   2. **Locate the row** where `season` and `episode` columns match the file under review
   3. **Extract the `painting_index`** from that specific row
   4. **Compare** the CSV value against the file's YAML `painting_index`
   5. **Only flag if there is a verified mismatch**

   If you cannot fetch or read the CSV, **skip painting_index validation entirely** - do not assume the index is wrong

2. **Episode Title**: Must match CSV `title` field exactly (including punctuation)

3. **Year**: Should match the CSV data or be historically accurate for that season

## Semantic Tag Validation

Verify all 5 required tags are present and reasonable:

```yaml
tags:
  composition_archetype: # e.g., "mountain reflection", "forest corridor"
  palette_identity:      # e.g., "dark woodland palette with luminous highlights"
  depth_style:           # e.g., "tunnel depth", "atmospheric fade"
  lighting_type:         # e.g., "backlit glow", "diffuse", "sunset"
  motion_profile:        # e.g., "center-pull perspective", "horizontal drift"
```

## Color List Validation

Cross-check colors against:
1. Bob Ross standard palette (13 colors)
2. The CSV `colors` column for this episode
3. Web search for "Bob Ross [episode title] colors used"

Standard colors: Alizarin Crimson, Bright Red, Cadmium Yellow, Dark Sienna, Indian Yellow, Midnight Black, Phthalo Blue, Phthalo Green, Prussian Blue, Sap Green, Titanium White, Van Dyke Brown, Yellow Ochre

## Content Accuracy

Use web search to verify semantic descriptions match the actual painting:
- Search for "Bob Ross [episode title]" images
- Verify composition elements (mountains, water, trees, structures) are accurate
- Check that mood/atmosphere descriptions align with the painting

## Section Structure

Ensure all 8 sections are present with appropriate content:
1. Composition - landforms, water, vegetation, sky, structures
2. Palette - colors and relationships
3. Mood & Atmosphere - tone and lighting
4. Structural Layout - spatial arrangement
5. Motion - flow and movement
6. Technique - brushes and methods
7. Narrative Layer - 2-4 sentence interpretation in quotes
8. Initial Canvas Treatment - foundation preparation

## Common Issues to Flag

- Missing or incorrect painting_index **(only after CSV verification - never guess)**
- Episode title doesn't match CSV **(only after CSV verification)**
- Colors not in standard Bob Ross palette
- Missing semantic identity tags
- Empty or placeholder sections
- Narrative layer not in quotation marks
- YAML metadata malformed or incomplete
