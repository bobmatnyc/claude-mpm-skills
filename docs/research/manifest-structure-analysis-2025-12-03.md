# Manifest.json Structure Analysis and Fix Requirements

**Research Date**: 2025-12-03
**Researcher**: Research Agent
**Scope**: manifest.json structure, schema, and path correction requirements
**Purpose**: Document current issues and provide implementation roadmap for fixing manifest.json

---

## Executive Summary

### Critical Issues Identified

1. **PATH MISMATCH**: manifest.json uses flat/incomplete paths instead of hierarchical paths
   - **Current**: `"source_path": "main/internal-comms/SKILL.md"`
   - **Correct**: `"source_path": "universal/main/internal-comms/SKILL.md"`
   - **Impact**: 100% of entries have incorrect paths (not usable for file operations)

2. **DUPLICATE ENTRIES**: Same skills appear multiple times with different paths
   - Example: "internal-comms" appears 5 times, "mcp-builder" appears 6 times
   - Impact: Manifest bloat and confusion

3. **INCONSISTENT STRUCTURE**: Path formats vary wildly
   - Some use full paths with SKILL.md: `"main/internal-comms/SKILL.md"`
   - Some use just filename: `"fastapi-local-dev.md"`
   - Some include subdirectories: `"main/mcp-builder/reference/design_principles.md"`

4. **WRONG FILE REFERENCES**: Some entries point to reference documents instead of SKILL.md
   - Example: `"source_path": "main/mcp-builder/reference/workflow.md"`
   - Should be: `"source_path": "universal/main/mcp-builder/SKILL.md"`

### Repository Statistics

- **Total Skills (Actual)**: 89 skills in source directories
- **Manifest Entries (Current)**: 69 reported (but contains duplicates and reference files)
- **Unique Skills in Manifest**: ~45-50 (estimated, many duplicates)
- **Path Accuracy**: 0% (all paths are incomplete/incorrect)

---

## Current Manifest Structure

### Top-Level Schema

```json
{
  "version": "1.0.0",
  "repository": "https://github.com/bobmatnyc/claude-mpm-skills",
  "updated": "2025-11-21",
  "description": "Curated collection of Claude Code skills for intelligent project development",
  "skills": {
    "universal": [ /* array of skill objects */ ],
    "toolchains": {
      "php": [ /* array */ ],
      "rust": [ /* array */ ],
      "python": [ /* array */ ],
      "javascript": [ /* array */ ]
    }
  },
  "metadata": { /* summary statistics */ },
  "provenance": { /* attribution info */ }
}
```

