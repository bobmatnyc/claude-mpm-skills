# Skills Library Versioning Policy

## Overview

This document defines the versioning strategy for the claude-mpm-skills library, based on analysis of Claude Code documentation and existing skill patterns.

## Version Format

All skills follow **Semantic Versioning 2.0.0** (MAJOR.MINOR.PATCH):

```
{MAJOR}.{MINOR}.{PATCH}
```

### Initial Version

All new skills start at version **1.0.0** to indicate:
- Production-ready content
- Complete core coverage
- Stable API/structure
- Ready for consumption

### Version Components

- **MAJOR**: Breaking changes to skill interface or structure
- **MINOR**: New features, backward-compatible additions
- **PATCH**: Bug fixes, documentation updates, clarifications

## When to Increment Versions

### MAJOR Version (X.0.0)

Increment when making **breaking changes** that affect how skills are consumed:

**Examples**:
- ✅ Restructuring progressive_disclosure format
- ✅ Changing metadata.json schema in incompatible ways
- ✅ Removing sections that consumers depend on
- ✅ Changing skill category or location in repository
- ✅ Removing or renaming key concepts

**NOT Major Changes**:
- ❌ Framework version updates (use skill name instead)
- ❌ Adding new sections (that's minor)
- ❌ Expanding existing content (that's minor)

### MINOR Version (x.Y.0)

Increment when adding **new features** in a backward-compatible manner:

**Examples**:
- ✅ Adding new sections (e.g., "Testing Patterns")
- ✅ Expanding coverage (e.g., adding new component examples)
- ✅ Adding new code examples
- ✅ Adding sub-skills or references
- ✅ Documenting newly released framework features
- ✅ Adding integration patterns with other skills

**Typical Triggers**:
- Framework releases new features (React 19 hooks, Next.js 15 caching)
- Community best practices evolve
- New integration patterns discovered
- Expanding "Advanced Patterns" section

### PATCH Version (x.y.Z)

Increment for **bug fixes and documentation improvements**:

**Examples**:
- ✅ Fixing code example errors
- ✅ Correcting typos or grammar
- ✅ Clarifying confusing explanations
- ✅ Updating outdated links
- ✅ Improving code formatting
- ✅ Fixing metadata.json errors (token counts, tags)

**Typical Triggers**:
- User reports incorrect code example
- Dead links discovered
- Token estimates need adjustment
- Tags missing or incorrect

## Framework Version Strategy

### Problem: How to Handle Framework Version Updates?

**Example**: React 18 vs React 19, Vue 3 vs Vue 4, Next.js 14 vs Next.js 15

### Solution: Framework Version in Skill Name

When framework versions have **significantly different APIs**, create **separate skills**:

```
toolchains/javascript/frameworks/react/      # React 18 (current stable)
toolchains/javascript/frameworks/react-19/   # React 19 (if breaking changes)
toolchains/nextjs/v14/                       # Next.js 14
toolchains/nextjs/v15/                       # Next.js 15
```

**Skill metadata.json**:
```json
{
  "name": "nextjs-v15",
  "version": "1.0.0",  // Skill version (not framework version)
  "framework": "nextjs",
  "tags": ["nextjs", "nextjs-15", "app-router"]
}
```

### When to Create Separate Version Skills

Create separate skill when framework version has:
- ✅ Breaking API changes (React class components → hooks)
- ✅ Major architectural shifts (Next.js Pages → App Router)
- ✅ Different mental models (Vue 2 Options → Vue 3 Composition)
- ✅ Incompatible upgrade paths

### When to Update Existing Skill

Update existing skill (bump MINOR) when:
- ✅ Framework adds backward-compatible features
- ✅ New APIs supplement existing ones (React 19 `use()` hook)
- ✅ Performance improvements don't change API
- ✅ Patch releases with bug fixes

**Example**: React 18.2 → React 18.3 = PATCH or MINOR update to existing skill

## Metadata Fields for Versioning

All skills must include these versioning-related fields in `metadata.json`:

```json
{
  "name": "skill-name",
  "version": "1.0.0",           // Semantic version of the skill content
  "created": "2025-11-30",      // ISO date when skill first created
  "updated": "2025-11-30",      // ISO date of last content update
  "modified": "2025-11-30",     // ISO date of any modification (same as updated)
  "maintainer": "Claude MPM Team",
  "author": "claude-mpm-skills",
  "repository": "https://github.com/bobmatnyc/claude-mpm-skills"
}
```

### Field Definitions

- **version**: Skill content version (semantic versioning)
- **created**: Never changes after initial creation
- **updated**: Changes with any version increment
- **modified**: Alias for updated (kept for compatibility)
- **maintainer**: Team or individual responsible for updates
- **author**: Original creator or organization

## Version Increment Workflow

### Step 1: Determine Change Type

Ask these questions:
1. Does this break existing skill consumption? → **MAJOR**
2. Does this add new content/features? → **MINOR**
3. Is this just a fix or clarification? → **PATCH**

### Step 2: Update metadata.json

```bash
# MAJOR increment: 1.0.0 → 2.0.0
# MINOR increment: 1.0.0 → 1.1.0
# PATCH increment: 1.0.0 → 1.0.1
```

Update fields:
```json
{
  "version": "1.1.0",          // ← Increment this
  "updated": "2025-11-30",     // ← Update to today
  "modified": "2025-11-30"     // ← Update to today
}
```

### Step 3: Document Changes

Add entry to skill's CHANGELOG (if exists) or commit message:

```
feat(react): add React 19 hooks section - v1.1.0

- Add `use()` hook documentation
- Add `useOptimistic()` examples
- Update best practices for concurrent rendering

Bumped version: 1.0.0 → 1.1.0 (MINOR - new features)
```

### Step 4: Commit with Clear Message

```bash
git add toolchains/javascript/frameworks/react/
git commit -m "feat(react): add React 19 hooks - bump to v1.1.0

- Document use() and useOptimistic() hooks
- Add concurrent rendering patterns
- Update examples for React 19

Version: 1.0.0 → 1.1.0 (MINOR)

🤖👥 Generated with [Claude MPM](https://github.com/bobmatnyc/claude-mpm)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Token Count Updates

When skill content changes **significantly**, update token estimates:

### Recalculate Token Counts

1. **Entry Point**: Count tokens in YAML frontmatter `progressive_disclosure.entry_point`
2. **Full Content**: Count tokens in entire SKILL.md file

### Update metadata.json

```json
{
  "entry_point_tokens": 85,  // ← Update if entry point changed
  "full_tokens": 5200        // ← Update if full content grew/shrank
}
```

### When to Recalculate

- ✅ After adding major sections (MINOR version)
- ✅ After restructuring content (MAJOR version)
- ✅ If token count changes by >10% (any version)
- ❌ Not needed for PATCH fixes (minor impact)

## Related Skills Updates

When creating new skills or versions:

### Update Cross-References

If **Skill A** references **Skill B**, and Skill B gets major version:

```json
// OLD: tailwind/metadata.json
{
  "related_skills": ["../../../javascript/frameworks/react"]
}

// NEW: If react-19 is created
{
  "related_skills": [
    "../../../javascript/frameworks/react",      // React 18
    "../../../javascript/frameworks/react-19"    // React 19
  ]
}
```

Bump related skill's **PATCH version** for cross-reference updates.

## Deprecation Strategy

### Marking Skills as Deprecated

When framework version becomes obsolete:

```json
{
  "name": "vue-2",
  "version": "1.5.0",
  "deprecated": true,
  "deprecation_notice": "Vue 2 reached end-of-life. Use vue-3 skill instead.",
  "successor": "../vue-3",
  "tags": ["vue", "vue-2", "legacy", "deprecated"]
}
```

Add deprecation notice to SKILL.md:

```markdown
> ⚠️ **DEPRECATED**: Vue 2 reached end-of-life on December 31, 2023.
> Consider migrating to [Vue 3](../vue-3/SKILL.md) for continued support.
```

### Retention Policy

- Keep deprecated skills for **2 years** after successor release
- Clearly mark as deprecated in metadata and content
- Provide migration path to successor skill

## Version History Tracking

### Optional: CHANGELOG.md

For skills with frequent updates, maintain `CHANGELOG.md`:

```markdown
# Changelog

## [1.2.0] - 2025-11-30

### Added
- React 19 `use()` hook documentation
- Server Components best practices

### Changed
- Updated async/await patterns for modern syntax

## [1.1.0] - 2025-11-15

### Added
- Suspense boundary examples
- Error boundary patterns

## [1.0.0] - 2025-11-01

Initial release
```

## Examples by Skill Type

### Toolchain Skill (React)

```json
{
  "name": "react",
  "version": "1.2.0",
  "category": "toolchain",
  "framework": "react",
  "created": "2025-11-21",
  "updated": "2025-11-30"
}
```

**Version History**:
- `1.0.0` - Initial React 18 skill
- `1.1.0` - Added hooks best practices
- `1.2.0` - Added React 19 features (use, useOptimistic)

### Framework Version Skill (Next.js)

```json
{
  "name": "nextjs-v15",
  "version": "1.0.0",
  "category": "toolchain",
  "framework": "nextjs",
  "tags": ["nextjs", "nextjs-15", "app-router"],
  "created": "2025-11-29",
  "updated": "2025-11-29"
}
```

**Separate from**: `nextjs-v14` (different App Router APIs)

### Universal Skill (Tailwind)

```json
{
  "name": "tailwind",
  "version": "1.0.0",
  "category": "universal",
  "subcategory": "styling",
  "created": "2025-11-30",
  "updated": "2025-11-30"
}
```

**Future Updates**:
- `1.1.0` - Add Tailwind v4 features when released
- `2.0.0` - If Tailwind v4 breaks existing patterns

## Summary: Quick Decision Tree

```
Is the change...

Breaking skill structure/format?
├─ YES → MAJOR version (2.0.0)
└─ NO ↓

Adding new features/sections?
├─ YES → MINOR version (1.1.0)
└─ NO ↓

Fixing errors/typos?
└─ YES → PATCH version (1.0.1)

Framework version changed?
├─ Breaking changes → Create new skill (react-19)
└─ Compatible additions → MINOR version (1.1.0)
```

## Best Practices

1. **Always increment version** when changing content
2. **Update `updated` field** with current date
3. **Use clear commit messages** mentioning version bump
4. **Recalculate token counts** for major content changes
5. **Update cross-references** when creating version-specific skills
6. **Document deprecations** clearly in both metadata and content
7. **Keep versions synchronized** with actual content changes
8. **Start at 1.0.0** for production-ready skills (not 0.1.0)

## References

- Semantic Versioning 2.0.0: https://semver.org/
- Claude Code Skills Documentation: https://code.claude.com/docs/en/skills
- Repository: https://github.com/bobmatnyc/claude-mpm-skills
