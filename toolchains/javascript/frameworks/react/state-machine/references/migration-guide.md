# Migration Guide: From React Hooks to State Machines

## From useState to State Machines

### Example 1: Simple Toggle

#### Before (useState)

```typescript
function ToggleButton() {
  const [isOn, setIsOn] = useState(false);
  
  return (
    <button onClick={() => setIsOn(!isOn)}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  );
}
```

#### After (State Machine)

```typescript
import { setup } from 'xstate';
import { useMachine } from '@xstate/react';

const toggleMachine = setup({
  types: {
    events: {} as { type: 'TOGGLE' }
  }
}).createMachine({
  id: 'toggle',
  initial: 'off',
  states: {
    off: { on: { TOGGLE: 'on' } },
    on: { on: { TOGGLE: 'off' } }
  }
});

function ToggleButton() {
  const [snapshot, send] = useMachine(toggleMachine);
  
  return (
    <button onClick={() => send({ type: 'TOGGLE' })}>
      {snapshot.matches('on') ? 'ON' : 'OFF'}
    </button>
  );
}
```

**When to migrate:** When you have boolean flags that represent distinct states.

### Example 2: Boolean Flag Explosion

#### Before (useState) - The Problem

```typescript
function DataFetcher() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRetrying, setIsRetrying] = useState(false);
  
  // ❌ Impossible states possible:
  // isLoading=true AND error=true
  // isLoading=false AND data=null AND error=null
  
  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await fetch('/api/data');
      setData(result);
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div>
      {isLoading && <div>Loading...</div>}
      {error && <div>Error: {error.message}</div>}
      {data && <div>{data}</div>}
    </div>
  );
}
```

#### After (State Machine) - Impossible States Eliminated

```typescript
import { setup, fromPromise } from 'xstate';
import { useMachine } from '@xstate/react';

const dataFetcherMachine = setup({
  types: {
    context: {} as { data: any; error: Error | null },
    events: {} as { type: 'FETCH' } | { type: 'RETRY' }
  },
  actors: {
    fetchData: fromPromise(async () => {
      const response = await fetch('/api/data');
      if (!response.ok) throw new Error('Failed to fetch');
      return response.json();
    })
  }
}).createMachine({
  id: 'dataFetcher',
  initial: 'idle',
  context: { data: null, error: null },
  states: {
    idle: {
      on: { FETCH: 'loading' }
    },
    loading: {
      invoke: {
        src: 'fetchData',
        onDone: {
          target: 'success',
          actions: assign({ data: ({ event }) => event.output })
        },
        onError: {
          target: 'failure',
          actions: assign({ error: ({ event }) => event.error })
        }
      }
    },
    success: {
      on: { FETCH: 'loading' }
    },
    failure: {
      on: { RETRY: 'loading' }
    }
  }
});

function DataFetcher() {
  const [snapshot, send] = useMachine(dataFetcherMachine);
  
  return (
    <div>
      {snapshot.matches('loading') && <div>Loading...</div>}
      {snapshot.matches('failure') && (
        <div>
          Error: {snapshot.context.error?.message}
          <button onClick={() => send({ type: 'RETRY' })}>Retry</button>
        </div>
      )}
      {snapshot.matches('success') && <div>{snapshot.context.data}</div>}
    </div>
  );
}
```

**When to migrate:** When you have 3+ boolean flags representing state.

### Example 3: Complex State Transitions

#### Before (useState) - Hard to Reason About

```typescript
function FormWizard() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  
  const goNext = () => {
    // ❌ Complex validation logic scattered
    if (step === 1 && !formData.name) {
      setErrors({ name: 'Required' });
      return;
    }
    if (step === 2 && !formData.email) {
      setErrors({ email: 'Required' });
      return;
    }
    setStep(step + 1);
  };
  
  const goBack = () => {
    if (step > 1) setStep(step - 1);
  };
  
  // ❌ Can accidentally set step to invalid value
  // setStep(99) - no protection
}
```

#### After (State Machine) - Explicit Transitions

