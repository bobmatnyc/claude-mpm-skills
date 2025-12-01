# Skill Creation PR Checklist

**Version:** 1.0.0
**Purpose:** Copy-paste checklist for new skill pull requests
**Reference:** [SKILL_SELF_CONTAINMENT_STANDARD.md](SKILL_SELF_CONTAINMENT_STANDARD.md)

---

## Quick Start

Copy this entire checklist into your PR description and check each item before submitting.

---

## New Skill Self-Containment Checklist

**Skill Name:** `[your-skill-name]`
**Category:** `[framework/testing/debugging/collaboration/etc]`
**Toolchain:** `[python/javascript/typescript/rust/go/php/universal/etc]`
**PR Author:** `[@your-github-username]`

---

### ✅ Self-Containment Verification

#### 1. Flat Directory Deployment Test

- [ ] **Copied skill to isolated directory**
  ```bash
  mkdir -p /tmp/skill-test
  cp -r your-skill-name /tmp/skill-test/
  cd /tmp/skill-test/your-skill-name
  ```

- [ ] **Verified all content accessible**
  - SKILL.md displays complete content
  - metadata.json validates
  - No missing files or broken references

- [ ] **No "file not found" errors**
  - All examples work
  - All referenced files exist within skill directory
  - References/ directory (if exists) is accessible

**Isolation Test Result:**
```
✅ PASS - Skill works in flat directory
Location tested: /tmp/skill-test/your-skill-name
All content accessible: YES
Broken references: NONE
```

---

#### 2. Zero Relative Path Violations

- [ ] **Ran grep verification for relative paths**
  ```bash
  cd /Users/masa/Projects/claude-mpm-skills
  grep -r "\.\\./" your-skill-name/
  ```

- [ ] **Output is empty (no violations found)**

- [ ] **Manually verified no path violations**
  - No `../` anywhere in skill
  - No `../../` in any files
  - No hierarchical assumptions

**Grep Verification Output:**
```bash
$ grep -r "\.\\./" your-skill-name/
[paste output here - should be empty]

$ grep -r "from skills\." your-skill-name/
[paste output here - should be empty]

$ grep -r "import.*\.\./" your-skill-name/
[paste output here - should be empty]
```

---

#### 3. Essential Content Inlined

- [ ] **Critical patterns included in SKILL.md**
  - Core functionality patterns (20-50 lines each)
  - Essential code examples
  - No "see other skill" for core features

- [ ] **Setup/configuration complete**
  - Installation instructions
  - Environment setup
  - Configuration examples
  - Dependencies listed

- [ ] **Working examples provided**
  - Examples are complete (not fragments)
  - Examples run independently
  - Examples demonstrate key concepts
  - Comments explain important parts

- [ ] **Common use cases covered**
  - 80% use case addressed
  - Basic patterns included
  - Error handling shown

**Content Completeness Check:**
```
✅ Can user accomplish core task with ONLY this skill? YES
✅ Are critical patterns included (not just referenced)? YES
✅ Do examples work without other skills? YES
✅ Is setup/configuration complete? YES
```

---

#### 4. Complementary Skills Listed Informationally

- [ ] **Used skill names only (no paths)**
  - References use text names: "pytest", "fastapi-local-dev"
  - No file paths: ~~`../../other-skill/SKILL.md`~~
  - No directory paths: ~~`../testing/pytest/`~~

- [ ] **Described relationships clearly**
  - Explained how skills complement each other
  - Noted specific use cases for combinations
  - Clarified integration points (if applicable)

- [ ] **Noted "if deployed" for optional enhancements**
  - Used "if deployed" language
  - Used "optional" or "recommended" language
  - Made clear these are enhancements, not requirements

- [ ] **No "required" or "must install" language**
  - No "This skill requires X"
  - No "Must have Y installed"
  - No "Depends on Z skill"

**Complementary Skills Section Example:**
```markdown
## Complementary Skills

When using this skill, consider (if deployed):

- **skill-name**: How it complements this skill
  - *Use case*: Specific scenario
  - *Integration*: How they work together (optional)

*Note: All skills are independently deployable.*
```

---

#### 5. Graceful Degradation Implemented

- [ ] **Basic functionality is self-contained**
  - Core features work without other skills
  - Essential patterns included inline
  - Minimum viable functionality complete

