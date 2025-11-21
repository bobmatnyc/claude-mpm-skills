# Contributing to Claude MPM Skills

Thank you for your interest in contributing to the Claude MPM Skills repository!

## Contribution Guidelines

### Skill Structure Requirements

Every skill must follow this structure:

```
skill-name/
├── SKILL.md          # Main skill content
└── metadata.json     # Skill metadata
```

### SKILL.md Format

Skills must use progressive disclosure with two tiers:

**Tier 1: Entry Point (30-50 tokens)**
```markdown
# Skill Name

Brief description (1-2 sentences) of what this skill does.

**When to Use**: Specific trigger conditions.
```

**Tier 2: Full Documentation**
```markdown
## Overview
Comprehensive explanation...

## Usage
Step-by-step instructions...

## Examples
Practical examples...

## Best Practices
Guidelines and tips...
```

### metadata.json Format

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "category": "framework|testing|debugging|collaboration",
  "toolchain": "python|javascript|rust|php|universal",
  "description": "Brief description",
  "tags": ["tag1", "tag2"],
  "dependencies": [],
  "author": "GitHub Username",
  "updated": "2025-11-21"
}
```

### Submission Process

1. **Fork** this repository
2. **Create feature branch**: `git checkout -b add-skill-name`
3. **Create skill directory** in appropriate category
4. **Add SKILL.md** following progressive disclosure format
5. **Add metadata.json** with complete information
6. **Test skill** in real Claude Code session
7. **Update manifest.json** (add your skill entry)
8. **Commit**: `git commit -m "feat: add skill-name for toolchain"`
9. **Push**: `git push origin add-skill-name`
10. **Create Pull Request** using PR template

### Review Process

All PRs require:
- ✅ Approval from @bobmatnyc (or designated maintainer)
- ✅ Passing CI validation (format, manifest, sensitive data check)
- ✅ Progressive disclosure format verified
- ✅ Real-world testing confirmation

### Skill Quality Standards

**Entry Point (Tier 1)**
- 30-50 tokens maximum
- Clear skill name and purpose
- Specific trigger conditions
- No implementation details

**Full Documentation (Tier 2)**
- Comprehensive usage instructions
- Practical examples
- Best practices
- Common pitfalls to avoid

**Metadata**
- Accurate category and toolchain
- Meaningful tags for discoverability
- Up-to-date version and timestamp

### Testing Requirements

Before submitting, verify:
- [ ] Skill loads correctly in Claude Code
- [ ] Entry point is concise (30-50 tokens)
- [ ] Full documentation is comprehensive
- [ ] Examples are practical and tested
- [ ] No sensitive data (API keys, tokens, passwords)
- [ ] metadata.json validates against schema
- [ ] Skill category is appropriate

### Code of Conduct

We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).

Be respectful, inclusive, and constructive.

### Questions?

- Open an issue for clarification
- Contact @bobmatnyc for governance questions
- Review existing skills for examples

## Skill Categories

**Toolchain Skills** (toolchains/)
- Language/framework-specific skills
- Require toolchain detection for deployment
- Examples: FastAPI, Next.js, Tauri

**Universal Skills** (universal/)
- Available to all projects
- Not toolchain-specific
- Examples: TDD, Debugging, Brainstorming

## Manifest Updates

When adding a skill, update manifest.json:

```json
{
  "skills": {
    "toolchains": {
      "python": [
        {
          "name": "your-skill-name",
          "path": "toolchains/python/frameworks/your-skill-name",
          "version": "1.0.0"
        }
      ]
    }
  }
}
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
