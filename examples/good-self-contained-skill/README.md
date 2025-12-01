# Good Self-Contained Skill Example

This directory contains a **template example** of a properly self-contained skill that follows all best practices from the [SKILL_SELF_CONTAINMENT_STANDARD.md](../../docs/SKILL_SELF_CONTAINMENT_STANDARD.md).

---

## What Makes This a Good Example?

### ✅ Self-Containment Principles

1. **Complete Content**: All essential patterns are inlined in SKILL.md
2. **No Dependencies**: Zero relative paths to other skills
3. **Works Standalone**: Can be deployed to any directory structure
4. **Graceful Degradation**: Notes optional enhancements without requiring them
5. **Informational References**: Mentions complementary skills by name only

---

## Key Features Demonstrated

### 1. Essential Content Inlining

**Pattern**: Include 20-50 line code examples for core functionality

**Example from SKILL.md**:
```python
# Complete database session pattern (30 lines)
@contextmanager
def get_db_session():
    """Database session context manager."""
    session = db.create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

**Why**: Users can accomplish database tasks with ONLY this skill.

---

### 2. No Relative Path Violations

**Pattern**: Never reference other skills with file paths

**Example**:
```markdown
❌ DON'T: See [pytest patterns](../../testing/pytest/SKILL.md)
✅ DO: Consider pytest-patterns skill for advanced testing (if deployed)
```

**Verification**:
```bash
$ grep -r "\.\\./" good-self-contained-skill/
(empty - no violations)
```

---

### 3. Complementary Skills Section

**Pattern**: List related skills informationally

**Example from SKILL.md**:
```markdown
## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **pytest-patterns**: Advanced testing patterns and fixtures
  - *Use case*: Comprehensive test suites with parametrization
  - *Integration*: Enhance basic testing patterns shown above
  - *Status*: Optional - basic testing patterns included in this skill

**Note**: All complementary skills are independently deployable.
```

**Why**: Clear that other skills enhance but aren't required.

---

### 4. Graceful Degradation

**Pattern**: Basic functionality self-contained, advanced features note optional skills

**Example from SKILL.md**:
```markdown
## Testing Pattern (Self-Contained)

**Essential testing patterns** - inlined from testing best practices:
[30-50 lines of complete testing code]

**Advanced fixtures** (if pytest-patterns skill deployed):
- Parametrized fixtures
- Fixture factories
- Scope management

*See pytest-patterns skill for comprehensive patterns.*
```

**Why**: Skill works independently, enhancements are optional.

---

### 5. Complete Examples

**Pattern**: All code examples are complete, working code (not fragments)

**Example from SKILL.md**:
```python
# Complete minimal application (self-contained)
from example_framework import App, route

app = App()

@route("/")
def home():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

**Why**: Users can copy-paste and run immediately.

---

### 6. Metadata Best Practices

**metadata.json highlights**:
```json
{
  "self_contained": true,
  "requires": [],  // No skill dependencies
  "dependencies": ["external-package"],  // Only external packages
  "complementary_skills": ["other-skill"],  // Informational only
  "tags": ["self-contained"]  // Self-containment tag
}
```

---

## Testing Self-Containment

### Isolation Test

```bash
# 1. Copy to isolated directory
mkdir -p /tmp/skill-test
cp -r good-self-contained-skill /tmp/skill-test/

# 2. Verify works standalone
cd /tmp/skill-test/good-self-contained-skill
cat SKILL.md  # Complete content - no missing references

# 3. Check for violations
grep -r "\.\\./" .  # Empty output - no relative paths
```

### Verification Commands

```bash
# All these should return empty (no violations)
grep -r "\.\\./" good-self-contained-skill/
grep -r "from skills\." good-self-contained-skill/
grep -r "import.*\.\./" good-self-contained-skill/
grep -i "requires.*skill" good-self-contained-skill/SKILL.md
```

---

## Use as Template

### When Creating New Skills

1. **Copy this structure**:
   ```bash
   cp -r examples/good-self-contained-skill your-new-skill
   ```

2. **Update metadata.json**:
   - Change name, category, toolchain
   - Keep `"self_contained": true`
   - Keep `"requires": []`

3. **Fill in SKILL.md**:
   - Follow progressive disclosure structure
   - Inline essential patterns (20-50 lines each)
   - Note complementary skills informationally
   - Include complete examples

4. **Test isolation**:
   ```bash
   grep -r "\.\\./" your-new-skill/
   # Should be empty
   ```

5. **Verify with checklist**:
   - Use [SKILL_CREATION_PR_CHECKLIST.md](../../docs/SKILL_CREATION_PR_CHECKLIST.md)

---

## Structure

```
good-self-contained-skill/
├── SKILL.md           # Complete, self-contained documentation
├── metadata.json      # Metadata with self_contained: true
├── README.md          # This file - explains the example
└── references/        # Optional progressive disclosure
    ├── advanced-patterns.md
    ├── performance.md
    └── api-reference.md
```

**Note**: `references/` is optional. Main SKILL.md is self-sufficient.

---

## Key Patterns to Copy

### Pattern 1: Inline Essential Content
```markdown
## Core Pattern (Self-Contained)

**Essential pattern** (inlined):
[20-50 lines of complete working code]

**Advanced usage** (if advanced-skill deployed):
- Feature 1
- Feature 2
```

### Pattern 2: Complementary Skills
```markdown
## Complementary Skills

- **skill-name**: How it complements
  - *Use case*: When to combine
  - *Status*: Optional enhancement

*Note: All skills independently deployable.*
```

### Pattern 3: Complete Examples
```python
# Complete working example (not fragment)
# Users can copy-paste and run
from framework import App

app = App()

@app.route("/")
def home():
    return {"message": "Works!"}

if __name__ == "__main__":
    app.run()
```

---

## Checklist for This Example

Verify this example follows all rules:

- [x] ✅ No `../` relative paths anywhere
- [x] ✅ Essential content inlined (database, testing, deployment)
- [x] ✅ Complete working examples (not fragments)
- [x] ✅ Complementary skills listed informationally
- [x] ✅ Graceful degradation implemented
- [x] ✅ Works in flat directory deployment
- [x] ✅ metadata.json has `self_contained: true`
- [x] ✅ No skill dependencies in `requires` field
- [x] ✅ Tested in isolation successfully
- [x] ✅ All grep verification commands pass

---

## Compare with Bad Example

See [../bad-interdependent-skill/](../bad-interdependent-skill/) for anti-patterns to avoid.

---

## Resources

- **[SKILL_SELF_CONTAINMENT_STANDARD.md](../../docs/SKILL_SELF_CONTAINMENT_STANDARD.md)**: Complete standard
- **[SKILL_CREATION_PR_CHECKLIST.md](../../docs/SKILL_CREATION_PR_CHECKLIST.md)**: PR checklist
- **[CONTRIBUTING.md](../../CONTRIBUTING.md)**: General guidelines

---

**Use this example as your template for creating new, properly self-contained skills.**
