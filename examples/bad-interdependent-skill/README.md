# ⚠️ Bad Interdependent Skill Example (Anti-Patterns)

**WARNING**: This directory contains **ANTI-PATTERN** examples showing what **NOT** to do.

**DO NOT COPY THIS STRUCTURE**. See [../good-self-contained-skill/](../good-self-contained-skill/) for correct approach.

---

## Purpose

This example demonstrates **common violations** of the self-containment standard. Study these anti-patterns to understand what to avoid when creating skills.

---

## ❌ Critical Violations Demonstrated

### Violation 1: Relative Path Dependencies

**Example from SKILL.md**:
```markdown
For setup, see [../setup-skill/SKILL.md](../setup-skill/SKILL.md)
For testing, see [../../testing/pytest/](../../testing/pytest/)
```

**Why It's Wrong**:
- Assumes hierarchical directory structure
- Breaks when deployed to flat directory (`~/.claude/skills/`)
- Links become invalid when skill deployed standalone

**Detection**:
```bash
$ grep -r "\.\\./" bad-interdependent-skill/
bad-interdependent-skill/SKILL.md:42:For setup, see [../setup-skill/...
```

**How to Fix**: Replace with informational skill name references (no paths)

---

### Violation 2: Missing Essential Content

**Example from SKILL.md**:
```markdown
## Testing

See pytest-patterns skill for all testing code.
```

**Why It's Wrong**:
- No actual testing patterns included
- Skill is incomplete without other skills
- Users can't accomplish testing tasks with only this skill

**How to Fix**: Inline essential testing patterns (20-50 lines)

---

### Violation 3: Hard Skill Dependencies

**Example from SKILL.md**:
```markdown
## Prerequisites

**Required Skills**:
1. setup-skill - Must be installed first
2. database-skill - Required for database operations

This skill will not work without these dependencies.
```

**Why It's Wrong**:
- Creates deployment coupling
- Violates self-containment principle
- Limits deployment flexibility

**How to Fix**: Make skill self-sufficient, note optional enhancements

---

### Violation 4: Cross-Skill Imports

**Example from SKILL.md**:
```python
# ❌ DON'T DO THIS
from skills.database_skill import get_db_session
from skills.pytest_patterns import fixture_factory
```

**Why It's Wrong**:
- Creates runtime dependency on other skills
- Code won't run without other skills installed
- Violates Python module boundaries

**How to Fix**: Include patterns inline within skill

---

### Violation 5: Hierarchical Directory Assumptions

**Example from SKILL.md**:
```markdown
Navigate to parent directories for related skills:
- `../` - Other framework skills
- `../../testing/` - Testing skills
```

**Why It's Wrong**:
- Assumes specific directory structure
- Won't work in flat deployment
- Location-dependent documentation

**How to Fix**: Reference skills by name only (no navigation)

---

### Violation 6: Incomplete Examples

**Example from SKILL.md**:
```python
# Database setup
# (See database-skill for complete implementation)
class User(db.Model):
    # ... see database-skill for model definition ...
    pass
```

**Why It's Wrong**:
- Examples are fragments, not complete code
- Users can't copy-paste and run
- No actual implementation guidance

**How to Fix**: Provide complete, working examples

---

### Violation 7: references/ with Cross-Skill Paths

**Example structure**:
```
bad-interdependent-skill/
└── references/
    └── testing.md          # Contains: ../../pytest-patterns/
```

**Why It's Wrong**:
- Progressive disclosure leads outside skill
- Breaks in flat deployment
- References aren't self-contained

**How to Fix**: Keep references/ within skill boundary

---

### Violation 8: metadata.json with Skill Dependencies

**Example from metadata.json**:
```json
{
  "requires": ["setup-skill", "database-skill"],
  "self_contained": false
}
```

**Why It's Wrong**:
- Lists other skills as requirements
- Marks skill as not self-contained
- Creates deployment coupling

