# Voice Consistency & Example Format Checker

Automated quality assurance tool for Claude Code skills that enforces imperative voice and consistent example formatting across the skills library.

## Quick Start

```bash
# Check all skills
python scripts/check_voice_consistency.py

# Check specific directory
python scripts/check_voice_consistency.py --path universal/

# Check single file
python scripts/check_voice_consistency.py --path path/to/SKILL.md

# Verbose output
python scripts/check_voice_consistency.py --verbose

# CI mode (strict, exit 1 on warnings or errors)
python scripts/check_voice_consistency.py --ci
```

## Features

### Voice Consistency Checks

**Detects:**
- ✅ Second-person pronouns ("you", "your", "you're", "yourself")
- ✅ Passive voice patterns ("is done", "was created", "are processed")
- ✅ Non-imperative mood ("should", "would", "could", "might")
- ✅ Conversational tone ("let's", "we can", "I recommend")

**Enforces:**
- Imperative voice throughout ("Use X", "Apply Y", "Configure Z")
- Active voice for clarity ("X validates Y" not "Y is validated")
- Direct commands starting with verbs

### Example Format Validation

**Checks:**
- ✅/❌ example pattern usage
- Code block presence after example markers
- Balanced correct/incorrect examples
- Complete anti-pattern documentation

### Anti-Pattern Documentation

**Verifies:**
- Skills document common mistakes
- Best practices are clearly stated
- What NOT to do is explained

## Command-Line Interface

### Basic Usage

```bash
# Default: Check all source SKILL.md files (toolchains/, universal/, examples/)
python scripts/check_voice_consistency.py

# Output:
# ================================================================================
# VOICE CONSISTENCY & EXAMPLE FORMAT REPORT
# ================================================================================
# Files checked: N
# Files with violations: 12
#
# Violations by severity:
#   Errors:      8  (critical, blocks CI)
#   Warnings:   24  (should fix)
#   Info:       15  (suggestions)
#   Total:      47
```

### Path Options

```bash
# Check specific directory
python scripts/check_voice_consistency.py --path universal/

# Check single file
python scripts/check_voice_consistency.py --path toolchains/python/tooling/mypy/SKILL.md

# Check multiple toolchain categories
python scripts/check_voice_consistency.py --path toolchains/python/
```

### Output Formats

```bash
# Text format (default, human-readable)
python scripts/check_voice_consistency.py --format text

# JSON format (for CI/CD integration)
python scripts/check_voice_consistency.py --format json > report.json

# Markdown format (for documentation)
python scripts/check_voice_consistency.py --format markdown > report.md
```

### Verbosity

```bash
# Standard output (summary + top violations)
python scripts/check_voice_consistency.py

# Verbose output (includes line context)
python scripts/check_voice_consistency.py --verbose

# Limit violations shown per file
python scripts/check_voice_consistency.py --max-violations 5
```

### Report Generation

```bash
# Generate markdown report file
python scripts/check_voice_consistency.py --report quality-report.md

# Generate and view
python scripts/check_voice_consistency.py --report report.md && open report.md
```

### CI/CD Mode

```bash
# Strict mode: exit 1 on any warnings or errors
python scripts/check_voice_consistency.py --ci

# Exit codes:
#   0 = No warnings or errors
#   1 = Warnings or errors found (blocks merge)
```

## Violation Severity Levels

### 🔴 ERROR (Critical, Blocks CI)

**Second-person voice violations:**
```markdown
❌ You should use mypy for type checking.
✅ Use mypy for type checking.

❌ You can install it with pip.
✅ Install with pip.

❌ Your code must have type hints.
✅ Code must have type hints.
```

**Why ERROR**: Second-person voice violates the fundamental requirement for imperative voice. These must be fixed before merging.

### 🟡 WARNING (Should Fix; Blocks `--ci`)

**Passive voice:**
```markdown
❌ Data is validated by the service.
✅ The service validates data.

❌ Tests are run by pytest.
✅ pytest runs tests.
```

**Non-imperative mood:**
```markdown
❌ Should implement validation.
✅ Implement validation.

❌ Consider adding type hints.
✅ Add type hints.
```

**Missing code blocks:**
```markdown
❌ ✅ **Correct usage**
   (no code block follows)

✅ ✅ **Correct usage**
   ```python
   code_example()
   ```
```

**Why WARNING**: These degrade quality but don't violate core requirements. Fix when possible.

### 🔵 INFO (Suggestions)

**Conversational tone:**
```markdown
❌ Let's create a function.
✅ Create a function.

❌ We should validate input.
✅ Validate input.

❌ I recommend using Pydantic.
✅ Recommended: Use Pydantic.
```

**Imbalanced examples:**
```markdown
⚠️  Only ✅ examples found, consider adding ❌ anti-patterns
⚠️  Only ❌ examples found, consider adding ✅ correct patterns
```