### Skill Object Schema (Current)

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "category": "universal" | "toolchain",
  "toolchain": "python" | "javascript" | "rust" | "php" | null,
  "framework": "django" | "react" | "tauri" | null,
  "tags": ["tag1", "tag2"],
  "entry_point_tokens": 91,
  "full_tokens": 563,
  "requires": [],
  "author": "bobmatnyc",
  "updated": "2025-11-21",
  "source_path": "main/internal-comms/SKILL.md"  // ❌ INCORRECT FORMAT
}
```

---

## Path Format Issues

### Issue 1: Missing Top-Level Category

**Problem**: Paths missing "universal/" or "toolchains/" prefix

**Examples**:
| Current (Wrong) | Correct Path |
|----------------|--------------|
| `main/internal-comms/SKILL.md` | `universal/main/internal-comms/SKILL.md` |
| `testing/test-driven-development/SKILL.md` | `universal/testing/test-driven-development/SKILL.md` |
| `debugging/systematic-debugging/SKILL.md` | `universal/debugging/systematic-debugging/SKILL.md` |
| `php/espocrm-development/SKILL.md` | `toolchains/php/frameworks/espocrm/SKILL.md` |
| `fastapi-local-dev.md` | `toolchains/python/frameworks/fastapi-local-dev/SKILL.md` |

**Impact**: File operations fail because paths don't exist

### Issue 2: Inconsistent File Naming

**Problem**: Some entries reference bare .md files instead of SKILL.md

**Examples**:
| Current (Wrong) | Correct Path |
|----------------|--------------|
| `fastapi-local-dev.md` | `toolchains/python/frameworks/fastapi-local-dev/SKILL.md` |
| `security-scanning.md` | `universal/security/security-scanning/SKILL.md` |
| `web-performance-optimization.md` | `universal/web/web-performance-optimization/SKILL.md` |
| `git-workflow.md` | `universal/collaboration/git-workflow/SKILL.md` |

**Impact**: Misleading - suggests root-level files when they're in skill directories

### Issue 3: Reference File Entries

**Problem**: Some entries point to reference documents, not main SKILL.md

**Examples (all wrong)**:
```json
{
  "name": "mcp-builder",
  "source_path": "main/mcp-builder/reference/design_principles.md"
},
{
  "name": "mcp-builder",
  "source_path": "main/mcp-builder/reference/workflow.md"
},
{
  "name": "internal-comms",
  "source_path": "main/internal-comms/examples/faq-answers.md"
}
```

**Correct Approach**: Each skill should have ONE entry pointing to SKILL.md only
```json
{
  "name": "mcp-builder",
  "source_path": "universal/main/mcp-builder/SKILL.md",
  "has_references": true,
  "reference_files": [
    "design_principles.md",
    "workflow.md",
    "mcp_best_practices.md",
    "python_mcp_server.md",
    "node_mcp_server.md",
    "evaluation.md"
  ]
}
```

### Issue 4: Duplicate Entries

**Problem**: Same skill appears multiple times

**Examples**:
- **internal-comms**: 5 entries (1 SKILL.md + 4 example files)
- **mcp-builder**: 6 entries (1 SKILL.md + 5 reference files)
- **env-manager**: 3 entries (1 SKILL.md + 2 reference files)
- **systematic-debugging**: 6 entries (1 SKILL.md + 5 test files)

**Impact**: Manifest bloat, confusion, incorrect skill counts

---

## Correct Schema Specification

### Required Fields

Every skill entry MUST have:

```typescript
interface SkillEntry {
  // Identity
  name: string;                    // Skill identifier (from directory name)
  version: string;                 // Semantic version (e.g., "1.0.0")

  // Classification
  category: "universal" | "toolchain";
  toolchain: string | null;        // python, javascript, typescript, rust, php, etc.
  framework: string | null;        // django, react, tauri, nextjs, etc.

  // Discovery
  tags: string[];                  // Searchable tags

  // Token Metrics
  entry_point_tokens: number;      // Entry point size (target: 60-95 tokens)
  full_tokens: number;             // Full skill size

  // Dependencies
  requires: string[];              // Array of required skill names (flat format)

  // Metadata
  author: string;                  // Author/maintainer
  updated: string;                 // ISO date (YYYY-MM-DD)

  // File Paths (CRITICAL - must be hierarchical)
  source_path: string;             // Path from repo root to SKILL.md
                                   // Format: "universal/category/skill-name/SKILL.md"
                                   //     or: "toolchains/language/.../skill-name/SKILL.md"

  // Optional: Reference tracking
  has_references?: boolean;        // True if references/ directory exists
  reference_files?: string[];      // Array of reference filenames (not full paths)
}
```

### Path Format Rules

**Universal Skills**:
```
Format: universal/{category}/{subcategory}/{skill-name}/SKILL.md

Examples:
- universal/main/internal-comms/SKILL.md
- universal/testing/test-driven-development/SKILL.md
- universal/debugging/systematic-debugging/SKILL.md
- universal/collaboration/git-workflow/SKILL.md
- universal/infrastructure/env-manager/SKILL.md
- universal/web/web-performance-optimization/SKILL.md
```

**Toolchain Skills**:
```
Format: toolchains/{language}/{category}/{framework}/{skill-name}/SKILL.md

