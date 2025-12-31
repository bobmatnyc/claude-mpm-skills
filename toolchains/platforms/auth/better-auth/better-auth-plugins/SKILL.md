---
name: better-auth-plugins
description: Better Auth plugin system for TypeScript. Use when adding advanced auth features (2FA, magic link, passkey, username, JWT, organizations) via server and client plugins.
progressive_disclosure:
  entry_point:
    summary: "Better Auth plugin system for TypeScript. Use when adding advanced auth features (2FA, magic link, passkey, username, JWT, organizations) via server and client plugins."
    when_to_use: "When implementing authentication, authorization, or security."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - plugins-index.md
---
# Better Auth Plugins

## Goals
- Add server plugins to extend auth features.
- Add client plugins for matching client methods.
- Apply schema changes when plugins add tables.

## Quick start
1. Import the plugin from `better-auth/plugins` and add it to `plugins`.
2. Run migrations (`generate` or `migrate`) when required.
3. Add the client plugin from `better-auth/client/plugins`.

### Example: Two-factor authentication
```ts
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [twoFactor()],
});
```

```ts
import { createAuthClient } from "better-auth/client";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [twoFactorClient({ twoFactorPage: "/two-factor" })],
});
```

## Migration reminder
Run the CLI when a plugin adds tables:

```bash
npx @better-auth/cli generate
```

```bash
npx @better-auth/cli migrate
```

## Guardrails
- Add server and client plugins together to keep APIs aligned.
- Keep `nextCookies` (if used) last in the server plugin list.
- Review plugin docs for required schema and env variables.

## References
- `toolchains/platforms/auth/better-auth/better-auth-plugins/references/plugins-index.md`
