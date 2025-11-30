# XState v5 Patterns and API

## The v4 to v5 Transition

XState v5 represents a philosophical shift from "state machines with actors" to "actors, some of which are state machines." Key terminology changes:

| v4 | v5 |
|----|-----|
| `interpret()` | `createActor()` |
| Services | Actors |
| `schema` | `types` (in `setup()`) |
| External typegen | Strong inference built-in |

## The setup() API

The `setup()` function is the recommended approach for TypeScript projects:

```typescript
import { setup, assign, fromPromise, sendTo } from 'xstate';

const authMachine = setup({
  types: {
    context: {} as { 
      user: User | null; 
      error: string | null;
      retryCount: number;
    },
    events: {} as 
      | { type: 'LOGIN'; username: string; password: string }
      | { type: 'LOGOUT' }
      | { type: 'RETRY' }
      | { type: 'RESET' }
  },
  actors: {
    loginUser: fromPromise(async ({ input, signal }) => {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(input),
        signal // Automatic abort on state exit
      });
      if (!response.ok) throw new Error('Login failed');
      return response.json();
    }),
    refreshSession: fromPromise(async ({ input }) => {
      return fetch('/api/refresh', {
        headers: { Authorization: `Bearer ${input.token}` }
      }).then(r => r.json());
    })
  },
  actions: {
    setUser: assign({ 
      user: ({ event }) => event.output,
      error: null 
    }),
    setError: assign({ 
      error: ({ event }) => event.error.message 
    }),
    incrementRetry: assign({
      retryCount: ({ context }) => context.retryCount + 1
    }),
    resetContext: assign({
      user: null,
      error: null,
      retryCount: 0
    })
  },
  guards: {
    canRetry: ({ context }) => context.retryCount < 3,
    hasValidCredentials: ({ event }) => 
      event.username.length > 0 && event.password.length > 0
  }
}).createMachine({
  id: 'auth',
  initial: 'idle',
  context: { user: null, error: null, retryCount: 0 },
  states: {
    idle: { 
      on: { 
        LOGIN: { 
          target: 'authenticating',
          guard: 'hasValidCredentials'
        } 
      } 
    },
    authenticating: {
      invoke: {
        src: 'loginUser',
        input: ({ event }) => ({ 
          username: event.username, 
          password: event.password 
        }),
        onDone: { target: 'authenticated', actions: 'setUser' },
        onError: [
          { target: 'authenticating', guard: 'canRetry', actions: 'incrementRetry' },
          { target: 'failed', actions: 'setError' }
        ]
      }
    },
    authenticated: { 
      on: { LOGOUT: { target: 'idle', actions: 'resetContext' } }
    },
    failed: {
      on: { 
        RETRY: 'authenticating',
        RESET: { target: 'idle', actions: 'resetContext' }
      }
    }
  }
});
```

## Statecharts: Solving State Explosion

### Hierarchical (Nested) States

Parent states share common transitions; children specialize behavior:

```typescript
const playerMachine = createMachine({
  id: 'player',
  initial: 'loading',
  states: {
    loading: {
      invoke: {
        src: 'loadMedia',
        onDone: 'loaded',
        onError: 'error'
      }
    },
    loaded: {
      // Common transition for all loaded substates
      on: { RELOAD: 'loading' },
      initial: 'paused',
      states: {
        playing: {
          on: { 
            PAUSE: 'paused',
            END: 'ended'
          }
        },
        paused: {
          on: { PLAY: 'playing' }
        },
        ended: {
          on: { RESTART: 'playing' }
        }
      }
    },
    error: {
      on: { RETRY: 'loading' }
    }
  }
});
```

### Parallel (Orthogonal) States

Independent concerns operate simultaneously without state explosion:

```typescript
const videoPlayerMachine = createMachine({
  id: 'videoPlayer',
  initial: 'loading',
  states: {
    loading: { on: { LOADED: 'ready' } },
    ready: {
      type: 'parallel',
      states: {
        playback: {
          initial: 'paused',
          states: {
            playing: { 
              on: { PAUSE: 'paused', END: 'ended' } 
            },
            paused: { 
              on: { PLAY: 'playing' } 
            },
            ended: { 
              on: { RESTART: 'playing' } 
            }
          }
        },
        volume: {
          initial: 'unmuted',
          states: {
            muted: { 
              on: { UNMUTE: 'unmuted' } 
            },
            unmuted: { 
              on: { MUTE: 'muted' } 
            }
          }
        },
        fullscreen: {
          initial: 'windowed',
          states: {
            windowed: { 
              on: { ENTER_FULLSCREEN: 'fullscreen' } 
            },
            fullscreen: { 
              on: { EXIT_FULLSCREEN: 'windowed' } 
            }
          }
        }
      }
    }
  }
});

// Check parallel states
snapshot.matches({ ready: { playback: 'playing', volume: 'muted' } });
```

### History States

Remember previous substate when re-entering compound states:

