# `react-advanced` Skill — Scoping Report

**Date:** 2026-06-15
**Status:** Research + scoping only (no skill files written)
**Recommended path:** `toolchains/javascript/frameworks/react/react-advanced/`

---

## 0. Executive Summary

The existing focused React siblings (`react-core`, `react-hooks-composition`, `react-state-machine`, `flexlayout-react`) collectively cover fundamentals, advanced custom-hook *composition*, XState finite-state machines, and a niche docking-layout library. **None of them cover modern React 19 platform features or rendering-performance architecture.** There is a clear, non-overlapping gap.

`react-advanced` fills the gap of **React-19-era platform capabilities and rendering architecture**: the React Compiler (and how it overturns the old manual-memoization advice), concurrent rendering (`useTransition` / `useDeferredValue` / Suspense for data), the `use()` hook, Actions/form hooks (`useActionState` / `useOptimistic` / `useFormStatus`), React-19 ref-as-prop and `<Context>`-as-provider changes, advanced component patterns (compound components, context selectors/splitting, error boundaries, portals), virtualization/code-splitting performance, and a conceptual treatment of the RSC / `'use client'` boundary. It explicitly defers data-fetching frameworks (Next.js) and external state libraries (Zustand, TanStack Query, XState) to their owning skills.

**Top 3 current-practice points that shape the skill:**
1. **The React Compiler (1.0 stable, Oct 2025) inverts the old memoization guidance.** Manually scattering `useMemo`/`useCallback`/`React.memo` is now largely an anti-pattern for new code; the compiler memoizes automatically (including conditionally, which manual memo cannot). Manual memo survives only as a deliberate escape hatch (e.g., stabilizing an *effect dependency*).
2. **React 19 changed core ergonomics:** `ref` is a plain prop (`forwardRef` deprecated), `<Context value>` replaces `<Context.Provider>`, document metadata hoists natively (no `react-helmet`), and the `use()` hook reads promises/context *conditionally* — breaking the old Rules-of-Hooks intuition.
3. **Actions are the new async-mutation primitive:** `useActionState` + `useOptimistic` + `useFormStatus` + `<form action={fn}>` provide built-in pending/error/optimistic handling at the React level (independent of any framework).

---

## 1. Coverage Map — What Each Sibling Owns

| Sibling skill | Path | OWNS (explicitly excluded from `react-advanced`) |
|---|---|---|
| **react-core** | `toolchains/javascript/frameworks/react/react-core/` | Fundamentals: components & JSX, props/state, the *core* hooks (`useState`/`useEffect`/`useRef`/`useMemo`/`useCallback`/`useContext`), composition via `children`, conditional/list rendering, controlled inputs, Rules of Hooks. The canonical "depends on React" baseline. |
| **react-hooks-composition** | `toolchains/javascript/frameworks/react/react-hooks-composition/` | Advanced **custom-hook composition**: SWR-backed data hooks with conditional (null) keys, debounced search with dual loading states, memoized **context provider** value pattern (`useMemo`/`useCallback` on the value), discriminated-union "poor-man's state machine" in hooks, pure helper functions for testability. |
| **react-state-machine** | `toolchains/javascript/frameworks/react/react-state-machine/` | **XState v5** finite-state machines & actor model: `setup()`, promise actors, guards/actions, `useMachine` vs `useActorRef`+`useSelector`, parallel/hierarchical states, persistence/hydration, visualization. The home for *explicit FSM* modeling. |
| **flexlayout-react** | `toolchains/javascript/frameworks/flexlayout-react/` | Niche: FlexLayout docking layout manager (drag-drop panels, tabs, splitters, layout persistence). IDE/dashboard layout UI only. |
| **tanstack-query** *(related)* | `toolchains/typescript/state/tanstack-query/` | Server-state caching: queries/mutations, cache invalidation, optimistic updates *via React Query*, pagination/infinite scroll, SSR hydration of query cache. |
| **zustand** *(related)* | `toolchains/typescript/state/zustand/` | Global client state via Zustand store (hook-based, no providers), SSR hydration of store. |
| **nextjs-core / nextjs-v16 / nextjs (frameworks)** *(related)* | `toolchains/nextjs/*`, `toolchains/javascript/frameworks/nextjs/` | **Framework-specific** Server Components wiring, Server Actions with `revalidateTag`/`revalidatePath`, route handlers, App Router data-fetching/caching, `"use cache"`, Turbopack, async request APIs. |

### The Gap `react-advanced` Fills

Everything **React-19-platform** and **rendering-architecture** that none of the above owns:

- The **React Compiler** and the consequent re-write of memoization guidance.
- **Concurrent rendering primitives** (`useTransition` incl. async transitions, `useDeferredValue`, `startTransition`, Suspense for data via thrown promises, streaming-SSR boundaries at the React level).
- **React 19 platform hooks/APIs**: `use()`, `useActionState`, `useOptimistic`, `useFormStatus`, `<form action>`, ref-as-prop / `useImperativeHandle`, `<Context>`-as-provider, native document metadata & resource preloading.
- **Advanced component-architecture patterns**: compound components, context selectors / context splitting (and the userland `use-context-selector` gap), render-props-vs-hooks today, error boundaries (`react-error-boundary`), portals (`createPortal`).
- **Performance architecture**: virtualization (TanStack Virtual / react-window / Virtuoso), `React.lazy`+Suspense code-splitting strategy, DevTools Profiler workflow, and a consolidated anti-patterns + detection catalog.
- **Conceptual RSC / `'use client'` boundary** (the React feature, deferring framework wiring to Next.js skills).

**Boundary discipline (what is OUT, deferred to siblings):**
- ❌ Core hooks tutorial → `react-core`
- ❌ SWR/debounce/memoized-provider custom-hook recipes → `react-hooks-composition`
- ❌ XState machines → `react-state-machine`
- ❌ React Query caching / optimistic-via-RQ → `tanstack-query`
- ❌ Zustand global store → `zustand`
- ❌ Next.js Server Action wiring, caching, routing, App Router data fetching → Next.js skills
- ❌ Docking layout UI → `flexlayout-react`

---

## 2. Proposed Skill Outline

### SKILL.md structure

**Entry point**
- **summary:** "Modern React 19 platform features and rendering architecture: the React Compiler (auto-memoization), concurrent rendering (useTransition/useDeferredValue/Suspense), the use() hook, Actions (useActionState/useOptimistic/useFormStatus), ref-as-prop, advanced component patterns, virtualization & code-splitting performance."
- **when_to_use:** "Adopting the React Compiler; using concurrent features for responsiveness; building with React 19 Actions/forms or the use() hook; optimizing render performance (context over-rendering, large lists, code-splitting); architecting compound components, context selectors, error boundaries, or portals; reasoning about the RSC/'use client' boundary at the React level."
- **quick_start:** "1. Enable eslint-plugin-react-hooks (v6+) and fix Rules of React, then turn on the React Compiler. 2. Stop hand-memoizing; reach for useMemo/useCallback only as a deliberate escape hatch. 3. Use useTransition/useDeferredValue to keep the UI responsive. 4. Use Actions (useActionState/useOptimistic) for async mutations."

**Core sections (in SKILL.md body)**

1. **Overview & boundary statement** — what this skill is, and an explicit "use sibling X for Y" map (core hooks → react-core; custom-hook recipes → react-hooks-composition; FSM → react-state-machine; server-state caching → tanstack-query; framework wiring → Next.js skills).

2. **The React Compiler — and the death of manual memoization** *(headline section)*
   - Status: Compiler 1.0 stable (Oct 2025); works with React 17/18/19, best on 19.
   - What it does: build-time granular auto-memoization, including *conditional* memoization manual memo can't express.
   - **CHANGE vs 17/18:** old "wrap everything in `useMemo`/`useCallback`/`React.memo`" advice is now obsolete for new code; over-memoization is an anti-pattern.
   - When manual memo still matters: memoized value used as an **effect dependency**; code the compiler can't analyze (it safely skips).
   - Existing code: compiler preserves your manual memo (`preserve-manual-memoization` lint); don't rip it out blindly.
   - Adoption path: ESLint plugin first → fix Rules of React → enable compiler (Babel/Vite/Metro/Rsbuild). "Memo ✨" badge in DevTools.

3. **Concurrent rendering**
   - `useTransition` (`isPending`, interruptible); React-19 **async** transitions and the post-`await` gotcha (re-wrap in `startTransition`).
   - `startTransition` standalone vs `useDeferredValue` (prefer deferred value over fixed debounce/throttle; `initialValue` in React 19).
   - Suspense for data fetching (promises thrown / read via `use()`); fallback timing rules; `key` to reset boundaries.
   - Streaming SSR at the React level (`renderToPipeableStream` for Node; shell design; `onShellReady`/`onShellError`); note Suspense reveal batching (19.2) — but defer framework specifics to Next.js.

