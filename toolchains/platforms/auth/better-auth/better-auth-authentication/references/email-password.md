# Email and password flows

## Enable email and password
```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
  },
});
```

## Sign up
```ts
await authClient.signUp.email({
  name,
  email,
  password,
  image,
  callbackURL: "/dashboard",
});
```

Disable automatic sign-in after sign-up:
```ts
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    autoSignIn: false,
  },
});
```

## Sign in
```ts
await authClient.signIn.email({
  email,
  password,
  rememberMe: true,
  callbackURL: "/dashboard",
});
```

## Sign out
```ts
await authClient.signOut();
```

Redirect on sign-out:
```ts
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => {
      router.push("/login");
    },
  },
});
```

## Email verification
Provide a server-side function that sends the verification email:

```ts
import { betterAuth } from "better-auth";
import { sendEmail } from "./email";

export const auth = betterAuth({
  emailVerification: {
    sendVerificationEmail: async ({ user, url, token }, request) => {
      void sendEmail({
        to: user.email,
        subject: "Verify your email address",
        text: `Click the link to verify your email: ${url}`,
      });
    },
  },
});
```

Require verification on sign-in:

```ts
export const auth = betterAuth({
  emailAndPassword: {
    requireEmailVerification: true,
  },
});
```

Handle verification errors on sign-in:

```ts
await authClient.signIn.email(
  { email, password },
  {
    onError: (ctx) => {
      if (ctx.error.status === 403) {
        alert("Please verify your email address");
      }
    },
  }
);
```
