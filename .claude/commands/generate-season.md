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

   4. Include all semantic identity tags:
      - palette_identity
      - depth_style
      - lighting_type
      - motion_profile
      - composition_archetype

   5. WRITE the file directly to:
      /home/user/bob-ross-hybrid-semantic-model/season-{XX}/s{XX}e{YY}-{title-slug}.md

   6. Return confirmation: "Episode {Y}: {Title} - COMPLETED"
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

4. **Commit and push to git**

   Once all episodes are written:
   ```bash
   git checkout -b claude/season-{XX}-generation-IDp4y
   git add season-{XX}/*.md
   git commit -m "Generate Season {XX} episodes (X/13)"
   git push -u origin claude/season-{XX}-generation-IDp4y
   ```

5. **Note:** INDEX.md updates happen separately using `/update-index` or `/rebuild-index`

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

Each episode file should follow this structure:

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
```

## Style Rules

- Concise bullet lists for structured fields
- Short descriptive paragraphs for narrative
- Consistent terminology across episodes
- No subjective critique
- No conversational language
- No references to the indexing process

## Example

See Season 2, Episode 6 "Black River" as the reference implementation.

## After Completion

Report:
- Number of episodes successfully written (verify with ls season-{XX}/*.md)
- Any episodes that failed (missing images, errors, etc.)
- Git commit status and branch name
- Reminder: Run `/update-index` after merging to main
