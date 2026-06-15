# Concurrent Rendering

> Source of truth: [useTransition](https://react.dev/reference/react/useTransition), [useDeferredValue](https://react.dev/reference/react/useDeferredValue), [Suspense](https://react.dev/reference/react/Suspense), and [renderToPipeableStream](https://react.dev/reference/react-dom/server/renderToPipeableStream). This reference applies that guidance.

Concurrent rendering lets React prepare a new UI in the background and interrupt it for more urgent work. Urgent updates (typing, clicking) stay responsive while expensive updates (filtering thousands of rows, navigating) render without blocking input.

## `useTransition`

`useTransition` marks a state update as a non-urgent **transition**. React renders the transition in the background, keeps the current UI interactive, and exposes `isPending` so the UI can show a subtle pending indication without a hard fallback.

```tsx
function TabbedView() {
  const [tab, setTab] = useState<'home' | 'reports'>('home');
  const [isPending, startTransition] = useTransition();

  function select(next: 'home' | 'reports') {
    // The tab button responds instantly; the heavy panel renders as a transition.
    startTransition(() => setTab(next));
  }

  return (
    <>
      <TabBar active={tab} onSelect={select} busy={isPending} />
      {tab === 'reports' ? <ExpensiveReports /> : <Home />}
    </>
  );
}
```

### React 19 async transitions and the post-`await` gotcha

React 19 allows `startTransition` to receive an async function (an "Action"). The subtle rule: only updates issued **synchronously within the transition scope** belong to the transition. Updates after an `await` run in a fresh task and escape it unless re-wrapped.

```tsx
// BAD: setResult runs after await, outside the transition; isPending ends early.
startTransition(async () => {
  const data = await fetchData();
  setResult(data);
});
```

```tsx
// GOOD: re-wrap the post-await update so it stays part of the transition.
startTransition(async () => {
  const data = await fetchData();
  startTransition(() => setResult(data));
});
```

## `startTransition` (standalone) vs `useDeferredValue`

`startTransition` (the standalone import) marks an update urgent-or-not at the **call site** — appropriate when an event handler triggers the expensive update. `useDeferredValue` marks a **value** as allowed to lag — appropriate when an expensive subtree should trail a fast-changing input.

Prefer `useDeferredValue` over a fixed `setTimeout` debounce for expensive *derived renders*: it is interruptible and device-adaptive (it defers more on slow devices, less on fast ones) rather than imposing one fixed delay on every user.

```tsx
function FilterList({ rows }: { rows: Row[] }) {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text, ''); // React 19 initialValue

  const filtered = rows.filter((r) => r.label.includes(deferredText));
  const isStale = text !== deferredText;

  return (
    <>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <ul style={{ opacity: isStale ? 0.6 : 1 }}>
        {filtered.map((r) => <li key={r.id}>{r.label}</li>)}
      </ul>
    </>
  );
}
```

## Suspense for Data

A component suspends when it reads a not-yet-resolved promise — either thrown by a data layer or read via `use()`. The nearest `<Suspense fallback>` shows until the promise resolves.

```tsx
function Page({ userPromise }: { userPromise: Promise<User> }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <Profile userPromise={userPromise} />
    </Suspense>
  );
}

function Profile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // suspends until resolved
  return <h1>{user.name}</h1>;
}
```

### Resetting a boundary with `key`

Changing the `key` on a Suspense boundary (or a component inside it) discards the previous tree and re-suspends — useful when switching the resource a boundary displays.

```tsx
// A new id remounts ProfileLoader and re-suspends on the new request.
<Suspense fallback={<Skeleton />}>
  <ProfileLoader key={userId} userId={userId} />
</Suspense>
```

### Fallback timing

A transition does **not** show a Suspense fallback for already-revealed content — that is what keeps navigation from flashing skeletons. Initial reveals still show the fallback. Design fallbacks to match the final layout to avoid layout shift.

## Streaming SSR (React Level)

For Node servers, `renderToPipeableStream` streams HTML as Suspense boundaries resolve. Design a meaningful **shell** — header, navigation, layout — that flushes immediately, and let slower data stream in behind Suspense rather than blocking the whole document on one root spinner.

```tsx
import { renderToPipeableStream } from 'react-dom/server';

function handler(req, res) {
  const { pipe, abort } = renderToPipeableStream(<App />, {
    bootstrapScripts: ['/main.js'],
    onShellReady() {
      // The shell (everything outside Suspense) is ready: start streaming.
      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/html');
      pipe(res);
    },
    onShellError(error) {
      res.statusCode = 500;
      res.send('<!doctype html><p>Loading failed</p>');
    },
  });

  setTimeout(abort, 10_000); // bound the stream
}
```

React 19.2 (2025-10-01) batches Suspense reveals that land close together — with a heuristic that protects Largest Contentful Paint — and adds Web Streams SSR plus `resume` for prerender-then-resume flows. `renderToReadableStream` serves Web-Streams runtimes (edge, Deno, Bun).

**Framework defer:** App Router streaming, route-level Suspense placement, and data-fetching orchestration belong to the Next.js skills. This reference covers the React-level primitives those frameworks build on.

## Anti-Patterns

| Anti-pattern | Why it is wrong | Detection |
|---|---|---|
| State update after `await` in an async transition | Escapes the transition; `isPending` ends early | UI flips to non-pending mid-operation |
| Fixed debounce/throttle for expensive derived renders | `useDeferredValue` is interruptible and adaptive | Janky typing on slow devices; hard-coded timers |
| One root spinner instead of a streamed shell | Blocks first paint on the slowest data | Long blank time-to-first-byte; no progressive reveal |
| Suspense fallback that mismatches final layout | Causes layout shift on reveal | Visible jump when content arrives |

## Sources

- https://react.dev/reference/react/useTransition
- https://react.dev/reference/react/startTransition
- https://react.dev/reference/react/useDeferredValue
- https://react.dev/reference/react/Suspense
- https://react.dev/reference/react-dom/server/renderToPipeableStream
- https://react.dev/reference/react-dom/server/renderToReadableStream
- https://react.dev/blog/2025/10/01/react-19-2