**How to Fix**: Use `"complementary_skills"` field instead

---

## Violation Detection

### Automated Checks

Run these commands to detect violations:

```bash
# Check 1: Relative path violations
grep -r "\.\\./" bad-interdependent-skill/
# Expected: Should find violations (this is bad example)

# Check 2: Cross-skill imports
grep -r "from skills\." bad-interdependent-skill/
# Expected: Should find violations

# Check 3: "Required" language
grep -i "requires.*skill\|must.*install" bad-interdependent-skill/SKILL.md
# Expected: Should find violations

# Check 4: Hierarchical assumptions
grep -i "navigate.*parent\|directory.*structure" bad-interdependent-skill/SKILL.md
# Expected: Should find violations
```

### Manual Review Checklist

- [ ] ❌ Uses `../` or `../../` paths (VIOLATION)
- [ ] ❌ Says "see other skill for X" without inlining (VIOLATION)
- [ ] ❌ Lists other skills as "required" (VIOLATION)
- [ ] ❌ Imports from other skills (VIOLATION)
- [ ] ❌ Assumes directory structure (VIOLATION)
- [ ] ❌ Provides incomplete examples (VIOLATION)
- [ ] ❌ references/ has cross-skill paths (VIOLATION)
- [ ] ❌ metadata.json lists skill dependencies (VIOLATION)

---

## How to Fix These Violations

### Fix Pattern 1: Replace Relative Paths

**Before (Wrong)**:
```markdown
See [pytest patterns](../../testing/pytest/SKILL.md)
```

**After (Correct)**:
```markdown
Consider pytest-patterns skill for advanced testing (if deployed)
```

---

### Fix Pattern 2: Inline Essential Content

**Before (Wrong)**:
```markdown
## Testing
See pytest-patterns skill for testing code.
```

**After (Correct)**:
```markdown
## Testing (Self-Contained)

**Essential pytest pattern** (inlined):
[20-50 lines of actual code]

**Advanced patterns** (if pytest-patterns deployed):
[Brief description]
```

---

### Fix Pattern 3: Remove Hard Dependencies

**Before (Wrong)**:
```markdown
**Required Skills**: pytest-patterns, database-skill
```

**After (Correct)**:
```markdown
**Complementary Skills** (optional, if deployed):
- pytest-patterns: Testing enhancements
- database-skill: ORM optimization
```

---

### Fix Pattern 4: Self-Contained Imports

**Before (Wrong)**:
```python
from skills.database import get_db_session
```

**After (Correct)**:
```python
# Inline the pattern
@contextmanager
def get_db_session():
    """Database session (self-contained)."""
    # Implementation here
```

---

### Fix Pattern 5: Remove Directory Assumptions

**Before (Wrong)**:
```markdown
Navigate to `../../testing/` for testing skills
```

**After (Correct)**:
```markdown
**Testing Skills** (informational):
- pytest-patterns: Testing framework
- test-driven-development: TDD workflow
```

---

### Fix Pattern 6: Complete Examples

**Before (Wrong)**:
```python
def test_user():
    # ... see pytest-patterns for fixtures ...
    pass
```

**After (Correct)**:
```python
@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    """Complete working test."""
    response = client.post("/users", json={
        "username": "test"
    })
    assert response.status_code == 201
```

---

### Fix Pattern 7: Self-Contained references/

**Before (Wrong)**:
```
references/testing.md contains:
"See ../../pytest-patterns/ for details"
```

**After (Correct)**:
```
references/advanced-testing.md contains:
"Advanced patterns for THIS skill:
[actual content about this skill]

For complementary patterns, see pytest-patterns (if deployed)"
```

---

### Fix Pattern 8: Update metadata.json

**Before (Wrong)**:
```json
{
  "requires": ["other-skill"],
  "self_contained": false
}
```

**After (Correct)**:
```json
{
  "requires": [],
  "self_contained": true,
  "complementary_skills": ["other-skill"]
}
```

