# Advanced Component Patterns

> Source of truth: [useContext](https://react.dev/reference/react/useContext), [createPortal](https://react.dev/reference/react-dom/createPortal), and [Component (error boundaries)](https://react.dev/reference/react/Component). This reference applies that guidance and notes the userland gaps it does not cover.

## Compound Components

Compound components let a parent and its sub-components coordinate through implicit shared state, so the consumer composes the pieces declaratively without wiring props between them. The shared state travels through context.

```tsx
const TabsContext = createContext<{
  active: string;
  setActive: (id: string) => void;
} | null>(null);

function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [active, setActive] = useState(defaultTab);
  return <TabsContext value={{ active, setActive }}>{children}</TabsContext>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useTabs();
  return (
    <button aria-selected={ctx.active === id} onClick={() => ctx.setActive(id)}>
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useTabs();
  return ctx.active === id ? <div role="tabpanel">{children}</div> : null;
}

function useTabs() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs.* must render inside <Tabs>');
  return ctx;
}

// Usage: the parent owns state; sub-components read it implicitly.
<Tabs defaultTab="a">
  <Tab id="a">First</Tab>
  <Tab id="b">Second</Tab>
  <TabPanel id="a">First panel</TabPanel>
  <TabPanel id="b">Second panel</TabPanel>
</Tabs>;
```

## Context Optimization

Native context has **no selector**. When a provider value changes, **every** consumer of that context re-renders, regardless of which slice each consumer reads. Three facts shape every fix:

- `React.memo` does **not** block context-driven re-renders. A memoized consumer still re-renders when its context value changes.
- `use(Context)` adds *conditional reading* but **not** *selective subscription* — a consumer still subscribes to the whole value.
- The React Compiler does **not** solve large-context over-rendering. This is an architectural problem, not a memoization one.

### Native fix 1 — memoize the provider value

A provider value object created inline is a new reference every render, re-rendering all consumers even when nothing changed. Memoize it. (The full memoized-provider recipe lives in **react-hooks-composition**; the point here is that it is necessary but not sufficient.)

```tsx
const value = useMemo(() => ({ user, signOut }), [user, signOut]);
return <AuthContext value={value}>{children}</AuthContext>;
```

### Native fix 2 — split contexts by change frequency

Separate slow-changing state from fast-changing state so a frequent update does not re-render consumers that only care about stable data.

```tsx
// BAD: theme (rare) and pointer (frequent) share one context.
const UIContext = createContext<{ theme: Theme; pointer: Point } | null>(null);
```

```tsx
// GOOD: independent contexts; pointer churn never re-renders theme consumers.
const ThemeContext = createContext<Theme | null>(null);
const PointerContext = createContext<Point | null>(null);
```

### Userland fix — `use-context-selector`

When a single context must hold many slices and consumers need to subscribe to *one* slice, the userland `use-context-selector` library provides selective subscription that native context lacks.

```tsx
import { createContext, useContextSelector } from 'use-context-selector';

const StoreContext = createContext<Store | null>(null);

// Re-renders only when `store.count` changes, not on every store update.
const count = useContextSelector(StoreContext, (s) => s!.count);
```

Caveats: it predates the React 19 idioms (uses its own provider), and selective subscription interacts with concurrent rendering's tearing guarantees — evaluate against a dedicated state library (zustand for global client state) when slice subscription becomes the dominant need.

## Render Props vs Custom Hooks

For reusing **logic**, custom hooks win: they compose, avoid the "wrapper hell" of nested render-prop components, and read linearly. Render props remain useful for **headless** components that own behavior but delegate *what to render* to the consumer.

```tsx
// Logic reuse → hook
function useHover() {
  const [hovered, setHovered] = useState(false);
  const bind = { onMouseEnter: () => setHovered(true), onMouseLeave: () => setHovered(false) };
  return [hovered, bind] as const;
}
```

```tsx
// Headless "what to render" → render prop
function Toggle({ children }: { children: (on: boolean, toggle: () => void) => React.ReactNode }) {
  const [on, setOn] = useState(false);
  return <>{children(on, () => setOn((v) => !v))}</>;
}
```

## Error Boundaries

Error boundaries are still **class-based** — there is no function-component equivalent. They catch errors thrown during render, in lifecycle methods, and in constructors of the tree below them. They do **not** catch errors in event handlers, async code, or the boundary's own render.

```tsx
class ErrorBoundary extends React.Component<
  { fallback: React.ReactNode; children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: Error, info: React.ErrorInfo) { report(error, info); }
  render() { return this.state.hasError ? this.props.fallback : this.props.children; }
}
```

For async and event-handler errors, `react-error-boundary` adds `useErrorBoundary().showBoundary(error)` to forward a caught error into the nearest boundary. React 19 logs caught errors once (no duplicate console noise) and adds root-level `onCaughtError`/`onUncaughtError` callbacks for centralized reporting.

```tsx
import { useErrorBoundary } from 'react-error-boundary';

function Saver() {
  const { showBoundary } = useErrorBoundary();
  async function save() {
    try { await api.save(); }
    catch (err) { showBoundary(err); } // routes an async error to the boundary
  }
  return <button onClick={save}>Save</button>;
}
```

## Portals

`createPortal` renders children into a **different DOM node** while keeping them in the same place in the **React tree**. Context still flows, events still bubble through the React hierarchy, and errors still propagate to React-tree ancestors — only the DOM placement changes. This makes portals the right tool for modals, tooltips, and toasts that must escape an overflow/z-index container.

```tsx
function Modal({ children }: { children: React.ReactNode }) {
  // Rendered into document.body, but still a React child of whatever rendered <Modal>.
  return createPortal(
    <div className="modal-overlay">{children}</div>,
    document.body,
  );
}
```

## Anti-Patterns

| Anti-pattern | Why it is wrong | Detection |
|---|---|---|
| One large context for high-frequency state | Every consumer re-renders on any change; `memo` cannot block it | Profiler shows unrelated consumers re-rendering |
| Expecting `React.memo` to stop context re-renders | Context bypasses prop comparison | Memoized child still re-renders on context change |
| Function-component "error boundary" | No FC equivalent exists | Render errors uncaught; only class/`react-error-boundary` works |
| Expecting native boundaries to catch async/event errors | They catch only render-phase errors | Event-handler throws crash the app |
| Reaching for a portal to fix layout flow | Portals change DOM placement, not React tree semantics | Context/event expectations broken by misuse |

## Sources

- https://react.dev/reference/react/useContext
- https://react.dev/reference/react-dom/createPortal
- https://react.dev/reference/react/Component
- https://www.npmjs.com/package/use-context-selector
- https://github.com/dai-shi/use-context-selector
- https://newsletter.daishikato.com/p/the-past-and-future-of-render-optimization-with-react-context
- https://blog.logrocket.com/react-error-handling-react-error-boundary/
