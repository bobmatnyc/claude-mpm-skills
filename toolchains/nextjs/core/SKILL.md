---
name: nextjs-core
description: Core Next.js patterns for App Router development including Server Components, Server Actions, route handlers, data fetching, and caching strategies. Use when building Next.js applications with the App Router, implementing server-side logic, or optimizing data flows. Version-agnostic patterns that apply to Next.js 14+.
---

# Next.js Core Patterns

Framework-level patterns for Next.js App Router. For version-specific features, see nextjs-v16.

## Server Components (Default)

All components are Server Components by default:

```typescript
// app/users/page.tsx - Server Component
async function UsersPage() {
  const users = await db.users.findMany(); // Direct database access
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

Add `'use client'` only when required:
- React hooks (useState, useEffect)
- Browser APIs (window, localStorage)
- Event handlers (onClick, onChange)

## Server Actions

```typescript
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const Schema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  const result = Schema.safeParse(Object.fromEntries(formData));
  if (!result.success) return { error: result.error.flatten() };
  
  await db.users.create({ data: result.data });
  revalidatePath('/users');
  return { success: true };
}
```

### Form Integration

```typescript
// Server Component form
export default function Page() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### Client Component with useActionState

```typescript
'use client';
import { useActionState } from 'react';

export function UserForm() {
  const [state, action, pending] = useActionState(createUser, null);
  return (
    <form action={action}>
      <input name="name" disabled={pending} />
      <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
}
```

## Route Handlers

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

type Context = { params: Promise<{ id: string }> };

export async function GET(req: NextRequest, ctx: Context) {
  const { id } = await ctx.params;
  const user = await db.users.findUnique({ where: { id } });
  if (!user) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(user);
}
```

## Data Fetching

### Parallel Fetching

```typescript
async function Dashboard() {
  const [users, posts] = await Promise.all([getUsers(), getPosts()]);
  return <><UserList users={users} /><PostList posts={posts} /></>;
}
```

### Streaming with Suspense

```typescript
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <SlowComponent />
    </Suspense>
  );
}
```

### Loading and Error States

```typescript
// app/dashboard/loading.tsx
export default function Loading() { return <Skeleton />; }

// app/dashboard/error.tsx
'use client';
export default function Error({ reset }: { reset: () => void }) {
  return <button onClick={reset}>Retry</button>;
}
```

## Caching & Revalidation

```typescript
import { revalidatePath, revalidateTag } from 'next/cache';

export async function updatePost(id: string, data: PostData) {
  await db.posts.update({ where: { id }, data });
  revalidatePath(`/posts/${id}`);  // Path-based
  revalidateTag(`post-${id}`);     // Tag-based
}
```

## Metadata

```typescript
// Static
export const metadata = { title: 'About', description: '...' };

// Dynamic
export async function generateMetadata({ params }) {
  const { slug } = await params;
  const post = await getPost(slug);
  return { title: post.title };
}
```

## Navigation

### Detailed References

- **[🔐 Server Actions](./references/server-actions.md)** - Type-safe actions with next-safe-action, validation patterns, optimistic updates. Load when implementing complex form handling.

- **[📊 Data Fetching](./references/data-fetching.md)** - Caching strategies, ISR, parallel fetching, database patterns. Load when optimizing performance.

- **[🛣️ Routing](./references/routing.md)** - Dynamic routes, parallel routes, intercepting routes, middleware. Load when setting up complex navigation.

- **[🔒 Authentication](./references/authentication.md)** - Auth.js integration, protected routes, session handling. Load when implementing user auth.

## Red Flags

**Stop and reconsider if:**
- Adding `'use client'` to fetch data
- Using `useEffect` for initial data load
- Sequential awaits that could be parallel
- Missing loading/error states
- Passing functions as props to Client Components

## Integration

- **typescript-core**: Type-safe patterns, Zod validation
- **nextjs-v16**: Breaking changes, Cache Components, Turbopack
