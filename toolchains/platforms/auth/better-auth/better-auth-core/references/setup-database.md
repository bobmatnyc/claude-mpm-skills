# Setup and data layer

## Environment variables
Set the required secrets and base URL:

```txt
BETTER_AUTH_SECRET=replace-with-32-plus-chars
BETTER_AUTH_URL=http://localhost:3000
```

## Create the auth instance
Create `auth.ts` and export `auth` (or default export):

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  // configure database and auth methods here
});
```

## Data layer options
Use either a direct driver or an adapter. Pass it to `database`.

### Direct drivers (examples)
```ts
import { betterAuth } from "better-auth";
import Database from "better-sqlite3";

export const auth = betterAuth({
  database: new Database("./sqlite.db"),
});
```

```ts
import { Pool } from "pg";
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: new Pool({
    // connection options
  }),
});
```

```ts
import { createPool } from "mysql2/promise";
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: createPool({
    // connection options
  }),
});
```

### Adapters (examples)
```ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db";

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg" }),
});
```

```ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@/generated/prisma/client";

const prisma = new PrismaClient();

export const auth = betterAuth({
  database: prismaAdapter(prisma, { provider: "sqlite" }),
});
```

```ts
import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { client } from "@/db";

export const auth = betterAuth({
  database: mongodbAdapter(client),
});
```

### Stateless mode
Omit `database` for stateless session management. Note that most plugins require a database.

## Create tables and migrations
Use the CLI to generate or apply schema changes:

```bash
npx @better-auth/cli generate
```

```bash
npx @better-auth/cli migrate
```

`migrate` is available only for the built-in Kysely adapter. Use `generate` to create SQL or ORM schema files for manual migrations.