---

## Transformation Example

### Before (All Violations)

```markdown
# Bad Skill

## Testing

This skill requires pytest-patterns skill for testing.

See [pytest patterns](../../testing/pytest/SKILL.md) for:
- Fixtures (../../testing/pytest/fixtures.md)
- Assertions (../../testing/pytest/assertions.md)

Install pytest-patterns first:
```bash
from skills.pytest_patterns import test_client
```
```

### After (Self-Contained)

```markdown
# Good Skill

## Testing (Self-Contained)

**Essential pytest patterns** (inlined):

```python
import pytest
from app import create_app

@pytest.fixture
def client():
    """Test client fixture."""
    app = create_app()
    return app.test_client()

def test_home(client):
    """Test homepage."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data
```

**Advanced fixtures** (if pytest-patterns skill deployed):
- Parametrized fixtures
- Database fixtures with rollback
- Mock fixtures for external services

*See pytest-patterns skill for comprehensive testing guide.*
```

---

## Checklist: Is Your Skill Like This Bad Example?

Use this checklist to verify your skill DOESN'T have these violations:

- [ ] ❌ My skill has `../` paths? (FIX REQUIRED)
- [ ] ❌ My skill says "see other skill" without inlining? (FIX REQUIRED)
- [ ] ❌ My skill lists other skills as "required"? (FIX REQUIRED)
- [ ] ❌ My skill imports from other skills? (FIX REQUIRED)
- [ ] ❌ My skill assumes directory structure? (FIX REQUIRED)
- [ ] ❌ My skill has incomplete examples? (FIX REQUIRED)
- [ ] ❌ My references/ has cross-skill paths? (FIX REQUIRED)
- [ ] ❌ My metadata.json lists skill dependencies? (FIX REQUIRED)

**If you checked ANY boxes, your skill has violations. Fix them before submitting.**

---

## Comparison: Bad vs. Good

| Aspect | Bad Example (This) | Good Example |
|--------|-------------------|--------------|
| **Paths** | `../../other-skill/` | Skill names only |
| **Content** | "See other skill" | Inlined patterns |
| **Dependencies** | "Requires X skill" | "Complements X (optional)" |
| **Imports** | `from skills.X import` | Inline implementation |
| **Structure** | Assumes hierarchy | Flat-compatible |
| **Examples** | Fragments | Complete working code |
| **references/** | Cross-skill paths | Within skill only |
| **metadata** | `"requires": ["X"]` | `"requires": []` |

---

## Study This Example To Learn

### What to Look For

1. **Identify each violation** - Find all 8 violation types
2. **Understand why it's wrong** - Read the explanations
3. **See the fix** - Compare with good example
4. **Apply to your skills** - Avoid these patterns

### Learning Exercise

1. Read through this SKILL.md
2. Find each violation (marked with ❌)
3. Read the "How to Fix" section
4. Compare with [good-self-contained-skill](../good-self-contained-skill/)
5. Apply lessons to your own skills

---

## Resources

- **[good-self-contained-skill](../good-self-contained-skill/)**: Correct template
- **[SKILL_SELF_CONTAINMENT_STANDARD.md](../../docs/SKILL_SELF_CONTAINMENT_STANDARD.md)**: Complete standard
- **[SKILL_CREATION_PR_CHECKLIST.md](../../docs/SKILL_CREATION_PR_CHECKLIST.md)**: PR checklist

---

## Summary

**This example is intentionally broken** to teach what NOT to do.

### 8 Critical Violations:
1. Relative path dependencies
2. Missing essential content
3. Hard skill dependencies
4. Cross-skill imports
5. Hierarchical directory assumptions
6. Incomplete examples
7. Cross-skill references/ paths
8. Skill dependencies in metadata.json

**Learn from these mistakes. Build self-contained skills instead.**

---

**Remember**: If your skill looks like this example, it violates self-containment. Fix it before submitting!
