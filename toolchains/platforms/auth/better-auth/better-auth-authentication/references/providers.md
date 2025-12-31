# Social providers

## Configure providers
Set providers in `socialProviders` and pass provider credentials.

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
    },
  },
});
```

## Sign in with a provider
```ts
await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
  errorCallbackURL: "/error",
  newUserCallbackURL: "/welcome",
  disableRedirect: false,
});
```

## Provider docs
Use provider-specific docs to configure redirect URLs and scopes.

Common providers:
- GitHub: https://www.better-auth.com/docs/authentication/github
- Google: https://www.better-auth.com/docs/authentication/google
- Apple: https://www.better-auth.com/docs/authentication/apple
- Discord: https://www.better-auth.com/docs/authentication/discord
- GitLab: https://www.better-auth.com/docs/authentication/gitlab
- Microsoft: https://www.better-auth.com/docs/authentication/microsoft
- Slack: https://www.better-auth.com/docs/authentication/slack

More providers:
- Other social providers list: https://www.better-auth.com/docs/authentication/other-social-providers
