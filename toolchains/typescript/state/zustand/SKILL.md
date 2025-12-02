---
name: zustand
description: Minimal, unopinionated state management library for React with simple hook-based API, no providers, and minimal boilerplate for global state without Redux complexity.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  full_content: true
  token_estimates:
    entry: 70
    full: 4500
---

# Zustand State Management

## Summary
Zustand is a minimal, unopinionated state management library for React. No providers, no boilerplate—just a simple hook-based API that feels natural in React applications.

## When to Use
- React apps needing global state without Redux complexity
- Projects wanting minimal boilerplate and bundle size
- Teams preferring direct state mutations over reducers
- SSR applications (Next.js) requiring flexible state hydration
- Migrating from Redux/Context API to simpler solution

## Quick Start

```bash
npm install zustand
```

```typescript
// stores/useCounterStore.ts
import { create } from 'zustand'

interface CounterState {
  count: number
  increment: () => void
  decrement: () => void
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}))

// components/Counter.tsx
import { useCounterStore } from '@/stores/useCounterStore'

export function Counter() {
  const { count, increment, decrement } = useCounterStore()

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  )
}
```

---

# Complete Zustand Guide

## Core Concepts

### Store Creation

```typescript
import { create } from 'zustand'

// Basic store
interface BearState {
  bears: number
  addBear: () => void
}

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  addBear: () => set((state) => ({ bears: state.bears + 1 })),
}))

// Store with get access
const useStore = create<State>((set, get) => ({
  count: 0,
  increment: () => {
    const currentCount = get().count
    set({ count: currentCount + 1 })
  },
}))
```

### State Access Patterns

```typescript
// Select entire store (re-renders on any change)
const state = useStore()

// Select specific fields (re-renders only when these change)
const bears = useStore((state) => state.bears)
const addBear = useStore((state) => state.addBear)

// Destructure with selector
const { bears, addBear } = useStore((state) => ({
  bears: state.bears,
  addBear: state.addBear,
}))

// Multiple selectors
const bears = useStore((state) => state.bears)
const fish = useStore((state) => state.fish)
```

### Mutations

```typescript
interface TodoState {
  todos: Todo[]
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
  removeTodo: (id: string) => void
}

const useTodoStore = create<TodoState>((set) => ({
  todos: [],

  // Add item
  addTodo: (text) => set((state) => ({
    todos: [...state.todos, { id: nanoid(), text, completed: false }]
  })),

  // Update item
  toggleTodo: (id) => set((state) => ({
    todos: state.todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    )
  })),

  // Remove item
  removeTodo: (id) => set((state) => ({
    todos: state.todos.filter(todo => todo.id !== id)
  })),
}))
```

## React Integration

### useStore Hook

```typescript
function BearCounter() {
  // Re-renders when bears changes
  const bears = useBearStore((state) => state.bears)
  return <h1>{bears} bears around here...</h1>
}

function Controls() {
  // Doesn't re-render when bears changes
  const addBear = useBearStore((state) => state.addBear)
  return <button onClick={addBear}>Add bear</button>
}
```

### Shallow Comparison

```typescript
import { shallow } from 'zustand/shallow'

// Prevent re-renders when object identity changes but values don't
const { nuts, honey } = useBearStore(
  (state) => ({ nuts: state.nuts, honey: state.honey }),
  shallow
)

// Custom equality function
const treats = useBearStore(
  (state) => state.treats,
  (prev, next) => prev.length === next.length
)
```

### Outside React Components

```typescript
// Read state
const count = useStore.getState().count

// Subscribe to changes
const unsubscribe = useStore.subscribe(
  (state) => console.log('Count changed:', state.count)
)

// Update state
useStore.setState({ count: 42 })

// Update with function
useStore.setState((state) => ({ count: state.count + 1 }))
```

## TypeScript Patterns

### Typed Store Creation

```typescript
interface UserState {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
}

const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}))

// Type inference works automatically
const user = useUserStore((state) => state.user) // User | null
```

### Store Type Inference

```typescript
// Extract store type
type UserStoreState = ReturnType<typeof useUserStore.getState>

// Selector type helper
type Selector<T> = (state: UserState) => T

const selectUsername: Selector<string | undefined> = (state) =>
  state.user?.name
```

### Combining Multiple Stores

```typescript
// Type-safe store combination
function useHybridStore<T, U>(
  selector1: (state: State1) => T,
  selector2: (state: State2) => U
): [T, U] {
  return [
    useStore1(selector1),
    useStore2(selector2),
  ]
}

const [user, theme] = useHybridStore(
  (s) => s.user,
  (s) => s.theme
)
```