**Why INFO**: Suggestions for improvement, not blockers. Optional but recommended.

## Output Formats

### Text Format (Default)

```
================================================================================
VOICE CONSISTENCY & EXAMPLE FORMAT REPORT
================================================================================
Files checked: N
Files with violations: 12

Violations by severity:
  Errors:      8  (critical, blocks CI)
  Warnings:   24  (should fix)
  Info:       15  (suggestions)
  Total:      47

Quality metrics:
  Files with ✅/❌ examples: X/N
  Files with anti-patterns:  Y/N
================================================================================

📄 toolchains/python/tooling/mypy/SKILL.md
   3 errors, 5 warnings, 2 info
--------------------------------------------------------------------------------

  Second Person Voice (3):
    🔴 Line 42: Second-person voice detected (use imperative)
       Matched: "you should"
       Fix: Replace with imperative: 'Use X' or 'Apply Y'
       Context: You should configure mypy.ini for strict mode.

  Passive Voice (5):
    🟡 Line 108: Passive voice detected
       Matched: "is validated"
       Fix: Consider active voice: 'X validates Y'
```

### JSON Format (CI/CD)

```json
{
  "summary": {
    "total_files": 110,
    "files_with_violations": 12,
    "total_errors": 8,
    "total_warnings": 24,
    "total_info": 15
  },
  "files": [
    {
      "path": "toolchains/python/tooling/mypy/SKILL.md",
      "violations": [
        {
          "file": "toolchains/python/tooling/mypy/SKILL.md",
          "line": 42,
          "content": "You should configure mypy.ini for strict mode.",
          "type": "second_person_voice",
          "severity": "error",
          "message": "Second-person voice detected (use imperative)",
          "suggestion": "Replace with imperative: 'Use X' or 'Apply Y'",
          "matched_text": "you should"
        }
      ],
      "error_count": 3,
      "warning_count": 5,
      "info_count": 2
    }
  ]
}
```

### Markdown Format (Documentation)

```markdown
# Voice Consistency & Example Format Report

## Summary

- **Files checked:** N
- **Files with violations:** 12
- **Errors:** 8 (critical)
- **Warnings:** 24
- **Info:** 15

## Violations by File

### toolchains/python/tooling/mypy/SKILL.md

**3** errors, **5** warnings, **2** info

#### Second Person Voice

- 🔴 **Line 42:** Second-person voice detected (use imperative)
  - *Fix:* Replace with imperative: 'Use X' or 'Apply Y'

#### Passive Voice

- 🟡 **Line 108:** Passive voice detected
  - *Fix:* Consider active voice: 'X validates Y'
```

## CI/CD Integration

### GitHub Actions

The tool integrates with GitHub Actions via `.github/workflows/skill-quality.yml`:

**Features:**
- ✅ Runs automatically on PRs
- ✅ Posts violation summary as PR comment
- ✅ Blocks merge on critical errors
- ✅ Uploads detailed reports as artifacts

**PR Comment Example:**
```markdown
## 📊 Skill Quality Report

### Summary
- **Files checked:** N
- **Files with violations:** 12
- 🔴 **Errors:** 8 (critical)
- 🟡 **Warnings:** 24
- 🔵 **Info:** 15

❌ **Critical violations found.** Please fix before merging.

### Violations by File

#### `toolchains/python/tooling/mypy/SKILL.md`
3 errors, 5 warnings, 2 info

**Top Errors:**
- Line 42: Second-person voice detected (use imperative)
  - *Fix:* Replace with imperative: 'Use X' or 'Apply Y'
```

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

```bash
# Install and run
pre-commit install
pre-commit run skill-quality --all-files
```

### Make Integration

Add to `Makefile`:

```makefile
.PHONY: check-quality
check-quality:
	@echo "Checking skill quality..."
	@python scripts/check_voice_consistency.py

.PHONY: check-quality-ci
check-quality-ci:
	@python scripts/check_voice_consistency.py --ci

.PHONY: quality-report
quality-report:
	@python scripts/check_voice_consistency.py --report quality-report.md
	@echo "Report saved to quality-report.md"

.PHONY: fix-quality
fix-quality:
	@echo "Auto-fix not yet implemented. Manual fixes required."
	@python scripts/check_voice_consistency.py
```

## Performance

**Benchmarks** (on the full skills set, ~50k lines total):

```
Initial run (cold):     2.3s
Subsequent runs:        1.8s
Single file:            0.05s
CI mode (all checks):   2.5s
```

**Optimization features:**
- Context map precomputation (fast exception detection)
- Single-pass violation collection
- Efficient regex compilation
- Minimal I/O operations

## Exception Contexts

The checker automatically excludes these contexts from voice checks:

