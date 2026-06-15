# React Integration Patterns

## Hook Selection Guide

### useMachine: Component-Scoped State

Most straightforward pattern—creates and starts actor from machine logic:

```typescript
import { useMachine } from '@xstate/react';
import { toggleMachine } from './machines/toggleMachine';

function Toggle() {
  const [snapshot, send, actorRef] = useMachine(toggleMachine);
  
  return (
    <div>
      <p>Current state: {snapshot.value}</p>
      <p>Count: {snapshot.context.count}</p>
      <button onClick={() => send({ type: 'TOGGLE' })}>
        {snapshot.matches('inactive') ? 'Turn On' : 'Turn Off'}
      </button>
    </div>
  );
}
```

**Caveat**: Re-renders on every state change. Fine for simple components; problematic for complex machines with frequent transitions.

### useActorRef + useSelector: Performance Optimization

Separate actor reference from state subscriptions for selective re-renders:

```typescript
import { useActorRef, useSelector } from '@xstate/react';
import { complexMachine } from './machines/complexMachine';

// Define selectors OUTSIDE component to prevent recreation
const selectCount = (snapshot) => snapshot.context.count;
const selectIsLoading = (snapshot) => snapshot.matches('loading');
const selectUser = (snapshot) => snapshot.context.user;
const selectError = (snapshot) => snapshot.context.error?.message;

function Dashboard() {
  const actorRef = useActorRef(complexMachine);
  
  // Each selector causes re-render ONLY when its value changes
  const count = useSelector(actorRef, selectCount);
  const isLoading = useSelector(actorRef, selectIsLoading);
  const user = useSelector(actorRef, selectUser);
  const error = useSelector(actorRef, selectError);
  
  return (
    <div>
      <header>
        <span>Welcome, {user?.name}</span>
        <span>Actions: {count}</span>
      </header>
      
      {isLoading && <LoadingSpinner />}
      {error && <ErrorBanner message={error} />}
      
      <button onClick={() => actorRef.send({ type: 'INCREMENT' })}>
        Do Action
      </button>
    </div>
  );
}
```

### Comparison selectors for complex values

```typescript
import { shallowEqual } from '@xstate/react';

// For arrays/objects, use comparison function
const selectTodos = (snapshot) => snapshot.context.todos;

function TodoList() {
  const actorRef = useActorRef(todoMachine);
  const todos = useSelector(actorRef, selectTodos, shallowEqual);
  
  return (
    <ul>
      {todos.map(todo => <TodoItem key={todo.id} todo={todo} />)}
    </ul>
  );
}
```

### createActorContext: Global State Without Prop Drilling

For application-wide state machines:

```typescript
import { createActorContext } from '@xstate/react';
import { appMachine } from './machines/appMachine';

// Create context outside components
export const AppMachineContext = createActorContext(appMachine);

// Provider wraps app
function App() {
  return (
    <AppMachineContext.Provider>
      <Header />
      <MainContent />
      <Footer />
    </AppMachineContext.Provider>
  );
}

// Any descendant accesses machine
function Header() {
  const user = AppMachineContext.useSelector(s => s.context.user);
  const actorRef = AppMachineContext.useActorRef();
  
  return (
    <header>
      <span>{user?.name}</span>
      <button onClick={() => actorRef.send({ type: 'LOGOUT' })}>
        Logout
      </button>
    </header>
  );
}

function MainContent() {
  const isAuthenticated = AppMachineContext.useSelector(
    s => s.matches('authenticated')
  );
  
  return isAuthenticated ? <Dashboard /> : <LoginForm />;
}
```

### Provider with initial state or input

```typescript
function App() {
  return (
    <AppMachineContext.Provider
      options={{
        input: { userId: 'user-123' },
        // Or restore from snapshot:
        // snapshot: JSON.parse(localStorage.getItem('appState'))
      }}
    >
      <MainContent />
    </AppMachineContext.Provider>
  );
}
```

## Side Effects: Actions vs Invoked Actors

### Actions (Fire-and-Forget)

Use for instant operations with no result handling:

