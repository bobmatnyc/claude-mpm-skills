# Scripts Directory

This directory contains utility scripts for managing the Claude MPM Skills repository.

## Available Scripts

| Script | Description |
|--------|-------------|
| **init_skill.py** | Initialize a new skill with proper structure |
| **package_skill.py** | Package and validate skills for deployment |
| **flatten_skills.sh** | Deploy all skills to flat directory structure |
| **generate_manifest.py** | Generate manifest.json from all skills |
| **check_voice_consistency.py** | Validate imperative voice in skills |
| **token_report.py** | Generate token usage reports |
| **create-labels.sh** | Create GitHub labels for the repository |

---

## init_skill.py

Initialize a new skill with proper directory structure, SKILL.md template, and metadata.json.

### Usage

```bash
# Interactive mode (recommended for first-time users)
python scripts/init_skill.py

# Create a toolchain skill
python scripts/init_skill.py --category toolchains --toolchain python --subcategory frameworks --framework fastapi

# Create a universal skill
python scripts/init_skill.py --category universal --subcategory testing --name tdd-patterns

# Quick mode with full path
python scripts/init_skill.py --path toolchains/rust/testing/integration

# With description
python scripts/init_skill.py --path toolchains/python/async/asyncio --description "Python asyncio patterns"

# Dry run (preview without creating files)
python scripts/init_skill.py --dry-run --path toolchains/go/testing/integration
```

### Options

| Option | Description |
|--------|-------------|
| `--path PATH` | Full skill path (e.g., toolchains/python/frameworks/django) |
| `--category {toolchains,universal,examples}` | Skill category |
| `--toolchain NAME` | Toolchain (e.g., python, javascript, rust) |
| `--subcategory NAME` | Subcategory (e.g., frameworks, testing, tooling) |
| `--framework NAME` | Framework or skill name |
| `--name NAME` | Skill name (for universal/examples) |
| `--description TEXT` | Skill description |
| `--tags LIST` | Comma-separated tags |
| `--force` | Overwrite existing skill |
| `--dry-run` | Preview without creating files |
| `--interactive, -i` | Run in interactive mode |

### What Gets Created

```
{skill_path}/
├── SKILL.md           # Main skill content with frontmatter template
└── metadata.json      # Skill metadata with proper structure
```

### Example Output

```
✅ Skill created successfully!

📁 Location: toolchains/python/frameworks/fastapi/
   - SKILL.md
   - metadata.json

📝 Next steps:
   1. Edit toolchains/python/frameworks/fastapi/SKILL.md with actual content
   2. Update metadata.json with accurate token counts
   3. Add related_skills references
   4. Run: python scripts/generate_manifest.py --validate
   5. Deploy: ./scripts/flatten_skills.sh
```

---

## package_skill.py

Package and validate individual skills for deployment to the Claude skills directory.

### Usage

```bash
# Package a single skill
python scripts/package_skill.py toolchains/python/frameworks/django

# Validate only (no copy)
python scripts/package_skill.py --validate toolchains/python/frameworks/django

# Package to custom target
python scripts/package_skill.py --target ~/.claude/skills toolchains/python/frameworks/django

# Package all skills matching pattern
python scripts/package_skill.py --pattern "toolchains/python/*"

# Package all skills
python scripts/package_skill.py --all

# Force overwrite existing
python scripts/package_skill.py --force toolchains/python/frameworks/django

# Verbose output
python scripts/package_skill.py --verbose toolchains/rust/frameworks/tauri
```

### Options

| Option | Description |
|--------|-------------|
| `skill_path` | Path to skill directory (relative to repo root) |
| `--pattern PATTERN` | Pattern to match multiple skills |
| `--target DIR` | Target directory for packaged skills (default: .claude/skills) |
| `--validate, -V` | Validate only, do not package |
| `--force, -f` | Overwrite existing packaged skills |
| `--dry-run` | Preview without packaging |
| `--verbose, -v` | Enable verbose output |
| `--all, -a` | Package all skills |

### Validation Checks

The script performs these validations:

1. **SKILL.md exists** with proper frontmatter
2. **metadata.json exists** with required fields (name, version, category)
3. **Token counts** are calculated and compared to declared values
4. **Progressive disclosure** section is present
5. **References** are detected and counted

### Example Output

```
🔧 Processing 1 skill(s)...
   Target: .claude/skills

📦 toolchains/python/frameworks/django
  SKILL.md: 4523 tokens
  metadata.json: {...}
  references/models.md: 1200 tokens
  Total tokens: 5723
   ✅ Packaged: toolchains-python-frameworks-django

==================================================
Summary: 1 successful, 0 failed

✅ Skills packaged to: .claude/skills

Next steps:
  - Verify deployment with: ls -la .claude/skills/
  - Run manifest generator: python scripts/generate_manifest.py
```

---

## flatten_skills.sh

Production-quality deployment script that transforms the hierarchical skill structure into a flat directory format suitable for Claude's skill system.

### Overview

The script auto-discovers all skills from `toolchains/`, `universal/`, and `examples/` directories, transforms their hierarchical paths to flat names (e.g., `toolchains/python/frameworks/django` → `toolchains-python-frameworks-django`), and copies all required files to the target deployment directory.

### Usage

