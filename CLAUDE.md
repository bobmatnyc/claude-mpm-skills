# Claude Code Instructions for claude-mpm-skills Project

## ⚠️ CRITICAL: This is a SKILLS REPOSITORY

**This project develops skills for the Claude MPM Skills Repository, NOT for local use.**

Skills are:
1. **Developed** in `toolchains/` or `universal/` directories
2. **Built** using `scripts/generate_manifest.py`
3. **Deployed** via `scripts/flatten_skills.sh` to `.claude/skills/` (gitignored)

**DO NOT create skills directly in `.claude/skills/`** - that's the deployment target, not the source!

---

## Skill Creation Workflow

### Step 1: Initialize New Skill

Use the init script (recommended):

```bash
# Interactive mode
python scripts/init_skill.py

# Toolchain skill (e.g., PHP framework)
python scripts/init_skill.py --path toolchains/php/frameworks/espocrm

# Universal skill
python scripts/init_skill.py --path universal/testing/integration-patterns

# With description
python scripts/init_skill.py --path toolchains/python/async/celery --description "Celery task queue patterns"

# Dry run to preview
python scripts/init_skill.py --dry-run --path toolchains/go/testing/integration
```

### Step 2: Skill Directory Structure

Skills are organized hierarchically in the repository:

```
claude-mpm-skills/
├── toolchains/           # Language/framework-specific skills
│   ├── python/
│   │   ├── frameworks/
│   │   │   └── django/
│   │   │       ├── SKILL.md
│   │   │       ├── metadata.json
│   │   │       └── references/     # Optional deep-dive docs
│   │   └── testing/
│   │       └── pytest/
│   └── php/
│       └── frameworks/
│           └── espocrm/            # ← Example: EspoCRM skill location
│               ├── SKILL.md
│               ├── metadata.json
│               └── references/
├── universal/            # Cross-language skills
│   ├── testing/
│   │   └── tdd-patterns/
│   └── architecture/
│       └── api-design/
└── manifest.json         # Auto-generated - DO NOT edit manually
```

### Step 3: Required Files

Each skill directory must contain:

#### SKILL.md (Required)
```markdown
---
name: skill-name
description: Brief description with use cases
version: 1.0.0
category: development
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "One-line summary"
    when_to_use: "When to activate this skill"
    quick_start: "Steps to get started"
  references:
    - architecture.md
    - patterns.md
context_limit: 800
tags:
  - tag1
  - tag2
requires_tools: []
---

# Skill Title

## Overview

## When to Use This Skill

## Core Concepts

## Implementation Patterns

## Best Practices

## Anti-Patterns

## Navigation (if references exist)
- **[Architecture](references/architecture.md)**: ...
- **[Patterns](references/patterns.md)**: ...
```

#### metadata.json (Required)
```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "framework": "django",
  "tags": ["web", "orm", "api"],
  "entry_point_tokens": 85,
  "full_tokens": 5000,
  "author": "Claude MPM Skills",
  "license": "MIT",
  "requires": [],
  "updated": "2025-01-02",
  "source_path": "toolchains/python/frameworks-django/SKILL.md"
}
```

### Step 4: Validate and Build

```bash
# Validate skill structure
python scripts/package_skill.py --validate toolchains/php/frameworks/espocrm

# Generate/update manifest.json
python scripts/generate_manifest.py --output manifest.json

# Validate entire manifest
python scripts/generate_manifest.py --validate
```

### Step 5: Deploy for Testing

```bash
# Deploy all skills to .claude/skills/ (for local testing)
./scripts/flatten_skills.sh

# Deploy with force overwrite
./scripts/flatten_skills.sh --force

# Dry run to preview
./scripts/flatten_skills.sh --dry-run
```

---

## Existing EspoCRM Skill

There is already an EspoCRM skill at:
```
toolchains/php/frameworks/espocrm/
├── SKILL.md
├── metadata.json
└── references/
    ├── architecture.md
    ├── common-tasks.md
    ├── development-workflow.md
    ├── frontend-customization.md
    ├── hooks-and-services.md
    └── testing-debugging.md
```

To extend or improve it, edit files in this location, NOT in `.claude/skills/`.

---

## Common Mistakes to Avoid

❌ **DON'T**: Create skills in `.claude/skills/` directly
✅ **DO**: Create in `toolchains/` or `universal/`, then deploy

❌ **DON'T**: Edit `manifest.json` manually
✅ **DO**: Run `python scripts/generate_manifest.py`

❌ **DON'T**: Commit `.claude/skills/` to git (it's gitignored)
✅ **DO**: Commit source files in `toolchains/` and `universal/`

❌ **DON'T**: Forget to run manifest generation after changes
✅ **DO**: Run build scripts before committing

---

## Research Documentation

When conducting research for new skills:
- Document findings in: `docs/research/{topic}-{YYYY-MM-DD}.md`

---

## Quick Reference

| Task | Command |
|------|---------|
| Create new skill | `python scripts/init_skill.py --path toolchains/...` |
| Validate skill | `python scripts/package_skill.py --validate path/to/skill` |
| Generate manifest | `python scripts/generate_manifest.py --output manifest.json` |
| Deploy locally | `./scripts/flatten_skills.sh --force` |
| Check token counts | `python scripts/token_report.py` |
| Voice consistency | `python scripts/check_voice_consistency.py` |

---

## See Also

- `scripts/README.md` - Detailed script documentation
- `README.md` - Repository overview and skill catalog
- `docs/` - Additional documentation
