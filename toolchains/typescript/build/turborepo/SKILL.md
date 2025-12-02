---
name: turborepo
description: High-performance monorepo build system with intelligent caching, task orchestration, and parallel execution for multi-package repositories and microservices.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  token_estimates:
    entry: 70
    full: 5500
---

# Turborepo Skill

## Summary
Turborepo is a high-performance monorepo build system with intelligent caching, task orchestration, and parallel execution. It provides fast incremental builds through content-aware hashing and remote caching, ideal for managing multiple packages, apps, and shared code.

## When to Use
- **Multi-package repositories** with shared dependencies and utilities
- **Microservices architectures** requiring coordinated builds
- **Component libraries** shared across multiple applications
- **Full-stack monorepos** with frontend, backend, and shared packages
- **Teams needing faster CI/CD** through intelligent caching and parallelization

---

## Quick Start

### Installation and Setup
```bash
# Create new Turborepo (recommended)
npx create-turbo@latest

# Or add to existing monorepo
npm install turbo --save-dev

# Initialize Turborepo
npx turbo init
```

### Basic Structure
```
my-turborepo/
├── apps/
│   ├── web/              # Next.js app
│   └── api/              # Express API
├── packages/
│   ├── ui/               # Shared React components
│   ├── config/           # Shared configs (eslint, tsconfig)
│   └── utils/            # Shared utilities
├── turbo.json            # Pipeline configuration
└── package.json          # Root package.json
```

### Essential turbo.json
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Run Tasks
```bash
# Build all packages and apps
turbo run build

# Run tests across workspace
turbo run test

# Run tasks in parallel
turbo run lint test build

# Filter by package
turbo run build --filter=web
turbo run test --filter=@myorg/ui

# Run in specific workspace
turbo run dev --filter=web...
```

---

## Core Concepts

