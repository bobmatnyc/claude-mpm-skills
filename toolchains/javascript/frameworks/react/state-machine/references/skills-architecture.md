# Skills Library Architecture

Building reusable state machine skills requires careful attention to parameterization, composition, and consumer customization.

## Recommended Project Structure

```
/src
  /skills
    /auth
      authMachine.ts      # Machine definition
      authMachine.test.ts # Unit tests
      types.ts            # Exported types
      index.ts            # Public API
    /network
      fetchMachine.ts
      retryMachine.ts
    /ui
      modalMachine.ts
      toastMachine.ts
  /hooks
    useAuthMachine.ts     # React-specific wrappers
  /actors
    index.ts              # Actor logic creators
```

## Input/Output Pattern for Parameterization

XState v5's first-class input support creates truly reusable skills:

```typescript
// Generic fetch skill
export const fetchSkillSetup = setup({
  types: {
    input: {} as { 
      url: string; 
      options?: RequestInit;
      retries?: number;
    },
    context: {} as { 
      data: unknown; 
      error: Error | null;
      attempts: number;
    },
    output: {} as {
      data: unknown;
      fetchedAt: Date;
      attempts: number;
    }
  },
  actors: {
    fetcher: fromPromise(async ({ input, signal }) => {
      const res = await fetch(input.url, { ...input.options, signal });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
  },
  guards: {
    canRetry: ({ context }) => context.attempts < (context.maxRetries ?? 3)
  }
});

export const fetchSkillMachine = fetchSkillSetup.createMachine({
  id: 'fetchSkill',
  initial: 'idle',
  context: ({ input }) => ({
    url: input.url,
    options: input.options,
    maxRetries: input.retries ?? 3,
    data: null,
    error: null,
    attempts: 0
  }),
  states: {
    idle: { 
      on: { FETCH: 'loading' } 
    },
    loading: {
      entry: assign({ attempts: ({ context }) => context.attempts + 1 }),
      invoke: {
        src: 'fetcher',
        input: ({ context }) => ({ 
          url: context.url, 
          options: context.options 
        }),
        onDone: { 
          target: 'success', 
          actions: assign({ data: ({ event }) => event.output }) 
        },
        onError: [
          { 
            target: 'loading', 
            guard: 'canRetry',
            actions: assign({ error: ({ event }) => event.error })
          },
          { 
            target: 'failure',
            actions: assign({ error: ({ event }) => event.error })
          }
        ]
      }
    },
    success: { 
      type: 'final',
      output: ({ context }) => ({
        data: context.data,
        fetchedAt: new Date(),
        attempts: context.attempts
      })
    },
    failure: { 
      on: { RETRY: 'loading' },
      output: ({ context }) => ({
        data: null,
        fetchedAt: new Date(),
        attempts: context.attempts
      })
    }
  }
});

// Consumer usage
const userFetcher = createActor(fetchSkillMachine, {
  input: {
    url: '/api/users/123',
    options: { headers: { Authorization: 'Bearer token' } },
    retries: 5
  }
});

userFetcher.subscribe((snapshot) => {
  if (snapshot.status === 'done') {
    console.log(snapshot.output); // Typed output!
  }
});

userFetcher.start();
userFetcher.send({ type: 'FETCH' });
```

## Placeholder Actions for Consumer Customization

Library machines provide sensible defaults while allowing override:

```typescript
// Library code
export const notificationMachine = setup({
  types: {
    context: {} as { message: string; type: 'success' | 'error' | 'info' },
    events: {} as { type: 'SHOW'; message: string } | { type: 'DISMISS' }
  },
  actions: {
    onShow: () => {}, // Noop default
    onDismiss: () => {}, // Noop default
    logNotification: ({ context }) => {
      console.log(`[${context.type}] ${context.message}`);
    }
  }
}).createMachine({
  initial: 'hidden',
  context: { message: '', type: 'info' },
  states: {
    hidden: {
      on: {
        SHOW: {
          target: 'visible',
          actions: [
            assign({ message: ({ event }) => event.message }),
            'onShow',
            'logNotification'
          ]
        }
      }
    },
    visible: {
      after: { 5000: 'hiding' },
      on: { DISMISS: 'hiding' }
    },
    hiding: {
      entry: 'onDismiss',
      after: { 300: 'hidden' }
    }
  }
});

// Consumer customizes behavior
const customizedNotification = notificationMachine.provide({
  actions: {
    onShow: sendTo(
      ({ system }) => system.get('analytics'),
      ({ context }) => ({ type: 'TRACK', event: 'notification_shown', data: context })
    ),
    onDismiss: ({ context }) => {
      // Custom cleanup logic
      clearRelatedAlerts(context.message);
    }
  }
});
```

## Composition: Invoke vs Spawn

### Invoke: Lifecycle Tied to State

Child actor stops when parent state exits:

```typescript
const checkoutMachine = createMachine({
  states: {
    payment: {
      invoke: {
        src: paymentMachine,
        id: 'payment',
        input: ({ context }) => ({ amount: context.total }),
        onDone: {
          target: 'confirmation',
          actions: assign({ paymentResult: ({ event }) => event.output })
        },
        onError: {
          target: 'paymentError',
          actions: assign({ paymentError: ({ event }) => event.error })
        }
      },
      on: {
        CANCEL: 'cart' // Exiting state stops payment actor
      }
    }
  }
});
```