Examples:
- toolchains/python/frameworks/django/SKILL.md
- toolchains/python/frameworks/fastapi-local-dev/SKILL.md
- toolchains/typescript/testing/vitest/SKILL.md
- toolchains/rust/frameworks/tauri/SKILL.md
- toolchains/php/frameworks/espocrm/SKILL.md
- toolchains/javascript/frameworks/nextjs/SKILL.md
```

### Path Validation Rules

1. **Must start with**: "universal/" OR "toolchains/"
2. **Must end with**: "/SKILL.md"
3. **Must exist**: File must be present at path
4. **Must be absolute from repo root**: No relative paths
5. **Must be unique**: Each skill has exactly ONE entry

---

## Required Field Values

### Category Field

- **universal**: Skills that work across all languages/frameworks
- **toolchain**: Language or framework-specific skills

**Mapping Rule**:
- If path starts with `universal/` → `category: "universal"`
- If path starts with `toolchains/` → `category: "toolchain"`

### Toolchain Field

**For Universal Skills**: `toolchain: null`

**For Toolchain Skills**: Extract from path
```
Path: toolchains/{language}/...
Value: {language}

Examples:
- toolchains/python/... → "python"
- toolchains/typescript/... → "typescript"
- toolchains/javascript/... → "javascript"
- toolchains/rust/... → "rust"
- toolchains/php/... → "php"
- toolchains/ui/... → "ui"
- toolchains/ai/... → "ai"
- toolchains/nextjs/... → "nextjs"
- toolchains/platforms/... → "platforms"
```

### Framework Field

**For Universal Skills**: `framework: null`

**For Toolchain Skills**:
- Extract from directory name OR metadata.json
- May be null if skill is language-level (not framework-specific)

**Examples**:
```
toolchains/python/frameworks/django → "django"
toolchains/python/frameworks/fastapi-local-dev → "fastapi"
toolchains/typescript/testing/vitest → "vitest"
toolchains/rust/frameworks/tauri → "tauri"
toolchains/javascript/frameworks/react → "react"
```

### Token Count Fields

**Source**: Calculate from actual SKILL.md file

**Methods**:
1. Count tokens using tiktoken (if available)
2. Estimate: ~4 characters per token (rough approximation)
3. Use existing metadata.json values if accurate

**Validation**:
- `entry_point_tokens`: Should be 50-100 (target: 60-95)
- `full_tokens`: Should be 500-15000 (typical range)

### Updated Field

**Format**: ISO date string "YYYY-MM-DD"

**Source Priority**:
1. Git last commit date for SKILL.md file
2. File modification timestamp
3. metadata.json updated field
4. Current date (if none available)

**Command to extract**:
```bash
git log -1 --format="%ad" --date=short -- path/to/SKILL.md
```

### Tags Field

**Source**: Extract from metadata.json or SKILL.md frontmatter

**Standard Tags** (for consistency):
- **Area**: frontend, backend, database, api, testing, debugging, performance, security, async
- **Skill Type**: framework, tool, pattern, workflow, architecture
- **Language**: language-specific tags (python, typescript, javascript, etc.)

---

## Transformation Requirements

### Task Breakdown

The manifest.json fix requires these transformations:

#### 1. Discover All Skills (Subtask 1)

**Goal**: Find every SKILL.md file in the repository

**Method**:
```bash
find toolchains/ universal/ examples/ -name "SKILL.md" -type f
```

**Output**: List of 89 skill paths

**Validation**: Cross-reference with directory count

#### 2. Extract Metadata (Subtask 2)

**Goal**: Read metadata.json and SKILL.md frontmatter for each skill

**For Each Skill**:
1. Parse metadata.json (if exists)
2. Parse SKILL.md YAML frontmatter
3. Extract git metadata (last commit date)
4. Calculate token counts

**Fields to Extract**:
- name (from directory name if not in metadata)
- version (from metadata.json or default "1.0.0")
- tags (from metadata.json or frontmatter)
- author (from metadata.json or default "Claude MPM")
- entry_point_tokens (calculate or use metadata)
- full_tokens (calculate or use metadata)

#### 3. Transform Paths (Subtask 3)

**Goal**: Convert discovered paths to correct hierarchical format

**Algorithm**:
```python
def transform_skill_path(discovered_path: str) -> str:
    """
    Transform discovered SKILL.md path to manifest format.

    Input: /Users/masa/Projects/claude-mpm-skills/universal/main/internal-comms/SKILL.md
    Output: universal/main/internal-comms/SKILL.md
    """
    # Get relative path from repo root
    relative_path = discovered_path.removeprefix(REPO_ROOT + "/")

    # Validate format
    assert relative_path.endswith("/SKILL.md")
    assert relative_path.startswith(("universal/", "toolchains/", "examples/"))

    return relative_path
