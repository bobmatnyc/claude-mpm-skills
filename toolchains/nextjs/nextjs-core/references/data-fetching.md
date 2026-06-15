# Data Fetching Patterns

Advanced caching, parallel fetching, streaming, and database integration patterns.

## Fetch Patterns

### Parallel vs Sequential

```typescript
// ❌ Sequential - slow
async function Page() {
  const user = await getUser();      // Wait
  const posts = await getPosts();    // Then wait
  const comments = await getComments(); // Then wait
  return <Dashboard user={user} posts={posts} comments={comments} />;
}

// ✅ Parallel - fast
async function Page() {
  const [user, posts, comments] = await Promise.all([
    getUser(),
    getPosts(),
    getComments(),
  ]);
  return <Dashboard user={user} posts={posts} comments={comments} />;
}
```

### Dependent Fetches

```typescript
// When data depends on previous fetch
async function Page({ params }: { params: Promise<{ userId: string }> }) {
  const { userId } = await params;
  
  // Must be sequential - posts depend on user
  const user = await getUser(userId);
  const posts = await getPostsByAuthor(user.id);
  
  // But these can be parallel
  const [comments, likes] = await Promise.all([
    getCommentsForPosts(posts.map(p => p.id)),
    getLikesForPosts(posts.map(p => p.id)),
  ]);
  
  return <UserProfile user={user} posts={posts} comments={comments} likes={likes} />;
}
```

## Streaming with Suspense

### Basic Streaming

```typescript
import { Suspense } from 'react';

export default async function Page() {
  // Fast data loads immediately
  const user = await getUser();
  
  return (
    <div>
      <Header user={user} />
      
      {/* Slow components stream in */}
      <Suspense fallback={<PostsSkeleton />}>
        <SlowPostsList />
      </Suspense>
      
      <Suspense fallback={<RecommendationsSkeleton />}>
        <SlowRecommendations />
      </Suspense>
    </div>
  );
}

async function SlowPostsList() {
  const posts = await getPostsSlowly(); // 3+ seconds
  return <PostList posts={posts} />;
}
```

### Nested Suspense

```typescript
export default function Page() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <MainContent />
    </Suspense>
  );
}

async function MainContent() {
  const data = await getMainData();
  
  return (
    <div>
      <PrimaryContent data={data} />
      
      {/* Secondary content streams independently */}
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>
    </div>
  );
}
```

### Loading UI

```typescript
// app/posts/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="space-y-3">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-24 bg-gray-200 rounded" />
        ))}
      </div>
    </div>
  );
}
```

## Caching Strategies

### Request Memoization

```typescript
// Automatically deduplicated within single render pass
async function getUser(id: string) {
  console.log('Fetching user:', id); // Only logs once
  return db.users.findUnique({ where: { id } });
}

// Multiple components can call same function
async function UserHeader({ userId }: { userId: string }) {
  const user = await getUser(userId);
  return <header>{user.name}</header>;
}

async function UserSidebar({ userId }: { userId: string }) {
  const user = await getUser(userId); // Same call, deduplicated
  return <aside>{user.bio}</aside>;
}
```

### React Cache

```typescript
import { cache } from 'react';

// Explicit memoization across components
export const getUser = cache(async (id: string) => {
  return db.users.findUnique({ where: { id } });
});

// Preload pattern
export const preloadUser = (id: string) => {
  void getUser(id); // Fire request early
};

// Usage in layout
export default async function Layout({ children, params }) {
  const { userId } = await params;
  preloadUser(userId); // Start fetch before child renders
  return <div>{children}</div>;
}
```

### Data Cache with Tags

```typescript
// Fetch with cache tags
async function getPosts(categoryId: string) {
  const posts = await fetch(`/api/posts?category=${categoryId}`, {
    next: { 
      tags: ['posts', `category-${categoryId}`],
      revalidate: 3600, // 1 hour
    },
  }).then(r => r.json());
  
  return posts;
}

// Invalidate by tag
import { revalidateTag } from 'next/cache';

export async function createPost(data: PostData) {
  await db.posts.create({ data });
  revalidateTag('posts');
  revalidateTag(`category-${data.categoryId}`);
}
```

### Time-Based Revalidation

