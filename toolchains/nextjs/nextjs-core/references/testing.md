# Testing Next.js App Router Apps

## Strategy

Use a layered approach:
- Unit tests for pure logic (parsing, validation, policies).
- Component tests for Client Components.
- Integration/E2E tests for critical user flows.

## Server Code: Make It Testable

Make server code testable by extracting business logic into pure functions and keeping handlers/actions as thin wrappers.

✅ Pattern: thin wrapper + pure core
```ts
// lib/posts.ts
export async function createPostCore(input: { title: string }, userId: string) {
  return db.posts.create({ data: { title: input.title, authorId: userId } });
}

// app/api/posts/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = await req.json();
  const post = await createPostCore(body, "test-user");
  return NextResponse.json(post, { status: 201 });
}
```

❌ Anti-pattern: monolithic handler logic
```ts
// app/api/posts/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = await req.json();
  if (!body?.title) {
    return NextResponse.json({ error: "invalid" }, { status: 400 });
  }

  const post = await db.posts.create({
    data: { title: body.title, authorId: "test-user" },
  });

  await fetch("https://example.com/webhook", {
    method: "POST",
    body: JSON.stringify(post),
  });

  return NextResponse.json(post, { status: 201 });
}
```

## Client Components

Test Client Components with a DOM-focused runner:
- validate rendering and UI state transitions
- mock network boundaries at the edges

Avoid over-testing framework wiring.

## E2E (Recommended for Critical Flows)

Run one E2E suite for:
- auth/login
- checkout/payment
- tenant switching / admin actions

Keep E2E stable:
- use `data-testid` selectors
- avoid fixed sleeps; wait on visible state or network aliases
- seed deterministic test data

Pair with `playwright` or `cypress` skills for tooling patterns.

## Anti-patterns

- ❌ Assert on implementation details (internal component state); ✅ assert on user-visible behavior.
- ❌ Flaky waits (`wait(1000)`); ✅ wait on conditions or network.
- ❌ E2E everything; ✅ reserve E2E for critical flows and keep the rest unit/component tests.
