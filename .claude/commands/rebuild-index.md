# Rebuild Index

Completely rebuild the INDEX.md file from scratch by scanning all episode files across all seasons.

## Instructions

You are rebuilding the master INDEX.md file for the Bob Ross Semantic Index project. This command performs a FULL REBUILD from scratch.

## Steps

1. **Scan all season folders** (`season-01/` through `season-31/`)
   - Find all episode markdown files matching pattern: `s??e??-*.md`
   - Read each file to extract metadata

2. **Extract metadata from each episode file:**
   - Season and episode number (from filename)
   - Title (from first heading)
   - Semantic identity tags:
     - `palette_identity`
     - `depth_style`
     - `lighting_type`
     - `motion_profile`
     - `composition_archetype`
   - Parse these from the markdown content (look for "Palette identity:", "Depth style:", etc.)

3. **Build the complete INDEX.md structure:**

```markdown
# Bob Ross Episode Index

A comprehensive semantic index of all 403 "The Joy of Painting" episodes (1983-1994).

## Quick Reference Table

| Season | Episode | Title | Palette Identity | Depth Style | Lighting | Link |
|--------|---------|-------|------------------|-------------|----------|------|
| 1 | 1 | A Walk in the Woods | ... | ... | ... | [view](https://raw.githubusercontent.com/darthmolen/bob-ross-hybrid-semantic-model/main/season-01/s01e01-a-walk-in-the-woods.md) |
...

## Episodes by Season

### Season 1 (1983)
- [Episode 1: A Walk in the Woods](season-01/s01e01-a-walk-in-the-woods.md)
- ...

### Season 2 (1983-1984)
- [Episode 1: Meadow Lake](season-02/s02e01-meadow-lake.md)
- ...

## Episodes by Tag

### Palette Identity

#### Alpine Palettes
- S01E13: Final Reflections - bright alpine palette with golden autumn accents
- S02E01: Meadow Lake - bright alpine palette with golden autumn accents
- ...

#### Dark Woodland Palettes
- S02E06: Black River - dark woodland palette with luminous water highlights
- ...

### Depth Style

#### Atmospheric Fade
- S01E01: A Walk in the Woods
- S02E05: Autumn Splendor
- ...

#### Tunnel Depth
- S02E06: Black River - tunnel-like depth with strong value contrast
- ...

### Lighting Type

#### Backlit Glow
- S02E06: Black River
- ...

#### Direct Sunlight
- S01E13: Final Reflections
- ...

### Motion Profile

#### Static Reflection
- S01E13: Final Reflections
- ...

### Composition Archetype

#### Mountain-Lake Reflections
- S01E13: Final Reflections
- ...

#### Forest Corridors
- S02E06: Black River
- ...

## Search Tips

- Search for specific colors: "Alizarin Crimson", "Cadmium Yellow"
- Search for techniques: "palette knife", "fan brush", "black gesso"
- Search for elements: "cabin", "waterfall", "ocean waves"
- Search for moods: "peaceful", "dramatic", "mysterious"
- Combine tags for precise queries: "tunnel depth" + "backlit glow"

---

**Total Episodes Indexed:** [count]
**Last Updated:** [date]
```

4. **Write the complete INDEX.md file** to the repository root

5. **Report statistics:**
   - Total episodes indexed
   - Episodes per season
   - Most common palette identities
   - Most common depth styles
   - Any missing episodes or incomplete metadata

## Important Notes

- This is a FULL REBUILD - it overwrites the existing INDEX.md completely
- Reads ALL episode files from scratch
- Use this when you want to ensure INDEX.md is fully synchronized with episode files
- Groups episodes by semantic tags for easy natural-language searching
- Includes both relative links (for GitHub) and raw URLs (for external access)

## After Completion

Report:
- Number of episodes indexed
- Seasons covered
- Any episodes with missing semantic tags
- Summary of tag distributions
