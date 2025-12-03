# Skill Deployment Structure Analysis

**Research Date**: 2025-12-03
**Researcher**: Research Agent
**Scope**: Repository structure, deployment mechanisms, and flattening requirements
**Purpose**: Document current structure and provide requirements for deployment script

---

## Executive Summary

### Key Findings

1. **Source Structure**: Hierarchical organization in `toolchains/` and `universal/` (89 skills total)
2. **Deployment Target**: Flat structure in `.claude/skills/` with hyphenated naming
3. **Naming Convention**: Source path `toolchains/python/frameworks/django` → Deployed as `toolchains-python-frameworks-django`
4. **File Preservation**: Must copy SKILL.md, metadata.json, and optional references/ directory
5. **Existing Mechanism**: Bundle deployment scripts exist but not a general flattening tool
6. **Metadata Handling**: .etag_cache.json files are deployment artifacts, not source files
7. **Current Deployment**: 77 skills deployed (88% coverage)

### Repository Health

- **Total Skills (Source)**: 89 (87 in toolchains/universal + 2 in examples)
- **Deployed Skills**: 77 in `.claude/skills/`
- **Skills with References**: 21 have `references/` subdirectories
- **Metadata Files**: 87 metadata.json files

---

## Current Repository Structure

### Source Organization (Hierarchical)

```
claude-mpm-skills/
├── toolchains/                      # Language/framework-specific skills (60)
│   ├── ai/                         # 7 skills (frameworks, protocols, sdks, services, techniques)
│   ├── javascript/                 # 10 skills (frameworks, testing, build, tooling)
│   ├── nextjs/                     # 2 skills (core, v16)
│   ├── php/                        # 6 skills (WordPress ecosystem, EspoCRM)
│   ├── platforms/                  # 4 skills (deployment, database, backend)
│   ├── python/                     # 10 skills (frameworks, testing, data, async, tooling, validation)
│   ├── rust/                       # 2 skills (desktop-applications, frameworks)
│   ├── typescript/                 # 12 skills (frameworks, testing, data, validation, state, api, build)
│   ├── ui/                         # 4 skills (styling, components)
│   └── universal/                  # 2 skills (infrastructure, data)
├── universal/                       # Universal skills (27)
│   ├── architecture/               # 1 skill (software-patterns)
│   ├── collaboration/              # 7 skills (git-workflow, brainstorming, etc.)
│   ├── data/                       # 3 skills (database-migration, xlsx, json-data-handling)
│   ├── debugging/                  # 3 skills (systematic, root-cause-tracing, verification)
│   ├── infrastructure/             # 1 skill (env-manager)
│   ├── main/                       # 2 skills (skill-creator, artifacts-builder)
│   ├── security/                   # 1 skill (security-scanning)
│   ├── testing/                    # 5 skills (TDD, webapp-testing, test-quality-inspector, etc.)
│   └── web/                        # 2 skills (api-documentation, web-performance-optimization)
└── examples/                        # 2 example skills (good/bad patterns)

Total: 89 skills
```

### Deployment Structure (Flat)

```
.claude/skills/
├── toolchains-ai-frameworks-dspy/
├── toolchains-ai-frameworks-langchain/
├── toolchains-python-frameworks-django/
├── toolchains-python-frameworks-flask/
├── toolchains-typescript-testing-vitest/
├── universal-debugging-systematic-debugging/
├── universal-testing-test-driven-development/
└── ... (77 total deployed)
```

---

## Naming Convention Transformation

### Pattern Rule

**Source Path → Deployed Name**
- Replace `/` (directory separators) with `-` (hyphens)
- Preserve full hierarchical path as flat name
- Keep original skill directory name at end

### Examples

| Source Path | Deployed Name |
|------------|---------------|
| `toolchains/python/frameworks/django` | `toolchains-python-frameworks-django` |
| `toolchains/typescript/testing/vitest` | `toolchains-typescript-testing-vitest` |
| `universal/debugging/systematic-debugging` | `universal-debugging-systematic-debugging` |
| `toolchains/ai/frameworks/langchain` | `toolchains-ai-frameworks-langchain` |
| `universal/main/skill-creator` | `universal-main-skill-creator` |

