# Skill Dependency Graph

**Generated**: 2025-11-30
**Purpose**: Visualize inter-skill dependencies for bundling strategy

---

## Legend

```
[Skill] ──────> [Referenced Skill]  (Hard dependency)
[Skill] - - - > [Referenced Skill]  (Soft reference)
[Parent] ═════> [Child]             (Hierarchical)
```

---

## Python Ecosystem Dependencies

### Python Testing Cluster (Should Bundle)

```
┌─────────────────────────────────────────────────────────┐
│ Python Testing Stack                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [pytest] ──────────────────────┐                     │
│      │                            │                      │
│      ├────────────> [fastapi-local-dev]                │
│      │                            ↑                      │
│      └──┐                         │                      │
│         │                         │                      │
│   [asyncio] ───────────────────┐ │                      │
│      │                          │ │                      │
│      └──────────> [fastapi-local-dev]                  │
│                                  │                       │
│   [pydantic] ────────────────────┘                      │
│      │                                                   │
│      ├────────────> [sqlalchemy]                        │
│      └────────────> [django]                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
            │
            └─────────────────────────────────────┐
                                                  ↓
┌─────────────────────────────────────────────────────────┐
│ Universal Skills (Always Deploy)                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [test-driven-development] <──── [pytest]             │
│            ↑                       [vitest]             │
│            │                       [jest]               │
│            │                                            │
│   [systematic-debugging] <────────[pytest]             │
│                                   [asyncio]            │
│                                   [root-cause-tracing] │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Bundle Recommendation**:
- **python-testing-stack**: pytest + asyncio + TDD (inlined summary)
- **python-frameworks**: fastapi-local-dev + flask + django
- **python-data**: pydantic + sqlalchemy

---

## TypeScript Ecosystem Dependencies

### TypeScript Testing Cluster

```
┌─────────────────────────────────────────────────────────┐
│ TypeScript Testing Stack                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [jest] ─────────────────┐                            │
│      │                     │                            │
│      ├──────> [typescript-core]                        │
│      │                     ↑                            │
│      └──────> [react] ────┘                            │
│                                                         │
│   [vitest] ───────────────┐                            │
│      │                     │                            │
│      ├──────> [typescript-core]                        │
│      ├──────> [react]                                  │
│      └──────> [test-driven-development] (universal)   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Bundle Recommendation**:
- **typescript-testing-stack**: jest + vitest + typescript-core
- **react-ecosystem**: react + react/state-machine + testing patterns

---

### TypeScript Data Cluster

```
┌─────────────────────────────────────────────────────────┐
│ TypeScript Data Stack                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [kysely] ────────────────┐                           │
│      │                      │                           │
│      ├──────> [typescript-core]                        │
│      │                      │                           │
│      └──────> [database-migration] (universal)         │
│                                                         │
│   [drizzle] - - - - - - - > [kysely] (comparison)     │
│   [prisma] - - - - - - - > [drizzle] (comparison)     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Bundle Recommendation**:
- **typescript-data-stack**: kysely + drizzle + prisma + migrations

---

## JavaScript Ecosystem Dependencies

### React Framework Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│ React Ecosystem                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [react] ═══════════════════════════════════════════> │
│      ║                                                  │
│      ╠═══════> [react/state-machine] (child)           │
│      ║                                                  │
│      ║                                                  │
│   [jest] ──────────> [react] <────────── [vitest]     │
│      │                  ↑                      │        │
│      │                  │                      │        │
│      └──────────────────┴──────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Bundle Recommendation**:
- **react-ecosystem**: react + state-machine + testing integration

---

## Cross-Language Dependencies

### Multi-Toolchain References

```
┌─────────────────────────────────────────────────────────┐
│ AI/MCP Protocol Stack                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [mcp] ──────────────────────┐                        │
│      │                         │                        │
│      ├──────> [typescript-core] (TypeScript impl)      │
│      ├──────> [python-core]     (Python impl)          │
│      └──────> [openrouter]      (Alternative API)      │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ PHP/WordPress → Python Testing                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [wordpress/testing-qa] - - - > [pytest] (Python)     │
│                          - - - > [github-actions]      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Bundle Recommendation**:
- **mcp-development**: mcp + typescript-core (inline Python patterns)
- **wordpress-stack**: Keep separate, soft refs only

---

## Universal Skills Web

### Core Universal Dependencies

```
┌─────────────────────────────────────────────────────────┐
│ Universal Skills (Always Deployed)                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [systematic-debugging]                                │
│         ↑                                               │
│         │                                               │
│         │                                               │
│   [root-cause-tracing] ────> [systematic-debugging]    │
│         │                         ↑                     │
│         │                         │                     │
│         └──────> [defense-in-depth] (pattern)          │
│                                                         │
│   [test-driven-development]                             │
│         ↑                                               │
│         │                                               │
│   [testing-anti-patterns] ──> [test-driven-development]│
│                           ──> [verification-*]          │
│                                                         │
│   [verification-before-completion]                      │
│         ↑                                               │
│         │                                               │
│         └──────── [All testing skills reference]       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Deployment**: Always deploy as individual skills (not bundled)

---

## Dependency Metrics

### Hub Skills (Most Referenced)

| Skill | Inbound References | Type | Should Bundle? |
|-------|-------------------|------|----------------|
| test-driven-development | 8+ | Universal | No - always deploy |
| systematic-debugging | 6+ | Universal | No - always deploy |
| typescript-core | 4 | Toolchain | Yes - with TS stack |
| fastapi-local-dev | 3 | Toolchain | Yes - with Python stack |
| react | 3 | Framework | Yes - with React ecosystem |

### Isolated Skills (No Dependencies)

**Count**: 60 skills (69%)
**Examples**:
- skill-creator
- git-workflow
- brainstorming
- condition-based-waiting
- env-manager
- stacked-prs
- etc.

**Recommendation**: These already meet self-containment requirements

---

## Bundling Strategy Visual

### Deployment Structure (Proposed)

```
User runs Claude Code in project
        ↓
┌───────────────────────────────────────┐
│ Toolchain Detection                   │
└───────────────────────────────────────┘
        ↓
    Detects: Python + React
        ↓
┌───────────────────────────────────────┐
│ Deploy These Bundles:                 │
├───────────────────────────────────────┤
│                                       │
│ ✅ python-testing-stack/              │
│    ├─ pytest.md                       │
│    ├─ asyncio.md                      │
│    └─ tdd-summary.md (inlined)        │
│                                       │
│ ✅ python-frameworks/                 │
│    ├─ fastapi-local-dev.md            │
│    ├─ flask.md                        │
│    └─ django.md                       │
│                                       │
│ ✅ react-ecosystem/                   │
│    ├─ react-core.md                   │
│    ├─ state-machine.md                │
│    └─ testing-patterns.md             │
│                                       │
│ ✅ universal/ (individual skills)     │
│    ├─ test-driven-development/        │
│    ├─ systematic-debugging/           │
│    ├─ verification-before-completion/ │
│    └─ condition-based-waiting/        │
│                                       │
└───────────────────────────────────────┘
        ↓
    All skills work standalone
    Cross-references intact within bundles
    Universal skills always available
```

---

## Critical Paths to Fix

### Priority 1 (Breaks Deployment)

```
[pydantic] ──> [fastapi] ❌ Hard path dependency
[pytest] ──> [../../../../universal/test-driven-development/] ❌ Deep cross-tree
[vitest] ──> [../../../../universal/test-driven-development/SKILL.md] ❌ Deepest path
[jest] ──> [../../../javascript/frameworks/react/SKILL.md] ❌ Complex navigation
```

**Fix**: Convert to skill name mentions + inline essential content

---

### Priority 2 (Informational Only)

```
[wordpress/testing-qa] - - > [pytest] ℹ️ Cross-language suggestion
[mypy] - - > [pytest, fastapi, pydantic] ℹ️ Ecosystem hints
[testing-anti-patterns] - - > [test-driven-development] ℹ️ Conceptual link
```

**Fix**: Already safe, but standardize format

---

## Circular Dependencies Check

### Analysis: NO CIRCULAR DEPENDENCIES FOUND ✅

All references flow in these directions:
- **Toolchain → Universal** (pytest → TDD)
- **Specific → General** (jest → typescript-core)
- **Child → Parent** (state-machine → react)

**No skill references back to its referencer** ✅

---

## Summary

**Total Unique Dependencies**: 23 hard links + 35 soft mentions
**Strongly Connected Components**: 0 (no circular deps)
**Hub Nodes**: test-driven-development (8 refs), systematic-debugging (6 refs)
**Leaf Nodes**: 60 skills with zero outbound refs
**Max Depth**: 4 levels (../../../../universal/...)

**Bundling Reduces Complexity**:
- Before: 87 individual skills with 23 hard cross-refs
- After: ~15 bundles + 60 standalone skills with 0 hard cross-refs

---

**See Also**:
- [Full Analysis Report](./inter-skill-references-analysis-2025-11-30.md)
- [Executive Summary](./inter-skill-references-summary.md)
- [Reference Catalog (CSV)](./inter-skill-references-catalog.csv)