```typescript
// Page-level revalidation
export const revalidate = 3600; // Revalidate every hour

export default async function Page() {
  const data = await getData();
  return <Content data={data} />;
}

// Segment-level in layout
// app/blog/layout.tsx
export const revalidate = 60; // All /blog/* pages revalidate every minute
```

### On-Demand Revalidation

```typescript
// API route for webhook
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  const { secret, path, tag } = await request.json();
  
  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ error: 'Invalid secret' }, { status: 401 });
  }
  
  if (path) {
    revalidatePath(path);
  }
  if (tag) {
    revalidateTag(tag);
  }
  
  return Response.json({ revalidated: true });
}
```

## Database Integration

### Prisma Patterns

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query'] : [],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = db;
}
```

### Drizzle Patterns

```typescript
// lib/db.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client, { schema });

// Usage with relations
const postsWithAuthor = await db.query.posts.findMany({
  with: {
    author: true,
    comments: {
      with: { author: true },
      limit: 5,
    },
  },
});
```

### Connection Pooling

```typescript
// For serverless (Vercel, AWS Lambda)
import { Pool } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-serverless';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool);

// Or with Prisma Accelerate
// In schema.prisma:
// datasource db {
//   provider = "postgresql"
//   url      = env("DATABASE_URL")
//   directUrl = env("DIRECT_URL")
// }
```

## Pagination Patterns

### Offset Pagination

```typescript
async function getPosts(page: number, pageSize: number = 10) {
  const [posts, total] = await Promise.all([
    db.posts.findMany({
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { createdAt: 'desc' },
    }),
    db.posts.count(),
  ]);
  
  return {
    posts,
    pagination: {
      page,
      pageSize,
      total,
      totalPages: Math.ceil(total / pageSize),
    },
  };
}
```

### Cursor Pagination

```typescript
async function getPosts(cursor?: string, limit: number = 10) {
  const posts = await db.posts.findMany({
    take: limit + 1, // Fetch one extra to check if more exist
    cursor: cursor ? { id: cursor } : undefined,
    orderBy: { createdAt: 'desc' },
  });
  
  const hasMore = posts.length > limit;
  const items = hasMore ? posts.slice(0, -1) : posts;
  
  return {
    items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
  };
}
```

### Infinite Scroll Component

```typescript
'use client';

import { useInfiniteQuery } from '@tanstack/react-query';
import { useInView } from 'react-intersection-observer';
import { useEffect } from 'react';

export function InfinitePostList() {
  const { ref, inView } = useInView();
  
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = 
    useInfiniteQuery({
      queryKey: ['posts'],
      queryFn: ({ pageParam }) => fetchPosts(pageParam),
      getNextPageParam: (lastPage) => lastPage.nextCursor,
    });
  
  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, fetchNextPage]);
  
  return (
    <div>
      {data?.pages.map((page) =>
        page.items.map((post) => <PostCard key={post.id} post={post} />)
      )}
      
      <div ref={ref}>
        {isFetchingNextPage && <Spinner />}
      </div>
    </div>
  );
}
```

## Error Handling

### Error Boundaries

```typescript
// app/posts/error.tsx
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error reporting service
    console.error(error);
  }, [error]);
  
  return (
    <div className="error-container">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Not Found

```typescript
// app/posts/[id]/page.tsx
import { notFound } from 'next/navigation';

export default async function PostPage({ params }) {
  const { id } = await params;
  const post = await getPost(id);
  
  if (!post) {
    notFound(); // Renders not-found.tsx
  }
  
  return <Post post={post} />;
}

// app/posts/[id]/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Post Not Found</h2>
      <p>Could not find the requested post.</p>
    </div>
  );
}
```

## Best Practices

1. **Fetch in Server Components** - Avoid useEffect for initial data
2. **Parallelize independent fetches** - Use Promise.all
3. **Stream slow content** - Wrap with Suspense
4. **Use appropriate caching** - Match strategy to data volatility
5. **Preload data** - Use React cache() for waterfall prevention
6. **Handle errors gracefully** - Use error.tsx boundaries
7. **Paginate large datasets** - Cursor pagination for infinite scroll
8. **Pool connections** - Essential for serverless