## Slices Pattern

### Creating Slices

```typescript
// authSlice.ts
export interface AuthSlice {
  user: User | null
  login: (credentials: Credentials) => Promise<void>
  logout: () => void
}

export const createAuthSlice: StateCreator<
  AuthSlice & TodoSlice,
  [],
  [],
  AuthSlice
> = (set) => ({
  user: null,
  login: async (credentials) => {
    const user = await api.login(credentials)
    set({ user })
  },
  logout: () => set({ user: null }),
})

// todoSlice.ts
export interface TodoSlice {
  todos: Todo[]
  addTodo: (text: string) => void
}

export const createTodoSlice: StateCreator<
  AuthSlice & TodoSlice,
  [],
  [],
  TodoSlice
> = (set) => ({
  todos: [],
  addTodo: (text) => set((state) => ({
    todos: [...state.todos, { id: nanoid(), text, completed: false }]
  })),
})

// store.ts
import { create } from 'zustand'
import { createAuthSlice, AuthSlice } from './authSlice'
import { createTodoSlice, TodoSlice } from './todoSlice'

export const useStore = create<AuthSlice & TodoSlice>()((...a) => ({
  ...createAuthSlice(...a),
  ...createTodoSlice(...a),
}))
```

### Cross-Slice Communication

```typescript
export const createTodoSlice: StateCreator<
  AuthSlice & TodoSlice,
  [],
  [],
  TodoSlice
> = (set, get) => ({
  todos: [],
  addTodo: (text) => {
    // Access other slice's state
    const user = get().user
    if (!user) throw new Error('Not authenticated')

    set((state) => ({
      todos: [...state.todos, {
        id: nanoid(),
        text,
        userId: user.id,
        completed: false
      }]
    }))
  },
})
```

## Middleware

### Persist Middleware

```typescript
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface PreferencesState {
  theme: 'light' | 'dark'
  language: string
  setTheme: (theme: 'light' | 'dark') => void
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'preferences-storage', // localStorage key
      storage: createJSONStorage(() => localStorage),

      // Partial persistence
      partialize: (state) => ({ theme: state.theme }),

      // Migration between versions
      version: 1,
      migrate: (persistedState: any, version: number) => {
        if (version === 0) {
          // Migrate from v0 to v1
          persistedState.language = 'en'
        }
        return persistedState as PreferencesState
      },
    }
  )
)

// Custom storage (e.g., AsyncStorage for React Native)
const customStorage = {
  getItem: async (name: string) => {
    const value = await AsyncStorage.getItem(name)
    return value ?? null
  },
  setItem: async (name: string, value: string) => {
    await AsyncStorage.setItem(name, value)
  },
  removeItem: async (name: string) => {
    await AsyncStorage.removeItem(name)
  },
}

const useStore = create(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => customStorage)
    }
  )
)
```

### DevTools Middleware

```typescript
import { devtools } from 'zustand/middleware'

interface CounterState {
  count: number
  increment: () => void
}

const useCounterStore = create<CounterState>()(
  devtools(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 }), false, 'increment'),
    }),
    {
      name: 'CounterStore',
      enabled: process.env.NODE_ENV === 'development'
    }
  )
)

// Action names in Redux DevTools
set({ count: 42 }, false, 'setCount')
set((state) => ({ count: state.count + 1 }), false, { type: 'increment', amount: 1 })
```

### Immer Middleware

```typescript
import { immer } from 'zustand/middleware/immer'

interface TodoState {
  todos: Todo[]
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
}

const useTodoStore = create<TodoState>()(
  immer((set) => ({
    todos: [],

    // Mutate state directly with Immer
    addTodo: (text) => set((state) => {
      state.todos.push({ id: nanoid(), text, completed: false })
    }),

    toggleTodo: (id) => set((state) => {
      const todo = state.todos.find(t => t.id === id)
      if (todo) todo.completed = !todo.completed
    }),
  }))
)
```

### Combining Middleware

```typescript
const useStore = create<State>()(
  devtools(
    persist(
      immer((set) => ({
        // Store implementation
      })),
      { name: 'app-storage' }
    ),
    { name: 'AppStore' }
  )
)
```

## Async Actions & API Integration

### Basic Async Actions

```typescript
interface UserState {
  users: User[]
  loading: boolean
  error: string | null
  fetchUsers: () => Promise<void>
}

const useUserStore = create<UserState>((set) => ({
  users: [],
  loading: false,
  error: null,

  fetchUsers: async () => {
    set({ loading: true, error: null })
    try {
      const users = await api.getUsers()
      set({ users, loading: false })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },
}))
```