### Spawn: Independent Lifecycle

Actors persist beyond state transitions—use for dynamic, unknown numbers:

```typescript
const taskManagerMachine = setup({
  types: {
    context: {} as {
      tasks: ActorRefFrom<typeof taskMachine>[];
    }
  }
}).createMachine({
  context: { tasks: [] },
  on: {
    ADD_TASK: {
      actions: assign({
        tasks: ({ context, event, spawn }) => [
          ...context.tasks,
          spawn(taskMachine, {
            id: `task-${event.taskId}`,
            input: { 
              title: event.title,
              dueDate: event.dueDate 
            }
          })
        ]
      })
    },
    TASK_COMPLETED: {
      actions: ({ context, event }) => {
        const task = context.tasks.find(t => t.id === event.taskId);
        task?.send({ type: 'COMPLETE' });
      }
    },
    REMOVE_TASK: {
      actions: assign({
        tasks: ({ context, event }) => {
          const task = context.tasks.find(t => t.id === event.taskId);
          task?.stop(); // Explicitly stop spawned actor
          return context.tasks.filter(t => t.id !== event.taskId);
        }
      })
    }
  }
});
```

## The Receptionist Pattern

Enable arbitrary actor communication without parent-child relationships:

```typescript
// Root machine registers system-wide actors
const appMachine = createMachine({
  invoke: [
    { src: notifierMachine, systemId: 'notifier' },
    { src: authMachine, systemId: 'auth' },
    { src: analyticsMachine, systemId: 'analytics' }
  ]
});

// Any descendant actor can access
const featureMachine = createMachine({
  states: {
    processing: {
      invoke: {
        src: 'heavyOperation',
        onDone: {
          actions: [
            // Notify user
            sendTo(
              ({ system }) => system.get('notifier'),
              { type: 'SHOW', message: 'Processing complete!' }
            ),
            // Track analytics
            sendTo(
              ({ system }) => system.get('analytics'),
              { type: 'TRACK', event: 'feature_completed' }
            )
          ]
        }
      }
    }
  }
});
```

## Export Patterns for Skills Library

### Type exports

```typescript
// types.ts
import type { ActorRefFrom, SnapshotFrom } from 'xstate';
import { fetchSkillMachine } from './fetchMachine';

export type FetchSkillActor = ActorRefFrom<typeof fetchSkillMachine>;
export type FetchSkillSnapshot = SnapshotFrom<typeof fetchSkillMachine>;
export type FetchSkillInput = {
  url: string;
  options?: RequestInit;
  retries?: number;
};
```

### Factory functions

```typescript
// index.ts
import { createActor } from 'xstate';
import { fetchSkillMachine } from './fetchMachine';
import type { FetchSkillInput } from './types';

export function createFetchActor(input: FetchSkillInput) {
  return createActor(fetchSkillMachine, { input });
}

export function createAuthenticatedFetchActor(
  url: string, 
  token: string,
  options?: Partial<FetchSkillInput>
) {
  return createActor(fetchSkillMachine, {
    input: {
      url,
      options: {
        headers: { Authorization: `Bearer ${token}` },
        ...options?.options
      },
      retries: options?.retries ?? 3
    }
  });
}
```

### React hooks wrapper

```typescript
// hooks/useFetchSkill.ts
import { useMachine } from '@xstate/react';
import { fetchSkillMachine } from '../skills/network/fetchMachine';
import type { FetchSkillInput } from '../skills/network/types';

export function useFetchSkill(input: FetchSkillInput) {
  return useMachine(fetchSkillMachine, { input });
}

// Selective subscription version
export function useFetchSkillData(input: FetchSkillInput) {
  const actorRef = useActorRef(fetchSkillMachine, { input });
  const data = useSelector(actorRef, s => s.context.data);
  const isLoading = useSelector(actorRef, s => s.matches('loading'));
  const error = useSelector(actorRef, s => s.context.error);
  
  return {
    data,
    isLoading,
    error,
    fetch: () => actorRef.send({ type: 'FETCH' }),
    retry: () => actorRef.send({ type: 'RETRY' })
  };
}
```

## Deep Persistence for Server-Side State

XState v5 supports recursive serialization of entire actor hierarchies:

```typescript
import { createActor } from 'xstate';

// Serialize
const actor = createActor(complexMachine);
actor.start();
// ... some operations ...
const persistedState = actor.getPersistedSnapshot();
const serialized = JSON.stringify(persistedState);

// Later: Restore
const restored = JSON.parse(serialized);
const restoredActor = createActor(complexMachine, {
  snapshot: restored
});
restoredActor.start(); // Resumes from exact state
```

### With React and localStorage

```typescript
function usePersistentMachine<T>(machine: T, storageKey: string) {
  const [restored, setRestored] = useState(false);
  
  const [snapshot, send, actorRef] = useMachine(machine, {
    snapshot: (() => {
      try {
        const saved = localStorage.getItem(storageKey);
        return saved ? JSON.parse(saved) : undefined;
      } catch {
        return undefined;
      }
    })()
  });
  
  useEffect(() => {
    const subscription = actorRef.subscribe((state) => {
      localStorage.setItem(
        storageKey, 
        JSON.stringify(actorRef.getPersistedSnapshot())
      );
    });
    
    setRestored(true);
    return () => subscription.unsubscribe();
  }, [actorRef, storageKey]);
  
  return { snapshot, send, actorRef, restored };
}
```
