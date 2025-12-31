---
name: better-auth-authentication
description: Better Auth authentication flows for TypeScript apps. Use when enabling email/password auth, configuring social providers, or implementing sign-up, sign-in, and verification flows.
progressive_disclosure:
  entry_point:
    summary: "Better Auth authentication flows for TypeScript apps. Use when enabling email/password auth, configuring social providers, or implementing sign-up, sign-in, and verification flows."
    when_to_use: "When implementing authentication, authorization, or security."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - email-password.md
    - providers.md
---
# Better Auth Authentication

## Goals
- Enable email/password authentication and social providers.
- Implement sign-up, sign-in, sign-out, and verification flows.
- Handle redirects and errors consistently.

## Quick start
1. Enable `emailAndPassword` and configure `socialProviders`.
2. Create a client with `createAuthClient`.
3. Use `signUp.email`, `signIn.email`, `signIn.social`, and `signOut` on the client.

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  emailAndPassword: { enabled: true },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
    },
  },
});
```

```ts
import { createAuthClient } from "better-auth/client";

const authClient = createAuthClient();

await authClient.signUp.email({
  email,
  password,
  name,
});

await authClient.signIn.email({
  email,
  password,
  callbackURL: "/dashboard",
});

await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
});

await authClient.signOut();
```

## Email verification
- Provide `emailVerification.sendVerificationEmail` to send the verification link.
- Use `emailAndPassword.requireEmailVerification` to enforce verification before sign-in.

## Social providers
- Configure providers in `socialProviders` with provider-specific credentials.
- Use `signIn.social` to start OAuth flows.
- Pass `callbackURL`, `errorCallbackURL`, and `newUserCallbackURL` for redirects.

## Guardrails
- Call client methods from the client only.
- Keep secrets in server-only env variables.
- Use `rememberMe` to control persistent sessions on email/password sign-in.

## References
- `toolchains/platforms/auth/better-auth/better-auth-authentication/references/email-password.md`
- `toolchains/platforms/auth/better-auth/better-auth-authentication/references/providers.md`