### Algorithm

```python
def transform_path_to_name(source_path: str) -> str:
    """
    Transform hierarchical source path to flat deployment name.

    Examples:
        toolchains/python/frameworks/django → toolchains-python-frameworks-django
        universal/testing/test-driven-development → universal-testing-test-driven-development
    """
    # Remove leading/trailing slashes
    path = source_path.strip('/')

    # Replace directory separators with hyphens
    deployed_name = path.replace('/', '-')

    return deployed_name
```

---

## File Structure Per Skill

### Minimal Skill Structure

```
skill-name/
├── SKILL.md              # REQUIRED: Main skill content
└── metadata.json         # REQUIRED: Skill metadata
```

### Extended Skill Structure (with References)

```
skill-name/
├── SKILL.md              # REQUIRED: Main skill content
├── metadata.json         # REQUIRED: Skill metadata
└── references/           # OPTIONAL: Progressive disclosure content
    ├── examples.md
    ├── best-practices.md
    ├── advanced-patterns.md
    └── troubleshooting.md
```

### Deployment Artifacts (Created During Deployment)

```
.claude/skills/deployed-skill-name/
├── SKILL.md              # Copied from source
├── metadata.json         # Copied from source
├── references/           # Copied if exists in source
│   └── *.md
└── .etag_cache.json      # CREATED BY DEPLOYMENT: Cache file for updates
```

**Important**: `.etag_cache.json` files are **deployment artifacts**, not source files. Do not copy these.

---

## Metadata File Structure

### metadata.json Format

```json
{
  "name": "django",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "framework": "django",
  "tags": ["web-framework", "django", "orm", "rest-api", "admin"],
  "entry_point_tokens": 85,
  "full_tokens": 5000,
  "related_skills": [
    "../../testing/pytest",
    "../fastapi",
    "../../data/sqlalchemy"
  ],
  "author": "Claude MPM",
  "license": "MIT"
}
```

### Key Fields

- **name**: Skill identifier (used for display)
- **version**: Semantic version (e.g., "1.0.0")
- **category**: "toolchain" or "universal"
- **toolchain**: Programming language (python, typescript, javascript, etc.)
- **framework**: Specific framework or null
- **tags**: Array of searchable tags
- **entry_point_tokens**: Token count for entry point
- **full_tokens**: Token count for full documentation
- **related_skills**: Relative paths to related skills (BREAKS IN FLAT DEPLOYMENT)
- **author**: Skill author/maintainer
- **license**: License type (usually "MIT")

### Metadata Preservation

**MUST PRESERVE**:
- All fields copied verbatim
- File structure and JSON formatting
- No modifications during deployment

**KNOWN ISSUE**: `related_skills` field contains relative paths that break in flat deployment (documented in inter-skill-references-analysis-2025-11-30.md)

---

## Existing Deployment Mechanisms

### 1. Bundle Deployment Scripts

**Location**: `.bundles/*/deploy.sh`

**Purpose**: Deploy curated skill bundles for specific stacks

**Features**:
- Flat and hierarchical deployment modes
- Validation before deployment
- Manifest generation
- Idempotent operation

**Example**:
```bash
cd .bundles/python-web-stack
./deploy.sh --flat ~/.claude/skills/
```

**Limitations**:
- Requires manual bundle curation (skills.list file)
- Not suitable for deploying entire repository
- No reverse operation (unflattening)

### 2. Template Deploy Script

**Location**: `.bundles/deploy-template.sh`

**Purpose**: Template for creating new bundle deployment scripts

**Features**:
- Skill list parsing
- Missing skill validation
- Directory creation
- Manifest generation

**Key Code**:
```bash
if [[ "$MODE" == "--flat" ]]; then
    # Flat deployment: copy directly to target
    target_path="$TARGET_DIR/$skill_name"
else
    # Hierarchical deployment: preserve directory structure
    target_path="$TARGET_DIR/$skill_path"
fi
```

### 3. Current Gap

**Missing**: General-purpose flattening script that:
- Discovers all skills automatically (no manual list)
- Deploys entire repository to flat structure
- Handles incremental updates
- Preserves all metadata and references
- Validates deployment completeness