```typescript
const wizardMachine = setup({
  types: {
    context: {} as { formData: any; errors: any },
    events: {} as
      | { type: 'NEXT' }
      | { type: 'PREVIOUS' }
      | { type: 'UPDATE'; field: string; value: any }
  },
  guards: {
    isStep1Valid: ({ context }) => !!context.formData.name,
    isStep2Valid: ({ context }) => !!context.formData.email
  }
}).createMachine({
  id: 'wizard',
  initial: 'step1',
  context: { formData: {}, errors: {} },
  states: {
    step1: {
      on: {
        NEXT: {
          target: 'step2',
          guard: 'isStep1Valid'
        },
        UPDATE: {
          actions: assign({
            formData: ({ context, event }) => ({
              ...context.formData,
              [event.field]: event.value
            })
          })
        }
      }
    },
    step2: {
      on: {
        NEXT: {
          target: 'step3',
          guard: 'isStep2Valid'
        },
        PREVIOUS: 'step1'
      }
    },
    step3: {
      on: {
        PREVIOUS: 'step2'
      }
    }
  }
});
```

**When to migrate:** When you have sequential states with validation.

## From useReducer to State Machines

### Example: Authentication Flow

#### Before (useReducer)

```typescript
type State = {
  status: 'idle' | 'loading' | 'authenticated' | 'error';
  user: User | null;
  error: Error | null;
};

type Action =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; user: User }
  | { type: 'LOGIN_FAILURE'; error: Error }
  | { type: 'LOGOUT' };

function authReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, status: 'loading', error: null };
    case 'LOGIN_SUCCESS':
      return { status: 'authenticated', user: action.user, error: null };
    case 'LOGIN_FAILURE':
      return { ...state, status: 'error', error: action.error };
    case 'LOGOUT':
      return { status: 'idle', user: null, error: null };
    default:
      return state;
  }
}

function useAuth() {
  const [state, dispatch] = useReducer(authReducer, {
    status: 'idle',
    user: null,
    error: null
  });
  
  const login = async (credentials) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const user = await api.login(credentials);
      dispatch({ type: 'LOGIN_SUCCESS', user });
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE', error });
    }
  };
  
  return { state, login };
}
```

#### After (State Machine)

```typescript
import { setup, fromPromise, assign } from 'xstate';
import { useMachine } from '@xstate/react';

const authMachine = setup({
  types: {
    context: {} as { user: User | null; error: Error | null },
    events: {} as
      | { type: 'LOGIN'; credentials: Credentials }
      | { type: 'LOGOUT' }
  },
  actors: {
    loginUser: fromPromise(async ({ input }) => {
      return await api.login(input.credentials);
    })
  }
}).createMachine({
  id: 'auth',
  initial: 'idle',
  context: { user: null, error: null },
  states: {
    idle: {
      on: {
        LOGIN: 'authenticating'
      }
    },
    authenticating: {
      invoke: {
        src: 'loginUser',
        input: ({ event }) => ({ credentials: event.credentials }),
        onDone: {
          target: 'authenticated',
          actions: assign({ user: ({ event }) => event.output })
        },
        onError: {
          target: 'idle',
          actions: assign({ error: ({ event }) => event.error })
        }
      }
    },
    authenticated: {
      on: {
        LOGOUT: {
          target: 'idle',
          actions: assign({ user: null })
        }
      }
    }
  }
});

function useAuth() {
  const [snapshot, send] = useMachine(authMachine);

  const login = (credentials: Credentials) => {
    send({ type: 'LOGIN', credentials });
  };

  const logout = () => {
    send({ type: 'LOGOUT' });
  };

  return {
    isAuthenticated: snapshot.matches('authenticated'),
    isLoading: snapshot.matches('authenticating'),
    user: snapshot.context.user,
    error: snapshot.context.error,
    login,
    logout
  };
}
```

**Benefits:**
- ✅ Async logic handled by machine (no manual try/catch)
- ✅ Impossible to be in `loading` and `authenticated` simultaneously
- ✅ Clear state transitions
- ✅ Built-in side effect management

## Migration Strategy

### Step-by-Step Process

#### 1. Identify State Patterns

Look for these patterns in your code:
- Multiple `useState` calls for related state
- Boolean flags that represent states (`isLoading`, `isError`, `isSuccess`)
- Complex `useEffect` dependencies
- State that depends on other state
- Sequential workflows (wizards, multi-step forms)

#### 2. Map States and Events

```typescript
// Current useState code
const [isLoading, setIsLoading] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
const [isError, setIsError] = useState(false);

// Map to states
// States: idle, loading, success, error

// Map events
// Events: FETCH, RETRY, RESET
```

#### 3. Create Machine Definition

```typescript
const machine = setup({
  types: {
    events: {} as
      | { type: 'FETCH' }
      | { type: 'RETRY' }
      | { type: 'RESET' }
  }
}).createMachine({
  initial: 'idle',
  states: {
    idle: { on: { FETCH: 'loading' } },
    loading: { /* ... */ },
    success: { on: { RESET: 'idle' } },
    error: { on: { RETRY: 'loading' } }
  }
});
```

