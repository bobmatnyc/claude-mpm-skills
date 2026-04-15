---
name: mpm-orchestration-demo
description: Reference implementation demonstrating the Command → Agent → Skill orchestration pattern in Claude MPM, showing both preloaded-skill and dynamic-skill-invocation styles
argument-hint: "[topic]"
user-invocable: true
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Canonical MPM orchestration example: Command → Agent → Skill with two invocation styles"
    when_to_use: "When building new MPM workflows, onboarding to MPM patterns, or referencing orchestration best practices"
    quick_start: "Run /mpm-orchestration-demo to see the pattern in action"
  references:
    - orchestration-patterns.md
context_limit: 600
tags:
  - orchestration
  - patterns
  - reference
  - mpm
  - agents
  - skills
requires_tools: []
---

# MPM Orchestration Demo

## Overview

This skill is the canonical reference for the **Command → Agent → Skill** orchestration pattern in Claude MPM. It demonstrates a code review workflow that shows how commands, agents, and skills compose together — and the two distinct ways a skill can be invoked.

Understanding this pattern is the foundation for building any non-trivial MPM workflow.

## The Two Invocation Styles

### Style 1: Preloaded Skills (Frontmatter)

A skill is listed in an agent's `skills:` frontmatter. The full skill content is injected into the agent's context at startup, becoming embedded domain knowledge.

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Reviews code for quality, security, and correctness
skills:
  - code-review-checklist    # Injected at startup
model: sonnet
---
```

**When to use:** The agent always needs this knowledge. It's core to the agent's purpose — not situational.

**Characteristics:**
- Content is present from the first turn
- No tool call overhead
- Consumes context tokens even if not needed
- Best for 1–3 essential knowledge bases

### Style 2: Dynamic Invocation (Skill Tool)

A skill is invoked at runtime using the `Skill` tool. The command or agent calls `Skill(skill: "skill-name")` when it needs that capability.

```
# In a command or agent's instructions
Skill(skill: "security-scanner")
```

**When to use:** The capability is situational — only needed under certain conditions or after gathering initial data.

**Characteristics:**
- Invoked only when needed
- Preserves context tokens otherwise
- Enables conditional logic ("if security issues found, invoke scanner")
- Best for optional, conditional, or heavyweight operations

## Concrete Example: Code Review Orchestration

This demo implements a three-component code review system.

### Flow

```
╔══════════════════════════════════════════════════════════════════╗
║              CODE REVIEW ORCHESTRATION                           ║
║           Command  →  Agent  →  Skill                            ║
╚══════════════════════════════════════════════════════════════════╝

                       ┌─────────────────────┐
                       │    User invokes      │
                       │  /code-review-demo   │
                       └──────────┬──────────┘
                                  │
                                  ▼
         ┌──────────────────────────────────────────────────┐
         │  /code-review-demo — Command (Entry Point)       │
         │  1. Accept file path argument                    │
         │  2. Invoke code-reviewer agent (Agent tool)      │
         │  3. If issues found: Skill("issue-formatter")    │
         └──────────────────────┬───────────────────────────┘
                                │
                        Agent tool call
                                │
                                ▼
         ┌──────────────────────────────────────────────────┐
         │  code-reviewer — Agent                           │
         │  skills: [code-review-checklist]  ← Style 1     │
         │                                                  │
         │  Uses preloaded checklist to review the file     │
         │  Returns: list of issues (or "no issues")        │
         └──────────────────────┬───────────────────────────┘
                                │
                       Returns issues
                                │
         ┌──────────────────────▼───────────────────────────┐
         │  Command receives issues                         │
         │  Conditionally invokes:                          │
         │  Skill("issue-formatter")  ← Style 2             │
         └──────────────────────┬───────────────────────────┘
                                │
                                ▼
                      ┌─────────────────────┐
                      │  issue-formatter    │
                      │  Formats and writes │
                      │  review-report.md   │
                      └─────────────────────┘
```

### Component Definitions

#### Command: `/code-review-demo`

```markdown
---
# .claude/commands/code-review-demo.md
description: Demo orchestration command for code review workflow
model: haiku
---

# Code Review Demo

Accept a file path as $ARGUMENTS.

1. Use the Agent tool to invoke code-reviewer:
   Agent(subagent_type="code-reviewer", prompt="Review $ARGUMENTS for quality and security issues")

2. If the agent returns any issues:
   Skill(skill: "issue-formatter")

3. Report: file reviewed, issue count, report location (if written)
```

#### Agent: `code-reviewer`

```markdown
---
# .claude/agents/code-reviewer.md
name: code-reviewer
description: Reviews code files for quality, security, and correctness
tools: Read
model: sonnet
skills:
  - code-review-checklist
---

You are a code reviewer. Use your preloaded code-review-checklist skill to
evaluate the file specified in the prompt. Return a structured list of issues,
or "NO_ISSUES" if the code is clean.
```

#### Preloaded Skill: `code-review-checklist`

```markdown
---
# .claude/skills/code-review-checklist/SKILL.md
name: code-review-checklist
user-invocable: false
---

# Code Review Checklist

Review code against these criteria:

1. Input validation — are all inputs validated before use?
2. Error handling — are errors caught and handled gracefully?
3. Null safety — are null/undefined values handled?
4. Security — SQL injection, XSS, hardcoded secrets?
5. Complexity — functions over 20 lines or cyclomatic complexity > 5?

Return findings as:
ISSUE: [line] [severity] [description]
```

#### Dynamic Skill: `issue-formatter`

```markdown
---
# .claude/skills/issue-formatter/SKILL.md
name: issue-formatter
description: Formats code review findings into a structured markdown report
---

# Issue Formatter

Format the issues from the current conversation into review-report.md.

Structure:
- Summary: total issues by severity
- Critical issues (fix before merge)
- Warnings (should fix)
- Suggestions (optional improvements)
```

## Pattern Template

Copy this template when building a new MPM orchestration workflow:

```
COMMAND (.claude/commands/my-workflow.md)
  ├── Accepts user arguments
  ├── Invokes specialized AGENT via Agent tool
  │     └── Agent has PRELOADED SKILL(s) for core knowledge (Style 1)
  ├── Receives structured result from agent
  └── Conditionally invokes DYNAMIC SKILL via Skill tool (Style 2)
        └── Skill formats or persists the result
```

### Checklist for New Workflows

- [ ] Command is the single entry point and orchestrator
- [ ] Agents are specialized (one responsibility)
- [ ] Preloaded skills contain always-needed domain knowledge
- [ ] Dynamic skills contain conditional or output-specific logic
- [ ] Agent returns structured data, not prose
- [ ] Command handles the "what to do with results" logic

## Anti-Patterns

**Don't preload everything.** Loading 5 skills into an agent wastes context tokens and slows startup. Preload only core domain knowledge; invoke the rest dynamically.

**Don't put orchestration logic in agents.** An agent should do one thing and return data. Decision logic ("if issues found, format them") belongs in the command.

**Don't invoke subagents from subagents.** Subagents cannot invoke other subagents via bash. All agent invocations must go through the Agent tool from a command or orchestrator context.

**Don't skip structured return values.** An agent that returns unstructured prose is hard to act on. Define a clear return format (e.g., `ISSUE: [line] [severity] [desc]`) so the command can make decisions.

**Don't duplicate skill content.** If two agents need the same knowledge, create one shared skill and preload it into both. Never copy-paste skill content into agent definitions.

## Navigation

- **[Orchestration Patterns](references/orchestration-patterns.md)**: Deep-dive reference — annotated weather system example, when to use each style, agent communication patterns, error handling
