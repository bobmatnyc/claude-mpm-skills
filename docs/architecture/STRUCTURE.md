# Repository Structure

## Directory Tree

```
claude-mpm-skills/
├── .github/
│   ├── CODEOWNERS                   # Require @bobmatnyc review
│   ├── pull_request_template.md    # PR submission template
│   └── workflows/
│       └── validate-skills.yml      # CI validation workflow
├── toolchains/
│   ├── python/
│   │   └── frameworks/              # FastAPI, Flask, etc.
│   ├── javascript/
│   │   └── frameworks/              # Next.js, React, etc.
│   ├── rust/
│   │   └── frameworks/              # Tauri, etc.
│   └── php/
│       └── frameworks/              # EspoCRM, etc.
├── universal/
│   ├── testing/                     # TDD, etc.
│   ├── debugging/                   # Systematic debugging, etc.
│   └── collaboration/               # Brainstorming, etc.
├── manifest.json                    # Skill catalog with metadata
├── README.md                        # Repository overview
├── CONTRIBUTING.md                  # Contribution guidelines
├── GOVERNANCE.md                    # Branch protection policies
└── LICENSE                          # MIT License
```

## File Statistics

- **Total Files**: 8
- **Total Directories**: 16

## Governance Files

### CODEOWNERS
- All changes require @bobmatnyc approval
- Toolchain-specific owners can be added
- Critical files always require owner review

### validate-skills.yml
- Validates SKILL.md and metadata.json existence
- Checks manifest.json syntax
- Scans for sensitive data patterns
- Runs on PR and main branch pushes

### GOVERNANCE.md
- Branch protection requirements
- Merge authority definition
- Contribution process
- Skill review criteria

## Progressive Loading Design

Skills use two-tier structure:

**Tier 1 (Entry Point)**
- 30-50 tokens
- Skill name + brief description
- When to use triggers

**Tier 2 (Full Documentation)**
- Complete usage guide
- Examples
- Best practices
- Common pitfalls

## Categories

### Toolchain Skills
- Python (FastAPI, Flask)
- JavaScript (Next.js, React)
- Rust (Tauri)
- PHP (EspoCRM)

### Universal Skills
- Testing (TDD)
- Debugging (Systematic)
- Collaboration (Brainstorming)