#### 4. Migrate Incrementally

Don't rewrite everything at once. Start with one component:

```typescript
// Phase 1: Keep old code, add machine alongside
function Component() {
  // Old code (keep working)
  const [isLoading, setIsLoading] = useState(false);

  // New machine (test in parallel)
  const [snapshot, send] = useMachine(newMachine);

  // Use old code in UI for now
  return <div>{isLoading ? 'Loading...' : 'Ready'}</div>;
}

// Phase 2: Switch UI to machine, keep old code
function Component() {
  const [isLoading, setIsLoading] = useState(false);
  const [snapshot, send] = useMachine(newMachine);

  // Use machine in UI
  return <div>{snapshot.matches('loading') ? 'Loading...' : 'Ready'}</div>;
}

// Phase 3: Remove old code
function Component() {
  const [snapshot, send] = useMachine(newMachine);
  return <div>{snapshot.matches('loading') ? 'Loading...' : 'Ready'}</div>;
}
```

#### 5. Test Thoroughly

```typescript
import { createActor } from 'xstate';
import { describe, it, expect } from 'vitest';

describe('Migration to state machine', () => {
  it('should handle same scenarios as old code', () => {
    const actor = createActor(newMachine);
    actor.start();

    // Test old behavior
    expect(actor.getSnapshot().matches('idle')).toBe(true);

    actor.send({ type: 'FETCH' });
    expect(actor.getSnapshot().matches('loading')).toBe(true);
  });
});
```

## Common Migration Pitfalls

### Pitfall 1: Over-Engineering Simple State

```typescript
// ❌ DON'T: Use state machine for simple boolean
const toggleMachine = setup({...}).createMachine({
  initial: 'off',
  states: {
    off: { on: { TOGGLE: 'on' } },
    on: { on: { TOGGLE: 'off' } }
  }
});

// ✅ DO: Use useState for simple cases
const [isOn, setIsOn] = useState(false);
```

**Rule:** If you only have 2 states and 1 event, useState is fine.

### Pitfall 2: Not Using Actors for Async

```typescript
// ❌ DON'T: Manual async in actions
const machine = setup({
  actions: {
    fetchData: async ({ context }) => {
      const data = await fetch('/api'); // Won't work!
      // Actions can't be async
    }
  }
});

// ✅ DO: Use invoke with fromPromise
const machine = setup({
  actors: {
    fetchData: fromPromise(async () => {
      return await fetch('/api').then(r => r.json());
    })
  }
}).createMachine({
  states: {
    loading: {
      invoke: {
        src: 'fetchData',
        onDone: 'success',
        onError: 'failure'
      }
    }
  }
});
```

### Pitfall 3: Forgetting to Handle All States in UI

```typescript
// ❌ DON'T: Forget states
function Component() {
  const [snapshot, send] = useMachine(machine);

  if (snapshot.matches('success')) {
    return <div>Success!</div>;
  }
  // What about loading? error? idle?
  return null; // ❌ Incomplete
}

// ✅ DO: Handle all states
function Component() {
  const [snapshot, send] = useMachine(machine);

  if (snapshot.matches('loading')) return <Spinner />;
  if (snapshot.matches('error')) return <Error />;
  if (snapshot.matches('success')) return <Success />;
  return <Idle />; // Default state
}
```

## Migration Checklist

### Before Migration

- [ ] Identify components with complex state logic
- [ ] Map out current states and transitions
- [ ] List all events that trigger state changes
- [ ] Document current behavior (write tests if needed)
- [ ] Choose one component to start with

### During Migration

- [ ] Create machine definition
- [ ] Add TypeScript types for context and events
- [ ] Implement guards for conditional transitions
- [ ] Use actors for async operations
- [ ] Test machine in isolation
- [ ] Integrate with React component
- [ ] Update UI to handle all states
- [ ] Test edge cases

### After Migration

- [ ] Remove old useState/useReducer code
- [ ] Update tests
- [ ] Document state machine (visualize with Stately)
- [ ] Monitor for regressions
- [ ] Share learnings with team

## Resources

- [XState v5 Migration Guide](https://stately.ai/docs/migration)
- [State Machine Visualizer](https://stately.ai/viz)
- [XState Examples](https://github.com/statelyai/xstate/tree/main/examples)


