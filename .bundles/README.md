# Ecosystem Bundles

Curated skill bundles for efficient deployment of complete development stacks.

## Bundle Philosophy

**Flat Deployment by Default**: All bundles deploy as flat skill collections in `.claude/` for maximum compatibility with Claude Code's skill system. The hierarchical source structure exists only for organization.

## Available Bundles

### Python Ecosystem
- **python-testing-stack**: pytest, asyncio, test-driven-development
- **python-web-stack**: FastAPI, Pydantic, SQLAlchemy, Celery
- **python-data-stack**: Pydantic, SQLAlchemy, database migrations

### Golang Ecosystem
- **golang-web-stack**: Go HTTP + gRPC + data access + testing + observability

### TypeScript/JavaScript Ecosystem
- **typescript-data-stack**: Kysely, Drizzle, Prisma, database migrations
- **react-ecosystem**: React, Zustand, TanStack Query, Jest, Vitest
- **nextjs-production-stack**: Next.js, React, TypeScript patterns

### Universal Development
- **universal-development**: TDD, systematic debugging, verification standards

### AI/MCP Development
- **ai-mcp-development**: MCP, Anthropic SDK, LangChain, DSPy, LangGraph

## Quick Start

```bash
# Deploy a bundle (flat mode - recommended)
cd .bundles/python-testing-stack
./deploy.sh --flat ~/.claude/

# Deploy with hierarchical structure (advanced)
./deploy.sh --hierarchical ~/.claude/

# Validate bundle before deployment
./deploy.sh --validate
```

## Bundle Structure

Each bundle contains:
- **BUNDLE.md**: Metadata, purpose, compatibility matrix
- **skills.list**: List of included skill paths with versions
- **deploy.sh**: Deployment script with validation

## Creating New Bundles

1. Create bundle directory: `.bundles/my-stack/`
2. Copy template files from `python-testing-stack/`
3. Edit `skills.list` with your skill paths
4. Update `BUNDLE.md` with metadata
5. Test deployment: `./deploy.sh --validate`

## Design Principles

- **Single Deployment Mode**: Flat deployment for all bundles
- **Version Pinning**: All skills referenced with versions
- **Validation**: Pre-deployment checks for missing skills
- **Idempotent**: Safe to run multiple times
- **Minimal Dependencies**: Self-contained deployment scripts
