# Bundle Creation Guide

Complete guide for creating new ecosystem bundles for Claude MPM Skills.

## Philosophy

**Bundles = Curated Skill Collections**: Each bundle represents a complete development stack or workflow that includes all necessary skills for a specific use case.

**Flat Deployment by Default**: All bundles deploy skills as flat collections for maximum compatibility with Claude Code's skill discovery system.

## Bundle Creation Workflow

### 1. Identify Use Case

Determine the development scenario or workflow:
- **Complete Stack**: Full-stack TypeScript, Python Web, etc.
- **Specific Domain**: Testing, Data, AI/MCP, etc.
- **Workflow**: TDD, Debugging, Deployment, etc.

**Good Bundle Ideas**:
- ✅ Python Testing Stack (testing-focused)
- ✅ React Ecosystem (framework + state + testing)
- ✅ AI/MCP Development (AI application stack)

**Poor Bundle Ideas**:
- ❌ Random Skills (no coherent theme)
- ❌ Single Skill (just use skill directly)
- ❌ Kitchen Sink (too many unrelated skills)

### 2. Research Skill Dependencies

Identify skills that naturally work together:

```bash
# Search for related skills
find toolchains/ universal/ -name "*.md" | xargs grep -l "keyword"

# Check skill metadata
cat toolchains/python/testing/pytest/metadata.json
```

**Dependency Patterns**:
- **Hard Dependencies**: Skill A requires Skill B (e.g., Next.js requires React)
- **Synergies**: Skills work better together (e.g., FastAPI + Pydantic)
- **Methodology**: Process skills (e.g., TDD + systematic-debugging)

### 3. Create Bundle Directory

```bash
cd .bundles/
mkdir my-stack-bundle
cd my-stack-bundle
```

### 4. Copy Template Files

```bash
cp ../deploy-template.sh deploy.sh
chmod +x deploy.sh
```

### 5. Create skills.list

Format: `path/to/skill:version` or `path/to/skill` (for latest)

```text
# My Stack Bundle - Skill Manifest
# Version: 1.0.0

# Core Framework
toolchains/language/frameworks/framework-name

# Data & Validation
toolchains/language/validation/validator

# Testing
toolchains/language/testing/test-framework
universal/testing/test-driven-development

# Methodology
universal/debugging/systematic-debugging
```

**Best Practices**:
- Group skills by category (Core, Data, Testing, etc.)
- Use comments to explain groupings
- List skills in logical dependency order
- Include version pins for stability (optional)

### 6. Write BUNDLE.md

Use this template structure:

```markdown
# Bundle Name

**Version:** 1.0.0
**Category:** Python|TypeScript|JavaScript|Universal|AI
**Deployment Mode:** flat (recommended)

## Bundle Purpose

[2-3 sentence description of what this bundle provides and why these skills belong together]

## Included Skills

- **skill-name** (path/to/skill) - Brief description
- **another-skill** (path/to/skill) - Brief description

## Use Cases

**When to Deploy This Bundle:**
- Use case 1
- Use case 2
- Use case 3

**What You Get:**
- Benefit 1
- Benefit 2
- Benefit 3

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| skill-1 | ✅ Yes | 🚀 Enhanced | None |
| skill-2 | ✅ Yes | 🚀 Enhanced | skill-1 (optional) |

**Bundle Synergies:**
- skill-1 + skill-2: Specific benefit
- skill-2 + skill-3: Another benefit

## Integration Example

```language
// Show how skills work together
// Concrete code example demonstrating synergy
```

## Version History

- **1.0.0** (YYYY-MM-DD): Initial release with X skills
```

### 7. Validate Bundle

```bash
# Validate all skills exist
./deploy.sh --validate

# Expected output:
# [SUCCESS] Found: path/to/skill
# [SUCCESS] Validation passed: all skills found
```

**Common Validation Errors**:
- `[ERROR] Missing: path/to/skill` → Check skill path is correct
- Directory not found → Skill may be in different location

### 8. Test Deployment

```bash
# Test in temporary directory
./deploy.sh --flat /tmp/test-bundle

# Verify deployment
ls /tmp/test-bundle/
cat /tmp/test-bundle/.bundle-manifest-*.json
```

