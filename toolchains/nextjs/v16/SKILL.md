---
name: nextjs-v16
description: Next.js 16 specific features, breaking changes, and migration guide. Use when upgrading from Next.js 15, implementing Cache Components with "use cache", working with Turbopack, or handling the new async request APIs. Released October 2025 with fundamental caching model changes.
---

# Next.js 16 Migration & Features

Next.js 16 fundamentally changes caching (opt-in via `"use cache"`), makes Turbopack the default bundler, and requires async request APIs. This skill covers breaking changes and new patterns.

## Breaking Changes Summary

| Requirement | Next.js 15 | Next.js 16 |
|-------------|------------|------------|
| **Node.js** | 18.18.0+ | **20.9.0+** |
| **TypeScript** | 4.7+ | **5.1.0+** |
| **Browsers** | Chrome 64+ | **Chrome 111+** |

## Critical Migration: Async Request APIs

**All request APIs are now async.** Builds fail without migration.

```typescript
// ❌ BREAKS in Next.js 16
export default function Page({ params, searchParams }) {
  const cookieStore = cookies();
  return <div>{params.slug}</div>;
}

// ✅ Required async pattern
export default async function Page({ 
  params, 
  searchParams 
}: { 
  params: Promise<{ slug: string }>;
  searchParams: Promise<Record<string, string>>;
}) {
  const { slug } = await params;
  const query = await searchParams;
  const cookieStore = await cookies();
  const headersList = await headers();
  return <div>{slug}</div>;
}
```

## Cache Components (`"use cache"`)

The new caching model is **opt-in**. Dynamic code runs at request time by default.

### Enable in Config

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
};
export default nextConfig;
```

### Basic Usage

```typescript
// Cached component
"use cache"
export default async function ProductList() {
  const products = await getProducts();
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}

// Cached function
"use cache"
async function getExpensiveData() {
  return await heavyComputation();
}
```

### New Caching APIs

```typescript
import { revalidateTag, updateTag, refresh } from 'next/cache';

// revalidateTag now requires cacheLife profile
revalidateTag('blog-posts', 'max');     // Built-in: 'max', 'hours', 'days'
revalidateTag('products', { expire: 3600 }); // Custom

// Read-your-writes semantics in Server Actions
'use server';
export async function updateProfile(data: Profile) {
  await db.users.update(data);
  updateTag(`user-${data.id}`); // Immediately reflects in reads
}

// Force uncached refresh
refresh();
```

## Middleware → proxy.ts

Middleware is renamed to `proxy.ts` and runs on Node.js runtime only:

```typescript
// proxy.ts (was middleware.ts)
import { NextRequest, NextResponse } from 'next/server';

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  if (pathname.startsWith('/admin')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*'],
};
```

## Turbopack (Default)

Turbopack is now the default bundler with 2-5x faster production builds.

### Configuration Changes

```typescript
// next.config.ts - options moved from experimental
const nextConfig = {
  turbopack: {
    resolveAlias: { fs: { browser: './empty.ts' } },
  },
  experimental: {
    turbopackFileSystemCacheForDev: true, // Beta: persist artifacts
  },
};
```

### Opt-out for Webpack

```bash
# If custom webpack config required
next build --webpack
```

## Removed Features

- **AMP support**: All AMP APIs removed
- **`next lint`**: Use ESLint/Biome directly
- **Runtime configs**: `serverRuntimeConfig`, `publicRuntimeConfig` (use env vars)
- **Parallel routes**: Now require explicit `default.js` files

## Image Optimization Changes

| Setting | Old Default | New Default |
|---------|-------------|-------------|
| `minimumCacheTTL` | 60s | **14400s (4 hours)** |
| `imageSizes` | Included 16px | **16px removed** |
| `qualities` | [1..100] | **[75] only** |

## Migration Workflow

### 1. Run Automated Codemod

```bash
npx @next/codemod@canary upgrade latest
```

### 2. Address Specific Transformations

```bash
# Async APIs (params, cookies, headers)
npx @next/codemod migrate-to-async-dynamic-apis .

# Middleware to proxy
npx @next/codemod@latest middleware-to-proxy

# Generate TypeScript types
npx next typegen
```

### 3. Manual Review

The codemod leaves `@next-codemod-error` comments where manual review needed:
- Complex params destructuring passed through helpers
- Conditional request API access
- Dynamic route patterns

### 4. Test Custom Webpack Configs

If using custom webpack configuration, test against Turbopack or opt out:

```bash
# Test build
next build

# If failures, temporarily opt out
next build --webpack
```

## Navigation

### Detailed References

- **[🔄 Migration Checklist](./references/migration-checklist.md)** - Step-by-step migration process, common issues, testing strategy. Load when upgrading existing projects.

- **[💾 Cache Components](./references/cache-components.md)** - Deep dive into `"use cache"`, cacheLife profiles, invalidation patterns. Load when implementing caching strategies.

- **[⚡ Turbopack](./references/turbopack.md)** - Configuration, loader migration, performance optimization. Load when troubleshooting builds or migrating webpack configs.

## Red Flags

**Stop and reconsider if:**
- Synchronous `cookies()`, `headers()`, or `params` access
- `middleware.ts` file still exists (rename to `proxy.ts`)
- Using `revalidateTag` with single argument
- Custom webpack config without Turbopack testing
- AMP pages in codebase
- Relying on `next lint` in CI

## Migration Time Estimates

- **Simple sites**: 2-4 hours
- **Medium complexity**: 4-8 hours
- **Complex apps**: 1-2 days (custom webpack, extensive middleware)

## Integration

- **nextjs-core**: Framework patterns that apply across versions
- **typescript-core**: Type-safe async patterns, validation
