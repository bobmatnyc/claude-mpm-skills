# Scripts Directory

This directory contains utility scripts for managing the Claude MPM Skills repository.

## Available Scripts

- **flatten_skills.sh** - Deploy skills to flat directory structure
- **check_voice_consistency.py** - Validate imperative voice in skills
- **create-labels.sh** - Create GitHub labels for the repository

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
