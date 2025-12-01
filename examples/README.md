# Skill Examples Directory

This directory contains **template examples** for creating self-contained skills that comply with the [SKILL_SELF_CONTAINMENT_STANDARD.md](../docs/SKILL_SELF_CONTAINMENT_STANDARD.md).

---

## Contents

### ✅ [good-self-contained-skill/](good-self-contained-skill/)

**Complete template** demonstrating proper self-containment patterns.

**Use this as your template** when creating new skills.

**Key Features**:
- ✅ No relative path violations
- ✅ Essential content inlined (20-50 lines per pattern)
- ✅ Complete working examples
- ✅ Complementary skills listed informationally
- ✅ Graceful degradation implemented
- ✅ Works in flat directory deployment
- ✅ `metadata.json` has `self_contained: true`

**When to Use**:
- Creating any new skill
- Refactoring existing skills
- Learning self-containment best practices

---

### ❌ [bad-interdependent-skill/](bad-interdependent-skill/)

**Anti-pattern example** showing what **NOT** to do.

**Study this to learn what to avoid**.

**Violations Demonstrated**:
1. Relative path dependencies (`../../other-skill/`)
2. Missing essential content ("see other skill")
3. Hard skill dependencies ("requires X skill")
4. Cross-skill imports (`from skills.X import`)
5. Hierarchical directory assumptions
6. Incomplete examples (code fragments)
7. Cross-skill references/ paths
8. Skill dependencies in metadata.json

**When to Use**:
- Learning what violations look like
- Identifying violations in existing skills
- Understanding why certain patterns are wrong

---

## Quick Start

### Creating a New Skill

```bash
# 1. Copy the good example
cp -r examples/good-self-contained-skill/ your-new-skill/

# 2. Customize
cd your-new-skill/
# Edit SKILL.md - replace example content with your skill
# Edit metadata.json - update name, category, toolchain, etc.

# 3. Verify self-containment
grep -r "\.\\./" .  # Should be empty
cat metadata.json | jq '.requires'  # Should be [] or external packages only

# 4. Test in isolation
mkdir -p /tmp/skill-test
cp -r ../your-new-skill /tmp/skill-test/
cd /tmp/skill-test/your-new-skill
cat SKILL.md  # Should be complete and useful
```

### Fixing an Existing Skill

```bash
# 1. Identify violations
grep -r "\.\\./" existing-skill/  # Find relative paths
grep -r "from skills\." existing-skill/  # Find cross-skill imports
grep -i "requires.*skill" existing-skill/SKILL.md  # Find hard dependencies

# 2. Study the bad example
# See: examples/bad-interdependent-skill/
# Compare violations with your skill

# 3. Study the good example
# See: examples/good-self-contained-skill/
# Learn correct patterns to apply

# 4. Apply fixes
# - Remove relative paths
# - Inline essential content
# - Remove hard dependencies
# - Replace imports with inline implementations
# - Update metadata.json

# 5. Verify with checklist
# Use: docs/SKILL_CREATION_PR_CHECKLIST.md
```

---

## Comparison

| Aspect | Good Example | Bad Example |
|--------|--------------|-------------|
| **Purpose** | Template to copy | Anti-pattern to avoid |
| **Paths** | Skill names only | `../../other-skill/` |
| **Content** | Inlined patterns | "See other skill" |
| **Dependencies** | External packages only | Other skills listed |
| **Imports** | Self-contained | `from skills.X import` |
| **Examples** | Complete working code | Code fragments |
| **metadata.json** | `self_contained: true` | `self_contained: false` |
| **Deployment** | Works anywhere | Breaks in flat structure |

---

## Learning Path

### Step 1: Study Good Example
1. Read `good-self-contained-skill/SKILL.md`
2. Note how essential content is inlined
3. See complete working examples
4. Observe complementary skills section format
5. Check `metadata.json` structure

### Step 2: Study Bad Example
1. Read `bad-interdependent-skill/SKILL.md`
2. Identify each violation (marked with ❌)
3. Understand why each pattern is wrong
4. See the "How to Fix" sections
5. Compare with good example

### Step 3: Apply to Your Skills
1. Use [SKILL_CREATION_PR_CHECKLIST.md](../docs/SKILL_CREATION_PR_CHECKLIST.md)
2. Run verification commands
3. Copy good patterns, avoid bad patterns
4. Test in isolation
5. Submit PR with completed checklist

---

## Key Principles

### Self-Containment Means:

✅ **Complete**: All essential content inlined
✅ **Independent**: Works without other skills
✅ **Deployable**: Functions in any directory structure
✅ **Graceful**: Notes optional enhancements without requiring them
✅ **Testable**: Verifiable in isolation

### Self-Containment Does NOT Mean:

❌ Can't mention other skills (you can, informationally)
❌ Can't have references/ directory (you can, within skill)
❌ Can't be part of bundles (you can, optionally)
❌ Must duplicate ALL content (just essential patterns)
❌ Can't suggest complementary skills (you should!)

---

## Testing Your Skill

### Isolation Test (Required)

```bash
# Copy to isolated directory
mkdir -p /tmp/skill-test
cp -r your-skill /tmp/skill-test/

# Verify works standalone
cd /tmp/skill-test/your-skill
cat SKILL.md  # Complete content?
ls -la  # All files present?

# Should feel complete and useful
```

### Violation Detection (Required)

```bash
# Run all checks
cd your-skill

# Check 1: Relative paths
grep -r "\.\\./" .
# Expected: (empty)

# Check 2: Cross-skill imports
grep -r "from skills\." .
# Expected: (empty)

# Check 3: Hard dependencies
grep -i "requires.*skill\|must.*install" SKILL.md
# Expected: (empty or optional context only)

# Check 4: Metadata
cat metadata.json | jq '.requires'
# Expected: [] or external packages only

cat metadata.json | jq '.self_contained'
# Expected: true
```

---

## Resources

### Documentation
- **[SKILL_SELF_CONTAINMENT_STANDARD.md](../docs/SKILL_SELF_CONTAINMENT_STANDARD.md)**: Complete standard
- **[SKILL_CREATION_PR_CHECKLIST.md](../docs/SKILL_CREATION_PR_CHECKLIST.md)**: PR checklist template
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: General contribution guidelines

### Examples
- **[good-self-contained-skill/](good-self-contained-skill/)**: ✅ Copy this
- **[bad-interdependent-skill/](bad-interdependent-skill/)**: ❌ Avoid this

### Verification
```bash
# Quick verification script
cat > verify-skill.sh << 'EOF'
#!/bin/bash
SKILL_DIR=$1

echo "Verifying: $SKILL_DIR"
echo ""

echo "Check 1: Relative paths"
grep -r "\.\\./" "$SKILL_DIR" && echo "❌ FAIL" || echo "✅ PASS"

echo "Check 2: Cross-skill imports"
grep -r "from skills\." "$SKILL_DIR" && echo "❌ FAIL" || echo "✅ PASS"

echo "Check 3: Hard dependencies"
grep -i "requires.*skill" "$SKILL_DIR/SKILL.md" && echo "❌ FAIL" || echo "✅ PASS"

echo "Check 4: Metadata self_contained"
cat "$SKILL_DIR/metadata.json" | jq -e '.self_contained == true' > /dev/null && echo "✅ PASS" || echo "❌ FAIL"

echo ""
echo "If all checks PASS, skill is self-contained!"
EOF

chmod +x verify-skill.sh
./verify-skill.sh your-skill-name/
```

---

## FAQ

**Q: Should I copy the good example or bad example?**
A: Copy **good-self-contained-skill/** as your template. Study **bad-interdependent-skill/** to learn what to avoid.

**Q: Can I modify the good example?**
A: Yes! It's a template. Replace the example content with your skill's actual patterns and examples.

**Q: What if my skill needs another skill?**
A: Your skill doesn't need another SKILL - it needs the PATTERNS from that skill. Inline those patterns (20-50 lines).

**Q: How much content should I inline?**
A: Inline the 80% use case. Reference the 20% advanced cases as "if X skill deployed".

**Q: Can I reference other skills?**
A: Yes - as informational mentions using skill names only (no paths). Note they're optional enhancements.

---

## Summary

### ✅ Use This Example
**[good-self-contained-skill/](good-self-contained-skill/)**
- Complete template
- Proper self-containment
- Copy as starting point

### ❌ Avoid This Example
**[bad-interdependent-skill/](bad-interdependent-skill/)**
- Anti-pattern demonstration
- Shows violations
- Study to learn what NOT to do

### 📋 Follow This Process
1. Copy good example
2. Customize for your skill
3. Inline essential content
4. Test in isolation
5. Verify with checklist
6. Submit PR

---

**Questions?** See [SKILL_SELF_CONTAINMENT_STANDARD.md](../docs/SKILL_SELF_CONTAINMENT_STANDARD.md) or open an issue.