### Monorepo Architecture
Turborepo manages multiple packages in a single repository:
- **apps/**: Application projects (Next.js, Express, etc.)
- **packages/**: Shared libraries and utilities
- **Workspace dependencies**: Internal package references
- **Single version control**: Unified commits and history

### Task Caching
Content-aware hashing for intelligent cache invalidation:
```json
{
  "pipeline": {
    "build": {
      "outputs": ["dist/**", ".next/**"],
      "inputs": ["src/**", "package.json"]
    }
  }
}
```
- **Cache hits**: Instant task completion (0ms)
- **Local cache**: `.turbo/cache` directory
- **Remote cache**: Shared across team (Vercel, custom)
- **Cache invalidation**: Automatic on file changes

### Pipeline Configuration
Define task dependencies and execution order:
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],        // Dependencies first
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"],         // After local build
      "outputs": ["coverage/**"]
    },
    "deploy": {
      "dependsOn": ["build", "test"], // Multiple dependencies
      "outputs": []
    }
  }
}
```

**Dependency Operators**:
- `^build`: Run dependencies' build tasks first (topological)
- `build`: Run local build task first
- No prefix: Run in parallel

---

## Project Structure

### Complete Monorepo Example
```
turborepo-example/
├── apps/
│   ├── web/                      # Next.js app
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── admin/                    # Admin dashboard
│   │   ├── src/
│   │   └── package.json
│   └── api/                      # Express API
│       ├── src/
│       └── package.json
├── packages/
│   ├── ui/                       # Component library
│   │   ├── src/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── config/                   # Shared configs
│   │   ├── eslint-config/
│   │   ├── tsconfig/
│   │   └── tailwind-config/
│   ├── utils/                    # Shared utilities
│   │   ├── src/
│   │   │   ├── format.ts
│   │   │   ├── validators.ts
│   │   │   └── index.ts
│   │   └── package.json
│   └── types/                    # Shared TypeScript types
│       ├── src/
│       └── package.json
├── .turbo/                       # Cache directory
├── turbo.json                    # Pipeline config
├── package.json                  # Root package
├── pnpm-workspace.yaml           # Workspace definition
└── tsconfig.json                 # Root TypeScript config
```

### Workspace Configuration

**Root package.json**:
```json
{
  "name": "my-turborepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "clean": "turbo run clean && rm -rf node_modules .turbo"
  },
  "devDependencies": {
    "turbo": "latest"
  },
  "engines": {
    "node": ">=18",
    "pnpm": ">=8"
  },
  "packageManager": "pnpm@8.10.0"
}
```

**pnpm-workspace.yaml**:
```yaml
packages:
  - "apps/*"
  - "packages/*"
```

---

## Package Manager Integration

### pnpm (Recommended)
Fast, efficient, and workspace-native:
```bash
# Install dependencies
pnpm install

# Add dependency to specific package
pnpm add react --filter=web
pnpm add @myorg/ui --filter=admin

# Add workspace dependency
cd apps/web
pnpm add @myorg/ui@workspace:*

# Run scripts
pnpm turbo run build
```

**pnpm-workspace.yaml**:
```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### npm Workspaces
```json
{
  "workspaces": ["apps/*", "packages/*"]
}
```

```bash
npm install
npm run build --workspace=web
npm run test --workspaces
```

### Yarn Workspaces
```json
{
  "workspaces": {
    "packages": ["apps/*", "packages/*"]
  }
}
```

```bash
yarn install
yarn workspace web build
yarn workspaces run test
```

---

## turbo.json Configuration

### Complete Configuration
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "globalEnv": ["NODE_ENV", "API_URL"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"],
      "env": ["NEXT_PUBLIC_API_URL"],
      "outputMode": "new-only"
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**", "test/**", "__tests__/**"]
    },
    "test:unit": {
      "dependsOn": [],
      "outputs": [],
      "cache": false
    },
    "lint": {
      "dependsOn": [],
      "outputs": []
    },
    "type-check": {
      "dependsOn": [],
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "clean": {
      "cache": false
    }
  }
}
```

### Pipeline Options

**dependsOn**: Task dependencies
```json
{
  "build": {
    "dependsOn": ["^build"]        // Run dependencies' build first
  },
  "test": {
    "dependsOn": ["build"]         // Run local build first
  },
  "deploy": {
    "dependsOn": ["build", "test"] // Multiple tasks
  }
}
```

**outputs**: Files to cache
```json
{
  "build": {
    "outputs": [
      "dist/**",           // Output directory
      ".next/**",          // Next.js build
      "!.next/cache/**"    // Exclude cache
    ]
  }
}
```

**inputs**: Files that invalidate cache
```json
{
  "build": {
    "inputs": [
      "src/**",            // Source files
      "package.json",      // Dependencies
      "tsconfig.json"      // Config files
    ]
  }
}
```

**env**: Environment variables affecting cache
```json
{
  "build": {
    "env": [
      "NEXT_PUBLIC_API_URL",
      "DATABASE_URL"
    ]
  }
}
```

**outputMode**: Control console output
```json
{
  "build": {
    "outputMode": "new-only"  // Only show new output
    // "full" | "hash-only" | "new-only" | "errors-only" | "none"
  }
}
```

**cache**: Enable/disable caching
```json
{
  "dev": {
    "cache": false,          // Don't cache dev server
    "persistent": true       // Keep process running
  }
}
```

### Global Configuration

**globalDependencies**: Files affecting all tasks
```json
{
  "globalDependencies": [
    ".env",
    "tsconfig.json",
    "package.json"
  ]
}
```

**globalEnv**: Environment variables for all tasks
```json
{
  "globalEnv": [
    "NODE_ENV",
    "CI",
    "VERCEL"
  ]
}
```

---

## Task Execution

### Running Tasks
```bash
# Run single task
turbo run build
turbo run test
turbo run lint

# Run multiple tasks
turbo run build test lint

# Run in specific order (sequential)
turbo run build && turbo run test && turbo run deploy
```

### Filtering and Scoping

**Filter by package**:
```bash
# Single package
turbo run build --filter=web
turbo run test --filter=@myorg/ui

# Multiple packages
turbo run build --filter=web --filter=admin
turbo run build --filter={web,admin}
```

**Include dependencies**:
```bash
# Package and its dependencies
turbo run build --filter=web...

# Package and its dependents
turbo run test --filter=...@myorg/ui
```

**Filter by directory**:
```bash
# All apps
turbo run build --filter=./apps/*

# Specific directory
turbo run test --filter=./packages/ui
```

**Filter by git changes**:
```bash
# Changed since main
turbo run build --filter=[main]

# Changed in last commit
turbo run test --filter=[HEAD^1]

# Changed packages only
turbo run lint --filter=[origin/main]
```

### Execution Options

**Parallel execution**:
```bash
# Control concurrency
turbo run build --concurrency=4
turbo run test --concurrency=50%

# Unlimited parallel (default)
turbo run lint --concurrency=100%
```

**Force execution** (bypass cache):
```bash
turbo run build --force
turbo run test --force
```

**Continue on error**:
```bash
turbo run test --continue
```

**Output modes**:
```bash
turbo run build --output-logs=new-only
turbo run test --output-logs=errors-only
turbo run lint --output-logs=full
```

**Dry run**:
```bash
turbo run build --dry
turbo run build --dry=json
```

**Environment modes**:
```bash
turbo run build --env-mode=strict    # Error on missing env vars
turbo run build --env-mode=loose     # Allow missing env vars
```

---

## Caching

### Local Cache
Automatic file-based caching in `.turbo/cache`:
```bash
# First run: Full execution
turbo run build
# >>> FULL TURBO
# >>> build: cache miss, executing...

# Second run: Cache hit
turbo run build
# >>> FULL TURBO
# >>> build: cache hit, replaying output...
```

Cache structure:
```
.turbo/
├── cache/
│   ├── abc123.tar.zst    # Compressed outputs
│   └── def456.tar.zst
└── runs/
    └── xyz789.json       # Run metadata
```

### Remote Cache (Vercel)
Share cache across team and CI:
```bash
# Link to Vercel
npx turbo login
npx turbo link

# Runs will now use remote cache
turbo run build
# >>> Remote caching enabled
```

**turbo.json** with remote cache:
```json
{
  "remoteCache": {
    "enabled": true
  }
}
```

### Custom Remote Cache
Self-hosted cache server:
```bash
# Configure custom cache
turbo run build --api="https://cache.mycompany.com" --token="${TURBO_TOKEN}"
```

**Environment variables**:
```bash
export TURBO_API="https://cache.mycompany.com"
export TURBO_TOKEN="your-secret-token"
export TURBO_TEAM="team-id"
```

### Cache Configuration

**Disable caching**:
```json
{
  "pipeline": {
    "dev": {
      "cache": false
    }
  }
}
```

**Cache signatures** (what affects cache):
- Input files (source code, configs)
- Environment variables (env)
- Dependencies' outputs (dependsOn)
- Global dependencies (globalDependencies)
- Task configuration (turbo.json)

**Invalidate cache**:
```bash
# Delete local cache
rm -rf .turbo/cache

# Force rebuild
turbo run build --force
```

---

## Code Sharing

### Internal Packages

**Shared component library**:
```
packages/ui/
├── src/
│   ├── Button.tsx
│   ├── Input.tsx
│   └── index.ts
├── package.json
└── tsconfig.json
```

**packages/ui/package.json**:
```json
{
  "name": "@myorg/ui",
  "version": "0.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./button": "./src/Button.tsx"
  },
  "scripts": {
    "lint": "eslint src/",
    "type-check": "tsc --noEmit"
  },
  "devDependencies": {
    "react": "^18.0.0",
    "typescript": "^5.0.0"
  }
}
```

**packages/ui/src/index.ts**:
```typescript
export { Button } from './Button';
export { Input } from './Input';
export type { ButtonProps, InputProps } from './types';
```

**Using in apps**:
```json
{
  "dependencies": {
    "@myorg/ui": "workspace:*"
  }
}
```

```typescript
import { Button, Input } from '@myorg/ui';
```

### Shared Configuration

**ESLint config package**:
```
packages/config/eslint-config/
├── index.js
├── package.json
└── README.md
```

**package.json**:
```json
{
  "name": "@myorg/eslint-config",
  "version": "0.0.0",
  "main": "index.js",
  "dependencies": {
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
```

**index.js**:
```javascript
module.exports = {
  extends: ['next', 'prettier'],
  rules: {
    '@next/next/no-html-link-for-pages': 'off',
  },
};
```

**Using in apps**:
```json
{
  "devDependencies": {
    "@myorg/eslint-config": "workspace:*"
  }
}
```

**.eslintrc.js**:
```javascript
module.exports = {
  extends: ['@myorg/eslint-config'],
};
```

### TypeScript Configuration

**Shared tsconfig**:
```
packages/config/tsconfig/
├── base.json
├── nextjs.json
├── react-library.json
└── package.json
```

**base.json**:
```json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "incremental": true
  }
}
```

**nextjs.json**:
```json
{
  "extends": "./base.json",
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "module": "esnext",
    "noEmit": true
  }
}
```

**Using in apps**:
```json
{
  "extends": "@myorg/tsconfig/nextjs.json",
  "compilerOptions": {
    "outDir": "dist"
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

### TypeScript Project References

**Root tsconfig.json**:
```json
{
  "files": [],
  "references": [
    { "path": "./apps/web" },
    { "path": "./apps/admin" },
    { "path": "./packages/ui" },
    { "path": "./packages/utils" }
  ]
}
```

**Package tsconfig.json**:
```json
{
  "extends": "@myorg/tsconfig/react-library.json",
  "compilerOptions": {
    "composite": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "references": [
    { "path": "../utils" }
  ]
}
```

Build with references:
```bash
tsc --build
turbo run type-check
```

---

## Integration Patterns

### Next.js in Monorepo

**apps/web/package.json**:
```json
{
  "name": "web",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "@myorg/ui": "workspace:*",
    "@myorg/utils": "workspace:*"
  }
}
```

**apps/web/next.config.js**:
```javascript
/** @type {import('next').NextConfig} */
module.exports = {
  transpilePackages: ['@myorg/ui', '@myorg/utils'],
  reactStrictMode: true,
};
```

**turbo.json**:
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### React Component Library

**packages/ui/package.json**:
```json
{
  "name": "@myorg/ui",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src/"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.0.0",
    "react": "^18.0.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  }
}
```

**packages/ui/tsup.config.ts**:
```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  sourcemap: true,
  clean: true,
  external: ['react'],
});
```

### API Packages

**packages/api-client/package.json**:
```json
{
  "name": "@myorg/api-client",
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "test": "vitest run",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@myorg/types": "workspace:*"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "vitest": "^1.0.0"
  }
}
```

**src/client.ts**:
```typescript
import type { User, Post } from '@myorg/types';

