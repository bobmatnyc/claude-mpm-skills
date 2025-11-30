# Next.js 16 Migration Checklist

Step-by-step migration process from Next.js 15 to 16.

## Pre-Migration Checklist

### Environment Requirements

- [ ] Node.js 20.9.0+ installed
- [ ] TypeScript 5.1.0+ in dependencies
- [ ] Target browsers support Chrome 111+, Safari 16.4+
- [ ] CI/CD environments updated to Node.js 20+

### Dependency Audit

```bash
# Check current versions
npm ls next react react-dom typescript

# Update to Next.js 16
npm install next@16 react@latest react-dom@latest
```

### Backup

```bash
# Create migration branch
git checkout -b nextjs-16-migration

# Commit current state
git add -A && git commit -m "Pre-migration snapshot"
```

## Migration Steps

### Step 1: Run Automated Codemod

```bash
npx @next/codemod@canary upgrade latest
```

This handles:
- Async params/searchParams conversion
- cookies()/headers() async calls
- Import updates
- Basic middleware rename

### Step 2: Async Request APIs

The codemod converts most cases, but manually verify:

```typescript
// Before (Next.js 15)
export default function Page({ params }: { params: { id: string } }) {
  const { id } = params;
  return <div>{id}</div>;
}

// After (Next.js 16)
export default async function Page({ 
  params 
}: { 
  params: Promise<{ id: string }> 
}) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

**Manual review needed for:**

```typescript
// Helper functions receiving params
function processParams(params: { id: string }) { /* ... */ }

// Must be updated to:
async function processParams(params: Promise<{ id: string }>) {
  const { id } = await params;
  // ...
}

// Conditional access
if (someCondition) {
  const cookie = await cookies(); // Each access must be awaited
}
```

### Step 3: Middleware to Proxy

```bash
npx @next/codemod@latest middleware-to-proxy
```

Rename manually if codemod misses:
```bash
mv middleware.ts proxy.ts
```

Update the export:
```typescript
// Before
export function middleware(request: NextRequest) { }

// After
export function proxy(request: NextRequest) { }
```

### Step 4: Update Caching Calls

Search for `revalidateTag` and update:

```typescript
// Before
revalidateTag('posts');

// After - requires cacheLife profile
revalidateTag('posts', 'max');
// Or with custom duration
revalidateTag('posts', { expire: 3600 });
```

### Step 5: Remove Deprecated Features

Search and remove:

```bash
# Find AMP usage
grep -r "useAmp\|amp: true" --include="*.tsx" --include="*.ts"

# Find runtime configs
grep -r "serverRuntimeConfig\|publicRuntimeConfig" --include="*.ts"

# Find next lint usage
grep -r "next lint" package.json .github/
```

Replace:
- AMP → Remove or use external AMP generator
- Runtime configs → Environment variables
- `next lint` → Direct ESLint/Biome commands

### Step 6: Parallel Routes Default Files

Add `default.js` to all parallel routes:

```typescript
// app/@modal/default.tsx
export default function Default() {
  return null;
}
```

### Step 7: Image Configuration

If relying on old defaults, explicitly set:

```typescript
// next.config.ts
const nextConfig = {
  images: {
    minimumCacheTTL: 60, // Restore old default if needed
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    qualities: [75], // Or restore range if needed
  },
};
```

### Step 8: Test Build

```bash
# Standard build (uses Turbopack)
npm run build

# If build fails with custom webpack, try:
next build --webpack
```

### Step 9: Run Type Generation

```bash
npx next typegen
```

### Step 10: Test Application

```bash
npm run dev
npm run build
npm start

# Run test suite
npm test
```

## Common Issues

### Issue: "params is not a Promise"

**Cause:** Component not converted to async

**Fix:**
```typescript
// Add async and await
export default async function Page({ params }) {
  const { id } = await params;
}
```

### Issue: "cookies() is not a function"

**Cause:** Missing await on cookies()

**Fix:**
```typescript
const cookieStore = await cookies();
```

### Issue: Turbopack build failures

**Cause:** Incompatible webpack loaders

**Fix:**
```bash
# Temporary: use webpack
next build --webpack

# Permanent: migrate loaders
# @svgr/webpack → @svgr/rollup or inline SVGs
# custom loaders → Turbopack equivalents
```

### Issue: "middleware" export not found

**Cause:** File not renamed

**Fix:**
```bash
mv middleware.ts proxy.ts
# Update export name to "proxy"
```

### Issue: revalidateTag type error

**Cause:** Missing second argument

**Fix:**
```typescript
revalidateTag('tag', 'max');
```

## Post-Migration Verification

- [ ] All pages render correctly
- [ ] Server Actions work
- [ ] Authentication flows complete
- [ ] API routes respond correctly
- [ ] Images load and optimize
- [ ] Build completes without errors
- [ ] Tests pass
- [ ] No console errors in browser
- [ ] Performance metrics acceptable

## Rollback Plan

If critical issues found:

```bash
# Revert to pre-migration
git checkout main
npm install

# Or pin to Next.js 15
npm install next@15
```

## CI/CD Updates

Update workflows:

```yaml
# .github/workflows/ci.yml
- uses: actions/setup-node@v4
  with:
    node-version: '20'  # Was '18'

- run: npm ci
- run: npm run build
- run: npm test

# Remove next lint if used
# - run: npm run lint
# Replace with:
- run: npx eslint .
```
