---
name: code-production-process
description: "Six-stage quality-gate pipeline for any code implementation task"
user-invocable: false
disable-model-invocation: true
license: Apache-2.0
compatibility: claude-code
progressive_disclosure:
  entry_point:
    summary: "6-stage gate pipeline (Research→Architect→Implement→Tests→Critic→Security). Hotfix path skips 1-2, mandatory 3-6. WARN proceeds with findings logged; BLOCK halts and returns to user — PM must NOT auto-retry without user direction."
    when_to_use: "When PM is about to dispatch an engineer for non-trivial implementation (>50 lines OR >1 source file touched). Also fires when engineer-dispatch produces .py/source file changes detected via git diff. EXCLUDE: docs edits, commit messages, config-only changes."
    quick_start: "1. MUST: dispatch Research before any engineer task. 2. MUST: Architect produces interface spec — NO implementation code. 3. Engineer implements + writes pytest. 3.5 MUST: pytest passes green — failing tests skip critic and return to engineer. 4. MUST: dispatch code-critic (isolated context — no implementer framing). 5. Verdict: APPROVE proceeds; WARN proceeds with findings logged to docs handoff; BLOCK halts and surfaces findings to user. 6. Security pass."
  references:
    - stage-research.md
    - stage-architect.md
    - stage-implement.md
    - stage-tests.md
    - stage-critic.md
    - stage-security.md
    - skip-rules.md
    - critic-isolation.md
---

# Code Production Process

## Overview

This skill implements a six-stage quality-gate pipeline that every non-trivial code implementation
task must pass through before being declared complete. The pipeline exists because the repository
owner cannot visually assess code quality — all quality assurance must therefore be enforced by
automated gates inside the agent pipeline itself, not by human review after the fact. Each stage
produces a concrete artifact and must clear a defined gate before the next stage may begin. No
stage may be skipped on the standard path. The critic agent operates with full context isolation
to prevent anchoring bias from the implementer's own framing. A deliberately adversarial review
catches issues that a cooperative pass-through would miss.

## Trigger Conditions

This skill loads when **any** of the following conditions are true:

**Explicit triggers (pre-dispatch):**
- PM is about to dispatch an engineer agent for a task that will produce >50 lines of source code
- PM is about to dispatch an engineer agent for a task that will touch >1 source file
- Task description contains implementation verbs: "implement", "write", "build", "create", "refactor", "add feature", "fix bug in [module]"

**Post-dispatch detection:**
- Engineer agent returns and `git diff --stat` shows source file changes (`.py`, `.ts`, `.js`, `.go`, `.rs`, `.java`, `.rb`, `.sh` with logic) regardless of stated task scope
- Engineer agent produces new files under `src/`, `lib/`, `app/`, `services/`, `api/` directories

**Explicit exclusions — do NOT trigger this pipeline for:**
- Documentation edits (`.md`, `.rst`, `.txt`, `.html` content-only)
- Commit messages, PR descriptions, changelogs
- Config-only changes (`*.yaml`, `*.toml`, `*.json`, `*.env` with no code logic)
- Single-line fixes with scope verified to be <5 lines
- Dependency version bumps with no code changes

**When in doubt:** err toward triggering the pipeline. A false positive costs one critic dispatch.
A false negative ships broken or insecure code.

## The 6-Stage Pipeline

Each stage has a defined agent, required output artifact, and a gate condition. The gate
condition must be satisfied before proceeding. Failing a gate returns to the current stage,
not to stage 1, unless the failure indicates a fundamental misunderstanding of requirements.

### Stage 1: Research

**Agent:** `research`

**Tools:** `mcp__vector-indexer-mcp__search_hybrid`, `mcp__knowledge__kb_search`,
`mcp__knowledge__search_local`

**What the agent does:**
- Searches the existing codebase for similar implementations that can be reused or extended
- Identifies existing abstractions, patterns, and conventions the implementation must follow
- Locates relevant KB entries covering architecture decisions, data models, API contracts
- Enumerates external dependencies and their established usage patterns in the codebase

**Required output artifact:** A written spec document (markdown) covering:
- What exists already (cite file paths and function names)
- What must be built new
- Which existing patterns the implementation must follow
- Input/output contracts the new code must satisfy
- Known edge cases from existing usage

**Gate:** Spec document exists and names at least one existing codebase reference. Research
agent MUST NOT produce implementation code. If no relevant existing code exists, the output
explicitly states "no prior implementation found" — this is a valid research finding, not a
failure.

**See:** `references/stage-research.md` for prompt templates and search strategy.

---

### Stage 2: Architect

**Agent:** `python-engineer` (in design mode — no implementation code produced)

**Skills loaded:** `software-patterns`

**What the agent does:**
- Reads the Stage 1 spec document
- Designs the public interface: class signatures, function signatures, data models, type annotations
- Specifies abstract base classes (ABCs) or Protocol classes where polymorphism is needed
- Documents invariants and preconditions for each public method
- Notes which external dependencies will be used and how

