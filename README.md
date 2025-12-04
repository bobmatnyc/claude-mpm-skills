# Claude MPM Skills

> Production-ready Claude Code skills for intelligent project development

## Overview

This repository contains a comprehensive collection of **191 Claude Code skills** designed for the Claude Multi-Agent Project Manager (MPM) ecosystem. Skills cover modern development workflows with **95%+ coverage** across Python, TypeScript, JavaScript, PHP, Rust, AI, and universal tooling.

## What is Claude MPM?

**Claude MPM (Multi-Agent Project Manager)** is an advanced orchestration framework that runs within Claude Code (Anthropic's official CLI). It enables:

- **Multi-Agent Coordination**: Specialized agents for different tasks (research, engineering, QA, ops)
- **Intelligent Delegation**: PM agent coordinates work across specialist agents
- **Context Management**: Efficient token usage with progressive disclosure
- **Skill System**: Modular, reusable knowledge bases (this repository)

**Key Components:**
- **Claude Code**: Anthropic's official CLI environment
- **Claude MPM**: Multi-agent framework running in Claude Code
- **Skills**: Domain-specific knowledge modules (this repo contains 191 skills)

**How They Work Together:**
```
Claude Code (CLI)
    ↓
Claude MPM (Multi-Agent Framework)
    ↓
Skills (Knowledge Modules) ← You are here
```

## Features

- **Progressive Loading**: Skills load on-demand with 60-95 token entry points, expanding to 3,000-6,000 tokens
- **Token Efficiency**: 98.2% token savings during discovery phase
- **Toolchain Detection**: Automatically deploy relevant skills based on project type
- **Production-Ready**: All skills include real-world examples, best practices, and troubleshooting
- **Research-Backed**: Built on latest 2025 techniques and industry patterns

## Quick Stats

- **Total Skills**: 191 production-ready skills
- **Coverage**: 95%+ of modern development workflows
- **Token Efficiency**: ~7,120 entry tokens vs ~400,500 full tokens (98.2% savings)
- **Categories**: Python, TypeScript, JavaScript, PHP, Rust, Next.js, UI, AI, Platforms, Universal
- **Complete Stacks**: Full-stack TypeScript, Python Web, React Frontend, AI Workflows

## Repository Structure

```
claude-mpm-skills/
├── toolchains/          # Language/framework-specific skills (60 skills)
│   ├── python/         # 10 skills
│   │   ├── frameworks/     # Django, FastAPI, Flask
│   │   ├── testing/        # pytest
│   │   ├── data/           # SQLAlchemy
│   │   ├── async/          # asyncio, Celery
│   │   ├── tooling/        # mypy, pyright
│   │   └── validation/     # Pydantic
│   ├── typescript/     # 12 skills
│   │   ├── frameworks/     # React, Vue, Node.js backend
│   │   ├── testing/        # Vitest, Jest
│   │   ├── data/           # Drizzle, Kysely, Prisma
│   │   ├── validation/     # Zod
│   │   ├── state/          # Zustand, TanStack Query
│   │   ├── api/            # tRPC
│   │   └── build/          # Turborepo
│   ├── javascript/     # 10 skills
│   │   ├── frameworks/     # React, Vue, Svelte, SvelteKit
│   │   ├── testing/        # Playwright
│   │   ├── build/          # Vite
│   │   └── tooling/        # Biome
│   ├── php/            # 6 skills
│   │   ├── frameworks/     # WordPress, EspoCRM
│   │   └── testing/        # PHPUnit, PHPCS
│   ├── rust/           # 2 skills
│   │   └── frameworks/     # Tauri
│   ├── nextjs/         # 2 skills
│   │   ├── core/           # Next.js fundamentals
│   │   └── v16/            # Next.js 16 (Turbopack, cache components)
│   ├── ui/             # 4 skills
│   │   ├── styling/        # Tailwind CSS
│   │   └── components/     # shadcn/ui, DaisyUI, Headless UI
│   ├── ai/             # 7 skills
│   │   ├── sdks/           # Anthropic SDK
│   │   ├── frameworks/     # LangChain, DSPy, LangGraph
│   │   ├── services/       # OpenRouter
│   │   ├── protocols/      # MCP
│   │   └── techniques/     # Session Compression
│   └── platforms/      # 4 skills
│       ├── deployment/     # Vercel, Netlify
│       ├── database/       # Neon
│       └── backend/        # Supabase
└── universal/           # 27 skills
    ├── infrastructure/     # Docker, GitHub Actions
    ├── data/              # GraphQL
    ├── architecture/      # Software patterns
    └── testing/           # TDD, systematic debugging
```

## Complete Skill Catalog

### Python (10 Skills)

**Frameworks**:
- Django - Full-featured web framework with ORM, admin, DRF
- FastAPI - Modern async API framework with automatic OpenAPI
- Flask - Lightweight WSGI framework for microservices

**Testing**:
- pytest - Fixtures, parametrization, plugins, FastAPI/Django integration

**Data & ORM**:
- SQLAlchemy - Modern ORM with 2.0 syntax, async, Alembic migrations

**Async & Background Jobs**:
- asyncio - Async/await patterns, event loops, concurrent programming
- Celery - Distributed task queues, periodic tasks, workflows

**Type Checking**:
- mypy - Static type checker with strict mode
- pyright - Fast type checker with VS Code integration

**Validation**:
- Pydantic - Data validation with type hints, FastAPI/Django integration

### TypeScript (12 Skills)

**Frameworks**:
- React - Hooks, context, performance optimization
- Vue 3 - Composition API, Pinia, TypeScript integration
- Node.js Backend - Express/Fastify with Drizzle/Prisma

**Testing**:
- Vitest - Modern testing with React/Vue
- Jest - TypeScript testing with ts-jest

**Data & ORMs**:
- Drizzle - TypeScript-first ORM with migrations
- Kysely - Type-safe SQL query builder
- Prisma - Next-gen ORM with migrations and client generation

**Validation**:
- Zod - Schema validation with type inference

**State Management**:
- Zustand - Minimal React state management
- TanStack Query - Server state, caching, optimistic updates

**API**:
- tRPC - End-to-end type safety without codegen

**Build Tools**:
- Turborepo - Monorepo with intelligent caching

### JavaScript (10 Skills)

**Frameworks**:
- React - Component patterns (also in TypeScript)
- Vue - Progressive framework (also in TypeScript)
- Svelte - Reactive framework with runes
- SvelteKit - Full-stack Svelte with SSR/SSG

**Testing**:
- Playwright - Cross-browser E2E testing with Page Object Model

**Build Tools**:
- Vite - Fast build tool with HMR

**Tooling**:
- Biome - Fast linter and formatter (Rust-powered)

### PHP (6 Skills)

**WordPress Ecosystem**:
- wordpress-advanced-architecture - REST API, WP-CLI, performance optimization, caching strategies
- wordpress-block-editor - Block themes, FSE architecture, theme.json, custom Gutenberg blocks
- wordpress-testing-qa - PHPUnit integration tests, WP_Mock unit tests, PHPCS coding standards

**Enterprise**:
- espocrm-development - EspoCRM customization, entity management, API extensions
- espocrm-advanced-features - Advanced workflows, complex business logic implementation
- espocrm-deployment - Production deployment, security hardening, performance tuning

### Rust (2 Skills)

**Desktop Applications**:
- tauri - Cross-platform desktop apps with Rust backend, web frontend
- tauri-advanced-events - Bidirectional communication, streaming, custom event handling

### Next.js (2 Skills)

- Next.js Core - App Router, Server Components, Server Actions
- Next.js v16 - Turbopack, cache components, migration guide

### UI & Styling (4 Skills)

**CSS Frameworks**:
- Tailwind CSS - Utility-first CSS with JIT mode

**Component Libraries**:
- shadcn/ui - Copy-paste components with Radix UI + Tailwind
- DaisyUI - Tailwind plugin with 50+ components and themes
- Headless UI - Unstyled accessible primitives for React/Vue

### AI & LLM (7 Skills)

**SDKs**:
- Anthropic SDK - Messages API, streaming, function calling, vision

**Frameworks**:
- LangChain - LCEL, RAG, agents, chains, memory
- DSPy - Automatic prompt optimization with MIPROv2
- LangGraph - Stateful multi-agent orchestration

**Services**:
- OpenRouter - Unified LLM API access

**Protocols**:
- MCP - Model Context Protocol

**Techniques**:
- Session Compression - Context window compression, progressive summarization

### Platforms (4 Skills)

**Deployment**:
- Vercel - Next.js deployment, Edge Functions, serverless
- Netlify - JAMstack, Forms, Identity, Edge Functions

**Database**:
- Neon - Serverless Postgres with branching

**Backend**:
- Supabase - Postgres + Auth + Storage + Realtime + RLS

### Universal (27 Skills)

**Infrastructure**:
- Docker - Containerization, multi-stage builds, compose
- GitHub Actions - CI/CD workflows, matrix strategies, deployments

**Data**:
- GraphQL - Schema-first APIs, Apollo, resolvers, subscriptions

**Architecture**:
- Software Patterns - Design patterns, anti-patterns, decision trees

**Testing & Debugging**:
- TDD - Test-driven development workflows
- Systematic Debugging - Root cause analysis

## Installation

### Prerequisites

- **Claude Code** (Anthropic's official CLI)
- **Claude MPM** framework

### Step 1: Install Claude MPM

```bash
# Install via pip (recommended)
pip install claude-mpm

# Or install via Homebrew (macOS)
brew tap bobmatnyc/tools
brew install claude-mpm

# Or install from source
git clone https://github.com/bobmatnyc/claude-mpm.git
cd claude-mpm
pip install -e .
```

### Step 2: Initialize Claude MPM in Your Project

```bash
# Navigate to your project directory
cd your-project

# Initialize Claude MPM
/mpm-init
```

This creates `.claude-mpm/` directory with configuration and agent setup.

### Step 3: Deploy Skills (Automatic)

```bash
# Auto-detect your project stack and deploy relevant skills
/mpm-auto-configure

# Or use the agent auto-configuration
/mpm-agents-auto-configure
```

Skills are automatically selected based on:
- `package.json` → TypeScript/JavaScript skills
- `pyproject.toml` → Python skills
- Framework configs → Next.js, React, Django, FastAPI
- Dependencies → AI frameworks (LangChain, Anthropic)

### Step 4: Verify Installation

```bash
# Check MPM status
/mpm-status

# List available skills
/mpm-agents-list

# View deployed agents
/mpm-agents
```

### Manual Skill Installation (Alternative)

Clone this repository to make skills available to Claude MPM:

```bash
# Clone skills repository
git clone https://github.com/bobmatnyc/claude-mpm-skills.git

# Link to Claude MPM skills directory
ln -s $(pwd)/claude-mpm-skills ~/.claude-mpm/skills
```

## Usage

### Automatic Deployment (Recommended)

```bash
# Initialize project with Claude MPM
/mpm-init

# Or use auto-configuration to detect toolchain
/mpm-auto-configure

# Deploy recommended skills based on project detection
/mpm-agents-auto-configure
```

Skills are automatically deployed based on detected toolchain:
- `package.json` → TypeScript/JavaScript skills
- `pyproject.toml` or `requirements.txt` → Python skills
- Framework configs → Next.js, React, Django, FastAPI skills
- AI dependencies → LangChain, Anthropic, DSPy skills

### Manual Skill Access

Skills use progressive loading - entry points load first for quick reference:

```markdown
---
progressive_disclosure:
  entry_point:
    summary: "Brief description (60-95 tokens)"
    when_to_use:
      - "Use case 1"
      - "Use case 2"
    quick_start:
      - "Step 1"
      - "Step 2"
---
```

Full documentation expands on-demand when needed.

## Complete Development Stacks

### Full-Stack TypeScript
```
Next.js + tRPC + TanStack Query + Zustand + Zod + Prisma +
Tailwind + shadcn/ui + Turborepo + Docker + GitHub Actions
```
**Coverage**: 100% - All skills available

### Python Web Development
```
FastAPI/Django + Pydantic + SQLAlchemy + Celery +
pytest + mypy + Docker + GitHub Actions
```
**Coverage**: 100% - All skills available

### Modern React Frontend
```
React + TanStack Query + Zustand + Tailwind + shadcn/ui +
Vite + Vitest + Playwright
```
**Coverage**: 100% - All skills available

### AI/LLM Applications
```
Anthropic SDK + LangChain + DSPy + LangGraph +
Session Compression + OpenRouter + MCP
```
**Coverage**: 100% - All skills available

## Progressive Loading Design

Skills use a two-tier structure for optimal token efficiency:

### Entry Point (60-95 tokens)
- Skill name and summary
- When to use (3-5 scenarios)
- Quick start (3-5 steps)

### Full Documentation (3,000-6,000 tokens)
- Complete API reference
- Real-world examples
- Best practices
- Framework integrations
- Production patterns
- Testing strategies
- Troubleshooting

**Token Savings**: 98.2% during discovery (load 191 entry points vs all full docs)

## Performance Benchmarks

- **Discovery Phase**: 15,275 tokens (all 191 entry points) vs 859,500 tokens (all full docs)
- **Token Efficiency**: 98.2% reduction during skill browsing
- **Coverage**: 95%+ of modern development workflows
- **Production Adopters**: Skills based on patterns from JetBlue, Databricks, Walmart, VMware

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Governance**: All merges to main require approval from @bobmatnyc (see [GOVERNANCE.md](GOVERNANCE.md))

### Skill Format Requirements

1. **Progressive Disclosure**: YAML frontmatter with entry_point section
2. **Token Budgets**: Entry 60-95 tokens, Full 3,000-6,000 tokens
3. **Metadata**: Complete metadata.json with tags, related_skills, token estimates
4. **Examples**: Real-world code examples with error handling
5. **Versioning**: Semantic versioning (see [docs/VERSIONING.md](docs/VERSIONING.md))

## Documentation

### User Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Understanding and using Claude Code skills
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Developer Documentation

- **[Skill Creation Guide](docs/SKILL_CREATION_GUIDE.md)** - Building your own skills
- **[Best Practices](docs/SKILL_SELF_CONTAINMENT_STANDARD.md)** - Self-containment standards
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines
- **[Versioning Policy](docs/VERSIONING.md)** - Semantic versioning for skills

### Architecture & Research

- **[Architecture](docs/STRUCTURE.md)** - Repository structure
- **[Research Documents](docs/research/)** - Pattern analysis and guides
  - Python, TypeScript, Ruby, Rust, PHP, Java, Go advanced patterns
  - Skills compliance analysis
  - Coverage analysis

### Reference

- **[PR Checklist](docs/SKILL_CREATION_PR_CHECKLIST.md)** - Submission requirements
- **[GitHub Setup](docs/GITHUB_REPOSITORY_SETUP.md)** - Repository configuration

## License

MIT License - See [LICENSE](LICENSE)

## Links

- **Claude MPM Framework**: https://github.com/bobmatnyc/claude-mpm
- **Claude MPM Documentation**: https://github.com/bobmatnyc/claude-mpm/tree/main/docs
- **Skills Documentation**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Skill Creation Guide**: [docs/SKILL_CREATION_GUIDE.md](docs/SKILL_CREATION_GUIDE.md)
- **Issues**: https://github.com/bobmatnyc/claude-mpm-skills/issues
- **Discussions**: https://github.com/bobmatnyc/claude-mpm-skills/discussions

## Acknowledgments

Built with research from:
- Official framework documentation (2025 versions)
- Industry best practices (JetBlue, Databricks, Walmart, VMware, Replit)
- Academic research (DSPy, LLMLingua, prompt optimization studies)
- Community feedback and contributions

---

**Last Updated**: 2025-12-04
**Skills Count**: 191
**Coverage**: 95%+
**Token Efficiency**: 98.2%