---

## Skill Content Requirements

### SKILL.md File Structure

```markdown
---
name: skill-name
description: Brief description for discovery
---

# Skill Title

---
progressive_disclosure:
  entry_point:
    summary: "60-95 token summary"
    when_to_use:
      - "Use case 1"
      - "Use case 2"
    quick_start:
      - "Step 1"
      - "Step 2"
  token_estimate:
    entry: 60-95
    full: 3000-6000
---

## Overview
[Full documentation content...]
```

### Key Sections (MUST PRESERVE)

1. **YAML Frontmatter**: name and description fields
2. **Progressive Disclosure Block**: Entry point metadata
3. **Full Documentation**: Complete skill content
4. **Related Skills References**: May contain broken relative paths

### Character Encoding

- **Format**: UTF-8 encoding
- **Line Endings**: Unix-style (LF) preferred
- **Special Characters**: Must preserve markdown formatting

---

## Directory Structure Statistics

### Skills by Category

| Category | Count | Examples |
|----------|-------|----------|
| Python | 10 | django, fastapi, flask, pytest, pydantic, sqlalchemy |
| TypeScript | 12 | vitest, jest, drizzle, kysely, prisma, zod, zustand, tanstack-query, trpc, turborepo |
| JavaScript | 10 | react, vue, svelte, sveltekit, playwright, vite, biome |
| PHP | 6 | wordpress (3), espocrm (3) |
| Rust | 2 | tauri, desktop-applications |
| Next.js | 2 | core, v16 |
| UI | 4 | tailwind, shadcn, daisyui, headlessui |
| AI | 7 | anthropic-sdk, langchain, dspy, langgraph, openrouter, mcp, session-compression |
| Platforms | 4 | vercel, netlify, neon, supabase |
| Universal Infrastructure | 3 | docker, github-actions, graphql, env-manager |
| Universal Testing | 5 | tdd, systematic-debugging, verification-before-completion, test-quality-inspector, webapp-testing |
| Universal Collaboration | 7 | git-workflow, brainstorming, stacked-prs, dispatching-parallel-agents |
| Universal Data | 3 | database-migration, xlsx, json-data-handling |
| Universal Other | 6 | software-patterns, security-scanning, api-documentation, web-performance-optimization, skill-creator, artifacts-builder |

### Skills with References/ Subdirectories (21 total)

| Skill | Reference Files Count |
|-------|----------------------|
| universal/main/skill-creator | 5 files |
| universal/collaboration/dispatching-parallel-agents | 4 files |
| universal/collaboration/requesting-code-review | 2 files |
| universal/collaboration/writing-plans | 2 files |
| universal/debugging/systematic-debugging | 4 files |
| universal/debugging/root-cause-tracing | 4 files |
| universal/debugging/verification-before-completion | 4 files |
| universal/infrastructure/env-manager | 5 files |
| universal/testing/test-driven-development | 4 files |
| universal/testing/test-quality-inspector | 3 files |
| universal/testing/condition-based-waiting | 1 file |
| universal/architecture/software-patterns | 1 file |
| toolchains/javascript/frameworks/react-state-machine | 4 files |
| toolchains/typescript/core | 3 files |
| toolchains/typescript/data/drizzle | 3 files |
| toolchains/nextjs/core | 4 files |
| toolchains/nextjs/v16 | 3 files |
| toolchains/rust/desktop-applications | 6 files |
| toolchains/php/frameworks/espocrm | 6 files |
| toolchains/ai/frameworks/langchain | 3 files |
| toolchains/ai/frameworks/langgraph | 3 files |

---

## Edge Cases and Special Considerations

### 1. Skills with Hyphenated Names

**Already Hyphenated Sources**:
- `toolchains/python/frameworks/fastapi-local-dev`
- `toolchains/php/frameworks/wordpress-advanced-architecture`
- `toolchains/php/frameworks/wordpress-block-editor`
- `universal/testing/test-driven-development`
- `universal/debugging/systematic-debugging`
- `universal/testing/condition-based-waiting`