### 9. Document Bundle

Add bundle to `.bundles/README.md`:

```markdown
### Category Name
- **bundle-name**: Brief description of bundle purpose
```

## Bundle Sizing Guidelines

**Optimal Bundle Size**: 4-8 skills

- **Too Small** (1-3 skills): Consider if bundle is necessary
- **Optimal** (4-8 skills): Focused, cohesive skill set
- **Large** (9-15 skills): Acceptable for complete stacks
- **Too Large** (16+ skills): Split into multiple bundles

## Bundle Naming Conventions

**Format**: `{domain}-{purpose}-{type}`

**Examples**:
- `python-testing-stack` → Language + Purpose + Type
- `react-ecosystem` → Framework + Scope
- `ai-mcp-development` → Domain + Protocol + Purpose
- `universal-development` → Scope + Purpose

**Avoid**:
- ❌ Generic names: `bundle-1`, `skills-collection`
- ❌ Abbreviations: `py-test`, `ts-data`
- ❌ Version in name: `python-stack-v2`

## Skill Path Resolution

**Toolchain Skills**: `toolchains/{language}/{category}/{skill-name}`
**Universal Skills**: `universal/{category}/{skill-name}`

**Examples**:
```
toolchains/python/testing/pytest
toolchains/typescript/data/drizzle
toolchains/ai/frameworks/langchain
universal/testing/test-driven-development
universal/debugging/systematic-debugging
```

## Deployment Script Features

The `deploy.sh` script provides:

1. **Validation**: `./deploy.sh --validate`
   - Checks all skills exist
   - Reports missing skills
   - Exit code 0 = success, 1 = failure

2. **Flat Deployment**: `./deploy.sh --flat /target/dir`
   - Copies skills to flat structure
   - Creates deployment manifest
   - Skips already-deployed skills

3. **Hierarchical Deployment**: `./deploy.sh --hierarchical /target/dir`
   - Preserves directory structure
   - Useful for archive/backup purposes

## Bundle Versioning

**Semantic Versioning**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (skill removed/replaced)
- **MINOR**: New skills added (backward compatible)
- **PATCH**: Documentation/metadata updates

**Version Locations**:
1. `BUNDLE.md` header: `**Version:** 1.0.0`
2. `skills.list` comment: `# Version: 1.0.0`

## Quality Checklist

Before committing new bundle:

- [ ] All skills validated with `./deploy.sh --validate`
- [ ] BUNDLE.md includes complete metadata
- [ ] skills.list has clear categories
- [ ] Integration example demonstrates synergy
- [ ] Compatibility matrix shows dependencies
- [ ] Test deployment successful
- [ ] Bundle listed in `.bundles/README.md`
- [ ] Naming follows conventions
- [ ] 4-8 skills (optimal range)

## Common Pitfalls

1. **Wrong Skill Paths**
   - ❌ `python/testing/pytest` (missing `toolchains/`)
   - ✅ `toolchains/python/testing/pytest`

2. **Missing Dependencies**
   - Include all required skills in bundle
   - Document optional dependencies in compatibility matrix

3. **Overly Broad Bundles**
   - Split into focused bundles (e.g., "python-stack" → "python-web-stack", "python-data-stack")

4. **No Integration Example**
   - Always show how skills work together
   - Concrete code examples, not theory

## Example Bundle: python-testing-stack

Perfect bundle example demonstrating all best practices:

**Strengths**:
- Focused purpose (testing)
- Clear synergies (pytest + asyncio for async tests)
- Methodology skills (TDD, debugging)
- Optimal size (5 skills)
- Validates successfully
- Complete documentation

**Structure**:
```
python-testing-stack/
├── BUNDLE.md           # Complete metadata
├── skills.list         # 5 skills with categories
└── deploy.sh          # Deployment script
```

Study this bundle as reference when creating new bundles.

## Support

Questions about bundle creation? Check:
- **Existing Bundles**: Study 8 reference bundles in `.bundles/`
- **Skill Catalog**: `README.md` in repo root
- **Deployment Script**: `deploy-template.sh` comments
