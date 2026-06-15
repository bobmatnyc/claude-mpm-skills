# Performance Architecture

> Source of truth for the React APIs: [lazy](https://react.dev/reference/react/lazy) and [Suspense](https://react.dev/reference/react/Suspense). Library comparisons reflect the 2026 landscape; verify versions against each library's current docs.

Rendering-performance work splits into three concerns: rendering fewer DOM nodes (virtualization), shipping less JavaScript up front (code-splitting), and measuring before optimizing (profiling). With the React Compiler handling memoization, performance effort shifts away from hand-tuned `useMemo` toward these architectural levers.

## Virtualization

A list of thousands of rows mounts thousands of DOM nodes, which tanks initial render and scroll performance. Virtualization renders only the rows in (and near) the viewport, recycling them as the user scrolls.

### Library comparison (2026)

| Library | Character | Use when |
|---|---|---|
| `@tanstack/react-virtual` | Modern, headless, strongest TypeScript; full control over markup | New code, custom row layouts, TS-first projects |
| `react-window` | Mature, small, but largely stalled | Simple fixed/variable lists where a settled API matters |
| `react-virtuoso` | Batteries-included (auto-sizing, grouping, sticky headers) | Rich list features without building them by hand |

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function BigList({ rows }: { rows: Row[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 40,
    overscan: 8,
  });

  return (
    <div ref={parentRef} style={{ height: 600, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map((vi) => (
          <div
            key={vi.key}
            style={{ position: 'absolute', top: 0, transform: `translateY(${vi.start}px)`, width: '100%' }}
          >
            <RowView row={rows[vi.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

**After virtualizing, the bottleneck moves to the per-item renderer.** Once only ~20 rows render at a time, an expensive `RowView` dominates. Keep row components light: avoid heavy per-row computation, deep trees, and large inline objects.

## Code-Splitting

`React.lazy` + `Suspense` defers loading a component's code until it renders, shrinking the initial bundle.

```tsx
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<RouteSkeleton />}>
      <Settings />
    </Suspense>
  );
}
```

### Strategy

- **Split by route first.** Route boundaries are the highest-value split points: a user loads only the route they visit.
- **Do not over-split.** Lazy-loading many tiny (<10KB) components creates a waterfall of small requests whose overhead outweighs the savings. Reserve `lazy` for genuinely heavy or rarely visited subtrees (editors, charts, admin panels).
- **Place the fallback to match layout** so the lazy boundary does not cause a layout shift on load.

## Profiling Workflow

Measure before optimizing. The React DevTools Profiler records commits and shows which components re-rendered and why.

1. **Profile a production build.** Development builds carry extra work and mislead timing. Use a production (or profiling) build for representative numbers.
2. **Record an interaction**, then read the flamegraph: wide bars are expensive commits; the "why did this render" panel attributes the cause (props, state, hooks, parent).
3. **Confirm the React Compiler is active** — components show a "Memo ✨" badge. Their absence on a hot path explains avoidable re-renders.
4. **Use Why-Did-You-Render** in development to log re-renders caused by unstable props when chasing a specific regression.

## Anti-Pattern → Detection → Fix Catalog

| Anti-pattern | Why it is wrong (2026) | How to detect | Fix |
|---|---|---|---|
| Hand-memoizing everything | Redundant with the compiler; adds noise/cost | Compiler on, code littered with manual memo | Remove; reserve memo for escape hatches |
| Removing manual memo blindly after enabling the compiler | Compiler preserves load-bearing memo (effect deps) | `preserve-manual-memoization` warnings; effects re-firing | Restore the meaningful memo |
| Large/high-frequency context without split or selector | Every consumer re-renders; `memo` cannot block it | Profiler highlights unrelated consumers | Split contexts / `use-context-selector` |
| `use()` treated as a normal hook, or inside `try/catch` | Intentional Rules-of-Hooks exception; `catch` misses suspension | Errors swallowed; promises recreated each render | Error Boundary; create promise high in the tree |
| State update after `await` in an async transition | Falls outside the transition; `isPending` ends early | UI flips to non-pending mid-operation | Re-wrap in `startTransition` |
| Manual debounce/throttle for expensive derived renders | `useDeferredValue` is interruptible and adaptive | Janky typing on slow devices; fixed timers | Use `useDeferredValue` |
| Large lists without virtualization | Thousands of DOM nodes; long commits | High node count; long commit times in Profiler | Virtualize |
| Over-splitting with `React.lazy` | Request overhead without payoff | Many <10KB lazy chunks; request waterfall | Split by route; coarser chunks |
| Fetch waterfalls (sequential `await`, fetch-in-`useEffect`) | Serial latency; client round-trips | Sequential network spans; chained data hooks | Parallelize; hoist data fetching |
| Legacy `forwardRef` / `<Context.Provider>` / `react-helmet` in new code | Superseded by React 19 idioms | Deprecation lint; legacy idioms in new files | Ref-as-prop, `<Context value>`, native metadata |

## Sources

- https://react.dev/reference/react/lazy
- https://react.dev/reference/react/Suspense
- https://www.pkgpulse.com/guides/tanstack-virtual-vs-react-window-vs-react-virtuoso-2026
- https://stevekinney.com/courses/react-performance/code-splitting-and-lazy-loading
- https://www.growin.com/blog/react-performance-optimization-2025/
- https://blog.openreplay.com/scan-react-code-anti-patterns-react-doctor/