4. **React 19 platform hooks & APIs**
   - `use()` — read promises/context conditionally (after early returns); not in try/catch; prefer creating promises server-side / passing down.
   - **Actions:** `useActionState` (pending/error/sequential; renamed from `useFormState`), `useOptimistic`, `useFormStatus`, `<form action={fn}>` (auto-reset, `requestFormReset`, multiple `formAction`s).
   - **Ergonomic changes:** `ref` as a prop (`forwardRef` deprecated; codemod), `useImperativeHandle` receiving the ref prop, `<Context value>` replacing `<Context.Provider>`.
   - Native document metadata (`<title>`/`<meta>`/`<link>` hoisting; replaces `react-helmet`) and resource preloading (`preload`/`preinit`/`preconnect`) — brief.

5. **Advanced component patterns**
   - Compound components (Context-backed implicit state sharing).
   - **Context optimization:** memoize provider value + split contexts; native context has **no selector** and `memo` doesn't block context re-renders; `use(Context)` adds conditional read but **not** selective subscription; userland `use-context-selector` fills the gap (+ caveats). Compiler does **not** fix large-context re-rendering.
   - Render props vs custom hooks today (hooks win for logic reuse; render props for headless "what to render").
   - Error boundaries (still class-based; `react-error-boundary` + `useErrorBoundary` for async/event errors; React 19 single-log + `onCaughtError`/`onUncaughtError`).
   - Portals (`createPortal`): DOM placement only — context/errors still flow through the React tree.

6. **Performance architecture**
   - Virtualization: TanStack Virtual (modern/headless) vs react-window (mature, stalled) vs react-virtuoso (batteries-included); post-virtualization bottleneck = item-renderer cost → keep rows light.
   - Code-splitting: `React.lazy`+Suspense, split by route first, don't over-split tiny components.
   - Profiling workflow: React DevTools Profiler (production build), "what changed", Why-Did-You-Render.
   - **Anti-pattern + detection catalog** (see §4).

