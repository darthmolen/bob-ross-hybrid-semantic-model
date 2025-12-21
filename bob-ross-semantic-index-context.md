# Bob Ross Semantic Index Project

A personal project to create a hybrid semantic model for all 403 Bob Ross "Joy of Painting" episodes, enabling natural language querying via Copilot, Claude, or a Semantic Kernel agent.

---

## Project Goals

- Catalog every Bob Ross painting episode using layered meaning, compositional analysis, and technical metadata
- Support natural-language search, filtering, and cross-episode comparison
- Store as markdown files on GitHub for URL context access
- Query on-the-go via mobile (Copilot/Claude)

---

## Data Sources

Existing datasets to bootstrap from:

- **GitHub Dataset**: https://github.com/jwilber/Bob_Ross_Paintings
  - CSV with metadata: title, season, episode, colors used, hex codes, YouTube links, featured items
  - PNG images for each painting
  
- **TwoInchBrush.com**: https://www.twoinchbrush.com/all-paintings
  - Complete database of all 403 paintings
  - Color search, season filtering
  
- **Wikipedia Episode List**: https://en.wikipedia.org/wiki/List_of_The_Joy_of_Painting_episodes

---

## Repository Structure

```
bob-ross-semantic-index/
├── README.md
├── INDEX.md                    # Master list with links to all episodes
├── TEMPLATE.md                 # The hybrid semantic model template
├── season-01/
│   ├── s01e01-a-walk-in-the-woods.md
│   ├── s01e02-mt-mckinley.md
│   └── ...
├── season-02/
│   ├── s02e01-meadow-lake.md
│   ├── s02e06-black-river.md
│   └── ...
└── ... (seasons 01-31)
```

Raw GitHub URLs for context:
```
https://raw.githubusercontent.com/{username}/bob-ross-semantic-index/main/season-02/s02e06-black-river.md
```

---

## Hybrid Semantic Model Template

Each episode entry must contain the following eight sections:

### 1. Composition
Describe the physical layout:
- Landforms
- Water features
- Trees and vegetation
- Sky conditions
- Presence/absence of structures
- Overall compositional archetype

### 2. Palette
List the dominant colors and their functional roles:
- Warm vs cool
- High-contrast vs low-contrast
- Signature color relationships
- Palette identity phrase

### 3. Mood & Atmosphere
Capture the emotional and atmospheric qualities:
- Tone (peaceful, dramatic, mysterious, etc.)
- Lighting type (diffuse, backlit, glowing, stormy)
- Emotional resonance

### 4. Structural Layout
Break down the spatial arrangement:
- Left / Right / Center
- Foreground / Midground / Background
- Depth style (atmospheric fade, tunnel depth, silhouette depth, etc.)

### 5. Motion
Identify any implied or explicit motion:
- Water flow
- Wave direction
- Cloud drift
- Compositional flow lines
- Atmospheric motion

### 6. Technique
List the technical methods used:
- Brush types
- Knife work
- Blending methods
- Reflection techniques
- Special effects (mist, glow, translucency)

### 7. Narrative Layer
Provide a short interpretive description:
- What story the painting suggests
- Emotional or symbolic meaning
- How the elements interact

### 8. Initial Canvas Treatment
Document the foundation:
- Liquid White / Liquid Clear
- Black gesso or dark underpainting
- Contact paper or masking
- Any special surface prep

---

## Semantic Identity Tags

Optional tags for advanced filtering and natural-language queries:

- `palette_identity` - e.g., "dark woodland palette with luminous water highlights"
- `depth_style` - e.g., "tunnel-like depth", "atmospheric fade", "silhouette depth"
- `lighting_type` - e.g., "backlit glow", "diffuse", "stormy"
- `motion_profile` - e.g., "center-pull perspective", "horizontal drift"
- `composition_archetype` - e.g., "forest corridor", "mountain reflection", "oceanscape"

---

## Style Requirements

- Use concise bullet lists for structured fields
- Use short descriptive paragraphs for narrative sections
- Maintain consistent terminology across episodes
- Avoid subjective critique; focus on semantic clarity
- Keep each episode self-contained and searchable
- No conversational language
- No references to the indexing process

---

## Example Entry: Season 2, Episode 6 — "Black River" (1984)

### 1. Composition
- Narrow river flowing toward the viewer
- Dense dark forest on both sides
- Soft distant tree line
- Subtle background glow
- No mountains
- No structures

A dark-toned forest-and-river corridor composition.

### 2. Palette
- Deep blacks and dark blues (underpainting)
- Earthy browns
- Cool greens for foliage
- Titanium white for water highlights
- Soft yellow-white glow in the distance

Palette identity: **dark woodland palette with luminous water highlights**

### 3. Mood & Atmosphere
- Mysterious
- Quiet
- Slightly dramatic
- Cool and shaded
- Depth emerging from darkness

Lighting: **backlit glow** illuminating the river and distant trees.

