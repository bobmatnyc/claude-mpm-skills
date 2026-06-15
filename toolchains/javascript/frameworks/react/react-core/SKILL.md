---
name: react-core
description: General React fundamentals - components and JSX, props and state, the core hooks (useState/useEffect/useRef/useMemo/useCallback/useContext), composition, conditional and list rendering, and controlled inputs. The canonical "depends on React" reference.
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "React fundamentals: components, JSX, props/state, core hooks, composition, conditional/list rendering, controlled inputs"
    when_to_use: "Building any React UI, or as the baseline dependency for React-ecosystem skills that require core React knowledge"
    quick_start: "1. Write a function component returning JSX 2. Hold state with useState 3. Run effects with useEffect 4. Compose via children and props"
context_limit: 700
tags:
  - react
  - components
  - jsx
  - hooks
  - useState
  - useEffect
  - props
  - state
  - composition
  - controlled-inputs
requires_tools: []
---

# React Core Fundamentals

## Overview

The canonical reference for general React fundamentals. This skill covers the building blocks every React application shares: components and JSX, props and state, the core hooks, composition patterns, conditional and list rendering, and controlled inputs. It is the baseline "depends on React" target for ecosystem skills (styling, data fetching, state management, deployment) that assume core React knowledge.

Keep this skill focused on fundamentals. For advanced hook composition (SWR-backed custom hooks, debounced contexts, memoized providers), use the sibling `react-hooks-composition` skill. For explicit finite-state-machine modeling of complex UI flows, use the sibling `react-state-machine` skill.

## When to Use This Skill

Reach for this skill when:
- Building components, wiring props, or managing local state
- Choosing among the core hooks for a given problem
- Rendering lists or conditional UI
- Implementing controlled form inputs
- Establishing the React baseline that another ecosystem skill depends on

## Components and JSX

A React component is a function that returns JSX. Name components in PascalCase. Return a single root node, or wrap siblings in a fragment (`<>...</>`).

```tsx
type GreetingProps = {
  name: string;
};

function Greeting({ name }: GreetingProps) {
  return (
    <>
      <h1>Hello, {name}</h1>
      <p>Welcome back.</p>
    </>
  );
}
```

JSX embeds expressions inside `{}`. Attributes use camelCase (`className`, `onClick`, `htmlFor`). JSX returns a description of the UI; React reconciles it against the DOM.

## Props and State

Props pass data down from parent to child and are read-only inside the child. State holds data a component owns and mutates over time.

```tsx
import { useState } from 'react';

function Counter({ step = 1 }: { step?: number }) {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount((prev) => prev + step)}>
      Count: {count}
    </button>
  );
}
```

Treat props and state as immutable. Update state through the setter, and prefer the functional updater (`setCount(prev => prev + 1)`) when the next value derives from the previous one.

## Core Hooks Overview

Call hooks only at the top level of a component or custom hook, never inside conditionals, loops, or nested functions. This rule keeps hook call order stable across renders.

### useState — local component state

Holds a value and a setter. Re-renders the component when the value changes.

```tsx
const [open, setOpen] = useState(false);
```

### useEffect — synchronize with external systems

Runs after render to perform side effects: subscriptions, timers, data fetching, manual DOM work. The dependency array controls when the effect re-runs. Return a cleanup function to tear down subscriptions.

```tsx
import { useEffect, useState } from 'react';

function WindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []); // empty deps: subscribe once on mount, clean up on unmount

  return <span>{width}px</span>;
}
```

### useRef — mutable value that survives renders

Stores a mutable value without triggering re-renders. Common uses: referencing a DOM node, or holding a value across renders (timer ids, previous values).

```tsx
import { useRef, useEffect } from 'react';

function AutoFocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => inputRef.current?.focus(), []);
  return <input ref={inputRef} />;
}
```

### useMemo — cache an expensive computation

Recomputes a value only when its dependencies change. Apply it for genuinely expensive calculations or to stabilize reference identity passed to memoized children.

```tsx
const sorted = useMemo(() => items.slice().sort(compare), [items]);
```

### useCallback — stabilize a function reference

Returns the same function instance across renders while dependencies stay equal. Pass stable callbacks to memoized children or to effect dependency arrays.