```typescript
const machine = setup({
  actions: {
    // Logging
    logTransition: ({ event }) => {
      console.log('Transition:', event.type);
    },
    
    // Analytics
    trackEvent: ({ context, event }) => {
      analytics.track(event.type, { userId: context.user?.id });
    },
    
    // DOM manipulation (rare, prefer React)
    focusInput: () => {
      document.getElementById('search-input')?.focus();
    },
    
    // Context updates
    updateCount: assign({
      count: ({ context }) => context.count + 1
    })
  }
}).createMachine({
  states: {
    idle: {
      entry: 'logTransition',
      on: {
        SEARCH: {
          target: 'searching',
          actions: ['trackEvent', 'updateCount']
        }
      }
    }
  }
});
```

### Invoked Actors (Managed Lifecycle)

Use for async operations with results, errors, and cleanup:

```typescript
const searchMachine = setup({
  actors: {
    searchAPI: fromPromise(async ({ input, signal }) => {
      const response = await fetch(
        `/api/search?q=${encodeURIComponent(input.query)}`,
        { signal } // Automatic abort on state exit
      );
      if (!response.ok) throw new Error('Search failed');
      return response.json();
    })
  }
}).createMachine({
  initial: 'idle',
  context: { query: '', results: [], error: null },
  states: {
    idle: {
      on: { 
        SEARCH: {
          target: 'searching',
          actions: assign({ query: ({ event }) => event.query })
        }
      }
    },
    searching: {
      invoke: {
        src: 'searchAPI',
        input: ({ context }) => ({ query: context.query }),
        onDone: {
          target: 'success',
          actions: assign({ 
            results: ({ event }) => event.output,
            error: null
          })
        },
        onError: {
          target: 'failure',
          actions: assign({ 
            error: ({ event }) => event.error.message 
          })
        }
      },
      on: {
        CANCEL: 'idle' // Exiting state aborts the fetch
      }
    },
    success: {
      on: { SEARCH: 'searching', CLEAR: 'idle' }
    },
    failure: {
      on: { RETRY: 'searching', CLEAR: 'idle' }
    }
  }
});
```

## Common UI Patterns

### Multi-Step Form with Validation

```typescript
const signUpMachine = setup({
  types: {
    context: {} as {
      step: number;
      name: string;
      email: string;
      password: string;
      plan: 'free' | 'pro' | 'enterprise';
      errors: Record<string, string>;
    }
  },
  guards: {
    hasValidName: ({ context }) => context.name.length >= 2,
    hasValidEmail: ({ context }) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(context.email),
    hasValidPassword: ({ context }) => context.password.length >= 8,
    hasSelectedPlan: ({ context }) => !!context.plan
  },
  actors: {
    submitForm: fromPromise(async ({ input }) => {
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input)
      });
      if (!response.ok) throw new Error('Signup failed');
      return response.json();
    })
  }
}).createMachine({
  id: 'signUp',
  initial: 'personalInfo',
  context: {
    step: 1,
    name: '',
    email: '',
    password: '',
    plan: 'free',
    errors: {}
  },
  states: {
    personalInfo: {
      on: {
        UPDATE_NAME: { actions: assign({ name: ({ event }) => event.value }) },
        UPDATE_EMAIL: { actions: assign({ email: ({ event }) => event.value }) },
        NEXT: [
          { 
            target: 'credentials',
            guard: 'hasValidName',
            actions: assign({ step: 2 })
          },
          { 
            actions: assign({ 
              errors: { name: 'Name must be at least 2 characters' } 
            })
          }
        ]
      }
    },
    credentials: {
      on: {
        UPDATE_PASSWORD: { actions: assign({ password: ({ event }) => event.value }) },
        BACK: { target: 'personalInfo', actions: assign({ step: 1 }) },
        NEXT: [
          {
            target: 'planSelection',
            guard: 'hasValidPassword',
            actions: assign({ step: 3 })
          },
          {
            actions: assign({
              errors: { password: 'Password must be at least 8 characters' }
            })
          }
        ]
      }
    },
    planSelection: {
      on: {
        SELECT_PLAN: { actions: assign({ plan: ({ event }) => event.plan }) },
        BACK: { target: 'credentials', actions: assign({ step: 2 }) },
        NEXT: { target: 'confirmation', actions: assign({ step: 4 }) }
      }
    },
    confirmation: {
      on: {
        BACK: { target: 'planSelection', actions: assign({ step: 3 }) },
        SUBMIT: 'submitting'
      }
    },
    submitting: {
      invoke: {
        src: 'submitForm',
        input: ({ context }) => ({
          name: context.name,
          email: context.email,
          password: context.password,
          plan: context.plan
        }),
        onDone: 'success',
        onError: {
          target: 'confirmation',
          actions: assign({
            errors: ({ event }) => ({ submit: event.error.message })
          })
        }
      }
    },
    success: { type: 'final' }
  }
});
```

