# Bundle Deployment Examples

Real-world deployment scenarios demonstrating flat and hierarchical modes.

## Quick Start

```bash
# Navigate to any bundle
cd .bundles/python-testing-stack

# Validate before deployment
./deploy.sh --validate

# Deploy to .claude directory
./deploy.sh --flat ~/.claude/
```

## Example 1: Python Testing Stack (Flat Deployment)

**Scenario**: Set up complete testing toolkit for Python project

```bash
cd .bundles/python-testing-stack
./deploy.sh --flat ~/.claude/
```

**Result**:
```
~/.claude/
├── pytest/                          # From toolchains/python/testing/pytest
├── asyncio/                         # From toolchains/python/async/asyncio
├── test-driven-development/         # From universal/testing/test-driven-development
├── systematic-debugging/            # From universal/debugging/systematic-debugging
├── verification-before-completion/  # From universal/debugging/verification-before-completion
└── .bundle-manifest-python-testing-stack.json
```

**Deployment Manifest**:
```json
{
  "bundle": "python-testing-stack",
  "mode": "--flat",
  "deployed_at": "2025-11-30T03:44:38Z",
  "skills_count": 5,
  "deployed_count": 5,
  "skipped_count": 0,
  "target_dir": "~/.claude/"
}
```

**Usage in Claude Code**:
- Skills auto-discovered in `.claude/` directory
- Progressive loading: entry points load first (~400 tokens)
- Full documentation expands on-demand (~18,000 tokens total)

## Example 2: React Ecosystem (Production Deployment)

**Scenario**: Deploy React stack to production project

```bash
# In your project directory
cd myapp/
mkdir -p .claude/

# Deploy React bundle
/path/to/claude-mpm-skills/.bundles/react-ecosystem/deploy.sh --flat ./.claude/
```

**Result**:
```
myapp/.claude/
├── react/
├── zustand/
├── tanstack-query/
├── jest/
├── vitest/
├── test-driven-development/
└── .bundle-manifest-react-ecosystem.json
```

**Project Integration**:
```typescript
// Skills available in Claude Code for this project
// Use TDD workflow with React components
import { create } from 'zustand';  // Zustand patterns from skill
import { useQuery } from '@tanstack/react-query';  // TanStack Query from skill

// Jest/Vitest patterns available for testing
describe('Component', () => {
  // Testing patterns from jest/vitest skills
});
```

## Example 3: Multiple Bundles (Layered Deployment)

**Scenario**: Full-stack TypeScript project needs multiple stacks

```bash
cd myapp/.claude/

# Deploy TypeScript data layer
/path/to/.bundles/typescript-data-stack/deploy.sh --flat ./

# Deploy React frontend
/path/to/.bundles/react-ecosystem/deploy.sh --flat ./

# Deploy universal development practices
/path/to/.bundles/universal-development/deploy.sh --flat ./
```

**Result**:
```
myapp/.claude/
├── drizzle/                    # TypeScript data stack
├── kysely/
├── prisma/
├── zod/
├── database-migration/
├── react/                      # React ecosystem
├── zustand/
├── tanstack-query/
├── jest/
├── vitest/
├── test-driven-development/    # Universal (shared)
├── systematic-debugging/       # Universal (shared)
├── verification-before-completion/
├── software-patterns/
├── git-workflow/
├── writing-plans/
├── .bundle-manifest-typescript-data-stack.json
├── .bundle-manifest-react-ecosystem.json
└── .bundle-manifest-universal-development.json
```

**Note**: `test-driven-development` appears in multiple bundles but only deployed once (idempotent).

## Example 4: Validation Before Deployment

**Scenario**: Verify bundle integrity before deploying to production

```bash
cd .bundles/ai-mcp-development

# Validate all skills exist
./deploy.sh --validate
```

**Success Output**:
```
[INFO] Bundle: ai-mcp-development
[INFO] Mode: --validate
[INFO] Target: ~/.claude

[SUCCESS] Found: toolchains/ai/protocols/mcp
[SUCCESS] Found: toolchains/ai/sdks/anthropic
[SUCCESS] Found: toolchains/ai/frameworks/langchain
[SUCCESS] Found: toolchains/ai/frameworks/dspy
[SUCCESS] Found: toolchains/ai/frameworks/langgraph
[SUCCESS] Found: toolchains/ai/techniques/session-compression

[INFO] Summary: 6 found, 0 missing

[SUCCESS] Validation passed: all skills found
```

**Failure Example** (missing skill):
```
[ERROR] Missing: toolchains/ai/frameworks/missing-skill

[INFO] Summary: 5 found, 1 missing

[ERROR] Validation failed: 1 missing skills
```

## Example 5: Team Deployment (Shared Skills)

**Scenario**: Multiple team members deploy same bundle

**Developer 1**:
```bash
./deploy.sh --flat ~/.claude/
```

**Developer 2** (later):
```bash
./deploy.sh --flat ~/.claude/
```

**Output** (idempotent):
```
[SUCCESS] Deployed: skill1
[WARNING] Skipped: skill2 (already exists)
[WARNING] Skipped: skill3 (already exists)
...

[INFO] Deployment complete
[SUCCESS] Deployed: 1 skills
[WARNING] Skipped: 5 skills (already exist)
```

