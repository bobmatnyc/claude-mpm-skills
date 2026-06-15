# RSC / `'use client'` Boundary (Conceptual)

> Source of truth: [Server Components](https://react.dev/reference/rsc/server-components), [`'use client'`](https://react.dev/reference/rsc/use-client), and [`'use server'`](https://react.dev/reference/rsc/use-server). This reference covers the React-level model; framework wiring defers to the Next.js skills.

This reference explains React Server Components as a **React feature** — the mental model, the boundary semantics, and the security rules. It deliberately stops at the framework edge: route loaders, caching, and App Router data fetching belong to the Next.js skills.

## Server Components by Default

In an RSC setup, components render on the server **ahead of time** and produce a serializable description of the UI. Server Components:

- Cannot hold state (`useState`), run effects (`useEffect`), or use browser-only APIs — they never run on the client.
- Can be `async` and `await` data directly in the component body.
- Reduce client JavaScript: their code is not shipped to the browser.

```tsx
// A Server Component: async, no hooks, code stays on the server.
async function ArticlePage({ id }: { id: string }) {
  const article = await db.articles.find(id); // direct data access on the server
  return (
    <article>
      <h1>{article.title}</h1>
      <LikeButton articleId={id} /> {/* a Client Component island */}
    </article>
  );
}
```

## The Boundary Is on the Module Graph, Not the Render Tree

The single most important model: `'use client'` marks a **module** (and everything it imports) as client code. The boundary is drawn on the **module dependency graph**, not on the render tree. Once a module is `'use client'`, the components it defines are Client Components, and modules it imports join the client bundle.

```tsx
'use client'; // this directive makes the whole module client code

import { useState } from 'react';

export function LikeButton({ articleId }: { articleId: string }) {
  const [liked, setLiked] = useState(false); // hooks allowed: this is a Client Component
  return <button onClick={() => setLiked(true)}>{liked ? '♥' : '♡'}</button>;
}
```

### Two consequences that surprise newcomers

1. **Props crossing into a Client Component must be serializable.** Numbers, strings, plain objects, arrays, and Server Functions cross the boundary; class instances, functions (other than Server Functions), and symbols do not.

2. **A Client Component can render a Server Component passed as `children`.** Composition through `children` lets a server-rendered subtree sit *inside* a client component without that subtree becoming client code.

```tsx
// Client Component accepts server-rendered children — the children stay on the server.
'use client';
export function Collapsible({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button onClick={() => setOpen((v) => !v)}>Toggle</button>
      {open && children} {/* may be a Server Component subtree */}
    </>
  );
}
```

## `'use server'` — Server Functions

`'use server'` marks a function (or a module of functions) as a **Server Function**: callable from the client but executed on the server. Server Functions are the mutation counterpart to Server Components.

```tsx
'use server';

export async function publishComment(formData: FormData) {
  const text = formData.get('text');
  // Arguments arrive from an untrusted client — validate and authorize.
  if (typeof text !== 'string' || text.length === 0) throw new Error('invalid');
  await requireAuthenticatedUser();
  await db.comments.insert({ text });
}
```

**Security rule:** a Server Function's arguments are an **untrusted, public-facing input boundary**, exactly like an HTTP endpoint. Validate every argument and authorize the caller inside the function — never assume the client sent well-formed or permitted data.

## Explicit Defer to Next.js Skills

The following are **framework** concerns and belong to the Next.js skills, not this skill:

- Route-level data fetching, loaders, and the App Router model.
- Caching directives (`"use cache"`, `revalidateTag`, `revalidatePath`) and request-time vs build-time rendering.
- Bundler configuration that wires the RSC graph.

## Version Pinning

RSC depends on bundler-facing APIs that are **not semver-stable within React 19.x**. Pin the exact React and React-DOM versions (and align them with the framework's expected versions) rather than using a caret range, so a patch bump does not break the server/client wiring.

```json
{
  "dependencies": {
    "react": "19.2.0",
    "react-dom": "19.2.0"
  }
}
```

## Anti-Patterns

| Anti-pattern | Why it is wrong | Detection |
|---|---|---|
| Using hooks/state in a Server Component | Server Components never run on the client | Build/runtime error referencing `useState` in a server module |
| Passing non-serializable props across the boundary | Only serializable values and Server Functions cross | "cannot be passed to Client Components" error |
| Trusting Server Function arguments | They are a public input boundary | Missing validation/authorization in `'use server'` functions |
| Caret-ranged React in an RSC app | RSC bundler APIs are not semver-stable in 19.x | Patch bump breaks server/client wiring |
| Reaching here for caching/routing | Those are framework concerns | Looking for `revalidateTag` in this skill — use Next.js skills |

## Sources

- https://react.dev/reference/rsc/server-components
- https://react.dev/reference/rsc/use-client
- https://react.dev/reference/rsc/use-server
