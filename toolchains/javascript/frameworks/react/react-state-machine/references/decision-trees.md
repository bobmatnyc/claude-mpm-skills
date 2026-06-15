# Decision Trees for State Machine Adoption

## When to Use State Machines vs Alternatives

### Decision Tree: State Management Strategy

```
Do you have UI behavior with distinct modes?
├─ NO → Use useState for simple values
│        Use useReducer for related state updates
│
└─ YES → Do you have 3+ boolean flags to track mode?
    ├─ NO → Is there async coordination between states?
    │   ├─ NO → useReducer is sufficient
    │   └─ YES → Consider state machine
    │
    └─ YES → Do you write complex conditionals like:
             if (isLoading && !isError && data && !isRefreshing)?
        ├─ NO → useReducer might work
        └─ YES → **Use state machine** ✓
```

### Concrete Examples

#### ✅ Use State Machine When:

**1. Boolean Flag Explosion**
```typescript
// ANTI-PATTERN: Boolean soup
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
const [isRetrying, setIsRetrying] = useState(false);
const [isRefreshing, setIsRefreshing] = useState(false);

// Impossible states are possible:
// isLoading=true, isSuccess=true, isError=true 🤯
```

**2. Complex State Transitions**
```typescript
// ANTI-PATTERN: Implicit state machine
if (status === 'idle' && !error) {
  // Can transition to loading
} else if (status === 'loading' && retryCount < 3) {
  // Can retry
} else if (status === 'success' && !isStale) {
  // Can refresh
}
// Hard to reason about, easy to introduce bugs
```

**3. Timing Coordination**
```typescript
// ANTI-PATTERN: Manual timeout management
useEffect(() => {
  if (showModal) {
    const timer = setTimeout(() => setIsAnimating(false), 300);
    return () => clearTimeout(timer);
  }
}, [showModal]);
// State machine handles this declaratively
```

**4. Multi-Step Workflows**
- Wizards, onboarding flows, checkout processes
- Each step has validation, can go back/forward
- Need to track progress and prevent invalid jumps

#### ❌ Don't Use State Machine When:

**1. Simple Toggle**
```typescript
// GOOD: Just use useState
const [isOpen, setIsOpen] = useState(false);
<button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
```

**2. Independent Form Fields**
```typescript
// GOOD: useReducer or react-hook-form
const [formData, setFormData] = useReducer(formReducer, initialState);
// No complex state transitions, just data updates
```

**3. Server State Caching**
```typescript
// GOOD: Use React Query / TanStack Query
const { data, isLoading, error } = useQuery(['users'], fetchUsers);
// React Query handles caching, refetching, background updates
```

**4. Simple Derived State**
```typescript
// GOOD: Just compute it
const [count, setCount] = useState(0);
const isEven = count % 2 === 0; // No state machine needed
```

## When to Split Machines

### Decision Tree: Machine Granularity

```
Is your machine definition > 200 lines?
├─ NO → Keep as single machine
│
└─ YES → Do you have parallel concerns?
    ├─ YES → Split into parallel states or separate machines
    │        Example: playback + volume + fullscreen
    │
    └─ NO → Do substates share no common transitions?
        ├─ YES → Extract to separate machines
        │        Example: auth machine + profile machine
        │
        └─ NO → Use hierarchical states
                 Example: form.editing.step1, form.editing.step2
```

### Splitting Strategies

#### 1. Parallel States (Orthogonal Concerns)

```typescript
// BEFORE: Flat state explosion
states: {
  playingMuted, playingUnmuted, pausedMuted, pausedUnmuted,
  playingFullscreen, pausedFullscreen, // ... 12+ states
}

// AFTER: Parallel states
states: {
  ready: {
    type: 'parallel',
    states: {
      playback: { initial: 'paused', states: { playing, paused } },
      volume: { initial: 'unmuted', states: { muted, unmuted } },
      fullscreen: { initial: 'windowed', states: { windowed, fullscreen } }
    }
  }
}
```

#### 2. Separate Machines (Independent Lifecycles)

```typescript
// BEFORE: Monolithic app machine
const appMachine = createMachine({
  states: {
    authenticating, authenticated, // Auth logic
    loadingProfile, profileLoaded, // Profile logic
    fetchingPosts, postsLoaded,    // Posts logic
  }
});

// AFTER: Composed machines
const authMachine = createMachine({ /* auth only */ });
const profileMachine = createMachine({ /* profile only */ });
const postsMachine = createMachine({ /* posts only */ });

// Coordinate via parent
const appMachine = createMachine({
  invoke: [
    { src: authMachine, systemId: 'auth' },
    { src: profileMachine, systemId: 'profile' },
    { src: postsMachine, systemId: 'posts' }
  ]
});
```

#### 3. Hierarchical States (Shared Transitions)

```typescript
// GOOD: Nested states for shared behavior
const editorMachine = createMachine({
  states: {
    editing: {
      // All substates can SAVE or CANCEL
      on: { SAVE: 'saving', CANCEL: 'idle' },
      initial: 'text',
      states: {
        text: { on: { FORMAT: 'formatting' } },
        formatting: { on: { DONE: 'text' } }
      }
    },
    saving: { /* ... */ }
  }
});
```

## Performance Considerations

### Decision Tree: Optimization Strategy

```
Is your component re-rendering too often?
├─ NO → No optimization needed
│
└─ YES → Are you using useMachine?
    ├─ YES → Switch to useActorRef + useSelector
    │        Only subscribe to needed values
    │
    └─ NO → Are your selectors recreated each render?
        ├─ YES → Move selectors outside component
        │        Or memoize with useCallback
        │
        └─ NO → Are you selecting complex objects?
            ├─ YES → Use comparison function (shallowEqual)
            │        Or select primitive values only
            │
            └─ NO → Profile with React DevTools
                     May be unrelated to state machine
```

### Performance Patterns

#### Pattern 1: Selective Subscriptions

```typescript
// SLOW: Re-renders on every state change
const [snapshot, send] = useMachine(complexMachine);

// FAST: Only re-renders when count changes
const actorRef = useActorRef(complexMachine);
const count = useSelector(actorRef, s => s.context.count);
```

#### Pattern 2: Memoized Selectors

```typescript
// SLOW: New function every render
const count = useSelector(actorRef, (s) => s.context.count);

// FAST: Stable reference
const selectCount = useCallback((s) => s.context.count, []);
const count = useSelector(actorRef, selectCount);

// BEST: Define outside component
const selectCount = (s) => s.context.count;
function Component() {
  const count = useSelector(actorRef, selectCount);
}
```

## Summary Cheat Sheet

| Scenario | Solution |
|----------|----------|
| Simple toggle | `useState` |
| Related state updates | `useReducer` |
| 3+ boolean flags for mode | State machine |
| Complex async coordination | State machine |
| Multi-step workflow | State machine |
| Server state caching | React Query |
| Independent form fields | `useReducer` or react-hook-form |
| Parallel concerns | Parallel states |
| Independent lifecycles | Separate machines |
| Shared transitions | Hierarchical states |
| Too many re-renders | `useActorRef` + `useSelector` |
| Complex object selection | Comparison function |