**Required output artifact:** An interface specification document containing:
- All public class/function signatures with full type annotations
- ABC or Protocol definitions (no method bodies — only `...` or `pass`)
- Data model schemas (Pydantic models, dataclasses, TypedDicts — no logic)
- Error types that will be raised and their hierarchy
- A one-paragraph statement of what the implementation will NOT do

**Gate:** Interface document exists. Zero implementation code (no function bodies with logic,
no algorithm steps, no I/O calls). The architect produces the contract; the engineer fills it.

**Important:** The `code-critic` agent may optionally be dispatched here to review the
interface design for API coherence before implementation begins. This is the Phase 2 design
critic pass. If dispatched, critic input is the interface document only — no code exists yet.

**See:** `references/stage-architect.md` for interface specification templates.

---

### Stage 3: Implement

**Agent:** `python-engineer`

**Skills loaded:** `software-patterns`, `asyncio` (if async code required), `pytest`

**What the agent does:**
- Implements the interface defined in Stage 2 exactly (no scope creep — flag to PM if interface
  needs amendment)
- Writes unit tests in `pytest` covering:
  - Happy path for each public function
  - Each documented error condition
  - At least one edge case per function
- Runs `mypy --strict` on the new code and resolves all type errors before declaring done
- Runs `pytest` locally and confirms all tests pass before returning

**Required output artifact:**
- Source file(s) implementing the Stage 2 interface
- Test file(s) with pytest tests
- `mypy --strict` output showing zero errors
- `pytest` output showing all tests passed

**Gate:** Engineer must provide mypy and pytest output with zero errors/failures before
returning to PM. If engineer cannot provide this output, the engineer did not finish — PM
must re-dispatch, not proceed to Stage 3.5.

**See:** `references/stage-implement.md` for implementation standards and self-check
checklist.

---

### Stage 3.5: Tests-Must-Pass Gate

**Agent:** PM (not an agent dispatch — PM evaluates the Stage 3 output directly)

**What PM does:**
- Inspects the pytest output artifact from Stage 3
- If pytest shows ANY failure: immediately return to Stage 3 engineer. Do NOT dispatch
  code-critic. Do NOT attempt to advance the pipeline. Failing tests mean implementation
  is incomplete.
- If pytest passes green (zero failures): proceed to Stage 4

**This gate is non-negotiable.** Dispatching code-critic against code with failing tests
wastes tokens on findings that may be artifacts of the broken state. The critic reviews
working code, not code under active repair.

**Failure return message to engineer (template):**
```
Tests failed. Return to Stage 3. Fix the following failures before requesting critic review:

[paste pytest output here]

When tests pass green, provide updated implementation + passing pytest output.
```

**See:** `references/stage-tests.md` for test quality requirements and coverage standards.

---

### Stage 4: Critic Review

**Agent:** `code-critic`

**Skills loaded:** `code-review-standards`, `code-production-process`

**Context isolation is mandatory.** See "Critic Isolation Rule" section below for full
requirements. Failure to isolate the critic context is a process violation.

**What the critic agent does:**
- Reviews the implementation against the Stage 2 interface specification
- Applies the `code-review-standards` severity-tagged checklist (CRITICAL/HIGH/MEDIUM/LOW)
- Produces a structured finding table with file+line citations for each finding
- Returns a top-level verdict: APPROVE, WARN, or BLOCK

**Required output artifact:**
- Verdict (APPROVE / WARN / BLOCK) stated at the top of response
- Finding table (may be empty for APPROVE) with columns: Severity | File | Line | Issue | Fix
- Summary paragraph explaining the verdict

**Gate:** Critic returns a verdict. PM acts on verdict per the Verdict Protocol below.

**See:** `references/stage-critic.md` for dispatch template and isolation checklist.

---

### Stage 5: Security

**Agent:** `security`

**Scope:** OWASP Top 10, secrets/credentials exposure, injection vulnerabilities (SQL, shell,
template), authentication and authorization bypass, arbitrary code execution paths, insecure
deserialization, cryptographic weaknesses.

