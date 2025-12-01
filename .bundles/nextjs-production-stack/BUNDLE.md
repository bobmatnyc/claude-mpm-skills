# Next.js Production Stack

**Version:** 1.0.0
**Category:** JavaScript/TypeScript
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Production-ready Next.js application stack with App Router, Server Components, TypeScript patterns, and React fundamentals. Optimized for modern Next.js 14/15 applications with server-side rendering and edge deployment.

## Included Skills

- **nextjs-core** (toolchains/nextjs/core) - App Router, Server Components, Server Actions
- **nextjs-v16** (toolchains/nextjs/v16) - Next.js 16 features (Turbopack, cache components)
- **react** (toolchains/typescript/frameworks/react) - React fundamentals and hooks
- **typescript-core** (toolchains/typescript/core) - TypeScript patterns and best practices
- **vercel** (toolchains/platforms/deployment/vercel) - Deployment and Edge Functions
- **tailwind** (toolchains/ui/styling/tailwind) - Utility-first CSS

## Use Cases

**When to Deploy This Bundle:**
- Building Next.js applications from scratch
- Migrating to App Router from Pages Router
- Projects deploying to Vercel Edge Network
- Full-stack TypeScript applications
- Applications requiring SSR/SSG/ISR

**What You Get:**
- App Router architecture patterns
- Server Component vs Client Component guidelines
- Server Actions for mutations
- TypeScript configuration for Next.js
- Vercel deployment optimizations
- Tailwind integration patterns

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| nextjs-core | ✅ Yes | 🚀 Enhanced | React (required) |
| nextjs-v16 | ✅ Yes | 🚀 Enhanced | nextjs-core (recommended) |
| react | ✅ Yes | 🚀 Enhanced | None |
| typescript-core | ✅ Yes | 🚀 Enhanced | None |
| vercel | ✅ Yes | 🚀 Enhanced | Next.js (recommended) |
| tailwind | ✅ Yes | 🚀 Enhanced | None |

**Bundle Synergies:**
- Next.js + React: Server and Client Components
- Next.js + TypeScript: Full type safety across frontend/backend
- Next.js + Vercel: Zero-config deployment with edge optimization
- Next.js + Tailwind: Rapid UI development with utility classes

## Integration Example

```typescript
// app/page.tsx - Server Component (default)
import { Suspense } from 'react';

async function Users() {
  const users = await fetchUsers(); // Direct DB access
  return <UserList users={users} />;
}

export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <Users />
    </Suspense>
  );
}

// app/actions.ts - Server Action
'use server'

export async function createUser(formData: FormData) {
  const email = formData.get('email');
  await db.users.insert({ email });
  revalidatePath('/users');
}

// app/components/UserForm.tsx - Client Component
'use client'

import { createUser } from '@/app/actions';

export function UserForm() {
  return (
    <form action={createUser}>
      <input name="email" type="email" />
      <button>Create</button>
    </form>
  );
}
```

## Version History

- **1.0.0** (2025-11-30): Initial release with 6 Next.js stack skills