```typescript
const editorMachine = createMachine({
  id: 'editor',
  initial: 'editing',
  states: {
    editing: {
      initial: 'code',
      states: {
        code: { on: { PREVIEW: 'preview' } },
        preview: { on: { CODE: 'code' } },
        split: { on: { CODE: 'code', PREVIEW: 'preview' } },
        history: { type: 'history', history: 'shallow' }
      },
      on: { MINIMIZE: 'minimized' }
    },
    minimized: {
      on: { RESTORE: 'editing.history' } // Returns to previous editing substate
    }
  }
});
```

## Promise Actors for Async Operations

```typescript
import { fromPromise } from 'xstate';

const fetchActor = fromPromise(async ({ input, signal }) => {
  const response = await fetch(input.url, {
    method: input.method || 'GET',
    headers: input.headers,
    body: input.body ? JSON.stringify(input.body) : undefined,
    signal // Automatic cancellation
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
});

// Usage in machine
invoke: {
  src: fetchActor,
  input: ({ context, event }) => ({
    url: `/api/users/${event.userId}`,
    headers: { Authorization: `Bearer ${context.token}` }
  }),
  onDone: {
    target: 'success',
    actions: assign({ data: ({ event }) => event.output })
  },
  onError: {
    target: 'failure',
    actions: assign({ error: ({ event }) => event.error })
  }
}
```

## Callback Actors for Subscriptions

```typescript
import { fromCallback } from 'xstate';

const websocketActor = fromCallback(({ sendBack, receive, input }) => {
  const ws = new WebSocket(input.url);
  
  ws.onmessage = (event) => {
    sendBack({ type: 'MESSAGE', data: JSON.parse(event.data) });
  };
  
  ws.onerror = () => {
    sendBack({ type: 'ERROR' });
  };
  
  ws.onclose = () => {
    sendBack({ type: 'CLOSED' });
  };
  
  // Receive events from parent
  receive((event) => {
    if (event.type === 'SEND') {
      ws.send(JSON.stringify(event.data));
    }
  });
  
  // Cleanup function
  return () => ws.close();
});
```

## Observable Actors for Streams

```typescript
import { fromObservable } from 'xstate';
import { interval } from 'rxjs';
import { map, takeUntil } from 'rxjs/operators';

const timerActor = fromObservable(({ input }) => 
  interval(input.interval).pipe(
    map(count => ({ type: 'TICK', count }))
  )
);
```

## Delayed Transitions

```typescript
const modalMachine = createMachine({
  initial: 'closed',
  states: {
    closed: { 
      on: { OPEN: 'opening' } 
    },
    opening: {
      after: { 
        300: 'open' // Transition after 300ms
      }
    },
    open: { 
      on: { CLOSE: 'closing' } 
    },
    closing: {
      after: {
        CLOSE_DELAY: 'closed' // Named delay
      }
    }
  }
}, {
  delays: {
    CLOSE_DELAY: ({ context }) => context.animationDuration || 300
  }
});
```

## Spawning Dynamic Actors

```typescript
import { spawn } from 'xstate';

const todoListMachine = setup({
  types: {
    context: {} as {
      todos: ActorRefFrom<typeof todoItemMachine>[];
    }
  }
}).createMachine({
  context: { todos: [] },
  on: {
    ADD_TODO: {
      actions: assign({
        todos: ({ context, event, spawn }) => [
          ...context.todos,
          spawn(todoItemMachine, {
            id: `todo-${Date.now()}`,
            input: { text: event.text }
          })
        ]
      })
    },
    REMOVE_TODO: {
      actions: assign({
        todos: ({ context, event }) => {
          const todo = context.todos.find(t => t.id === event.todoId);
          todo?.stop();
          return context.todos.filter(t => t.id !== event.todoId);
        }
      })
    }
  }
});
```

## The Receptionist Pattern (systemId)

Allow any actor to communicate with another without parent-child relationship:

```typescript
const appMachine = createMachine({
  invoke: [
    { 
      src: notificationMachine, 
      systemId: 'notifier' // Register globally
    },
    { 
      src: authMachine, 
      systemId: 'auth' 
    }
  ]
});

// Any child actor can now access
const childMachine = createMachine({
  entry: sendTo(
    ({ system }) => system.get('notifier'),
    { type: 'SHOW_NOTIFICATION', message: 'Hello!' }
  )
});
```

## Input and Output for Parameterized Actors

```typescript
const fetchMachine = setup({
  types: {
    input: {} as { url: string; retries?: number },
    output: {} as { data: unknown; fetchedAt: Date }
  }
}).createMachine({
  context: ({ input }) => ({
    url: input.url,
    retries: input.retries ?? 3,
    data: null
  }),
  states: {
    // ...
    success: {
      type: 'final',
      output: ({ context }) => ({
        data: context.data,
        fetchedAt: new Date()
      })
    }
  }
});

// Consumer receives typed output
const parentMachine = createMachine({
  invoke: {
    src: fetchMachine,
    input: { url: '/api/data', retries: 5 },
    onDone: {
      actions: ({ event }) => {
        console.log(event.output.data);      // Typed!
        console.log(event.output.fetchedAt); // Typed!
      }
    }
  }
});
```
