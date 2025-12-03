# Manifest Generation Script

## Overview

The `generate_manifest.py` script generates a correct, validated `manifest.json` for all skills in the repository. It addresses the critical issues identified in the manifest structure analysis:

1. **Incorrect Paths**: Flat/incomplete paths → Hierarchical paths with correct prefixes
2. **Duplicate Entries**: Same skill appearing multiple times → Single entry per skill
3. **Missing Reference Tracking**: No reference files listed → Complete reference file tracking
4. **Inconsistent Metadata**: Missing/incomplete metadata → Complete validated metadata

## Features

### 1. Skill Discovery
- Automatically finds all `SKILL.md` files in:
  - `universal/` directory
  - `toolchains/` directory
  - `examples/` directory
- Excludes `.claude/skills` deployment directory
- Discovers **89 skills** (as of 2025-12-03)

### 2. Metadata Extraction
- Reads `metadata.json` if present in skill directory
- Parses YAML frontmatter from `SKILL.md` as fallback
- Extracts:
  - Name, version, category
  - Toolchain, framework
  - Tags, requires
  - Author, license

### 3. Token Counting
- Uses `tiktoken` library (cl100k_base encoding) if available
- Falls back to character estimation (~4 chars/token) if not
- Calculates:
  - **Entry point tokens**: SKILL.md only
  - **Full tokens**: SKILL.md + all reference/example files

### 4. Git History Integration
- Extracts last commit date using `git log`
- Falls back to file modification time if git unavailable
- Formats as ISO date (YYYY-MM-DD)

### 5. Path Transformation
- Converts absolute paths to relative paths from repo root
- Ensures correct format:
  - `universal/{category}/{skill-name}/SKILL.md`
  - `toolchains/{language}/{category}/{skill-name}/SKILL.md`
  - `examples/{skill-name}/SKILL.md`

### 6. Classification
- Determines category: `universal`, `toolchain`, or `example`
- Extracts toolchain from path (e.g., `python`, `typescript`, `rust`)
- Identifies framework from path or skill name

### 7. Reference File Tracking
- Detects `references/` directory
- Detects `examples/` directory
- Lists all `.md` files as reference files
- Adds `has_references` boolean flag

### 8. Validation
- Path format validation (must start with universal/toolchains/examples)
- Path existence validation (file must exist)
- Duplicate detection (no duplicate skill names)
- Token count sanity checks (30-200 entry, 100-50000 full)
- Date format validation (YYYY-MM-DD)
- Version format validation (semver)
- Category validation (universal/toolchain/example)

## Usage

### Basic Usage

Generate new manifest:
```bash
python3 scripts/generate_manifest.py
```

This creates `manifest.json` in the repository root.

### Specify Output File

```bash
python3 scripts/generate_manifest.py --output manifest-new.json
```

### Dry Run (Preview Only)

```bash
python3 scripts/generate_manifest.py --dry-run
```

Shows what would be generated without writing file.

### Verbose Output

```bash
python3 scripts/generate_manifest.py --verbose
```

Shows detailed progress for each skill processed.

### Validate Existing Manifest

```bash
python3 scripts/generate_manifest.py --validate
```

Validates the existing `manifest.json` without generating.

## Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output FILE` | `-o` | Output file path (default: manifest.json) |
| `--validate` | | Validate existing manifest instead of generating |
| `--dry-run` | | Preview changes without writing file |
| `--verbose` | `-v` | Enable verbose output |
| `--help` | `-h` | Show help message |

## Output Format

The generated manifest follows this structure:

```json
{
  "version": "1.0.0",
  "repository": "https://github.com/bobmatnyc/claude-mpm-skills",
  "updated": "2025-12-03",
  "description": "Curated collection...",
  "skills": {
    "universal": [
      {
        "name": "skill-name",
        "version": "1.0.0",
        "category": "universal",
        "toolchain": null,
        "framework": null,
        "tags": ["tag1", "tag2"],
        "entry_point_tokens": 75,
        "full_tokens": 2500,
        "requires": [],
        "author": "Claude MPM Team",
        "updated": "2025-12-03",
        "source_path": "universal/category/skill-name/SKILL.md",
        "has_references": true,
        "reference_files": ["file1.md", "file2.md"]
      }
    ],
    "toolchains": {
      "python": [...],
      "typescript": [...],
      ...
    }
  },
  "metadata": {
    "total_skills": 89,
    "categories": {
      "universal": 27,
      "toolchains": 60,
      "examples": 2
    },
    "toolchains": {
      "python": 10,
      "typescript": 12,
      ...
    },
    "last_updated": "2025-12-03",
    "schema_version": "2.0.0"
  },
  "provenance": {
    "source_repository": "https://github.com/bobmatnyc/claude-mpm",
    "skills_repository": "https://github.com/bobmatnyc/claude-mpm-skills",
    "author": "Claude MPM Team",
    "license": "MIT",
    "attribution_required": true
  }
}
```

