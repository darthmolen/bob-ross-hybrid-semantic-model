# Bob Ross Semantic Index

A hybrid semantic model for all 403 Bob Ross "Joy of Painting" episodes, enabling natural language querying and exploration of painting characteristics, techniques, and compositional elements.

## Project Overview

This repository catalogs every Bob Ross painting episode using layered meaning, compositional analysis, and technical metadata. Each episode is analyzed across eight semantic dimensions to support natural-language search, filtering, and cross-episode comparison.

## Repository Structure

```
bob-ross-semantic-index/
├── README.md                    # This file
├── INDEX.md                     # Master list with links to all episodes
├── TEMPLATE.md                  # The hybrid semantic model template
├── season-01/
│   ├── s01e01-a-walk-in-the-woods.md
│   ├── s01e02-mt-mckinley.md
│   └── ...
├── season-02/
│   ├── s02e01-meadow-lake.md
│   └── ...
└── ... (seasons 01-31)
```

## Hybrid Semantic Model

Each episode entry contains eight structured sections:

1. **Composition** - Physical layout, landforms, water features, vegetation, sky, structures
2. **Palette** - Dominant colors, warm/cool relationships, color roles
3. **Mood & Atmosphere** - Emotional tone, lighting type, atmospheric qualities
4. **Structural Layout** - Spatial arrangement (left/right/center, foreground/midground/background)
5. **Motion** - Implied movement (water flow, cloud drift, compositional flow)
6. **Technique** - Brush types, knife work, blending methods, special effects
7. **Narrative Layer** - Interpretive description, emotional meaning, story
8. **Initial Canvas Treatment** - Foundation (Liquid White/Clear, gesso, masking)

See [TEMPLATE.md](TEMPLATE.md) for the complete template specification.

## Semantic Identity Tags

Episodes include optional tags for advanced filtering:

- `palette_identity` - e.g., "dark woodland palette with luminous water highlights"
- `depth_style` - e.g., "tunnel-like depth", "atmospheric fade", "silhouette depth"
- `lighting_type` - e.g., "backlit glow", "diffuse", "stormy"
- `motion_profile` - e.g., "center-pull perspective", "horizontal drift"
- `composition_archetype` - e.g., "forest corridor", "mountain reflection", "oceanscape"

## Quick Reference

- **Total Episodes**: 403 (31 seasons, 1983-1994)
- **Episode Length**: ~26 minutes each
- **Official Channel**: [Bob Ross YouTube](https://www.youtube.com/user/BobRossInc)

## Data Sources

- [GitHub Dataset](https://github.com/jwilber/Bob_Ross_Paintings) - CSV metadata, images
- [TwoInchBrush.com](https://www.twoinchbrush.com/all-paintings) - Complete painting database
- [Wikipedia Episode List](https://en.wikipedia.org/wiki/List_of_The_Joy_of_Painting_episodes)

## Usage

Browse the [INDEX.md](INDEX.md) for a searchable master list of all episodes with semantic tags and direct links to episode markdown files.

Raw GitHub URLs for programmatic access:
```
https://raw.githubusercontent.com/{username}/bob-ross-semantic-index/main/season-02/s02e06-black-river.md
```

## AI Chat Client Integration

This semantic model is optimized for use with AI assistants like Claude, ChatGPT, GitHub Copilot, and others. The structured format enables natural language queries about Bob Ross paintings, techniques, and compositional elements.

See [AI-CLIENT-CHAT-USAGE.md](AI-CLIENT-CHAT-USAGE.md) for detailed instructions on:
- Querying the dataset with AI chat clients
- Platform-specific usage (Claude, ChatGPT, Copilot)
- Example prompts for finding paintings, learning techniques, and analysis
- Tips for getting the best results

## Contributing

This is a personal project focused on semantic richness and natural language accessibility. Episode entries follow strict style requirements:

- Concise bullet lists for structured fields
- Short descriptive paragraphs for narrative sections
- Consistent terminology across episodes
- No subjective critique; focus on semantic clarity
- Each episode self-contained and searchable

## License

Episode descriptions and semantic analysis are original work. Bob Ross paintings and "The Joy of Painting" are properties of Bob Ross Inc.