**Deployment Names**: Hyphens preserved
- `toolchains-python-frameworks-fastapi-local-dev`
- `universal-testing-test-driven-development`

**No Special Handling Required**: Treat hyphens as regular characters

### 2. Multi-Level Nesting

**Deepest Paths** (5 levels):
- `toolchains/typescript/testing/vitest` (4 levels)
- `toolchains/python/frameworks/django` (4 levels)
- `universal/debugging/verification-before-completion` (3 levels)

**Deployment**: All flatten to same level regardless of depth

### 3. Example Skills

**Location**: `examples/good-self-contained-skill`, `examples/bad-interdependent-skill`

**Purpose**: Teaching examples for skill creation

**Deployment Status**: Currently deployed in `.claude/skills/`

**Recommendation**: Deploy but mark as examples in manifest

### 4. Cross-Skill References

**Problem**: 27 skills (31%) contain relative path references to other skills

**Example** (from metadata.json):
```json
"related_skills": [
  "../../testing/pytest",
  "../fastapi",
  "../../data/sqlalchemy"
]
```

**Impact**: These paths break in flat deployment

**Solution Options**:
1. **Update Metadata**: Transform relative paths to flat names during deployment
2. **Document Issue**: Mark as known limitation
3. **Fix at Source**: Update all metadata.json files with flat references

**Recommendation**: Option 1 (transform during deployment) + Option 3 (fix source over time)

### 5. References Directory Consistency

**With References**: 21 skills (24%)
**Without References**: 68 skills (76%)

**Deployment Rule**:
- If `references/` exists: Copy entire directory
- If not exists: Skip (no error)

### 6. Hidden Files

**.gitignore Rules**:
- `.etag_cache.json` files should NOT be copied (deployment artifacts)
- `.DS_Store` files should be excluded (macOS artifacts)

**Validation**: Check for presence of unwanted hidden files

### 7. Symbolic Links

**Not Used**: No symbolic links detected in current structure

**Recommendation**: Script should handle symlinks gracefully (resolve or skip)

### 8. Empty Directories

**Intermediate Directories**: Some category directories may be empty
- Example: `toolchains/python/` contains only subdirectories

**Deployment Rule**: Only deploy directories containing SKILL.md files

---

## Deployment Validation Requirements

### Pre-Deployment Checks

1. **Source Validation**:
   - All skills have SKILL.md file
   - All skills have metadata.json file
   - References/ directory is valid (if present)
   - No broken symlinks

2. **Target Validation**:
   - Target directory exists or can be created
   - Write permissions available
   - Sufficient disk space

3. **Naming Validation**:
   - No naming conflicts in flattened structure
   - All skill names are valid directory names
   - No reserved names or special characters

### Post-Deployment Checks

1. **Completeness**:
   - All source skills deployed
   - File counts match expectations
   - No missing SKILL.md or metadata.json files

2. **Integrity**:
   - File sizes match source
   - No corrupted files
   - Proper permissions set

3. **Manifest Generation**:
   - Deployment manifest created
   - All deployed skills listed
   - Timestamps recorded

---

## Recommended Flattening Script Requirements

### Core Functionality

1. **Auto-Discovery**:
   - Scan toolchains/, universal/, examples/ directories
   - Find all directories containing SKILL.md
   - Build complete skill list automatically

2. **Path Transformation**:
   - Apply naming convention (/ → -)
   - Validate transformed names are unique
   - Handle edge cases (hyphens in source names)

3. **File Operations**:
   - Copy SKILL.md (required)
   - Copy metadata.json (required)
   - Copy references/ directory (if exists)
   - Exclude .etag_cache.json and hidden files
   - Preserve file permissions and timestamps

4. **Metadata Transformation** (Optional Enhancement):
   - Parse metadata.json
   - Transform related_skills relative paths to flat names
   - Write updated metadata to deployed location

5. **Validation**:
   - Pre-flight checks
   - Post-deployment verification
   - Error reporting

6. **Manifest Generation**:
   - JSON manifest of deployed skills
   - Timestamps and version info
   - Deployment mode and target path

### Command-Line Interface

