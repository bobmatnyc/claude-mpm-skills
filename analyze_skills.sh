#!/bin/bash
# Claude Code Skills Compliance Analysis Script

echo "# CLAUDE CODE SKILLS COMPLIANCE ANALYSIS"
echo "# Generated: $(date)"
echo ""

TOTAL=0
YAML_PRESENT=0
YAML_MISSING=0
HAS_NAME=0
HAS_DESCRIPTION=0
CROSS_REFS=0
RELATIVE_PATHS=0

echo "## 1. YAML FRONTMATTER ANALYSIS"
echo ""
echo "Skill | Has YAML | Has Name | Has Description | Status"
echo "------|----------|----------|-----------------|-------"

find toolchains universal -name "SKILL.md" | while read skill; do
    TOTAL=$((TOTAL + 1))
    skill_name=$(dirname "$skill")

    # Check for YAML frontmatter
    if head -1 "$skill" | grep -q "^---$"; then
        YAML_PRESENT=$((YAML_PRESENT + 1))
        yaml_status="✅"

        # Check for name field
        if grep -q "^name:" "$skill"; then
            HAS_NAME=$((HAS_NAME + 1))
            name_status="✅"
        else
            name_status="❌"
        fi

        # Check for description field
        if grep -q "^description:" "$skill"; then
            HAS_DESCRIPTION=$((HAS_DESCRIPTION + 1))
            desc_status="✅"
        else
            desc_status="❌"
        fi
    else
        YAML_MISSING=$((YAML_MISSING + 1))
        yaml_status="❌"
        name_status="❌"
        desc_status="❌"
    fi

    if [ "$yaml_status" = "✅" ] && [ "$name_status" = "✅" ] && [ "$desc_status" = "✅" ]; then
        overall="✅ OK"
    else
        overall="❌ ISSUES"
    fi

    echo "$skill_name | $yaml_status | $name_status | $desc_status | $overall"
done

echo ""
echo "## 2. CROSS-REFERENCE ANALYSIS"
echo ""
echo "Checking for relative paths (../) that would break in flat deployment:"
echo ""

find toolchains universal -name "SKILL.md" -o -name "*.md" | while read f; do
    if grep -q "\.\\./" "$f" 2>/dev/null; then
        echo "❌ $f contains relative paths:"
        grep -n "\.\\./" "$f" | head -5
        echo ""
    fi
done

echo ""
echo "## 3. CROSS-SKILL IMPORT ANALYSIS"
echo ""
echo "Checking for imports from other skills:"
echo ""

find toolchains universal -name "SKILL.md" | while read f; do
    if grep -q "from skills\." "$f" 2>/dev/null; then
        echo "❌ $f contains cross-skill imports:"
        grep -n "from skills\." "$f"
        echo ""
    fi
done

echo ""
echo "## 4. SUMMARY STATISTICS"
echo ""
total=$(find toolchains universal -name "SKILL.md" | wc -l | tr -d ' ')
echo "Total skills analyzed: $total"
