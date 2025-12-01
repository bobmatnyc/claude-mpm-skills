# Anthropic Skills Repository Structure Analysis
**Date:** 2025-11-30  
**Researcher:** Claude Research Agent  
**Purpose:** Compare official Anthropic skills structure with claude-mpm-skills implementation

## Executive Summary

After comprehensive analysis of Anthropic's official skills repository and our claude-mpm-skills implementation, key differences have been identified:

**Anthropic's Approach:**
- Minimal required structure (skill directory + SKILL.md)
- Supporting files (examples/, scripts/) as separate directories
- Actual code samples in dedicated .py/.js files
- Inline code blocks primarily for demonstration/snippets

**Our Current Approach:**
- Extended structure with references/ directories
- Heavy use of inline code blocks (80-160 per SKILL.md file)
- Separation of documentation into references/*.md files
- No separate code sample files (.py, .js, .ts)

## Detailed Findings

### 1. Anthropic Official Repository Structure

#### Repository Organization
```
anthropics/skills/
├── .claude-plugin/
├── algorithmic-art/
├── brand-guidelines/
├── canvas-design/
├── document-skills/          # Special: Contains subdirectories
│   ├── docx/
│   ├── pdf/
│   ├── pptx/
│   └── xlsx/
├── frontend-design/
├── internal-comms/
├── mcp-builder/
├── skill-creator/
├── slack-gif-creator/
├── template-skill/            # Reference implementation
├── theme-factory/
├── web-artifacts-builder/
├── webapp-testing/            # Example analyzed in detail
├── .gitignore
├── README.md
├── THIRD_PARTY_NOTICES.md
└── agent_skills_spec.md       # Official specification
```

#### Individual Skill Structure Patterns

**Pattern 1: Minimal (Most Common)**
```
skill-name/
├── SKILL.md                   # Required
└── LICENSE.txt                # Optional
```

**Pattern 2: With Supporting Code**
```
document-skills/xlsx/
├── SKILL.md                   # Main documentation
├── recalc.py                  # Utility script
└── LICENSE.txt                # License
```

**Pattern 3: With Examples and Scripts**
```
webapp-testing/
├── examples/                  # Demonstration code
│   ├── console_logging.py
│   ├── element_discovery.py
│   └── static_html_automation.py
├── scripts/                   # Utility scripts
│   └── with_server.py
├── SKILL.md                   # Main documentation
└── LICENSE.txt                # License
```

#### SKILL.md Structure

**Required Elements:**
```yaml
---
name: skill-name              # Must match directory name
description: Complete explanation of functionality and when to use
---

# Markdown content (no restrictions)
```

**Optional Frontmatter:**
- `license`: License name or reference
- `allowed-tools`: Pre-approved tool list (Claude Code only)
- `metadata`: Custom key-value pairs

**Content Organization:**
- Instructions and guidelines in markdown
- Inline code blocks for **snippets and demonstrations**
- References to separate files for **actual runnable code**
- No restrictions on markdown body structure

### 2. Claude MPM Skills Current Structure

#### Repository Organization
```
claude-mpm-skills/
├── toolchains/               # Language/framework-specific
│   ├── python/
│   ├── typescript/
│   ├── javascript/
│   ├── php/
│   ├── ui/
│   ├── platforms/
│   ├── universal/
│   └── ai/
├── universal/                # Cross-cutting concerns
│   ├── collaboration/
│   ├── debugging/
│   ├── testing/
│   ├── architecture/
│   ├── security/
│   ├── web/
│   ├── infrastructure/
│   ├── data/
│   └── main/
├── docs/
├── .claude-mpm/
├── manifest.json
├── README.md
└── STRUCTURE.md
```

#### Individual Skill Structure Pattern

**Current Pattern (20 out of 87 skills):**
```
skill-name/
├── SKILL.md                   # Main skill file (large, 1000-2500 lines)
├── metadata.json              # Skill metadata
└── references/                # Supporting documentation
    ├── examples.md
    ├── workflow.md
    ├── anti-patterns.md
    ├── troubleshooting.md
    └── integration.md
```

**Standard Pattern (67 out of 87 skills):**
```
skill-name/
├── SKILL.md                   # Main skill file (large, 1000-2500 lines)
└── metadata.json              # Skill metadata
```

#### Code Block Analysis

**Django Skill:**
- Total lines: ~1,600
- Code blocks: 86 (43 opening + 43 closing backticks)
- All code inline in SKILL.md
- No separate .py files for runnable examples

**FastAPI Skill:**
- Total lines: ~1,200
- Code blocks: 160 (80 opening + 80 closing backticks)
- All code inline in SKILL.md
- No separate .py files for runnable examples

**LangGraph Skill:**
- Total lines: 2,432 (largest)
- Extensive inline code examples
- No separate code files

#### Key Observations

1. **No Code Sample Files**: Zero .py, .js, or .ts files found in any skill
2. **Heavy Inline Code**: 40-80 code blocks per large skill
3. **References Pattern**: 20 skills use references/ for extended documentation
4. **Metadata Extension**: All skills have metadata.json (not in Anthropic spec)

### 3. Gap Analysis

#### Structural Differences

| Aspect | Anthropic Official | Claude MPM Skills | Gap/Issue |
|--------|-------------------|-------------------|-----------|
| Code Samples | Separate .py/.js files in examples/ | Inline code blocks only | ❌ Missing separate runnable examples |
| Utility Scripts | Separate scripts/ directory | None | ❌ Missing utility scripts directory |
| Documentation | Primarily in SKILL.md | Split across SKILL.md + references/*.md | ⚠️ Different organization approach |
| File Size | Lean SKILL.md (300-800 lines) | Large SKILL.md (1000-2500 lines) | ⚠️ Our files are 2-3x larger |
| Code Block Count | 10-30 snippets per SKILL.md | 40-160 blocks per SKILL.md | ⚠️ Heavy embedding approach |
| Metadata | Minimal frontmatter | metadata.json + extended frontmatter | ✓ Enhanced metadata (acceptable) |

#### Specific Examples of Gaps

**Example 1: Django Skill**
- **Current**: 1,600 lines, 86 code blocks, all inline
- **Should be**: 
  ```
  django/
  ├── SKILL.md                 # Core patterns, 400-600 lines
  ├── examples/
  │   ├── project_setup.py
  │   ├── model_example.py
  │   ├── view_patterns.py
  │   ├── form_handling.py
  │   └── rest_api.py
  └── scripts/
      └── quick_start.sh
  ```

**Example 2: Test-Driven Development**
- **Current**: All language examples inline in SKILL.md
- **Should be**:
  ```
  test-driven-development/
  ├── SKILL.md                 # TDD principles and patterns
  ├── references/              # Keep current structure
  │   ├── examples.md
  │   ├── workflow.md
  │   └── anti-patterns.md
  └── examples/                # NEW: Add runnable examples
      ├── python_tdd_example/
      │   ├── test_calculator.py
      │   └── calculator.py
      ├── javascript_tdd_example/
      │   ├── calculator.test.js
      │   └── calculator.js
      └── go_tdd_example/
          ├── calculator_test.go
          └── calculator.go
  ```

**Example 3: FastAPI Local Dev**
- **Current**: 1,200 lines, 160 code blocks
- **Should be**:
  ```
  fastapi-local-dev/
  ├── SKILL.md                 # Core concepts, 500-700 lines
  ├── examples/
  │   ├── basic_app/
  │   │   ├── main.py
  │   │   ├── models.py
  │   │   └── requirements.txt
  │   ├── async_database/
  │   │   ├── main.py
  │   │   ├── database.py
  │   │   └── models.py
  │   └── testing_example/
  │       ├── test_api.py
  │       └── conftest.py
  └── scripts/
      ├── dev_setup.sh
      └── run_with_reload.sh
  ```

### 4. Benefits of Anthropic's Approach

#### Advantages

1. **Runnable Examples**
   - Users can copy entire working examples
   - Can be tested independently
   - Serve as project templates

2. **Reduced Token Usage**
   - SKILL.md focuses on concepts and patterns
   - Code samples loaded on demand
   - Smaller context window consumption

3. **Better Organization**
   - Clear separation: docs vs. code
   - Examples directory is self-documenting
   - Scripts directory for utilities

4. **Easier Maintenance**
   - Update code samples without touching docs
   - Test examples independently
   - Version control friendly (separate file diffs)

5. **User Experience**
   - Quick reference in SKILL.md
   - Deep dive with examples when needed
   - Copy-paste ready project starters

#### Current Approach Drawbacks

1. **Bloated SKILL.md Files**
   - 2-3x larger than necessary
   - High token consumption on skill load
   - Difficult to navigate

2. **Non-Runnable Code**
   - Snippets are educational only
   - Can't be executed directly
   - No way to verify they work

3. **Maintenance Burden**
   - Code embedded in docs
   - Changes require doc updates
   - Harder to test code accuracy

### 5. Alignment Recommendations

#### Priority 1: High-Value Skills (Immediate Action)

**Criteria:**
- Large SKILL.md files (>1,500 lines)
- High code block count (>60 blocks)
- Framework/toolchain skills with clear example patterns

**Skills to Restructure First:**

1. **langgraph/** (2,432 lines)
   - Extract graph examples
   - Create working agent examples
   - Add utility scripts for testing

2. **django/** (1,600 lines, 86 blocks)
   - Extract project setup examples
   - Create model/view/template examples
   - Add quick start script

3. **fastapi-local-dev/** (1,200 lines, 160 blocks)
   - Extract API endpoint examples
   - Create async database examples
   - Add development setup scripts

4. **tanstack-query/** (2,397 lines)
   - Extract query examples
   - Create mutation patterns
   - Add optimization examples

5. **graphql/** (2,311 lines)
   - Extract schema examples
   - Create resolver patterns
   - Add client examples

#### Priority 2: Universal Skills (Secondary)

**Skills:**
- test-driven-development/
- systematic-debugging/
- web-performance-optimization/
- dispatching-parallel-agents/

**Approach:**
- Keep references/ structure (working well)
- Add examples/ for multi-language runnable code
- Keep SKILL.md focused on principles

#### Priority 3: Simple Skills (No Change Needed)

**Skills:**
- Skills with <800 lines
- Skills with <30 code blocks
- Skills focused on concepts over code

**Examples:**
- git-workflow/
- brainstorming/
- writing-plans/
- env-manager/

### 6. Implementation Strategy

#### Phase 1: Template Creation (Week 1)

**Create skill structure templates:**

**Template A: Framework Skill with Examples**
```
framework-name/
├── SKILL.md                   # Core concepts (400-800 lines)
├── metadata.json              # Keep current metadata
├── examples/                  # NEW
│   ├── basic/                 # Simple starter
│   ├── intermediate/          # Common patterns
│   └── advanced/              # Complex scenarios
└── scripts/                   # NEW
    ├── setup.sh               # Environment setup
    └── run_example.sh         # Quick test
```

**Template B: Multi-Language Skill**
```
skill-name/
├── SKILL.md                   # Core principles
├── metadata.json
├── references/                # Keep existing
│   └── *.md
└── examples/                  # NEW
    ├── python/
    ├── javascript/
    ├── typescript/
    └── go/
```

#### Phase 2: Pilot Restructuring (Week 2)

**Select 3 skills for pilot:**
1. django/ (large, clear examples)
2. fastapi-local-dev/ (high value)
3. test-driven-development/ (multi-language)

**Process:**
1. Create examples/ directory
2. Extract inline code to separate files
3. Slim down SKILL.md (remove redundant code)
4. Add README.md in examples/ explaining structure
5. Test examples independently
6. Update SKILL.md to reference examples

#### Phase 3: Bulk Restructuring (Weeks 3-4)

**Batch process remaining high-priority skills:**
- Create examples/ directories
- Extract code samples
- Update documentation references
- Add utility scripts where applicable

#### Phase 4: Validation and Documentation (Week 5)

**Quality checks:**
- Verify all examples run correctly
- Test scripts work as documented
- Update STRUCTURE.md
- Update README.md with new patterns

**Documentation:**
- Add examples/README.md to each skill
- Document example usage in SKILL.md
- Create migration guide for contributors

### 7. File Organization Standards

#### SKILL.md Content Guidelines

**What should be in SKILL.md:**
- Conceptual explanations
- Design patterns and principles
- When/why to use the skill
- Quick reference snippets (5-15 lines max)
- Links to examples and scripts
- Architecture diagrams (ASCII or markdown)
- Best practices and anti-patterns

**What should be in separate files:**
- Complete working examples (>20 lines)
- Full application templates
- Configuration files
- Utility scripts
- Multi-file examples (projects)

#### Naming Conventions

**Examples directory:**
```
examples/
├── 01_basic/                  # Numbered for progression
├── 02_intermediate/
├── 03_advanced/
├── use_case_auth/             # Or named by use case
└── use_case_testing/
```

**Scripts directory:**
```
scripts/
├── setup.sh                   # Environment setup
├── run_tests.sh               # Testing utilities
├── dev_server.sh              # Development helpers
└── utils/                     # Supporting utilities
    └── helper.py
```

**References directory (keep current):**
```
references/
├── examples.md                # Example walkthroughs
├── workflow.md                # Process documentation
├── anti-patterns.md           # What to avoid
├── troubleshooting.md         # Common issues
└── integration.md             # Integration guides
```

#### File Size Targets

**SKILL.md:**
- Simple skills: 200-500 lines
- Framework skills: 400-800 lines
- Complex skills: 800-1,200 lines (max)
- Universal skills: 600-1,000 lines

**Code blocks in SKILL.md:**
- Snippets only: 5-15 lines each
- Maximum 20-30 code blocks
- For longer code: reference separate file

### 8. Migration Checklist

#### Per-Skill Migration

- [ ] Analyze SKILL.md for extractable code
- [ ] Create examples/ directory
- [ ] Extract inline code to separate files
- [ ] Organize examples by complexity or use case
- [ ] Create scripts/ if utilities needed
- [ ] Update SKILL.md to reference external files
- [ ] Add examples/README.md with usage
- [ ] Test all examples independently
- [ ] Update metadata.json if needed
- [ ] Document in STRUCTURE.md

#### Quality Gates

- [ ] All examples run without errors
- [ ] SKILL.md reduced by 30-50%
- [ ] Examples have clear README
- [ ] Scripts are executable and documented
- [ ] No broken references in SKILL.md
- [ ] Progressive disclosure maintained

## Conclusion

**Key Takeaways:**

1. **Anthropic's approach is superior for:**
   - Runnable examples
   - Token efficiency
   - Maintainability
   - User experience

2. **Our current approach has value in:**
   - Rich documentation (references/)
   - Enhanced metadata
   - Detailed explanations

3. **Hybrid approach recommended:**
   - Keep references/ pattern (our innovation)
   - Add examples/ pattern (Anthropic's approach)
   - Add scripts/ pattern (Anthropic's approach)
   - Slim down SKILL.md (align with Anthropic)

4. **Impact:**
   - 25 skills need restructuring (large framework skills)
   - 20 skills need examples/ added (multi-language skills)
   - 42 skills are fine as-is (concept-focused, small)

5. **Timeline:**
   - Pilot: 1 week (3 skills)
   - Bulk restructuring: 2 weeks (22 skills)
   - Validation: 1 week
   - Total: 4-5 weeks

**Next Steps:**
1. Review and approve restructuring plan
2. Create templates for examples/ and scripts/
3. Start pilot with django/, fastapi-local-dev/, test-driven-development/
4. Document learnings and refine process
5. Batch process remaining skills

---

**Research Metadata:**
- Files analyzed: 87 SKILL.md files
- External repositories examined: 1 (anthropics/skills)
- Skills with references/: 20
- Skills needing restructuring: 25
- Average SKILL.md size: 900 lines
- Target SKILL.md size: 500 lines