7. **RSC / `'use client'` boundary (conceptual)**
   - Server Components are the default, render ahead, can't use `useState`; boundary is on the **module dependency tree**, not the render tree; props crossing must be serializable; Client Components can render Server Components passed as children.
   - `'use server'` marks Server *Functions* (untrusted args — validate/authorize).
   - **Explicit defer:** caching, route loaders, App Router data fetching → Next.js skills. Pin React version (RSC bundler APIs aren't semver-stable in 19.x).

8. **Anti-Patterns to Avoid** (consolidated — see §4)

9. **Best Practices Summary** (numbered, mirrors sibling style)

10. **Navigation to references** + **References** (URLs)

### Proposed `references/*.md` deep-dives

| File | Contents |
|---|---|
| `react-compiler.md` | Full adoption guide: install per bundler, ESLint integration, Rules of React, what breaks/skips, `preserve-manual-memoization`, when to keep/remove manual memo, DevTools badge, before/after examples. |
| `concurrent-rendering.md` | `useTransition` (sync + async + post-await gotcha), `useDeferredValue`, Suspense-for-data deep patterns, streaming SSR shell design, reveal batching, boundary `key` resets. |
| `react19-actions-and-apis.md` | `use()`, `useActionState`, `useOptimistic`, `useFormStatus`, `<form action>`, ref-as-prop / `useImperativeHandle`, `<Context value>`, metadata/preloading — with complete code examples and migration notes from 17/18. |
| `component-patterns.md` | Compound components, context selectors/splitting + `use-context-selector` caveats, render-props-vs-hooks decision, error boundaries (`react-error-boundary`), portals. |
| `performance.md` | Virtualization library comparison & usage, code-splitting strategy, Profiler workflow, full anti-pattern→detection→fix table. |
| `rsc-boundary.md` | Conceptual RSC/`'use client'`/`'use server'` model, serialization rules, server-function security, the explicit Next.js hand-off, version-pinning note. |

> Keep `references/` count at ~6 to match the breadth of `react-state-machine` (11 refs) without over-fragmenting; merge `rsc-boundary.md` into `concurrent-rendering.md` if token budget is tight, since both touch streaming/Suspense.

---

## 3. Key Current-Practice Notes (must shape the guidance)

Each item below changes pre-React-19 advice and must be presented as *current*, with the stale advice flagged.

1. **React Compiler 1.0 (stable Oct 7 2025)** — auto-memoization makes manual `useMemo`/`useCallback`/`React.memo` largely unnecessary; over-memoization is now an anti-pattern. Escape hatch: stabilizing **effect dependencies**, or code the compiler can't analyze. Enable via ESLint (`eslint-plugin-react-hooks` v6+, which absorbed `eslint-plugin-react-compiler`) → fix Rules of React → turn on compiler. Sources: https://react.dev/blog/2025/10/07/react-compiler-1 · https://react.dev/learn/react-compiler/introduction · https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization

2. **React 19 core ergonomic changes** (Dec 5 2024): `ref` is a normal prop, `forwardRef` deprecated (codemod available); `<Context value>` replaces `<Context.Provider>` (now legacy); document metadata hoists natively (drop `react-helmet`). Sources: https://react.dev/blog/2024/12/05/react-19 · https://react.dev/reference/react/forwardRef · https://react.dev/reference/react/createContext

3. **The `use()` hook** reads promises and context **conditionally** (callable after early returns) — a deliberate exception to Rules of Hooks; cannot live in try/catch (use Error Boundaries); prefer creating promises in Server Components and passing down. Source: https://react.dev/reference/react/use

4. **Actions are the async-mutation primitive:** `useActionState` (renamed from canary `useFormState`), `useOptimistic`, `useFormStatus`, `<form action={fn}>` — built-in pending/error/optimistic handling at the React level. Sources: https://react.dev/reference/react/useActionState · https://react.dev/reference/react/useOptimistic · https://react.dev/reference/react-dom/hooks/useFormStatus · https://react.dev/reference/react-dom/components/form

5. **Async transitions gotcha (React 19):** `startTransition` accepts async functions, but state updates *after* an `await` aren't part of the transition unless re-wrapped in `startTransition`. Prefer `useDeferredValue` (with new `initialValue`) over fixed debounce/throttle for derived values. Sources: https://react.dev/reference/react/useTransition · https://react.dev/reference/react/useDeferredValue

6. **Context still has no native selector** — `memo` does not block context-driven re-renders, and `use(Context)` adds conditional reading but **not** selective subscription. The compiler does **not** fix large-context over-rendering. Native fixes: memoize value + split contexts; userland `use-context-selector` for slice subscriptions (with tearing/class caveats). Sources: https://react.dev/reference/react/useContext · https://www.npmjs.com/package/use-context-selector · https://newsletter.daishikato.com/p/the-past-and-future-of-render-optimization-with-react-context

7. **Streaming SSR (React level):** `renderToPipeableStream` recommended for Node; design a meaningful shell, not one root spinner; React 19.2 (Oct 1 2025) batches Suspense reveals (with an LCP-protecting heuristic) and adds Web-Streams SSR + `resume` in Node. Sources: https://react.dev/reference/react-dom/server/renderToPipeableStream · https://react.dev/blog/2025/10/01/react-19-2

8. **RSC boundary is module-graph based, not render-tree based;** `'use server'` marks Server *Functions* (validate untrusted args); pin React version since RSC bundler APIs aren't semver-stable in 19.x; framework data-fetching belongs to Next.js skills. Sources: https://react.dev/reference/rsc/use-client · https://react.dev/reference/rsc/server-components · https://react.dev/reference/rsc/use-server

9. **Virtualization (2026):** `@tanstack/react-virtual` (modern, headless, best TS) vs `react-window` (mature but stalled) vs `react-virtuoso` (batteries-included); after virtualizing, item-renderer cost becomes the bottleneck. Source: https://www.pkgpulse.com/guides/tanstack-virtual-vs-react-window-vs-react-virtuoso-2026

---

## 4. Anti-Patterns the Skill Should Call Out

| Anti-pattern | Why it's wrong (2026) | How to detect |
|---|---|---|
| **Hand-memoizing everything** (`useMemo`/`useCallback`/`React.memo` by reflex) | With the Compiler on, it's redundant and adds noise/cost; over-memoization can be net-negative even without the compiler. | Compiler enabled but code still littered with manual memo; profile shows no benefit. |
| **Removing manual memo blindly after enabling the compiler** | Compiler *preserves* manual memo intentionally; some was load-bearing (effect deps). | `preserve-manual-memoization` lint warnings; effects firing unexpectedly. |
| **Using context for high-frequency / large shared state without splitting or selectors** | Any provider-value change re-renders **all** consumers; `memo` doesn't help; compiler doesn't fix it. | DevTools Profiler highlights unrelated consumers re-rendering. |
| **Treating `use()` like a normal hook everywhere / inside try-catch** | It's an intentional Rules-of-Hooks exception; try/catch doesn't catch its suspension — needs Error Boundary. | Runtime errors swallowed; promises recreated each render (client-created). |
| **State updates after `await` inside an async transition** | They fall outside the transition; `isPending` ends early. | UI flips to non-pending mid-operation. |
| **Debounce/throttle by hand for expensive derived renders** | `useDeferredValue` is interruptible & device-adaptive — better UX. | Janky typing on slow devices; fixed timers in code. |
| **Large lists rendered without virtualization** | Thousands of DOM nodes tank render/scroll. | High node count in Profiler; long commit times. |
| **Over-splitting with `React.lazy`** | Tiny chunks add request overhead without payoff. | Many <10KB lazy chunks; waterfall of small requests. |
| **Fetch waterfalls** (sequential awaits / fetching in `useEffect` on the client) | Serial latency; client round-trips. | Sequential network spans; data hooks chained. |
| **Still using `forwardRef` / `<Context.Provider>` / `react-helmet` in new React 19 code** | Superseded: ref-as-prop, `<Context value>`, native metadata. | Deprecation lint; legacy idioms in new files. |
| **Function-component "error boundary" expectation** | No FC equivalent yet; must be class or `react-error-boundary`. | Errors in event handlers/async not caught by native boundary. |

---

## 5. Proposed Frontmatter

Consistent with sibling field set (`react-core`, `react-hooks-composition`, `react-state-machine`): `user-invocable: false`, `disable-model-invocation: true`, `category: toolchain`, `progressive_disclosure.entry_point` with `summary`/`when_to_use`/`quick_start`, a `references` list, `context_limit: 700`, `tags`, `requires_tools: []`.

```yaml
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
```

**Companion `metadata.json` fields** (mirror siblings): `name`, `version`, `category: toolchain`, `toolchain: javascript`, `framework: react`, `tags`, `entry_point_tokens`, `full_tokens`, `author`, `license`, `requires: []`, `related_skills: ["react-core", "react-hooks-composition", "react-state-machine"]`, `has_references: true`, `reference_files: [...]`, `updated`/`created`/`modified`, `source_path`, repository/maintainer/attribution fields.

---

## 6. Recommended Path

```
toolchains/javascript/frameworks/react/react-advanced/
├── SKILL.md
├── metadata.json
└── references/
    ├── react-compiler.md
    ├── concurrent-rendering.md
    ├── react19-actions-and-apis.md
    ├── component-patterns.md
    ├── performance.md
    └── rsc-boundary.md
```

This sits alongside `react-core`, `react-hooks-composition`, and `react-state-machine` under the existing `react/` family directory, consistent with the established hierarchy.

---

## Sources

- https://react.dev/blog/2025/10/07/react-compiler-1
- https://react.dev/learn/react-compiler/introduction
- https://react.dev/learn/react-compiler/installation
- https://react.dev/reference/eslint-plugin-react-hooks
- https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization
- https://react.dev/blog/2024/12/05/react-19
- https://react.dev/blog/2024/04/25/react-19-upgrade-guide
- https://react.dev/blog/2025/10/01/react-19-2
- https://react.dev/reference/react/use
- https://react.dev/reference/react/useActionState
- https://react.dev/reference/react/useOptimistic
- https://react.dev/reference/react-dom/hooks/useFormStatus
- https://react.dev/reference/react-dom/components/form
- https://react.dev/reference/react/forwardRef
- https://react.dev/reference/react/useImperativeHandle
- https://react.dev/reference/react/createContext
- https://react.dev/reference/react/useContext
- https://react.dev/reference/react-dom/components/meta
- https://react.dev/reference/react/useTransition
- https://react.dev/reference/react/startTransition
- https://react.dev/reference/react/useDeferredValue
- https://react.dev/reference/react/Suspense
- https://react.dev/reference/react-dom/server/renderToPipeableStream
- https://react.dev/reference/react-dom/server/renderToReadableStream
- https://react.dev/reference/react/Component
- https://react.dev/reference/react-dom/createPortal
- https://react.dev/reference/rsc/server-components
- https://react.dev/reference/rsc/use-client
- https://react.dev/reference/rsc/use-server
- https://react.dev/learn/reusing-logic-with-custom-hooks
- https://www.pkgpulse.com/guides/tanstack-virtual-vs-react-window-vs-react-virtuoso-2026
- https://stevekinney.com/courses/react-performance/code-splitting-and-lazy-loading
- https://www.growin.com/blog/react-performance-optimization-2025/
- https://blog.openreplay.com/scan-react-code-anti-patterns-react-doctor/
- https://www.npmjs.com/package/use-context-selector
- https://github.com/dai-shi/use-context-selector
- https://newsletter.daishikato.com/p/the-past-and-future-of-render-optimization-with-react-context
- https://blog.logrocket.com/react-error-handling-react-error-boundary/
