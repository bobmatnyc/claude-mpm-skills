# Performance Optimization Patterns

## Selector Memoization

### Problem: Recreating Selectors Every Render

```typescript
// ❌ BAD: New function every render
function Component() {
  const actorRef = useActorRef(machine);
  const count = useSelector(actorRef, (s) => s.context.count); // New function!
  // Component re-renders even if count hasn't changed
}
```

### Solution 1: Define Selectors Outside Component

```typescript
// ✅ GOOD: Stable selector reference
const selectCount = (s) => s.context.count;
const selectUser = (s) => s.context.user;
const selectIsLoading = (s) => s.matches('loading');

function Component() {
  const actorRef = useActorRef(machine);
  const count = useSelector(actorRef, selectCount);
  const user = useSelector(actorRef, selectUser);
  const isLoading = useSelector(actorRef, selectIsLoading);
}
```

### Solution 2: useCallback for Dynamic Selectors

```typescript
function Component({ userId }: { userId: string }) {
  const actorRef = useActorRef(machine);
  
  // Memoize selector with dependencies
  const selectUserById = useCallback(
    (s) => s.context.users.find(u => u.id === userId),
    [userId]
  );
  
  const user = useSelector(actorRef, selectUserById);
}
```

### Solution 3: Selector Factory Pattern

```typescript
// Create selector factory
const createUserSelector = (userId: string) => (s) => 
  s.context.users.find(u => u.id === userId);

function Component({ userId }: { userId: string }) {
  const actorRef = useActorRef(machine);
  const selectUser = useMemo(() => createUserSelector(userId), [userId]);
  const user = useSelector(actorRef, selectUser);
}
```

## Complex Object Selection

### Problem: Reference Equality for Objects/Arrays

```typescript
// ❌ BAD: New array reference every time
const selectTodos = (s) => s.context.todos.filter(t => !t.completed);

function TodoList() {
  const actorRef = useActorRef(machine);
  const todos = useSelector(actorRef, selectTodos);
  // Re-renders even if todos haven't changed!
}
```

### Solution: Use Comparison Function

```typescript
import { useSelector } from '@xstate/react';

// Shallow equality comparison
function shallowEqual<T>(a: T, b: T): boolean {
  if (a === b) return true;
  if (!a || !b) return false;
  
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  
  if (keysA.length !== keysB.length) return false;
  
  return keysA.every(key => a[key] === b[key]);
}

// Array shallow equality
function arrayShallowEqual<T>(a: T[], b: T[]): boolean {
  if (a === b) return true;
  if (a.length !== b.length) return false;
  return a.every((item, index) => item === b[index]);
}

// Usage
const selectTodos = (s) => s.context.todos;

function TodoList() {
  const actorRef = useActorRef(machine);
  const todos = useSelector(actorRef, selectTodos, arrayShallowEqual);
  // Only re-renders when todos array actually changes
}
```

### Solution: Select Primitive Values

```typescript
// ✅ BETTER: Select only what you need
const selectTodoCount = (s) => s.context.todos.length;
const selectCompletedCount = (s) => s.context.todos.filter(t => t.completed).length;

function TodoStats() {
  const actorRef = useActorRef(machine);
  const total = useSelector(actorRef, selectTodoCount);
  const completed = useSelector(actorRef, selectCompletedCount);
  
  return <div>{completed} / {total} completed</div>;
}
```

## React.memo Integration

### Memoizing Components with State Machine Props

```typescript
import { memo } from 'react';
import { useSelector } from '@xstate/react';

// Memoized child component
const TodoItem = memo(({ 
  todo, 
  onToggle, 
  onDelete 
}: { 
  todo: Todo; 
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}) => {
  console.log('TodoItem render:', todo.id);
  
  return (
    <div className="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span>{todo.text}</span>
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </div>
  );
});

// Parent component
function TodoList() {
  const actorRef = useActorRef(todoMachine);
  const todos = useSelector(actorRef, s => s.context.todos, arrayShallowEqual);
  
  // Memoize callbacks to prevent child re-renders
  const handleToggle = useCallback((id: string) => {
    actorRef.send({ type: 'TOGGLE_TODO', id });
  }, [actorRef]);
  
  const handleDelete = useCallback((id: string) => {
    actorRef.send({ type: 'DELETE_TODO', id });
  }, [actorRef]);
  
  return (
    <div>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}
```