```bash
# Basic usage
./flatten-skills.sh

# Specify target directory
./flatten-skills.sh --target ~/.claude/skills

# Dry-run mode (validate only)
./flatten-skills.sh --dry-run

# Force overwrite existing skills
./flatten-skills.sh --force

# Transform metadata references
./flatten-skills.sh --fix-references

# Verbose output
./flatten-skills.sh --verbose

# Help
./flatten-skills.sh --help
```

### Output Example

```
[INFO] Skill Flattening Script v1.0.0
[INFO] Source: /Users/masa/Projects/claude-mpm-skills
[INFO] Target: /Users/masa/.claude/skills
[INFO] Mode: Standard deployment

[INFO] Discovering skills...
[SUCCESS] Found 89 skills

[INFO] Validating names...
[SUCCESS] No naming conflicts detected

[INFO] Deploying skills...
[SUCCESS] toolchains-python-frameworks-django
[SUCCESS] toolchains-typescript-testing-vitest
[SUCCESS] universal-testing-test-driven-development
... (89 total)

[INFO] Generating manifest...
[SUCCESS] Manifest: /Users/masa/.claude/skills/.deployment-manifest.json

[INFO] Deployment Summary
[SUCCESS] Deployed: 89 skills
[SUCCESS] Skipped: 0 skills (already exist)
[SUCCESS] Failed: 0 skills

[SUCCESS] Deployment complete!
```

---

## Manifest File Format

### .deployment-manifest.json

```json
{
  "deployment_version": "1.0.0",
  "deployed_at": "2025-12-03T10:30:00Z",
  "source_repository": "/Users/masa/Projects/claude-mpm-skills",
  "target_directory": "/Users/masa/.claude/skills",
  "deployment_mode": "flat",
  "skills_total": 89,
  "skills_deployed": 89,
  "skills_skipped": 0,
  "skills_failed": 0,
  "skills": [
    {
      "name": "toolchains-python-frameworks-django",
      "source_path": "toolchains/python/frameworks/django",
      "deployed_path": "/Users/masa/.claude/skills/toolchains-python-frameworks-django",
      "has_references": false,
      "files_copied": ["SKILL.md", "metadata.json"],
      "size_bytes": 45123,
      "deployed_at": "2025-12-03T10:30:01Z"
    },
    {
      "name": "universal-main-skill-creator",
      "source_path": "universal/main/skill-creator",
      "deployed_path": "/Users/masa/.claude/skills/universal-main-skill-creator",
      "has_references": true,
      "references_count": 5,
      "files_copied": ["SKILL.md", "metadata.json", "references/"],
      "size_bytes": 89456,
      "deployed_at": "2025-12-03T10:30:02Z"
    }
  ],
  "validation": {
    "pre_deployment": {
      "source_skills_found": 89,
      "source_skills_valid": 89,
      "naming_conflicts": 0
    },
    "post_deployment": {
      "skills_verified": 89,
      "integrity_check": "passed",
      "missing_files": 0
    }
  }
}
```

---

## Implementation Recommendations

### Phase 1: Basic Flattening (MVP)

**Goal**: Deploy all skills to flat structure

**Features**:
- Auto-discovery of skills
- Path transformation
- File copying (SKILL.md, metadata.json, references/)
- Basic validation
- Manifest generation

**Estimated Complexity**: Low-Medium

### Phase 2: Enhanced Validation

**Goal**: Robust error handling and validation

**Features**:
- Pre-flight checks (permissions, conflicts)
- Post-deployment verification
- Detailed error reporting
- Dry-run mode
- Rollback capability

**Estimated Complexity**: Medium

### Phase 3: Metadata Transformation

**Goal**: Fix cross-skill references during deployment

**Features**:
- Parse metadata.json files
- Transform relative paths to flat names
- Update related_skills arrays
- Validate transformed paths exist

**Estimated Complexity**: Medium-High

### Phase 4: Incremental Updates

**Goal**: Support updating deployed skills without full redeployment

**Features**:
- Detect changed skills (hash comparison)
- Update only modified skills
- Preserve deployment manifest
- Track update history

**Estimated Complexity**: High

---

## Known Issues and Limitations

