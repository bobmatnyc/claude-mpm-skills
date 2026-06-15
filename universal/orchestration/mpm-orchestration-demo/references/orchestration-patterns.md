# Orchestration Patterns — Deep Dive

## The Canonical Example: Weather System

The weather system in `claude-code-best-practice` is the reference implementation for Command → Agent → Skill orchestration. This section walks through it annotated, then generalizes the patterns.

### Weather System Components

```
/weather-orchestrator   ← Command: entry point, user interaction
    │
    ├─ Agent("weather-agent")        ← Agent tool call
    │      skills: [weather-fetcher]  ← Style 1: preloaded
    │      Returns: temperature + unit
    │
    └─ Skill("weather-svg-creator")  ← Style 2: dynamic
           Creates: weather.svg, output.md
```

**Why this structure?**

The command splits responsibilities cleanly:
- "Get the data" goes to a specialized agent with domain knowledge preloaded
- "Render the data" goes to a skill invoked after the data is available

Neither the agent nor the SVG skill needs to know about the other. The command is the only component with the full picture.

### Annotated Flow

```
Step 1: User runs /weather-orchestrator
        Command: "Celsius or Fahrenheit?" → user responds

Step 2: Command → Agent tool
        Agent: weather-agent
        Prompt: "Get Dubai temperature in Celsius"

        weather-agent has weather-fetcher preloaded:
        └─ Skill content injected at agent startup
        └─ Agent follows skill instructions, calls Open-Meteo API
        └─ Returns: "temperature=26, unit=Celsius"

Step 3: Command receives structured result
        Command → Skill tool
        Skill: weather-svg-creator
        Context includes: temperature=26, unit=Celsius

        weather-svg-creator runs:
        └─ Reads SVG template from reference.md
        └─ Writes orchestration-workflow/weather.svg
        └─ Writes orchestration-workflow/output.md

Step 4: Command reports result to user
```

## When to Use Each Style

### Use Preloaded Skills (Style 1) When

**The knowledge is always relevant to the agent's purpose.**

```yaml
# Good: security-auditor always needs these standards
skills:
  - owasp-top-10
  - secure-coding-checklist
```

**The knowledge is compact** (under ~400 tokens). Preloading large skills wastes context.

**You have 1–3 skills.** Beyond that, consider whether some should be invoked dynamically instead.

**Examples:**
- A `sql-optimizer` agent preloading `query-patterns`
- A `docs-writer` agent preloading `style-guide`
- A `test-runner` agent preloading `test-standards`

### Use Dynamic Invocation (Style 2) When

**The skill is conditional** — only needed based on what was found.

```
# Only format a report if issues were found
if issues:
    Skill("issue-formatter")
```

**The skill produces output** — files, reports, artifacts. These are naturally downstream.

**The skill is heavyweight** — large context, many instructions. Don't pay the cost unless needed.

**The skill is shared across commands** — a formatting skill invoked by multiple commands.

**Examples:**
- A report formatter invoked only when there's something to report
- A notification skill invoked only on failure
- A diagram generator invoked after analysis completes

## The `context: fork` Pattern

Beyond preloaded (Style 1) and dynamic (Style 2) skill invocation, an agent can run as a **forked sub-agent** that inherits the parent's accumulated context. This is the `context: fork` pattern: instead of starting the sub-agent with a clean slate, the orchestrator forks the current context so the sub-agent sees everything gathered so far.

### Fresh Context vs. Forked Context

```
DEFAULT (fresh context):
  Command gathers data → Agent("specialist") starts CLEAN
  └─ Sub-agent sees only the prompt; parent findings must be
     re-passed explicitly in the prompt string.

context: fork:
  Command gathers data → Agent("specialist", context: fork)
  └─ Sub-agent INHERITS the parent conversation: prior findings,
     file reads, and intermediate results are already present.
```

### Where Fork Fits in the Orchestration Flow

```
Step 1: /code-review-demo gathers context
        └─ Reads src/auth.py, src/api.py (now in parent context)

Step 2: Command → Agent tool with fork
        Agent(
          subagent_type="code-reviewer",
          context: fork,                  ← inherit parent context
          prompt="Review the files already read for security issues"
        )
        └─ Forked code-reviewer already sees the file contents;
           no need to re-read or re-pass them.

Step 3: Forked agent returns structured issues
        └─ Parent continues; context: fork did not pollute the
           parent with the agent's internal reasoning.
```

### When to Fork vs. Start Fresh

Use `context: fork` when the sub-agent's work depends on substantial context the orchestrator already gathered — file contents, prior analysis, or a running decision trail — and re-passing it in the prompt would be lossy or expensive.

Start fresh (the default) when the sub-agent's task is self-contained and a clean, focused context produces better results. A fresh context avoids distracting the sub-agent with irrelevant parent history.