- [ ] **Advanced features note optional skills**
  - Clearly marked "Advanced" sections
  - Note which skill provides enhancement
  - Explain what additional capability unlocks

- [ ] **Clear distinction: what's included vs. what needs other skills**
  - Inline patterns: "Self-contained pattern (included)"
  - Optional enhancements: "If X skill deployed"
  - Progressive disclosure: Basic → Advanced

**Graceful Degradation Example:**
```markdown
## Testing (Self-Contained)

**Basic testing** (included):
[20-40 lines of inline pattern]

**Advanced fixtures** (if pytest skill deployed):
- Feature 1
- Feature 2

*See pytest skill for comprehensive patterns.*
```

---

#### 6. Tested in Isolation

- [ ] **Verified skill works alone**
  - Deployed to empty directory
  - Read SKILL.md start to finish
  - Confirmed understanding without external references

- [ ] **Examples run without other skills**
  - Copied examples to test environment
  - Ran examples independently
  - Verified no missing imports/dependencies

- [ ] **Documentation makes sense standalone**
  - No unexplained concepts
  - No "see elsewhere" for critical info
  - Complete mental model from SKILL.md alone

- [ ] **No assumptions about other skills being present**
  - Doesn't assume directory structure
  - Doesn't assume other skills deployed
  - Doesn't require bundle deployment

**Isolation Test Evidence:**
```bash
$ cp -r your-skill-name /tmp/skill-test/
$ cd /tmp/skill-test/your-skill-name
$ cat SKILL.md | head -50

[paste first 50 lines - shows content is accessible]

✅ All content loads correctly
✅ No missing references
✅ Examples are complete
✅ Setup instructions present
```

---

#### 7. Bundle Membership Documented

- [ ] **Listed in metadata.json "bundles" field** (if applicable)
  ```json
  {
    "bundles": ["bundle-name"]
  }
  ```

- [ ] **Bundle deployment noted as optional**
  - SKILL.md mentions bundle membership
  - Clarifies bundle is optional
  - Notes skill works outside bundle

- [ ] **Skill works independently of bundle**
  - Tested without other bundle skills
  - No bundle-specific dependencies
  - Standalone functionality complete

**Bundle Membership Section** (if applicable):
```markdown
## Bundle Context

This skill is part of the **[Bundle Name]** bundle.

**If deployed via bundle**, these skills work together:
- skill-1
- skill-2
- skill-3

**If deployed standalone**, this skill is fully functional.

*Bundle deployment is optional.*
```

---

#### 8. Metadata Validation

- [ ] **No other skills in "requires" field**
  ```json
  {
    "requires": []  // Empty or external packages only
  }
  ```

- [ ] **"dependencies" lists only external packages**
  ```json
  {
    "dependencies": ["package-name"]  // External packages, not skills
  }
  ```

- [ ] **"tags" include "self-contained"**
  ```json
  {
    "tags": ["self-contained", "framework", "testing"]
  }
  ```

- [ ] **Version and author specified**
  ```json
  {
    "version": "1.0.0",
    "author": "github-username",
    "updated": "2025-11-30"
  }
  ```

**metadata.json Validation:**
```bash
$ cat your-skill-name/metadata.json | jq .

[paste output here - should show valid JSON]

✅ Valid JSON: YES
✅ No skill dependencies: YES
✅ Self-contained tag: YES
✅ Version specified: YES
```

---

### 🔍 Verification Commands

Run these commands and paste output in PR:

```bash
# Command 1: Check for relative path violations
cd /Users/masa/Projects/claude-mpm-skills
grep -r "\.\\./" your-skill-name/

# Expected output: (empty)

# Command 2: Check for skill import violations
grep -r "from skills\." your-skill-name/

# Expected output: (empty)

# Command 3: Check references/ directory (if exists)
find your-skill-name/references/ -name "*.md" -exec grep -l "\\.\\./\\.\\." {} \;

# Expected output: (empty)

# Command 4: Validate metadata.json
cat your-skill-name/metadata.json | jq .

# Expected output: Valid JSON with required fields

# Command 5: Check for "requires" language
grep -i "requires.*skill\|must.*install\|depends.*on" your-skill-name/SKILL.md

# Expected output: (empty or only "optional"/"if deployed" contexts)
```

---

### 📋 Reviewer Checklist

**For reviewers to verify:**