**What the agent does:**
- Reviews the Stage 3 implementation for security vulnerabilities in the above scope
- Does NOT re-review for code style or structural issues (that is the critic's domain)
- Produces a finding list with severity (CRITICAL / HIGH / MEDIUM / LOW) and remediation

**Gate:** Zero security findings at CRITICAL or HIGH severity. MEDIUM findings are documented
and logged. LOW findings are noted. If CRITICAL or HIGH security findings are present, PM
halts and surfaces to user — same protocol as a critic BLOCK.

**See:** `references/stage-security.md` for security review scope and OWASP mapping.

---

## Critic Isolation Rule

The critic agent's verdict is only as independent as the context it receives. Anchoring bias
— where the reviewer unconsciously accepts the author's framing of what the code does — is
the primary failure mode of code review in multi-agent systems.

**The PM MUST construct the critic dispatch prompt to contain ONLY:**
1. The Stage 1 spec document (what was asked)
2. The Stage 2 interface specification (what was designed)
3. The Stage 3 implementation files (what was built)
4. The Stage 3 pytest output (test results)

**The PM MUST NOT include in the critic dispatch prompt:**
- The engineer's commit message
- The engineer's stated rationale or design notes from the implementation response
- Any summary the PM wrote about what the engineer did
- Phrases like "the engineer explained that..." or "according to the implementer..."

If the engineer's implementation response contains inline explanatory text mixed with code,
PM must extract only the code and test output for the critic dispatch — strip the
implementer's narration.

This rule exists because an engineer who writes "I chose this approach because the
alternative would have performance issues" subtly pre-argues against the critic raising
performance concerns. The critic must encounter the code cold.

**See:** `references/critic-isolation.md` for prompt construction templates.

## Verdict Protocol

PM behavior is fully determined by the critic's top-level verdict. PM MUST NOT use judgment
to override or soften the verdict protocol.

**APPROVE** (zero CRITICAL findings, zero HIGH findings):
- Proceed to Stage 5 (Security)
- No additional action required from engineer
- Finding table (if non-empty, containing only MEDIUM/LOW) is passed to the Documentation
  agent handoff as "notes for future reference"

**WARN** (zero CRITICAL findings, one or more HIGH findings):
- Proceed to Stage 5 (Security) — do NOT halt the pipeline
- PM MUST append the full critic finding table to the handoff message sent to the
  Documentation agent
- PM MUST log the findings in a note (KB entry or todo comment) for tracking
- PM MUST NOT silently discard HIGH findings — they must be surfaced somewhere

**BLOCK** (any CRITICAL finding):
- PM halts the pipeline immediately
- PM surfaces the critic finding table verbatim to the user
- PM states: "Critic has blocked this implementation. The following CRITICAL issues must be
  resolved before the pipeline can continue. Please confirm your direction."
- PM awaits explicit user direction: fix-and-retry, override with justification, or abandon
- PM MUST NOT auto-re-delegate to engineer without user input
- When user directs fix-and-retry: return to Stage 3 (Implement) with the critic finding
  table as an additional input. The architect interface from Stage 2 remains authoritative
  unless the CRITICAL finding reveals a fundamental interface design flaw, in which case
  PM returns to Stage 2.

## Skip Rules (Hotfix Path)

The following rules define when stages may be skipped. **Stages 3 through 5 are NEVER
skippable regardless of path.**

**Standard path:** All 6 stages. Required for all new features, refactors >100 lines, any
change to authentication/authorization code, any change to data models.

**Hotfix path:** Stages 1 and 2 may be skipped when ALL of the following are true:
- The bug being fixed is confirmed in production (not a hypothetical or local-only failure)
- The fix scope is verified to be ≤20 lines of net new code across ≤2 files
- The fix does NOT touch authentication, authorization, cryptography, or data serialization
- PM explicitly notes "hotfix path" in the session log

Even on the hotfix path: Stage 3 (Implement + Tests), Stage 3.5 (Tests-Must-Pass Gate),
Stage 4 (Critic), and Stage 5 (Security) are mandatory and cannot be skipped.

**Documentation-only path:** If ALL changes are confirmed to be documentation, configuration
values, or dependency version bumps with no logic changes — all 6 stages are skipped.
PM should verify via `git diff --stat` that no source files were modified.

**See:** `references/skip-rules.md` for skip rule decision tree and examples.

## Failure Loop Protocol

When a stage gate fails, the finding returns to the responsible agent in a structured format.
PM does not attempt to interpret or patch the finding — PM passes it verbatim.

**Format for returning to engineer after BLOCK:**

```
PIPELINE GATE FAILURE — Return to Stage [N]

Critic verdict: BLOCK
Findings (CRITICAL):

| Severity | File | Line | Issue | Required Fix |
|----------|------|------|-------|--------------|
[paste finding table verbatim]

Instructions:
- Fix ALL CRITICAL items above
- Re-run pytest (must pass green)
- Re-run mypy --strict (must pass)
- Return updated implementation with fresh test output

Do NOT return until all CRITICAL findings are resolved and tests pass.
```

**Format for returning to engineer after WARN (if user requests fixes):**

```
PIPELINE GATE — WARN findings for review

Critic verdict: WARN
Pipeline proceeded, but the following HIGH findings were logged:

| Severity | File | Line | Issue | Recommended Fix |
|----------|------|------|-------|-----------------|
[paste finding table]

These were noted in the documentation handoff. If you choose to address them in this session,
re-run tests and confirm they still pass. No re-critic required for WARN resolutions.
```

## Token Efficiency Note

Stages 1 and 2 are lightweight by design. Research and Architect agents operate primarily on
text documents (specs, KB entries, interface files) rather than large codebases. The majority
of token spend occurs in Stages 3-5, where the implementation, tests, critic review, and
security review all operate on the full codebase context. Dispatching Research and Architect
first ensures that Stage 3 (Implement) receives a clear spec and does not require iterative
clarification, reducing the number of engineer re-dispatches — which is the primary source
of token waste in unstructured implementation workflows.