```bash
# Deploy to default location (.claude/skills)
./scripts/flatten_skills.sh

# Deploy to custom location
./scripts/flatten_skills.sh --target ~/.claude/skills

# Preview deployment without making changes
./scripts/flatten_skills.sh --dry-run

# Force overwrite existing deployment
./scripts/flatten_skills.sh --force

# Verbose output with detailed logging
./scripts/flatten_skills.sh --verbose

# Show help
./scripts/flatten_skills.sh --help
```

### Options

| Option | Description |
|--------|-------------|
| `--target DIR` | Target directory for deployment (default: `.claude/skills`) |
| `--dry-run` | Show what would be deployed without making changes |
| `--force` | Overwrite existing files in target directory |
| `--verbose` | Show detailed output during deployment |
| `--help` | Show usage information |

### What Gets Deployed

For each skill, the script copies:

1. **SKILL.md** (required) - The main skill file
2. **metadata.json** (optional) - Skill metadata; warning if missing
3. **references/** (optional) - Reference materials if present

Files excluded:
- `.etag_cache.json`
- `.DS_Store`
- Hidden files (`.*)`
- `README.md`

### Output Format

```
🔄 Flattening skills for deployment...
Source: /Users/masa/Projects/claude-mpm-skills
Target: /Users/masa/Projects/claude-mpm-skills/.claude/skills

[1/N] toolchains-python-frameworks-django ✓
[2/N] toolchains-javascript-frameworks-react ✓
...
[N/N] examples-good-self-contained-skill ✓

✅ Deployment Summary:
   - Skills deployed: N
   - Files copied: 264
   - References preserved: 21
   - Target: .claude/skills/
```

### Features

- **Auto-discovery**: Automatically finds all skills with SKILL.md files
- **Path transformation**: Converts hierarchical paths to flat names
- **Color-coded output**: Green (success), yellow (warning), red (error)
- **Progress tracking**: Shows X/N progress indicator for each skill
- **Validation**: Checks source directories, target permissions, existing deployments
- **References preservation**: Automatically copies references/ directories
- **Deployment manifest**: Generates `.deployment_manifest` with deployment metadata
- **Error handling**: Graceful error handling with detailed messages
- **Dry-run mode**: Preview changes before applying

### Exit Codes

- `0` - Success
- `1` - Error occurred during deployment

### Examples

#### Standard Deployment

```bash
# First-time deployment
./scripts/flatten_skills.sh

# Output:
# ✅ Deployment Summary:
#    - Skills deployed: N
#    - Files copied: 264
#    - References preserved: 21
```

#### Preview Changes

```bash
# See what would be deployed
./scripts/flatten_skills.sh --dry-run --verbose

# Shows detailed output for each skill without making changes
```

#### Update Existing Deployment

```bash
# Update all skills (overwrites existing)
./scripts/flatten_skills.sh --force

# Use verbose mode to see what changed
./scripts/flatten_skills.sh --force --verbose
```

#### Deploy to User Directory

```bash
# Deploy to user's Claude config
./scripts/flatten_skills.sh --target ~/.claude/skills --force
```

### Error Handling

The script handles various error conditions:

1. **Missing SKILL.md**: Error and skip skill
2. **Missing metadata.json**: Warning but continues
3. **Target exists without --force**: Error with helpful message
4. **Insufficient permissions**: Error before attempting deployment
5. **Source directories missing**: Error during validation

### Deployment Manifest

Each deployment generates a `.deployment_manifest` file in the target directory with:

```
# Skill Deployment Manifest
# Generated: 2025-12-03 14:58:17 UTC
# Source: /Users/masa/Projects/claude-mpm-skills
# Target: /Users/masa/Projects/claude-mpm-skills/.claude/skills
# Skills Deployed: N
# Files Copied: 264
# References Preserved: 21
# Script Version: 1.0.0
```

### Technical Details

- **Shell**: Bash (requires bash 4.0+)
- **Dependencies**: Standard Unix utilities (find, cp, mkdir, etc.)
- **Compatibility**: macOS, Linux
- **Safety**: Uses `set -euo pipefail` for robust error handling
- **Performance**: Processes all skills quickly (depends on total count)

### Troubleshooting

#### "Target directory already exists"

```bash
# Use --force to overwrite
./scripts/flatten_skills.sh --force
```

#### "Target parent directory is not writable"

```bash
# Check permissions on parent directory
ls -ld $(dirname ~/.claude/skills)

# Create parent directory if needed
mkdir -p ~/.claude
```

#### "No skills found to deploy"

```bash
# Verify you're running from project root
pwd
# Should show: /Users/.../claude-mpm-skills

# Check source directories exist
ls -ld toolchains/ universal/ examples/
```

### Development

When modifying the script:

1. Test with `--dry-run` first
2. Verify color output works in your terminal
3. Test error conditions (missing files, permissions, etc.)
4. Ensure proper cleanup on errors
5. Update version in deployment manifest if making breaking changes

### Integration

This script is designed to be used:

- **Locally**: Deploy skills to `.claude/skills` for development
- **CI/CD**: Automated deployment to user directories
- **Documentation**: Generate deployment manifests for tracking
- **Testing**: Validate skill structure and completeness

For questions or issues, see the main project README or open an issue.
