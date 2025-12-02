# Troubleshooting Claude Code Skills

**Version:** 1.0.0
**Last Updated:** 2025-12-02
**Purpose:** Diagnose and resolve common skill-related issues

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [How to Use This Guide](#how-to-use-this-guide)
3. [Discovery Issues](#discovery-issues)
4. [Loading Issues](#loading-issues)
5. [Expansion Issues](#expansion-issues)
6. [Content Issues](#content-issues)
7. [Performance Issues](#performance-issues)
8. [Self-Containment Issues](#self-containment-issues)
9. [Common Error Messages](#common-error-messages)
10. [Diagnostic Tools](#diagnostic-tools)
11. [Getting Help](#getting-help)

---

## Quick Reference

### Common Issues at a Glance

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Skill not in catalog | Invalid metadata.json | Validate JSON syntax |
| Skill won't expand | Malformed YAML frontmatter | Check YAML syntax |
| "File not found" | Relative path broken in flat deployment | Use skill names, not paths |
| Context window exceeded | Too many skills deployed | Deploy selectively |
| Slow responses | Large skill files | Check token counts |
| Broken references | Self-containment violation | Inline essential content |
| Missing content | Incomplete inlining | Add patterns to SKILL.md |

### Emergency Diagnostic Commands

```bash
# Check if skill file exists and is readable
ls -lh /path/to/your-skill/SKILL.md

# Validate metadata.json syntax
cat your-skill/metadata.json | jq .

# Check for relative path violations
grep -r "\.\\./" your-skill/

# Verify YAML frontmatter
head -20 your-skill/SKILL.md

# Test skill in isolation
cp -r your-skill /tmp/skill-test/ && cd /tmp/skill-test/your-skill
```

---

## How to Use This Guide

### Step-by-Step Approach

1. **Identify Your Symptom**: Match your issue to a category below
2. **Run Diagnostic Commands**: Use provided commands to gather information
3. **Apply Solutions**: Follow step-by-step fixes
4. **Verify Resolution**: Test that the issue is resolved
5. **Report if Unresolved**: See [Getting Help](#getting-help)

### Before You Start

- **Collect Information**: Error messages, file paths, recent changes
- **Check Documentation**: [SKILL_SELF_CONTAINMENT_STANDARD.md](SKILL_SELF_CONTAINMENT_STANDARD.md)
- **Review Examples**: [examples/good-self-contained-skill/](../examples/good-self-contained-skill/)
- **Try Isolation Test**: Test skill in empty directory first

### When to Escalate

File a GitHub issue if:
- Problem persists after following this guide
- You suspect a Claude Code bug
- Multiple skills affected
- Data loss or corruption
- Security concerns

---

## Discovery Issues

### Issue 1: Skill Not Appearing in Catalog

**Symptoms:**
- Deployed skill doesn't show in skill list
- Claude Code doesn't recognize skill exists
- Skill not available for invocation

**Common Causes:**

#### Cause 1.1: Invalid metadata.json

**Diagnostic:**
```bash
# Check if metadata.json exists
ls -l your-skill/metadata.json

# Validate JSON syntax
cat your-skill/metadata.json | jq .

# Expected: Valid JSON output
# Error indicates syntax problem
```

**Solution:**
```bash
# Check for common JSON errors:
# - Missing commas
# - Trailing commas
# - Unescaped quotes
# - Missing closing braces

# Example valid metadata.json:
cat > your-skill/metadata.json << 'EOF'
{
  "name": "your-skill-name",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "tags": ["framework", "testing"],
  "entry_point_tokens": 60,
  "full_tokens": 4000,
  "requires": [],
  "author": "your-github-username",
  "updated": "2025-12-02"
}
EOF

# Validate again
cat your-skill/metadata.json | jq .
```

**Verification:**
```bash
# Should output formatted JSON without errors
cat your-skill/metadata.json | jq '.'

# Check required fields present
cat your-skill/metadata.json | jq '{name, version, category}'

# Output should show all three fields with values
```

---

#### Cause 1.2: Missing or Invalid YAML Frontmatter

**Diagnostic:**
```bash
# Check first 20 lines of SKILL.md
head -20 your-skill/SKILL.md

# Look for:
# ---
# name: skill-name
# description: ...
# ---

# Verify YAML syntax
python3 << 'EOF'
import yaml
with open('your-skill/SKILL.md', 'r') as f:
    content = f.read()
    if content.startswith('---'):
        yaml_end = content.find('---', 3)
        yaml_content = content[3:yaml_end]
        try:
            data = yaml.safe_load(yaml_content)
            print("✅ Valid YAML frontmatter")
            print(f"Name: {data.get('name', 'MISSING')}")
            print(f"Description: {data.get('description', 'MISSING')}")
        except yaml.YAMLError as e:
            print(f"❌ YAML Error: {e}")
    else:
        print("❌ No YAML frontmatter found")
EOF
```

**Solution:**

Add valid YAML frontmatter at the top of SKILL.md:

```yaml
---
name: your-skill-name
description: Brief description of what this skill does
version: 1.0.0
progressive_disclosure:
  entry_point:
    summary: "Concise summary (60 tokens)"
    when_to_use: "Trigger conditions"
    quick_start: "1. Step one 2. Step two 3. Step three"
---
```

**Common YAML Errors:**
- Missing opening/closing `---`
- Incorrect indentation (use 2 spaces)
- Unquoted colons in values
- Missing required fields (`name`, `description`)

**Verification:**
```bash
# Validate YAML frontmatter
head -20 your-skill/SKILL.md

# Should see:
# ---
# name: your-skill-name
# description: ...
# ---
```

---

#### Cause 1.3: Deployed to Wrong Directory

**Diagnostic:**
```bash
# Check expected skill location
ls -la ~/.claude/skills/your-skill-name/

# Check alternative locations
find ~/.claude -name "SKILL.md" | grep your-skill-name

# Verify directory structure
tree -L 2 ~/.claude/skills/
```

**Solution:**
```bash
# Remove from wrong location (if found)
rm -rf ~/.claude/incorrect-location/your-skill-name

# Deploy to correct location
mkdir -p ~/.claude/skills/your-skill-name
cp -r /path/to/skill/source/* ~/.claude/skills/your-skill-name/

# Verify deployment
ls -la ~/.claude/skills/your-skill-name/
# Should see: SKILL.md, metadata.json, and any references/
```

**Expected Structure:**
```
~/.claude/skills/
├── your-skill-name/
│   ├── SKILL.md
│   ├── metadata.json
│   └── references/ (optional)
```

---

#### Cause 1.4: File Permission Issues

**Diagnostic:**
```bash
# Check file permissions
ls -l ~/.claude/skills/your-skill-name/

# Check if files are readable
cat ~/.claude/skills/your-skill-name/SKILL.md > /dev/null
echo $?  # Should output 0 (success)

# Check directory permissions
ls -ld ~/.claude/skills/your-skill-name/
# Should show: drwxr-xr-x (755 or more permissive)
```

**Solution:**
```bash
# Fix file permissions
chmod 644 ~/.claude/skills/your-skill-name/*.md
chmod 644 ~/.claude/skills/your-skill-name/*.json

# Fix directory permissions
chmod 755 ~/.claude/skills/your-skill-name/

# Fix recursively if needed
chmod -R u+rw,go+r ~/.claude/skills/your-skill-name/

# Verify
ls -la ~/.claude/skills/your-skill-name/
```

---

#### Cause 1.5: Missing Required Fields

**Diagnostic:**
```bash
# Check for required metadata fields
cat your-skill/metadata.json | jq '{name, version, category, description: .description // "MISSING"}'

# Check YAML frontmatter fields
head -30 your-skill/SKILL.md | grep -E "^name:|^description:"
```

**Required Fields in metadata.json:**
- `name` (string)
- `version` (semver string)
- `category` (string: "toolchain" or "universal")

**Required Fields in YAML frontmatter:**
- `name` (string)
- `description` (string)

**Solution:**
```bash
# Add missing fields to metadata.json
jq '. + {name: "your-skill-name", version: "1.0.0", category: "toolchain"}' \
  your-skill/metadata.json > temp.json && mv temp.json your-skill/metadata.json

# Verify
cat your-skill/metadata.json | jq '{name, version, category}'
```

---

### Issue 2: Skill Appears But Shows as "Invalid"

**Symptoms:**
- Skill listed in catalog with warning icon
- Marked as "invalid" or "incomplete"
- Can't be invoked

**Diagnostic:**
```bash
# Check metadata.json completeness
cat your-skill/metadata.json | jq .

# Verify SKILL.md content
wc -l your-skill/SKILL.md
# Should be >50 lines for meaningful skill

# Check for empty or minimal content
head -50 your-skill/SKILL.md
```

**Solution:**

Ensure skill has:
1. Complete YAML frontmatter with all fields
2. Meaningful content (>50 lines)
3. Valid JSON in metadata.json
4. At least one example or pattern

**Verification:**
```bash
# Content length check
wc -l your-skill/SKILL.md
# Should be >100 lines for full skill

# Field completeness
cat your-skill/metadata.json | jq 'keys | length'
# Should be >5 fields

# YAML validation
python3 -c "import yaml; yaml.safe_load(open('your-skill/SKILL.md').read().split('---')[1])"
# Should exit without error
```

---

## Loading Issues

### Issue 3: Skill Loads Partially (Entry Point Only)

**Symptoms:**
- Entry point displays correctly
- Full documentation doesn't expand
- Skill appears truncated

**Common Causes:**

#### Cause 3.1: Progressive Disclosure Not Triggered

**Diagnostic:**
```bash
# Check if skill has progressive disclosure config
grep -A 5 "progressive_disclosure:" your-skill/SKILL.md

# Check content after YAML frontmatter
tail -n +30 your-skill/SKILL.md | head -50
```

**Expected Behavior:**
- Entry point shows first (30-95 tokens)
- Full documentation expands when skill is invoked
- Expansion triggered by Claude Code automatically

**Solution:**

This is **normal behavior**. Progressive disclosure means:
1. **Entry point loads first** (efficient discovery)
2. **Full content expands on use** (when you reference the skill)

If you need full documentation immediately:
- Explicitly reference the skill in your prompt
- Ask Claude Code to "use the [skill-name] skill"
- Full documentation will expand automatically

**Not a Bug If:**
- Entry point is visible and accurate
- Full content expands when skill is used
- Token counts in metadata.json are reasonable

---

#### Cause 3.2: SKILL.md Content After Frontmatter Missing

**Diagnostic:**
```bash
# Check total file size
wc -l your-skill/SKILL.md

# Check content after frontmatter
tail -n +30 your-skill/SKILL.md | wc -l
# Should be >50 lines

# Verify content structure
grep "^##" your-skill/SKILL.md
# Should show section headers
```

**Solution:**
```bash
# If content is missing, add full documentation after YAML frontmatter:

cat >> your-skill/SKILL.md << 'EOF'

# Skill Name

## Overview
[Comprehensive explanation of skill purpose and capabilities]

## Quick Start
[Installation and minimal working example]

## Core Patterns
[Essential patterns with 20-50 line code examples]

## Advanced Usage
[Complex scenarios and integrations]

## Best Practices
[Guidelines and tips]

## Complementary Skills
[Related skills - informational only]

## Troubleshooting
[Common issues and solutions]
EOF

# Verify content added
wc -l your-skill/SKILL.md
```

---

### Issue 4: "SKILL.md Not Found" Errors

**Symptoms:**
- Error message: "SKILL.md not found"
- Skill directory exists but file missing
- Broken skill reference

**Diagnostic:**
```bash
# Check if SKILL.md exists
ls -l ~/.claude/skills/your-skill-name/SKILL.md

# Check for case sensitivity issues
ls -la ~/.claude/skills/your-skill-name/ | grep -i skill

# Check for alternative names
find ~/.claude/skills/your-skill-name/ -name "*.md"
```

**Solution:**
```bash
# Case 1: File has wrong name (e.g., skill.md, Skill.md)
cd ~/.claude/skills/your-skill-name/
mv skill.md SKILL.md  # Must be uppercase

# Case 2: File is in subdirectory
mv subdirectory/SKILL.md ./SKILL.md

# Case 3: File is completely missing
# Re-deploy skill from source
cp /path/to/source/SKILL.md ~/.claude/skills/your-skill-name/

# Verify
ls -l ~/.claude/skills/your-skill-name/SKILL.md
```

**File Naming Requirements:**
- Must be named exactly `SKILL.md` (all caps)
- Must be in skill root directory
- Must have `.md` extension
- No spaces in filename

---

### Issue 5: Skill Loads Old/Cached Version

**Symptoms:**
- Updates to SKILL.md not reflected
- Changes not appearing
- Old content still shows

**Diagnostic:**
```bash
# Check file modification time
ls -l ~/.claude/skills/your-skill-name/SKILL.md

# Compare source and deployed versions
diff /path/to/source/SKILL.md ~/.claude/skills/your-skill-name/SKILL.md

# Check if multiple copies exist
find ~/.claude -name "SKILL.md" | xargs grep "your-skill-name"
```

**Solution:**
```bash
# Clear cached version
rm -rf ~/.claude/skills/your-skill-name/

# Re-deploy fresh copy
cp -r /path/to/source/your-skill-name ~/.claude/skills/

# Restart Claude Code session (if needed)
# Force reload of skill catalog

# Verify timestamp
ls -l ~/.claude/skills/your-skill-name/SKILL.md
# Should show recent modification time
```

---

## Expansion Issues

### Issue 6: Full Documentation Won't Expand

**Symptoms:**
- Entry point visible
- Full content doesn't load when skill invoked
- Skill seems "stuck" at entry point

**Common Causes:**

#### Cause 6.1: Malformed YAML Frontmatter

**Diagnostic:**
```bash
# Extract and validate YAML frontmatter
python3 << 'EOF'
import yaml
with open('your-skill/SKILL.md', 'r') as f:
    lines = f.readlines()
    if lines[0].strip() == '---':
        yaml_lines = []
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                break
            yaml_lines.append(line)
        try:
            data = yaml.safe_load(''.join(yaml_lines))
            print("✅ Valid YAML")
            print(yaml.dump(data, default_flow_style=False))
        except yaml.YAMLError as e:
            print(f"❌ YAML Error: {e}")
            print("Problematic YAML:")
            print(''.join(yaml_lines))
EOF
```

**Common YAML Errors:**
```yaml
# ❌ Wrong indentation
progressive_disclosure:
entry_point:  # Should be indented

# ❌ Missing quotes around colons
when_to_use: Scenario: with colon  # Should quote "Scenario: with colon"

# ❌ Tabs instead of spaces
progressive_disclosure:
	entry_point:  # Use 2 spaces, not tab

# ❌ Inconsistent indentation
progressive_disclosure:
  entry_point:
     summary: "..."  # Should be 4 spaces, not 5
```

**Solution:**
```yaml
# ✅ Correct YAML frontmatter format:
---
name: your-skill-name
description: Brief description
version: 1.0.0
progressive_disclosure:
  entry_point:
    summary: "Concise summary"
    when_to_use: "Trigger conditions"
    quick_start: "1. Step 2. Step 3. Step"
---
```

**Verification:**
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('your-skill/SKILL.md').read().split('---')[1])"
# Should exit without error

# Check indentation consistency
cat your-skill/SKILL.md | head -20 | grep -E "^[[:space:]]"
# Should show consistent 2-space indentation
```

---

#### Cause 6.2: Entry Point Exceeds Token Budget

**Diagnostic:**
```bash
# Count tokens in entry point (approximate)
head -20 your-skill/SKILL.md | wc -w
# Should be <100 words (~95 tokens max)

# Check entry_point_tokens in metadata.json
cat your-skill/metadata.json | jq '.entry_point_tokens'
# Should be 30-95

# Visual inspection of entry point
head -20 your-skill/SKILL.md
```

**Token Estimation:**
- 1 token ≈ 1 word (rough approximation)
- 1 token ≈ 4 characters (average)
- Entry point should be 30-95 tokens

**Solution:**

Trim entry point to 30-95 tokens:

```yaml
# ❌ Too verbose (150+ tokens)
progressive_disclosure:
  entry_point:
    summary: "This comprehensive skill covers all aspects of the framework including setup, configuration, testing strategies, deployment patterns, and advanced usage scenarios with detailed examples for each use case."
    when_to_use: "When you are building web applications using this framework and need guidance on proper setup, configuration, testing, deployment, and following best practices for production environments"

# ✅ Concise (60 tokens)
progressive_disclosure:
  entry_point:
    summary: "Framework setup, testing, deployment with production best practices"
    when_to_use: "Building web apps, API development, production deployment"
```

**Verification:**
```bash
# Count words in entry_point section
grep -A 3 "entry_point:" your-skill/SKILL.md | wc -w
# Should be <100
```

---

#### Cause 6.3: Missing progressive_disclosure Field

**Diagnostic:**
```bash
# Check if progressive_disclosure exists
grep "progressive_disclosure:" your-skill/SKILL.md
# Should find at least one match

# Check structure
grep -A 5 "progressive_disclosure:" your-skill/SKILL.md
```

**Solution:**

Add progressive_disclosure to YAML frontmatter:

```yaml
---
name: your-skill-name
description: Brief description
version: 1.0.0
progressive_disclosure:
  entry_point:
    summary: "Concise summary of what skill does"
    when_to_use: "Trigger scenarios for using this skill"
    quick_start: "1. Install 2. Configure 3. Use"
context_limit: 700
---
```

**Verification:**
```bash
# Verify field exists and is properly structured
grep -A 5 "progressive_disclosure:" your-skill/SKILL.md
# Should show nested structure with entry_point
```

---

### Issue 7: Sections Not Loading

**Symptoms:**
- Some sections visible, others missing
- Incomplete content display
- References broken within skill

**Diagnostic:**
```bash
# Check file completeness
wc -l your-skill/SKILL.md
# Should match expected line count

# Check for truncation
tail -10 your-skill/SKILL.md
# Should show proper ending, not cut off mid-sentence

# Check for encoding issues
file your-skill/SKILL.md
# Should show: "UTF-8 Unicode text"

# Check for special characters
cat -A your-skill/SKILL.md | grep -E "[\x80-\xff]"
```

**Solution:**
```bash
# Case 1: File truncated during copy
# Re-copy from source
cp /path/to/source/SKILL.md ~/.claude/skills/your-skill-name/

# Case 2: Encoding issues
# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 your-skill/SKILL.md > temp.md
mv temp.md your-skill/SKILL.md

# Case 3: Line ending issues (Windows CRLF)
dos2unix your-skill/SKILL.md  # If dos2unix installed
# Or:
sed -i 's/\r$//' your-skill/SKILL.md  # Remove CRLF

# Verify
tail -20 your-skill/SKILL.md
# Should show complete content
```

---

## Content Issues

### Issue 8: Broken Links and References

**Symptoms:**
- "File not found" when clicking links
- References to missing files
- Broken internal links

**Common Causes:**

#### Cause 8.1: Relative Paths in Flat Deployment

**Diagnostic:**
```bash
# Check for relative path violations
grep -r "\.\\./" your-skill/

# Check for hierarchical assumptions
grep -rE "\.\./\.\./|parent directory|sibling skill" your-skill/

# Check for file:// links
grep -r "file://" your-skill/
```

**Typical Violations:**
```markdown
❌ [pytest](../../testing/pytest/SKILL.md)
❌ See ../fastapi/examples/
❌ Navigate to parent directory
❌ file://../../shared/patterns.md
```

**Solution:**

Replace relative paths with informational references:

```markdown
# ✅ Correct approach:
## Complementary Skills

When working with this skill, consider (if deployed):

- **pytest**: Testing framework for comprehensive test coverage
  - *Use case*: Writing unit and integration tests
  - *Integration*: Use fixtures for database session management

- **fastapi-local-dev**: Advanced FastAPI patterns
  - *Use case*: Development server configuration
  - *Integration*: Hot reload and debugging

*Note: All skills are independently deployable. This skill functions without them.*
```

**Verification:**
```bash
# Should return empty (no violations)
grep -r "\.\\./" your-skill/

# Check informational references format
grep -A 2 "Complementary Skills" your-skill/SKILL.md
# Should show skill names only, no paths
```

---

#### Cause 8.2: Cross-Skill References Broken

**Diagnostic:**
```bash
# Check for skill-to-skill references
grep -rE "skills\.|from skills" your-skill/

# Check for import statements
grep -rE "^import|^from.*import" your-skill/SKILL.md

# Check for dependency assumptions
grep -ri "requires.*skill|must.*install|depends on" your-skill/
```

**Solution:**

Replace hard dependencies with self-contained patterns:

```markdown
# ❌ Hard dependency
## Database Setup
For database configuration, see sqlalchemy skill (required).

# ✅ Self-contained
## Database Setup (Self-Contained)

**Essential database pattern** (inline):

```python
# Complete database setup (no external dependencies)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./app.db")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Advanced patterns** (if sqlalchemy skill deployed):
- Connection pooling configuration
- Async session management
- Migration strategies
```

**Verification:**
```bash
# No hard dependencies
grep -ri "requires.*skill" your-skill/SKILL.md
# Should be empty or only "optional"/"if deployed" contexts

# Self-contained examples present
grep -c "```python" your-skill/SKILL.md
# Should be >5 for comprehensive skill
```

---

#### Cause 8.3: Missing Referenced Files

**Diagnostic:**
```bash
# Check for referenced files
grep -oE "\[.*\]\(.*\)" your-skill/SKILL.md

# Verify referenced files exist
for ref in $(grep -oP '\(.*?\)' your-skill/SKILL.md | tr -d '()'); do
  if [[ $ref == ./* ]]; then
    echo "Checking: $ref"
    ls -l "your-skill/$ref" 2>&1
  fi
done

# Check references/ directory
ls -la your-skill/references/
```

**Solution:**
```bash
# Case 1: Move referenced files into skill directory
mkdir -p your-skill/references/
cp /path/to/missing/file.md your-skill/references/

# Case 2: Inline referenced content
# Extract content and add to SKILL.md
cat referenced-file.md >> your-skill/SKILL.md

# Case 3: Fix link to point to correct location
# Edit SKILL.md to update link path
sed -i 's|../../missing/file.md|references/file.md|g' your-skill/SKILL.md

# Verify all references resolve
grep -oP '\]\(\K[^)]+' your-skill/SKILL.md | while read link; do
  [[ -f "your-skill/$link" ]] && echo "✅ $link" || echo "❌ $link"
done
```

---

### Issue 9: Examples Don't Work

**Symptoms:**
- Code examples produce errors
- Examples incomplete or outdated
- Missing imports or dependencies

**Diagnostic:**
```bash
# Extract code examples
grep -A 20 "```python" your-skill/SKILL.md | head -50

# Check for imports
grep "^import\|^from.*import" your-skill/SKILL.md

# Check for placeholder code
grep -E "# \.\.\.|# TODO|# Implementation" your-skill/SKILL.md
```

**Solution:**

Ensure examples are complete and working:

```python
# ❌ Incomplete example
@app.route("/users")
def get_users():
    # ...implementation
    pass

# ✅ Complete, working example
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: str

@app.get("/users", response_model=List[User])
async def get_users():
    """Get all users."""
    try:
        users = [
            User(id=1, username="alice", email="alice@example.com"),
            User(id=2, username="bob", email="bob@example.com")
        ]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Example Requirements:**
- ✅ All imports included
- ✅ Complete function/class definitions
- ✅ Error handling demonstrated
- ✅ Working code (not pseudo-code)
- ✅ Comments explain non-obvious parts
- ✅ 20-50 lines per core pattern

**Verification:**
```bash
# Extract and test example
grep -A 30 "```python" your-skill/SKILL.md | head -35 > test_example.py
python3 test_example.py
# Should run without import errors
```

---

### Issue 10: Outdated Information

**Symptoms:**
- Examples use deprecated APIs
- Framework version mismatch
- Best practices outdated

**Diagnostic:**
```bash
# Check version information
grep -E "version|^#.*[0-9]+\.[0-9]+" your-skill/SKILL.md

# Check metadata update date
cat your-skill/metadata.json | jq '.updated'

# Check framework versions in examples
grep -E "pip install|npm install|cargo add" your-skill/SKILL.md
```

**Solution:**
```bash
# Update version references in SKILL.md
# Update framework version numbers
# Update deprecated API usage
# Update metadata.json timestamp

# Example update:
cat your-skill/metadata.json | \
  jq '.updated = "2025-12-02" | .version = "1.1.0"' > temp.json
mv temp.json your-skill/metadata.json

# Increment version in YAML frontmatter
sed -i 's/version: 1.0.0/version: 1.1.0/' your-skill/SKILL.md

# Add changelog entry
cat >> your-skill/SKILL.md << 'EOF'

## Changelog

### Version 1.1.0 (2025-12-02)
- Updated framework to v5.0
- Replaced deprecated APIs
- Updated examples with current best practices
EOF
```

**Version Update Guidelines:**
- **Patch (1.0.x)**: Bug fixes, typos, minor clarifications
- **Minor (1.x.0)**: New examples, additional patterns, updated frameworks
- **Major (x.0.0)**: Breaking changes, major restructuring, framework version jump

**Verification:**
```bash
# Check versions updated
grep "version:" your-skill/SKILL.md
cat your-skill/metadata.json | jq '.version, .updated'

# Verify consistency
diff <(grep "^version:" your-skill/SKILL.md | cut -d' ' -f2) \
     <(cat your-skill/metadata.json | jq -r '.version')
# Should be identical
```

---

## Performance Issues

### Issue 11: Skills Load Slowly

**Symptoms:**
- Noticeable delay loading skill catalog
- Slow skill expansion
- Claude Code response time increased

**Diagnostic:**
```bash
# Check skill file sizes
du -h ~/.claude/skills/*/SKILL.md | sort -h

# Check token counts
for skill in ~/.claude/skills/*/metadata.json; do
  name=$(basename $(dirname $skill))
  tokens=$(cat "$skill" | jq -r '.full_tokens // .entry_point_tokens')
  echo "$name: $tokens tokens"
done | sort -t: -k2 -n

# Check number of deployed skills
ls -d ~/.claude/skills/*/ | wc -l

# Check total token budget
for skill in ~/.claude/skills/*/metadata.json; do
  cat "$skill" | jq -r '.full_tokens // 0'
done | awk '{sum+=$1} END {print sum " total tokens"}'
```

**Token Budget Guidelines:**
- **Entry point**: 30-95 tokens (optimal: ~60)
- **Full documentation**: 3,000-6,000 tokens (optimal: ~4,000)
- **Total deployed skills**: <100 skills recommended
- **Total token budget**: <500,000 tokens for all skills

**Solution:**

#### Optimize Large Skills

```bash
# Find skills exceeding token budget
for skill in ~/.claude/skills/*/metadata.json; do
  name=$(basename $(dirname $skill))
  tokens=$(cat "$skill" | jq -r '.full_tokens // 0')
  if [ "$tokens" -gt 6000 ]; then
    echo "⚠️  $name: $tokens tokens (exceeds 6,000)"
  fi
done

# Reduce skill size:
# 1. Remove redundant examples
# 2. Consolidate similar patterns
# 3. Move advanced content to references/
# 4. Shorten verbose explanations
# 5. Use tables instead of lists
```

#### Deploy Selectively

```bash
# Identify unused skills
# Remove skills not relevant to current project

# Keep only essential skills
ls ~/.claude/skills/ | while read skill; do
  echo "Keep $skill? (y/n)"
  read answer
  if [ "$answer" != "y" ]; then
    rm -rf ~/.claude/skills/"$skill"
  fi
done

# Or deploy skill bundles instead of individual skills
```

**Verification:**
```bash
# Check token counts after optimization
for skill in ~/.claude/skills/*/metadata.json; do
  name=$(basename $(dirname $skill))
  tokens=$(cat "$skill" | jq -r '.full_tokens')
  echo "$name: $tokens tokens"
done | awk '{if ($2 > 6000) print "⚠️  " $0; else print "✅ " $0}'

# Verify skill count reasonable
ls -d ~/.claude/skills/*/ | wc -l
# Recommended: <50 skills for optimal performance
```

---

### Issue 12: Context Window Exceeded

**Symptoms:**
- Error: "Context window exceeded"
- Claude Code truncates responses
- Can't load additional content

**Diagnostic:**
```bash
# Count deployed skills
ls -d ~/.claude/skills/*/ | wc -l

# Calculate total entry point tokens
for skill in ~/.claude/skills/*/metadata.json; do
  cat "$skill" | jq -r '.entry_point_tokens // 60'
done | awk '{sum+=$1} END {print sum " entry point tokens total"}'

# Calculate total if all expanded
for skill in ~/.claude/skills/*/metadata.json; do
  cat "$skill" | jq -r '.full_tokens // 4000'
done | awk '{sum+=$1} END {print sum " full tokens if all expanded"}'

# Check individual conversation context
# (Claude Code tracks this internally)
```

**Context Window Limits:**
- **Claude 3.5 Sonnet**: 200,000 tokens
- **Claude 3 Opus**: 200,000 tokens
- **Claude 3 Haiku**: 200,000 tokens
- **Entry points**: ~1,100 tokens for 82 skills (99.7% savings)
- **All expanded**: ~348,000 tokens (exceeds limit!)

**Solution:**

#### Reduce Deployed Skills

```bash
# Deploy only project-relevant skills
# Remove unused skills
rm -rf ~/.claude/skills/unused-skill-1
rm -rf ~/.claude/skills/unused-skill-2

# Deploy via toolchain detection instead
# Let Claude Code auto-detect needed skills
```

#### Use Skill Bundles

```bash
# Instead of deploying 30 individual skills,
# Deploy curated bundle with 10 essential skills

# Remove individual skills
rm -rf ~/.claude/skills/skill-*

# Deploy bundle
cp -r /path/to/bundles/python-fastapi-bundle ~/.claude/bundles/
```

#### Optimize Skill Token Counts

```bash
# Reduce full_tokens in large skills
# Target: <5,000 tokens per skill

# Example: Trim verbose skill
# Before: 8,000 tokens
# After: 4,500 tokens (remove redundant examples)
```

**Verification:**
```bash
# Recalculate token budget
total_entry=$(for skill in ~/.claude/skills/*/metadata.json; do
  cat "$skill" | jq -r '.entry_point_tokens // 60'
done | awk '{sum+=$1} END {print sum}')

total_full=$(for skill in ~/.claude/skills/*/metadata.json; do
  cat "$skill" | jq -r '.full_tokens // 4000'
done | awk '{sum+=$1} END {print sum}')

echo "Entry point tokens: $total_entry (should be <5,000)"
echo "Full expansion tokens: $total_full (should be <150,000)"

# Test loading skills
# Context window error should be resolved
```

---

### Issue 13: Token Budget Exceeded in Single Skill

**Symptoms:**
- Individual skill very large
- Skill takes long to load
- Skill difficult to navigate

**Diagnostic:**
```bash
# Check skill size
wc -l ~/.claude/skills/problem-skill/SKILL.md

# Check token count
cat ~/.claude/skills/problem-skill/metadata.json | jq '.full_tokens'

# Identify large sections
grep "^##" ~/.claude/skills/problem-skill/SKILL.md | nl

# Count code blocks
grep -c "```" ~/.claude/skills/problem-skill/SKILL.md
```

**Token Budget Per Skill:**
- **Target**: 4,000 tokens
- **Maximum**: 6,000 tokens
- **Minimum**: 2,000 tokens (for comprehensive skill)

**Solution:**

#### Split Large Skill

```bash
# If skill >6,000 tokens, consider splitting:
# - skill-name-basics (core patterns)
# - skill-name-advanced (advanced patterns)

# Example: Split large FastAPI skill
# - fastapi-core (routing, models, dependency injection)
# - fastapi-advanced (background tasks, WebSockets, middleware)
```

#### Move Content to references/

```bash
# Move detailed examples to references/
mkdir -p ~/.claude/skills/problem-skill/references/

# Move advanced patterns
mv large-content.md ~/.claude/skills/problem-skill/references/

# Reference in SKILL.md:
cat >> ~/.claude/skills/problem-skill/SKILL.md << 'EOF'

## Advanced Patterns

For comprehensive advanced examples, see `references/` directory:
- `references/websockets.md`: WebSocket implementation patterns
- `references/background-tasks.md`: Celery and background job patterns
- `references/middleware.md`: Custom middleware examples
EOF
```

#### Consolidate Redundant Content

```bash
# Remove duplicate examples
# Consolidate similar patterns
# Use tables instead of verbose explanations

# Example: Before (verbose)
## Pattern 1
[50 lines of explanation]

## Pattern 2
[50 lines of explanation]

## Pattern 3
[50 lines of explanation]

# Example: After (consolidated)
## Common Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Pattern 1 | Scenario A | [10 line code snippet] |
| Pattern 2 | Scenario B | [10 line code snippet] |
| Pattern 3 | Scenario C | [10 line code snippet] |
```

**Verification:**
```bash
# Check reduced token count
cat ~/.claude/skills/problem-skill/metadata.json | jq '.full_tokens'
# Should be <6,000

# Verify content completeness
grep "^##" ~/.claude/skills/problem-skill/SKILL.md
# Should still cover 80% use case

# Test skill functionality
# Core patterns should still be inline and complete
```

---

## Self-Containment Issues

### Issue 14: Skill Doesn't Work in Flat Deployment

**Symptoms:**
- Works in source repository
- Breaks when deployed to `~/.claude/skills/`
- Missing content or broken references

**Diagnostic:**
```bash
# Test flat deployment
mkdir -p /tmp/skill-test
cp -r ~/.claude/skills/your-skill /tmp/skill-test/
cd /tmp/skill-test/your-skill

# Check content accessible
cat SKILL.md | head -50

# Check for broken references
grep -r "\.\\./" .

# Check metadata
cat metadata.json | jq .

# Look for missing files
grep -oP '\]\(\K[^)]+' SKILL.md | while read link; do
  [[ -f "$link" ]] && echo "✅ $link" || echo "❌ Missing: $link"
done
```

**Self-Containment Requirements:**
- ✅ Works in any directory (no path assumptions)
- ✅ No `../` relative paths
- ✅ All essential content inline
- ✅ References are informational only
- ✅ No dependencies on other skills

**Solution:**

Follow self-containment standard:

```bash
# 1. Eliminate relative paths
sed -i 's|\.\./\.\./[^)]*|SKILL_NAME|g' SKILL.md

# 2. Inline essential content
# Add 20-50 line code examples directly in SKILL.md

# 3. Make references informational
# Change: "See ../other-skill for examples"
# To: "See other-skill skill (if deployed) for advanced examples"

# 4. Test in isolation
mkdir -p /tmp/skill-test
cp -r your-skill /tmp/skill-test/
cd /tmp/skill-test/your-skill
cat SKILL.md  # Should be complete and understandable
```

**Verification:**
```bash
# Run self-containment checks
cd /tmp/skill-test/your-skill

# Check 1: No relative paths
grep -r "\.\\./" . && echo "❌ FAIL: Relative paths found" || echo "✅ PASS"

# Check 2: No skill imports
grep -r "from skills\." . && echo "❌ FAIL: Skill imports found" || echo "✅ PASS"

# Check 3: Content complete
wc -l SKILL.md
# Should be >100 lines

# Check 4: Examples work
grep -c "```python\|```javascript\|```typescript" SKILL.md
# Should be >5 for comprehensive skill

# Check 5: No hard dependencies
grep -i "requires.*skill\|must.*install.*skill" SKILL.md
# Should be empty or only "optional"/"if deployed"
```

---

### Issue 15: Missing Essential Content

**Symptoms:**
- Skill references other skills for core functionality
- Can't accomplish basic tasks with skill alone
- "See other-skill" without inlined alternative

**Diagnostic:**
```bash
# Check for "see other-skill" patterns
grep -i "see.*skill\|refer.*skill\|check.*skill" your-skill/SKILL.md

# Check for hard requirements
grep -i "requires\|must\|need.*skill" your-skill/SKILL.md

# Count inlined examples
grep -c "```" your-skill/SKILL.md
# Should be >5 for comprehensive skill

# Check content comprehensiveness
wc -l your-skill/SKILL.md
# Should be >200 lines for full skill
```

**Content Inlining Guidelines:**
- **Inline**: Core functionality (80% use case)
- **Inline**: Setup/configuration
- **Inline**: Essential patterns (20-50 lines each)
- **Reference**: Advanced patterns (20% use case)
- **Reference**: Optional enhancements

**Solution:**

#### Inline Essential Patterns

```markdown
# ❌ Hard dependency (missing content)
## Database Integration

For database patterns, see sqlalchemy skill.

# ✅ Self-contained (inlined content)
## Database Integration (Self-Contained)

**Essential database pattern** (inline):

```python
# Complete database setup (no external dependencies)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///./app.db")
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Advanced patterns** (if sqlalchemy skill deployed):
- Connection pooling configuration
- Async session management
- Complex relationship loading

*See sqlalchemy skill for comprehensive ORM patterns.*
```

#### Add Graceful Degradation

```markdown
## [Topic] (Self-Contained)

**Basic pattern** (included):
[20-40 lines of working code]

**Advanced patterns** (if [complementary-skill] deployed):
- Feature 1
- Feature 2
- Feature 3

*See [complementary-skill] for detailed examples.*
```

**Verification:**
```bash
# Can user accomplish core task with ONLY this skill?
# Read SKILL.md and answer:
# - Can I set up the framework? (YES/NO)
# - Can I create basic functionality? (YES/NO)
# - Can I run examples? (YES/NO)
# - Can I handle errors? (YES/NO)
# All should be YES

# Check content coverage
grep -c "```" your-skill/SKILL.md
# Should be >5

# Check graceful degradation
grep -c "(if.*deployed)" your-skill/SKILL.md
# Should be >2 for skills with complementary relationships
```

---

### Issue 16: Broken Links After Deployment

**Symptoms:**
- Internal links work in repo
- Break after deployment to flat structure
- "File not found" errors

**Diagnostic:**
```bash
# Check for internal links
grep -oE "\[.*\]\(.*\)" your-skill/SKILL.md

# Check for references/ directory
ls -la your-skill/references/

# Test link resolution in flat deployment
cd /tmp/skill-test/your-skill
for link in $(grep -oP '\]\(\K[^)]+' SKILL.md); do
  if [[ $link == /* ]] || [[ $link == http* ]]; then
    echo "✅ Absolute: $link"
  elif [[ $link == ./* ]]; then
    [[ -f "$link" ]] && echo "✅ Relative: $link" || echo "❌ Broken: $link"
  else
    echo "⚠️  Unknown: $link"
  fi
done
```

**Link Guidelines:**
- ✅ Absolute URLs: `https://example.com/docs`
- ✅ Relative to skill root: `references/example.md`
- ✅ Internal anchors: `#section-name`
- ❌ Parent directory: `../../other-skill/`
- ❌ Sibling directory: `../testing/pytest/`

**Solution:**

Fix broken links:

```bash
# Pattern 1: Fix references/ links
# Change: [Example](../references/example.md)
# To: [Example](references/example.md)
sed -i 's|\.\./references/|references/|g' your-skill/SKILL.md

# Pattern 2: Fix inter-skill links
# Change: [pytest](../../testing/pytest/SKILL.md)
# To: pytest skill (if deployed)
sed -i 's|\[pytest\](../../testing/pytest/SKILL.md)|pytest skill (if deployed)|g' your-skill/SKILL.md

# Pattern 3: Keep external links unchanged
# https://example.com/docs - works fine

# Pattern 4: Fix internal anchors
# Change: [Section](#section-name) - works fine
# Keep as-is
```

**Verification:**
```bash
# Test all links
cd /tmp/skill-test/your-skill

# Extract and test links
grep -oP '\]\(\K[^)]+' SKILL.md | while read link; do
  case "$link" in
    http*|https*)
      echo "✅ External: $link"
      ;;
    \#*)
      echo "✅ Anchor: $link"
      ;;
    */*)
      [[ -f "$link" ]] && echo "✅ Relative: $link" || echo "❌ Broken: $link"
      ;;
    *)
      echo "⚠️  Check: $link"
      ;;
  esac
done

# Should show all ✅ or ⚠️ (no ❌)
```

---

## Common Error Messages

### Error Dictionary with Solutions

#### Error: "Invalid JSON in metadata.json"

**Message:**
```
Error parsing metadata.json: Invalid JSON
```

**Cause:** Syntax error in metadata.json

**Solution:**
```bash
# Validate JSON
cat your-skill/metadata.json | jq .

# Common issues:
# - Missing comma between fields
# - Trailing comma before closing brace
# - Unescaped quotes in string values
# - Missing closing brace/bracket

# Fix syntax and validate again
cat your-skill/metadata.json | jq . > temp.json && mv temp.json your-skill/metadata.json
```

---

#### Error: "YAML frontmatter parse error"

**Message:**
```
Error: Could not parse YAML frontmatter in SKILL.md
```

**Cause:** Malformed YAML syntax

**Solution:**
```bash
# Validate YAML
python3 << 'EOF'
import yaml
with open('your-skill/SKILL.md', 'r') as f:
    content = f.read()
    yaml_content = content.split('---')[1]
    try:
        yaml.safe_load(yaml_content)
        print("✅ Valid YAML")
    except yaml.YAMLError as e:
        print(f"❌ Error: {e}")
EOF

# Common issues:
# - Inconsistent indentation (use 2 spaces)
# - Tabs instead of spaces
# - Missing quotes around strings with colons
# - Missing colon after field name
```

---

#### Error: "Skill entry point exceeds token budget"

**Message:**
```
Warning: Entry point for skill 'your-skill' exceeds 95 token limit (found: 150)
```

**Cause:** Entry point too verbose

**Solution:**
```bash
# Trim entry point to <95 tokens
# Edit YAML frontmatter, reduce verbosity

# Before:
# summary: "This comprehensive skill provides detailed coverage of..."

# After:
# summary: "Framework patterns, testing, deployment best practices"

# Count tokens (approximate)
grep -A 3 "entry_point:" your-skill/SKILL.md | wc -w
# Should be <100 words
```

---

#### Error: "Relative path detected in skill"

**Message:**
```
Error: Relative path '../other-skill/' detected in SKILL.md
Self-containment violation
```

**Cause:** Relative path to other skill

**Solution:**
```bash
# Find and fix relative paths
grep -n "\.\\./" your-skill/SKILL.md

# Replace with skill name (informational)
sed -i 's|\.\./\.\./testing/pytest/SKILL\.md|pytest skill (if deployed)|g' your-skill/SKILL.md

# Verify fix
grep "\.\\./" your-skill/SKILL.md
# Should be empty
```

---

#### Error: "Missing required field 'name' in metadata.json"

**Message:**
```
Error: metadata.json missing required field: 'name'
```

**Cause:** Required field missing from metadata.json

**Solution:**
```bash
# Add missing field
jq '. + {name: "your-skill-name"}' your-skill/metadata.json > temp.json
mv temp.json your-skill/metadata.json

# Verify
cat your-skill/metadata.json | jq '{name, version, category}'
```

---

#### Error: "Skill requires other skill (dependency violation)"

**Message:**
```
Warning: Skill 'your-skill' has dependency on 'other-skill'
Self-containment violation
```

**Cause:** Skill references other skill as requirement

**Solution:**
```bash
# Find dependency statements
grep -i "requires.*skill\|must.*install.*skill\|depends on.*skill" your-skill/SKILL.md

# Replace with optional language
# Before: "This skill requires pytest skill"
# After: "Works well with pytest skill (if deployed)"

# Or inline essential content instead
```

---

#### Error: "Context window exceeded"

**Message:**
```
Error: Context window limit exceeded
Unable to load additional skills
```

**Cause:** Too many skills deployed or expanded

**Solution:**
```bash
# Reduce number of deployed skills
ls -d ~/.claude/skills/*/ | wc -l

# Deploy only essential skills
rm -rf ~/.claude/skills/unused-skill-*

# Or use skill bundles instead
```

---

#### Error: "Skill file not found"

**Message:**
```
Error: SKILL.md not found in skill directory
```

**Cause:** Missing or misnamed SKILL.md file

**Solution:**
```bash
# Check file exists
ls -l ~/.claude/skills/your-skill/SKILL.md

# Check for case sensitivity
ls -la ~/.claude/skills/your-skill/ | grep -i skill

# Fix filename if wrong
mv ~/.claude/skills/your-skill/skill.md ~/.claude/skills/your-skill/SKILL.md
# Must be exactly "SKILL.md" (all caps)
```

---

#### Error: "Invalid version format"

**Message:**
```
Error: Invalid version format in metadata.json
Expected: X.Y.Z (semantic versioning)
```

**Cause:** Version doesn't follow semantic versioning

**Solution:**
```bash
# Check current version
cat your-skill/metadata.json | jq '.version'

# Fix to semantic versioning format
jq '.version = "1.0.0"' your-skill/metadata.json > temp.json
mv temp.json your-skill/metadata.json

# Format: MAJOR.MINOR.PATCH
# Example: 1.2.3
```

---

## Diagnostic Tools

### Validation Scripts

#### Complete Skill Validation Script

```bash
#!/bin/bash
# validate-skill.sh - Comprehensive skill validation

SKILL_DIR="$1"

if [ -z "$SKILL_DIR" ]; then
  echo "Usage: $0 <skill-directory>"
  exit 1
fi

echo "=== Validating Skill: $SKILL_DIR ==="
echo

# Check 1: Required files exist
echo "Check 1: Required files"
[[ -f "$SKILL_DIR/SKILL.md" ]] && echo "✅ SKILL.md exists" || echo "❌ SKILL.md missing"
[[ -f "$SKILL_DIR/metadata.json" ]] && echo "✅ metadata.json exists" || echo "❌ metadata.json missing"
echo

# Check 2: JSON syntax
echo "Check 2: JSON validation"
if jq empty "$SKILL_DIR/metadata.json" 2>/dev/null; then
  echo "✅ Valid JSON"
  jq '{name, version, category}' "$SKILL_DIR/metadata.json"
else
  echo "❌ Invalid JSON"
fi
echo

# Check 3: YAML frontmatter
echo "Check 3: YAML frontmatter"
python3 << EOF
import yaml
try:
    with open('$SKILL_DIR/SKILL.md', 'r') as f:
        content = f.read()
        if content.startswith('---'):
            yaml_content = content.split('---')[1]
            data = yaml.safe_load(yaml_content)
            print("✅ Valid YAML")
            print(f"  Name: {data.get('name', 'MISSING')}")
            print(f"  Description: {data.get('description', 'MISSING')[:50]}...")
        else:
            print("❌ No YAML frontmatter")
except Exception as e:
    print(f"❌ YAML Error: {e}")
EOF
echo

# Check 4: Relative paths
echo "Check 4: Relative path violations"
if grep -r "\.\\./" "$SKILL_DIR/" 2>/dev/null | grep -v ".git"; then
  echo "❌ Relative paths found (see above)"
else
  echo "✅ No relative paths"
fi
echo

# Check 5: Skill dependencies
echo "Check 5: Skill dependencies"
if grep -i "requires.*skill\|must.*install.*skill" "$SKILL_DIR/SKILL.md" | grep -v "optional\|if deployed"; then
  echo "❌ Hard dependencies found (see above)"
else
  echo "✅ No hard dependencies"
fi
echo

# Check 6: Content size
echo "Check 6: Content metrics"
lines=$(wc -l < "$SKILL_DIR/SKILL.md")
code_blocks=$(grep -c '```' "$SKILL_DIR/SKILL.md")
echo "  Lines: $lines (should be >100)"
echo "  Code blocks: $code_blocks (should be >5)"
[[ $lines -gt 100 ]] && echo "✅ Sufficient content" || echo "⚠️  Minimal content"
echo

# Check 7: Token counts
echo "Check 7: Token estimates"
entry_tokens=$(jq -r '.entry_point_tokens // "MISSING"' "$SKILL_DIR/metadata.json")
full_tokens=$(jq -r '.full_tokens // "MISSING"' "$SKILL_DIR/metadata.json")
echo "  Entry point: $entry_tokens (target: 30-95)"
echo "  Full doc: $full_tokens (target: 3000-6000)"
echo

# Check 8: Isolation test
echo "Check 8: Isolation test"
temp_dir="/tmp/skill-test-$$"
mkdir -p "$temp_dir"
cp -r "$SKILL_DIR" "$temp_dir/"
skill_name=$(basename "$SKILL_DIR")
if [[ -f "$temp_dir/$skill_name/SKILL.md" ]]; then
  echo "✅ Skill copies successfully"
  echo "✅ Content accessible in isolation"
else
  echo "❌ Isolation test failed"
fi
rm -rf "$temp_dir"
echo

echo "=== Validation Complete ==="
```

**Usage:**
```bash
# Make executable
chmod +x validate-skill.sh

# Run validation
./validate-skill.sh your-skill-name/

# Check all skills
for skill in ~/.claude/skills/*/; do
  ./validate-skill.sh "$skill"
done
```

---

#### YAML Linter

```bash
#!/bin/bash
# yaml-lint.sh - Validate YAML frontmatter

SKILL_FILE="$1"

if [ -z "$SKILL_FILE" ]; then
  echo "Usage: $0 <SKILL.md>"
  exit 1
fi

python3 << EOF
import yaml
import sys

try:
    with open('$SKILL_FILE', 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        print("❌ No YAML frontmatter (must start with ---)")
        sys.exit(1)

    # Extract YAML section
    parts = content.split('---')
    if len(parts) < 3:
        print("❌ YAML frontmatter not properly closed (missing second ---)")
        sys.exit(1)

    yaml_content = parts[1]

    # Parse YAML
    data = yaml.safe_load(yaml_content)

    # Check required fields
    required = ['name', 'description']
    missing = [field for field in required if field not in data]

    if missing:
        print(f"❌ Missing required fields: {', '.join(missing)}")
        sys.exit(1)

    print("✅ Valid YAML frontmatter")
    print(f"\nFields found:")
    for key in data.keys():
        print(f"  - {key}")

    # Check progressive disclosure structure
    if 'progressive_disclosure' in data:
        pd = data['progressive_disclosure']
        if isinstance(pd, dict) and 'entry_point' in pd:
            print("\n✅ Progressive disclosure structure present")
            ep = pd['entry_point']
            if 'summary' in ep:
                print(f"  Summary length: {len(ep['summary'])} chars")
            if 'when_to_use' in ep:
                print(f"  When to use: {len(ep['when_to_use'])} chars")
        else:
            print("\n⚠️  Progressive disclosure field exists but incomplete")

    sys.exit(0)

except yaml.YAMLError as e:
    print(f"❌ YAML syntax error:")
    print(f"  {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF
```

**Usage:**
```bash
# Validate single skill
./yaml-lint.sh your-skill/SKILL.md

# Validate all skills
find ~/.claude/skills -name "SKILL.md" -exec ./yaml-lint.sh {} \;
```

---

#### Self-Containment Checker

```bash
#!/bin/bash
# check-self-containment.sh - Verify self-containment compliance

SKILL_DIR="$1"

if [ -z "$SKILL_DIR" ]; then
  echo "Usage: $0 <skill-directory>"
  exit 1
fi

echo "=== Self-Containment Check: $(basename $SKILL_DIR) ==="
echo

VIOLATIONS=0

# Check 1: Relative paths
echo "Test 1: Relative path violations"
if grep -r "\.\\./" "$SKILL_DIR/" 2>/dev/null | grep -v ".git\|node_modules"; then
  echo "❌ FAIL: Relative paths found"
  VIOLATIONS=$((VIOLATIONS + 1))
else
  echo "✅ PASS: No relative paths"
fi
echo

# Check 2: Skill imports
echo "Test 2: Cross-skill imports"
if grep -r "from skills\." "$SKILL_DIR/" 2>/dev/null; then
  echo "❌ FAIL: Skill imports found"
  VIOLATIONS=$((VIOLATIONS + 1))
else
  echo "✅ PASS: No skill imports"
fi
echo

# Check 3: Hard dependencies
echo "Test 3: Hard dependencies"
if grep -i "requires.*skill\|must.*install.*skill\|depends on.*skill" "$SKILL_DIR/SKILL.md" 2>/dev/null | grep -v "optional\|if deployed"; then
  echo "❌ FAIL: Hard dependencies found"
  VIOLATIONS=$((VIOLATIONS + 1))
else
  echo "✅ PASS: No hard dependencies"
fi
echo

# Check 4: Content completeness
echo "Test 4: Content completeness"
code_blocks=$(grep -c '```' "$SKILL_DIR/SKILL.md" 2>/dev/null)
if [ "$code_blocks" -lt 3 ]; then
  echo "⚠️  WARNING: Only $code_blocks code blocks (recommend >5)"
  echo "   May need more inlined examples"
else
  echo "✅ PASS: $code_blocks code blocks found"
fi
echo

# Check 5: Metadata dependencies
echo "Test 5: Metadata dependencies"
if [ -f "$SKILL_DIR/metadata.json" ]; then
  requires=$(jq -r '.requires // []' "$SKILL_DIR/metadata.json")
  if [ "$requires" != "[]" ]; then
    echo "⚠️  WARNING: 'requires' field not empty"
    echo "   Contents: $requires"
    echo "   Should only list external packages, not skills"
  else
    echo "✅ PASS: No dependencies in metadata"
  fi
else
  echo "⚠️  WARNING: metadata.json not found"
fi
echo

# Check 6: Isolation test
echo "Test 6: Isolation deployment"
temp_dir="/tmp/self-containment-test-$$"
mkdir -p "$temp_dir"
cp -r "$SKILL_DIR" "$temp_dir/"
skill_name=$(basename "$SKILL_DIR")

# Check if all referenced files exist
cd "$temp_dir/$skill_name" 2>/dev/null
if [ $? -eq 0 ]; then
  missing_refs=0
  grep -oP '\]\(\K[^)]+' SKILL.md 2>/dev/null | while read link; do
    # Skip external URLs and anchors
    if [[ ! $link =~ ^http ]] && [[ ! $link =~ ^# ]]; then
      if [[ ! -f "$link" ]]; then
        echo "  ❌ Missing: $link"
        missing_refs=$((missing_refs + 1))
      fi
    fi
  done

  if [ $missing_refs -eq 0 ]; then
    echo "✅ PASS: All references resolve in isolation"
  else
    echo "❌ FAIL: Missing references in isolation"
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
else
  echo "❌ FAIL: Could not deploy to isolation"
  VIOLATIONS=$((VIOLATIONS + 1))
fi

rm -rf "$temp_dir"
echo

# Summary
echo "=== Summary ==="
if [ $VIOLATIONS -eq 0 ]; then
  echo "✅ All self-containment checks passed"
  exit 0
else
  echo "❌ $VIOLATIONS violation(s) found"
  exit 1
fi
```

**Usage:**
```bash
# Check single skill
./check-self-containment.sh your-skill/

# Check all skills
for skill in ~/.claude/skills/*/; do
  ./check-self-containment.sh "$skill"
done
```

---

#### Token Counter

```bash
#!/bin/bash
# count-tokens.sh - Estimate token count

FILE="$1"

if [ -z "$FILE" ]; then
  echo "Usage: $0 <markdown-file>"
  exit 1
fi

# Simple token estimation:
# ~1 token per word
# ~1 token per 4 characters
# More accurate: use tiktoken library

words=$(wc -w < "$FILE")
chars=$(wc -c < "$FILE")

tokens_by_words=$words
tokens_by_chars=$((chars / 4))
estimated_tokens=$(((tokens_by_words + tokens_by_chars) / 2))

echo "Token Estimates for: $(basename $FILE)"
echo "  Words: $words"
echo "  Characters: $chars"
echo "  Estimated tokens (by words): $tokens_by_words"
echo "  Estimated tokens (by chars): $tokens_by_chars"
echo "  Average estimate: $estimated_tokens"
echo

# Check against guidelines
if [ $estimated_tokens -lt 2000 ]; then
  echo "⚠️  Low token count (<2,000) - may be incomplete"
elif [ $estimated_tokens -gt 6000 ]; then
  echo "⚠️  High token count (>6,000) - consider reducing"
else
  echo "✅ Token count within recommended range (3,000-6,000)"
fi
```

**Usage:**
```bash
# Count tokens in skill
./count-tokens.sh your-skill/SKILL.md

# Count entry point tokens
head -20 your-skill/SKILL.md > /tmp/entry-point.md
./count-tokens.sh /tmp/entry-point.md
```

---

### Batch Validation

```bash
#!/bin/bash
# validate-all-skills.sh - Validate all deployed skills

SKILLS_DIR="${1:-$HOME/.claude/skills}"

echo "=== Validating All Skills in: $SKILLS_DIR ==="
echo

total=0
passed=0
failed=0

for skill_dir in "$SKILLS_DIR"/*/; do
  total=$((total + 1))
  skill_name=$(basename "$skill_dir")

  echo "[$total] Validating: $skill_name"

  # Quick validation checks
  errors=0

  # Check SKILL.md exists
  if [[ ! -f "$skill_dir/SKILL.md" ]]; then
    echo "  ❌ SKILL.md missing"
    errors=$((errors + 1))
  fi

  # Check metadata.json exists and valid
  if [[ ! -f "$skill_dir/metadata.json" ]]; then
    echo "  ❌ metadata.json missing"
    errors=$((errors + 1))
  elif ! jq empty "$skill_dir/metadata.json" 2>/dev/null; then
    echo "  ❌ Invalid JSON"
    errors=$((errors + 1))
  fi

  # Check for relative paths
  if grep -r "\.\\./" "$skill_dir/" 2>/dev/null | grep -qv ".git"; then
    echo "  ❌ Relative paths found"
    errors=$((errors + 1))
  fi

  # Summary
  if [ $errors -eq 0 ]; then
    echo "  ✅ Passed"
    passed=$((passed + 1))
  else
    echo "  ❌ Failed ($errors error(s))"
    failed=$((failed + 1))
  fi
  echo
done

echo "=== Validation Summary ==="
echo "Total skills: $total"
echo "Passed: $passed"
echo "Failed: $failed"
echo

if [ $failed -eq 0 ]; then
  echo "✅ All skills passed validation"
  exit 0
else
  echo "❌ $failed skill(s) failed validation"
  exit 1
fi
```

**Usage:**
```bash
# Validate all skills in default location
./validate-all-skills.sh

# Validate skills in custom location
./validate-all-skills.sh /path/to/skills

# Save report to file
./validate-all-skills.sh > validation-report.txt 2>&1
```

---

## Getting Help

### When to Seek Additional Help

File a GitHub issue if:

1. **Problem persists after troubleshooting**
   - Followed this guide completely
   - Issue not resolved
   - Uncertain about next steps

2. **Suspected Claude Code bug**
   - Skill follows all standards
   - Validation passes
   - Still doesn't work

3. **Multiple skills affected**
   - Widespread issue
   - Affects many skills
   - Pattern suggests systemic problem

4. **Data loss or corruption**
   - Skill content lost
   - Metadata corrupted
   - Cannot recover manually

5. **Security concerns**
   - Potential vulnerability
   - Suspicious behavior
   - Privacy issues

### Information to Provide

When filing an issue, include:

#### 1. System Information
```bash
# Claude Code version
claude-code --version

# Operating system
uname -a

# Skill directory
ls -la ~/.claude/skills/problem-skill/
```

#### 2. Skill Information
```bash
# Skill name and version
cat problem-skill/metadata.json | jq '{name, version}'

# YAML frontmatter
head -30 problem-skill/SKILL.md

# Validation output
./validate-skill.sh problem-skill/
```

#### 3. Error Messages
```bash
# Full error message (copy-paste)
# Stack trace if available
# Context (what you were doing when error occurred)
```

#### 4. Steps to Reproduce
```markdown
1. Deploy skill to ~/.claude/skills/
2. Invoke skill with command: [command]
3. Error appears: [error message]
4. Expected: [what should happen]
5. Actual: [what actually happens]
```

#### 5. Troubleshooting Attempted
```markdown
- Followed section: [section name in this guide]
- Ran diagnostic: [command]
- Result: [output]
- Still not working: [describe issue]
```

### GitHub Issues Process

#### 1. Search Existing Issues
```
https://github.com/bobmatnyc/claude-mpm-skills/issues
```
- Search for similar issues
- Check if already reported
- Review solutions in closed issues

#### 2. Create New Issue
**Title:** `[Troubleshooting] Brief description`

**Template:**
```markdown
## Problem Description
[Clear description of issue]

## Skill Information
- Name: your-skill-name
- Version: 1.0.0
- Category: toolchain/universal

## System Information
- Claude Code version: X.Y.Z
- OS: macOS/Linux/Windows
- Skill location: ~/.claude/skills/your-skill/

## Steps to Reproduce
1. Step one
2. Step two
3. Error occurs

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Diagnostic Output
```bash
[validation output]
```

## Troubleshooting Attempted
- Followed: [guide section]
- Tried: [solution]
- Result: [still broken/partially fixed]

## Additional Context
[Screenshots, logs, or other relevant information]
```

#### 3. Label Appropriately
- `troubleshooting`: Issue related to this guide
- `bug`: Suspected bug in Claude Code
- `documentation`: Documentation issue
- `help wanted`: Need community assistance

### Community Resources

#### Discussions
```
https://github.com/bobmatnyc/claude-mpm-skills/discussions
```
- Ask questions
- Share experiences
- Get advice from community

#### Discord/Slack (if available)
- Real-time help
- Community support
- Quick questions

#### Documentation
- [SKILL_SELF_CONTAINMENT_STANDARD.md](SKILL_SELF_CONTAINMENT_STANDARD.md)
- [SKILL_CREATION_PR_CHECKLIST.md](SKILL_CREATION_PR_CHECKLIST.md)
- [VERSIONING.md](VERSIONING.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)

### Contributing Fixes

Found a solution? Help others by:

1. **Update This Guide**
   - Add solution to relevant section
   - Include diagnostic commands
   - Provide working examples

2. **Submit PR**
   - Follow [CONTRIBUTING.md](../CONTRIBUTING.md)
   - Update troubleshooting guide
   - Add to error dictionary

3. **Share in Discussions**
   - Post solution in GitHub Discussions
   - Help others with same issue
   - Document workarounds

---

## Contributing Troubleshooting Tips

### How to Add New Solutions

1. **Identify Common Issue**
   - Encountered multiple times
   - Not covered in guide
   - Clear solution exists

2. **Document Thoroughly**
   - Problem description
   - Diagnostic commands
   - Step-by-step solution
   - Verification steps

3. **Submit PR**
   ```bash
   # Fork repository
   git clone https://github.com/your-username/claude-mpm-skills.git
   cd claude-mpm-skills

   # Create branch
   git checkout -b troubleshooting-update

   # Edit guide
   vim docs/TROUBLESHOOTING.md

   # Commit changes
   git add docs/TROUBLESHOOTING.md
   git commit -m "docs: add troubleshooting for [issue]"

   # Push and create PR
   git push origin troubleshooting-update
   ```

4. **PR Description**
   ```markdown
   ## Troubleshooting Update

   **Issue:** [Problem description]

   **Solution:** [Brief description of fix]

   **Changes:**
   - Added diagnostic commands for [issue]
   - Documented solution steps
   - Included verification commands

   **Tested:** Yes/No
   ```

### What Makes a Good Troubleshooting Entry

✅ **Good Troubleshooting Entry:**
- Clear problem description
- Reliable diagnostic commands
- Step-by-step solution
- Verification steps
- Example output
- Links to related docs

❌ **Poor Troubleshooting Entry:**
- Vague problem description
- No diagnostic commands
- "Just try this" without explanation
- No verification
- No examples

### Review Process

1. **Maintainer Review**
   - Verify solution works
   - Check formatting
   - Test commands
   - Approve or request changes

2. **Community Feedback**
   - Other users test solution
   - Suggest improvements
   - Report issues

3. **Merge**
   - Solution added to guide
   - Acknowledged in commit
   - Available for all users

---

## Appendix: Quick Reference Commands

### Essential Diagnostics

```bash
# Check if skill exists
ls -lh ~/.claude/skills/your-skill/SKILL.md

# Validate JSON
cat your-skill/metadata.json | jq .

# Validate YAML
head -20 your-skill/SKILL.md

# Check relative paths
grep -r "\.\\./" your-skill/

# Check self-containment
grep -i "requires.*skill" your-skill/SKILL.md

# Count tokens
wc -w your-skill/SKILL.md

# Test isolation
mkdir /tmp/test && cp -r your-skill /tmp/test/ && cd /tmp/test/your-skill
```

### Validation Suite

```bash
# Full validation
for skill in ~/.claude/skills/*/; do
  echo "Validating: $(basename $skill)"

  # Check files
  [[ -f "$skill/SKILL.md" ]] && echo "✅ SKILL.md" || echo "❌ SKILL.md missing"

  # Check JSON
  jq empty "$skill/metadata.json" 2>/dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

  # Check paths
  grep -r "\.\\./" "$skill" | grep -qv ".git" && echo "❌ Relative paths" || echo "✅ No relative paths"

  echo "---"
done
```

### Common Fixes

```bash
# Fix JSON syntax
cat your-skill/metadata.json | jq . > temp.json && mv temp.json your-skill/metadata.json

# Remove relative paths
sed -i 's|\.\./\.\./[^)]*|SKILL_NAME (if deployed)|g' your-skill/SKILL.md

# Fix file permissions
chmod 644 your-skill/*.md your-skill/*.json

# Re-deploy skill
rm -rf ~/.claude/skills/your-skill
cp -r /path/to/source/your-skill ~/.claude/skills/
```

---

**Version:** 1.0.0
**Last Updated:** 2025-12-02
**Maintainer:** Claude MPM Team
**License:** MIT

For updates to this guide, see: [CONTRIBUTING.md](../CONTRIBUTING.md)