### Optimistic Updates

```typescript
interface TodoState {
  todos: Todo[]
  addTodo: (text: string) => Promise<void>
}

const useTodoStore = create<TodoState>((set, get) => ({
  todos: [],

  addTodo: async (text) => {
    const tempId = `temp-${Date.now()}`
    const optimisticTodo = { id: tempId, text, completed: false }

    // Add optimistically
    set((state) => ({ todos: [...state.todos, optimisticTodo] }))

    try {
      const savedTodo = await api.createTodo(text)

      // Replace temp with real todo
      set((state) => ({
        todos: state.todos.map(t =>
          t.id === tempId ? savedTodo : t
        )
      }))
    } catch (error) {
      // Rollback on error
      set((state) => ({
        todos: state.todos.filter(t => t.id !== tempId)
      }))
      throw error
    }
  },
}))
```

### Request Deduplication

```typescript
interface DataState {
  data: Data | null
  loading: boolean
  fetchData: () => Promise<void>
}

let currentRequest: Promise<void> | null = null

const useDataStore = create<DataState>((set) => ({
  data: null,
  loading: false,

  fetchData: async () => {
    // Return existing request if in progress
    if (currentRequest) return currentRequest

    set({ loading: true })

    currentRequest = api.getData()
      .then((data) => {
        set({ data, loading: false })
      })
      .catch((error) => {
        set({ loading: false })
        throw error
      })
      .finally(() => {
        currentRequest = null
      })

    return currentRequest
  },
}))
```

## Computed Values (Selectors)

### Basic Selectors

```typescript
interface TodoState {
  todos: Todo[]
}

// Memoized with useCallback or outside component
const selectCompletedCount = (state: TodoState) =>
  state.todos.filter(t => t.completed).length

const selectActiveCount = (state: TodoState) =>
  state.todos.filter(t => !t.completed).length

function TodoStats() {
  const completedCount = useTodoStore(selectCompletedCount)
  const activeCount = useTodoStore(selectActiveCount)

  return <div>{completedCount} / {activeCount + completedCount}</div>
}
```

### Derived State in Store

```typescript
interface TodoState {
  todos: Todo[]
  get completed(): Todo[]
  get active(): Todo[]
  get stats(): { total: number; completed: number; active: number }
}

const useTodoStore = create<TodoState>((set, get) => ({
  todos: [],

  get completed() {
    return get().todos.filter(t => t.completed)
  },

  get active() {
    return get().todos.filter(t => !t.completed)
  },

  get stats() {
    const todos = get().todos
    return {
      total: todos.length,
      completed: todos.filter(t => t.completed).length,
      active: todos.filter(t => !t.completed).length,
    }
  },
}))

// Usage
const stats = useTodoStore((state) => state.stats)
```

### Parameterized Selectors

```typescript
// Create selector factory
const selectTodoById = (id: string) => (state: TodoState) =>
  state.todos.find(t => t.id === id)

function TodoItem({ id }: { id: string }) {
  const todo = useTodoStore(selectTodoById(id))
  return <div>{todo?.text}</div>
}
```

## Performance Optimization

### Subscription Patterns

```typescript
// Subscribe to specific state changes
useEffect(() => {
  const unsubscribe = useTodoStore.subscribe(
    (state) => state.todos,
    (todos) => {
      console.log('Todos changed:', todos)
    }
  )

  return unsubscribe
}, [])

// Subscribe with selector and equality
const unsubscribe = useTodoStore.subscribe(
  (state) => state.todos.length,
  (length) => console.log('Todo count:', length),
  { equalityFn: (a, b) => a === b }
)
```

### Transient Updates

```typescript
// Updates that don't trigger subscribers
interface ScrubbingState {
  position: number
  updatePosition: (pos: number) => void
}

const useScrubbingStore = create<ScrubbingState>((set) => ({
  position: 0,
  updatePosition: (pos) => set({ position: pos }, true), // true = transient
}))

// Subscribers won't be notified
useScrubbingStore.getState().updatePosition(50)
```

### Batching Updates

```typescript
const useTodoStore = create<TodoState>((set) => ({
  todos: [],

  batchUpdate: (updates: Partial<TodoState>[]) => {
    // Single re-render for multiple updates
    set((state) => {
      let newState = { ...state }
      updates.forEach(update => {
        newState = { ...newState, ...update }
      })
      return newState
    })
  },
}))
```

