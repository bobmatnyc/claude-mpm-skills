# Cache Components in Next.js 16

Deep dive into the new `"use cache"` directive, cacheLife profiles, and invalidation patterns.

## Architectural Shift

Next.js 16 moves from **implicit caching** to **explicit opt-in caching**:

| Next.js 15 | Next.js 16 |
|------------|------------|
| fetch() cached by default | fetch() dynamic by default |
| Opt-out with `no-store` | Opt-in with `"use cache"` |
| Implicit data cache | Explicit Cache Components |

## Enabling Cache Components

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true, // Replaces experimental.ppr and dynamicIO
};

export default nextConfig;
```

## Basic Usage

### Cached Component

```typescript
"use cache"

export default async function ProductList() {
  // This entire component is cached
  const products = await db.products.findMany();
  
  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          <ProductCard product={product} />
        </li>
      ))}
    </ul>
  );
}
```

### Cached Function

```typescript
"use cache"

async function getExpensiveData(category: string) {
  // Function result is cached based on arguments
  const data = await heavyComputation(category);
  return data;
}

// Different arguments = different cache entries
await getExpensiveData('electronics'); // Cache miss, computed
await getExpensiveData('electronics'); // Cache hit
await getExpensiveData('clothing');    // Cache miss, computed
```

### Partial Caching

```typescript
import { Suspense } from 'react';

// Uncached wrapper
export default async function Page() {
  const user = await getCurrentUser(); // Dynamic, not cached
  
  return (
    <div>
      <Header user={user} />
      <Suspense fallback={<Loading />}>
        {/* Cached component */}
        <CachedProductList />
      </Suspense>
    </div>
  );
}

"use cache"
async function CachedProductList() {
  const products = await getProducts();
  return <ProductGrid products={products} />;
}
```

## cacheLife Profiles

### Built-in Profiles

| Profile | Duration | Use Case |
|---------|----------|----------|
| `'max'` | Long-term | Static content, rarely changes |
| `'days'` | 1-7 days | Semi-static content |
| `'hours'` | 1-24 hours | Frequently updated content |

```typescript
"use cache"
cacheLife('max');

export default async function StaticContent() {
  const content = await getStaticContent();
  return <div>{content}</div>;
}
```

### Custom Profiles

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
  experimental: {
    cacheLife: {
      // Custom profile definitions
      'short': { expire: 300 },        // 5 minutes
      'medium': { expire: 3600 },      // 1 hour
      'long': { expire: 86400 },       // 1 day
      'session': { expire: 1800 },     // 30 minutes
    },
  },
};
```

Usage:
```typescript
"use cache"
cacheLife('short');

async function FrequentlyUpdated() {
  return await getLatestData();
}
```

## Cache Invalidation

### revalidateTag (Updated API)

```typescript
import { revalidateTag } from 'next/cache';

// Now requires cacheLife profile as second argument
revalidateTag('products', 'max');
revalidateTag('blog-posts', 'hours');
revalidateTag('user-data', { expire: 3600 });
```

### updateTag (New: Read-Your-Writes)

Immediate cache update within the same request:

```typescript
'use server';

import { updateTag } from 'next/cache';

export async function updateUserProfile(userId: string, data: ProfileData) {
  // Update database
  await db.users.update({
    where: { id: userId },
    data,
  });
  
  // Immediately update cache - subsequent reads see new data
  updateTag(`user-${userId}`);
  
  // Any component reading this tag in the same request
  // will see the updated data
  return { success: true };
}
```

### refresh (New: Force Uncached)

Force a fresh, uncached data fetch:

```typescript
import { refresh } from 'next/cache';

export async function forceRefresh() {
  refresh(); // Clear all cached data for this request
}
```

## Tagging Strategies

### Component-Level Tags

```typescript
"use cache"
cacheTag('products', 'homepage');

export default async function FeaturedProducts() {
  const products = await getFeaturedProducts();
  return <ProductGrid products={products} />;
}

// Invalidate both tags
revalidateTag('products', 'max');    // All product caches
revalidateTag('homepage', 'max');    // All homepage caches
```

### Entity-Based Tags

```typescript
"use cache"
cacheTag(`product-${productId}`);

export default async function ProductDetail({ productId }: Props) {
  const product = await getProduct(productId);
  return <ProductView product={product} />;
}

// Invalidate specific product
export async function updateProduct(productId: string, data: ProductData) {
  await db.products.update({ where: { id: productId }, data });
  revalidateTag(`product-${productId}`, 'max');
}
```

### Hierarchical Tags

```typescript
"use cache"
cacheTag('catalog', `category-${categoryId}`, `product-${productId}`);

// Invalidation hierarchy:
revalidateTag('catalog', 'max');           // All catalog data
revalidateTag(`category-${categoryId}`, 'max');  // Category and its products
revalidateTag(`product-${productId}`, 'max');    // Single product
```

## Patterns

### Cached API Layer

```typescript
// lib/cache.ts
"use cache"
cacheTag('api');

export async function cachedFetch<T>(
  url: string, 
  tags: string[]
): Promise<T> {
  tags.forEach(tag => cacheTag(tag));
  
  const response = await fetch(url);
  return response.json();
}

// Usage
"use cache"
export async function getProducts() {
  return cachedFetch<Product[]>('/api/products', ['products']);
}
```

### Time-Based Segments

```typescript
// Short-lived data (news, prices)
"use cache"
cacheLife('hours');
cacheTag('prices');

export async function LivePrices() {
  return await getPrices();
}

// Long-lived data (product catalog)
"use cache"
cacheLife('days');
cacheTag('catalog');

export async function ProductCatalog() {
  return await getCatalog();
}
```

### User-Specific Caching

```typescript
// Cache per user, but still cached
"use cache"

export async function UserDashboard({ userId }: { userId: string }) {
  cacheTag(`user-${userId}`, 'dashboard');
  cacheLife('hours');
  
  const data = await getUserDashboardData(userId);
  return <Dashboard data={data} />;
}
```

## Debugging

### Cache Headers

Check response headers for cache status:
- `x-nextjs-cache: HIT` - Served from cache
- `x-nextjs-cache: MISS` - Cache miss, computed
- `x-nextjs-cache: STALE` - Stale cache, revalidating

### Development Mode

In development, caching is disabled by default. Enable for testing:

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
  experimental: {
    // Enable cache in dev for testing
    cacheHandlerPath: './cache-handler.js',
  },
};
```

## Migration from fetch() cache

### Before (Next.js 15)

```typescript
// Implicit caching
const data = await fetch(url); // Cached

// Opt-out
const fresh = await fetch(url, { cache: 'no-store' });

// Time-based
const timed = await fetch(url, { next: { revalidate: 3600 } });
```

### After (Next.js 16)

```typescript
// Default: no cache
const data = await fetch(url); // Not cached

// Explicit cache with "use cache"
"use cache"
async function getCachedData() {
  cacheLife('hours');
  return await fetch(url).then(r => r.json());
}
```

## Best Practices

1. **Cache at boundaries** - Cache at component level, not individual fetches
2. **Use meaningful tags** - Entity-based tags enable surgical invalidation
3. **Profile appropriately** - Match cacheLife to data volatility
4. **Combine with Suspense** - Stream uncached shells with cached content
5. **Invalidate precisely** - Avoid broad invalidation when specific tags work
6. **Monitor hit rates** - Track cache effectiveness in production