### 4. Structural Layout
- **Left:** Dense trees leaning inward
- **Right:** Matching forest mass
- **Center:** River reflecting distant light
- **Foreground:** Grassy banks and water highlights
- **Background:** Soft glow behind distant trees

Depth style: **tunnel-like depth with strong value contrast**

### 5. Motion
- Gentle river flow toward the viewer
- Subtle foam streaks
- Faint upward atmospheric glow
- Compositional flow: **center-pull perspective**

### 6. Technique
- Dark toned canvas (early black-gesso-style approach)
- Fan-brush evergreens and bushes
- Knife-scraped tree trunks
- Pull-down reflections for water
- Horizontal smoothing strokes
- Liner brush twigs and grasses

Signature technique: **light water highlights over a dark river base**

### 7. Narrative Layer
"A quiet, shadowed river winding through a dark forest.
The distant glow adds mystery and depth, while the water catches the faintest hints of light."

### 8. Initial Canvas Treatment
- Dark toned canvas
- Liquid White applied selectively for glow and water
- No contact paper
- No masking
- No textured gesso

A foundational dark-base woodland scene emphasizing contrast and atmospheric depth.

---

## Generation Approach

### Option A: Claude Code Task Tool (Parallel)
Fan out vision analysis across all 403 images. Each subagent:
1. Fetches painting image from existing dataset
2. Analyzes against the 8-section template
3. Generates structured markdown
4. Saves to `/episodes/season-XX/episode-YY-title.md`

### Option B: Batch Python Script
```python
# Pseudocode
for episode in episodes_csv:
    image_url = episode['img_src']
    response = claude_api.analyze_image(
        image=image_url,
        prompt=TEMPLATE_PROMPT
    )
    save_markdown(response, episode)
```

### Option C: Season-at-a-Time Slash Command
Create `.claude/commands/generate-season.md` that processes 13 episodes per run with QA between seasons.

---

## Querying Architecture

Simple personal setup using GitHub + Claude/Copilot clients:

```
┌─────────────────────────────────────────────┐
│  You (mobile/desktop)                        │
│  "Show me dramatic winter scenes with        │
│   tunnel depth from seasons 10-15"           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Claude / Copilot Client                     │
│  - Fetch INDEX.md gist for episode lookup   │
│  - Fetch specific episode markdown via      │
│    raw GitHub URLs                          │
│  - Natural language search across context   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  GitHub Storage                              │
│  ├── Gist: INDEX.md (master lookup)         │
│  │   - All episodes with tags & links       │
│  │   - Searchable metadata summary          │
│  └── Repo: Raw markdown files               │
│       - 403 individual episode entries      │
│       - Directly fetchable URLs             │
└─────────────────────────────────────────────┘
```

### How It Works

1. **INDEX.md Gist** - A single searchable document with:
   - Every episode title, season, episode number
   - Key semantic tags (palette_identity, depth_style, lighting_type, etc.)
   - Raw GitHub URL to full episode markdown
   
2. **Query Flow**:
   - Ask Claude/Copilot to fetch the INDEX gist
   - Describe what you're looking for naturally
   - Claude/Copilot identifies matching episodes from index
   - Fetches full episode markdown(s) for detailed info

3. **Example Prompts**:
   ```
   "Fetch this gist: [INDEX_URL] and find me peaceful lake scenes with atmospheric fade"
   
   "From the Bob Ross index, which episodes use black gesso underpainting?"
   
   "Get the full entry for Season 2 Episode 6 Black River"
   ```

### INDEX.md Format

```markdown
# Bob Ross Episode Index

## Quick Reference
| S | E | Title | Palette | Depth | Lighting | Link |
|---|---|-------|---------|-------|----------|------|
| 1 | 1 | A Walk in the Woods | earth tones | atmospheric fade | diffuse | [raw](url) |
| 2 | 6 | Black River | dark woodland | tunnel depth | backlit glow | [raw](url) |
...

## By Tag

### Depth Style: Tunnel Depth
- S02E06 Black River
- S05E12 ...

### Lighting: Backlit Glow
- S02E06 Black River
- ...

### Palette: Dark Woodland
- S02E06 Black River
- ...
```

### URL Patterns

**Gist (INDEX.md)**:
```
https://gist.githubusercontent.com/{username}/{gist_id}/raw/INDEX.md
```

**Repo (episode files)**:
```
https://raw.githubusercontent.com/{username}/bob-ross-semantic-index/main/season-02/s02e06-black-river.md
```

---

## Quick Reference: Bob Ross Palette Colors

Standard colors used across episodes:
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

Base coatings:
- Liquid White
- Liquid Clear
- Black Gesso
- Grey Gesso

---

## Notes

- 31 seasons, 403 episodes (1983-1994)
- Each episode ~26 minutes
- Bob Ross created 3 versions of each painting (reference, on-air, book detail)
- YouTube: Official Bob Ross channel has most episodes
- Twitch: Weekly marathons every Monday since 2015