### React component for form

```typescript
function SignUpForm() {
  const [snapshot, send] = useMachine(signUpMachine);
  const { step, name, email, password, plan, errors } = snapshot.context;
  
  return (
    <div className="signup-form">
      <ProgressIndicator currentStep={step} totalSteps={4} />
      
      {snapshot.matches('personalInfo') && (
        <div>
          <input
            value={name}
            onChange={(e) => send({ type: 'UPDATE_NAME', value: e.target.value })}
            placeholder="Name"
          />
          {errors.name && <span className="error">{errors.name}</span>}
          <button onClick={() => send({ type: 'NEXT' })}>Next</button>
        </div>
      )}
      
      {snapshot.matches('credentials') && (
        <div>
          <input
            type="password"
            value={password}
            onChange={(e) => send({ type: 'UPDATE_PASSWORD', value: e.target.value })}
            placeholder="Password"
          />
          {errors.password && <span className="error">{errors.password}</span>}
          <button onClick={() => send({ type: 'BACK' })}>Back</button>
          <button onClick={() => send({ type: 'NEXT' })}>Next</button>
        </div>
      )}
      
      {snapshot.matches('submitting') && <LoadingSpinner />}
      
      {snapshot.matches('success') && (
        <div className="success">
          <h2>Welcome!</h2>
          <p>Your account has been created.</p>
        </div>
      )}
    </div>
  );
}
```

### Modal with Animation States

```typescript
const modalMachine = createMachine({
  id: 'modal',
  initial: 'closed',
  states: {
    closed: {
      on: { OPEN: 'opening' }
    },
    opening: {
      after: { 300: 'open' }
    },
    open: {
      on: { CLOSE: 'closing' }
    },
    closing: {
      after: { 300: 'closed' }
    }
  }
});

function Modal({ children }) {
  const [snapshot, send] = useMachine(modalMachine);
  
  // Don't render when fully closed
  if (snapshot.matches('closed')) return null;
  
  const animationClass = snapshot.matches('opening') 
    ? 'modal-enter' 
    : snapshot.matches('closing') 
      ? 'modal-exit' 
      : 'modal-visible';
  
  return (
    <div className={`modal-overlay ${animationClass}`}>
      <div className="modal-content">
        <button 
          className="modal-close" 
          onClick={() => send({ type: 'CLOSE' })}
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
}
```

### Debounced Search with Cancel

```typescript
const searchMachine = setup({
  actors: {
    search: fromPromise(async ({ input, signal }) => {
      const res = await fetch(`/api/search?q=${input.query}`, { signal });
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
        300: 'searching' // Wait 300ms before searching
      },
      on: {
        TYPE: {
          target: 'debouncing', // Restart debounce
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
        },
        onError: 'idle'
      },
      on: {
        TYPE: {
          target: 'debouncing', // Cancel current, start new
          actions: assign({ query: ({ event }) => event.value })
        }
      }
    }
  }
});
```

## Integrating with External State

### React Query / TanStack Query

State machines handle UI state; React Query handles server state:

```typescript
function UserProfile() {
  // Server state via React Query
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId)
  });
  
  // UI state via state machine
  const [snapshot, send] = useMachine(profileUIMachine);
  
  return (
    <div>
      {isLoading && <Skeleton />}
      {error && <ErrorMessage error={error} />}
      {user && (
        <>
          <UserCard user={user} />
          {snapshot.matches('editing') && (
            <EditForm 
              user={user}
              onSave={() => send({ type: 'SAVE' })}
              onCancel={() => send({ type: 'CANCEL' })}
            />
          )}
        </>
      )}
    </div>
  );
}
```

### Zustand for simple global state

```typescript
import { create } from 'zustand';
import { createActorContext } from '@xstate/react';

// Zustand for simple preferences
const usePreferences = create((set) => ({
  theme: 'dark',
  setTheme: (theme) => set({ theme })
}));

// XState for complex workflows
const WorkflowContext = createActorContext(workflowMachine);

function App() {
  const theme = usePreferences(s => s.theme);
  
  return (
    <div className={theme}>
      <WorkflowContext.Provider>
        <MainContent />
      </WorkflowContext.Provider>
    </div>
  );
}
```
