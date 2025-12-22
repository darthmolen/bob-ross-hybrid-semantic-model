# Generate Bob Ross Season

Generate semantic index entries for a full season of Bob Ross episodes.

## Instructions

You are generating structured markdown entries for Bob Ross "Joy of Painting" episodes using the Hybrid Semantic Model.

**Season to process:** $ARGUMENTS

## Steps

1. **Fetch episode data** for the specified season from:
   - https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv
   - Filter to the requested season number
   - Build a list of episodes to process (typically 13 per season)
   - **CRITICAL: Extract the `painting_index` column value for each episode** (see Image Numbering section below)

2. **Spawn parallel subagents using the Task Tool**

   **IMPORTANT: Use the Task tool to process episodes in parallel, not sequentially.**

   For each episode in the season, spawn a separate Task subagent:

   ```
   Task: "Process Season X Episode Y - {Title}"

   Instructions for subagent:
   1. Check for painting image in local images/ folder first:
      - Local path: /home/user/bob-ross-hybrid-semantic-model/images/painting{index}.png
      - If found, use the local image
      - If not found, fallback to GitHub URL: https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/paintings/painting{index}.png

   2. Analyze the image using Claude's vision capabilities

   3. Generate the complete 8-section markdown entry following the template at:
      /home/user/bob-ross-hybrid-semantic-model/TEMPLATE.md

   ⚠️ **CRITICAL: Section headings MUST be numbered exactly like this:**
      - ## 1. Composition
      - ## 2. Palette
      - ## 3. Mood & Atmosphere
      - ## 4. Structural Layout
      - ## 5. Motion
      - ## 6. Technique
      - ## 7. Narrative Layer
      - ## 8. Initial Canvas Treatment

   **DO NOT omit the numbers. "## Composition" is WRONG. "## 1. Composition" is CORRECT.**

   4. Include all semantic identity tags inline in the text:
      - palette_identity
      - depth_style
      - lighting_type
      - motion_profile
      - composition_archetype

   ⚠️ **CRITICAL: Tag Value Formatting**
      - Use **Title Case with Spaces** for all tag values
      - ✅ CORRECT: "Layered Mountain Valley with Lake Reflection"
      - ✅ CORRECT: "Warm Sunset Radiance with Cool Mountain Tones"
      - ❌ WRONG: "layered_mountain_valley_with_lake_reflection" (snake_case)
      - ❌ WRONG: "layered mountain valley" (all lowercase)
      - Format inline tags as: **tag_name**: Tag Value in Title Case
      - Use the SAME formatting in both inline text AND YAML metadata

   5. **REQUIRED: Add YAML metadata section at the end of the file**
      The metadata MUST be wrapped in code fences exactly like this:

      ---

      ```yaml
      tags:
        composition_archetype: "..."
        palette_identity: "..."
        depth_style: "..."
        lighting_type: "..."
        motion_profile: "..."

      episode:
        season: X
        episode: Y
        title: "..."
        year: YYYY
        painting_index: NNN

      colors:
        - Color1
        - Color2
      ```

      ⚠️ **CRITICAL CODE FENCE REQUIREMENTS:**
      - You MUST include the opening fence: ```yaml (three backticks + yaml)
      - You MUST include the closing fence: ``` (three backticks alone on a line)
      - Missing either fence will break YAML parsing
      - The --- horizontal rule comes BEFORE the code fence
      - Verify your output includes BOTH fences before writing the file

   6. WRITE the file directly to:
      /home/user/bob-ross-hybrid-semantic-model/season-{XX}/s{XX}e{YY}-{title-slug}.md

   7. Return confirmation: "Episode {Y}: {Title} - COMPLETED"
   ```

   **Launch all subagents concurrently in a single response.** Each subagent independently:
   - Reads the painting image (local or remote)
   - Analyzes all 8 sections
   - Generates semantic identity tags
   - **Writes its own markdown file directly**
   - Reports completion

3. **Verify completion**

   After all Task agents complete:
   - Check how many episodes were successfully written
   - Verify files exist in the season-{XX}/ folder
   - Report any failures or missing episodes

4. **Generate SOURCE_IMAGES.md manifest**

   Create a manifest file documenting the image sources used for each episode:

   **File:** `/home/user/bob-ross-hybrid-semantic-model/season-{XX}/SOURCE_IMAGES.md`

   **Format:**
   ```markdown
   # Season {XX} Source Images

   This file documents the painting images used to generate the semantic entries for Season {XX}.

   | Episode | Title | Painting Index | Image Source |
   |---------|-------|----------------|--------------|
   | S{XX}E01 | {Title} | {painting_index} | [local/github] painting{index}.png |
   | S{XX}E02 | {Title} | {painting_index} | [local/github] painting{index}.png |
   | ... | ... | ... | ... |

   ## Source URLs

   - **Local images:** `/home/user/bob-ross-hybrid-semantic-model/images/painting{index}.png`
   - **GitHub fallback:** `https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/paintings/painting{index}.png`

   ## CSV Data Source

   Episode metadata from: `https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv`

   Generated: {YYYY-MM-DD}
   ```

   This manifest provides traceability for:
   - Which painting image was analyzed for each episode
   - Whether local or remote images were used
   - The painting_index mapping for verification

