# Update Index

Incrementally update INDEX.md by adding new episodes that aren't already indexed.

## Instructions

You are updating the INDEX.md file to include newly added episodes. This command performs an INCREMENTAL UPDATE, preserving existing content.

## Steps

1. **Read the current INDEX.md file**
   - Parse existing episodes to build a list of what's already indexed
   - Note the current structure and format

2. **Scan all season folders** (`season-01/` through `season-31/`)
   - Find all episode markdown files matching pattern: `s??e??-*.md`
   - Compare against existing INDEX.md entries
   - Identify NEW episodes that need to be added

3. **Extract metadata from NEW episodes only:**
   - Season and episode number (from filename)
   - Title (from first heading)
   - Semantic identity tags:
     - `palette_identity`
     - `depth_style`
     - `lighting_type`
     - `motion_profile`
     - `composition_archetype`
   - Parse these from the markdown content

4. **Update INDEX.md sections:**

   **Quick Reference Table:**
   - Add new rows in proper order (by season/episode number)
   - Maintain consistent formatting with existing entries

   **Episodes by Season:**
   - Add new episodes to their respective season sections
   - Create new season sections if needed
   - Maintain chronological order

   **Episodes by Tag:**
   - Add new episodes to existing tag groupings
   - Create new tag groupings if new tag values appear
   - Keep tag sections organized alphabetically

5. **Preserve existing content:**
   - Don't remove or modify existing episode entries
   - Maintain the current structure and formatting
   - Only ADD new content

6. **Update metadata:**
   - Update "Total Episodes Indexed" count
   - Update "Last Updated" date

## Strategy

This command uses an additive approach:
- Reads existing INDEX.md
- Identifies gaps (episodes in folders but not in index)
- Adds only the missing episodes
- Faster than full rebuild for incremental updates

## When to Use

Use `/update-index` when:
- You've just merged a new season branch
- You've added a handful of new episodes
- You want to preserve manual edits to INDEX.md
- You want a faster update than full rebuild

Use `/rebuild-index` when:
- You want a completely fresh index
- You've made structural changes to episode files
- You want to ensure perfect synchronization
- You've reorganized semantic tags

## After Completion

Report:
- Number of NEW episodes added
- Seasons updated
- Any episodes with missing semantic tags
- Confirmation that existing entries were preserved
