# TypeScript and type inference

## Infer core types
Use `$Infer` to extract types from the server or client instance.

```ts
import { createAuthClient } from "better-auth/client";

const authClient = createAuthClient();
export type Session = typeof authClient.$Infer.Session;
```

```ts
import { betterAuth } from "better-auth";
import Database from "better-sqlite3";

export const auth = betterAuth({
  database: new Database("database.db"),
});

type Session = typeof auth.$Infer.Session;
```

## Add additional fields
Define additional fields on the user or session and keep them out of user input when needed.

```ts
import { betterAuth } from "better-auth";
import Database from "better-sqlite3";

export const auth = betterAuth({
  database: new Database("database.db"),
  user: {
    additionalFields: {
      role: {
        type: "string",
        input: false,
      },
    },
  },
});
```

## Infer additional fields on the client
When server and client live in the same project, use `inferAdditionalFields`.

```ts
import { createAuthClient } from "better-auth/react";
import { inferAdditionalFields } from "better-auth/client/plugins";
import type { auth } from "./auth";

export const authClient = createAuthClient({
  plugins: [inferAdditionalFields<typeof auth>()],
});
```

When client and server are separate, specify the fields directly.

```ts
import { createAuthClient } from "better-auth/client";
import { inferAdditionalFields } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    inferAdditionalFields({
      user: {
        role: { type: "string" },
      },
    }),
  ],
});
```