## Type Narrowing with Guards

### Discriminated Unions for Events

```typescript
// ✅ GOOD: Discriminated union with type narrowing
type TodoEvent =
  | { type: 'ADD_TODO'; text: string }
  | { type: 'TOGGLE_TODO'; id: string }
  | { type: 'DELETE_TODO'; id: string }
  | { type: 'UPDATE_TODO'; id: string; text: string };

const todoMachine = setup({
  types: {
    events: {} as TodoEvent
  },
  guards: {
    hasText: ({ event }) => {
      // TypeScript knows event.type could be any TodoEvent
      if (event.type === 'ADD_TODO') {
        // Now TypeScript knows event has 'text' property
        return event.text.length > 0;
      }
      return false;
    }
  }
}).createMachine({
  // ...
});
```

### Branded Types for IDs

```typescript
// Create branded type for type safety
type TodoId = string & { readonly __brand: 'TodoId' };
type UserId = string & { readonly __brand: 'UserId' };

function createTodoId(id: string): TodoId {
  return id as TodoId;
}

function createUserId(id: string): UserId {
  return id as UserId;
}

interface TodoContext {
  todos: Map<TodoId, Todo>;
  currentUserId: UserId | null;
}

// TypeScript prevents mixing up IDs
const todoMachine = setup({
  types: {
    context: {} as TodoContext
  },
  guards: {
    isTodoOwner: ({ context, event }) => {
      const todo = context.todos.get(event.todoId); // TodoId required
      return todo?.ownerId === context.currentUserId; // UserId comparison
    }
  }
});
```

## Machine Splitting Strategies

### Strategy 1: Extract Independent Concerns

```typescript
// ❌ BAD: Monolithic machine
const dashboardMachine = createMachine({
  context: {
    user: null,
    notifications: [],
    settings: {},
    analytics: {},
    // ... 20 more fields
  },
  states: {
    // 50+ states handling everything
  }
});

// ✅ GOOD: Split by domain
const userMachine = createMachine({
  context: { user: null, profile: null },
  states: { idle, loading, authenticated }
});

const notificationsMachine = createMachine({
  context: { notifications: [], unreadCount: 0 },
  states: { idle, fetching, polling }
});

const settingsMachine = createMachine({
  context: { theme: 'light', language: 'en' },
  states: { idle, saving }
});

// Compose in parent
const dashboardMachine = createMachine({
  invoke: [
    { src: userMachine, systemId: 'user' },
    { src: notificationsMachine, systemId: 'notifications' },
    { src: settingsMachine, systemId: 'settings' }
  ]
});
```

### Strategy 2: Use Parallel States for Orthogonal Concerns

```typescript
// ✅ GOOD: Parallel states for independent features
const editorMachine = createMachine({
  type: 'parallel',
  states: {
    // Document state
    document: {
      initial: 'clean',
      states: {
        clean: { on: { EDIT: 'dirty' } },
        dirty: { on: { SAVE: 'saving' } },
        saving: { on: { SAVED: 'clean' } }
      }
    },

    // Collaboration state (independent)
    collaboration: {
      initial: 'solo',
      states: {
        solo: { on: { JOIN: 'connected' } },
        connected: { on: { DISCONNECT: 'solo' } }
      }
    },

    // Preview state (independent)
    preview: {
      initial: 'hidden',
      states: {
        hidden: { on: { SHOW_PREVIEW: 'visible' } },
        visible: { on: { HIDE_PREVIEW: 'hidden' } }
      }
    }
  }
});
```

### Strategy 3: Lazy Loading Machines

```typescript
import { lazy, Suspense } from 'react';
import { useMachine } from '@xstate/react';

// Lazy load heavy machines
const HeavyFeatureMachine = lazy(() =>
  import('./heavyFeatureMachine').then(m => ({ default: m.heavyFeatureMachine }))
);

function FeatureComponent() {
  const [showFeature, setShowFeature] = useState(false);

  return (
    <div>
      <button onClick={() => setShowFeature(true)}>
        Load Feature
      </button>

      {showFeature && (
        <Suspense fallback={<div>Loading...</div>}>
          <HeavyFeature />
        </Suspense>
      )}
    </div>
  );
}

function HeavyFeature() {
  const machine = useMemo(() => createHeavyMachine(), []);
  const [snapshot, send] = useMachine(machine);
  // ...
}
```

