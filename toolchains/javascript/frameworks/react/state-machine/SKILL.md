---
name: react-state-machines
description: "Building reusable React state machine skills with XState v5 and the actor model"
version: 1.0.0
category: development
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Build type-safe, visualizable React state machines using XState v5's actor model for predictable UI behavior"
    when_to_use: "Complex async flows, multi-step forms, modal animations, media players, boolean flag explosion, defensive coding patterns"
    quick_start: "1. Define states/events with setup() 2. Use promise actors for async 3. useMachine for simple, useActorRef+useSelector for performance 4. Test with createActor 5. Visualize in Stately Studio"
  references:
    - xstate-v5-patterns.md
    - react-integration.md
    - skills-architecture.md
    - testing-patterns.md
    - decision-trees.md
    - real-world-patterns.md
    - error-handling.md
    - performance.md
    - persistence-hydration.md
    - migration-guide.md
    - composition-patterns.md
context_limit: 700
tags:
  - react
  - state-machine
  - xstate
  - actors
  - async
  - forms
  - ui-logic
requires_tools: []
---

# React State Machines with XState v5

## Overview

State machines make impossible states unrepresentable by modeling UI behavior as explicit states, transitions, and events. XState v5 (2.5M+ weekly npm downloads) unifies state machines with the actor model—every machine is an independent entity with its own lifecycle, enabling sophisticated composition patterns.

## When to Use This Skill

**Trigger patterns:**
- Boolean flag explosion: multiple `isLoading`, `isError`, `isSuccess` flags
- Implicit states: writing `if (isLoading && !isError && data)` to derive mode
- Defensive coding: guards before state updates to prevent invalid transitions
- Timing coordination: timeouts, delays, debouncing across states
- State dependencies: one state depends on another to update correctly

**Do not use for:**
- Simple boolean toggles with no async (useState is simpler)
- Single form fields with basic validation (useReducer suffices)
- Server state caching (React Query/TanStack Query handles this)
- Static data transformations (useMemo is better)
- Simple counters or toggles (useState is clearer)

**See decision-trees.md for comprehensive decision guidance**

## Core Mental Model

**Finite states** represent modes of behavior: `idle`, `loading`, `success`, `error`. A component can only be in ONE state at a time.

**Context (extended state)** stores quantitative data that doesn't define distinct states. The finite state says "playing"; context says *what* at *what volume*.

**Events** trigger transitions between states. Events are objects: `{ type: 'SUBMIT', data: formData }`.

**Guards** conditionally allow/block transitions: `{ guard: 'hasValidInput' }`.

**Actions** are fire-and-forget side effects during transitions or state entry/exit.

**Invoked actors** are long-running processes (API calls, subscriptions) with lifecycle management and cleanup.

## Quick Start: XState v5 setup() Pattern

```typescript
import { setup, assign, fromPromise } from 'xstate';

const fetchMachine = setup({
  types: {
    context: {} as { data: User | null; error: string | null },
    events: {} as 
      | { type: 'FETCH'; userId: string }
      | { type: 'RETRY' }
  },
  actors: {
    fetchUser: fromPromise(async ({ input, signal }) => {
      const res = await fetch(`/api/users/${input.userId}`, { signal });
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
  },
  actions: {
    setData: assign({ data: ({ event }) => event.output }),
    setError: assign({ error: ({ event }) => event.error.message })
  }
}).createMachine({
  id: 'fetch',
  initial: 'idle',
  context: { data: null, error: null },
  states: {
    idle: { on: { FETCH: 'loading' } },
    loading: {
      invoke: {
        src: 'fetchUser',
        input: ({ event }) => ({ userId: event.userId }),
        onDone: { target: 'success', actions: 'setData' },
        onError: { target: 'failure', actions: 'setError' }
      }
    },
    success: { on: { FETCH: 'loading' } },
    failure: { on: { RETRY: 'loading' } }
  }
});
```

## React Integration Decision Tree

| Use Case | Hook | Why |
|----------|------|-----|
| Simple component state | `useMachine` | Straightforward, re-renders on all changes |
| Performance-critical | `useActorRef` + `useSelector` | Selective re-renders only |
| Global/shared state | `createActorContext` | React Context integration |

**Basic pattern:**
```typescript
import { useMachine } from '@xstate/react';

function Toggle() {
  const [snapshot, send] = useMachine(toggleMachine);
  return (
    <button onClick={() => send({ type: 'TOGGLE' })}>
      {snapshot.matches('inactive') ? 'Off' : 'On'}
    </button>
  );
}
```

**Performance pattern:**
```typescript
import { useActorRef, useSelector } from '@xstate/react';

const selectCount = (s) => s.context.count;
const selectLoading = (s) => s.matches('loading');

function Counter() {
  const actorRef = useActorRef(counterMachine);
  const count = useSelector(actorRef, selectCount);
  const loading = useSelector(actorRef, selectLoading);
  // Only re-renders when count or loading changes
}
```

## Anti-Patterns to Avoid

❌ **State explosion**: Flat states for orthogonal concerns. Use parallel states instead.

❌ **Sending events from actions**: Never `send()` inside `assign`. Use `raise` for internal events.

❌ **Impure guards**: Guards must be pure—no side effects, no external mutations.

❌ **Subscribing to entire state**: Use focused selectors with `useSelector`.

❌ **Not memoizing model**:
```typescript
// WRONG
const model = Model.fromJson(layout);  // New model every render

// CORRECT
const modelRef = useRef(Model.fromJson(layout));
```

## Navigation to References

### Core Patterns
- **xstate-v5-patterns.md**: Complete v5 API, statecharts (hierarchy/parallel/history), promise actors
- **react-integration.md**: useMachine vs useActorRef, Context patterns, side effect handling
- **testing-patterns.md**: Unit testing, mocking actors, visualization debugging

### Decision Making & Best Practices
- **decision-trees.md**: When to use state machines vs useState/useReducer/React Query, machine splitting strategies
- **real-world-patterns.md**: Complete examples - auth flows, file uploads, wizards, undo/redo, shopping carts
- **error-handling.md**: Error boundaries, retry strategies, circuit breakers, graceful degradation
- **performance.md**: Selector memoization, React.memo integration, machine splitting for performance

### Advanced Topics
- **persistence-hydration.md**: localStorage persistence, SSR/Next.js hydration, snapshot serialization
- **migration-guide.md**: Step-by-step migration from useState/useReducer with before/after examples
- **composition-patterns.md**: Actor communication, machine composition, higher-order machines, systemId
- **skills-architecture.md**: Input/output parameterization, library structure

## Key Reminders

1. **setup() is the v5 way**: Strong TypeScript inference, actor registration, action definitions
2. **Invoke for async, actions for sync**: Actions are fire-and-forget; invoked actors have lifecycle
3. **Finite states for modes, context for data**: Don't create states for every data variation
4. **Visualize first**: Stately Studio (stately.ai/editor) makes machines living documentation

## Red Flags

- More than 3-4 boolean flags → Need state machine
- Writing `if (a && !b && c)` to determine mode → States should be explicit
- Bugs from invalid state combinations → Machine prevents impossible states
- Can't explain state transitions to stakeholders → Visualization solves this

## Related Skills

- **react**: Parent skill for React patterns
- **nextjs**: Server/client state coordination
- **test-driven-development**: Test machines with createActor before UI integration
