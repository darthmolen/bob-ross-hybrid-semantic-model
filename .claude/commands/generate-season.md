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
   1. Fetch painting image from: {img_src_url}
   2. Analyze the image using Claude's vision capabilities
   3. Generate the 8-section markdown entry following the template
   4. Include all semantic identity tags
   5. Return the complete markdown content
   ```

   Launch all 13 subagents concurrently. Each subagent handles:

   a. Fetching the painting image from the `img_src` URL

   b. Vision analysis to generate all 8 sections:
      - Composition
      - Palette
      - Mood & Atmosphere
      - Structural Layout
      - Motion
      - Technique
      - Narrative Layer
      - Initial Canvas Treatment

   c. Generating semantic identity tags:
      - palette_identity
      - depth_style
      - lighting_type
      - motion_profile
      - composition_archetype

   d. Returning formatted markdown

3. **Collect results from all subagents**

   As each Task completes, collect the markdown output.

4. **Save each episode** as:
   ```
   season-{XX}/s{XX}e{YY}-{title-slug}.md
   ```

5. **Update INDEX.md** with new entries including tags and raw URLs

## Parallel Processing Notes

- Spawn all episode tasks simultaneously—do NOT process sequentially
- Each subagent operates independently with its own context
- Main agent coordinates and collects results
- This dramatically reduces total processing time (13 parallel vs 13 sequential)
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
- Number of episodes processed
- Any episodes that couldn't be analyzed (missing images, etc.)
- List of generated files