```

**Examples**:
| Discovered Path | Manifest Path |
|----------------|---------------|
| `/Users/.../universal/main/internal-comms/SKILL.md` | `universal/main/internal-comms/SKILL.md` |
| `/Users/.../toolchains/python/frameworks/django/SKILL.md` | `toolchains/python/frameworks/django/SKILL.md` |
| `/Users/.../toolchains/typescript/testing/vitest/SKILL.md` | `toolchains/typescript/testing/vitest/SKILL.md` |

#### 4. Classify Skills (Subtask 4)

**Goal**: Determine category, toolchain, framework for each skill

**Classification Logic**:
```python
def classify_skill(path: str) -> dict:
    parts = path.split('/')

    if parts[0] == 'universal':
        return {
            'category': 'universal',
            'toolchain': None,
            'framework': None
        }
    elif parts[0] == 'toolchains':
        return {
            'category': 'toolchain',
            'toolchain': parts[1],  # e.g., 'python', 'typescript'
            'framework': extract_framework(path)
        }
    elif parts[0] == 'examples':
        return {
            'category': 'example',
            'toolchain': None,
            'framework': None
        }

def extract_framework(path: str) -> str | None:
    # If path contains /frameworks/, get next directory name
    # e.g., toolchains/python/frameworks/django → 'django'
    # Otherwise check skill directory name or metadata
    ...
