# Complete Skill Creation Guide

**Version**: 1.0.0
**Last Updated**: 2025-12-02
**Audience**: Skill creators and contributors
**Purpose**: End-to-end guide for creating high-quality Claude Code skills

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [YAML Frontmatter Deep Dive](#yaml-frontmatter-deep-dive)
4. [Progressive Disclosure](#progressive-disclosure)
5. [Skill Structure](#skill-structure)
6. [Self-Containment Requirements](#self-containment-requirements)
7. [Content Organization](#content-organization)
8. [Directory Structure](#directory-structure)
9. [Testing Your Skill](#testing-your-skill)
10. [Submission Process](#submission-process)
11. [Advanced Topics](#advanced-topics)
12. [Examples & Templates](#examples--templates)

---

## Introduction

### Who Should Create Skills?

You should consider creating a skill if you have:

- **Deep expertise** in a specific framework, tool, or methodology
- **Battle-tested patterns** that work well in practice
- **Clear use cases** where your knowledge would benefit Claude Code users
- **Time to maintain** and update the skill as technologies evolve

### Benefits of Creating Skills

**For Users:**
- Extends Claude's capabilities in your domain
- Provides consistent, tested patterns
- Saves time through progressive disclosure
- Enables better code generation

**For You:**
- Share your expertise with the community
- Build your reputation in the ecosystem
- Learn by teaching (skill creation clarifies knowledge)
- Contribute to an open-source project

### Creation Process Overview

```
Ideation → Design → Implementation → Testing → Submission → Iteration
   ↓         ↓           ↓            ↓          ↓            ↓
  2 hrs    4 hrs      8-12 hrs      2 hrs     1 hr       2-4 hrs
```

**Total time for first skill**: 20-30 hours (subsequent skills: 8-15 hours)

**Key Phases:**
1. **Ideation**: Validate idea, check for duplication
2. **Design**: Plan progressive disclosure, self-containment strategy
3. **Implementation**: Write YAML frontmatter, entry point, full documentation
4. **Testing**: Verify self-containment, test in isolation
5. **Submission**: Complete PR checklist, submit for review
6. **Iteration**: Address feedback, improve based on usage

---

## Quick Start

### Your First Skill in 30 Minutes

Let's create a minimal skill to understand the basics.

#### Step 1: Create Directory Structure

```bash
# Choose appropriate category
mkdir -p toolchains/python/my-framework

# Or for universal skills
mkdir -p universal/my-category/my-skill

cd toolchains/python/my-framework
```

#### Step 2: Create Minimal SKILL.md

```markdown
---
name: my-framework
description: Brief framework description and when to use it for routing, validation, async operations
---

# My Framework

## Overview

Brief explanation of what this framework does and why it's useful.

## Quick Start

### Installation

```bash
pip install my-framework
```

### Minimal Example

```python
# Complete, working code example (20-30 lines)
from my_framework import App

app = App()

@app.route("/")
def home():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run()
```

## Core Patterns

### Pattern 1: Essential Setup

```python
# Complete pattern with error handling (30-50 lines)
from my_framework import App, Config

config = Config(debug=True)
app = App(config=config)

@app.route("/users")
def get_users():
    try:
        # Implementation
        return {"users": []}
    except Exception as e:
        return {"error": str(e)}, 500
```

## Best Practices

- Use X for Y
- Avoid A when doing B
- Always include error handling

## Resources

- Official Docs: https://example.com
- GitHub: https://github.com/example/my-framework
```

#### Step 3: Create metadata.json

```json
{
  "name": "my-framework",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "tags": ["framework", "web", "api"],
  "entry_point_tokens": 45,
  "full_tokens": 1200,
  "requires": [],
  "author": "your-github-username",
  "license": "MIT"
}
```

#### Step 4: Test in Isolation

```bash
# Copy to flat directory
mkdir -p /tmp/skill-test
cp -r my-framework /tmp/skill-test/
cd /tmp/skill-test/my-framework

# Verify no relative paths
grep -r "\.\\./" .
# Should return nothing

# Read through SKILL.md
cat SKILL.md
# Verify it makes sense standalone
```

#### Step 5: Test in Claude Code

```bash
# Deploy to Claude Code skills directory
cp -r my-framework ~/.claude/skills/

# Start Claude Code session
# Verify skill appears in catalog
# Test that examples work
```

**Congratulations!** You've created your first skill. Now let's dive deeper.

---

## YAML Frontmatter Deep Dive

### Purpose of YAML Frontmatter

YAML frontmatter serves two critical purposes:

1. **Metadata**: Categorization, versioning, authorship
2. **Progressive Disclosure**: Entry point for efficient skill discovery

**Location**: Always at the very top of SKILL.md, between `---` delimiters.

### Required Fields

#### name (Required)

**Purpose**: Unique identifier for the skill

**Format**: Lowercase, hyphenated string

**Examples:**
```yaml
name: pytest                    # ✅ Good: concise, clear
name: fastapi-local-dev         # ✅ Good: descriptive with context
name: brainstorming            # ✅ Good: single concept
name: My Framework Skill        # ❌ Bad: spaces, capitalization
name: my_framework_skill        # ❌ Bad: underscores
```

**Guidelines:**
- Use lowercase with hyphens
- Be concise (1-3 words)
- Match directory name for consistency
- Avoid version numbers in name
- Use descriptive terms, not abbreviations

#### description (Required)

**Purpose**: Brief overview including when to use the skill

**Format**: 1-2 sentences, 20-50 words

**Pattern**: `[Framework/Tool] - [Capabilities] when [Use Cases]`

**Examples:**

**Pattern 1: Capability + Use Case**
```yaml
description: pytest - Python's most powerful testing framework with fixtures, parametrization, plugins, and framework integration for FastAPI, Django, Flask
```

**Pattern 2: Purpose + Context**
```yaml
description: Interactive idea refinement using Socratic method to develop fully-formed designs
```

**Pattern 3: Comprehensive with Triggers**
```yaml
description: Advanced TypeScript patterns and best practices for 2025. Use when working with TypeScript projects requiring type system mastery (generics, conditional types, mapped types), tsconfig optimization, runtime validation integration (Zod, TypeBox, Valibot), or type-safe API patterns
```

**Guidelines:**
- Include capabilities (what it does)
- Include use cases (when to use)
- Use active language
- Avoid jargon without context
- 20-50 words (sweet spot: 30-40)
- Think: "What would make me choose this skill?"

**Anti-Patterns:**
```yaml
# ❌ Too vague
description: Testing framework

# ❌ Too technical without context
description: Implements SOLID principles with DI containers

# ❌ Too long
description: This is a comprehensive skill that covers all aspects of the framework including installation, configuration, basic usage, advanced patterns, testing strategies, deployment options, performance optimization, and troubleshooting common issues

# ✅ Just right
description: FastAPI local development patterns including hot reload, debugging, database migrations, and test environments
```

### Optional Fields

#### version (Recommended)

**Purpose**: Semantic versioning for skill evolution

**Format**: MAJOR.MINOR.PATCH (e.g., `1.2.3`)

```yaml
version: 1.0.0    # Initial release
version: 1.1.0    # Added new patterns (minor)
version: 2.0.0    # Breaking changes (major)
version: 1.0.1    # Bug fixes (patch)
```

**See**: [VERSIONING.md](VERSIONING.md) for complete versioning policy.

#### category (Recommended)

**Purpose**: High-level categorization

**Valid Values:**
- `toolchain`: Language/framework-specific (Python, TypeScript, React)
- `universal`: Cross-language (testing, architecture, collaboration)
- `framework`: Specific framework skill

```yaml
category: toolchain   # For FastAPI, pytest, Next.js
category: universal   # For TDD, brainstorming, debugging
```

#### toolchain (Recommended for toolchain skills)

**Purpose**: Language/platform association

**Valid Values:**
```yaml
toolchain: python
toolchain: javascript
toolchain: typescript
toolchain: rust
toolchain: php
toolchain: go
toolchain: java
```

#### tags (Recommended)

**Purpose**: Discoverability via search

**Format**: Array of lowercase strings

```yaml
tags:
  - pytest
  - testing
  - python
  - tdd
  - fixtures
  - async
```

**Guidelines:**
- 5-10 tags
- Include framework name
- Include category (testing, api, database)
- Include key features (async, fixtures, decorators)
- Include use cases (tdd, integration-testing)

#### author (Recommended)

**Purpose**: Attribution and maintainer contact

```yaml
author: github-username
author: Claude MPM Team
```

#### license (Recommended)

**Purpose**: Legal clarity

```yaml
license: MIT
license: Apache-2.0
license: CC-BY-4.0
```

### Progressive Disclosure Configuration

Progressive disclosure enables token-efficient skill discovery. There are **three patterns** you can use:

---

#### Pattern 1: Simple Level-Based (Compact Skills)

**Best for**: Skills under 100 lines, simple concepts

```yaml
---
name: brainstorming
description: Interactive idea refinement using Socratic method to develop fully-formed designs
when_to_use: when partner describes any feature or project idea, before writing code or implementation plans
version: 2.2.0
progressive_disclosure:
  level: 1
  references: []
  note: Already optimal at 75 lines - intentionally compact, no references needed
---
```

**Characteristics:**
- Minimal frontmatter
- `level: 1` indicates fully loaded skill
- `references: []` shows no external references
- `when_to_use` provides clear trigger conditions
- Entire skill is entry point + content

**Token Budget**: 30-95 tokens for entry point

**Use When:**
- Skill is naturally concise (< 100 lines)
- No need for separate entry point
- Content is already optimized
- Adding structure would add complexity

---

#### Pattern 2: Entry Point Structure (Recommended)

**Best for**: Most skills (100-800 lines), clear structure needed

```yaml
---
name: pytest
description: pytest - Python's most powerful testing framework with fixtures, parametrization, plugins, and framework integration for FastAPI, Django, Flask
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Professional Python testing: fixtures, parametrize, markers, async support, FastAPI/Django/Flask integration, coverage, mocking"
    when_to_use: "Writing unit tests, integration tests, API testing, TDD workflow, testing async code, database testing, mocking dependencies"
    quick_start: "1. pip install pytest 2. Create test_*.py files 3. Use fixtures with @pytest.fixture 4. Parametrize with @pytest.mark.parametrize 5. Run: pytest -v"
context_limit: 700
tags:
  - pytest
  - testing
  - python
  - tdd
  - fixtures
requires_tools: []
---
```

**Characteristics:**
- Structured `entry_point` with three sub-fields
- `summary`: Compressed capabilities (60-80 tokens)
- `when_to_use`: Trigger scenarios (40-60 tokens)
- `quick_start`: Fast-track steps (40-60 tokens)
- `context_limit`: Token budget for full documentation

**Token Budget Breakdown:**
- `summary`: 60-80 tokens
- `when_to_use`: 40-60 tokens
- `quick_start`: 40-60 tokens
- **Total entry point**: 140-200 tokens

**Writing Guidelines:**

**summary:**
```yaml
# ✅ Good: Feature-packed, comma-separated
summary: "Professional Python testing: fixtures, parametrize, markers, async support, FastAPI/Django/Flask integration, coverage, mocking"

# ❌ Bad: Too verbose
summary: "This is a comprehensive testing framework that provides powerful features for writing unit tests, integration tests, and API tests. It includes fixtures for dependency injection, parametrization for data-driven tests, and markers for test organization."

# ✅ Good: Compressed keywords
summary: "Type-safe SQL queries, migrations, schema validation, relationships, async support, PostgreSQL/MySQL/SQLite"
```

**when_to_use:**
```yaml
# ✅ Good: Comma-separated scenarios
when_to_use: "Writing unit tests, integration tests, API testing, TDD workflow, testing async code, database testing, mocking dependencies"

# ❌ Bad: Full sentences
when_to_use: "You should use this skill when you need to write tests for your Python application. It's useful for unit testing, integration testing, and API testing."

# ✅ Good: Specific triggers
when_to_use: "Building REST APIs with Python, automatic OpenAPI docs, async performance, type-safe request/response validation"
```

**quick_start:**
```yaml
# ✅ Good: Numbered steps
quick_start: "1. pip install pytest 2. Create test_*.py files 3. Use fixtures with @pytest.fixture 4. Parametrize with @pytest.mark.parametrize 5. Run: pytest -v"

# ❌ Bad: Too detailed
quick_start: "First, you need to install pytest using pip. Then create test files that start with test_. Define fixtures using the @pytest.fixture decorator. You can parametrize tests with @pytest.mark.parametrize. Finally, run your tests using the pytest command with the -v flag for verbose output."

# ✅ Good: Compressed checklist
quick_start: "1. Install package 2. Configure settings 3. Create routes 4. Add middleware 5. Run server: npm start"
```

**Use When:**
- Skill is 100-800 lines
- Multiple distinct sections
- Clear quick start path exists
- Users need filtering criteria (when_to_use)

---

#### Pattern 3: Minimal Description (Simple Skills)

**Best for**: Very simple skills, framework-agnostic patterns

```yaml
---
name: typescript-core
description: Advanced TypeScript patterns and best practices for 2025. Use when working with TypeScript projects requiring type system mastery (generics, conditional types, mapped types), tsconfig optimization, runtime validation integration (Zod, TypeBox, Valibot), or type-safe API patterns. Essential for Next.js, Node.js, and full-stack TypeScript development.
---
```

**Characteristics:**
- Only `name` and `description`
- Description doubles as usage guidance
- No explicit progressive disclosure structure
- Relies on content organization for entry point
- First section acts as implicit entry point

**Token Budget**: Description should be 40-60 tokens

**Use When:**
- Skill structure is self-explanatory
- No complex entry point needed
- Description provides sufficient context
- Content is naturally progressive (basic → advanced)

**Important**: If using this pattern, ensure first section (after frontmatter) is concise and serves as entry point.

---

### Choosing Your Pattern

**Decision Tree:**

```
Is skill < 100 lines AND naturally concise?
├─ YES → Pattern 1 (Simple Level-Based)
└─ NO  → Continue

Does skill need structured entry point with quick start?
├─ YES → Pattern 2 (Entry Point Structure) ⭐ RECOMMENDED
└─ NO  → Continue

Is skill very straightforward with self-explanatory structure?
├─ YES → Pattern 3 (Minimal Description)
└─ NO  → Use Pattern 2 (Entry Point Structure)
```

**Recommendation**: **Use Pattern 2** for 90% of skills. It provides the best balance of discoverability, token efficiency, and user experience.

---

### Complete YAML Examples

#### Example 1: Minimal (Pattern 3)

```yaml
---
name: systematic-debugging
description: Root cause analysis using hypothesis-driven debugging with logging, reproduction steps, and fix validation
---
```

**Total entry point**: ~25 tokens

---

#### Example 2: Recommended (Pattern 2)

```yaml
---
name: fastapi-core
description: FastAPI web framework for Python with automatic OpenAPI docs, async support, and Pydantic validation
version: 1.2.0
category: toolchain
toolchain: python
author: claude-mpm-team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Modern Python web API: async routes, Pydantic validation, auto OpenAPI docs, dependency injection, middleware, WebSockets"
    when_to_use: "Building REST APIs, microservices, GraphQL backends, real-time services, replacing Flask/Django for API-only services"
    quick_start: "1. pip install fastapi uvicorn 2. Create FastAPI() app 3. Define routes with @app.get/post 4. Add Pydantic models 5. Run: uvicorn main:app --reload"
context_limit: 800
tags:
  - fastapi
  - python
  - api
  - async
  - pydantic
  - rest
  - openapi
  - microservices
requires_tools: []
---
```

**Entry point tokens**: ~180 tokens
**Full skill budget**: 800 tokens maximum

---

#### Example 3: Comprehensive (Pattern 2 with extras)

```yaml
---
name: nextjs-app-router
description: Next.js 14+ App Router with Server Components, Server Actions, streaming, and advanced caching
version: 2.0.0
category: framework
toolchain: typescript
framework: nextjs
author: claude-mpm-team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Next.js App Router: Server Components, Server Actions, streaming SSR, route handlers, parallel routes, intercepting routes, advanced caching"
    when_to_use: "Building modern web apps with Next.js 14+, migrating from Pages Router, React Server Components, server-side rendering, streaming UI"
    quick_start: "1. npx create-next-app@latest 2. Use app/ directory 3. Create routes with page.tsx 4. Server Components by default 5. Add 'use client' for interactivity"
    complexity: intermediate
    prerequisites: ["React basics", "TypeScript", "Async/await"]
context_limit: 1200
tags:
  - nextjs
  - react
  - typescript
  - app-router
  - server-components
  - server-actions
  - streaming
  - ssr
  - caching
requires_tools:
  - Node.js >= 18
  - npm or pnpm or yarn
related_skills:
  - react-patterns
  - typescript-core
  - api-design
---
```

**Entry point tokens**: ~210 tokens
**Full skill budget**: 1,200 tokens maximum

**Note**: `complexity`, `prerequisites`, and `related_skills` are optional extensions.

---

### Token Counting

**How to count tokens:**

```bash
# Using Python tiktoken library
pip install tiktoken

python3 << 'EOF'
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

text = """
Progressive disclosure entry point text here
"""

tokens = enc.encode(text)
print(f"Token count: {len(tokens)}")
EOF
```

**Quick estimation** (without tools):
- **1 token ≈ 4 characters** (average)
- **1 token ≈ 0.75 words** (average)

**Example:**
- 60 words ≈ 80 tokens
- 200 characters ≈ 50 tokens

**Target ranges:**
- Entry point: **140-200 tokens** (Pattern 2)
- Full skill: **3,000-6,000 tokens**
- Absolute minimum: **1,500 tokens** (very simple skills)
- Absolute maximum: **8,000 tokens** (comprehensive frameworks)

---

## Progressive Disclosure

### What is Progressive Disclosure?

Progressive disclosure is a two-tier loading system that enables efficient skill discovery without token overhead.

**The Problem**: Loading all 82+ skills completely would consume ~348,000 tokens, exceeding context windows and slowing discovery.

**The Solution**: Load entry points first (1,100 tokens), expand full documentation only when skill is invoked (99.7% token savings).

### Why Progressive Disclosure Matters

**Benefits:**

1. **Token Efficiency**
   - Discovery: 1,100 tokens for 82 skills
   - Without PD: 348,000 tokens for 82 skills
   - Savings: 99.7%

2. **Fast Discovery**
   - Scan all skills in seconds
   - No context window issues
   - Efficient filtering by use case

3. **Scalability**
   - Support 100+ skills without overhead
   - Add skills without token budget concerns
   - Future-proof architecture

4. **Better UX**
   - Quick "is this relevant?" check
   - Full details on demand
   - No information overload

### The Two-Tier System

#### Tier 1: Entry Point (30-95 tokens)

**Purpose**: Answer "Is this skill relevant to my current task?"

**Contents:**
- Skill name and brief description
- When to use (trigger scenarios)
- Quick start steps (optional)
- Capability summary

**Token Budget**: 30-95 tokens (target: 60)

**Loaded**: Always (during skill catalog browsing)

**Example Entry Point:**

```yaml
name: pytest
description: pytest - Python's most powerful testing framework
progressive_disclosure:
  entry_point:
    summary: "Python testing: fixtures, parametrize, markers, async"
    when_to_use: "Unit tests, integration tests, TDD workflow"
    quick_start: "1. pip install pytest 2. Create test_*.py 3. Run: pytest -v"
```

**Tokens**: ~65 tokens

---

#### Tier 2: Full Documentation (3,000-6,000 tokens)

**Purpose**: Answer "How do I accomplish my goal with this skill?"

**Contents:**
- Comprehensive overview
- Installation and setup
- Core patterns with complete examples
- Advanced usage
- Best practices
- Troubleshooting
- Related skills (optional)

**Token Budget**: 3,000-6,000 tokens (target: 4,000)

**Loaded**: On-demand (when skill is invoked)

**Example Full Documentation Structure:**

```markdown
# pytest - Professional Python Testing

## Overview
[Comprehensive explanation]

## Quick Start
[Installation + minimal example]

## Core Patterns
### Pattern 1: Fixtures
[Complete 30-50 line example]

### Pattern 2: Parametrization
[Complete 30-50 line example]

## Advanced Usage
[Complex scenarios]

## Best Practices
[Guidelines and tips]

## Troubleshooting
[Common issues]
```

**Tokens**: ~4,200 tokens

---

### Entry Point Design Principles

#### Principle 1: Token Efficiency

**Goal**: Maximum information density in minimum tokens

**Techniques:**

**Use comma-separated lists instead of sentences:**
```yaml
# ❌ 45 tokens
when_to_use: "Use this skill when you need to write unit tests. It's also helpful for integration testing and TDD workflows."

# ✅ 15 tokens
when_to_use: "Unit tests, integration testing, TDD workflows"
```

**Use abbreviations strategically:**
```yaml
# ✅ Common abbreviations okay
summary: "REST API, CRUD operations, JWT auth, OpenAPI docs"

# ❌ Obscure abbreviations bad
summary: "HATEOAS impl, HAL+JSON, ALPS profiles"
```

**Compress with semicolons:**
```yaml
# ✅ Semicolons separate related concepts
summary: "Server Components: RSC, streaming; Server Actions: mutations, forms; Caching: fetch, unstable_cache"
```

---

#### Principle 2: Clear Triggers

**Goal**: User immediately knows if skill is relevant

**Pattern**: Start with USE CASES, not features

```yaml
# ❌ Feature-focused (unclear when to use)
when_to_use: "Provides fixtures, parametrization, markers, and plugins"

# ✅ Use-case focused (clear triggers)
when_to_use: "Writing unit tests, integration tests, TDD workflow, testing async code"
```

**Effective Triggers:**
- Start with action verbs ("Writing tests", "Building APIs", "Debugging issues")
- Include context ("Python projects", "React apps", "Microservices")
- Mention pain points ("Slow test suites", "Complex state management")
- List scenarios ("API testing, database testing, mocking")

---

#### Principle 3: Actionable Quick Start

**Goal**: User can get started in 5 minutes

**Pattern**: Numbered steps, imperative commands

```yaml
# ❌ Too general
quick_start: "Install the package and create a configuration file, then define your routes and run the server"

# ✅ Specific, actionable
quick_start: "1. pip install fastapi uvicorn 2. Create main.py 3. Define @app.get('/') route 4. Run: uvicorn main:app --reload"
```

**Guidelines:**
- 3-5 steps maximum
- Include exact commands
- Specify file names
- End with verification step

---

#### Principle 4: Relevance Filtering

**Goal**: User can quickly rule out irrelevant skills

**Include:**
- Prerequisites ("Requires Docker", "TypeScript projects only")
- Platform constraints ("Linux/macOS only", "Node 18+")
- Complexity level ("Intermediate", "Advanced patterns")
- Framework version ("Next.js 14+", "React 18+")

```yaml
progressive_disclosure:
  entry_point:
    summary: "Next.js 14+ App Router patterns"
    when_to_use: "Building with Next.js 14+, React Server Components"
    quick_start: "1. Ensure Next.js 14+ 2. Use app/ directory 3. Create page.tsx"
    prerequisites: ["Next.js 14+", "React 18+", "TypeScript"]
```

---

### Full Documentation Design Principles

#### Principle 1: Progressive Complexity

**Structure**: Basic → Intermediate → Advanced

```markdown
## Quick Start
[Minimal working example - 20 lines]

## Core Patterns
### Pattern 1: Basic Usage
[Essential pattern - 30 lines]

### Pattern 2: Common Scenario
[Frequently needed - 40 lines]

## Advanced Usage
### Pattern 3: Complex Integration
[Advanced scenario - 50 lines]

### Pattern 4: Performance Optimization
[Expert-level - 40 lines]
```

**Benefit**: Users can stop reading when they have enough information.

---

#### Principle 2: Complete Examples

**Every example must be:**
- ✅ **Runnable**: Copy-paste-run without modification
- ✅ **Complete**: All imports, all setup, all cleanup
- ✅ **Commented**: Explain non-obvious parts
- ✅ **Error-handled**: Include try/catch, validation

```python
# ❌ Incomplete Example
@app.route("/users")
def get_users():
    # ...implementation
    pass
```

```python
# ✅ Complete Example
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# In-memory database (for demonstration)
users_db = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.get("/users", response_model=List[dict])
async def get_users():
    """
    Get all users.

    Returns:
        List of user dictionaries
    """
    try:
        return users_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Length Guidelines:**
- Minimal examples: 15-25 lines
- Core patterns: 30-50 lines
- Advanced patterns: 50-80 lines
- Maximum single example: 100 lines

---

#### Principle 3: Token Budgeting

**Allocation Strategy** (for 4,000 token skill):

- **Overview**: 200 tokens (5%)
- **Quick Start**: 400 tokens (10%)
- **Core Patterns**: 2,000 tokens (50%)
- **Advanced Usage**: 800 tokens (20%)
- **Best Practices**: 400 tokens (10%)
- **Troubleshooting**: 200 tokens (5%)

**Optimization Techniques:**

**Use tables for reference data:**
```markdown
## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| debug | bool | false | Enable debug mode |
| port | int | 8000 | Server port |
```

**Tokens saved**: ~30% vs. paragraph format

**Use code comments instead of prose:**
```python
# ✅ Efficient: Comments in code
def setup():
    # Load configuration from environment
    config = load_env_config()
    # Initialize database connection pool
    db.init(config.db_url, pool_size=10)
    # Register middleware
    app.add_middleware(LoggingMiddleware)
```

**Tokens saved**: ~20% vs. separate explanation paragraphs

**Consolidate related concepts:**
```markdown
## Error Handling

Standard pattern for all routes:

```python
@app.route("/endpoint")
async def handler():
    try:
        # Operation
        return result
    except ValidationError as e:
        return {"error": "validation", "detail": str(e)}, 400
    except NotFoundError as e:
        return {"error": "not_found", "detail": str(e)}, 404
    except Exception as e:
        logger.exception("Unexpected error")
        return {"error": "internal", "detail": "Server error"}, 500
```

**Apply this pattern to all routes.**
```

**Tokens saved**: ~40% vs. repeating pattern for each route type

---

#### Principle 4: Graceful Degradation

**Pattern**: Inline 80% use case, reference 20% advanced features

```markdown
## Database Integration (Self-Contained)

**Essential pattern** (inlined):

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./app.db")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Basic CRUD** covers 80% of use cases.

**Advanced patterns** (if sqlalchemy-patterns skill deployed):
- Complex joins and subqueries
- Relationship loading strategies (lazy, eager, subquery)
- Connection pooling optimization
- Async SQLAlchemy with asyncio

*Note: This skill functions without sqlalchemy-patterns skill.*
```

**Benefits:**
- Skill works standalone (self-contained)
- Users know where to go for advanced features
- No hard dependency on other skills
- Clear separation of basic vs. advanced

---

### Common Progressive Disclosure Mistakes

#### Mistake 1: Verbose Entry Points

**Problem**: Entry point exceeds 95 tokens, defeating progressive disclosure

```yaml
# ❌ 180 tokens
progressive_disclosure:
  entry_point:
    summary: "This is a comprehensive testing framework that provides powerful capabilities for writing unit tests, integration tests, and API tests. It includes an advanced fixture system for dependency injection, parametrization support for data-driven testing, rich assertion introspection so you don't need self.assertEqual, and a vast plugin ecosystem including pytest-cov for coverage, pytest-asyncio for async testing, and pytest-mock for mocking."
```

**Solution**: Compress to keyword format

```yaml
# ✅ 65 tokens
progressive_disclosure:
  entry_point:
    summary: "Python testing: fixtures for DI, parametrization, rich assertions, plugins (pytest-cov, pytest-asyncio, pytest-mock), async support"
```

**Technique**: Remove articles (a, an, the), use commas instead of conjunctions, abbreviate common terms (DI = Dependency Injection).

---

#### Mistake 2: Missing Trigger Conditions

**Problem**: User can't determine when skill is relevant

```yaml
# ❌ No context
when_to_use: "Web development"

# ❌ Features instead of use cases
when_to_use: "Async routes, Pydantic models, OpenAPI generation"
```

**Solution**: Specific use cases and contexts

```yaml
# ✅ Clear triggers
when_to_use: "Building REST APIs with Python, replacing Flask/Django for API-only services, microservices with OpenAPI, async web services"
```

---

#### Mistake 3: Sparse Full Documentation

**Problem**: Full documentation under 2,000 tokens, lacks examples

```markdown
# ❌ Too sparse (800 tokens)

# My Framework

## Overview
My Framework is a web framework.

## Usage
Install it and create routes.

## Example
```python
@app.route("/")
def home():
    return "Hello"
```

## Best Practices
Follow best practices.
```

**Solution**: Expand with complete examples and comprehensive coverage

```markdown
# ✅ Comprehensive (4,200 tokens)

# My Framework

## Overview
[2 paragraphs explaining purpose, key features, when to use]

## Quick Start
### Installation
[Detailed installation steps]

### Minimal Example
[Complete 30-line working example with comments]

## Core Patterns
### Pattern 1: Route Definition
[50-line example with error handling]

### Pattern 2: Database Integration
[50-line example with connection management]

### Pattern 3: Middleware
[40-line example with logging and CORS]

## Advanced Usage
[Complex scenarios: authentication, rate limiting, caching]

## Best Practices
[Specific guidelines with rationale]

## Troubleshooting
[Common issues and solutions]
```

---

#### Mistake 4: Token Bloat in Advanced Sections

**Problem**: Advanced section exceeds budget with repetitive examples

```markdown
# ❌ Repetitive (2,000 tokens)

## Advanced Patterns

### Pattern 1: Complex Query
[80 lines of similar code]

### Pattern 2: Another Complex Query
[80 lines of nearly identical code]

### Pattern 3: Yet Another Query
[80 lines of repeated patterns]
```

**Solution**: Consolidate patterns, show variations

```markdown
# ✅ Consolidated (600 tokens)

## Advanced Patterns

### Complex Queries

**Base pattern** (all queries follow this):

```python
from sqlalchemy import select, join

def complex_query(session, filters):
    """
    Template for complex queries.
    Adapt filter and join clauses as needed.
    """
    stmt = (
        select(User)
        .join(User.orders)
        .where(*filters)
        .order_by(User.created_at.desc())
    )
    return session.execute(stmt).scalars().all()
```

**Variations:**

```python
# With aggregation
stmt = select(User.id, func.count(Order.id)).group_by(User.id)

# With subquery
subq = select(Order.total).where(Order.user_id == User.id).scalar_subquery()
stmt = select(User).where(subq > 1000)

# With window function
stmt = select(User, func.row_number().over(partition_by=User.region))
```

**Apply base pattern to your specific use case.**
```

---

#### Mistake 5: Unclear Section Organization

**Problem**: Jumbled structure makes it hard to find information

```markdown
# ❌ Disorganized

# Framework

Some basic info.

## Advanced Authentication
[Complex pattern]

## Installation
[Should be near the top]

## Middleware Example
[Core pattern, should be earlier]

## Quick Example
[Should be right after installation]
```

**Solution**: Logical progressive flow

```markdown
# ✅ Organized

# Framework

## Overview
[Purpose and capabilities]

## Quick Start
### Installation
[Setup steps]

### Minimal Example
[Hello World]

## Core Patterns
[Essential day-to-day patterns]

## Advanced Usage
[Complex integrations]

## Best Practices
[Guidelines]

## Troubleshooting
[Common issues]
```

**Principle**: Basic → Common → Advanced → Reference

---

### Case Studies: Well-Designed Progressive Disclosure

#### Case Study 1: pytest Skill (Entry Point Structure)

**Entry Point** (165 tokens):
```yaml
progressive_disclosure:
  entry_point:
    summary: "Professional Python testing: fixtures, parametrize, markers, async support, FastAPI/Django/Flask integration, coverage, mocking"
    when_to_use: "Writing unit tests, integration tests, API testing, TDD workflow, testing async code, database testing, mocking dependencies"
    quick_start: "1. pip install pytest 2. Create test_*.py files 3. Use fixtures with @pytest.fixture 4. Parametrize with @pytest.mark.parametrize 5. Run: pytest -v"
```

**Analysis:**
- ✅ **Compressed summary**: Keywords, not sentences
- ✅ **Clear triggers**: Specific testing scenarios
- ✅ **Actionable quick start**: Exact commands
- ✅ **Token efficient**: 165 tokens for comprehensive entry

**Full Documentation** (4,500 tokens):
- Overview: 250 tokens
- Quick Start: 400 tokens
- Core Patterns: 2,200 tokens (fixtures, parametrization, markers)
- Advanced: 900 tokens (plugins, async, framework integration)
- Best Practices: 450 tokens
- Troubleshooting: 300 tokens

**Token Distribution**:
```
Entry Point:     165 (3.5%)
Full Docs:     4,500 (96.5%)
Total:         4,665 tokens
```

**Efficiency**: 96.5% savings during discovery phase

---

#### Case Study 2: Brainstorming Skill (Simple Level-Based)

**Entry Point** (45 tokens):
```yaml
name: Brainstorming Ideas Into Designs
description: Interactive idea refinement using Socratic method to develop fully-formed designs
when_to_use: when partner describes any feature or project idea, before writing code or implementation plans
progressive_disclosure:
  level: 1
  references: []
```

**Analysis:**
- ✅ **Compact**: Entire skill is 75 lines
- ✅ **Clear purpose**: Socratic method for design
- ✅ **Specific trigger**: "Before writing code"
- ✅ **No artificial separation**: Skill naturally compact

**Full Documentation** (600 tokens):
- Overview: 100 tokens
- The Process: 400 tokens (4 phases)
- Best Practices: 100 tokens

**Efficiency**: Skill is already optimized, no need for complex structure

**Lesson**: Don't add complexity if skill is naturally concise.

---

#### Case Study 3: TypeScript Core (Minimal Description)

**Entry Point** (52 tokens):
```yaml
name: typescript-core
description: Advanced TypeScript patterns and best practices for 2025. Use when working with TypeScript projects requiring type system mastery (generics, conditional types, mapped types), tsconfig optimization, runtime validation integration (Zod, TypeBox, Valibot), or type-safe API patterns.
```

**Analysis:**
- ✅ **Description doubles as entry**: Use cases embedded
- ✅ **Year-specific**: Signals up-to-date content
- ✅ **Key features listed**: Generics, conditional types, etc.
- ✅ **Integration points**: Zod, TypeBox, Valibot

**Full Documentation** (5,200 tokens):
- Quick Reference: 800 tokens (tsconfig, essential types)
- Core Patterns: 2,400 tokens (generics, utility types)
- Runtime Validation: 1,200 tokens (Zod, TypeBox)
- Best Practices: 800 tokens

**Lesson**: Simple structure works when content is self-organizing.

---

## Skill Structure

### SKILL.md Anatomy

A well-structured skill has clear sections in logical order:

```markdown
---
[YAML frontmatter]
---

# Skill Name

## Overview
[Purpose, capabilities, when to use]

## Quick Start
### Installation
[Setup commands]

### Minimal Example
[20-30 line complete working example]

## Core Patterns
### Pattern 1: [Most Common Use Case]
[30-50 line complete example]

### Pattern 2: [Second Most Common]
[30-50 line complete example]

### Pattern 3: [Third Most Common]
[30-50 line complete example]

## Advanced Usage
### Advanced Pattern 1
[50-80 line complex example]

### Advanced Pattern 2
[50-80 line complex example]

## Best Practices
- Guideline 1 with rationale
- Guideline 2 with rationale
- Guideline 3 with rationale

## Complementary Skills
[Optional: Related skills with informational references]

## Troubleshooting
### Issue 1: [Common Problem]
**Symptoms**: [What user sees]
**Cause**: [Why it happens]
**Solution**: [How to fix]

## Resources
- Official Docs: [URL]
- GitHub: [URL]
- Community: [URL]
```

**Total**: 3,500-5,000 tokens

---

### Supporting Files Organization

For skills requiring reference documentation:

```
my-skill/
├── SKILL.md                    # Main skill file (required)
├── metadata.json               # Metadata (required)
├── README.md                   # Overview for GitHub (optional)
└── references/                 # Supporting docs (optional)
    ├── api-reference.md       # Complete API documentation
    ├── advanced-patterns.md   # Deep dive on advanced topics
    ├── migration-guide.md     # Version migration
    └── examples/              # Extended examples
        ├── example-1.py
        └── example-2.py
```

**Guidelines:**
- **SKILL.md**: Self-contained, includes 80% use case
- **references/**: Optional deep dives, not required for basic usage
- **references/** linked from SKILL.md, but SKILL.md functions without them
- Keep references/ minimal (most content should be in SKILL.md)

**Anti-Pattern:**
```
❌ Don't split essential content:

my-skill/
├── SKILL.md                # Just overview
├── installation.md         # Required for setup
├── patterns.md            # Required for usage
└── examples.md            # Required for understanding

Problem: User needs to read 4 files to get started
```

**Correct Pattern:**
```
✅ Essential in SKILL.md, optional in references/:

my-skill/
├── SKILL.md               # Complete: overview + install + patterns + examples
└── references/            # Optional: API reference, advanced topics
    └── api-reference.md
```

---

### Reference Documentation

**When to use references/:**
- ✅ Complete API documentation (overwhelming in SKILL.md)
- ✅ Migration guides between versions
- ✅ Deep dives on single advanced topic
- ✅ Extended example collections
- ✅ Framework-specific integrations

**When NOT to use references/:**
- ❌ Essential installation steps
- ❌ Core usage patterns
- ❌ Common examples
- ❌ Basic troubleshooting

**Linking Pattern:**

```markdown
## Advanced Topics

For more detailed information:

- **[API Reference](references/api-reference.md)**: Complete API documentation
- **[Advanced Patterns](references/advanced-patterns.md)**: Deep dive on optimization
- **[Migration Guide](references/migration-v2.md)**: Upgrading to v2.0

**Note**: SKILL.md covers 80% of use cases. References provide optional deep dives.
```

---

### Examples and Anti-Patterns

#### Good Skill Structure Example

```markdown
---
name: fastapi-core
description: FastAPI web framework for Python with automatic OpenAPI docs and async support
version: 1.0.0
progressive_disclosure:
  entry_point:
    summary: "Modern Python web API: async routes, Pydantic validation, auto OpenAPI docs"
    when_to_use: "Building REST APIs, microservices, replacing Flask for API-only services"
    quick_start: "1. pip install fastapi uvicorn 2. Create app = FastAPI() 3. Define @app.get('/') 4. Run: uvicorn main:app --reload"
---

# FastAPI Core Patterns

## Overview

FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. Key features: automatic OpenAPI documentation, async support, Pydantic validation, dependency injection.

**Best for**: REST APIs, microservices, GraphQL backends, WebSocket services

**Performance**: On par with NodeJS and Go (via Starlette + Uvicorn)

## Quick Start

### Installation

```bash
# Install FastAPI and ASGI server
pip install fastapi uvicorn[standard]

# For development dependencies
pip install fastapi uvicorn[standard] pytest httpx
```

### Minimal Example (Self-Contained)

```python
"""
Minimal FastAPI application.
Demonstrates: basic routing, automatic docs, async support.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """Get item by ID with optional query parameter."""
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run it:**
```bash
python main.py
# Visit: http://localhost:8000
# Automatic docs: http://localhost:8000/docs
```

## Core Patterns

### Pattern 1: Request Validation with Pydantic

[30-50 line complete example]

### Pattern 2: Dependency Injection

[30-50 line complete example]

### Pattern 3: Error Handling

[30-50 line complete example]

## Advanced Usage

### Pattern 4: Background Tasks

[50-80 line complex example]

## Best Practices

- Always use async def for I/O-bound operations
- Leverage dependency injection for reusable components
- Use Pydantic models for request/response validation
- Enable automatic API documentation (built-in)
- Structure large apps with routers

## Complementary Skills

When using FastAPI, consider these related skills (if deployed):

- **pytest**: Testing FastAPI applications with async test client
- **sqlalchemy-patterns**: Database integration with async SQLAlchemy
- **pydantic-advanced**: Advanced validation and custom validators
- **docker-patterns**: Containerizing FastAPI applications

*Note: This skill is fully functional without complementary skills.*

## Troubleshooting

### Issue 1: Import errors for `uvicorn`
**Solution**: Install with standard extras: `pip install uvicorn[standard]`

### Issue 2: Async dependency errors
**Solution**: Use `async def` for dependencies that perform I/O

## Resources

- Official Docs: https://fastapi.tiangolo.com
- GitHub: https://github.com/tiangolo/fastapi
- Community: https://discord.gg/fastapi
```

**What makes this good:**
- ✅ Clear structure (Overview → Quick Start → Core → Advanced)
- ✅ Complete examples (runnable, commented)
- ✅ Self-contained (essential patterns inlined)
- ✅ Graceful degradation (complementary skills optional)
- ✅ Troubleshooting included
- ✅ 4,000-5,000 token range

---

#### Anti-Pattern Example 1: Fragmented Content

```markdown
# ❌ BAD: Content split across files

# My Framework

## Overview
My Framework is a web framework.

For installation, see [installation.md](./installation.md).
For usage patterns, see [patterns.md](./patterns.md).
For examples, see [examples.md](./examples.md).

## Resources
- Docs: https://example.com
```

**Problems:**
- ❌ Not self-contained
- ❌ Requires reading multiple files
- ❌ Breaks in flat deployment
- ❌ Poor user experience

---

#### Anti-Pattern Example 2: Over-Reliance on Other Skills

```markdown
# ❌ BAD: Depends on other skills

# My Framework

## Database Integration

To integrate databases, use the **sqlalchemy-patterns** skill.

## Testing

To test your application, use the **pytest-patterns** skill.

## Deployment

To deploy, use the **docker-patterns** skill.
```

**Problems:**
- ❌ Not self-contained
- ❌ User can't accomplish anything without other skills
- ❌ Violates 80% use case inline rule

**Solution:** Inline essential patterns, reference for advanced:

```markdown
# ✅ GOOD: Self-contained with optional references

# My Framework

## Database Integration (Self-Contained)

**Essential pattern** (inlined):

```python
from my_framework import Database

db = Database("sqlite:///./app.db")

@app.route("/users")
def get_users():
    return db.query("SELECT * FROM users").fetchall()
```

**Covers 80% of database use cases.**

**Advanced patterns** (if sqlalchemy-patterns skill deployed):
- Complex joins and subqueries
- Connection pooling optimization
- Async database operations

*Note: Basic database integration works without sqlalchemy-patterns.*
```

---

## Self-Containment Requirements

### Why Self-Containment Matters

Self-containment is the **#1 requirement** for skills. Here's why:

#### Deployment Flexibility

Skills can be deployed:
- **Individually**: User selects only needed skills
- **In bundles**: Curated collections for workflows
- **Selectively**: Based on toolchain detection
- **In flat structure**: All skills in single directory

Self-containment ensures skills work in **all scenarios**.

#### Flat Directory Reality

**Source structure** (hierarchical):
```
toolchains/
└── python/
    └── frameworks/
        └── fastapi/
            └── SKILL.md
```

**Deployed structure** (flat):
```
~/.claude/skills/
├── fastapi/
│   └── SKILL.md
├── pytest/
│   └── SKILL.md
└── sqlalchemy/
    └── SKILL.md
```

**Implication**: Relative paths (`../../pytest/SKILL.md`) **break**.

#### Testing and Validation

Self-contained skills can be:
- ✅ Tested in isolation
- ✅ Verified without dependencies
- ✅ Validated before submission
- ✅ Maintained independently

---

### The Golden Rule

> **Every skill must function as a standalone, atomic unit that works in any deployment scenario.**

**This means:**
- ❌ **Never** use relative paths to other skills
- ❌ **Never** list other skills in `requires` field
- ❌ **Never** import from other skills in examples
- ❌ **Never** assume specific directory structure
- ✅ **Always** inline essential content (20-50 lines per pattern)
- ✅ **Always** use skill names for informational references
- ✅ **Always** provide graceful degradation
- ✅ **Always** test in flat directory isolation

---

### Implementation Rules

#### Rule 1: No Relative Paths to Other Skills

**❌ DON'T:**
```markdown
For advanced testing, see [pytest skill](../../testing/pytest/SKILL.md).

Refer to [fastapi patterns](../fastapi/SKILL.md) for API integration.
```

**✅ DO:**
```markdown
For advanced testing, consider the **pytest** skill (if deployed).

The **fastapi** skill provides complementary API integration patterns.
```

**Why**: Relative paths break in flat deployment. Skill names work everywhere.

---

#### Rule 2: Inline Essential Content (80% Use Case)

**❌ DON'T:**
```markdown
## Database Integration

See the sqlalchemy-patterns skill for database integration.
```

**✅ DO:**
```markdown
## Database Integration (Self-Contained)

**Essential pattern** (covers 80% of use cases):

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Database setup
engine = create_engine("sqlite:///./app.db")
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    """Database session context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Usage in route
@app.route("/users")
def get_users():
    with get_db() as db:
        users = db.query(User).all()
        return [user.to_dict() for user in users]
```

**Advanced patterns** (if sqlalchemy-patterns skill deployed):
- Complex queries with joins
- Relationship loading strategies
- Connection pooling optimization

*Note: Basic pattern above handles most use cases.*
```

**Guideline**: Inline 20-50 lines per essential pattern.

---

#### Rule 3: No Skill Dependencies in `requires`

**❌ DON'T:**
```json
{
  "requires": ["pytest-patterns", "sqlalchemy-patterns"]
}
```

**✅ DO:**
```json
{
  "requires": []
}
```

**Or** (external packages only):
```json
{
  "requires": ["pytest", "sqlalchemy", "fastapi"]
}
```

**Rule**: `requires` is for **external packages**, not other skills.

---

#### Rule 4: Examples Must Be Self-Contained

**❌ DON'T:**
```python
# Import from other skill
from skills.pytest_patterns import advanced_fixture

# Use pattern from other skill
@advanced_fixture
def my_fixture():
    return setup_data()
```

**✅ DO:**
```python
# Inline the pattern
import pytest

@pytest.fixture
def my_fixture():
    """
    Fixture setup pattern (self-contained).

    This pattern is adapted from common testing practices.
    """
    data = setup_data()
    yield data
    cleanup_data(data)
```

**Guideline**: All imports must be from external packages, not other skills.

---

#### Rule 5: Graceful Degradation for Advanced Features

**Pattern**: `Core (inlined) + Advanced (optional reference)`

```markdown
## Testing (Self-Contained)

**Basic testing pattern** (inlined):

```python
import pytest

@pytest.fixture
def client():
    """Test client fixture."""
    from my_app import create_app
    app = create_app(testing=True)
    return app.test_client()

def test_home(client):
    """Test home page."""
    response = client.get("/")
    assert response.status_code == 200
```

**Covers 80% of testing needs.**

**Advanced fixtures** (if pytest skill deployed):
- Database session fixtures with transaction rollback
- Parametrized fixtures for data-driven tests
- Async test fixtures for async code
- Mock fixtures for external dependencies

*Note: Basic pattern above is sufficient for most testing.*
```

**Structure:**
1. **Basic pattern** (20-50 lines, inlined)
2. **Note** that basic covers 80% of use cases
3. **Advanced features** (bullet list, not detailed)
4. **Conditional language** ("if X skill deployed")
5. **Disclaimer** ("Note: This skill functions without X")

---

#### Rule 6: Informational References Only

**❌ DON'T:**
```markdown
## Setup

First, deploy the docker-patterns skill. Then follow these steps:
```

**✅ DO:**
```markdown
## Setup

### Local Development

[20-30 line self-contained setup]

### Docker Deployment (Optional)

For containerized deployment, consider the **docker-patterns** skill (if deployed), which provides:
- Multi-stage Dockerfile templates
- Docker Compose configurations
- Production deployment patterns

*Note: Local development above works without Docker.*
```

**Language:**
- ✅ "Consider"
- ✅ "If deployed"
- ✅ "Works well with"
- ✅ "Complementary"
- ❌ "Requires"
- ❌ "Depends on"
- ❌ "First deploy"

---

### Content Inlining Strategies

#### Strategy 1: Identify the 80% Use Case

**Ask:**
- What do 80% of users need to accomplish?
- What patterns are used daily vs. occasionally?
- What's essential vs. nice-to-have?

**Example (FastAPI skill):**
- **80% use case**: Define routes, validate requests, handle errors, connect database
- **20% use case**: WebSockets, background tasks, streaming responses, custom middleware

**Action**: Inline 80%, reference 20%.

---

#### Strategy 2: Compress Examples

**Technique**: Show complete pattern once, then variations concisely.

**❌ Verbose** (repeats full setup for each variation):
```markdown
## Pattern 1: Simple Route
[50 lines: imports, app setup, route, example]

## Pattern 2: Route with Validation
[50 lines: same imports, same app setup, different route, example]

## Pattern 3: Route with Database
[50 lines: same imports, same app setup, different route, example]
```

**Total**: 150 lines

**✅ Compressed** (show setup once, variations briefly):
```markdown
## Route Patterns (Self-Contained)

**Base setup** (applies to all patterns):

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
```

**Pattern 1: Simple route**
```python
@app.get("/")
async def root():
    return {"message": "Hello"}
```

**Pattern 2: With validation**
```python
class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    return {"created": item}
```

**Pattern 3: With database**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404)
    return user.to_dict()
```
```

**Total**: 60 lines

**Savings**: 60% reduction

---

#### Strategy 3: Extract Reusable Patterns

**Technique**: Show pattern once, apply everywhere.

```markdown
## Error Handling Pattern (Self-Contained)

**Standard pattern** (apply to all routes):

```python
from fastapi import HTTPException

@app.route("/endpoint")
async def handler():
    try:
        # Your logic here
        result = perform_operation()
        return {"data": result}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Internal error")
```

**Apply this pattern to all routes in your application.**

No need to repeat for each route type.
```

**Benefit**: Show once, reference everywhere.

---

#### Strategy 4: Use Tables for Configuration

**❌ Verbose** (paragraph format):
```markdown
The debug option is a boolean that controls debug mode. It defaults to false. When enabled, it provides detailed error messages.

The port option is an integer that specifies the server port. It defaults to 8000. You can set it to any valid port number.
```

**✅ Compressed** (table format):
```markdown
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| debug | bool | false | Enable debug mode with detailed errors |
| port | int | 8000 | Server port number |
| workers | int | 1 | Number of worker processes |
```

**Savings**: ~50% reduction

---

### Testing for Self-Containment

#### Verification Checklist

Before submitting, verify:

```bash
# 1. No relative paths to other skills
grep -r "\.\\./" your-skill/
# Expected: No results

# 2. No skill imports in code examples
grep -r "from skills\." your-skill/
grep -r "from \.\." your-skill/
# Expected: No results

# 3. No skill dependencies
cat your-skill/metadata.json | jq '.requires'
# Expected: [] or external packages only

# 4. Test in flat directory
mkdir -p /tmp/skill-test
cp -r your-skill /tmp/skill-test/
cd /tmp/skill-test/your-skill
cat SKILL.md
# Read through: Does it make sense standalone?

# 5. Verify examples are complete
# Extract code blocks and try running them
# All examples should work without other skills
```

---

#### Isolation Test Protocol

**Step-by-step isolation test:**

```bash
# 1. Create isolated test environment
mkdir -p /tmp/claude-skill-test
cd /tmp/claude-skill-test

# 2. Copy ONLY your skill (no other skills)
cp -r /path/to/your-skill ./

# 3. Verify no relative path references
grep -r "\.\\./" your-skill/
# Should return nothing

# 4. Check metadata dependencies
cat your-skill/metadata.json | jq '.requires'
# Should be empty array or external packages only

# 5. Read through SKILL.md
cat your-skill/SKILL.md

# Ask yourself:
# - Can I understand the purpose without other context? ✅
# - Are all examples complete and runnable? ✅
# - Are essential patterns included inline? ✅
# - Do references use skill names, not paths? ✅
# - Does skill work without other skills? ✅

# 6. Test examples (if applicable)
# Extract and run code examples
# Verify they work without other skills
```

**If ANY check fails**, skill is not self-contained.

---

## Content Organization

### Logical Flow and Structure

#### Principle: Progressive Complexity

Structure content from **basic → common → advanced → reference**.

**Optimal Flow:**

```markdown
# Skill Name

## Overview
[What it is, why it matters, when to use - 200 tokens]

## Quick Start
### Installation
[Setup commands - 100 tokens]

### Minimal Example
[Hello World - 300 tokens]

## Core Patterns (50% of content)
### Pattern 1: Most Common Use Case
[30-50 line example]

### Pattern 2: Second Most Common
[30-50 line example]

### Pattern 3: Third Most Common
[30-50 line example]

## Advanced Usage (25% of content)
### Advanced Pattern 1
[50-80 line complex example]

### Advanced Pattern 2
[50-80 line complex example]

## Best Practices (15% of content)
- Guideline 1
- Guideline 2
- Guideline 3

## Troubleshooting (10% of content)
### Common Issue 1
### Common Issue 2

## Resources
- Links to official docs
```

**Benefits:**
- Users can stop reading when they have enough
- Most important content comes first
- Natural progression of difficulty
- Easy to scan and find information

---

### Code Examples Best Practices

#### Guideline 1: Every Example Must Be Complete

**Complete means:**
- ✅ All imports included
- ✅ All setup included
- ✅ Full implementation (no `...` or `# TODO`)
- ✅ Error handling included
- ✅ Comments explaining non-obvious parts
- ✅ Can be copied and run immediately

**❌ Incomplete Example:**
```python
@app.route("/users")
def get_users():
    # ...implementation
    pass
```

**✅ Complete Example:**
```python
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

# In-memory database (for demonstration)
users_db: List[User] = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com")
]

@app.get("/users", response_model=List[User])
async def get_users():
    """
    Get all users.

    Returns:
        List of all users in database
    """
    try:
        return users_db
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve users: {str(e)}"
        )
```

---

#### Guideline 2: Comment Non-Obvious Parts

**What to comment:**
- ✅ Why (not what): Explain rationale
- ✅ Gotchas: Warn about pitfalls
- ✅ Context: Provide background
- ✅ Trade-offs: Explain alternatives

**What NOT to comment:**
- ❌ Obvious code: `x = 5  # Set x to 5`
- ❌ Implementation details covered by code
- ❌ API documentation (use docstrings)

**Example:**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID."""

    # Use filter_by for simple queries (more readable than filter)
    user = db.query(User).filter_by(id=user_id).first()

    if not user:
        # Return 404 (not 500) for missing resources
        raise HTTPException(status_code=404, detail="User not found")

    # Return dictionary (FastAPI handles JSON serialization)
    return user.to_dict()
```

---

#### Guideline 3: Show Error Handling

**Every example should demonstrate:**
- ✅ Validation errors (400)
- ✅ Not found errors (404)
- ✅ Server errors (500)
- ✅ Cleanup on failure

**Pattern:**
```python
@app.route("/endpoint")
async def handler(data: InputModel):
    try:
        # Validation (handled by Pydantic)
        validated = data.model_validate(data)

        # Business logic
        result = perform_operation(validated)

        # Success
        return {"data": result}

    except ValidationError as e:
        # 400: Invalid input
        raise HTTPException(status_code=400, detail=str(e))

    except NotFoundError as e:
        # 404: Resource not found
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # 500: Unexpected error
        logger.exception("Unexpected error in handler")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

---

#### Guideline 4: Example Length Guidelines

**By complexity:**

- **Minimal examples**: 15-25 lines
  - Purpose: Quick illustration of concept
  - Use: "Hello World", basic syntax

- **Core patterns**: 30-50 lines
  - Purpose: Demonstrate common use case
  - Use: Day-to-day patterns users will copy

- **Advanced patterns**: 50-80 lines
  - Purpose: Show complex integration
  - Use: Production-ready examples with error handling

- **Maximum**: 100 lines
  - Beyond 100 lines, split into multiple examples
  - Or extract to references/ directory

**Example progression:**

```python
# Minimal (20 lines)
@app.get("/")
async def root():
    return {"message": "Hello"}

# Core (40 lines)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    try:
        # Validation automatic via Pydantic
        items_db.append(item)
        return {"created": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Advanced (80 lines)
# [Full example with database, authentication, error handling]
```

---

### When to Use Sub-Sections

**Use sub-sections when:**
- ✅ Section exceeds 50 lines
- ✅ Multiple related patterns exist
- ✅ Logical groupings emerge
- ✅ Improves scannability

**Pattern:**

```markdown
## Core Patterns

### Pattern 1: Route Definition
#### Basic Route
[Example]

#### Route with Parameters
[Example]

#### Route with Query Parameters
[Example]

### Pattern 2: Request Validation
#### Pydantic Models
[Example]

#### Custom Validators
[Example]
```

**Don't over-nest:**
- ✅ H2 → H3 → H4 (maximum depth)
- ❌ H2 → H3 → H4 → H5 → H6 (too deep)

---

### Reference Material Placement

#### In-Skill References (Inline)

**Place in SKILL.md:**
- ✅ Essential configuration options (table)
- ✅ Common command flags (list)
- ✅ Error codes and meanings (table)
- ✅ Key concepts (brief explanations)

**Example:**
```markdown
## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| debug | bool | false | Enable debug mode |
| port | int | 8000 | Server port |
| workers | int | 1 | Number of workers |
| reload | bool | false | Auto-reload on changes |
```

---

#### External References (references/)

**Place in references/ directory:**
- ✅ Complete API documentation
- ✅ Exhaustive option lists (50+ items)
- ✅ Migration guides between versions
- ✅ Deep dives on single advanced topic
- ✅ Extended example collections

**Example:**
```
references/
├── api-reference.md          # Every class, method, parameter
├── configuration-guide.md    # All 100+ config options
├── migration-v2.md          # Upgrading from v1 to v2
└── examples/
    ├── complex-auth.py      # 200-line auth example
    └── websockets.py        # 150-line WebSocket example
```

**Linking:**
```markdown
## Advanced Configuration

Common options are listed above.

For comprehensive configuration documentation, see:
- **[Configuration Guide](references/configuration-guide.md)**: All 100+ options
- **[API Reference](references/api-reference.md)**: Complete API documentation
```

---

## Directory Structure

### Categorization: toolchains/ vs universal/

#### toolchains/ Directory

**Purpose**: Language or framework-specific skills

**Structure:**
```
toolchains/
├── python/
├── typescript/
├── javascript/
├── rust/
├── php/
├── nextjs/
├── ui/
└── ai/
```

**Place skill in toolchains/ when:**
- ✅ Tied to specific language (Python, JavaScript, Rust)
- ✅ Tied to specific framework (FastAPI, React, Next.js)
- ✅ Requires language-specific tooling
- ✅ Uses language-specific patterns

**Examples:**
- `toolchains/python/frameworks/fastapi/`
- `toolchains/typescript/testing/vitest/`
- `toolchains/javascript/frameworks/react/`

---

#### universal/ Directory

**Purpose**: Cross-language skills applicable everywhere

**Structure:**
```
universal/
├── architecture/
├── collaboration/
├── testing/
├── debugging/
├── security/
├── infrastructure/
└── main/
```

**Place skill in universal/ when:**
- ✅ Language-agnostic concepts (TDD, brainstorming, code review)
- ✅ Applies to all languages (architecture patterns, debugging)
- ✅ Workflow-oriented (collaboration, planning)
- ✅ Infrastructure (Docker, CI/CD)

**Examples:**
- `universal/testing/test-driven-development/`
- `universal/collaboration/brainstorming/`
- `universal/architecture/software-patterns/`

---

### Language/Framework Organization

#### Python Skills

```
toolchains/python/
├── frameworks/
│   ├── fastapi/
│   ├── django/
│   └── flask/
├── testing/
│   └── pytest/
├── data/
│   └── sqlalchemy/
├── async/
│   ├── asyncio/
│   └── celery/
├── tooling/
│   ├── mypy/
│   └── pyright/
└── validation/
    └── pydantic/
```

**Organization principle**: By sub-category (frameworks, testing, data, async, tooling)

---

#### TypeScript Skills

```
toolchains/typescript/
├── core/                  # Core TypeScript patterns
├── testing/
│   ├── jest/
│   └── vitest/
├── data/
│   ├── prisma/
│   ├── drizzle/
│   └── kysely/
└── frameworks/
    └── (see toolchains/nextjs/)
```

---

#### Next.js Skills (Special Case)

```
toolchains/nextjs/
├── core/                  # App Router, Server Components
├── v16/                  # Version-specific (Next.js 16)
└── frameworks/
    └── (integrations)
```

**Note**: Next.js gets top-level directory due to size and complexity.

---

### Naming Conventions

#### Skill Directory Names

**Pattern**: `lowercase-with-hyphens`

**Examples:**
```
✅ fastapi-local-dev
✅ test-driven-development
✅ brainstorming
✅ nextjs-app-router

❌ FastAPILocalDev
❌ test_driven_development
❌ Brainstorming
❌ nextjs_app_router
```

---

#### SKILL.md Filename

**Required**: Always `SKILL.md` (uppercase)

**❌ Don't:**
- `skill.md` (lowercase)
- `README.md` (wrong file)
- `FastAPI.md` (wrong name)

**✅ Do:**
- `SKILL.md` (correct)

---

#### metadata.json Filename

**Required**: Always `metadata.json` (lowercase)

**❌ Don't:**
- `METADATA.json` (uppercase)
- `Metadata.json` (mixed case)
- `meta.json` (wrong name)

**✅ Do:**
- `metadata.json` (correct)

---

### Multi-File Skills

**When to use multiple files:**
- ✅ Skill exceeds 800 lines
- ✅ Comprehensive API documentation needed
- ✅ Multiple complex examples (100+ lines each)
- ✅ Version-specific migration guides

**Structure:**
```
my-skill/
├── SKILL.md                    # Main skill (required)
├── metadata.json               # Metadata (required)
├── README.md                   # GitHub overview (optional)
└── references/                 # Supporting docs (optional)
    ├── api-reference.md       # Complete API
    ├── advanced-patterns.md   # Deep dive
    ├── migration-guide.md     # Version migration
    └── examples/              # Extended examples
        ├── example-1.py
        └── example-2.py
```

**Important:**
- **SKILL.md must be self-contained** (80% use case)
- **references/ is optional** (for deep dives)
- **No relative paths** between files that assume directory structure

**Linking from SKILL.md:**
```markdown
## Advanced Topics

For more detailed information:

- **[API Reference](references/api-reference.md)**: Complete API documentation
- **[Advanced Patterns](references/advanced-patterns.md)**: Optimization techniques
- **[Examples](references/examples/)**: Extended code examples

**Note**: SKILL.md covers 80% of use cases. References provide optional deep dives.
```

---

## Testing Your Skill

### Local Testing Workflow

#### Step 1: Isolation Test (Self-Containment)

**Purpose**: Verify skill works standalone in flat directory

```bash
# 1. Create isolated test environment
mkdir -p /tmp/claude-skill-test
cd /tmp/claude-skill-test

# 2. Copy ONLY your skill
cp -r /path/to/your-skill ./my-skill
cd my-skill

# 3. Verify no relative path violations
grep -rn "\.\\./" .
# Expected: No results (empty output)

# 4. Check for skill imports in examples
grep -rn "from skills\." .
grep -rn "from \.\." .
# Expected: No results

# 5. Verify metadata dependencies
cat metadata.json | jq '.requires'
# Expected: [] or ["external-package-1", "external-package-2"]
# NOT: ["other-skill-name"]

# 6. Read through SKILL.md completely
cat SKILL.md | less

# Ask yourself:
# - Does it make sense without other files? ✅
# - Are examples complete and runnable? ✅
# - Are essential patterns inlined (not referenced)? ✅
# - Does it work without other skills? ✅
```

**If ANY check fails**, fix before proceeding.

---

#### Step 2: Example Validation

**Purpose**: Verify code examples are complete and runnable

```bash
# 1. Extract code examples from SKILL.md
# (Manual process: copy examples to test files)

# 2. Create test environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required packages (from metadata.json requires)
pip install fastapi uvicorn pytest  # Example

# 4. Test each example
python example_1.py
# Verify: Runs without errors

python example_2.py
# Verify: Runs without errors

# 5. Run example tests
pytest example_tests.py -v
# Verify: All tests pass
```

**Common issues:**
- Missing imports
- Undefined variables
- Incomplete setup
- No error handling

**Fix** before proceeding.

---

#### Step 3: Token Count Verification

**Purpose**: Ensure entry point and full skill within token budgets

```bash
# Install tiktoken
pip install tiktoken

# Count entry point tokens
python3 << 'EOF'
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

# Extract entry point from YAML frontmatter
entry_point = """
summary: "Professional Python testing: fixtures, parametrize, markers, async"
when_to_use: "Unit tests, integration tests, TDD workflow, testing async code"
quick_start: "1. pip install pytest 2. Create test_*.py 3. Run: pytest -v"
"""

tokens = enc.encode(entry_point)
print(f"Entry point tokens: {len(tokens)}")
print(f"Target: 140-200 tokens")
print(f"Status: {'✅ PASS' if 140 <= len(tokens) <= 200 else '❌ FAIL'}")
EOF

# Count full skill tokens
python3 << 'EOF'
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

with open("SKILL.md", "r") as f:
    content = f.read()

tokens = enc.encode(content)
print(f"Full skill tokens: {len(tokens)}")
print(f"Target: 3000-6000 tokens")
print(f"Status: {'✅ PASS' if 3000 <= len(tokens) <= 6000 else '⚠️ WARNING' if len(tokens) < 8000 else '❌ FAIL'}")
EOF
```

**Token Budgets:**
- Entry point: 140-200 tokens (Pattern 2)
- Entry point: 30-95 tokens (Pattern 1, 3)
- Full skill: 3,000-6,000 tokens (target)
- Full skill: Up to 8,000 tokens (maximum)

---

#### Step 4: Claude Code Integration Test

**Purpose**: Test skill in actual Claude Code environment

```bash
# 1. Deploy skill to Claude Code
mkdir -p ~/.claude/skills/
cp -r my-skill ~/.claude/skills/

# 2. Start Claude Code session
# (Start Claude Code CLI or desktop app)

# 3. Verify skill appears in catalog
# Run: /skills list
# Look for your skill name

# 4. Test skill invocation
# Ask Claude Code to use your skill
# Example: "Use the pytest skill to create a test suite"

# 5. Verify full documentation expands
# Check that full content is available when skill is invoked

# 6. Test examples in context
# Ask Claude to implement examples from your skill
# Verify examples work as documented
```

**Checklist:**
- ✅ Skill appears in catalog
- ✅ Entry point is concise and clear
- ✅ Full documentation expands on invocation
- ✅ Examples work when implemented
- ✅ Skill provides value in actual usage

---

### Validation Checklist

Use this checklist before submission:

#### Self-Containment Validation

```bash
# No relative paths to other skills
grep -rn "\.\\./" . | grep -v "node_modules" | grep -v ".git"
# ✅ Expected: No results

# No skill imports in examples
grep -rn "from skills\." . | grep -v "node_modules"
grep -rn "from \.\." . | grep -v "node_modules"
# ✅ Expected: No results

# No skill dependencies
cat metadata.json | jq '.requires | map(select(. | test("skill";"i")))'
# ✅ Expected: []

# All examples are complete (no ... or TODO)
grep -rn "\.\.\." SKILL.md
grep -rn "TODO" SKILL.md
# ✅ Expected: Only in comments explaining patterns, not in code
```

---

#### Content Validation

```bash
# SKILL.md exists
test -f SKILL.md && echo "✅ SKILL.md exists" || echo "❌ SKILL.md missing"

# metadata.json exists
test -f metadata.json && echo "✅ metadata.json exists" || echo "❌ metadata.json missing"

# Valid JSON
jq empty metadata.json && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# Required YAML frontmatter
head -1 SKILL.md | grep -q "^---$" && echo "✅ YAML frontmatter present" || echo "❌ Missing frontmatter"

# Entry point token count
# (Use token counting script from Step 3 above)

# Full skill token count
# (Use token counting script from Step 3 above)
```

---

#### Example Validation

```bash
# Extract all code blocks
# Verify each is complete:
# - Has all imports
# - Has full implementation
# - Has error handling
# - Can be copied and run

# Run example tests (if applicable)
# pytest tests/ -v
```

---

### Common Issues to Check

#### Issue 1: Incomplete Examples

**Symptom**: Code snippets with `...` or `# TODO`

**Check:**
```bash
grep -n "\.\.\." SKILL.md
grep -n "# TODO" SKILL.md
```

**Fix**: Complete all examples before submission.

---

#### Issue 2: Broken References

**Symptom**: Links to files using relative paths

**Check:**
```bash
grep -n "](\.\./" SKILL.md
grep -n "](/\.\./" SKILL.md
```

**Fix**: Use skill names, not relative paths.

---

#### Issue 3: Missing Error Handling

**Symptom**: Examples without try/catch or error checks

**Check**: Review all examples manually

**Fix**: Add error handling to all examples.

---

#### Issue 4: Over-Sized Entry Point

**Symptom**: Entry point exceeds 200 tokens

**Check**: Use token counting script

**Fix**: Compress using techniques from Progressive Disclosure section.

---

#### Issue 5: Under-Sized Full Documentation

**Symptom**: Full skill under 2,000 tokens

**Check**: Use token counting script

**Fix**: Expand with more examples, best practices, troubleshooting.

---

### Self-Containment Verification

**Final verification before submission:**

```bash
#!/bin/bash
# save as verify-skill.sh

SKILL_DIR=$1

echo "=== Skill Self-Containment Verification ==="
echo

# 1. Check relative paths
echo "1. Checking for relative paths..."
if grep -rn "\.\\./" "$SKILL_DIR" | grep -v "node_modules" | grep -v ".git"; then
    echo "❌ FAIL: Relative paths found"
    exit 1
else
    echo "✅ PASS: No relative paths"
fi
echo

# 2. Check skill imports
echo "2. Checking for skill imports..."
if grep -rn "from skills\." "$SKILL_DIR" | grep -v "node_modules"; then
    echo "❌ FAIL: Skill imports found"
    exit 1
else
    echo "✅ PASS: No skill imports"
fi
echo

# 3. Check metadata dependencies
echo "3. Checking metadata dependencies..."
if cat "$SKILL_DIR/metadata.json" | jq '.requires | map(select(. | test("skill";"i")))' | grep -q "skill"; then
    echo "❌ FAIL: Skill dependencies found"
    exit 1
else
    echo "✅ PASS: No skill dependencies"
fi
echo

# 4. Check required files
echo "4. Checking required files..."
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ FAIL: SKILL.md missing"
    exit 1
else
    echo "✅ PASS: SKILL.md exists"
fi

if [ ! -f "$SKILL_DIR/metadata.json" ]; then
    echo "❌ FAIL: metadata.json missing"
    exit 1
else
    echo "✅ PASS: metadata.json exists"
fi
echo

# 5. Check JSON validity
echo "5. Checking JSON validity..."
if jq empty "$SKILL_DIR/metadata.json" 2>/dev/null; then
    echo "✅ PASS: Valid JSON"
else
    echo "❌ FAIL: Invalid JSON"
    exit 1
fi
echo

# 6. Check YAML frontmatter
echo "6. Checking YAML frontmatter..."
if head -1 "$SKILL_DIR/SKILL.md" | grep -q "^---$"; then
    echo "✅ PASS: YAML frontmatter present"
else
    echo "❌ FAIL: Missing YAML frontmatter"
    exit 1
fi
echo

echo "=== ✅ All checks passed ==="
```

**Usage:**
```bash
chmod +x verify-skill.sh
./verify-skill.sh path/to/your-skill
```

---

## Submission Process

### Using SKILL_CREATION_PR_CHECKLIST.md

Before submitting a PR, complete the checklist:

**Location**: `docs/SKILL_CREATION_PR_CHECKLIST.md`

**Process:**

1. **Copy checklist** to your PR description
2. **Run verification commands** (provided in checklist)
3. **Paste command output** as proof
4. **Check all boxes** that apply
5. **Submit PR** with completed checklist

**Checklist sections:**
- ✅ Self-containment verification
- ✅ Required files present
- ✅ Token budget compliance
- ✅ Example completeness
- ✅ Testing confirmation

**Example PR description:**

```markdown
## Skill: pytest

### Description
Comprehensive pytest skill covering fixtures, parametrization, markers, async testing, and framework integration.

### Checklist

- [x] **Self-Containment**: No relative paths to other skills
  ```bash
  $ grep -rn "\.\\./" pytest/
  # No results
  ```

- [x] **Required Files**: SKILL.md and metadata.json present
  ```bash
  $ ls pytest/
  SKILL.md  metadata.json  references/
  ```

- [x] **Token Budget**: Entry point within limits
  ```
  Entry point tokens: 165
  Target: 140-200 tokens
  Status: ✅ PASS
  ```

- [x] **Examples Complete**: All examples are runnable
  - Tested fixtures example ✅
  - Tested parametrization example ✅
  - Tested async example ✅

- [x] **Isolation Test**: Verified in flat directory
  ```bash
  $ cp -r pytest /tmp/test/
  $ cd /tmp/test/pytest
  $ cat SKILL.md
  # Read through: Makes sense standalone ✅
  ```

### Additional Notes
- Added references/ directory for extended examples
- Included framework integration sections (FastAPI, Django, Flask)
- Token count: 4,500 tokens (within 3,000-6,000 range)
```

---

### PR Requirements

**Required for PR approval:**

1. **Completed Checklist**
   - All items checked
   - Verification commands run
   - Output pasted

2. **Self-Containment Compliance**
   - No relative paths
   - No skill dependencies
   - Examples are complete

3. **File Structure**
   - SKILL.md present
   - metadata.json present
   - Both valid

4. **Token Budgets**
   - Entry point: 140-200 tokens (Pattern 2) or 30-95 (Pattern 1/3)
   - Full skill: 3,000-6,000 tokens (up to 8,000 acceptable)

5. **Content Quality**
   - Examples are complete and runnable
   - Error handling included
   - Best practices documented

6. **Testing**
   - Isolation test passed
   - Claude Code integration test passed

---

### Review Process

**What to expect:**

1. **Initial Review** (2-3 days)
   - Maintainer reviews checklist
   - Verifies self-containment
   - Checks token budgets

2. **Feedback** (if needed)
   - Specific issues identified
   - Suggestions for improvement
   - References to guidelines

3. **Iteration** (1-2 rounds typical)
   - Address feedback
   - Update PR
   - Re-submit for review

4. **Approval**
   - All checks passed
   - Quality standards met
   - Ready to merge

5. **Merge**
   - Skill added to repository
   - Appears in next release

**Average timeline**: 1-2 weeks from submission to merge

---

### Versioning Considerations

**Initial submission**: Always `1.0.0`

**Future updates**: Follow semantic versioning

- **MAJOR** (2.0.0): Breaking changes
  - Changed skill structure
  - Removed essential content
  - Incompatible with previous version

- **MINOR** (1.1.0): New features (backward-compatible)
  - Added new patterns
  - Expanded examples
  - New sections

- **PATCH** (1.0.1): Bug fixes (backward-compatible)
  - Fixed typos
  - Corrected examples
  - Updated links

**See**: [VERSIONING.md](VERSIONING.md) for complete policy.

---

## Advanced Topics

### Large Skills Optimization

**Challenge**: Skill exceeds 6,000 tokens

**Strategies:**

#### Strategy 1: Split into Multiple Skills

**When to split:**
- Skill covers multiple distinct topics
- Topics can be used independently
- Each topic is 2,000+ tokens

**Example:**

**Before** (8,000 tokens):
```
fastapi-complete/
└── SKILL.md  # Covers: routing, validation, auth, testing, deployment
```

**After** (split):
```
fastapi-core/
└── SKILL.md  # 4,000 tokens: routing, validation, basics

fastapi-auth/
└── SKILL.md  # 2,500 tokens: authentication patterns

fastapi-testing/
└── SKILL.md  # 2,500 tokens: testing patterns
```

---

#### Strategy 2: Move Reference Material to references/

**Pattern:**
- Keep 80% use case in SKILL.md (4,000 tokens)
- Move API reference to references/ (2,000 tokens)
- Move extended examples to references/ (1,000 tokens)

**Before** (7,000 tokens in SKILL.md):
```
SKILL.md:
- Overview (500 tokens)
- Quick Start (500 tokens)
- Core Patterns (2,000 tokens)
- Advanced (1,500 tokens)
- Complete API Reference (2,000 tokens)  ← Too much
- Extended Examples (500 tokens)  ← Too much
```

**After** (4,500 tokens in SKILL.md + 2,500 in references/):
```
SKILL.md (4,500 tokens):
- Overview (500 tokens)
- Quick Start (500 tokens)
- Core Patterns (2,000 tokens)
- Advanced (1,000 tokens)
- Best Practices (500 tokens)

references/ (2,500 tokens):
- api-reference.md (2,000 tokens)
- extended-examples/ (500 tokens)
```

---

#### Strategy 3: Consolidate Examples

**Technique**: Show pattern once, list variations

**Before** (3,000 tokens):
```markdown
## Pattern 1: GET Route
[Full 50-line example]

## Pattern 2: POST Route
[Full 50-line example with same setup]

## Pattern 3: PUT Route
[Full 50-line example with same setup]

## Pattern 4: DELETE Route
[Full 50-line example with same setup]
```

**After** (1,000 tokens):
```markdown
## Route Patterns

**Base setup** (applies to all):
[30-line setup once]

**GET Route**:
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item": item_id}
```

**POST Route**:
```python
@app.post("/items")
async def create_item(item: Item):
    return {"created": item}
```

**Variations** (PUT, DELETE): Apply base setup, change method and logic.
```

**Savings**: 66% reduction

---

### Multi-Level Progressive Disclosure

**Advanced technique**: Multiple disclosure levels

**Use case**: Very large skills (8,000+ tokens) that can't be split

**Structure:**

```yaml
progressive_disclosure:
  entry_point:
    summary: "Brief summary (60 tokens)"
    when_to_use: "Use cases (40 tokens)"
    quick_start: "Steps (40 tokens)"
  levels:
    - level: 1
      sections: ["Overview", "Quick Start", "Core Patterns"]
      tokens: 2000
    - level: 2
      sections: ["Advanced Usage", "Best Practices"]
      tokens: 2000
    - level: 3
      sections: ["Expert Patterns", "Performance Tuning"]
      tokens: 2000
```

**Benefit**: Load only needed depth

**Caveat**: More complex to implement, requires tooling support

---

### Cross-Skill Coordination (Without Dependencies)

**Challenge**: Skills need to work together without hard dependencies

**Pattern**: Informational references + graceful degradation

#### Pattern 1: Skill Recommendations

**In SKILL.md:**
```markdown
## Complementary Skills

When using this skill, consider (if deployed):

- **pytest**: Testing framework for comprehensive test coverage
  - *Use case*: Writing unit and integration tests
  - *Integration*: Use fixtures from pytest for database session management

- **docker-patterns**: Containerization and deployment
  - *Use case*: Production deployment
  - *Integration*: Dockerfiles for this framework

*Note: All skills are independently deployable. This skill functions without them.*
```

---

#### Pattern 2: Conditional Guidance

**In SKILL.md:**
```markdown
## Testing (Self-Contained)

**Basic testing pattern** (inlined):
[30-line pytest example]

**Advanced fixtures** (if pytest skill deployed):
- Parametrized test fixtures
- Database session fixtures with rollback
- Mock external API dependencies

*See pytest skill for comprehensive fixture patterns.*
```

---

#### Pattern 3: Integration Notes

**In SKILL.md:**
```markdown
## FastAPI Integration

**Basic integration** (self-contained):
[40-line integration example]

**Advanced patterns** (if fastapi-advanced skill deployed):
- Background tasks with Celery
- WebSocket integration
- GraphQL endpoints

*Note: Basic integration covers 80% of use cases.*
```

---

#### Anti-Pattern: Hard Dependencies

**❌ Don't:**
```markdown
## Testing

This skill requires the **pytest-patterns** skill.

First, deploy pytest-patterns, then follow these steps:
1. Import from pytest-patterns skill
2. Use advanced fixtures
```

**✅ Do:**
```markdown
## Testing (Self-Contained)

**Essential testing pattern** (inlined):
[Complete 40-line example with pytest]

**Advanced patterns** (if pytest-patterns skill deployed):
- See pytest-patterns for advanced fixtures
```

---

### Token Budget Optimization

**Goal**: Maximize information density

#### Technique 1: Use Tables

**Before** (200 tokens):
```markdown
The debug option is a boolean that defaults to false. When enabled, it provides detailed error messages and stack traces.

The port option is an integer that defaults to 8000. You can set it to any valid port number between 1 and 65535.

The workers option is an integer that defaults to 1. It controls the number of worker processes for handling requests.
```

**After** (80 tokens):
```markdown
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| debug | bool | false | Enable detailed errors and stack traces |
| port | int | 8000 | Server port (1-65535) |
| workers | int | 1 | Number of worker processes |
```

**Savings**: 60%

---

#### Technique 2: Compress with Comments

**Before** (150 tokens):
```markdown
### Error Handling

FastAPI provides several ways to handle errors. You can use HTTPException for standard HTTP errors. You can also define custom exception handlers using the @app.exception_handler decorator. For validation errors, Pydantic automatically returns 422 status codes.

Example:
[code]
```

**After** (60 tokens):
```python
# Error handling patterns

# Standard HTTP errors
raise HTTPException(status_code=404, detail="Not found")

# Custom exception handler
@app.exception_handler(CustomError)
async def custom_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

# Validation errors (automatic with Pydantic)
```

**Savings**: 60%

---

#### Technique 3: Eliminate Redundancy

**Before** (300 tokens):
```markdown
### GET Routes

To define a GET route, use the @app.get() decorator:
[example]

### POST Routes

To define a POST route, use the @app.post() decorator:
[example]

### PUT Routes

To define a PUT route, use the @app.put() decorator:
[example]
```

**After** (120 tokens):
```markdown
### Route Definitions

Use decorators for each HTTP method:

```python
@app.get("/items")      # GET
@app.post("/items")     # POST
@app.put("/items/{id}") # PUT
@app.delete("/items/{id}") # DELETE
```

Pattern applies to all methods: `@app.{method}(path)`.
```

**Savings**: 60%

---

## Examples & Templates

### Minimal Skill Template

**Use for**: Simple skills under 100 lines

**File**: `minimal-skill-template/SKILL.md`

```markdown
---
name: my-simple-skill
description: Brief description including when to use it for specific use cases
---

# My Simple Skill

## Overview

Brief explanation of what this skill provides and why it's useful.

**Best for**: Specific use cases

## Quick Start

### Installation

```bash
# Installation commands
pip install my-package
```

### Minimal Example

```python
# Complete, runnable example (20-30 lines)
from my_package import Thing

thing = Thing()
result = thing.do_something()
print(result)
```

## Core Pattern

### Essential Usage

```python
# Complete pattern with error handling (30-50 lines)
from my_package import Thing, ThingError

def main():
    try:
        thing = Thing(config="production")
        result = thing.do_something()
        return result
    except ThingError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    main()
```

## Best Practices

- Use X for Y
- Avoid A when doing B
- Always include error handling

## Resources

- Official Docs: https://example.com
- GitHub: https://github.com/example/my-package
```

**metadata.json:**
```json
{
  "name": "my-simple-skill",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "tags": ["simple", "package", "tool"],
  "entry_point_tokens": 40,
  "full_tokens": 800,
  "requires": ["my-package"],
  "author": "your-github-username",
  "license": "MIT"
}
```

---

### Standard Skill Template

**Use for**: Most skills (100-800 lines)

**File**: `standard-skill-template/SKILL.md`

```markdown
---
name: my-framework
description: Framework description with capabilities and use cases
version: 1.0.0
category: toolchain
toolchain: python
author: your-github-username
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Compressed capabilities: feature1, feature2, feature3, integrations"
    when_to_use: "Use case 1, use case 2, use case 3, specific scenarios"
    quick_start: "1. Install package 2. Create app 3. Define routes 4. Run server"
context_limit: 800
tags:
  - framework
  - web
  - api
  - async
requires_tools: []
---

# My Framework

## Overview

Comprehensive explanation of the framework, its purpose, key features, and when to use it.

**Key Features**:
- Feature 1
- Feature 2
- Feature 3

**Best for**: Specific use cases

**Performance**: Performance characteristics

## Quick Start

### Installation

```bash
# Install framework
pip install my-framework

# Install dev dependencies
pip install my-framework[dev]
```

### Minimal Example (Self-Contained)

```python
"""
Minimal My Framework application.
Demonstrates: basic setup, routing, running server.
"""
from my_framework import App

app = App()

@app.route("/")
def home():
    """Home route."""
    return {"message": "Hello, World!"}

@app.route("/items/{item_id}")
def get_item(item_id: int):
    """Get item by ID."""
    return {"item_id": item_id}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

**Run it:**
```bash
python main.py
# Visit: http://localhost:8000
```

## Core Patterns

### Pattern 1: [Most Common Use Case]

[30-50 line complete, working example with comments]

### Pattern 2: [Second Most Common Use Case]

[30-50 line complete, working example with comments]

### Pattern 3: [Third Most Common Use Case]

[30-50 line complete, working example with comments]

## Advanced Usage

### Advanced Pattern 1: [Complex Integration]

[50-80 line complex example with error handling]

### Advanced Pattern 2: [Performance Optimization]

[50-80 line example demonstrating optimization]

## Best Practices

### 1. [Practice Category]

**Guideline**: Specific guideline

**Rationale**: Why this matters

**Example**:
```python
# Good example
```

### 2. [Another Practice Category]

**Guideline**: Another guideline

**Rationale**: Why this matters

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **skill-name**: Brief description
  - *Use case*: Specific integration
  - *Integration*: How they work together
  - *Status*: Optional/Recommended

*Note: All complementary skills are independently deployable. This skill is fully functional without them.*

## Troubleshooting

### Issue 1: [Common Problem]

**Symptoms**: What user sees

**Cause**: Why it happens

**Solution**: How to fix
```bash
# Fix commands
```

### Issue 2: [Another Common Problem]

**Symptoms**: What user sees

**Cause**: Why it happens

**Solution**: How to fix

## Resources

**Official Documentation**:
- Docs: https://example.com/docs
- API Reference: https://example.com/api
- GitHub: https://github.com/example/my-framework

**Community**:
- Discord: https://discord.gg/example
- Forum: https://forum.example.com

---

**Version**: 1.0.0
**Last Updated**: 2025-12-02
**Self-Containment**: ✅ Fully Compliant
```

**metadata.json:**
```json
{
  "name": "my-framework",
  "version": "1.0.0",
  "category": "toolchain",
  "toolchain": "python",
  "framework": "my-framework",
  "tags": [
    "framework",
    "web",
    "api",
    "async",
    "routing"
  ],
  "entry_point_tokens": 180,
  "full_tokens": 4500,
  "requires": [
    "my-framework"
  ],
  "author": "your-github-username",
  "updated": "2025-12-02",
  "license": "MIT"
}
```

---

### Progressive Disclosure Template

**Use for**: Skills needing structured entry points

**Key sections to include:**

```yaml
---
name: skill-name
description: One-line description with use cases
version: 1.0.0
progressive_disclosure:
  entry_point:
    summary: "Keyword-dense summary (60-80 tokens)"
    when_to_use: "Specific trigger scenarios (40-60 tokens)"
    quick_start: "1. Step 2. Step 3. Step 4. Step 5. Command"
context_limit: 800
tags: [tag1, tag2, tag3]
---
```

**Entry point writing checklist:**

- [ ] Summary uses commas, not sentences
- [ ] Summary is 60-80 tokens
- [ ] when_to_use has specific triggers
- [ ] when_to_use is 40-60 tokens
- [ ] quick_start has 3-5 numbered steps
- [ ] quick_start includes exact commands
- [ ] Total entry point is 140-200 tokens

---

### Reference to good-self-contained-skill Example

**Location**: `examples/good-self-contained-skill/`

**What it demonstrates:**

✅ **Self-Containment**:
- No relative paths
- All essential patterns inlined
- Complete examples
- No external skill dependencies

✅ **Structure**:
- Clear section organization
- Progressive complexity
- Graceful degradation

✅ **Examples**:
- Complete, runnable code
- Error handling included
- Comments explaining patterns

✅ **Complementary Skills Section**:
- Informational references only
- Optional status clearly stated
- Integration points described

**Use as template**: Copy structure and adapt to your skill.

**Compare with**: `examples/bad-interdependent-skill/` to see anti-patterns.

---

## Summary

### Key Takeaways

1. **Self-Containment is #1 Priority**
   - Inline 80% use case
   - No relative paths
   - No skill dependencies
   - Works in flat directory

2. **Progressive Disclosure Enables Scale**
   - Entry point: 140-200 tokens
   - Full docs: 3,000-6,000 tokens
   - 99.7% token savings

3. **Complete Examples Matter**
   - Runnable, not fragments
   - Include error handling
   - Comment non-obvious parts
   - 30-50 lines per pattern

4. **Structure Improves Usability**
   - Overview → Quick Start → Core → Advanced
   - Progressive complexity
   - Clear section organization
   - Easy to scan

5. **Testing Ensures Quality**
   - Test in isolation (flat directory)
   - Verify examples work
   - Check token budgets
   - Test in Claude Code

### Getting Started

**Your first skill in 3 steps:**

1. **Copy template**:
   ```bash
   cp -r examples/good-self-contained-skill/ my-new-skill/
   ```

2. **Adapt to your content**:
   - Replace YAML frontmatter
   - Update overview and quick start
   - Add your patterns (20-50 lines each)
   - Include best practices

3. **Test and submit**:
   ```bash
   ./verify-skill.sh my-new-skill/
   # Complete PR checklist
   # Submit PR
   ```

### Resources

- **[Self-Containment Standard](SKILL_SELF_CONTAINMENT_STANDARD.md)**: Complete self-containment requirements
- **[PR Checklist](SKILL_CREATION_PR_CHECKLIST.md)**: Verification checklist for submissions
- **[Versioning Policy](VERSIONING.md)**: Semantic versioning for skills
- **[Contributing Guide](../CONTRIBUTING.md)**: General contribution guidelines
- **[Examples](../examples/)**: Good and bad examples side-by-side

### Questions?

- **GitHub Discussions**: https://github.com/bobmatnyc/claude-mpm-skills/discussions
- **Issues**: Tag with `question` label
- **Community**: [Discord/Slack link if available]

---

**Ready to create your first skill?** Start with the [Quick Start](#quick-start) section!

---

**Document Metadata**:
- **Version**: 1.0.0
- **Last Updated**: 2025-12-02
- **Author**: Claude MPM Team
- **License**: MIT
- **Based on**: Research analysis 2025-12-02