**Behavior**: Existing skills are preserved, only new skills deployed.

## Example 6: Hierarchical Deployment (Advanced)

**Scenario**: Archive bundle with preserved directory structure

```bash
cd .bundles/python-testing-stack

# Deploy with hierarchy preserved
./deploy.sh --hierarchical ~/skill-archive/
```

**Result**:
```
~/skill-archive/
├── toolchains/
│   └── python/
│       ├── testing/
│       │   └── pytest/
│       └── async/
│           └── asyncio/
└── universal/
    ├── testing/
    │   └── test-driven-development/
    └── debugging/
        ├── systematic-debugging/
        └── verification-before-completion/
```

**Use Case**: Backup, archive, or preserving original structure.

## Example 7: CI/CD Deployment

**Scenario**: Automated deployment in CI pipeline

```bash
#!/bin/bash
# deploy-skills.sh - CI deployment script

set -euo pipefail

BUNDLE_REPO="/path/to/claude-mpm-skills"
BUNDLES=("python-testing-stack" "python-web-stack")

for bundle in "${BUNDLES[@]}"; do
  echo "Deploying $bundle..."

  # Validate first
  "$BUNDLE_REPO/.bundles/$bundle/deploy.sh" --validate

  # Deploy if validation passes
  "$BUNDLE_REPO/.bundles/$bundle/deploy.sh" --flat ~/.claude/
done

echo "All bundles deployed successfully"
```

**GitHub Actions Example**:
```yaml
name: Deploy Skills
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          repository: bobmatnyc/claude-mpm-skills

      - name: Deploy Python Testing Stack
        run: |
          cd .bundles/python-testing-stack
          ./deploy.sh --validate
          ./deploy.sh --flat ~/.claude/
```

## Deployment Manifest Format

Each deployment creates a JSON manifest:

```json
{
  "bundle": "bundle-name",
  "mode": "--flat",
  "deployed_at": "2025-11-30T03:44:38Z",
  "skills_count": 6,
  "deployed_count": 6,
  "skipped_count": 0,
  "target_dir": "/path/to/deployment"
}
```

**Fields**:
- `bundle`: Bundle identifier
- `mode`: Deployment mode (--flat or --hierarchical)
- `deployed_at`: ISO 8601 timestamp
- `skills_count`: Total skills in bundle
- `deployed_count`: Newly deployed skills
- `skipped_count`: Already-existing skills
- `target_dir`: Deployment target directory

## Bundle Comparison

| Bundle | Skills | Primary Use | Recommended For |
|--------|--------|-------------|-----------------|
| python-testing-stack | 5 | Testing | Python projects with test requirements |
| python-web-stack | 6 | Web APIs | FastAPI/Django backends |
| python-data-stack | 5 | Data processing | ETL, data validation |
| typescript-data-stack | 5 | Database | Node.js with TypeScript ORM |
| react-ecosystem | 6 | Frontend | React SPAs with state management |
| nextjs-production-stack | 6 | Full-stack | Next.js applications |
| universal-development | 6 | Methodology | Any software project |
| ai-mcp-development | 6 | AI apps | Claude-powered applications |

## Deployment Best Practices

1. **Always Validate First**
   ```bash
   ./deploy.sh --validate  # Before deployment
   ```

2. **Use Flat Mode for Claude Code**
   ```bash
   ./deploy.sh --flat ~/.claude/  # Recommended
   ```

3. **Deploy to Project Directory**
   ```bash
   ./deploy.sh --flat ./myproject/.claude/  # Project-specific
   ```

4. **Layer Bundles for Complete Stacks**
   - Deploy base stack first (e.g., python-web-stack)
   - Add testing stack (e.g., python-testing-stack)
   - Add universal practices (e.g., universal-development)

5. **Check Manifests After Deployment**
   ```bash
   cat ~/.claude/.bundle-manifest-*.json
   ```

6. **Re-run for Updates** (idempotent)
   ```bash
   # Safe to re-run - skips existing skills
   ./deploy.sh --flat ~/.claude/
   ```

## Troubleshooting

**Issue**: Skills not found in Claude Code
**Solution**: Verify skills deployed to `~/.claude/` (Claude Code default)

**Issue**: Validation fails with missing skills
**Solution**: Check skill paths in `skills.list` are correct

**Issue**: Deployment skips all skills
**Solution**: Normal if skills already deployed (idempotent behavior)

**Issue**: Permission denied
**Solution**: Ensure deployment script is executable (`chmod +x deploy.sh`)

## Performance Notes

**Deployment Speed**:
- Small bundle (5 skills): ~1 second
- Large bundle (6 skills): ~2 seconds
- Multiple bundles: ~3-5 seconds total

**Disk Space**:
- Average skill: 30-50 KB
- Small bundle: ~150-250 KB
- Large bundle: ~300-400 KB
- All 8 bundles: ~2-3 MB total

**Token Budget** (Progressive Loading):
- Entry points: ~60-95 tokens per skill
- Small bundle entries: ~300-475 tokens
- Large bundle entries: ~360-570 tokens
- Full bundle loaded: ~15,000-20,000 tokens
