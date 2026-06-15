# React Compiler — Adoption & Memoization Guidance

> Source of truth: [React Compiler docs](https://react.dev/learn/react-compiler/introduction) and the [1.0 announcement](https://react.dev/blog/2025/10/07/react-compiler-1). This reference applies that guidance; consult react.dev for the canonical API.

## What the Compiler Is

The React Compiler is a build-time optimizing compiler that rewrites components and hooks to memoize automatically. It reached **1.0 stable on 2025-10-07**. It analyzes which values a component computes, which of those depend on which inputs, and emits memoization at fine granularity — including **conditional** memoization that a hand-written `useMemo` cannot express, because a manual `useMemo` runs unconditionally with a fixed dependency array.

It supports React 17, 18, and 19, and produces the best results on 19. On 17/18 it relies on a runtime helper (`react-compiler-runtime`).

## The Memoization Inversion

Pre-compiler React guidance optimized for reference stability by hand: wrap derived values in `useMemo`, wrap callbacks in `useCallback`, wrap components in `React.memo`. With the compiler enabled, that work is redundant for new code, and over-memoization carries real cost (larger code, more cache slots, harder reading).

### Before (manual, pre-compiler)

```tsx
function Dashboard({ items, onSelect }: Props) {
  const sorted = useMemo(() => items.slice().sort(byName), [items]);
  const total = useMemo(() => items.reduce((s, i) => s + i.value, 0), [items]);
  const handleSelect = useCallback((id: string) => onSelect(id), [onSelect]);

  return <List items={sorted} total={total} onSelect={handleSelect} />;
}

const List = React.memo(function List({ items, total, onSelect }: ListProps) {
  return /* ... */;
});
```

### After (compiler enabled)

```tsx
// Plain code. The compiler memoizes `sorted`, `total`, `handleSelect`,
// and the List render output as needed — including conditionally.
function Dashboard({ items, onSelect }: Props) {
  const sorted = items.slice().sort(byName);
  const total = items.reduce((s, i) => s + i.value, 0);
  const handleSelect = (id: string) => onSelect(id);

  return <List items={sorted} total={total} onSelect={handleSelect} />;
}

function List({ items, total, onSelect }: ListProps) {
  return /* ... */;
}
```

## When Manual Memo Still Earns Its Place

The compiler does not eliminate every reason to memoize by hand. Keep manual memo when:

1. **A value is an effect dependency and correctness depends on its reference identity.** The compiler optimizes *render*; it does not guarantee a particular identity contract for an effect's dependency array. A value recreated each render re-fires the effect.

```tsx
// Correctness, not just performance: a stable `config` prevents the
// subscription effect from tearing down and re-subscribing every render.
const config = useMemo(() => ({ url, token }), [url, token]);
useEffect(() => subscribe(config), [config]);
```

2. **Code the compiler cannot statically analyze.** The compiler is conservative: when it cannot prove a component follows the Rules of React, it skips that component entirely (leaving it un-optimized) rather than risk a miscompile. In a skipped component, manual memo remains a valid local optimization.

## Do Not Strip Existing Manual Memo Blindly

The compiler is designed to *preserve* existing `useMemo`/`useCallback`/`React.memo`. Some of that memo was load-bearing (effect-dependency stability, third-party identity contracts). The [`preserve-manual-memoization`](https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization) lint flags cases where removing or altering manual memo would change behavior. Treat its warnings as a signal that the memo carried meaning beyond performance.

## Adoption Path

Order matters — lint and fix *before* enabling the compiler:

1. **Install ESLint support.** `eslint-plugin-react-hooks` v6+ absorbed the former `eslint-plugin-react-compiler`. Enable the recommended config.

```bash
npm install --save-dev eslint-plugin-react-hooks@^6
```

2. **Fix the reported Rules of React violations.** The plugin surfaces mutations during render, conditional hook calls, and other patterns that prevent safe compilation.

3. **Enable the compiler in the build.** Add the compiler to the toolchain — Babel, Vite, Metro, or Rsbuild.

```js
// vite.config.ts
import react from '@vitejs/plugin-react';

export default {
  plugins: [
    react({
      babel: { plugins: [['babel-plugin-react-compiler', {}]] },
    }),
  ],
};
```

4. **Verify in DevTools.** React DevTools marks compiler-optimized components with a "Memo ✨" badge.

## Rollout Strategy for Existing Codebases

- Start in a directory-scoped mode if the build plugin supports it, expanding as the lint passes clean.
- Do not mix a half-migrated mental model: once the compiler is on for a module, write new code plainly and reserve manual memo for the documented escape hatches.
- Keep `preserve-manual-memoization` enabled so refactors do not silently remove meaningful memo.

## Detection Checklist

| Symptom | Likely cause | Action |
|---|---|---|
| New code still littered with `useMemo`/`useCallback` | Reflex memoization habit | Remove; let the compiler handle it |
| `preserve-manual-memoization` warnings after a cleanup | Removed load-bearing memo | Restore the memo; it was an effect/identity contract |
| A component shows no "Memo ✨" badge | Compiler skipped it (unanalyzable) | Fix Rules of React violations, or accept manual memo there |
| Effect re-fires every render | A dependency value is recreated each render | Memoize that single dependency by hand |

## Sources

- https://react.dev/blog/2025/10/07/react-compiler-1
- https://react.dev/learn/react-compiler/introduction
- https://react.dev/learn/react-compiler/installation
- https://react.dev/reference/eslint-plugin-react-hooks
- https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization
