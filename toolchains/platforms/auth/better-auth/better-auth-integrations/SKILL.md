---
name: better-auth-integrations
description: Better Auth framework integrations for TypeScript. Use when wiring route handlers in Next.js, SvelteKit, Remix, Express, Hono, or other web frameworks.
progressive_disclosure:
  entry_point:
    summary: "Better Auth framework integrations for TypeScript. Use when wiring route handlers in Next.js, SvelteKit, Remix, Express, Hono, or other web frameworks."
    when_to_use: "When implementing authentication, authorization, or security."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - frameworks.md
    - nextjs.md
---
# Better Auth Integrations

## Goals
- Mount the Better Auth handler at `/api/auth/*` (or a custom base path).
- Use framework helpers where available.
- Ensure cookies and headers flow correctly in SSR and server actions.

## Quick start
1. Create an `auth` instance (see `better-auth-core`).
2. Add a catch-all route for `/api/auth/*`.
3. Use a framework helper (or `auth.handler`) to return a Response.

### Next.js App Router
```ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### Next.js Pages Router
```ts
import { auth } from "@/lib/auth";
import { toNodeHandler } from "better-auth/node";

export const config = { api: { bodyParser: false } };
export default toNodeHandler(auth.handler);
```

## Cookie handling in Next.js server actions
Use the `nextCookies` plugin so server actions set cookies correctly.

```ts
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

export const auth = betterAuth({
  // ...config
  plugins: [nextCookies()],
});
```

## Guardrails
- Keep the base path consistent between server and client.
- Prefer framework helpers when available.
- Avoid running custom body parsers before the auth handler.

## References
- `toolchains/platforms/auth/better-auth/better-auth-integrations/references/nextjs.md`
- `toolchains/platforms/auth/better-auth/better-auth-integrations/references/frameworks.md`