| Question | Fresh context (default) | `context: fork` |
|---|---|---|
| Sub-agent needs prior file reads? | Re-pass in prompt | Inherited automatically |
| Sub-agent task self-contained? | Preferred | Unnecessary overhead |
| Risk of context pollution? | Low (isolated) | Higher (inherits everything) |
| Token cost | Lower per agent | Higher (carries parent history) |

### Fork and the Two Invocation Styles

`context: fork` composes with both styles. A forked agent still preloads its `skills:` frontmatter (Style 1) and can still invoke dynamic skills via the `Skill` tool (Style 2). Fork governs *what context the agent starts with*, not *how skills attach to it*. Preloaded skills are injected on top of the inherited context; dynamic skills run downstream as usual.

**Anti-pattern:** Do not fork by default. Forking every sub-agent carries the full parent history into each one, inflating token cost and risking context pollution where a focused, fresh agent would perform better. Reserve fork for genuine context-dependence.

## Agent Communication Patterns

### Return Format Contract

Agents should return structured data that commands can parse and act on. Define the contract explicitly in the agent definition.

**Good: structured return**
```markdown
# In agent definition
Return your findings as:
RESULT: [status]
ISSUES: [count]
DETAILS:
- ISSUE: [line] [severity] [description]
```

**Bad: unstructured prose**
```
I reviewed the code and found a few potential issues. The function on line 47
could potentially throw a NullPointerException if the input is null...
```

Prose requires the command to interpret natural language. Structured data enables deterministic logic.

### Passing Data to Skills

When a command invokes a dynamic skill via `Skill(skill: "name")`, the skill receives the full conversation context. This means data the agent returned is automatically available.

```
Command receives: "temperature=26, unit=Celsius"
Command invokes: Skill("weather-svg-creator")
Skill sees in context: "temperature=26, unit=Celsius"
Skill uses it: no explicit parameter passing needed
```

This is the key insight: **skills read from context, not from explicit arguments**. Structure agent return values so downstream skills can find what they need.

### Agent Tool Syntax

```python
# Correct: use subagent_type, not "launch" or "run"
Agent(
    subagent_type="code-reviewer",
    description="Review src/auth.py for security issues",
    prompt="Review the file src/auth.py. Return findings in structured format."
)
```

Note: use `subagent_type`, not a bash invocation. Subagents cannot be launched via shell commands.

## Error Handling in Orchestration Chains

### At the Command Level

Commands should handle agent failures explicitly:

```markdown
# In command definition
If the agent returns an error or "FAILED":
- Log the error
- Report failure to user with context
- Do NOT proceed to downstream skills
```

### At the Agent Level

Agents should return distinguishable failure states:

```
SUCCESS: [data]
FAILED: [reason]
NO_RESULT: [explanation]
```

Never let an agent return empty output — the command cannot distinguish "nothing to report" from "I failed silently."

### Defensive Skill Design

Skills should validate their inputs from context before proceeding:

```markdown
# In skill definition
Before creating output:
1. Verify the required data is present in context
2. If missing: output "ERROR: required data not found — [what was expected]"
3. Do not create partial output files
```

## Composition Depth

Keep orchestration chains to **two levels**: Command → Agent → Skill.

```
GOOD: Command → Agent (with preloaded skill) → Dynamic Skill
BAD:  Command → Agent → Agent → Agent → Skill
```

Deep chains create debugging nightmares. If you need more steps, structure them sequentially in the command rather than nesting agents.

```markdown
# Better: sequential steps in command
1. Agent("analyzer") → findings
2. Agent("planner", context=findings) → plan
3. Skill("reporter", context=plan) → report
```

Each step is visible and debuggable from the command level.

## File Organization Reference

```
.claude/
├── commands/
│   └── my-workflow.md          # Entry point command
├── agents/
│   └── my-specialist.md        # Specialized agent
│       # skills: [preloaded-knowledge]
└── skills/
    ├── preloaded-knowledge/
    │   └── SKILL.md             # Style 1: preloaded
    │       # user-invocable: false
    └── output-formatter/
        └── SKILL.md             # Style 2: dynamic
            # description: enables auto-discovery
```

## Quick Reference Card

| Question | Answer |
|---|---|
| Where does user interaction happen? | In the command |
| Where does domain logic happen? | In specialized agents |
| What goes in `skills:` frontmatter? | Always-needed domain knowledge |
| What gets invoked via `Skill` tool? | Conditional or output operations |
| How does data flow between components? | Via conversation context (structured return values) |
| How deep should chains be? | Two levels maximum |
| What returns from agents? | Structured data, not prose |
| Who owns the "what to do with results" logic? | The command |
