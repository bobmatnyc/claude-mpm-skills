---
name: react-advanced
description: Modern React 19 platform features and rendering architecture - the React Compiler (auto-memoization) and how it changes memoization guidance, concurrent rendering (useTransition/useDeferredValue/Suspense), the use() hook, Actions (useActionState/useOptimistic/useFormStatus), ref-as-prop and Context-as-provider changes, compound components, context selectors, error boundaries, portals, virtualization, code-splitting, and the RSC/'use client' boundary.
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "React 19 platform features + rendering architecture: React Compiler auto-memoization, concurrent rendering, use()/Actions hooks, advanced component patterns, virtualization & code-splitting, RSC boundary"
    when_to_use: "Adopting the React Compiler; using concurrent features; building with React 19 Actions/forms or use(); optimizing render performance; architecting compound components, context selectors, error boundaries, or portals; reasoning about the RSC/'use client' boundary"
    quick_start: "1. Enable eslint-plugin-react-hooks v6+ and fix Rules of React, then turn on the React Compiler 2. Stop hand-memoizing; use useMemo/useCallback only as an escape hatch 3. Use useTransition/useDeferredValue for responsiveness 4. Use Actions (useActionState/useOptimistic) for async mutations"
  references:
    - react-compiler.md
    - concurrent-rendering.md
    - react19-actions-and-apis.md
    - component-patterns.md
    - performance.md
    - rsc-boundary.md
context_limit: 700
tags:
  - react
  - react-19
  - react-compiler
  - concurrent
  - useTransition
  - useDeferredValue
  - suspense
  - use-hook
  - useActionState
  - useOptimistic
  - actions
  - performance
  - virtualization
  - code-splitting
  - error-boundaries
  - portals
  - context-optimization
  - rsc
requires_tools: []
---

# React Advanced: React 19 Platform & Rendering Architecture

## Overview

The reference for React-19-era platform capabilities and rendering architecture. This skill covers the features that reshape how modern React applications are built and optimized: the React Compiler and the end of reflexive manual memoization, concurrent rendering primitives, the `use()` hook, Actions and the form hooks, the React 19 ergonomic changes (ref as a plain prop, `<Context>` as provider, native metadata), advanced component-architecture patterns, rendering-performance engineering, and a conceptual treatment of the React Server Component boundary.