```

#### 5. Generate New Manifest (Subtask 5)

**Goal**: Create correct manifest.json structure

**Structure**:
```json
{
  "version": "1.0.0",
  "repository": "https://github.com/bobmatnyc/claude-mpm-skills",
  "updated": "2025-12-03",
  "description": "Curated collection of Claude Code skills for intelligent project development",
  "skills": {
    "universal": [
      // All universal/* skills, ONE entry each
    ],
    "toolchains": {
      "python": [
        // All toolchains/python/* skills
      ],
      "typescript": [
        // All toolchains/typescript/* skills
      ],
      "javascript": [
        // All toolchains/javascript/* skills
      ],
      "rust": [
        // All toolchains/rust/* skills
      ],
      "php": [
        // All toolchains/php/* skills
      ],
      "ui": [
        // All toolchains/ui/* skills
      ],
      "ai": [
        // All toolchains/ai/* skills
      ],
      "nextjs": [
        // All toolchains/nextjs/* skills
      ],
      "platforms": [
        // All toolchains/platforms/* skills
      ]
    },
    "examples": [
      // All examples/* skills (if included)
    ]
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
      "javascript": 10,
      "rust": 2,
      "php": 6,
      "ui": 4,
      "ai": 7,
      "nextjs": 2,
      "platforms": 4,
      "universal": 3
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

---

## Implementation Roadmap

### Phase 1: Core Transformation (PRIORITY 1)

**Subtasks**:
1. ✅ **Skill Discovery**: Find all SKILL.md files
2. ✅ **Metadata Extraction**: Parse metadata.json and frontmatter
3. ✅ **Path Transformation**: Convert to hierarchical paths
4. ✅ **Skill Classification**: Determine category/toolchain/framework
5. ✅ **Manifest Generation**: Create new manifest.json

**Validation**:
- All 89 skills present
- Zero duplicates
- All paths valid and exist
- Correct category/toolchain/framework values

### Phase 2: Metadata Enhancement (PRIORITY 2)

**Tasks**:
- Calculate accurate token counts
- Extract git commit dates
- Validate and normalize tags
- Add reference file tracking

### Phase 3: Validation and Testing (PRIORITY 3)

**Tasks**:
- Schema validation (JSON Schema)
- Path existence checks
- Duplicate detection
- Token count validation
- Cross-reference integrity

---

## Validation Rules

### Required Validations

1. **Path Existence**:
   ```bash
   for path in $(jq -r '.skills.universal[].source_path' manifest.json); do
     [[ -f "$path" ]] || echo "Missing: $path"
   done
   ```

2. **No Duplicates**:
   ```bash
   jq -r '.skills.universal[].name' manifest.json | sort | uniq -d
   ```

3. **Correct Category**:
   - universal/* → category: "universal"
   - toolchains/* → category: "toolchain"

4. **Token Count Sanity**:
   - entry_point_tokens: 30-150
   - full_tokens: 100-20000

5. **Date Format**:
   - Pattern: YYYY-MM-DD
   - Valid date

### JSON Schema (for validation)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "repository", "updated", "skills", "metadata"],
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "repository": {
      "type": "string",
      "format": "uri"
    },
    "updated": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    },
    "skills": {
      "type": "object",
      "required": ["universal", "toolchains"],
      "properties": {
        "universal": {
          "type": "array",
          "items": { "$ref": "#/definitions/skill" }
        },
        "toolchains": {
          "type": "object",
          "additionalProperties": {
            "type": "array",
            "items": { "$ref": "#/definitions/skill" }
          }
        }
      }
    }
  },
  "definitions": {
    "skill": {
      "type": "object",
      "required": ["name", "version", "category", "source_path"],
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
        "category": { "enum": ["universal", "toolchain", "example"] },
        "toolchain": { "type": ["string", "null"] },
        "framework": { "type": ["string", "null"] },
        "tags": { "type": "array", "items": { "type": "string" } },
        "entry_point_tokens": { "type": "integer", "minimum": 1 },
        "full_tokens": { "type": "integer", "minimum": 1 },
        "requires": { "type": "array", "items": { "type": "string" } },
        "author": { "type": "string" },
        "updated": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
        "source_path": {
          "type": "string",
          "pattern": "^(universal|toolchains|examples)/.*/(SKILL\\.md|[^/]+\\.md)$"
        }
      }
    }
  }
}
```

---

## Example Transformations

### Before → After: Universal Skill

**Before (WRONG)**:
```json
{
  "name": "internal-comms",
  "version": "1.0.0",
  "category": "universal",
  "toolchain": null,
  "framework": null,
  "tags": ["frontend"],
  "entry_point_tokens": 91,
  "full_tokens": 563,
  "requires": [],
  "author": "bobmatnyc",
  "updated": "2025-11-21",
  "source_path": "main/internal-comms/SKILL.md"
}
```

**After (CORRECT)**:
```json
{
  "name": "internal-comms",
  "version": "1.0.0",
  "category": "universal",
  "toolchain": null,
  "framework": null,
  "tags": ["communication", "internal-tools", "content-generation"],
  "entry_point_tokens": 91,
  "full_tokens": 563,
  "requires": [],
  "author": "Claude MPM Team",
  "updated": "2025-12-02",
  "source_path": "universal/main/internal-comms/SKILL.md",
  "has_references": true,
  "reference_files": [
    "examples/faq-answers.md",
    "examples/company-newsletter.md",
    "examples/general-comms.md",
    "examples/3p-updates.md"
  ]
}
```

### Before → After: Toolchain Skill

**Before (WRONG)**:
```json
{
  "name": "fastapi-local-dev",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "framework": "fastapi",
  "tags": ["performance", "async", "api", "testing", "debugging"],
  "entry_point_tokens": 51,
  "full_tokens": 6352,
  "requires": [],
  "author": "bobmatnyc",
  "updated": "2025-11-21",
  "source_path": "fastapi-local-dev.md"
}
```

**After (CORRECT)**:
```json
{
  "name": "fastapi-local-dev",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "framework": "fastapi",
  "tags": ["performance", "async", "api", "testing", "debugging", "local-development"],
  "entry_point_tokens": 51,
  "full_tokens": 6352,
  "requires": ["python"],
  "author": "Claude MPM Team",
  "updated": "2025-11-30",
  "source_path": "toolchains/python/frameworks/fastapi-local-dev/SKILL.md",
  "has_references": false
}
```

---

## Script Requirements

### Input

- Repository root path
- Current manifest.json (optional, for comparison)

### Output

- New manifest.json with correct structure
- Validation report
- Transformation statistics

### Features

1. **Auto-Discovery**: Find all SKILL.md files automatically
2. **Metadata Extraction**: Parse metadata.json and frontmatter
3. **Path Transformation**: Convert to hierarchical format
4. **Duplicate Removal**: Ensure one entry per skill
5. **Validation**: Check all paths exist and are valid
6. **Statistics**: Report transformation details

### Command-Line Interface

```bash
# Generate new manifest
./scripts/generate_manifest.py