```tsx
const handleSelect = useCallback((id: string) => onSelect(id), [onSelect]);
```

### useContext — read shared state without prop drilling

Reads the current value of a context provided higher in the tree.

```tsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext<'light' | 'dark'>('light');

function ThemedLabel() {
  const theme = useContext(ThemeContext);
  return <span className={theme}>Themed</span>;
}
```

For memoized provider patterns that prevent unnecessary consumer re-renders, see `react-hooks-composition`.

## Composition Patterns

Favor composition over configuration. Pass content through `children` and pass behavior through props.

```tsx
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="card">
      <h2>{title}</h2>
      <div className="card-body">{children}</div>
    </section>
  );
}

// Usage
<Card title="Profile">
  <Avatar />
  <p>Bio text</p>
</Card>;
```

Extract shared logic into custom hooks (`useSomething`) rather than copying it between components. Keep components small and single-purpose.

## Conditional and List Rendering

Render conditionally with `&&` for presence or a ternary for either/or. Render lists with `map`, and give each item a stable `key` derived from its identity (not the array index where order can change).

```tsx
function TodoList({ todos }: { todos: { id: string; text: string; done: boolean }[] }) {
  if (todos.length === 0) return <p>No todos yet.</p>;

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>
          {todo.done ? <s>{todo.text}</s> : todo.text}
        </li>
      ))}
    </ul>
  );
}
```

## Controlled Inputs

A controlled input derives its value from state and reports changes through `onChange`. State is the single source of truth.

```tsx
import { useState } from 'react';

function NameField() {
  const [name, setName] = useState('');

  return (
    <label>
      Name
      <input
        value={name}
        onChange={(event) => setName(event.target.value)}
      />
    </label>
  );
}
```

## Anti-Patterns to Avoid

### ❌ Don't: Mutate state directly

Direct mutation skips the setter, so React does not re-render.

```tsx
// BAD: mutates the array in place; React sees the same reference
function addItem(items: string[], next: string) {
  items.push(next);
  setItems(items);
}
```

```tsx
// GOOD: create a new array so the reference changes
function addItem(items: string[], next: string) {
  setItems([...items, next]);
}
```

### ❌ Don't: Call hooks conditionally

Conditional hook calls break the stable call order React relies on.

```tsx
// BAD: hook call order changes between renders
function Profile({ id }: { id?: string }) {
  if (id) {
    const data = useUser(id); // conditional hook call
    return <span>{data.name}</span>;
  }
  return null;
}
```

```tsx
// GOOD: call the hook unconditionally; branch on its result
function Profile({ id }: { id?: string }) {
  const data = useUser(id); // useUser must accept an undefined id (no fetch / returns null) so the hook is always called
  if (!id || !data) return null;
  return <span>{data.name}</span>;
}
```

### ❌ Don't: Use array index as key for reorderable lists

Index keys cause React to misattribute state when items move.

```tsx
// BAD: index key breaks on reorder/insert/delete
{items.map((item, i) => <Row key={i} item={item} />)}
```

```tsx
// GOOD: stable identity key
{items.map((item) => <Row key={item.id} item={item} />)}
```

## When to Reach for Sibling Skills

- **`react-hooks-composition`**: advanced custom-hook composition — SWR-backed data fetching, debounced search with dual loading states, memoized context providers, and reusable async state hooks.
- **`react-state-machine`**: explicit finite-state-machine modeling with XState v5 for complex flows (multi-step forms, media players, modals with animations) where impossible states must be unrepresentable.

## Best Practices Summary

1. **Components return JSX**: PascalCase names, single root or fragment.
2. **Props are read-only**: pass data down, lift state up when sharing.
3. **Update state immutably**: use the setter, prefer the functional updater.
4. **Top-level hooks only**: never call hooks conditionally.
5. **Effects synchronize external systems**: scope with dependencies, clean up subscriptions.
6. **Memoize deliberately**: apply useMemo/useCallback for expensive work or stable identity, not by default.
7. **Stable keys**: key lists by identity, not array index.
8. **Controlled inputs**: state is the single source of truth.

## References

- [React Documentation](https://react.dev/)
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- [Thinking in React](https://react.dev/learn/thinking-in-react)