This guidance treats **React 19 (Dec 2024) and React Compiler 1.0 (stable Oct 2025)** as current. Pre-19 memoization advice — wrapping values in `useMemo`/`useCallback`/`React.memo` by reflex — is now an anti-pattern for new code. The compiler memoizes automatically. Authoritative documentation lives at [react.dev](https://react.dev/); this skill distills and applies it rather than restating it.

## Boundary Map: What This Skill Does NOT Cover

This skill stays focused on the React-19 platform and rendering architecture. Defer to the owning skill for everything else:

| Topic | Owning skill |
|---|---|
| Core hooks tutorial (`useState`/`useEffect`/`useRef`/`useMemo`/`useCallback`/`useContext`), JSX, props/state, lists, controlled inputs | **react-core** |
| Advanced custom-hook *composition* recipes — SWR-backed data hooks, debounced search, memoized-provider value pattern, discriminated-union hook states | **react-hooks-composition** |
| Explicit finite-state-machine modeling with XState v5 (`setup()`, actors, guards, parallel states) | **react-state-machine** |
| Server-state caching, query invalidation, optimistic updates via React Query | **tanstack-query** |
| Global client state via a store with no providers | **zustand** |
| Framework wiring of Server Components, Server Actions (`revalidateTag`/`revalidatePath`), App Router data fetching, caching, Turbopack | **Next.js skills** (`nextjs-core`, `nextjs-v16`) |
| Docking layout UI (drag-drop panels, splitters) | **flexlayout-react** |

This skill explains the *React-level* concepts (concurrent rendering, the RSC boundary as a React feature, Actions as a React primitive). Framework-specific wiring of those concepts belongs to the Next.js skills.

## When to Use This Skill

Reach for this skill when:
- Adopting the React Compiler and untangling the old memoization habits
- Using concurrent features (`useTransition`, `useDeferredValue`, Suspense for data) to keep a UI responsive
- Building with React 19 Actions, forms, or the `use()` hook
- Optimizing render performance: context over-rendering, large lists, code-splitting
- Architecting compound components, context selectors, error boundaries, or portals
- Reasoning about the RSC / `'use client'` boundary at the React level

## The React Compiler — and the End of Manual Memoization

The React Compiler reached **1.0 stable on 2025-10-07**. It is a build-time tool that auto-memoizes components and hooks at fine granularity, including *conditional* memoization that hand-written `useMemo` cannot express. It works with React 17, 18, and 19, and performs best on 19.

**The change vs React 17/18:** the long-standing advice to wrap values in `useMemo`/`useCallback` and components in `React.memo` is obsolete for new code. The compiler handles memoization. Scattering manual memo by reflex now adds noise and can be net-negative.

```tsx
// BEFORE (pre-compiler reflex): hand-memoize everything
const sorted = useMemo(() => items.slice().sort(compare), [items]);
const onPick = useCallback((id: string) => onSelect(id), [onSelect]);
const Row = React.memo(function Row({ item }: { item: Item }) { /* ... */ });
```

```tsx
// AFTER (compiler enabled): write plain code; the compiler memoizes
const sorted = items.slice().sort(compare);
const onPick = (id: string) => onSelect(id);
function Row({ item }: { item: Item }) { /* ... */ }
```

**When manual memo still matters (the escape hatch):**
- A computed value feeds an **effect dependency array** and must hold a stable reference for correctness, not just performance.
- Code the compiler cannot statically analyze — it safely skips such components rather than miscompiling them, so manual memo remains a valid local optimization.

**Existing code:** the compiler *preserves* manual memoization on purpose; the `preserve-manual-memoization` lint flags memo that was load-bearing. Do not strip `useMemo`/`useCallback` blindly after enabling the compiler.

**Adoption path:** install `eslint-plugin-react-hooks` v6+ (it absorbed the former `eslint-plugin-react-compiler`) → fix the reported Rules of React violations → enable the compiler in the build (Babel / Vite / Metro / Rsbuild). React DevTools shows a "Memo ✨" badge on compiler-optimized components.

Full adoption guide, per-bundler setup, and before/after analysis: [react-compiler.md](references/react-compiler.md).

## Concurrent Rendering

Concurrent features let React interrupt and prioritize rendering so urgent updates (typing) stay responsive while expensive updates (filtering a large list) yield.

- **`useTransition`** marks a state update as non-urgent and exposes `isPending`. React keeps the old UI interactive while the transition renders in the background.
- **React 19 async transitions:** `startTransition` accepts async functions. The gotcha: state updates issued *after* an `await` fall outside the transition unless re-wrapped in `startTransition`.
- **`useDeferredValue`** produces a lagging copy of a value and is interruptible and device-adaptive. Prefer it over a fixed `setTimeout` debounce for expensive derived renders; React 19 adds an `initialValue`.
- **Suspense for data** suspends on a thrown promise (or one read via `use()`) and shows the nearest `<Suspense fallback>`. A changing `key` resets a boundary.

```tsx
function ProductSearch({ allProducts }: { allProducts: Product[] }) {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query); // lags behind input under load

  // Filtering reads the deferred value, so typing stays responsive.
  const results = allProducts.filter((p) => p.name.includes(deferredQuery));

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ResultsList results={results} stale={query !== deferredQuery} />
    </>
  );
}
```

Streaming SSR at the React level (`renderToPipeableStream`, shell design, Suspense reveal batching in 19.2) is covered in [concurrent-rendering.md](references/concurrent-rendering.md); framework streaming specifics defer to the Next.js skills.

## React 19 Platform Hooks & APIs

### The `use()` hook

`use()` reads a promise or a context value and may be called **conditionally** — after early returns — a deliberate exception to the Rules of Hooks. It cannot sit inside `try/catch`; surface rejected promises through an Error Boundary instead. Prefer creating the promise high in the tree (or on the server) and passing it down, since a promise created during render is recreated each render.

### Actions

Actions are the React-level async-mutation primitive, independent of any framework:
- **`useActionState`** (renamed from the canary `useFormState`) runs an action, tracking pending and error state and threading the previous result forward.
- **`useOptimistic`** renders an optimistic value while the action is in flight, reverting automatically on completion.
- **`useFormStatus`** reads the pending state of the enclosing `<form>` from a child, with no prop drilling.
- **`<form action={fn}>`** wires a function directly to submission, auto-resetting on success.

```tsx
function NameForm({ save }: { save: (name: string) => Promise<string> }) {
  const [error, submit, isPending] = useActionState(
    async (_prev: string | null, formData: FormData) => {
      const result = await save(formData.get('name') as string);
      return result.startsWith('error') ? result : null;
    },
    null,
  );

  return (
    <form action={submit}>
      <input name="name" disabled={isPending} />
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
```

### Ergonomic changes

- **`ref` is a plain prop.** `forwardRef` is deprecated (a codemod migrates existing usage); a function component receives `ref` like any other prop.
- **`<Context value>`** replaces `<Context.Provider>`, which is now legacy.
- **Native document metadata:** `<title>`, `<meta>`, and `<link>` hoist to `<head>` automatically, replacing `react-helmet`. `preload`/`preinit`/`preconnect` handle resource hints.

Complete examples and migration notes from 17/18: [react19-actions-and-apis.md](references/react19-actions-and-apis.md).

## Advanced Component Patterns

- **Compound components** share implicit state through context so a parent and its sub-components coordinate without prop drilling (`<Tabs>` / `<Tabs.Tab>`).
- **Context optimization:** native context has **no selector**. Any change to a provider value re-renders *all* consumers; `React.memo` does not block context-driven re-renders, and `use(Context)` adds conditional reading but **not** selective subscription. The compiler does not fix large-context over-rendering. The native fixes are memoizing the provider value and splitting contexts by change frequency; the userland `use-context-selector` adds slice subscriptions (with tearing/legacy caveats).
- **Render props vs custom hooks:** hooks win for logic reuse; render props remain useful for headless "what to render" components.
- **Error boundaries** are still class-based; `react-error-boundary` adds a hook (`useErrorBoundary`) for async and event-handler errors that native boundaries miss. React 19 logs caught errors once and adds `onCaughtError`/`onUncaughtError`.
- **Portals** (`createPortal`) change DOM placement only — context and errors still flow through the React tree, not the DOM tree.

Decision guides and full examples: [component-patterns.md](references/component-patterns.md).

## Performance Architecture

- **Virtualization** renders only visible rows. `@tanstack/react-virtual` is the modern headless choice with the strongest TypeScript story; `react-window` is mature but stalled; `react-virtuoso` is batteries-included. After virtualizing, the per-item renderer cost becomes the bottleneck — keep rows light.
- **Code-splitting** with `React.lazy` + `Suspense` splits by route first. Avoid over-splitting tiny components into many sub-10KB chunks, which adds request overhead without payoff.
- **Profiling** uses the React DevTools Profiler against a production build to see what actually re-rendered and why; Why-Did-You-Render helps trace avoidable renders.

Library comparison, code-splitting strategy, and the full anti-pattern → detection → fix table: [performance.md](references/performance.md).

## RSC / `'use client'` Boundary (Conceptual)

React Server Components render ahead of time, cannot hold state or run effects, and produce serializable output. The boundary is defined on the **module dependency graph** (a `'use client'` directive at the top of a module), not on the render tree. Props crossing into a Client Component must be serializable, and a Client Component may still render a Server Component passed to it as `children`. The `'use server'` directive marks Server *Functions* whose arguments are untrusted and must be validated and authorized.

**Explicit defer:** caching, route loaders, and App Router data fetching belong to the Next.js skills. Pin the React version, since RSC bundler APIs are not semver-stable within 19.x. Conceptual model and the framework hand-off: [rsc-boundary.md](references/rsc-boundary.md).

## Anti-Patterns to Avoid

### ❌ Don't: Hand-memoize everything with the compiler enabled

```tsx
// BAD: redundant manual memo once the compiler is on; adds noise and cost
const value = useMemo(() => ({ a, b }), [a, b]);
const onClick = useCallback(() => doThing(a), [a]);
```

```tsx
// GOOD: write plain code; let the compiler memoize
const value = { a, b };
const onClick = () => doThing(a);
```

### ❌ Don't: Strip manual memo blindly after enabling the compiler

```tsx
// BAD: removing memo that stabilized an effect dependency changes behavior
const config = { endpoint, token }; // recreated each render → effect re-fires
useEffect(() => subscribe(config), [config]);
```

```tsx
// GOOD: keep the deliberate escape hatch the preserve-manual-memoization lint protects
const config = useMemo(() => ({ endpoint, token }), [endpoint, token]);
useEffect(() => subscribe(config), [config]);
```

### ❌ Don't: Put high-frequency state in one large context

```tsx
// BAD: every consumer re-renders when any field changes; memo cannot block it
const AppContext = createContext<{ theme: Theme; cursor: Point } | null>(null);
```

```tsx
// GOOD: split by change frequency so fast-changing state is isolated
const ThemeContext = createContext<Theme | null>(null);   // changes rarely
const CursorContext = createContext<Point | null>(null);  // changes often
```

### ❌ Don't: Update state after `await` inside an async transition

```tsx
// BAD: the post-await update escapes the transition; isPending ends early
startTransition(async () => {
  const data = await load();
  setData(data); // not part of the transition
});
```

```tsx
// GOOD: re-wrap the post-await update
startTransition(async () => {
  const data = await load();
  startTransition(() => setData(data));
});
```

### ❌ Don't: Keep `forwardRef` / `<Context.Provider>` / `react-helmet` in new React 19 code

```tsx
// BAD: superseded idioms in new code
const Input = forwardRef<HTMLInputElement, Props>((props, ref) => <input ref={ref} {...props} />);
<ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>;
```

```tsx
// GOOD: ref as a plain prop, <Context> as provider, native metadata
function Input({ ref, ...props }: Props & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
<ThemeContext value={theme}>{children}</ThemeContext>;
```

The `& { ref?: ... }` intersection is only needed when `Props` is a custom interface that must expose `ref`. For wrappers over an intrinsic element, deriving `Props` from `React.ComponentProps<'input'>` already includes a correctly-typed `ref`, so the intersection is redundant.

## When to Reach for Sibling Skills

- **react-core**: fundamentals — components, JSX, props/state, core hooks, lists, controlled inputs.
- **react-hooks-composition**: custom-hook composition recipes — SWR data hooks, debounced search, memoized providers, async-state hooks.
- **react-state-machine**: explicit XState v5 finite-state machines for complex flows where impossible states must be unrepresentable.
- **tanstack-query** / **zustand**: server-state caching and global client state, respectively.
- **Next.js skills**: framework wiring of Server Components, Server Actions, routing, and caching.

## Best Practices Summary

1. **Compiler first**: enable `eslint-plugin-react-hooks` v6+, fix Rules of React, then turn on the React Compiler.
2. **Stop reflexive memoization**: reach for `useMemo`/`useCallback`/`React.memo` only as a deliberate escape hatch (effect-dependency stability, or unanalyzable code).
3. **Stay responsive with concurrency**: prefer `useTransition`/`useDeferredValue` over manual debounce for expensive renders; re-wrap post-`await` updates.
4. **Use Actions for mutations**: `useActionState` + `useOptimistic` + `useFormStatus` cover pending, error, and optimistic states at the React level.
5. **Read `use()` correctly**: call it conditionally, never in `try/catch`, and create promises high in the tree.
6. **Adopt React 19 ergonomics**: `ref` as a prop, `<Context value>`, native metadata — drop `forwardRef` and `react-helmet`.
7. **Fix context over-rendering structurally**: memoize the value and split contexts; the compiler does not solve this.
8. **Engineer list and bundle performance**: virtualize large lists, code-split by route, and profile against production builds.
9. **Respect the RSC boundary**: it is module-graph-based; keep crossing props serializable, validate server-function inputs, and pin the React version.

## Navigation

- **[React Compiler](references/react-compiler.md)**: adoption per bundler, ESLint/Rules of React, what the compiler skips, `preserve-manual-memoization`, before/after examples.
- **[Concurrent Rendering](references/concurrent-rendering.md)**: `useTransition` (sync/async + post-await gotcha), `useDeferredValue`, Suspense-for-data, streaming SSR shells, reveal batching, boundary `key` resets.
- **[React 19 Actions & APIs](references/react19-actions-and-apis.md)**: `use()`, `useActionState`, `useOptimistic`, `useFormStatus`, `<form action>`, ref-as-prop, `useImperativeHandle`, `<Context value>`, metadata/preloading, with migration notes.
- **[Component Patterns](references/component-patterns.md)**: compound components, context selectors/splitting + `use-context-selector`, render-props-vs-hooks, error boundaries, portals.
- **[Performance](references/performance.md)**: virtualization library comparison, code-splitting strategy, Profiler workflow, anti-pattern → detection → fix catalog.
- **[RSC Boundary](references/rsc-boundary.md)**: conceptual `'use client'`/`'use server'` model, serialization rules, server-function security, Next.js hand-off, version pinning.

## References

- [React Documentation](https://react.dev/) — authoritative source for all APIs in this skill
- [React Compiler 1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
- [React 19 release](https://react.dev/blog/2024/12/05/react-19)
- [React 19.2](https://react.dev/blog/2025/10/01/react-19-2)
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
