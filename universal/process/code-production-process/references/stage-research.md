# Stage 1: Research — Detailed Protocol

## Purpose

The Research stage prevents "build from scratch" when an existing implementation
can be reused or extended. It also surfaces the codebase conventions the new code
must follow, so the engineer does not introduce a third pattern where two already exist.

## Agent and Tools

- **Agent:** `research`
- **Primary tools:**
  - `mcp__vector-indexer-mcp__search_hybrid` — semantic + lexical code search
  - `mcp__knowledge__kb_search` — KB entries for architecture decisions
  - `mcp__knowledge__search_local` — local document search
- **Secondary tools:** `Grep`, `Glob` for exact-string follow-up on vector results

## Dispatch Prompt Template

```
Research task for: [task description]

Perform the following searches and document findings:

1. Search the codebase for existing implementations of [domain concept]:
   - Use search_hybrid("[domain keywords]")
   - List file paths, function/class names, and what each does

2. Search KB for prior architectural decisions about [domain]:
   - Use kb_search("[domain] architecture")
   - Note any decisions that constrain the new implementation

3. Identify established patterns for [specific mechanism, e.g., async HTTP, DB access]:
   - Search for existing usage in the codebase
   - Identify which libraries/frameworks are already in use

4. List known edge cases from existing implementations

Output format:
- Section: "Existing Implementations Found" (paths + descriptions)
- Section: "Conventions to Follow" (patterns, naming, error handling)
- Section: "What Must Be Built New" (gaps research found)
- Section: "Edge Cases Noted"
- Section: "Input/Output Contracts Required"
```

## Gate Checklist

Before proceeding to Stage 2:

- [ ] Spec document is written (not just a list of search results)
- [ ] At least one existing codebase reference is cited (or "no prior implementation found" stated explicitly)
- [ ] Conventions section identifies naming patterns, error handling style, import style
- [ ] No implementation code appears in the research output

## TODO: Expand with domain-specific search strategies

<!-- TODO: Add example searches for common domains: async HTTP, database access, auth, file I/O -->
<!-- TODO: Add guidance on interpreting zero-result searches (new domain vs. wrong query) -->
<!-- TODO: Add checklist for reviewing external dependency usage patterns -->