5. **Commit and push to git**

   Once all episodes and the SOURCE_IMAGES.md manifest are written:
   ```bash
   git checkout -b claude/season-{XX}-generation-{ID}
   git add season-{XX}/*.md
   git add season-{XX}/SOURCE_IMAGES.md
   git commit -m "Generate Season {XX} episodes (X/13)"
   git push -u origin claude/season-{XX}-generation-{ID}
   ```

6. **Note:** INDEX.md updates happen separately using `/update-index` or `/rebuild-index`

## ⚠️ Image Numbering — CRITICAL

The `painting{index}.png` filename uses the **`painting_index` column** from the CSV dataset. This is **NOT**:
- ❌ The episode number (1-13)
- ❌ The row number in the CSV
- ❌ A sequential number per season

**The `painting_index` is a unique identifier for each painting in the entire Bob Ross catalog.**

### How to find the correct painting_index

1. Fetch the CSV: `https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/master/data/bob_ross_paintings.csv`
2. Filter rows where `season` equals your target season
3. For each episode, read the **`painting_index`** column value
4. Use that value in the image filename: `painting{painting_index}.png`

### Example: Season 3 (from actual CSV data)

| Episode | Title | painting_index | Image File |
|---------|-------|----------------|------------|
| S03E01 | Mountain Retreat | 256 | painting256.png |
| S03E02 | Blue Moon | 257 | painting257.png |
| S03E03 | Bubbling Stream | 258 | painting258.png |
| ... | ... | ... | ... |
| S03E13 | Peaceful Waters | 268 | painting268.png |

### ⚠️ DO NOT USE FORMULAS

**There is NO formula to calculate painting_index.** The `painting_index` values in the CSV do NOT follow a predictable pattern:

- Season 1, Episode 1 has `painting_index = 282` (not 1!)
- Season 3 has indices 256-268 (not 27-39!)
- Season 6 has indices 217-229 (not 66-78!)
- The indices are NOT sequential by season

**You MUST read the actual `painting_index` column from the CSV for each episode.** Never try to calculate or guess these values.

### Verification

Before spawning subagents, verify you have the correct painting indices by logging them:
```
Season 3 Episodes (from CSV):
- S03E01 "Mountain Retreat" -> painting_index: 256
- S03E02 "Blue Moon" -> painting_index: 257
...
```

---

## Parallel Processing Notes

- Spawn all episode tasks simultaneously in a SINGLE response—do NOT process sequentially
- Each subagent operates independently with its own context
- Each subagent WRITES ITS OWN FILE directly (no sequential bottleneck)
- Main agent only coordinates and verifies completion
- This achieves TRUE parallel processing:
  - 13 parallel image analyses ✓
  - 13 parallel file writes ✓
- Total processing time: ~same as slowest single episode (vs 13x sequential)
- If a subagent fails, note the failure and continue with others

## Output Format

Each episode file MUST follow this structure, including the YAML metadata section:

```markdown
# Season X, Episode Y — "Title" (Year)

## 1. Composition
[bullets]

## 2. Palette
[bullets + palette_identity]

## 3. Mood & Atmosphere
[bullets + lighting type]

## 4. Structural Layout
[bullets + depth_style]

## 5. Motion
[bullets + motion_profile]

## 6. Technique
[bullets]

## 7. Narrative Layer
[short paragraph]

## 8. Initial Canvas Treatment
[bullets]

---

```yaml
tags:
  composition_archetype: "[from section 1]"
  palette_identity: "[from section 2]"
  depth_style: "[from section 4]"
  lighting_type: "[from section 3]"
  motion_profile: "[from section 5]"

episode:
  season: X
  episode: Y
  title: "Title"
  year: YYYY
  painting_index: NNN

colors:
  - [Bob Ross colors from section 2]
```
```

## ⚠️ YAML Metadata Section — REQUIRED

**Every episode file MUST include the YAML metadata block at the end.** This is NOT optional. The metadata section provides:
- Structured semantic identity tags for programmatic access
- Episode identification (season, episode, title, year, painting_index)
- Color palette array for searchability

Extract the tag values from the inline content in each section (e.g., `Palette identity: **dark woodland palette**` becomes `palette_identity: "dark woodland palette"`).

## Style Rules

- Concise bullet lists for structured fields
- Short descriptive paragraphs for narrative
- Consistent terminology across episodes
- No subjective critique
- No conversational language
- No references to the indexing process

## ⚠️ Official Bob Ross Colors — ONLY USE THESE

The `colors` array in the YAML metadata must ONLY include colors from this official list:

**Oil Colors (13):**
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

**Mediums (used for thinning/base coats):**
- Liquid White
- Liquid Black
- Liquid Clear

**DO NOT use:**
- Invented colors (e.g., "Lavender", "Sky Blue", "Forest Green")
- Color descriptions (e.g., "warm brown", "deep blue")
- Mixed color names (e.g., "Blue-Green")

If a color appears in the painting that isn't on this list, identify which official colors were mixed to create it, and list only those official colors.

## Example

See Season 2, Episode 6 "Black River" as the reference implementation.

## After Completion

Report:
- Number of episodes successfully written (verify with `ls season-{XX}/*.md`)
- Confirm SOURCE_IMAGES.md manifest was generated (verify with `cat season-{XX}/SOURCE_IMAGES.md`)
- Any episodes that failed (missing images, errors, etc.)
- The painting_index range used (e.g., "Used painting indices 27-39 for Season 3")
- Git commit status and branch name
- Reminder: Run `/update-index` after merging to main
