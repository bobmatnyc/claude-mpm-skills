# Client and server usage

## Create a client instance
Import the framework-specific client (or the vanilla client) and create the instance.

```ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: "http://localhost:3000", // optional if same domain
});
```

Framework packages include:
- `better-auth/react`
- `better-auth/vue`
- `better-auth/svelte`
- `better-auth/solid`

## Common client calls
```ts
const { data, error } = await authClient.signIn.email({
  email,
  password,
});

const { data: session } = await authClient.getSession();
```

Use `authClient.useSession()` for reactive session state in supported frameworks.

## Server-side API calls
Call endpoints through `auth.api` and pass inputs as `{ body, headers, query }`.

```ts
import { auth } from "./auth";

const session = await auth.api.getSession({
  headers: request.headers,
});

await auth.api.signInEmail({
  body: { email, password },
  headers: request.headers,
});
```

### Return headers or Response
```ts
const { headers } = await auth.api.signUpEmail({
  returnHeaders: true,
  body: { email, password, name },
});

const response = await auth.api.signInEmail({
  body: { email, password },
  asResponse: true,
});
```

### Error handling
```ts
import { APIError, isAPIError } from "better-auth/api";

try {
  await auth.api.signInEmail({
    body: { email, password },
  });
} catch (error) {
  if (isAPIError(error)) {
    console.error(error.message, error.status);
  }
}
```