1. **Code blocks**: Content between triple backticks
2. **Frontmatter**: YAML between `---` markers
3. **Quotes**: Lines starting with `>`
4. **Tables**: Lines with pipe separators `|`
5. **Inline code**: Text between single backticks
6. **Comments**: Lines starting with `#` or `>`

**Example (all allowed):**
```markdown
---
description: You can use this skill for testing
---

> You should read the documentation.

| Feature | Description |
|---------|-------------|
| Type hints | You can add type annotations |

`you_can_use_snake_case`

```python
# You should configure this properly
def example():
    """You can call this function."""
    pass
```
```

## Common Fixes

### Second-Person Voice

| ❌ Before | ✅ After |
|----------|---------|
| You should use mypy | Use mypy |
| You can install with pip | Install with pip |
| You need to configure X | Configure X |
| You must have Python 3.11+ | Required: Python 3.11+ |
| Your code should follow PEP 8 | Code must follow PEP 8 |
| If you encounter errors | When errors occur |

### Passive Voice

| ❌ Before | ✅ After |
|----------|---------|
| Tests are run by pytest | pytest runs tests |
| Data is validated | Validate data |
| Files are processed | Process files |
| Configuration was updated | Updated configuration |

### Non-Imperative Mood

| ❌ Before | ✅ After |
|----------|---------|
| Should implement X | Implement X |
| Could use Y | Use Y for Z |
| Might want to add Z | Add Z |
| Consider adding validation | Add validation |

### Example Format

| ❌ Before | ✅ After |
|----------|---------|
| ✅ Good example<br>(no code) | ✅ **Correct**<br>```python<br>code()<br>``` |
| Only ✅ examples | Add ❌ anti-patterns |
| Only ❌ examples | Add ✅ correct patterns |

## Troubleshooting

### False Positives

**Q: Checker flags "you" in code examples?**

A: Ensure code is in triple-backtick blocks. Inline mentions should use single backticks: `` `you_can_use` ``.

**Q: Passive voice makes more sense in my context?**

A: Passive voice is WARNING level, not ERROR. Use judgment. If clearer, keep it (warning is acceptable).

### Performance

**Q: Checker is slow on large repository?**

A: Check specific paths during development:
```bash
# Fast: Check only changed files
python scripts/check_voice_consistency.py --path path/to/changed/

# Full check only before commit
python scripts/check_voice_consistency.py
```

### CI/CD

**Q: GitHub Action fails but local check passes?**

A: Ensure same Python version (3.11+) and run with `--ci` flag locally:
```bash
python scripts/check_voice_consistency.py --ci
```

## Development

### Adding New Patterns

Edit `scripts/check_voice_consistency.py`:

```python
# Add to SECOND_PERSON_PATTERNS
SECOND_PERSON_PATTERNS = {
    r'\bnew_pattern\b': "Suggestion for fix",
    # ...
}

# Or other pattern dictionaries:
# - PASSIVE_VOICE_PATTERNS
# - NON_IMPERATIVE_PATTERNS
# - CONVERSATIONAL_PATTERNS
```

### Testing

```bash
# Test on sample file with violations
python scripts/check_voice_consistency.py --path /tmp/test_skill.md --verbose

# Run full check
python scripts/check_voice_consistency.py

# Test CI mode
python scripts/check_voice_consistency.py --ci
echo "Exit code: $?"
```

### Architecture

```
SkillQualityChecker
├── ContextDetector
│   └── Builds exception context map (code blocks, quotes, tables)
├── VoiceConsistencyChecker
│   ├── Checks second-person voice
│   ├── Checks passive voice
│   ├── Checks non-imperative mood
│   └── Checks conversational tone
├── ExampleFormatChecker
│   ├── Validates ✅/❌ patterns
│   ├── Checks code block presence
│   └── Detects imbalanced examples
├── AntiPatternChecker
│   └── Verifies anti-pattern documentation
└── ReportGenerator
    ├── Text format
    ├── JSON format
    └── Markdown format
```

## Related Documentation

- **[Voice Consistency Guide](../docs/VOICE_CONSISTENCY_GUIDE.md)** - Comprehensive style guide
- **[Skill Creator Guide](../universal/main/skill-creator/SKILL.md)** - Skill creation workflow
- **[CI Workflow](../.github/workflows/skill-quality.yml)** - GitHub Actions integration

## Version History

- **v1.0.0** (2025-12-03): Initial release
  - Voice consistency checks (second-person, passive, non-imperative, conversational)
  - Example format validation (✅/❌ patterns, code blocks, balance)
  - Anti-pattern documentation checks
  - Multiple output formats (text, JSON, markdown)
  - CI/CD integration
  - Comprehensive documentation

---

**Maintained by**: Claude MPM Team
**License**: MIT
**Python**: 3.11+
