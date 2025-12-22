# Update Season Formatting

Apply current formatting guidelines to an existing season's episode files without regenerating content.

## Instructions

**Season to update:** $ARGUMENTS

This command fixes formatting issues in existing episode files to match current standards, preserving the semantic content.

## Formatting Rules to Apply

### 1. Identity Label Format

Each section should end with an identity label in this format:
```
Label: **value**
```

**Fix these patterns:**
| Wrong Pattern | Correct Pattern |
|--------------|-----------------|
| `**Palette identity**: value` | `Palette identity: **value**` |
| `**palette_identity**: value` | `Palette identity: **value**` |
| `**Palette identity: "value"**` | `Palette identity: **value**` |
| `- **palette_identity**: value` | `Palette identity: **value**` |
| Inline at end of paragraph | Extract to standalone line |

**Labels by section:**
- Section 2: `Palette identity: **value**`
- Section 3: `Lighting: **value**` (optionally with additional text)
- Section 4: `Depth style: **value**`
- Section 5: `Motion profile: **value**`
- Section 6: `Signature technique: **value**`

### 2. Colors YAML Array

Remove canvas treatments from the `colors` array:
- Liquid White
- Liquid Black
- Liquid Clear
- Black Gesso
- Grey Gesso

These should only be mentioned in prose (Sections 6 & 8), not in the YAML.

### 3. Section Numbering

Ensure all section headers are numbered:
- `## 1. Composition` (not `## Composition`)
- `## 2. Palette`
- etc.

## Steps

1. **List episode files** in the specified season folder:
   ```
   /home/user/bob-ross-hybrid-semantic-model/season-{XX}/s{XX}e??-*.md
   ```

2. **For each episode file**, read the content and apply fixes:

   a. **Fix identity label formatting:**
      - Find patterns like `**Label**: value` or `**label_name**: value`
      - Convert to `Label: **value**`
      - Remove quotes from values
      - Extract inline tags to standalone lines
      - Convert snake_case to Title Case

   b. **Fix colors YAML array:**
      - Remove Liquid White, Liquid Black, Liquid Clear
      - Remove Black Gesso, Grey Gesso
      - Keep only actual paint colors

   c. **Fix section numbering** if missing

3. **Write the corrected file** back

4. **Report changes:**
   - List each file processed
   - Summarize what was fixed in each file
   - Note any files that couldn't be processed

## Example Usage

```
/update-season 16
```

This would process all 13 episodes in season-16/ and fix formatting issues.

## Processing Notes

- Read each file completely before making changes
- Preserve all semantic content (descriptions, narratives, etc.)
- Only modify formatting, not meaning
- Use Edit tool for targeted fixes rather than rewriting entire files
- Process files sequentially to avoid conflicts

## After Completion

Report:
- Number of files processed
- Summary of fixes applied per file type:
  - Identity label fixes
  - Color array cleanups
  - Section numbering fixes
- Any files that had no issues
- Any errors encountered

Then commit changes:
```bash
git add season-{XX}/*.md
git commit -m "Update Season {XX} formatting to current standards"
```