# Validate existing manifest
./scripts/generate_manifest.py --validate manifest.json

# Dry-run (show what would change)
./scripts/generate_manifest.py --dry-run

# Output to different file
./scripts/generate_manifest.py --output manifest-new.json

# Verbose mode
./scripts/generate_manifest.py --verbose
```

---

## Testing Strategy

### Unit Tests

1. Path transformation logic
2. Category classification
3. Toolchain/framework extraction
4. Duplicate detection
5. JSON schema validation

### Integration Tests

1. Full manifest generation
2. All skills discovered
3. No duplicates in output
4. All paths valid
5. Metadata accuracy

### Validation Tests

1. Compare old vs new manifest
2. Verify skill count matches
3. Check path existence
4. Validate JSON structure
5. Test with subset of skills

---

## Success Criteria

- ✅ All 89 skills present in manifest
- ✅ Zero duplicate entries
- ✅ 100% correct hierarchical paths
- ✅ All paths verified to exist
- ✅ Correct category/toolchain/framework values
- ✅ Valid JSON schema
- ✅ Metadata complete and accurate
- ✅ Reference files tracked (where applicable)

---

## Related Documentation

- **Skill Deployment Structure**: `docs/research/skill-deployment-structure-analysis-2025-12-03.md`
- **Inter-Skill References**: `docs/research/inter-skill-references-analysis-2025-11-30.md`
- **Skill Compliance**: `docs/research/skill-compliance-analysis-2025-12-01.md`

---

## Conclusion

The current manifest.json has critical structural issues:
1. **Flat/incomplete paths** instead of hierarchical paths
2. **Duplicate entries** for reference/example files
3. **Inconsistent formatting** (some .md, some SKILL.md, some reference files)

**Fix requires**:
1. Rediscovering all skills from source directories
2. Extracting correct metadata from metadata.json and frontmatter
3. Transforming paths to full hierarchical format
4. Removing duplicates (one entry per skill)
5. Adding reference file tracking
6. Validating output against schema

**Deliverables**:
- Python script to generate correct manifest.json
- JSON schema for validation
- Documentation of transformation process
- Test suite for validation

---

**Research Complete**: 2025-12-03
**Next Steps**: Implement manifest generation script (Python)