### Issue 1: Broken Cross-References

**Problem**: 27 skills contain relative path references that break in flat deployment

**Affected Skills**: Listed in docs/research/inter-skill-references-analysis-2025-11-30.md

**Impact**: Related skills links won't work in deployed environment

**Workaround**: Document as known limitation + fix during Phase 3

### Issue 2: Incomplete Deployment

**Problem**: Only 77/89 skills currently deployed (88% coverage)

**Missing Skills**: 12 skills not yet in .claude/skills/

**Impact**: Some skill references point to non-existent deployments

**Solution**: Full deployment via flattening script will resolve

### Issue 3: Manual Bundle Maintenance

**Problem**: Bundle deploy scripts require manual skills.list curation

**Impact**: Bundles can become outdated as skills evolve

**Solution**: Generate bundles automatically from skill tags/categories

---

## Testing Strategy

### Unit Tests

1. **Path Transformation**:
   - Verify correct hyphenation
   - Handle edge cases (trailing slashes, hyphens)
   - Detect naming conflicts

2. **File Operations**:
   - Copy single files correctly
   - Copy directories recursively
   - Preserve file attributes
   - Exclude hidden files

3. **Metadata Parsing**:
   - Parse valid JSON correctly
   - Handle malformed JSON gracefully
   - Transform paths accurately

### Integration Tests

1. **End-to-End Deployment**:
   - Deploy small subset of skills
   - Verify all files present
   - Check manifest accuracy
   - Validate deployed skill structure

2. **Incremental Updates**:
   - Deploy initial set
   - Update single skill
   - Verify only changed skill updated
   - Check manifest reflects updates

3. **Error Handling**:
   - Test with missing source files
   - Test with permission errors
   - Test with disk space issues
   - Verify rollback works

### Validation Tests

1. **Pre-Deployment**:
   - Detect naming conflicts
   - Verify source skill structure
   - Check target directory permissions

2. **Post-Deployment**:
   - Count deployed skills matches source
   - All SKILL.md files present
   - All metadata.json files present
   - References/ directories copied when present

---

## Success Criteria

### Deployment Script

- ✅ Discovers all 89 skills automatically
- ✅ Deploys to flat structure with correct naming
- ✅ Preserves all metadata and references
- ✅ Generates deployment manifest
- ✅ Validates deployment completeness
- ✅ Provides clear error messages
- ✅ Supports dry-run mode
- ✅ Idempotent (safe to run multiple times)

### Documentation

- ✅ Clear usage instructions
- ✅ Command-line options documented
- ✅ Error messages explained
- ✅ Examples provided
- ✅ Edge cases covered

### Quality

- ✅ No data loss during deployment
- ✅ Consistent results across runs
- ✅ Performance acceptable (<5 minutes for full deployment)
- ✅ Works on macOS, Linux, Windows (via WSL)

---

## Related Documentation

- **Inter-Skill References Analysis**: `docs/research/inter-skill-references-analysis-2025-11-30.md`
- **Skill Compliance Analysis**: `docs/research/skill-compliance-analysis-2025-12-01.md`
- **Bundle Deployment Guide**: `.bundles/README.md`
- **Deployment Examples**: `.bundles/DEPLOYMENT_EXAMPLES.md`
- **User Guide**: `docs/USER_GUIDE.md`

---

## Conclusion

The claude-mpm-skills repository uses a hierarchical source structure (`toolchains/`, `universal/`) that must be flattened for deployment to `.claude/skills/`. The naming convention is straightforward (replace `/` with `-`), but care must be taken to:

1. Preserve all skill content (SKILL.md, metadata.json, references/)
2. Exclude deployment artifacts (.etag_cache.json)
3. Handle cross-skill references gracefully
4. Validate deployment completeness
5. Generate deployment manifest for tracking

A well-designed flattening script will automate the deployment process, reduce errors, and enable consistent skill distribution across development environments. The recommended phased approach (MVP → validation → metadata transformation → incremental updates) allows iterative improvement while delivering value at each stage.

---

**Research Complete**: 2025-12-03
**Next Steps**: Implement Phase 1 (Basic Flattening MVP)