export class APIClient {
  constructor(private baseUrl: string) {}

  async getUser(id: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/users/${id}`);
    return response.json();
  }

  async getPosts(): Promise<Post[]> {
    const response = await fetch(`${this.baseUrl}/posts`);
    return response.json();
  }
}
```

---

## Docker Integration

### Pruned Builds
Build only what you need:
```dockerfile
FROM node:18-alpine AS base
RUN npm install -g turbo pnpm

FROM base AS builder
WORKDIR /app
COPY . .
# Prune workspace to only include 'web' app
RUN turbo prune --scope=web --docker

FROM base AS installer
WORKDIR /app
# Copy pruned workspace
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN pnpm install --frozen-lockfile

COPY --from=builder /app/out/full/ .
RUN pnpm turbo run build --filter=web...

FROM base AS runner
WORKDIR /app
COPY --from=installer /app/apps/web/.next/standalone ./
COPY --from=installer /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=installer /app/apps/web/public ./apps/web/public

EXPOSE 3000
CMD ["node", "apps/web/server.js"]
```

### Multi-App Docker
```dockerfile
# Build stage with pruning
FROM node:18-alpine AS builder
RUN npm install -g turbo pnpm
WORKDIR /app
COPY . .

# Prune for specific app (passed as build arg)
ARG APP
RUN turbo prune --scope=${APP} --docker

# Install dependencies
FROM node:18-alpine AS installer
WORKDIR /app
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/pnpm-lock.yaml ./pnpm-lock.yaml
RUN pnpm install --frozen-lockfile

# Build
COPY --from=builder /app/out/full/ .
ARG APP
RUN pnpm turbo run build --filter=${APP}...

# Runtime
FROM node:18-alpine AS runner
ARG APP
WORKDIR /app
COPY --from=installer /app .
CMD pnpm --filter=${APP} start
```

Build:
```bash
docker build --build-arg APP=web -t my-web-app .
docker build --build-arg APP=admin -t my-admin-app .
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        APP: web
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - API_URL=http://api:3001

  admin:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        APP: admin
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=production

  api:
    build:
      context: .
      dockerfile: apps/api/Dockerfile
    ports:
      - "3001:3001"
    environment:
      - DATABASE_URL=postgres://db:5432/mydb

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_PASSWORD: secret
```

---

## CI/CD Integration

### GitHub Actions
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo run build

      - name: Test
        run: pnpm turbo run test

      - name: Lint
        run: pnpm turbo run lint
```

### With Turborepo Remote Cache
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build and test
        run: pnpm turbo run build test lint --cache-dir=.turbo

      - name: Upload cache
        uses: actions/cache@v3
        with:
          path: .turbo
          key: ${{ runner.os }}-turbo-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-turbo-
```

### Changed Files Only
```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build changed packages
        run: pnpm turbo run build --filter=[origin/main]

      - name: Test changed packages
        run: pnpm turbo run test --filter=[origin/main]
```

---

## Deployment Strategies

### Vercel Deployment
Automatic deployment with remote cache:
```json
{
  "buildCommand": "turbo run build",
  "framework": "nextjs",
  "installCommand": "pnpm install",
  "outputDirectory": "apps/web/.next"
}
```

**vercel.json**:
```json
{
  "buildCommand": "turbo run build --filter=web",
  "installCommand": "pnpm install --frozen-lockfile",
  "framework": null,
  "outputDirectory": "apps/web/.next"
}
```

### Deploy Affected Apps
```bash
# Get changed apps since last deploy
CHANGED_APPS=$(turbo run build --filter=[origin/main] --dry=json | jq -r '.packages[]')

# Deploy each changed app
for app in $CHANGED_APPS; do
  echo "Deploying $app..."
  # Your deployment command
done
```

**GitHub Actions example**:
```yaml
- name: Get changed apps
  id: changed
  run: |
    CHANGED=$(pnpm turbo run build --filter=[origin/main] --dry=json | jq -r '.packages | join(",")')
    echo "apps=$CHANGED" >> $GITHUB_OUTPUT

- name: Deploy web
  if: contains(steps.changed.outputs.apps, 'web')
  run: vercel deploy --prod apps/web

- name: Deploy admin
  if: contains(steps.changed.outputs.apps, 'admin')
  run: vercel deploy --prod apps/admin
```

### Docker Deployment
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push Docker image
        run: |
          docker build --build-arg APP=web -t myregistry/web:latest .
          docker push myregistry/web:latest

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/web web=myregistry/web:latest
```

---

## Migration from Single Repo

### Step-by-Step Migration

**1. Initialize Turborepo**:
```bash
# In existing repo
npm install turbo --save-dev
npx turbo init
```

**2. Create workspace structure**:
```bash
mkdir -p apps/web packages/ui
```

**3. Move existing app**:
```bash
# Move current code to apps/web
git mv src apps/web/src
git mv public apps/web/public
git mv package.json apps/web/package.json
```

**4. Update root package.json**:
```json
{
  "name": "monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
```

**5. Configure turbo.json**:
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

**6. Extract shared code**:
```bash
# Create shared package
mkdir -p packages/ui/src

# Move components
mv apps/web/src/components packages/ui/src/

# Update imports in apps/web
```

**7. Install dependencies**:
```bash
pnpm install
```

**8. Test**:
```bash
pnpm turbo run build
pnpm turbo run dev
```

### Gradual Migration Strategy
1. Start with single app in monorepo
2. Extract shared utilities to `packages/utils`
3. Extract UI components to `packages/ui`
4. Add second app (admin, marketing, etc.)
5. Extract common configs
6. Set up remote caching
7. Optimize CI/CD for monorepo

---

## Comparison with Alternatives

### Turborepo vs Nx
| Feature | Turborepo | Nx |
|---------|-----------|-----|
| **Caching** | Content-based | Content-based |
| **Remote cache** | Vercel + custom | Nx Cloud + custom |
| **Complexity** | Minimal config | Feature-rich |
| **Learning curve** | Low | Medium-High |
| **Code generation** | No | Yes (generators) |
| **Best for** | Simple monorepos | Enterprise apps |

### Turborepo vs Lerna
| Feature | Turborepo | Lerna |
|---------|-----------|-------|
| **Caching** | Advanced | Basic |
| **Speed** | Very fast | Slower |
| **Maintenance** | Active | Maintenance mode |
| **Focus** | Build system | Package management |
| **Best for** | Modern monorepos | Legacy projects |

### Turborepo vs Rush
| Feature | Turborepo | Rush |
|---------|-----------|------|
| **Package manager** | Any | pnpm-focused |
| **Complexity** | Simple | Complex |
| **Configuration** | Minimal | Extensive |
| **Best for** | Most teams | Large enterprises |

**When to choose Turborepo**:
- Want simple, fast monorepo builds
- Need remote caching out of the box
- Using Vercel ecosystem
- Prefer minimal configuration
- Small to medium teams

**When to consider alternatives**:
- Need code generation (Nx)
- Want plugin ecosystem (Nx)
- Very large enterprise (Rush)
- Legacy Lerna project (stay with Lerna)

---

## Performance Optimization

### Cache Optimization
```json
{
  "pipeline": {
    "build": {
      "outputs": [
        "dist/**",
        ".next/**",
        "!**/*.map",           // Exclude source maps
        "!.next/cache/**"      // Exclude Next.js cache
      ]
    }
  }
}
```

### Parallel Execution
```bash
# Limit concurrency for memory-constrained environments
turbo run build --concurrency=2

# Use all cores
turbo run test --concurrency=100%

# Specific number
turbo run lint --concurrency=8
```

### Selective Execution
```bash
# Only changed packages
turbo run build --filter=[HEAD^1]

# Package and dependencies
turbo run build --filter=web...

# Exclude packages
turbo run test --filter=!admin
```

### Environment Variable Optimization
```json
{
  "globalEnv": ["NODE_ENV", "CI"],
  "pipeline": {
    "build": {
      "env": [
        "NEXT_PUBLIC_API_URL",
        "DATABASE_URL"
      ]
    }
  }
}
```

Only list env vars that affect output - unnecessary env vars invalidate cache.

### Dependency Optimization
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],    // Necessary
      "inputs": [
        "src/**/*.{ts,tsx}",      // Source only
        "!**/__tests__/**"        // Exclude tests
      ]
    }
  }
}
```

---

## Troubleshooting

### Cache Not Working

**Check cache hits**:
```bash
turbo run build --dry=json | jq '.tasks[] | {task: .taskId, cache: .cache}'
```

**Common causes**:
- Environment variables not declared in `env`
- Outputs not properly configured
- Global dependencies changing
- Non-deterministic builds (timestamps, random data)

**Debug caching**:
```bash
# Force execution
turbo run build --force

# Check what invalidated cache
turbo run build --output-logs=hash-only
```

### Build Failures

**Dependency issues**:
```bash
# Clear and reinstall
rm -rf node_modules .turbo
pnpm install --frozen-lockfile
```

**TypeScript errors**:
```bash
# Check project references
tsc --build --force

# Type check all packages
turbo run type-check
```

### Performance Issues

**Profile builds**:
```bash
turbo run build --profile
```

**Check task graph**:
```bash
turbo run build --graph
```

Generates `graph.png` showing task dependencies.

**Optimize concurrency**:
```bash
# Too many parallel tasks can exhaust memory
turbo run build --concurrency=4
```

### Remote Cache Not Working

**Check authentication**:
```bash
npx turbo login
npx turbo link
```

**Verify environment variables**:
```bash
echo $TURBO_TOKEN
echo $TURBO_TEAM
```

**Test connection**:
```bash
turbo run build --remote-only
```

---

## Best Practices

### Project Organization
- **apps/**: Application code (Next.js, Express, etc.)
- **packages/**: Shared libraries and utilities
- **config/**: Shared configurations (ESLint, TypeScript, Tailwind)
- Keep apps independent - avoid direct imports between apps
- Use workspace protocol: `"@myorg/ui": "workspace:*"`

### Pipeline Configuration
- Use `^build` for topological dependencies
- Configure `outputs` for all build artifacts
- List only necessary `env` variables
- Use `cache: false` for dev servers and watch modes
- Set `persistent: true` for long-running processes

### Caching Strategy
- Enable remote cache for teams
- Use `.turbo/` in `.gitignore`
- Don't cache non-deterministic outputs
- Explicitly list all build outputs
- Use `--force` to bypass cache when needed

### Workspace Dependencies
- Use workspace protocol: `workspace:*`
- Keep internal packages versioned at `0.0.0`
- Configure package exports properly
- Use TypeScript project references for type checking
- Transpile packages in consuming apps (Next.js)

### CI/CD
- Cache `.turbo/` directory
- Use `--filter=[origin/main]` for changed packages
- Set `TURBO_TOKEN` and `TURBO_TEAM` for remote cache
- Use `--frozen-lockfile` for reproducible builds
- Deploy only changed apps

### TypeScript
- Use project references for better type checking
- Share tsconfig via config package
- Enable `composite: true` for referenced projects
- Configure `paths` for clean imports
- Use `tsup` or `tsup` for library builds

### Testing
- Run tests in parallel: `turbo run test`
- Use `--filter` to test changed packages
- Configure test outputs for caching
- Share test utilities in packages
- Mock external dependencies

### Performance
- Profile with `--profile` flag
- Monitor cache hit rate
- Optimize `outputs` configuration
- Use concurrency limits on CI
- Enable remote caching

### Code Sharing
- Extract common utilities early
- Create focused, single-purpose packages
- Document package APIs
- Version internal packages together
- Use peer dependencies for React, etc.

---

## Advanced Patterns

### Conditional Outputs
```json
{
  "pipeline": {
    "build": {
      "outputs": [
        "dist/**",
        ".next/**",
        "{projectRoot}/build/**"    // Project-specific
      ]
    }
  }
}
```

### Task-Specific Environment
```json
{
  "pipeline": {
    "build:production": {
      "dependsOn": ["^build"],
      "env": ["NODE_ENV", "API_URL"],
      "outputs": ["dist/**"]
    },
    "build:staging": {
      "dependsOn": ["^build"],
      "env": ["NODE_ENV", "STAGING_API_URL"],
      "outputs": ["dist/**"]
    }
  }
}
```

### Workspace Filtering Examples
```bash
# Build web and its dependencies
turbo run build --filter=web...

# Build everything that depends on ui
turbo run build --filter=...ui

# Build changed packages and dependents
turbo run build --filter=[main]...

# Build specific scope
turbo run build --filter=@myorg/*

# Exclude packages
turbo run test --filter=!admin --filter=!legacy
```

### Multiple Entry Points
```json
{
  "name": "@myorg/ui",
  "exports": {
    ".": "./src/index.ts",
    "./button": "./src/button.tsx",
    "./input": "./src/input.tsx",
    "./hooks": "./src/hooks/index.ts"
  }
}
```

```typescript
import { Button } from '@myorg/ui/button';
import { useDebounce } from '@myorg/ui/hooks';
```

### Shared Build Scripts
```
packages/scripts/
├── build.js
├── test.js
└── package.json
```

**build.js**:
```javascript
#!/usr/bin/env node
const { build } = require('tsup');

build({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  sourcemap: true,
  clean: true,
}).catch((error) => {
  console.error(error);
  process.exit(1);
});
```

**Using in packages**:
```json
{
  "scripts": {
    "build": "node ../../packages/scripts/build.js"
  }
}
```

---

## Resources

### Official Documentation
- [Turborepo Docs](https://turbo.build/repo/docs)
- [Quick Start Guide](https://turbo.build/repo/docs/getting-started)
- [API Reference](https://turbo.build/repo/docs/reference/configuration)
- [Examples](https://github.com/vercel/turbo/tree/main/examples)

### Community
- [GitHub Discussions](https://github.com/vercel/turbo/discussions)
- [Discord](https://turbo.build/discord)
- [Twitter](https://twitter.com/turborepo)

### Related Tools
- [pnpm](https://pnpm.io/) - Fast package manager
- [tsup](https://tsup.egoist.dev/) - TypeScript bundler
- [changesets](https://github.com/changesets/changesets) - Version management
- [Vercel](https://vercel.com/) - Deployment platform

---

*This skill provides comprehensive Turborepo knowledge for building high-performance monorepos with intelligent caching and task orchestration.*
