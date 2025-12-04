# Claude Code Instructions for claude-mpm-skills Project

## Skill Creation Pattern

**IMPORTANT**: When creating new skills for this project, follow this exact structure:

### Directory Structure

```
.claude/skills/{category-toolchain-framework}/
  ├── SKILL.md           # Main skill content
  ├── metadata.json      # Skill metadata
  └── .etag_cache.json   # Optional cache file
```

### Example Structure Reference

See: `.claude/skills/toolchains-python-frameworks-django/` for a complete example.

### metadata.json Format

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "language-name",
  "framework": "framework-name",
  "tags": ["tag1", "tag2", "tag3"],
  "entry_point_tokens": 85,
  "full_tokens": 5000,
  "related_skills": [
    "../../category/skill-name",
    "../sibling-skill"
  ],
  "author": "Claude MPM",
  "license": "MIT"
}
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief description with use cases
---

# Skill Title

---
progressive_disclosure:
  entry_point:
    summary: "One-line summary"
    when_to_use:
      - "Use case 1"
      - "Use case 2"
    quick_start:
      - "Step 1"
      - "Step 2"
  token_estimate:
    entry: 75
    full: 4000-5000
---

## Core Concepts

## Implementation Patterns

## Best Practices

## Anti-Patterns

## Decision Trees

## Examples

## Resources
```

### Key Points

1. **Location**: Skills MUST be in `.claude/skills/`, NOT `src/claude_mpm/skills/`
2. **Naming**: Directory name uses format: `{category}-{toolchain}-{framework}`
3. **Files**: ALWAYS include both `SKILL.md` and `metadata.json`
4. **Git**: The `.claude/` directory is gitignored (intentional - skills managed separately)

### Common Mistakes to Avoid

❌ **DON'T**: Create skills as single files like `golang-testing-strategies.md`
✅ **DO**: Create directory with `SKILL.md` and `metadata.json`

❌ **DON'T**: Put skills in `src/claude_mpm/skills/`
✅ **DO**: Put skills in `.claude/skills/`

❌ **DON'T**: Forget the `metadata.json` file
✅ **DO**: Always create both `SKILL.md` and `metadata.json`

### Verification Checklist

Before considering a skill complete:

- [ ] Directory created in `.claude/skills/{category-toolchain-framework}/`
- [ ] `SKILL.md` file with full content
- [ ] `metadata.json` file with proper structure
- [ ] Frontmatter in SKILL.md with progressive_disclosure
- [ ] Token estimates in both metadata.json and SKILL.md
- [ ] Related skills references updated
- [ ] Code examples are runnable
- [ ] Decision trees included
- [ ] Anti-patterns documented
- [ ] Resources section with current links

## Research Documentation

When conducting research for skills, document findings in:
- `docs/research/{topic}-{YYYY-MM-DD}.md`

## Related Documentation

- Skill creation guide: `docs/skills/README.md` (if exists)
- Skill examples: `.claude/skills/examples-good-self-contained-skill/`
