# Voice Consistency & Example Format Guide

Comprehensive guide for maintaining imperative voice and consistent example formatting across all skills.

## Table of Contents

- [Voice Consistency Standards](#voice-consistency-standards)
- [Example Format Standards](#example-format-standards)
- [Automated Checking](#automated-checking)
- [Common Violations & Fixes](#common-violations--fixes)
- [CI/CD Integration](#cicd-integration)

---

## Voice Consistency Standards

All skills MUST use imperative voice throughout. This means:

### ✅ Correct: Imperative Voice

**Pattern**: Direct commands starting with verbs

```markdown
Use mypy for static type checking.
Install dependencies with pip install mypy.
Configure strict mode in mypy.ini.
Apply type hints to all public APIs.
```

**Why**: Imperative voice is clear, direct, and actionable. It tells Claude exactly what to do.

### ❌ Incorrect: Second-Person Voice

**Pattern**: Using "you", "your", "you should", "you can"

```markdown
You should use mypy for type checking.
You can install it with pip.
You need to configure mypy.ini.
Your code should have type hints.
```

**Why**: Second-person voice is conversational but less direct. It distances the instruction from the action.

---

## Imperative Voice Patterns

### 1. Direct Commands

✅ **Correct:**
```markdown
Create a new file.
Run the test suite.
Update the configuration.
Delete the old version.
```

❌ **Wrong:**
```markdown
You should create a new file.
You can run the test suite.
You need to update the configuration.
You'll want to delete the old version.
```

### 2. Conditional Actions

✅ **Correct:**
```markdown
When tests fail, check error messages.
If validation fails, review input data.
For large datasets, use streaming.
```

❌ **Wrong:**
```markdown
When you see test failures, you should check errors.
If you encounter validation failures, you need to review data.
When you have large datasets, you can use streaming.
```

### 3. Capabilities and Options

✅ **Correct:**
```markdown
To optimize performance, enable caching.
For better debugging, increase log verbosity.
Async operations improve throughput.
```

❌ **Wrong:**
```markdown
You can optimize performance by enabling caching.
You should increase log verbosity for debugging.
If you want better throughput, you can use async.
```

### 4. Requirements and Constraints

✅ **Correct:**
```markdown
Required: Python 3.11+
Must install dependencies before running.
Always validate user input.
```

❌ **Wrong:**
```markdown
You must have Python 3.11+.
You need to install dependencies first.
You should always validate user input.
```

---

## Example Format Standards

All code examples MUST follow the ✅/❌ pattern to show correct and incorrect usage.

### Pattern Structure

```markdown
### Feature Name

✅ **Correct:** Brief explanation
```language
// Correct implementation
```

❌ **Wrong:** Brief explanation
```language
// Incorrect implementation
```
```

### Complete Example

```markdown
### Type Annotations

✅ **Correct: Explicit return type**
```python
def get_user(user_id: int) -> Optional[User]:
    return db.query(User).get(user_id)
```

❌ **Wrong: Missing return type**
```python
def get_user(user_id: int):
    return db.query(User).get(user_id)
```
```

### Requirements

1. **Pair Examples**: Always provide both ✅ correct and ❌ incorrect examples
2. **Code Blocks**: Every ✅/❌ label must be followed by a code block
3. **Explanations**: Include brief context (e.g., "**Correct: Explicit return type**")
4. **Balance**: Aim for equal numbers of ✅ and ❌ examples

---

## Common Violations & Fixes

### Second-Person Voice

| ❌ Violation | ✅ Fix |
|-------------|-------|
| "You should use X" | "Use X" |
| "You can do Y" | "To do Y, [verb]" or "Y enables Z" |
| "You need to configure" | "Configure" or "Required: configure" |
| "You must install" | "Install" or "Must install" |
| "You'll want to" | "To accomplish X, [verb]" |
| "Your code should" | "Code must" or "[Verb] the code" |
| "If you encounter" | "When X occurs" or "If X happens" |

### Passive Voice

| ❌ Violation | ✅ Fix |
|-------------|-------|
| "Tests are run by pytest" | "pytest runs tests" |
| "Data is validated" | "Validate data" or "X validates data" |
| "Files are processed" | "Process files" or "X processes files" |

### Non-Imperative Mood

| ❌ Violation | ✅ Fix |
|-------------|-------|
| "Should implement X" | "Implement X" |
| "Could use Y" | "Use Y for Z" or "Y enables Z" |
| "Might want to" | "To accomplish X, [verb]" |
| "Consider adding" | "Add X" or "X improves Y" |

### Conversational Tone

| ❌ Violation | ✅ Fix |
|-------------|-------|
| "Let's create X" | "Create X" |
| "We can use Y" | "Use Y" or "Y enables Z" |
| "We should do Z" | "Do Z" |
| "I recommend X" | "Recommended: X" or "Use X for Y" |

---

## Automated Checking

### Running the Checker

```bash
# Check all skills
python scripts/check_voice_consistency.py

# Check specific directory
python scripts/check_voice_consistency.py --path universal/

# Check single file
python scripts/check_voice_consistency.py --path path/to/SKILL.md

# Verbose output with line context
python scripts/check_voice_consistency.py --verbose

# Generate markdown report
python scripts/check_voice_consistency.py --report quality-report.md

# JSON output for CI/CD
python scripts/check_voice_consistency.py --format json > report.json

# CI mode (strict, exit 1 on errors)
python scripts/check_voice_consistency.py --ci
```

### Violation Severity Levels

- **🔴 ERROR** (Critical, blocks CI):
  - Second-person voice ("you should", "you can", etc.)
  - Test-only methods in production code
  - Critical format violations

- **🟡 WARNING** (Should fix):
  - Passive voice patterns
  - Non-imperative mood
  - Missing code blocks after ✅/❌
  - Missing anti-pattern documentation

- **🔵 INFO** (Suggestions):
  - Conversational tone
  - Imbalanced examples (only ✅ or only ❌)
  - Style improvements

### Understanding Reports

**Summary Output:**
```
================================================================================
VOICE CONSISTENCY & EXAMPLE FORMAT REPORT
================================================================================
Files checked: 89
Files with violations: 12

Violations by severity:
  Errors:      8  (critical, blocks CI)
  Warnings:   24  (should fix)
  Info:       15  (suggestions)
  Total:      47

Quality metrics:
  Files with ✅/❌ examples: 67/89
  Files with anti-patterns:  72/89
================================================================================
```

**Detailed Output:**
```
📄 toolchains/python/tooling/mypy/SKILL.md
   3 errors, 5 warnings, 2 info
--------------------------------------------------------------------------------

  Second Person Voice (3):
    🔴 Line 42: Second-person voice detected (use imperative)
       Matched: "you should"
       Fix: Replace with imperative: 'Use X' or 'Apply Y'

  Passive Voice (5):
    🟡 Line 108: Passive voice detected
       Matched: "is validated"
       Fix: Consider active voice: 'X validates Y'
```

---

## CI/CD Integration

### GitHub Actions Workflow

The `.github/workflows/skill-quality.yml` workflow runs automatically on:
- Pull requests that modify `.md` files
- Pushes to `main` branch

**Features:**
- Runs quality checks on all skills
- Posts PR comments with violation summary
- Blocks merge if critical errors found
- Uploads detailed reports as artifacts

### Pre-Commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: skill-quality
        name: Skill Quality Checks
        entry: python scripts/check_voice_consistency.py --ci
        language: python
        pass_filenames: false
        files: '\.md$'
```

### Make Integration

Add to `Makefile`:

```makefile
.PHONY: check-quality
check-quality:
	python scripts/check_voice_consistency.py

.PHONY: check-quality-ci
check-quality-ci:
	python scripts/check_voice_consistency.py --ci

.PHONY: quality-report
quality-report:
	python scripts/check_voice_consistency.py --report quality-report.md
	@echo "Report saved to quality-report.md"
```

---

## Best Practices

### 1. Write in Imperative Voice from the Start

✅ **Do this:**
- Think "Give Claude a command"
- Start sentences with verbs
- Be direct and actionable

❌ **Don't do this:**
- Write conversationally first, then fix
- Use second-person pronouns
- Defer to user's discretion

### 2. Always Pair ✅ Correct with ❌ Wrong

**Why**: Showing what NOT to do is as important as showing what to do.

✅ **Good section:**
```markdown
### Type Safety

✅ **Correct: Explicit types**
```python
def process(data: dict[str, Any]) -> list[str]:
    return list(data.keys())
```

❌ **Wrong: Missing types**
```python
def process(data):
    return list(data.keys())
```
```

❌ **Incomplete section:**
```markdown
### Type Safety

✅ **Correct: Explicit types**
```python
def process(data: dict[str, Any]) -> list[str]:
    return list(data.keys())
```

<!-- Missing ❌ anti-pattern! -->
```

### 3. Use Context-Appropriate Exceptions

Some contexts allow second-person voice:
- Inside code comments (examples showing user code)
- Inside quoted text or documentation excerpts
- Inside tables comparing options
- YAML frontmatter metadata

**Example (allowed):**
```python
# ✅ Inside code comment (showing user code)
def validate_user(user_id: int) -> bool:
    """
    Validate user exists.

    Example:
        # You can call this with any user ID
        is_valid = validate_user(123)
    """
```

### 4. Document Anti-Patterns

Every skill should have:
- At least one ❌ example showing what NOT to do
- Anti-pattern section explaining common mistakes
- Clear rationale for why anti-pattern is wrong

### 5. Run Checks Before Committing

```bash
# Quick check
python scripts/check_voice_consistency.py --path path/to/changed/SKILL.md

# Full check with report
python scripts/check_voice_consistency.py --verbose
```

---

## Troubleshooting

### False Positives

**Q: Checker flags valid second-person usage in code examples?**

A: Code examples inside triple backticks (```) are automatically excluded. If still flagged:
- Ensure code block has proper opening/closing ```
- Check if line is actually outside code block
- Use inline code backticks for single-word references

**Q: Passive voice is sometimes clearer?**

A: Passive voice warnings are ⚠️ WARNING level, not 🔴 ERROR. Use judgment:
- If active voice is awkward, keep passive (warning is acceptable)
- If easily rewritable, prefer active voice
- Document why passive is better in comment if needed

### Common Pitfalls

**Pitfall 1: Forgetting to update after editing**

✅ **Solution:** Run checker in watch mode during editing:
```bash
# Install entr for file watching
brew install entr

# Watch and re-check on save
find . -name "SKILL.md" | entr python scripts/check_voice_consistency.py --path /_
```

**Pitfall 2: Bulk "you" replacements breaking meaning**

❌ **Wrong bulk fix:**
```markdown
Original: "You can use async for I/O-bound operations"
Bad fix:  "Can use async for I/O-bound operations"  # Missing verb!
```

✅ **Correct fix:**
```markdown
"Use async for I/O-bound operations"
```

**Pitfall 3: Removing all ❌ examples to "pass" checks**

Never remove anti-patterns to avoid imbalanced warnings! Skills need both:
- ✅ Show correct usage
- ❌ Show common mistakes

---

## Examples from Real Skills

### Example 1: mypy Skill (Good)

✅ **Imperative voice throughout:**
```markdown
## Type Annotation Basics

Add type hints to variables, functions, and classes for static type checking.

### Variable Type Hints

```python
# Basic types
name: str = "Alice"
age: int = 30
```

Infer types automatically when possible. mypy infers types from assignments.
```

### Example 2: Testing Anti-Patterns (Excellent)

✅ **Consistent ✅/❌ patterns:**
```markdown
### Anti-Pattern 1: Testing Mock Behavior

❌ **WRONG**:
```python
mock_api = Mock()
assert mock_api.testId == "user-mock"  # Testing the mock!
```

✅ **CORRECT**:
```python
real_api = UserAPI()
assert real_api.get_user(123).name == "Alice"  # Testing real behavior
```
```

---

## Summary Checklist

Before submitting a skill, verify:

- [ ] No second-person pronouns outside code/quotes
- [ ] All ✅ examples have corresponding ❌ anti-patterns
- [ ] All ❌ examples have corresponding ✅ correct patterns
- [ ] Code blocks follow all ✅/❌ labels
- [ ] Imperative voice used throughout prose
- [ ] Anti-patterns documented (for skills >100 lines)
- [ ] Ran `python scripts/check_voice_consistency.py` locally
- [ ] Fixed all 🔴 ERROR violations
- [ ] Addressed 🟡 WARNING violations (or documented why not)

---

## Resources

- **Checker Script**: `scripts/check_voice_consistency.py`
- **CI Workflow**: `.github/workflows/skill-quality.yml`
- **Example Skills**:
  - `toolchains/python/tooling/mypy/SKILL.md` (imperative voice)
  - `universal/testing/testing-anti-patterns/SKILL.md` (excellent ✅/❌ patterns)
  - `universal/main/skill-creator/SKILL.md` (progressive disclosure example)

**Remember**: Imperative voice + ✅/❌ examples = Clear, actionable skills that Claude can execute confidently.