## Testing Strategies

### Mock Stores

```typescript
// __tests__/Counter.test.tsx
import { create } from 'zustand'
import { render, screen, fireEvent } from '@testing-library/react'
import { Counter } from '@/components/Counter'
import { useCounterStore } from '@/stores/useCounterStore'

// Mock the store
jest.mock('@/stores/useCounterStore')

describe('Counter', () => {
  beforeEach(() => {
    const mockStore = create<CounterState>((set) => ({
      count: 0,
      increment: jest.fn(() => set((state) => ({ count: state.count + 1 }))),
      decrement: jest.fn(),
    }))

    useCounterStore.mockImplementation(mockStore)
  })

  it('increments count', () => {
    render(<Counter />)
    fireEvent.click(screen.getByText('+'))
    expect(screen.getByText('Count: 1')).toBeInTheDocument()
  })
})
```

### Test Utilities

```typescript
// test-utils.ts
import { create } from 'zustand'

export function createTestStore<T>(initialState: Partial<T>) {
  return create<T>(() => initialState as T)
}

// Usage in tests
const testStore = createTestStore<TodoState>({
  todos: [
    { id: '1', text: 'Test todo', completed: false }
  ]
})
```

### Reset Store Between Tests

```typescript
// stores/useCounterStore.ts
const initialState = { count: 0 }

export const useCounterStore = create<CounterState>((set) => ({
  ...initialState,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set(initialState),
}))

// __tests__/Counter.test.tsx
afterEach(() => {
  useCounterStore.getState().reset()
})
```

## Migration Guides

### From Redux

```typescript
// Redux
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1 },
    decrement: (state) => { state.value -= 1 },
  },
})

// Zustand equivalent
const useCounterStore = create<CounterState>((set) => ({
  value: 0,
  increment: () => set((state) => ({ value: state.value + 1 })),
  decrement: () => set((state) => ({ value: state.value - 1 })),
}))

// Redux usage
const dispatch = useDispatch()
const value = useSelector((state) => state.counter.value)
dispatch(increment())

// Zustand usage
const { value, increment } = useCounterStore()
increment()
```

### From Context API

```typescript
// Context API
const ThemeContext = createContext<ThemeContextType>(null!)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)

// Zustand equivalent (no provider needed!)
export const useThemeStore = create<ThemeState>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}))

// Usage is simpler
const { theme, setTheme } = useThemeStore()
```

## Next.js Integration

### App Router (RSC)

```typescript
// stores/useCartStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useCartStore = create<CartState>()(
  persist(
    (set) => ({
      items: [],
      addItem: (item) => set((state) => ({
        items: [...state.items, item]
      })),
    }),
    {
      name: 'cart-storage',
      // Skip persistence on server
      skipHydration: true,
    }
  )
)

// components/Cart.tsx (Client Component)
'use client'

import { useCartStore } from '@/stores/useCartStore'
import { useEffect } from 'react'

export function Cart() {
  const { items, addItem } = useCartStore()

  // Hydrate persisted state
  useEffect(() => {
    useCartStore.persist.rehydrate()
  }, [])

  return <div>{items.length} items</div>
}
```

### Server Actions Integration

```typescript
// actions/cart.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function syncCartToServer(items: CartItem[]) {
  await db.cart.upsert({
    where: { userId: 'current-user' },
    update: { items },
    create: { userId: 'current-user', items },
  })

  revalidatePath('/cart')
}

// stores/useCartStore.ts
export const useCartStore = create<CartState>((set) => ({
  items: [],
  addItem: async (item) => {
    set((state) => ({ items: [...state.items, item] }))

    // Sync to server
    const items = useCartStore.getState().items
    await syncCartToServer(items)
  },
}))
```

### SSR Hydration

```typescript
// app/layout.tsx
import { CartStoreProvider } from '@/providers/CartStoreProvider'

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html>
      <body>
        <CartStoreProvider>
          {children}
        </CartStoreProvider>
      </body>
    </html>
  )
}

// providers/CartStoreProvider.tsx
'use client'

import { useRef } from 'react'
import { useCartStore } from '@/stores/useCartStore'

export function CartStoreProvider({ children }: { children: ReactNode }) {
  const initialized = useRef(false)

  if (!initialized.current) {
    // Initialize with server data if needed
    useCartStore.setState({ items: [] })
    initialized.current = true
  }

  return <>{children}</>
}
```

## Best Practices

### Store Organization

