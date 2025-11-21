# Claude MPM Skills

> Reusable Claude Code skills for intelligent project development

## Overview

This repository contains a curated collection of Claude Code skills designed for the Claude Multi-Agent Project Manager (MPM) ecosystem. Skills are automatically deployed based on project toolchain detection.

## Features

- **Progressive Loading**: Skills load on-demand with 30-50 token entry points
- **Toolchain Detection**: Automatically deploy relevant skills based on project type
- **Universal Skills**: Core skills available to all projects
- **Community Driven**: Open for contributions (with governance)

## Repository Structure

```
claude-mpm-skills/
├── toolchains/          # Language/framework-specific skills
│   ├── python/
│   │   └── frameworks/
│   │       ├── fastapi-local-dev/
│   │       └── flask-local-dev/
│   ├── javascript/
│   │   └── frameworks/
│   │       ├── nextjs/
│   │       └── react/
│   ├── rust/
│   │   └── frameworks/
│   │       └── tauri/
│   └── php/
│       └── frameworks/
│           └── espocrm/
└── universal/           # Skills for all projects
    ├── testing/
    │   └── test-driven-development/
    ├── debugging/
    │   └── systematic-debugging/
    └── collaboration/
        └── brainstorming/
```

## Usage

### Automatic Deployment (Recommended)

```bash
# During project initialization
claude-mpm init

# Or manually deploy skills
claude-mpm skills deploy
```

Skills are automatically deployed based on detected toolchain (package.json, pyproject.toml, Cargo.toml, etc.)

### Manual Deployment

```bash
# Download specific skill
curl -o ~/.claude/skills/fastapi-local-dev.skill \
  https://raw.githubusercontent.com/bobmatnyc/claude-mpm-skills/main/toolchains/python/frameworks/fastapi-local-dev/SKILL.md
```

## Available Skills

See [manifest.json](manifest.json) for complete skill catalog.

### Toolchain Skills

**Python**
- FastAPI Local Development
- Flask Local Development

**JavaScript/TypeScript**
- Next.js Application Development
- React Component Development

**Rust**
- Tauri Desktop Application Development

**PHP**
- EspoCRM Development

### Universal Skills

**Testing**
- Test-Driven Development (TDD)

**Debugging**
- Systematic Debugging

**Collaboration**
- Brainstorming and Ideation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

**Governance**: All merges to main require approval from @bobmatnyc (see [GOVERNANCE.md](GOVERNANCE.md))

## Progressive Loading Design

Skills use a two-tier structure:

1. **Entry Point** (30-50 tokens): Skill name, brief description, when to use
2. **Full Documentation**: Complete usage guide, examples, best practices

This design minimizes token usage while providing comprehensive guidance when needed.

## License

MIT License - See [LICENSE](LICENSE)

## Links

- **Claude MPM**: https://github.com/bobmatnyc/claude-mpm
- **Documentation**: https://github.com/bobmatnyc/claude-mpm/tree/main/docs
- **Issues**: https://github.com/bobmatnyc/claude-mpm-skills/issues
