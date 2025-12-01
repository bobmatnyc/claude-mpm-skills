# Skill Self-Containment Standard

**Version:** 1.0.0
**Date:** 2025-11-30
**Status:** Mandatory for all new skills

---

## Table of Contents

1. [Core Principle](#core-principle)
2. [Absolute Rules](#absolute-rules)
3. [Reference Patterns](#reference-patterns)
4. [Content Inlining Guidelines](#content-inlining-guidelines)
5. [Soft Reference Format](#soft-reference-format)
6. [Testing Checklist](#testing-checklist)
7. [Bundle vs. Skill Responsibilities](#bundle-vs-skill-responsibilities)
8. [PR Checklist Template](#pr-checklist-template)
9. [Examples from Fixed Skills](#examples-from-fixed-skills)
10. [FAQ](#faq)

---

## Core Principle

### What is Self-Containment?

**A self-contained skill is a standalone, atomic unit of knowledge that functions independently without requiring other skills to be present.**

Every skill must be deployable to a flat directory structure (e.g., `~/.claude/skills/`) and remain fully functional without any parent directories, sibling skills, or hierarchical assumptions.

### Why Skills Must Be Atomic Units

Claude Code's skill discovery system may deploy skills in various ways:
- **Flat deployment**: All skills in single directory (`~/.claude/skills/`)
- **Bundle deployment**: Curated collections (`~/.claude/bundles/fastapi-bundle/`)
- **Selective deployment**: User picks individual skills from catalog
- **Toolchain detection**: Auto-deploy based on project analysis

**Self-containment ensures skills work correctly in ALL deployment scenarios.**

### How Deployment Flattening Works

When Claude Code deploys skills, it may:

1. **Copy skills to flat structure**:
   ```
   Source (hierarchical):
   toolchains/python/frameworks/fastapi/
   toolchains/python/testing/pytest/
   universal/testing/test-driven-development/

   Deployed (flat):
   ~/.claude/skills/fastapi/
   ~/.claude/skills/pytest/
   ~/.claude/skills/test-driven-development/
   ```

2. **Relative paths break**:
   ```markdown
   ❌ [pytest](../../testing/pytest/SKILL.md)  # Broken - no parent directories
   ✅ pytest skill (if deployed)                # Works - informational reference
   ```

3. **Skills must function independently**:
   - No assumptions about directory structure
   - No relative path navigation
   - No dependencies on other skills being present

### Benefits for Claude Code Skill Discovery

Self-contained skills enable:
- **Flexible deployment**: Any combination of skills works
- **Selective loading**: Users choose only needed skills
- **Bundle independence**: Skills work outside bundles
- **Discoverability**: Skills stand alone in catalog
- **Maintainability**: Changes don't cascade across skills
- **Testing**: Each skill verifiable in isolation

---

## Absolute Rules

### The "NEVER" List

❌ **NEVER use relative paths to other skills**
```markdown
❌ [FastAPI Skill](../../frameworks/fastapi/SKILL.md)
❌ See ../testing/pytest/ for test examples
❌ Include: ../../shared/patterns.md
```

❌ **NEVER depend on other skills being present**
```markdown
❌ "This skill requires pytest skill to be installed"
❌ "Use alongside fastapi-local-dev skill (required)"
❌ "Assumes test-driven-development skill is available"
```

❌ **NEVER import code from other skills**
```python
# ❌ DON'T DO THIS
from skills.fastapi.patterns import setup_app
from ..testing.pytest.fixtures import db_session
```

❌ **NEVER assume hierarchical directory structure**
```markdown
❌ This skill lives in toolchains/python/frameworks/
❌ Navigate to parent directory for related skills
❌ See sibling skills in this category
```

### The "ALWAYS" List

✅ **ALWAYS inline essential content**
```markdown
✅ Include critical code patterns directly in SKILL.md
✅ Duplicate core concepts if needed across skills
✅ Provide self-sufficient examples
```

✅ **ALWAYS use skill names for references (informational only)**
```markdown
✅ "Consider using pytest skill for testing"
✅ "Complements fastapi-local-dev skill"
✅ "Works well with test-driven-development workflow"
```

✅ **ALWAYS test skill in isolation**
```bash
✅ Copy skill to empty directory
✅ Verify all content accessible
✅ Check no broken links or missing references
```

✅ **ALWAYS provide graceful degradation**
```markdown
✅ "If pytest skill available, you can also..."
✅ "For advanced patterns, see fastapi skill (if deployed)"
✅ "Note: Full test examples available in pytest skill"
```

---

## Reference Patterns

### Before/After Examples

#### Example 1: Hard Path Dependency → Inlined Content

**❌ BEFORE (Hard Dependency)**
```markdown
## Testing

For testing patterns, see [pytest skill](../../testing/pytest/SKILL.md).

Key fixtures:
- db_session: See pytest/fixtures.md
- client: See pytest/client.md
```

**✅ AFTER (Self-Contained)**
```markdown
## Testing

**Essential Pytest Patterns** (inlined from pytest skill):

```python
# Test fixtures
@pytest.fixture
def db_session():
    """Database session fixture."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    """Test client fixture."""
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
```

**Complementary Skills:**
- **pytest**: Full testing framework documentation (if deployed)
- **test-driven-development**: TDD workflow guidance (if deployed)
```

#### Example 2: Cross-Skill Imports → Self-Contained Implementation

**❌ BEFORE (Import Dependency)**
```markdown
## FastAPI Integration

This skill integrates with fastapi skill. Install both skills:

```python
# Use patterns from fastapi skill
from skills.fastapi import setup_routes, configure_middleware
```

Refer to `../../frameworks/fastapi/` for setup instructions.
```

**✅ AFTER (Self-Contained)**
```markdown
## FastAPI Integration

**Self-Contained Integration Pattern**:

```python
# Complete FastAPI setup (no external dependencies)
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example model
class User(BaseModel):
    username: str
    email: str

# Example route with dependency injection
@app.post("/users/")
def create_user(user: User, db: Session = Depends(get_db)):
    # Implementation here
    return user
```

**Complementary Skills:**
- **fastapi-local-dev**: Advanced FastAPI patterns (if deployed)
- **pydantic**: Validation best practices (if deployed)
```

#### Example 3: Hierarchical Assumptions → Flat-Compatible Design

**❌ BEFORE (Hierarchical Assumption)**
```markdown
## Related Skills

Navigate to parent directory to find:
- pytest (../testing/pytest/)
- asyncio (../async/asyncio/)
- sqlalchemy (../data/sqlalchemy/)

All skills in toolchains/python/frameworks/ are related.
```

**✅ AFTER (Flat-Compatible)**
```markdown
## Related Skills

**Complementary Python Skills** (informational - no paths assumed):

- **pytest**: Testing framework and fixtures
- **asyncio**: Asynchronous programming patterns
- **sqlalchemy**: ORM and database patterns
- **pydantic**: Data validation and serialization
- **fastapi-local-dev**: Development server patterns

*Note: Skills are independently deployable. References are informational only.*
```

---

## Content Inlining Guidelines

### When to Inline vs. Reference

**Inline This** (20-50 lines typical):
- ✅ Essential code patterns users will need immediately
- ✅ Core concepts required to understand the skill
- ✅ Critical examples that demonstrate key principles
- ✅ Common use cases (80% of users need this)
- ✅ Setup/configuration boilerplate

**Reference This** (soft mentions only):
- 📖 Advanced patterns (20% of users need this)
- 📖 Comprehensive API documentation (see official docs)
- 📖 Alternative approaches (mention exists)
- 📖 Deep dives into related topics (optional reading)
- 📖 Full examples in other skills (note their existence)

### How Much Content to Inline

**Size Guidelines:**
- **Minimal pattern**: 5-15 lines (quick reference snippet)
- **Standard pattern**: 20-40 lines (complete working example)
- **Complex pattern**: 40-80 lines (realistic implementation)
- **Maximum inline**: 100 lines (absolute upper limit)

**Quality over Quantity:**
- One excellent 30-line example > five 5-line snippets
- Complete working code > partial fragments
- Real-world patterns > toy examples
- Commented code > bare implementations

### What Deserves Full Duplication

**Duplicate Without Hesitation:**
1. **Core patterns** - If 3+ skills need it, each should include it
2. **Setup boilerplate** - Common initialization code
3. **Configuration examples** - Working config files
4. **Error handling** - Standard patterns
5. **Best practices** - Critical do's and don'ts

**Example: Database Session Pattern**
```python
# This pattern appears in fastapi, sqlalchemy, pytest skills
# Each skill includes its own copy - THAT'S CORRECT!

@contextmanager
def get_db_session():
    """Database session context manager."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Progressive Disclosure Pattern

**Skill Structure for Content Organization:**

```
skill-name/
├── SKILL.md              # Main content (self-contained)
├── metadata.json         # Skill metadata
├── references/           # OPTIONAL: Progressive disclosure
│   ├── advanced.md       # Deep dive topics
│   ├── api-reference.md  # Comprehensive API docs
│   └── examples.md       # Extended examples
└── examples/             # OPTIONAL: Runnable code
    ├── basic/
    ├── intermediate/
    └── advanced/
```

**Rules for references/ Directory:**
- ✅ Use for progressive disclosure (optional deep dives)
- ✅ Keep references/ within single skill (no cross-skill paths)
- ✅ Main SKILL.md must be self-sufficient without references/
- ❌ No `../../other-skill/` paths in references/ files

---

## Soft Reference Format

### Recommended Pattern for Mentioning Other Skills

```markdown
## Complementary Skills

When using {this-skill}, consider these related skills (if deployed):

- **skill-name**: Brief description of how it complements this skill
  - *Use case*: When to combine these skills
  - *Integration*: How they work together (if applicable)
  - *Status*: Optional, independent enhancement

- **another-skill**: Brief description of complementary functionality
  - *Use case*: Specific scenario where both skills help
  - *Note*: Each skill works independently

**Note**: All skills are independently deployable. These references are informational only and do not indicate dependencies.
```

### Example: FastAPI Skill Mentioning Pytest

```markdown
## Complementary Skills

When building FastAPI applications, consider these skills (if deployed):

- **pytest**: Testing framework for API endpoints
  - *Use case*: Write comprehensive test suites for FastAPI routes
  - *Integration*: Use TestClient with pytest fixtures
  - *Status*: Optional - FastAPI works without testing skills

- **pydantic**: Data validation and serialization
  - *Use case*: Define request/response models with validation
  - *Integration*: FastAPI natively supports Pydantic models
  - *Status*: Recommended - enhances FastAPI development

- **sqlalchemy**: ORM for database operations
  - *Use case*: Add database persistence to FastAPI applications
  - *Integration*: Use dependency injection for database sessions
  - *Status*: Optional - for database-backed applications

**Note**: FastAPI skill is fully self-contained. Complementary skills enhance specific use cases but are not required.
```

### Graceful Degradation Notes

**Pattern for Optional Enhancements:**

```markdown
## Advanced Testing

**Basic testing patterns** (included in this skill):
```python
# Self-contained minimal test example
def test_basic():
    assert function() == expected
```

**Advanced fixtures** (if pytest skill deployed):
- Database fixtures with automatic rollback
- Mock fixtures for external services
- Parametrized test patterns

*Note: See pytest skill for comprehensive testing patterns.*
```

### Cross-Bundle References

**When skills might be deployed together in bundles:**

```markdown
## Bundle Context

This skill is part of the **FastAPI Development Bundle**.

**If deployed via bundle**, these skills work together:
- fastapi-local-dev
- pytest
- pydantic
- sqlalchemy

**If deployed standalone**, this skill is fully functional without other bundle members.

**Bundle deployment is optional** - skill works independently.
```

---

## Testing Checklist

### Pre-Submission Verification

Before submitting a new skill PR, verify:

#### 1. Flat Directory Test

```bash
# Test 1: Copy skill to isolated directory
mkdir -p /tmp/skill-test
cp -r your-skill-name /tmp/skill-test/
cd /tmp/skill-test/your-skill-name

# Test 2: Verify all content loads
cat SKILL.md  # Should display complete, useful content
cat metadata.json  # Should validate

# Test 3: Check for broken references
# All content should be accessible
# No "file not found" or missing sections
```

#### 2. No Relative Paths Verification

```bash
# Test 4: Grep for relative path violations
cd /Users/masa/Projects/claude-mpm-skills

# Check SKILL.md
grep -n "\.\\./" your-skill-name/SKILL.md
# Expected output: (empty)

# Check all files in skill
grep -r "\.\\./" your-skill-name/
# Expected output: (empty)

# Check for common violations
grep -r "../../" your-skill-name/
grep -r "../" your-skill-name/
grep -r "from skills\." your-skill-name/
# All expected output: (empty)
```

#### 3. Content Sufficiency Test

```bash
# Test 5: Verify essential content inlined
# Read SKILL.md - ask yourself:
# - Can user accomplish task with ONLY this skill?
# - Are critical patterns included (not just referenced)?
# - Do examples work without other skills?
# - Is setup/configuration complete?

# If answer is "NO" to any -> inline more content
```

#### 4. Reference Pattern Check

```bash
# Test 6: Check soft references are informational
grep -A 3 "Complementary Skills" your-skill-name/SKILL.md
grep -A 3 "Related Skills" your-skill-name/SKILL.md

# Verify:
# - References use skill names (not paths)
# - Descriptions explain relationship
# - No "required" or "must have" language
# - Graceful degradation notes present
```

#### 5. Progressive Disclosure Validation

```bash
# Test 7: Check references/ directory (if exists)
find your-skill-name/references/ -name "*.md" -exec grep -l "\\.\\./\\.\\." {} \;
# Expected output: (empty)

# Verify:
# - No cross-skill paths in references/
# - References stay within skill boundary
# - SKILL.md is self-sufficient without references/
```

#### 6. Metadata Validation

```bash
# Test 8: Validate metadata.json
cd your-skill-name
cat metadata.json | jq .

# Verify:
# - No "requires" field with other skills
# - "dependencies" only lists external packages
# - "tags" include "self-contained"
# - "bundles" listed (if applicable) but not required
```

### Complete Testing Checklist

Copy this checklist for your PR:

```markdown
## Self-Containment Testing Checklist

- [ ] **Flat directory test**: Skill works in isolated directory
- [ ] **Zero `../` paths**: `grep -r "\.\\./" skill-name/` returns empty
- [ ] **Essential content inlined**: Critical patterns included (not just referenced)
- [ ] **Complementary skills listed informationally**: Names only, no paths
- [ ] **Graceful degradation notes**: Optional enhancements clearly marked
- [ ] **Tested skill in isolation**: Verified functionality without other skills
- [ ] **Bundle membership documented**: Listed in metadata.json (if applicable)
- [ ] **No dependency assumptions**: Skill doesn't assume other skills present
- [ ] **Complete examples**: All code examples are self-contained
- [ ] **References/ validated**: No cross-skill paths (if references/ exists)

**Grep Verification Output:**
```bash
$ grep -r "\.\\./" skill-name/
(empty - no violations found)
```

**Isolation Test Result:**
- ✅ Copied to /tmp/skill-test/
- ✅ All content accessible
- ✅ No broken references
- ✅ Examples work independently
```

---

## Bundle vs. Skill Responsibilities

### Skill Responsibility: Self-Containment

**Each skill MUST:**
- ✅ Function completely standalone
- ✅ Include all essential patterns and examples
- ✅ Work in any deployment scenario (flat, bundled, selective)
- ✅ Provide graceful degradation for optional features
- ✅ Document complementary skills informationally (no paths)

**Each skill MUST NOT:**
- ❌ Depend on other skills being present
- ❌ Use relative paths to other skills
- ❌ Assume hierarchical directory structure
- ❌ Require bundle deployment to function

### Bundle Responsibility: Curation

**Bundles provide:**
- 📦 Curated collections of related skills
- 📦 Deployment topology recommendations
- 📦 Skill combination suggestions
- 📦 Ecosystem documentation
- 📦 Cross-skill integration guides

**Bundle file structure:**
```
.bundles/fastapi-dev-bundle/
├── bundle.json           # Bundle metadata
├── README.md             # Bundle overview
├── deployment-guide.md   # How to deploy bundle
└── integration-guide.md  # How skills work together
```

**Example bundle.json:**
```json
{
  "name": "fastapi-dev-bundle",
  "version": "1.0.0",
  "description": "Complete FastAPI development environment",
  "skills": [
    "fastapi-local-dev",
    "pytest",
    "pydantic",
    "sqlalchemy"
  ],
  "optional_skills": [
    "asyncio",
    "redis-patterns"
  ],
  "deployment": "recommended-together",
  "note": "All skills work independently - bundle deployment is optional"
}
```

### Clear Separation of Concerns

| Concern | Skill Responsibility | Bundle Responsibility |
|---------|---------------------|----------------------|
| **Functionality** | Complete, standalone | N/A (no functionality) |
| **Content** | Self-contained | Curation, organization |
| **Dependencies** | None (between skills) | Lists related skills |
| **Deployment** | Works anywhere | Recommends topology |
| **Integration** | Graceful degradation | Documents integration |
| **Testing** | Independent testing | Bundle-level validation |

### Why This Separation Matters

**User deploys single skill:**
```bash
claude-code skills add fastapi-local-dev
# Works immediately - no dependencies
```

**User deploys bundle:**
```bash
claude-code bundles add fastapi-dev-bundle
# Deploys: fastapi-local-dev, pytest, pydantic, sqlalchemy
# Each skill still works independently
# Bundle provides integration guidance
```

**User selectively deploys:**
```bash
claude-code skills add fastapi-local-dev pytest
# Partial bundle - works fine
# Skills adapt (graceful degradation)
```

---

## PR Checklist Template

### Copy-Paste Checklist for New Skill PRs

When submitting a new skill, include this checklist in your PR description:

```markdown
## New Skill Self-Containment Checklist

**Skill Name:** [your-skill-name]
**Category:** [framework/testing/debugging/etc]
**Toolchain:** [python/javascript/universal/etc]

### Self-Containment Verification

- [ ] **Flat directory deployment tested**
  - Copied skill to `/tmp/skill-test/`
  - Verified all content accessible
  - No broken references or missing files

- [ ] **Zero relative path violations**
  - Ran: `grep -r "\.\\./" skill-name/`
  - Output: (empty - no violations)
  - Verified manually: no `../` paths anywhere

- [ ] **Essential content inlined**
  - Critical patterns included in SKILL.md
  - Setup/configuration complete
  - Working examples provided
  - No "see other skill" for core functionality

- [ ] **Complementary skills listed informationally**
  - Used skill names only (no paths)
  - Described relationships clearly
  - Noted "if deployed" for optional enhancements
  - No "required" or "must install" language

- [ ] **Graceful degradation implemented**
  - Basic functionality self-contained
  - Advanced features note optional skills
  - Clear which features need other skills
  - Skill works independently

- [ ] **Tested in isolation**
  - Verified skill works alone
  - Examples run without other skills
  - Documentation makes sense standalone
  - No assumptions about other skills

- [ ] **Bundle membership documented**
  - Listed in metadata.json "bundles" field (if applicable)
  - Bundle deployment noted as optional
  - Skill works outside bundle

- [ ] **Metadata validation**
  - No other skills in "requires" field
  - "dependencies" only external packages
  - "tags" include "self-contained"
  - Version and author specified

### Grep Verification Output

```bash
$ grep -r "\.\\./" skill-name/
[paste output here - should be empty]

$ grep -r "from skills\." skill-name/
[paste output here - should be empty]
```

### Isolation Test Evidence

```bash
$ cp -r skill-name /tmp/skill-test/
$ cd /tmp/skill-test/skill-name
$ cat SKILL.md | head -50
[paste first 50 lines to show content is accessible]

✅ All content loads correctly
✅ No missing references
✅ Examples are complete
```

### Reviewer Notes

**For reviewers to verify:**
- [ ] Grep verification output is empty (no violations)
- [ ] SKILL.md is self-sufficient (read it standalone)
- [ ] Examples work without other skills
- [ ] Complementary skills are informational only
- [ ] No relative paths in references/ directory (if exists)
- [ ] Metadata.json doesn't list skill dependencies

**Common violations to watch for:**
- `../../other-skill/` paths
- "This skill requires X skill" language
- Missing essential content (just references)
- Incomplete examples
- Hierarchical directory assumptions

### Additional Context

[Add any context about design decisions, content inlining choices, or complementary skill relationships]
```

---

## Examples from Fixed Skills

### Overview of Fixed Skills

During the self-containment initiative (2025-11-30), **8 skills** were fixed to eliminate inter-skill dependencies:

1. **toolchains/python/validation/pydantic**
2. **toolchains/python/testing/pytest**
3. **toolchains/python/async/asyncio**
4. **toolchains/typescript/testing/jest**
5. **toolchains/typescript/testing/vitest**
6. **toolchains/typescript/testing/playwright**
7. **toolchains/rust/testing/rust-testing**
8. **toolchains/go/testing/go-testing**

### Example 1: Pydantic (Hard Paths → Inlined Content)

**BEFORE (Violation):**
```markdown
## Related Documentation
- FastAPI Integration: `../../frameworks/fastapi/`
- SQLAlchemy ORM: `../../data/sqlalchemy/`
- Django Framework: `../../frameworks/django/`
- Python Type Hints: `../types/`
- Testing with Pytest: `../testing/pytest/`
```

**AFTER (Self-Contained):**
```markdown
## Framework Integration Examples

### FastAPI Integration (Inlined Pattern)

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr

app = FastAPI()

@app.post("/users/")
def create_user(user: User):
    return user  # Auto-validated
```

### SQLAlchemy Integration (Inlined Pattern)

```python
from sqlalchemy.orm import Session
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user
```

## Complementary Skills

- **fastapi-local-dev**: Full FastAPI patterns (if deployed)
- **sqlalchemy**: Advanced ORM patterns (if deployed)
- **pytest**: Testing validation logic (if deployed)
```

**Key Changes:**
- ❌ Removed relative path links
- ✅ Inlined essential integration patterns
- ✅ Added soft references with "if deployed" notes
- ✅ Made skill self-sufficient

### Example 2: Pytest (Cross-Tree References → Flat-Compatible)

**BEFORE (Violation):**
```markdown
## Related Skills

- **[fastapi-local-dev](../../frameworks/fastapi-local-dev/SKILL.md)**: FastAPI development server patterns
- **[test-driven-development](../../../../universal/testing/test-driven-development/)**: TDD workflow and philosophy
- **[systematic-debugging](../../../../universal/debugging/systematic-debugging/)**: Debugging failing tests
```

**AFTER (Self-Contained):**
```markdown
## Testing Workflows

### TDD Pattern (Inlined from test-driven-development)

```python
# 1. Write failing test first
def test_user_creation():
    user = create_user("john", "john@example.com")
    assert user.username == "john"
    assert user.email == "john@example.com"

# 2. Implement minimal code to pass
def create_user(username, email):
    return User(username=username, email=email)

# 3. Refactor
def create_user(username: str, email: str) -> User:
    """Create user with validation."""
    if not username or not email:
        raise ValueError("Username and email required")
    return User(username=username, email=email)
```

### FastAPI Testing (Inlined Pattern)

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    response = client.post("/users/", json={
        "username": "john",
        "email": "john@example.com"
    })
    assert response.status_code == 200
```

## Complementary Skills

- **test-driven-development**: Full TDD workflow (if deployed)
- **fastapi-local-dev**: Advanced FastAPI patterns (if deployed)
- **systematic-debugging**: Debugging techniques (if deployed)
```

**Key Changes:**
- ❌ Removed cross-tree path references (../../../../universal/)
- ✅ Inlined essential TDD and FastAPI testing patterns
- ✅ Converted hard links to soft skill name references
- ✅ Added graceful degradation notes

### Example 3: TypeScript Jest (Complex Relative Paths → Inlined)

**BEFORE (Violation):**
```markdown
## Related Skills

- **[../../typescript-core](../../core/SKILL.md)**: Advanced TypeScript patterns and type safety
- **[../../../javascript/frameworks/react](../../../javascript/frameworks/react/SKILL.md)**: React component patterns and hooks
```

**AFTER (Self-Contained):**
```markdown
## TypeScript Testing Patterns (Self-Contained)

### Type-Safe Test Examples

```typescript
// Type-safe test setup
interface User {
  id: number;
  name: string;
  email: string;
}

describe('User operations', () => {
  it('creates user with correct types', () => {
    const user: User = {
      id: 1,
      name: 'John',
      email: 'john@example.com'
    };

    expect(user).toMatchObject({
      id: expect.any(Number),
      name: expect.any(String),
      email: expect.stringContaining('@')
    });
  });
});
```

### React Component Testing (Inlined Pattern)

```typescript
import { render, screen } from '@testing-library/react';

interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ onClick, children }) => (
  <button onClick={onClick}>{children}</button>
);

describe('Button', () => {
  it('renders and handles clicks', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    const button = screen.getByText('Click me');
    button.click();

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## Complementary Skills

- **typescript-core**: Advanced TypeScript patterns (if deployed)
- **react**: Full React component patterns (if deployed)
```

**Key Changes:**
- ❌ Removed complex multi-level relative paths
- ✅ Inlined TypeScript and React testing patterns
- ✅ Provided complete, working examples
- ✅ Made references informational only

### Common Transformation Patterns

**Pattern 1: Replace Paths with Names**
```markdown
❌ [skill-name](../../path/to/skill/SKILL.md)
✅ skill-name (if deployed)
```

**Pattern 2: Inline Essential Content**
```markdown
❌ For X pattern, see other-skill
✅ Essential X Pattern (inlined):
    [20-40 lines of actual pattern code]

    For advanced X patterns, see other-skill (if deployed)
```

**Pattern 3: Graceful Degradation**
```markdown
❌ This skill requires other-skill
✅ Basic functionality (self-contained):
    [working example]

    Advanced functionality (if other-skill deployed):
    [brief description of what's available]
```

---

## FAQ

### Q1: What if my skill legitimately needs another skill?

**A: Your skill doesn't "need" another skill - it needs the PATTERNS from that skill.**

**Solution:** Inline the essential patterns (20-50 lines).

**Example:**
```markdown
Don't say: "This skill requires pytest skill"

Instead:
## Testing (Self-Contained)

**Essential pytest fixture** (inlined):
```python
@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Advanced fixtures** (if pytest skill deployed):
- Parametrized fixtures
- Fixture factories
- Scope management

*See pytest skill for comprehensive patterns.*
```

**Rule:** If 90% of users need it, inline it. If 10% need it, reference it.

### Q2: Can I reference other skills for context?

**A: Yes - as informational mentions using skill names only (no paths).**

**DO:**
```markdown
## Complementary Skills

- **pytest**: Testing framework for writing unit tests
- **fastapi-local-dev**: Development server patterns
- **pydantic**: Data validation and serialization

*Note: These skills enhance this skill but are not required.*
```

**DON'T:**
```markdown
## Related Skills

- [pytest](../../testing/pytest/SKILL.md) - Required for testing
- See `../fastapi/` for server setup
- This skill depends on pydantic being installed
```

**Guidelines:**
- ✅ Use skill names (text only)
- ✅ Describe relationship/benefit
- ✅ Note "if deployed" or "optional"
- ❌ No file paths or links
- ❌ No "required" or "must have" language
- ❌ No dependency assumptions

### Q3: What about the references/ directory?

**A: Fine for progressive disclosure within a skill - but no cross-skill paths.**

**Allowed:**
```
skill-name/
├── SKILL.md              # Self-contained main content
└── references/
    ├── advanced.md       # ✅ Deep dive on this skill's topics
    ├── api-reference.md  # ✅ Comprehensive API for this skill
    └── examples.md       # ✅ Extended examples for this skill
```

**Not Allowed:**
```
skill-name/
└── references/
    ├── integration.md    # ❌ Contains: See ../../other-skill/
    └── related.md        # ❌ Contains: [other-skill](../../other/SKILL.md)
```

**Rules:**
- ✅ references/ stays within skill boundary
- ✅ All content in references/ is about THIS skill
- ✅ No `../` paths to other skills
- ✅ SKILL.md must be self-sufficient without references/
- ✅ references/ is for optional deep dives only

### Q4: How much content should I inline vs. reference?

**A: Inline the 80% use case - reference the 20% advanced cases.**

**Decision Framework:**

| Content Type | Action | Reasoning |
|-------------|--------|-----------|
| **Setup/Config** | Inline (20-30 lines) | Every user needs this |
| **Common patterns** | Inline (20-40 lines each) | 80% of users need this |
| **Basic examples** | Inline (30-50 lines) | First thing users try |
| **Error handling** | Inline (15-25 lines) | Critical for success |
| **Best practices** | Inline (10-20 bullets) | Prevents common mistakes |
| **Advanced patterns** | Reference | 20% of users, optional |
| **Full API docs** | Reference | Look up as needed |
| **Edge cases** | Reference | Uncommon scenarios |
| **Deep dives** | Reference | Optional learning |

**Example: Database Patterns**

**Inline (80% use case):**
```python
# Basic session management (everyone needs this)
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Basic CRUD (everyone does this)
def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**Reference (20% advanced use case):**
```markdown
**Advanced Database Patterns** (see sqlalchemy skill if deployed):
- Connection pooling configuration
- Advanced query optimization
- Relationship loading strategies
- Custom column types
```

### Q5: What if skills are designed to work together in a bundle?

**A: Bundle coordination is fine - skill dependencies are not.**

**Each skill must:**
- ✅ Work completely standalone
- ✅ Provide full basic functionality independently
- ✅ Gracefully degrade when other skills absent

**Bundle provides:**
- 📦 Curated deployment of related skills
- 📦 Integration documentation
- 📦 Cross-skill workflows
- 📦 Recommended combinations

**Example:**

**Skill: fastapi-local-dev (standalone)**
```markdown
# FastAPI Local Development

## Quick Start (Self-Contained)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Complementary Skills

When deployed with FastAPI Development Bundle:
- **pytest**: API endpoint testing
- **pydantic**: Request/response validation
- **sqlalchemy**: Database integration

*Each skill works independently. Bundle deployment is optional.*
```

**Bundle: fastapi-dev-bundle (coordination)**
```markdown
# FastAPI Development Bundle

## Skills Included
- fastapi-local-dev
- pytest
- pydantic
- sqlalchemy

## Integration Workflow

1. **Use fastapi-local-dev** for server setup
2. **Use pydantic** for model validation
3. **Use sqlalchemy** for database
4. **Use pytest** for testing

## Cross-Skill Examples

[Examples showing skills working together]

*Note: All skills work independently. This bundle demonstrates recommended integration.*
```

### Q6: How do I test that my skill is truly self-contained?

**A: Use the isolation test protocol.**

**Step-by-Step Verification:**

```bash
# 1. Create isolated test environment
mkdir -p /tmp/skill-isolation-test
cd /tmp/skill-isolation-test

# 2. Copy ONLY your skill (no siblings, no parents)
cp -r /path/to/your-skill-name .

# 3. Verify structure
ls -la your-skill-name/
# Should show: SKILL.md, metadata.json, references/ (optional)

# 4. Read the skill
cat your-skill-name/SKILL.md

# 5. Ask these questions:
# ✅ Can I understand the skill completely from SKILL.md?
# ✅ Are all examples complete and runnable?
# ✅ Is setup/configuration included?
# ✅ Do code snippets work without external references?
# ✅ Are complementary skills mentioned (not required)?

# 6. Grep for violations
grep -r "\.\\./" your-skill-name/
# Expected: (empty)

grep -r "from skills\." your-skill-name/
# Expected: (empty)

grep -i "requires.*skill" your-skill-name/SKILL.md
# Expected: (empty or graceful degradation only)

# 7. Metadata check
cat your-skill-name/metadata.json | jq '.requires // empty'
# Expected: (empty or external packages only)
```

**Pass Criteria:**
- ✅ All grep checks return empty (no violations)
- ✅ SKILL.md is complete and understandable standalone
- ✅ Examples work without other files
- ✅ No "missing content" feeling
- ✅ Complementary skills noted but not required

**Fail Criteria:**
- ❌ Any `../` paths found
- ❌ "See other-skill for X" without inlining X
- ❌ Incomplete examples
- ❌ Missing setup/configuration
- ❌ "Requires other-skill" language

### Q7: What about shared patterns across many skills?

**A: Duplicate them - self-containment > DRY principle.**

**In traditional code:** Don't Repeat Yourself (DRY) is critical
**In skills:** Self-Containment > DRY

**Why duplication is correct:**
- Skills are documentation, not code
- Each skill must stand alone
- Users may have only one skill deployed
- Maintenance cost is low (docs, not runtime)
- Discovery/deployment flexibility > code efficiency

**Example: Database Session Pattern**

This pattern appears in **5+ skills**:
- fastapi-local-dev
- sqlalchemy
- pytest
- django
- flask

**Each skill includes it** - that's correct!

```python
# This pattern is in ALL database-related skills
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Why this is good:**
- ✅ User with only fastapi skill has complete pattern
- ✅ User with only pytest skill has complete pattern
- ✅ Each skill is self-sufficient
- ✅ No coordination needed between skills
- ✅ Flexible deployment (any combination works)

**When patterns change:**
- Update all skills with the pattern
- Skills remain independent
- No cascading breakage

### Q8: Can I create a "shared" or "common" skill that other skills reference?

**A: No - this violates self-containment.**

**Don't create:**
```
toolchains/python/shared/
├── SKILL.md          # Common patterns
└── patterns/
    ├── database.py
    └── testing.py

toolchains/python/frameworks/fastapi/
└── SKILL.md          # References: ../../shared/patterns/database.py
```

**Instead:**
```
toolchains/python/frameworks/fastapi/
└── SKILL.md          # Includes database patterns inline

toolchains/python/testing/pytest/
└── SKILL.md          # Includes database patterns inline (duplicate is OK)
```

**Why "shared" skills break self-containment:**
- Creates dependency (other skills need "shared" skill)
- Breaks flat deployment (relative path assumptions)
- Reduces flexibility (can't deploy skills individually)
- Complicates maintenance (changing "shared" affects many skills)

**Alternative: Pattern Documentation**

If patterns are truly universal, create:
- **Official docs** (not a skill): `docs/patterns/database.md`
- **Bundle guide**: `.bundles/python-dev/integration-patterns.md`
- **Inline in each skill**: Copy essential pattern to each skill

**Skills stay independent, patterns stay accessible.**

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-30 | Initial release - comprehensive self-containment standard |

---

## See Also

- **[SKILL_CREATION_PR_CHECKLIST.md](SKILL_CREATION_PR_CHECKLIST.md)**: Copy-paste checklist for PRs
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: General contribution guidelines
- **[examples/good-self-contained-skill/](../examples/good-self-contained-skill/)**: Template following all rules
- **[examples/bad-interdependent-skill/](../examples/bad-interdependent-skill/)**: Anti-pattern examples

---

**Questions or clarifications?** Open an issue or contact maintainers.

**Remember**: Self-containment enables flexible deployment. When in doubt, inline more content.
