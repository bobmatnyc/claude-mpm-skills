---
name: systematic-debugging
description: "Step-by-step debugging workflow: reproduce the bug, isolate the failing component, trace to root cause, apply a targeted fix, and verify the fix resolves the issue without regressions. Use when you encounter a bug, error, exception, crash, or unexpected behavior that needs troubleshooting."
user-invocable: false
disable-model-invocation: true
license: Apache-2.0
compatibility: claude-code
progressive_disclosure:
  entry_point:
    summary: "Systematic debugging methodology emphasizing root cause analysis over quick fixes"
    when_to_use: "When debugging issues, tracing errors, fixing bugs, troubleshooting crashes, investigating exceptions, or diagnosing 'not working' reports."
    quick_start: "1. Reproduce the bug reliably. 2. Isolate the failing component. 3. Trace to root cause. 4. Fix at root cause. 5. Verify fix + no regressions."
  references:
    - workflow.md
    - anti-patterns.md
    - examples.md
    - troubleshooting.md
---
# Systematic Debugging

## When to Use

- A bug, error, exception, or crash needs investigation
- Something is "not working" and the cause is unclear
- A test is failing and the reason isn't obvious
- You need to troubleshoot unexpected behavior in any language or framework

## Core Workflow

Follow these five phases sequentially. Do not skip ahead to fixing before completing isolation and tracing.

### Phase 1: Reproduce

Establish a reliable way to trigger the bug before doing anything else.

1. Read the full error message, stack trace, and logs — note exact text, line numbers, and error codes
2. Create a minimal reproduction case that triggers the issue consistently
3. Record the exact steps, inputs, and environment that cause the failure

**Checkpoint:** Can you trigger the bug on demand? If intermittent, gather more data before proceeding.

### Phase 2: Isolate

Narrow down where the failure originates.

1. Use binary search to find the failing component — disable or stub out halves of the system
2. Check recent changes with `git log --oneline -20` and `git diff` against the last known good state
3. Add targeted logging or use a debugger to observe state at key boundaries

```bash
# Find which commit introduced the bug
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Git will checkout midpoints — test each one and mark good/bad
```

**Checkpoint:** You can point to a specific function, module, or data flow where the bug lives.

### Phase 3: Trace to Root Cause

Understand *why* the failure happens — not just *where*.

1. Read the code path completely from entry point through the failure site
2. Check assumptions: what does each function expect vs. what it actually receives?
3. Trace data flow backward — where does the bad value originate?
4. Verify with evidence: add assertions or print statements to confirm your hypothesis

```python
# Example: verify assumptions about incoming data
def process_order(order):
    assert order.status == "pending", f"Expected pending, got {order.status}"
    assert order.items, "Order has no items"
    # ... rest of processing
```

**Checkpoint:** You can explain the chain of causation from trigger to symptom, and you have evidence (logs, assertions, debugger output) supporting your explanation.

### Phase 4: Fix at Root Cause

Apply a targeted fix that addresses the actual cause, not just the symptom.

1. Fix the root cause, not a downstream effect
2. Keep the fix minimal — change only what's necessary
3. Avoid "band-aid" fixes that mask the underlying problem (e.g., adding a try/except around a crash without fixing why it crashes)

### Phase 5: Verify

Confirm the fix works and doesn't introduce regressions.

1. Run the reproduction case from Phase 1 — confirm the bug is gone
2. Run the full test suite to check for regressions
3. Test edge cases related to the fix
4. If the bug was missing a test, add one that would have caught it

**Checkpoint:** Reproduction case passes, test suite is green, and you have a new test covering this bug.

## Key Anti-Patterns to Avoid

- **Shotgun debugging**: making random changes hoping something works
- **Fix-and-pray**: applying a fix without understanding the cause
- **Skipping reproduction**: jumping to code changes without confirming you can trigger the bug
- **Fixing symptoms**: wrapping errors in try/catch instead of fixing what produces them

See **[anti-patterns.md](references/anti-patterns.md)** for the full catalog.

## Related Skills

- **[root-cause-tracing](../root-cause-tracing/SKILL.md)**: Deep call-stack tracing techniques — use after Phase 2 when the bug is deep in execution chains
- **[verification-before-completion](../verification-before-completion/SKILL.md)**: Mandatory verification gates — reinforces Phase 5 before claiming a fix is complete

## Deep-Dive References

- **[workflow.md](references/workflow.md)**: Detailed phase-by-phase instructions with decision trees
- **[examples.md](references/examples.md)**: Worked debugging examples across languages
- **[troubleshooting.md](references/troubleshooting.md)**: Common debugging scenarios and solutions
- **[anti-patterns.md](references/anti-patterns.md)**: Patterns to avoid and how to recognize them
