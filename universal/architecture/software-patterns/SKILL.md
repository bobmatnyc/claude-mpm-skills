---
name: software-patterns
description: "Compare tradeoffs and recommend architectural patterns — dependency injection, service-oriented architecture, repository, domain events, circuit breaker, and anti-corruption layer. Use when choosing between design patterns, planning microservices boundaries, evaluating system design alternatives, or asking 'which pattern should I use' for a specific coupling or resilience problem."
user-invocable: false
disable-model-invocation: true
version: 1.0.0
languages: all
progressive_disclosure:
  entry_point:
    summary: "Compare tradeoffs and recommend architectural patterns for coupling, resilience, and boundary problems"
    when_to_use: "When choosing between design patterns, planning microservices, evaluating dependency injection vs service locator, or deciding how to decouple services"
    quick_start: "1. Identify the problem class 2. Check decision tree 3. Apply foundational patterns (DI+SOA) 4. Layer situational patterns as needed"
  references:
    - foundational-patterns.md
    - situational-patterns.md
    - anti-patterns.md
    - decision-trees.md
    - examples.md
tags:
  - architecture
  - patterns
  - design-patterns
  - dependency-injection
  - service-oriented-architecture
  - microservices
  - system-design
---

# Software Patterns Primer

## Overview

Architectural patterns solve specific structural problems. This skill provides a decision framework for when to apply each pattern, not a catalog to memorize.

**Core philosophy:** Patterns solve problems. No problem? No pattern needed.

## When to Use This Skill

Activate when:
- Designing a new system or major feature
- Adding external service integrations
- Code becomes difficult to test or modify
- Services start calling each other in circles
- Failures in one component cascade to others
- Business logic scatters across multiple locations

## Pattern Hierarchy

### Foundational (Apply by Default)

These patterns provide the structural foundation for maintainable systems. Apply unless you have specific reasons not to.

| Pattern | Problem Solved | Signal to Apply |
|---------|---------------|-----------------|
| **Dependency Injection** | Tight coupling, untestable code | Classes instantiate their own dependencies |
| **Service-Oriented Architecture** | Monolithic tangles, unclear boundaries | Business logic scattered, no clear ownership |

**DI quick example — before and after:**

```python
# BEFORE: tight coupling, hard to test
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()       # concrete dependency
        self.mailer = SmtpMailer()         # concrete dependency

# AFTER: dependencies injected, easily testable
class OrderService:
    def __init__(self, db: Database, mailer: Mailer):
        self.db = db
        self.mailer = mailer
# In tests: OrderService(db=FakeDatabase(), mailer=FakeMailer())
```

### Situational (Apply When Triggered)

These patterns address specific problems. Don't apply preemptively.

| Pattern | Problem Solved | Signal to Apply |
|---------|---------------|-----------------|
| **Repository** | Data access coupling | Services know about database details |
| **Domain Events** | Circular dependencies, temporal coupling | Service A calls B calls C calls A |
| **Anti-Corruption Layer** | External system coupling | External API changes break your code |
| **Circuit Breaker** | Cascading failures | One slow service takes down everything |

→ [Foundational Patterns Detail](references/foundational-patterns.md)
→ [Situational Patterns Detail](references/situational-patterns.md)

## Quick Decision Tree

```
Is code hard to test?
├─ Yes → Apply Dependency Injection
└─ No → Continue

Is business logic scattered?
├─ Yes → Apply Service-Oriented Architecture
└─ No → Continue

Do services know database details?
├─ Yes → Apply Repository Pattern
└─ No → Continue

Do services call each other in cycles?
├─ Yes → Apply Domain Events
└─ No → Continue

Does external API change break your code?
├─ Yes → Apply Anti-Corruption Layer
└─ No → Continue

Does one slow service break everything?
├─ Yes → Apply Circuit Breaker
└─ No → Current patterns sufficient
```

→ [Complete Decision Trees](references/decision-trees.md)

## Implementation Priority

When starting a new system:

1. **First:** Establish DI container/pattern
2. **Second:** Define service boundaries (SOA)
3. **Third:** Add Repository for data access
4. **Then:** Layer situational patterns as problems emerge

When refactoring existing system:

1. **First:** Identify the specific pain point
2. **Second:** Apply the minimal pattern that solves it
3. **Third:** Validate improvement before adding more

## Navigation

### Pattern Details
- **[Foundational Patterns](references/foundational-patterns.md)**: DI and SOA implementation guides, when to deviate
- **[Situational Patterns](references/situational-patterns.md)**: Repository, Domain Events, ACL, Circuit Breaker details

### Decision Support
- **[Decision Trees](references/decision-trees.md)**: Complete flowcharts for pattern selection
- **[Anti-Patterns](references/anti-patterns.md)**: Common misapplications and how to recognize them

### Implementation
- **[Examples](references/examples.md)**: Language-agnostic pseudocode for each pattern combination

## Red Flags - STOP

STOP when:
- "Let me add all these patterns upfront" → Apply only what solves current problems
- "This pattern is best practice" → Best practice for what problem?
- "We might need this later" → YAGNI - add when needed
- "Service Locator is simpler" → Hidden dependencies cause testing pain
- "I'll just call this service directly" → Consider if events would decouple better
- "External API is stable, no need for ACL" → APIs always change eventually

**ALL of these mean: STOP. Identify the specific problem first.**

## Integration with Other Skills

- **test-driven-development**: DI enables testability; TDD validates pattern application
- **systematic-debugging**: Clear boundaries (SOA) simplify debugging
- **root-cause-tracing**: Well-structured services have clearer call chains

## Pattern Combinations

Common effective combinations:

| Scenario | Patterns |
|----------|----------|
| New microservice | DI + SOA + Repository |
| External API integration | DI + ACL + Circuit Breaker |
| Event-driven system | DI + SOA + Domain Events |
| Data-heavy application | DI + SOA + Repository + Unit of Work |

---

**Remember:** Patterns exist to solve problems. Start with the problem, not the pattern.