- [ ] **Grep verification output is empty** (no violations)
- [ ] **SKILL.md is self-sufficient** (read it standalone - makes sense?)
- [ ] **Examples work without other skills** (complete, runnable code)
- [ ] **Complementary skills are informational only** (no paths, no "required")
- [ ] **No relative paths in references/** (if references/ exists)
- [ ] **metadata.json doesn't list skill dependencies** (only external packages)
- [ ] **Content is inlined appropriately** (80% use case covered)
- [ ] **Graceful degradation implemented** (basic vs. advanced clear)

**Common violations to watch for:**
- ❌ `../../other-skill/` paths anywhere
- ❌ "This skill requires X skill" language
- ❌ Missing essential content (just references to other skills)
- ❌ Incomplete examples (fragments, not working code)
- ❌ Hierarchical directory assumptions
- ❌ "See other-skill for setup" without inlining setup

---

### 📝 Additional Context

**Design Decisions:**

[Explain any design choices, content inlining decisions, or trade-offs]

**Content Inlining Rationale:**

[Why you chose to inline certain patterns vs. reference others]

**Complementary Skill Relationships:**

[Explain how this skill relates to others in the ecosystem]

**Testing Approach:**

[Describe how you tested self-containment]

---

### 📚 Reference Documentation

Before submitting, review:

- **[SKILL_SELF_CONTAINMENT_STANDARD.md](SKILL_SELF_CONTAINMENT_STANDARD.md)**: Complete standard
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: General contribution guidelines
- **[examples/good-self-contained-skill/](../examples/good-self-contained-skill/)**: Template to follow
- **[examples/bad-interdependent-skill/](../examples/bad-interdependent-skill/)**: Anti-patterns to avoid

---

### ✨ Pre-Submission Final Check

Before clicking "Create Pull Request":

- [ ] **All checkboxes above are checked**
- [ ] **All grep commands return empty** (no violations)
- [ ] **Isolation test passed** (works in /tmp/skill-test/)
- [ ] **SKILL.md is self-sufficient** (read it - makes sense alone?)
- [ ] **Examples are complete** (not fragments)
- [ ] **No relative paths anywhere** (verified with grep)
- [ ] **Complementary skills noted informationally** (no paths)
- [ ] **metadata.json validated** (valid JSON, no skill deps)
- [ ] **Graceful degradation implemented** (basic vs. advanced clear)
- [ ] **Bundle membership documented** (if applicable, optional)

---

### 🎯 Success Criteria

This PR is ready to merge when:

✅ All verification commands return expected output (empty or valid)
✅ Skill works in flat directory deployment
✅ No relative path violations found
✅ Essential content inlined (80% use case)
✅ Complementary skills listed informationally only
✅ Graceful degradation implemented
✅ Tested in isolation successfully
✅ Reviewer checklist items verified
✅ CI/CD checks pass

---

## Example: Filled Checklist

**Skill Name:** `fastapi-local-dev`
**Category:** `framework`
**Toolchain:** `python`
**PR Author:** `@example-author`

### ✅ Self-Containment Verification

#### 1. Flat Directory Deployment Test
- [x] Copied skill to isolated directory
- [x] Verified all content accessible
- [x] No "file not found" errors

**Isolation Test Result:**
```
✅ PASS - Skill works in flat directory
Location tested: /tmp/skill-test/fastapi-local-dev
All content accessible: YES
Broken references: NONE
```

#### 2. Zero Relative Path Violations
- [x] Ran grep verification for relative paths
- [x] Output is empty (no violations found)
- [x] Manually verified no path violations

**Grep Verification Output:**
```bash
$ grep -r "\.\\./" fastapi-local-dev/
(empty - no violations)

$ grep -r "from skills\." fastapi-local-dev/
(empty - no violations)
```

#### 3. Essential Content Inlined
- [x] Critical patterns included in SKILL.md
- [x] Setup/configuration complete
- [x] Working examples provided
- [x] Common use cases covered

**Content Completeness Check:**
```
✅ Can user accomplish core task with ONLY this skill? YES
✅ Are critical patterns included (not just referenced)? YES
✅ Do examples work without other skills? YES
✅ Is setup/configuration complete? YES
```

[Continue with remaining checklist items...]

---

## Template Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-30 | Initial PR checklist template |

---

**Questions?** Review [SKILL_SELF_CONTAINMENT_STANDARD.md](SKILL_SELF_CONTAINMENT_STANDARD.md) or contact maintainers.
