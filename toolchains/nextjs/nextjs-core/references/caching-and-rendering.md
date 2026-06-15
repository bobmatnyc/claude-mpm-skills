# Caching and Rendering Strategy (App Router)

Use caching intentionally. Incorrect cache boundaries create stale UI, data leaks (user A sees user B), or unnecessary load.

## Mental Model

- **Request memoization**: identical calls can be deduped within a single render pass.
- **Data cache**: `fetch` can cache across requests when configured.
- **Revalidation**: invalidate by path (`revalidatePath`) or tag (`revalidateTag`) after mutations.

If using Next.js 16 Cache Components (`"use cache"`), see `nextjs-v16` for the new opt-in model.

## Static vs Dynamic Rendering

Prefer static for shared, cache-safe content; prefer dynamic for per-user or rapidly changing content.

Common triggers for dynamic rendering:
- per-user data (sessions, cookies)
- request headers/cookies access
- real-time requirements

## Tag-Based Revalidation (Preferred)

Tags scale better than path-based invalidation when many routes depend on the same data.

```ts
// Read with tags
async function getPosts() {
  return fetch("https://example.com/api/posts", {
    next: { tags: ["posts"], revalidate: 3600 },
  }).then((r) => r.json());
}

// After a mutation
import { revalidateTag } from "next/cache";

export async function createPost(data: unknown) {
  await db.posts.create({ data });
  revalidateTag("posts");
}
```

## Path-Based Revalidation

Use when only a small number of routes depend on the data, or when tags are not available.

```ts
import { revalidatePath } from "next/cache";

export async function updatePost(id: string, data: unknown) {
  await db.posts.update({ where: { id }, data });
  revalidatePath(`/posts/${id}`);
}
```

## Personalized Data: Avoid Shared Caches

Cache boundaries must not mix users.

✅ Correct patterns:
```ts
// ✅ Keep per-user reads dynamic (no shared cache)
import { auth } from "@/auth";

export async function getMe() {
  const session = await auth();
  if (!session) return null;
  return db.users.findUnique({ where: { id: session.user.id } });
}

// ✅ Cache shared data and combine with dynamic per-user overlays
export async function getCatalog() {
  return fetch("https://example.com/api/catalog", {
    next: { tags: ["catalog"], revalidate: 3600 },
  }).then((r) => r.json());
}
```

❌ Anti-pattern: caching a per-user response
```ts
// ❌ Do not cache personalized data under a shared key/tag
fetch("/api/me", { next: { tags: ["me"] } });
```

## Decision Checklist

- Does the response include user-specific data? → keep it dynamic.
- Is it safe for another user to see this? → if not, do not share-cache it.
- Do many pages depend on the same data? → prefer tag revalidation.
- Do only one or two routes depend on it? → path revalidation is fine.

## Common Pitfalls

- ❌ `revalidatePath("/")` everywhere → ✅ revalidate the smallest affected tag/path.
- ❌ caching auth/session-derived data → ✅ keep auth-derived reads dynamic.
- ❌ mixing static and dynamic in a way that disables caching unintentionally → ✅ isolate dynamic reads.
