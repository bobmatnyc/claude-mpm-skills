---
name: better-auth-core
description: Better Auth core setup for TypeScript apps. Use when configuring the Better Auth instance, wiring server handlers and client instances, working with sessions, or calling server-side auth APIs.
progressive_disclosure:
  entry_point:
    summary: "Better Auth core setup for TypeScript apps. Use when configuring the Better Auth instance, wiring server handlers and client instances, working with sessions, or calling server-side auth APIs."
    when_to_use: "When implementing authentication, authorization, or security."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - client-server.md
    - setup-database.md
    - typescript.md
---
# Better Auth Core (TypeScript)

## Goals
- Set up a Better Auth instance with environment variables and data layer wiring.
- Wire server handlers and a client instance.
- Use sessions and server-side API methods safely.
- Keep data-layer choices pluggable (drivers or adapters).

## Quick start
1. Install `better-auth`.
2. Set `BETTER_AUTH_SECRET` (32+ chars) and `BETTER_AUTH_URL`.
3. Create `auth.ts` and export `auth`.
4. Provide `database` (driver or adapter) or omit for stateless sessions.
5. Mount a handler (`auth.handler` or a framework helper).
6. Create a client with `createAuthClient`.

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: myDatabaseOrAdapter, // driver or adapter; omit for stateless mode
  emailAndPassword: { enabled: true },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
    },
  },
});
```

## Core setup checklist
- Export the instance as `auth` (or default export) so helpers find it.
- Keep `BETTER_AUTH_URL` in sync with the public base URL.
- Pass the full base URL to the client if you change the `/api/auth` base path.
- Add database migrations before enabling plugins that require tables.

## Server API usage
- Call server endpoints via `auth.api.*` with `{ body, headers, query }`.
- Use `asResponse: true` if you need a `Response` object.
- Use `returnHeaders: true` to access `Set-Cookie` headers.

```ts
import { auth } from "./auth";

const session = await auth.api.getSession({
  headers: request.headers,
});

const response = await auth.api.signInEmail({
  body: { email, password },
  asResponse: true,
});
```

## Session access
- Client: `authClient.useSession()` or `authClient.getSession()`.
- Server: `auth.api.getSession({ headers })`.

## TypeScript tips
- Infer types with `auth.$Infer` and `authClient.$Infer`.
- Use `inferAdditionalFields` on the client when you extend the user schema.

## References
- `toolchains/platforms/auth/better-auth/better-auth-core/references/setup-database.md`
- `toolchains/platforms/auth/better-auth/better-auth-core/references/client-server.md`
- `toolchains/platforms/auth/better-auth/better-auth-core/references/typescript.md`