## Debouncing and Throttling

### Debounced Input with State Machine

```typescript
const searchMachine = setup({
  types: {
    context: {} as { query: string; results: any[] },
    events: {} as
      | { type: 'TYPE'; value: string }
      | { type: 'SEARCH' }
  },
  actors: {
    search: fromPromise(async ({ input }) => {
      const res = await fetch(`/api/search?q=${input.query}`);
      return res.json();
    })
  }
}).createMachine({
  initial: 'idle',
  context: { query: '', results: [] },
  states: {
    idle: {
      on: {
        TYPE: {
          target: 'debouncing',
          actions: assign({ query: ({ event }) => event.value })
        }
      }
    },

    debouncing: {
      after: {
        300: 'searching' // Wait 300ms
      },
      on: {
        TYPE: {
          target: 'debouncing', // Restart timer
          actions: assign({ query: ({ event }) => event.value })
        }
      }
    },

    searching: {
      invoke: {
        src: 'search',
        input: ({ context }) => ({ query: context.query }),
        onDone: {
          target: 'idle',
          actions: assign({ results: ({ event }) => event.output })
        }
      },
      on: {
        TYPE: {
          target: 'debouncing',
          actions: assign({ query: ({ event }) => event.value })
        }
      }
    }
  }
});
```

### Throttled Scroll Events

```typescript
const scrollMachine = setup({
  types: {
    context: {} as { scrollY: number; isAtBottom: boolean },
    events: {} as { type: 'SCROLL'; scrollY: number }
  }
}).createMachine({
  initial: 'idle',
  context: { scrollY: 0, isAtBottom: false },
  states: {
    idle: {
      on: {
        SCROLL: {
          target: 'throttling',
          actions: assign({
            scrollY: ({ event }) => event.scrollY,
            isAtBottom: ({ event }) =>
              event.scrollY + window.innerHeight >= document.body.scrollHeight - 100
          })
        }
      }
    },

    throttling: {
      after: {
        100: 'idle' // Ignore events for 100ms
      }
    }
  }
});
```

## Performance Monitoring

### Measuring State Machine Performance

```typescript
import { createActor } from 'xstate';

function createMonitoredActor(machine) {
  const actor = createActor(machine);

  actor.subscribe({
    next: (snapshot) => {
      // Log transition time
      console.time(`Transition to ${snapshot.value}`);
    },
    complete: () => {
      console.timeEnd('Actor lifecycle');
    }
  });

  // Wrap send to measure event processing
  const originalSend = actor.send.bind(actor);
  actor.send = (event) => {
    const start = performance.now();
    originalSend(event);
    const duration = performance.now() - start;

    if (duration > 16) { // Longer than 1 frame
      console.warn(`Slow event processing: ${event.type} took ${duration}ms`);
    }
  };

  return actor;
}
```

## Best Practices Summary

### Performance Checklist

✅ **Define selectors outside components** for stable references
✅ **Use comparison functions** for complex objects/arrays
✅ **Select primitive values** when possible
✅ **Memoize callbacks** passed to child components
✅ **Use React.memo** for expensive child components
✅ **Split large machines** into smaller, focused ones
✅ **Use parallel states** for orthogonal concerns
✅ **Debounce/throttle** high-frequency events
✅ **Lazy load** heavy machines
✅ **Monitor performance** in development
✅ **Profile with React DevTools** to find bottlenecks

### Common Performance Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Inline selectors | Re-renders on every state change | Define outside component |
| useMachine for large state | Unnecessary re-renders | Use useActorRef + useSelector |
| No comparison function | Re-renders on object reference change | Use shallowEqual |
| Monolithic machines | Hard to optimize, slow transitions | Split by domain |
| No memoization | Child components re-render unnecessarily | Use React.memo + useCallback |
| Synchronous heavy work | Blocks UI thread | Move to Web Worker or async |