```typescript
// ✅ Good: Single responsibility stores
const useAuthStore = create<AuthState>(...)
const useTodoStore = create<TodoState>(...)
const useUIStore = create<UIState>(...)

// ❌ Bad: God store
const useAppStore = create<AppState>(...)
```

### Action Naming

```typescript
// ✅ Good: Clear, verb-based actions
const useStore = create((set) => ({
  addTodo: (text) => set(...),
  removeTodo: (id) => set(...),
  toggleTodo: (id) => set(...),
}))

// ❌ Bad: Vague or noun-based
const useStore = create((set) => ({
  todo: (text) => set(...),  // What does this do?
  update: (id) => set(...),  // Update what?
}))
```

### Selector Optimization

```typescript
// ✅ Good: Specific selectors
const user = useStore((state) => state.user)
const theme = useStore((state) => state.theme)

// ❌ Bad: Selecting entire store
const state = useStore()  // Re-renders on any change
```

### Error Handling

```typescript
// ✅ Good: Explicit error state
interface State {
  data: Data | null
  loading: boolean
  error: Error | null
  fetchData: () => Promise<void>
}

// ❌ Bad: Silent failures
const fetchData = async () => {
  try {
    const data = await api.getData()
    set({ data })
  } catch (error) {
    // Error silently ignored
  }
}
```

## Common Patterns

### Loading States

```typescript
interface ResourceState<T> {
  data: T | null
  loading: boolean
  error: Error | null
  status: 'idle' | 'loading' | 'success' | 'error'
}

function createResourceStore<T>() {
  return create<ResourceState<T>>((set) => ({
    data: null,
    loading: false,
    error: null,
    status: 'idle',

    fetch: async () => {
      set({ loading: true, status: 'loading', error: null })
      try {
        const data = await fetchData()
        set({ data, loading: false, status: 'success' })
      } catch (error) {
        set({ error, loading: false, status: 'error' })
      }
    },
  }))
}
```

### Undo/Redo

```typescript
interface HistoryState<T> {
  past: T[]
  present: T
  future: T[]
  set: (state: T) => void
  undo: () => void
  redo: () => void
}

function createHistoryStore<T>(initialState: T) {
  return create<HistoryState<T>>((set) => ({
    past: [],
    present: initialState,
    future: [],

    set: (newPresent) => set((state) => ({
      past: [...state.past, state.present],
      present: newPresent,
      future: [],
    })),

    undo: () => set((state) => {
      if (state.past.length === 0) return state

      const previous = state.past[state.past.length - 1]
      const newPast = state.past.slice(0, -1)

      return {
        past: newPast,
        present: previous,
        future: [state.present, ...state.future],
      }
    }),

    redo: () => set((state) => {
      if (state.future.length === 0) return state

      const next = state.future[0]
      const newFuture = state.future.slice(1)

      return {
        past: [...state.past, state.present],
        present: next,
        future: newFuture,
      }
    }),
  }))
}
```

## Comparison with Alternatives

### vs Redux

**Zustand Advantages:**
- No boilerplate (no actions, reducers, dispatch)
- No provider needed
- Smaller bundle size (~1kb vs ~20kb)
- Simpler async handling
- TypeScript inference works out of the box

**Redux Advantages:**
- Time-travel debugging
- Larger ecosystem and middleware
- Strict unidirectional data flow
- Better for very large applications

### vs Context API

**Zustand Advantages:**
- No provider hell
- Better performance (no re-render entire subtree)
- Simpler API
- Built-in middleware

**Context Advantages:**
- Built into React (no dependency)
- Better for component-local state
- Explicit component boundaries

### vs Jotai

**Zustand Advantages:**
- More traditional store-based approach
- Better for complex state logic
- Easier migration from Redux

**Jotai Advantages:**
- Atomic state management
- Better code splitting
- More React-like (atom-based)
- Suspense support out of the box

## Resources

- [Official Documentation](https://docs.pmnd.rs/zustand)
- [GitHub Repository](https://github.com/pmndrs/zustand)
- [TypeScript Guide](https://docs.pmnd.rs/zustand/guides/typescript)
- [Middleware Reference](https://docs.pmnd.rs/zustand/integrations/persisting-store-data)

## Related Skills

When using Zustand, these skills enhance your workflow:
- **react**: React integration patterns and hooks for Zustand stores
- **tanstack-query**: Server-state management (use with Zustand for client state)
- **nextjs**: Zustand with Next.js App Router and Client Components
- **test-driven-development**: Testing Zustand stores, actions, and selectors

[Full documentation available in these skills if deployed in your bundle]
