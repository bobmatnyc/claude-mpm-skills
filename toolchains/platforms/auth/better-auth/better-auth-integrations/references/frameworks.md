# Framework handler recipes

## SvelteKit
```ts
import { auth } from "$lib/auth";
import { svelteKitHandler } from "better-auth/svelte-kit";
import { building } from "$app/environment";

export async function handle({ event, resolve }) {
  return svelteKitHandler({ event, resolve, auth, building });
}
```

## Remix
```ts
import { auth } from "~/lib/auth.server";
import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  return auth.handler(request);
}

export async function action({ request }: ActionFunctionArgs) {
  return auth.handler(request);
}
```

## Express
```ts
import express from "express";
import { toNodeHandler } from "better-auth/node";
import { auth } from "./auth";

const app = express();
app.all("/api/auth/*", toNodeHandler(auth));
app.use(express.json());
```

## Hono
```ts
import { Hono } from "hono";
import { auth } from "./auth";

const app = new Hono();
app.on(["POST", "GET"], "/api/auth/*", (c) => auth.handler(c.req.raw));
```

## Cloudflare Workers
```ts
import { auth } from "./auth";

export default {
  async fetch(request: Request) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/api/auth")) {
      return auth.handler(request);
    }
    return new Response("Not found", { status: 404 });
  },
};
```