## Validation Rules

### Path Format
- ✅ Must start with: `universal/`, `toolchains/`, or `examples/`
- ✅ Must end with: `/SKILL.md`
- ✅ Must exist in filesystem
- ✅ Must be unique (no duplicates)

### Token Counts
- ⚠️ Warning if `entry_point_tokens` < 30 or > 200
- ⚠️ Warning if `full_tokens` < 100 or > 50000
- ❌ Error if `entry_point_tokens` > `full_tokens`

### Date Format
- ✅ Must match: `YYYY-MM-DD` (ISO 8601)
- ✅ Must be valid date

### Version Format
- ⚠️ Warning if not semver format (e.g., `1.0.0`)

### Category
- ✅ Must be: `universal`, `toolchain`, or `example`

## Comparison: Old vs New Manifest

### Statistics
| Metric | Old | New |
|--------|-----|-----|
| Total Skills | 69 | 89 |
| Universal Skills | 51 | 27 |
| Toolchain Skills | 18 | 60 |
| Correct Paths | 0% | 100% |
| Duplicates | 7 | 0 |
| Reference Tracking | 0 | 14 skills |

### Fixed Issues

#### 1. Path Corrections
**Before (Wrong)**:
```json
"source_path": "main/internal-comms/SKILL.md"
```

**After (Correct)**:
```json
"source_path": "universal/main/internal-comms/SKILL.md"
```

#### 2. Duplicate Elimination
**Before**: `mcp-builder` appeared 7 times (1 SKILL.md + 6 reference files)

**After**: `mcp-builder` appears 1 time with reference files tracked separately

#### 3. Reference File Tracking
**Before**: No reference tracking

**After**:
```json
{
  "has_references": true,
  "reference_files": [
    "design_principles.md",
    "workflow.md",
    "mcp_best_practices.md"
  ]
}
```

## Error Handling

The script handles errors gracefully:

### Missing tiktoken
```
Warning: tiktoken not available. Token counts will be estimated.
```
Falls back to character-based estimation.

### Missing git history
Falls back to file modification time.

### Invalid metadata.json
Logs warning and uses defaults.

### Missing frontmatter
Uses directory name as skill name.

## Dependencies

### Required
- Python 3.8+
- Standard library only (json, re, subprocess, pathlib, etc.)

### Optional
- `tiktoken` - For accurate token counting
  ```bash
  pip install tiktoken
  ```
  Without tiktoken, token counts are estimated using character count.

## Troubleshooting

### Script shows "tiktoken not available"
This is just a warning. Token counts will be estimated. To install tiktoken:
```bash
pip install tiktoken
```

### Validation shows "Path doesn't exist"
The skill file was moved or deleted. Update the skill structure or remove the entry.

### High token count warnings
Some WordPress skills legitimately have high token counts (>10K). This is normal for comprehensive skills with extensive examples.

### Git command fails
The script falls back to file modification time. This is normal in non-git directories.

## Integration

### CI/CD Integration
Add to GitHub Actions workflow:
```yaml
- name: Validate Manifest
  run: python3 scripts/generate_manifest.py --validate
```

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 scripts/generate_manifest.py --validate
if [ $? -ne 0 ]; then
  echo "Manifest validation failed!"
  exit 1
fi
```

### Automated Updates
Regenerate manifest on skill changes:
```bash
# After adding/modifying skills
python3 scripts/generate_manifest.py
git add manifest.json
git commit -m "Update manifest after skill changes"
```

## Related Documentation

- **Manifest Structure Analysis**: `docs/research/manifest-structure-analysis-2025-12-03.md`
- **Skill Deployment Structure**: `docs/research/skill-deployment-structure-analysis-2025-12-03.md`
- **Inter-Skill References**: `docs/research/inter-skill-references-analysis-2025-11-30.md`

## Success Criteria

- ✅ All 89 skills present in manifest
- ✅ Zero duplicate entries
- ✅ 100% correct hierarchical paths
- ✅ All paths verified to exist
- ✅ Correct category/toolchain/framework values
- ✅ Valid JSON schema
- ✅ Metadata complete and accurate
- ✅ Reference files tracked (where applicable)

## Future Enhancements

### Planned Features
- Schema validation against JSON Schema
- Auto-fix common metadata issues
- Integration with Claude Code for skill deployment
- Dependency graph visualization
- Token count optimization suggestions

### Possible Improvements
- Parallel processing for faster generation
- Caching for incremental updates
- More sophisticated framework detection
- Support for skill aliases/redirects
- Changelog generation from git history
