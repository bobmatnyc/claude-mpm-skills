---
name: tanstack-query
description: TanStack Query (React Query) for asynchronous server-state management with automatic caching, background refetching, optimistic updates, and pagination in React applications.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  intermediate:
    - core_concepts
    - queries
    - mutations
    - cache_management
  advanced:
    - optimistic_updates
    - pagination
    - ssr_hydration
    - integration_patterns
    - performance
---

# TanStack Query (React Query) Skill

## Summary

TanStack Query (formerly React Query) is a powerful asynchronous state management library for React that handles server-state fetching, caching, synchronization, and updates. It eliminates the need for manual data fetching boilerplate and provides built-in features like background refetching, optimistic updates, pagination, and intelligent cache management.

## When to Use

**Use TanStack Query when:**
- Fetching data from REST APIs, GraphQL, or tRPC endpoints
- Need automatic background refetching and cache invalidation
- Building real-time dashboards with polling or websocket data
- Implementing infinite scroll or pagination
- Require optimistic UI updates for mutations
- Managing complex server-state synchronization
- Need offline support with cache persistence
- Building applications with frequent data updates

**TanStack Query excels at:**
- Server-state management (API data, external state)
- Request deduplication and caching
- Stale-while-revalidate patterns
- Loading and error state management
- Prefetching and eager loading
- Parallel and dependent query orchestration

**Avoid TanStack Query for:**
- Pure client-side state (use Zustand, Jotai, or Context)
- Form state management (use React Hook Form, Formik)
- Simple one-time fetches without caching needs

## Quick Start

### Installation

```bash
npm install @tanstack/react-query
# DevTools (optional but recommended)
npm install @tanstack/react-query-devtools
```

### Basic Setup

```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### First Query

```tsx
// components/UserProfile.tsx
import { useQuery } from '@tanstack/react-query';

interface User {
  id: number;
  name: string;
  email: string;
}

function UserProfile({ userId }: { userId: number }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      return response.json() as Promise<User>;
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </div>
  );
}
```

### First Mutation

```tsx
// components/CreateUserForm.tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreateUserForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (newUser: { name: string; email: string }) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newUser),
      });
      return response.json();
    },
    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    mutation.mutate({
      name: formData.get('name') as string,
      email: formData.get('email') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create User'}
      </button>
      {mutation.isError && <p>Error: {mutation.error.message}</p>}
    </form>
  );
}
```

---

## Core Concepts

### Server State vs Client State

**Server State Characteristics:**
- Persisted remotely (database, API, cloud)
- Requires asynchronous APIs for fetching/updating
- Can be out of sync with client
- Can be updated by other users/systems
- Examples: User data, posts, products, settings

**Client State Characteristics:**
- Persisted locally (memory, localStorage)
- Synchronously accessible
- Fully controlled by client
- Examples: UI theme, modal open/closed, form inputs

**TanStack Query manages server state**. Use Zustand/Context for client state.

### Query Keys

Query keys uniquely identify queries and their cached data.

**Key Structure:**
```tsx
// String key (simple)
queryKey: ['todos']

// Array key (recommended for dependencies)
queryKey: ['todo', todoId]
queryKey: ['todos', { status: 'active', page: 1 }]

// Nested arrays (complex hierarchies)
queryKey: ['users', userId, 'posts', { sort: 'date' }]
```

**Key Matching:**
```tsx
// Exact match
queryClient.invalidateQueries({ queryKey: ['todos', 1], exact: true });

// Prefix match (invalidates all matching)
queryClient.invalidateQueries({ queryKey: ['todos'] }); // Matches ['todos', 1], ['todos', 2], etc.

// Predicate match
queryClient.invalidateQueries({
  predicate: (query) => query.queryKey[0] === 'todos' && query.state.data?.status === 'draft'
});
```

**Best Practices:**
- Use arrays with hierarchical structure: `['resource', id, 'subresource']`
- Place variables at the end: `['users', { filter, sort }]`
- Consistent ordering across components
- Use objects for complex parameters

### Query Lifecycle

```
FRESH → STALE → INACTIVE → GARBAGE COLLECTED
  ↓       ↓         ↓              ↓
  0ms   staleTime  no observers  cacheTime
```

**States:**
- **Fresh**: Data is considered up-to-date (within `staleTime`)
- **Stale**: Data might be outdated, will refetch on trigger
- **Inactive**: No components using the query
- **Garbage Collected**: Removed from cache after `cacheTime`

**Configuration:**
```tsx
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: 5 * 60 * 1000,     // 5 minutes (data fresh)
  gcTime: 10 * 60 * 1000,       // 10 minutes (cache retention)
  refetchOnWindowFocus: true,    // Refetch when window regains focus
  refetchOnReconnect: true,      // Refetch when reconnecting
  refetchInterval: 30000,        // Poll every 30 seconds
});
```

### Cache Behavior

**Automatic Caching:**
```tsx
// First component - triggers fetch
function ComponentA() {
  const { data } = useQuery({ queryKey: ['user', 1], queryFn: fetchUser });
  return <div>{data?.name}</div>;
}

// Second component - uses cache instantly
function ComponentB() {
  const { data } = useQuery({ queryKey: ['user', 1], queryFn: fetchUser });
  return <div>{data?.email}</div>; // No second fetch!
}
```

**Stale-While-Revalidate:**
```tsx
// Shows cached data immediately, refetches in background if stale
const { data, isRefetching } = useQuery({
  queryKey: ['posts'],
  queryFn: fetchPosts,
  staleTime: 60000, // Fresh for 1 minute
});

// data available from cache immediately
// isRefetching = true if background refetch happening
```

---

## Queries

### useQuery Hook

**Basic Syntax:**
```tsx
const {
  data,           // Query result
  error,          // Error object if failed
  isLoading,      // First load (no cached data)
  isFetching,     // Any fetch (including background)
  isSuccess,      // Query succeeded
  isError,        // Query failed
  status,         // 'pending' | 'error' | 'success'
  fetchStatus,    // 'fetching' | 'paused' | 'idle'
  refetch,        // Manual refetch function
} = useQuery({
  queryKey: ['key'],
  queryFn: async () => { /* fetch logic */ },
});
```

### Query Function Patterns

**Basic Fetch:**
```tsx
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: async () => {
    const response = await fetch('/api/users');
    if (!response.ok) throw new Error('Network error');
    return response.json();
  },
});
```

**Query Key in Function:**
```tsx
const { data } = useQuery({
  queryKey: ['user', userId],
  queryFn: async ({ queryKey }) => {
    const [_key, userId] = queryKey;
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
  },
});
```

**Abort Signal (Cancellation):**
```tsx
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: async ({ signal }) => {
    const response = await fetch('/api/todos', { signal });
    return response.json();
  },
});
// Automatically cancels on unmount or when query becomes inactive
```

**Axios Pattern:**
```tsx
import axios from 'axios';

const { data } = useQuery({
  queryKey: ['repos', username],
  queryFn: ({ signal }) =>
    axios.get(`/api/repos/${username}`, { signal }).then(res => res.data),
});
```

### Dependent Queries

**Sequential Queries:**
```tsx
// Wait for user before fetching projects
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user!.id),
  enabled: !!user, // Only run when user exists
});
```

**Conditional Queries:**
```tsx
const { data } = useQuery({
  queryKey: ['premium-features', userId],
  queryFn: fetchPremiumFeatures,
  enabled: user?.isPremium === true, // Only fetch for premium users
});
```

### Parallel Queries

**Manual Parallel:**
```tsx
function Dashboard() {
  const users = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
  const posts = useQuery({ queryKey: ['posts'], queryFn: fetchPosts });
  const projects = useQuery({ queryKey: ['projects'], queryFn: fetchProjects });

  if (users.isLoading || posts.isLoading || projects.isLoading) {
    return <Spinner />;
  }

  return <div>/* render dashboard */</div>;
}
```

**useQueries (Dynamic Parallel):**
```tsx
import { useQueries } from '@tanstack/react-query';

function MultiUserProfiles({ userIds }: { userIds: number[] }) {
  const results = useQueries({
    queries: userIds.map(id => ({
      queryKey: ['user', id],
      queryFn: () => fetchUser(id),
      staleTime: 60000,
    })),
  });

  const allLoaded = results.every(r => r.isSuccess);

  if (!allLoaded) return <Spinner />;

  return (
    <div>
      {results.map((result, i) => (
        <UserCard key={userIds[i]} user={result.data} />
      ))}
    </div>
  );
}
```

### Query Placeholders

**Placeholder Data (Instant UI):**
```tsx
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  placeholderData: [], // Show empty array while loading
});

// Dynamic placeholder from cache
const { data } = useQuery({
  queryKey: ['todo', id],
  queryFn: () => fetchTodo(id),
  placeholderData: () => {
    // Use cached list to find placeholder
    return queryClient
      .getQueryData(['todos'])
      ?.find(d => d.id === id);
  },
});
```

**Initial Data (Hydration):**
```tsx
const { data } = useQuery({
  queryKey: ['todo', id],
  queryFn: () => fetchTodo(id),
  initialData: () => {
    return queryClient
      .getQueryData(['todos'])
      ?.find(d => d.id === id);
  },
  initialDataUpdatedAt: () =>
    queryClient.getQueryState(['todos'])?.dataUpdatedAt,
});
```

**Difference:**
- `placeholderData`: Not persisted to cache, purely UI
- `initialData`: Persisted to cache as real data

---

## Mutations

### useMutation Hook

**Basic Mutation:**
```tsx
const mutation = useMutation({
  mutationFn: async (newTodo: Todo) => {
    const response = await fetch('/api/todos', {
      method: 'POST',
      body: JSON.stringify(newTodo),
    });
    return response.json();
  },
  onSuccess: (data) => {
    console.log('Created:', data);
  },
  onError: (error) => {
    console.error('Failed:', error);
  },
});

// Trigger mutation
mutation.mutate({ title: 'New Todo', done: false });

// Async/await variant
try {
  const data = await mutation.mutateAsync(newTodo);
  console.log(data);
} catch (error) {
  console.error(error);
}
```

**Mutation State:**
```tsx
const {
  mutate,          // Trigger function
  mutateAsync,     // Promise variant
  data,            // Result from successful mutation
  error,           // Error from failed mutation
  isPending,       // Mutation in progress
  isSuccess,       // Mutation succeeded
  isError,         // Mutation failed
  reset,           // Reset mutation state
} = useMutation({ /* ... */ });
```

### Cache Invalidation

**Invalidate Queries After Mutation:**
```tsx
const mutation = useMutation({
  mutationFn: createTodo,
  onSuccess: () => {
    // Refetch all 'todos' queries
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

**Multiple Invalidations:**
```tsx
const mutation = useMutation({
  mutationFn: updateUser,
  onSuccess: (data, variables) => {
    // Invalidate multiple query families
    queryClient.invalidateQueries({ queryKey: ['user', variables.id] });
    queryClient.invalidateQueries({ queryKey: ['users'] });
    queryClient.invalidateQueries({ queryKey: ['teams', data.teamId] });
  },
});
```

**Selective Invalidation:**
```tsx
// Only invalidate specific queries
queryClient.invalidateQueries({
  queryKey: ['todos'],
  exact: true, // Only ['todos'], not ['todos', 1]
});

// Predicate-based invalidation
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'todos' &&
    query.state.data?.status === 'draft',
});
```

### Manual Cache Updates

**setQueryData (Direct Update):**
```tsx
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: (updatedTodo) => {
    // Update specific todo in cache
    queryClient.setQueryData(
      ['todo', updatedTodo.id],
      updatedTodo
    );

    // Update todo in list
    queryClient.setQueryData(['todos'], (old: Todo[] = []) =>
      old.map(todo =>
        todo.id === updatedTodo.id ? updatedTodo : todo
      )
    );
  },
});
```

**Immutable Updates:**
```tsx
// Add to list
queryClient.setQueryData(['todos'], (old: Todo[] = []) =>
  [...old, newTodo]
);

// Remove from list
queryClient.setQueryData(['todos'], (old: Todo[] = []) =>
  old.filter(todo => todo.id !== deletedId)
);

// Update in list
queryClient.setQueryData(['todos'], (old: Todo[] = []) =>
  old.map(todo => todo.id === id ? { ...todo, ...updates } : todo)
);
```

---

## Optimistic Updates

### Basic Optimistic Update

```tsx
const mutation = useMutation({
  mutationFn: updateTodo,
  // Before mutation executes
  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // Snapshot previous value
    const previousTodos = queryClient.getQueryData(['todos']);

    // Optimistically update cache
    queryClient.setQueryData(['todos'], (old: Todo[] = []) =>
      old.map(todo => todo.id === newTodo.id ? newTodo : todo)
    );

    // Return context with snapshot
    return { previousTodos };
  },
  // On error, rollback
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context?.previousTodos);
  },
  // Always refetch after success or error
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

### Complex Optimistic Update Pattern

```tsx
interface Todo {
  id: number;
  title: string;
  done: boolean;
}

const useUpdateTodo = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (updatedTodo: Todo) => {
      const response = await fetch(`/api/todos/${updatedTodo.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTodo),
      });
      if (!response.ok) throw new Error('Update failed');
      return response.json();
    },

    onMutate: async (updatedTodo) => {
      // Cancel queries to prevent race conditions
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      await queryClient.cancelQueries({ queryKey: ['todo', updatedTodo.id] });

      // Snapshot current state
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);
      const previousTodo = queryClient.getQueryData<Todo>(['todo', updatedTodo.id]);

      // Optimistically update list
      if (previousTodos) {
        queryClient.setQueryData<Todo[]>(['todos'], (old = []) =>
          old.map(todo => todo.id === updatedTodo.id ? updatedTodo : todo)
        );
      }

      // Optimistically update detail
      queryClient.setQueryData(['todo', updatedTodo.id], updatedTodo);

      return { previousTodos, previousTodo };
    },

    onError: (err, updatedTodo, context) => {
      // Rollback on error
      if (context?.previousTodos) {
        queryClient.setQueryData(['todos'], context.previousTodos);
      }
      if (context?.previousTodo) {
        queryClient.setQueryData(['todo', updatedTodo.id], context.previousTodo);
      }
    },

    onSettled: (data, error, variables) => {
      // Always refetch to ensure sync
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      queryClient.invalidateQueries({ queryKey: ['todo', variables.id] });
    },
  });
};

// Usage
function TodoItem({ todo }: { todo: Todo }) {
  const updateTodo = useUpdateTodo();

  const toggleDone = () => {
    updateTodo.mutate({ ...todo, done: !todo.done });
  };

  return (
    <div>
      <input
        type="checkbox"
        checked={todo.done}
        onChange={toggleDone}
        disabled={updateTodo.isPending}
      />
      {todo.title}
    </div>
  );
}
```

---

## Pagination

### useInfiniteQuery (Infinite Scroll)

**Basic Infinite Query:**
```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

interface PostsResponse {
  posts: Post[];
  nextCursor?: number;
}

function InfinitePosts() {
  const {
    data,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: async ({ pageParam = 0 }) => {
      const response = await fetch(`/api/posts?cursor=${pageParam}`);
      return response.json() as Promise<PostsResponse>;
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: 0,
  });

  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.posts.map(post => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? 'Loading more...'
          : hasNextPage
          ? 'Load More'
          : 'Nothing more to load'}
      </button>
    </div>
  );
}
```

**Bi-directional Pagination:**
```tsx
const {
  data,
  fetchNextPage,
  fetchPreviousPage,
  hasNextPage,
  hasPreviousPage,
} = useInfiniteQuery({
  queryKey: ['posts'],
  queryFn: async ({ pageParam = 0 }) => {
    const response = await fetch(`/api/posts?cursor=${pageParam}`);
    return response.json();
  },
  getNextPageParam: (lastPage) => lastPage.nextCursor,
  getPreviousPageParam: (firstPage) => firstPage.prevCursor,
  initialPageParam: 0,
});
```

**Infinite Scroll with Intersection Observer:**
```tsx
import { useInfiniteQuery } from '@tanstack/react-query';
import { useInView } from 'react-intersection-observer';
import { useEffect } from 'react';

function AutoLoadPosts() {
  const { ref, inView } = useInView();

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: 0,
  });

  // Auto-fetch when sentinel comes into view
  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, fetchNextPage]);

  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.posts.map(post => <PostCard key={post.id} post={post} />)}
        </div>
      ))}

      {/* Sentinel element */}
      <div ref={ref}>
        {isFetchingNextPage && <Spinner />}
      </div>
    </div>
  );
}
```

### Traditional Pagination

**Page-Based Pagination:**
```tsx
function PaginatedPosts() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['posts', page],
    queryFn: () => fetchPosts(page),
    placeholderData: (previousData) => previousData, // Keep previous data while loading
  });

  return (
    <div>
      {isLoading ? (
        <Spinner />
      ) : (
        <div>
          {data.posts.map(post => <PostCard key={post.id} post={post} />)}
        </div>
      )}

      <div>
        <button
          onClick={() => setPage(old => Math.max(old - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page}</span>
        <button
          onClick={() => setPage(old => old + 1)}
          disabled={!data?.hasMore}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

**Prefetch Next Page:**
```tsx
function PaginatedPosts() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);

  const { data } = useQuery({
    queryKey: ['posts', page],
    queryFn: () => fetchPosts(page),
  });

  // Prefetch next page
  useEffect(() => {
    if (data?.hasMore) {
      queryClient.prefetchQuery({
        queryKey: ['posts', page + 1],
        queryFn: () => fetchPosts(page + 1),
      });
    }
  }, [data, page, queryClient]);

  return (
    <div>
      {/* ... */}
    </div>
  );
}
```

---

## Cache Management

### Query Client Methods

**getQueryData (Read Cache):**
```tsx
const todos = queryClient.getQueryData<Todo[]>(['todos']);
const user = queryClient.getQueryData<User>(['user', userId]);
```

**setQueryData (Write Cache):**
```tsx
queryClient.setQueryData(['user', 1], newUser);

// Updater function
queryClient.setQueryData<Todo[]>(['todos'], (old = []) => [...old, newTodo]);
```

**invalidateQueries (Mark Stale + Refetch):**
```tsx
// Invalidate all queries
queryClient.invalidateQueries();

// Invalidate by key prefix
queryClient.invalidateQueries({ queryKey: ['todos'] });

// Exact match only
queryClient.invalidateQueries({ queryKey: ['todos'], exact: true });

// With refetch control
queryClient.invalidateQueries({
  queryKey: ['todos'],
  refetchType: 'active', // 'active' | 'inactive' | 'all' | 'none'
});
```

**refetchQueries (Immediate Refetch):**
```tsx
// Refetch all active queries
await queryClient.refetchQueries();

// Refetch specific queries
await queryClient.refetchQueries({ queryKey: ['todos'] });

// Refetch with filters
await queryClient.refetchQueries({
  queryKey: ['todos'],
  type: 'active', // Only refetch active queries
});
```

**removeQueries (Delete from Cache):**
```tsx
// Remove all queries
queryClient.removeQueries();

// Remove specific
queryClient.removeQueries({ queryKey: ['todos', 1] });

// Remove with predicate
queryClient.removeQueries({
  predicate: (query) =>
    query.queryKey[0] === 'todos' &&
    query.state.data?.isArchived === true,
});
```

**resetQueries (Reset to Initial State):**
```tsx
// Reset all queries
queryClient.resetQueries();

// Reset specific
queryClient.resetQueries({ queryKey: ['todos'] });
```

### Cache Configuration

**Global Defaults:**
```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,           // 1 minute
      gcTime: 5 * 60 * 1000,          // 5 minutes (formerly cacheTime)
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
    mutations: {
      retry: 1,
    },
  },
});
```

**Per-Query Configuration:**
```tsx
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: Infinity,      // Never mark stale
  gcTime: Infinity,         // Never garbage collect
  refetchInterval: 5000,    // Refetch every 5s
  refetchIntervalInBackground: false, // Don't refetch when tab inactive
});
```

### Cache Persistence

**Persist to LocalStorage:**
```tsx
import { QueryClient } from '@tanstack/react-query';
import { persistQueryClient } from '@tanstack/react-query-persist-client';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24 hours
    },
  },
});

const persister = createSyncStoragePersister({
  storage: window.localStorage,
});

persistQueryClient({
  queryClient,
  persister,
  maxAge: 1000 * 60 * 60 * 24, // 24 hours
});
```

**IndexedDB Persistence:**
```tsx
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister';
import { get, set, del } from 'idb-keyval';

const persister = createAsyncStoragePersister({
  storage: {
    getItem: async (key) => await get(key),
    setItem: async (key, value) => await set(key, value),
    removeItem: async (key) => await del(key),
  },
});
```

---

## Error Handling and Retry

### Error Handling

**Query Error Boundaries:**
```tsx
import { QueryErrorResetBoundary } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ error, resetErrorBoundary }) => (
            <div>
              <p>Error: {error.message}</p>
              <button onClick={resetErrorBoundary}>Try again</button>
            </div>
          )}
        >
          <Component />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}

// Component throws errors to boundary
function Component() {
  const { data } = useQuery({
    queryKey: ['user'],
    queryFn: fetchUser,
    throwOnError: true, // Throw errors to error boundary
  });
  return <div>{data.name}</div>;
}
```

**Custom Error Types:**
```tsx
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

const { error } = useQuery({
  queryKey: ['user'],
  queryFn: async () => {
    const response = await fetch('/api/user');
    if (!response.ok) {
      throw new APIError(
        'Failed to fetch user',
        response.status,
        await response.text()
      );
    }
    return response.json();
  },
});

if (error instanceof APIError) {
  if (error.status === 404) return <NotFound />;
  if (error.status === 401) return <Unauthorized />;
}
```

### Retry Logic

**Default Retry:**
```tsx
// Retries 3 times with exponential backoff
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  retry: 3, // Number of retries
  retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

**Conditional Retry:**
```tsx
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  retry: (failureCount, error) => {
    // Don't retry on 404
    if (error instanceof APIError && error.status === 404) {
      return false;
    }
    // Retry up to 3 times for other errors
    return failureCount < 3;
  },
});
```

**Mutation Retry:**
```tsx
useMutation({
  mutationFn: createUser,
  retry: 2, // Retry mutations (use sparingly)
  retryDelay: 1000,
});
```

### Network Status Detection

**Online/Offline Handling:**
```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      networkMode: 'offlineFirst', // 'online' | 'always' | 'offlineFirst'
      refetchOnReconnect: true,
    },
  },
});

// Custom online/offline indicator
function OnlineStatus() {
  const queryClient = useQueryClient();
  const isOnline = useOnlineManager().isOnline();

  useEffect(() => {
    if (isOnline) {
      queryClient.refetchQueries();
    }
  }, [isOnline, queryClient]);

  return isOnline ? <OnlineIcon /> : <OfflineIcon />;
}
```

---

## SSR and Hydration

### Next.js App Router

**Server Component Data Fetching:**
```tsx
// app/users/page.tsx
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { UsersList } from './UsersList';

export default async function UsersPage() {
  const queryClient = new QueryClient();

  // Prefetch on server
  await queryClient.prefetchQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UsersList />
    </HydrationBoundary>
  );
}
```

**Client Component:**
```tsx
// app/users/UsersList.tsx
'use client';

import { useQuery } from '@tanstack/react-query';

export function UsersList() {
  // Uses hydrated data from server
  const { data } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  return (
    <ul>
      {data?.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

### Next.js Pages Router

**getServerSideProps:**
```tsx
import { dehydrate, QueryClient } from '@tanstack/react-query';

export async function getServerSideProps() {
  const queryClient = new QueryClient();

  await queryClient.prefetchQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  return {
    props: {
      dehydratedState: dehydrate(queryClient),
    },
  };
}

function UsersPage() {
  const { data } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  return <div>{/* ... */}</div>;
}

export default UsersPage;
```

**_app.tsx Setup:**
```tsx
// pages/_app.tsx
import { useState } from 'react';
import { QueryClient, QueryClientProvider, HydrationBoundary } from '@tanstack/react-query';

export default function App({ Component, pageProps }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <HydrationBoundary state={pageProps.dehydratedState}>
        <Component {...pageProps} />
      </HydrationBoundary>
    </QueryClientProvider>
  );
}
```

### Streaming SSR

**Suspense Integration:**
```tsx
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: number }) {
  const { data } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  // No loading state needed - Suspense handles it
  return <div>{data.name}</div>;
}

// In parent component
<Suspense fallback={<Spinner />}>
  <UserProfile userId={1} />
</Suspense>
```

---

## Integration Patterns

### tRPC Integration

**Setup:**
```tsx
// utils/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '@/server/routers/_app';

export const trpc = createTRPCReact<AppRouter>();
```

**Provider:**
```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import { trpc } from '@/utils/trpc';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

**Usage:**
```tsx
function UserProfile() {
  // Query
  const { data } = trpc.user.getById.useQuery({ id: 1 });

  // Mutation
  const utils = trpc.useUtils();
  const mutation = trpc.user.create.useMutation({
    onSuccess: () => {
      utils.user.list.invalidate();
    },
  });

  return <div>{data?.name}</div>;
}
```

### REST API with Axios

**API Client:**
```tsx
// lib/api-client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**Query Hooks:**
```tsx
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async ({ signal }) => {
      const { data } = await apiClient.get('/users', { signal });
      return data;
    },
  });
}

export function useUser(id: number) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async ({ signal }) => {
      const { data } = await apiClient.get(`/users/${id}`, { signal });
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newUser: NewUser) =>
      apiClient.post('/users', newUser).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### GraphQL Integration

**Apollo Client Alternative:**
```tsx
import { useQuery } from '@tanstack/react-query';
import { request, gql } from 'graphql-request';

const endpoint = 'https://api.example.com/graphql';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => request(endpoint, GET_USERS),
  });
}

// With variables
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async () => request(endpoint, GET_USER, { id }),
  });
}
```

### Zustand for Global State

**Combined Pattern:**
```tsx
// store/useAuthStore.ts
import { create } from 'zustand';

interface AuthState {
  token: string | null;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  setToken: (token) => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
    set({ token });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null });
  },
}));

// hooks/useAuthenticatedQuery.ts
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/store/useAuthStore';

export function useAuthenticatedQuery() {
  const token = useAuthStore(state => state.token);

  return useQuery({
    queryKey: ['profile', token],
    queryFn: async () => {
      const response = await fetch('/api/profile', {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.json();
    },
    enabled: !!token,
  });
}
```

---

## TypeScript Patterns

### Typed Queries

**Generic Query Hook:**
```tsx
interface User {
  id: number;
  name: string;
  email: string;
}

// Explicit typing
const { data } = useQuery<User, Error>({
  queryKey: ['user', id],
  queryFn: async () => {
    const response = await fetch(`/api/users/${id}`);
    return response.json(); // TypeScript infers return type
  },
});

// data is User | undefined
// error is Error | null
```

**Type-safe Query Keys:**
```tsx
// Define query keys with types
const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: number) => [...userKeys.details(), id] as const,
};

// Usage with full type safety
const { data } = useQuery({
  queryKey: userKeys.detail(userId),
  queryFn: () => fetchUser(userId),
});

// Invalidate with autocomplete
queryClient.invalidateQueries({ queryKey: userKeys.lists() });
```

**Custom Hook with Types:**
```tsx
interface User {
  id: number;
  name: string;
  email: string;
}

interface UseUserOptions {
  enabled?: boolean;
  onSuccess?: (user: User) => void;
}

function useUser(id: number, options?: UseUserOptions) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async (): Promise<User> => {
      const response = await fetch(`/api/users/${id}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      return response.json();
    },
    enabled: options?.enabled,
    // Type-safe callbacks
    onSuccess: options?.onSuccess,
  });
}

// Usage
const { data } = useUser(1, {
  enabled: true,
  onSuccess: (user) => {
    console.log(user.name); // TypeScript knows user is User
  },
});
```

### Typed Mutations

```tsx
interface CreateUserPayload {
  name: string;
  email: string;
}

interface User {
  id: number;
  name: string;
  email: string;
}

function useCreateUser() {
  return useMutation<User, Error, CreateUserPayload>({
    mutationFn: async (payload) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      return response.json();
    },
    onSuccess: (data) => {
      // data is User
      console.log('Created user:', data.name);
    },
    onError: (error) => {
      // error is Error
      console.error('Failed:', error.message);
    },
  });
}

// Usage
const mutation = useCreateUser();
mutation.mutate({ name: 'John', email: 'john@example.com' });
```

### Query Client Typing

```tsx
import { QueryClient } from '@tanstack/react-query';

// Type-safe query client methods
const user = queryClient.getQueryData<User>(['user', 1]);

queryClient.setQueryData<User>(['user', 1], (old) => {
  // old is User | undefined
  if (!old) return old;
  return { ...old, name: 'Updated' };
});

// Type-safe invalidation
queryClient.invalidateQueries<User>({
  queryKey: ['users'],
  predicate: (query) => {
    // query.state.data is User | undefined
    return query.state.data?.isActive === true;
  },
});
```

---

## Testing

### Setup Testing Environment

**Test Utils:**
```tsx
// test/utils.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render } from '@testing-library/react';
import { ReactNode } from 'react';

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Don't retry failed queries in tests
        gcTime: Infinity,
      },
    },
    logger: {
      log: console.log,
      warn: console.warn,
      error: () => {}, // Silence errors in tests
    },
  });
}

export function renderWithClient(ui: ReactNode) {
  const testQueryClient = createTestQueryClient();

  return render(
    <QueryClientProvider client={testQueryClient}>
      {ui}
    </QueryClientProvider>
  );
}
```

### Testing Queries

**Basic Query Test:**
```tsx
// UserProfile.test.tsx
import { renderWithClient } from '@/test/utils';
import { screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { UserProfile } from './UserProfile';

const server = setupServer(
  rest.get('/api/users/1', (req, res, ctx) => {
    return res(
      ctx.json({
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('displays user profile', async () => {
  renderWithClient(<UserProfile userId={1} />);

  expect(screen.getByText('Loading...')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});

test('handles fetch error', async () => {
  server.use(
    rest.get('/api/users/1', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );

  renderWithClient(<UserProfile userId={1} />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

### Testing Mutations

```tsx
// CreateUserForm.test.tsx
import { renderWithClient } from '@/test/utils';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { CreateUserForm } from './CreateUserForm';

const server = setupServer(
  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json();
    return res(
      ctx.json({
        id: 1,
        ...body,
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('creates user successfully', async () => {
  const user = userEvent.setup();
  renderWithClient(<CreateUserForm />);

  await user.type(screen.getByPlaceholderText('Name'), 'John Doe');
  await user.type(screen.getByPlaceholderText('Email'), 'john@example.com');
  await user.click(screen.getByRole('button', { name: /create/i }));

  await waitFor(() => {
    expect(screen.getByText(/created successfully/i)).toBeInTheDocument();
  });
});
```

### Testing with Mock Data

**Hydrate Query Data:**
```tsx
test('renders with initial data', () => {
  const testQueryClient = createTestQueryClient();

  // Pre-populate cache
  testQueryClient.setQueryData(['user', 1], {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
  });

  render(
    <QueryClientProvider client={testQueryClient}>
      <UserProfile userId={1} />
    </QueryClientProvider>
  );

  // Data immediately available (no loading state)
  expect(screen.getByText('John Doe')).toBeInTheDocument();
});
```

### Testing Custom Hooks

```tsx
// useUser.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { useUser } from './useUser';

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'John Doe' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('fetches user data', async () => {
  const queryClient = new QueryClient();
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );

  const { result } = renderHook(() => useUser(1), { wrapper });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toEqual({ id: 1, name: 'John Doe' });
});
```

---

## Performance Optimization

### Query Deduplication

**Automatic Deduplication:**
```tsx
// Multiple components request same data - only one network request
function Dashboard() {
  return (
    <div>
      <UserStats userId={1} />    {/* Triggers fetch */}
      <UserProfile userId={1} />  {/* Uses cache */}
      <UserActivity userId={1} /> {/* Uses cache */}
    </div>
  );
}
```

### Prefetching

**Hover Prefetch:**
```tsx
function UserLink({ userId }: { userId: number }) {
  const queryClient = useQueryClient();

  const prefetchUser = () => {
    queryClient.prefetchQuery({
      queryKey: ['user', userId],
      queryFn: () => fetchUser(userId),
      staleTime: 60000,
    });
  };

  return (
    <Link
      href={`/users/${userId}`}
      onMouseEnter={prefetchUser}
      onFocus={prefetchUser}
    >
      View User
    </Link>
  );
}
```

**Route Prefetch:**
```tsx
// Next.js App Router
import { QueryClient, HydrationBoundary, dehydrate } from '@tanstack/react-query';

export default async function UserPage({ params }: { params: { id: string } }) {
  const queryClient = new QueryClient();

  // Prefetch user data
  await queryClient.prefetchQuery({
    queryKey: ['user', params.id],
    queryFn: () => fetchUser(params.id),
  });

  // Prefetch related data
  await queryClient.prefetchQuery({
    queryKey: ['user-posts', params.id],
    queryFn: () => fetchUserPosts(params.id),
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UserProfile userId={params.id} />
    </HydrationBoundary>
  );
}
```

### Select and Transform Data

**Memo-ized Selectors:**
```tsx
// Only re-render when selected data changes
function TodoList({ filter }: { filter: 'all' | 'done' | 'pending' }) {
  const { data: filteredTodos } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    select: (todos) => {
      // This only runs when todos change
      if (filter === 'done') return todos.filter(t => t.done);
      if (filter === 'pending') return todos.filter(t => !t.done);
      return todos;
    },
  });

  // Component only re-renders when filteredTodos change
  return (
    <ul>
      {filteredTodos?.map(todo => <li key={todo.id}>{todo.title}</li>)}
    </ul>
  );
}
```

**Expensive Computations:**
```tsx
const { data: sortedUsers } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
  select: (users) => {
    // Heavy sorting only runs when users change
    return users
      .slice()
      .sort((a, b) => a.name.localeCompare(b.name));
  },
});
```

### Structural Sharing

**Automatic Structural Sharing:**
```tsx
// TanStack Query automatically does structural sharing
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  structuralSharing: true, // Default
});

// If refetch returns identical data structure,
// component doesn't re-render even though fetch completed
```

**Custom Structural Sharing:**
```tsx
import { replaceEqualDeep } from '@tanstack/react-query';

const { data } = useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  structuralSharing: (oldData, newData) => {
    // Custom comparison logic
    return replaceEqualDeep(oldData, newData);
  },
});
```

### Query Cancellation

**Abort In-Flight Requests:**
```tsx
const { data, refetch } = useQuery({
  queryKey: ['search', searchTerm],
  queryFn: async ({ signal }) => {
    const response = await fetch(`/api/search?q=${searchTerm}`, {
      signal, // Pass abort signal
    });
    return response.json();
  },
});

// When searchTerm changes, previous request is cancelled automatically
```

**Manual Cancellation:**
```tsx
const queryClient = useQueryClient();

// Cancel all queries
queryClient.cancelQueries();

// Cancel specific query
queryClient.cancelQueries({ queryKey: ['todos'] });
```

---

## Best Practices and Common Patterns

### Query Key Factories

**Centralized Query Keys:**
```tsx
// lib/query-keys.ts
export const queryKeys = {
  users: {
    all: ['users'] as const,
    lists: () => [...queryKeys.users.all, 'list'] as const,
    list: (filters: UserFilters) => [...queryKeys.users.lists(), filters] as const,
    details: () => [...queryKeys.users.all, 'detail'] as const,
    detail: (id: number) => [...queryKeys.users.details(), id] as const,
  },
  posts: {
    all: ['posts'] as const,
    lists: () => [...queryKeys.posts.all, 'list'] as const,
    list: (filters: PostFilters) => [...queryKeys.posts.lists(), filters] as const,
    details: () => [...queryKeys.posts.all, 'detail'] as const,
    detail: (id: number) => [...queryKeys.posts.details(), id] as const,
  },
};

// Usage
const { data } = useQuery({
  queryKey: queryKeys.users.detail(userId),
  queryFn: () => fetchUser(userId),
});

// Invalidate all user lists
queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });
```

### Custom Hook Patterns

**Resource Hook Factory:**
```tsx
// lib/create-resource-hooks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function createResourceHooks<T, CreateT = Partial<T>, UpdateT = Partial<T>>(
  resourceName: string,
  api: {
    getAll: () => Promise<T[]>;
    getOne: (id: string | number) => Promise<T>;
    create: (data: CreateT) => Promise<T>;
    update: (id: string | number, data: UpdateT) => Promise<T>;
    delete: (id: string | number) => Promise<void>;
  }
) {
  const keys = {
    all: [resourceName] as const,
    lists: () => [...keys.all, 'list'] as const,
    details: () => [...keys.all, 'detail'] as const,
    detail: (id: string | number) => [...keys.details(), id] as const,
  };

  return {
    useList: () =>
      useQuery({
        queryKey: keys.lists(),
        queryFn: api.getAll,
      }),

    useDetail: (id: string | number) =>
      useQuery({
        queryKey: keys.detail(id),
        queryFn: () => api.getOne(id),
        enabled: !!id,
      }),

    useCreate: () => {
      const queryClient = useQueryClient();
      return useMutation({
        mutationFn: api.create,
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: keys.lists() });
        },
      });
    },

    useUpdate: () => {
      const queryClient = useQueryClient();
      return useMutation({
        mutationFn: ({ id, data }: { id: string | number; data: UpdateT }) =>
          api.update(id, data),
        onSuccess: (_, { id }) => {
          queryClient.invalidateQueries({ queryKey: keys.detail(id) });
          queryClient.invalidateQueries({ queryKey: keys.lists() });
        },
      });
    },

    useDelete: () => {
      const queryClient = useQueryClient();
      return useMutation({
        mutationFn: api.delete,
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: keys.lists() });
        },
      });
    },
  };
}

// Usage
const userHooks = createResourceHooks('users', userApi);

function UsersList() {
  const { data: users } = userHooks.useList();
  const createUser = userHooks.useCreate();
  const deleteUser = userHooks.useDelete();

  return (
    <div>
      {users?.map(user => (
        <div key={user.id}>
          {user.name}
          <button onClick={() => deleteUser.mutate(user.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}
```

### Error Handling Patterns

**Centralized Error Handler:**
```tsx
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error) => {
        if (error instanceof APIError) {
          toast.error(`Error: ${error.message}`);
        }
      },
    },
    mutations: {
      onError: (error) => {
        toast.error(`Failed to save: ${error.message}`);
      },
    },
  },
});
```

### Migration from SWR

**SWR to TanStack Query:**
```tsx
// Before (SWR)
import useSWR from 'swr';

function Profile() {
  const { data, error, mutate } = useSWR('/api/user', fetcher);

  if (error) return <div>Error</div>;
  if (!data) return <div>Loading...</div>;
  return <div>{data.name}</div>;
}

// After (TanStack Query)
import { useQuery, useQueryClient } from '@tanstack/react-query';

function Profile() {
  const { data, error, isLoading } = useQuery({
    queryKey: ['/api/user'],
    queryFn: () => fetcher('/api/user'),
  });

  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['/api/user'] });

  if (error) return <div>Error</div>;
  if (isLoading) return <div>Loading...</div>;
  return <div>{data.name}</div>;
}
```

**Comparison:**
- `useSWR(key, fetcher)` → `useQuery({ queryKey: [key], queryFn: fetcher })`
- `mutate()` → `queryClient.invalidateQueries()`
- `!data` loading → `isLoading`
- `useSWRConfig()` → `useQueryClient()`

---

## DevTools

**Setup DevTools:**
```tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

**Production Build:**
```tsx
// DevTools are automatically excluded in production builds
// No need to conditionally render
```

**DevTools Features:**
- View all queries and their states
- Inspect query data and errors
- Manually trigger refetch
- Invalidate queries
- View query timelines
- Monitor cache size
- Debug network waterfalls

---

## Common Pitfalls

**❌ Don't Create QueryClient Inside Component:**
```tsx
// WRONG - Creates new client on every render
function App() {
  const queryClient = new QueryClient(); // ❌
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>;
}

// CORRECT - Stable client instance
function App() {
  const [queryClient] = useState(() => new QueryClient()); // ✅
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>;
}
```

**❌ Don't Use Query Data in Render Without Checking:**
```tsx
// WRONG - data might be undefined
function UserProfile() {
  const { data } = useQuery({ queryKey: ['user'], queryFn: fetchUser });
  return <div>{data.name}</div>; // ❌ Crashes if data is undefined
}

// CORRECT - Handle loading state
function UserProfile() {
  const { data, isLoading } = useQuery({ queryKey: ['user'], queryFn: fetchUser });
  if (isLoading) return <Spinner />; // ✅
  return <div>{data.name}</div>;
}
```

**❌ Don't Forget Query Keys Are Dependencies:**
```tsx
// WRONG - Missing dependency in query key
function UserPosts({ userId, filter }: Props) {
  const { data } = useQuery({
    queryKey: ['posts'], // ❌ Missing userId and filter
    queryFn: () => fetchUserPosts(userId, filter),
  });
}

// CORRECT - All dependencies in key
function UserPosts({ userId, filter }: Props) {
  const { data } = useQuery({
    queryKey: ['posts', userId, filter], // ✅
    queryFn: () => fetchUserPosts(userId, filter),
  });
}
```

**❌ Don't Mutate Query Data Directly:**
```tsx
// WRONG - Mutating cached data
const { data } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos });
data.push(newTodo); // ❌ Mutates cache directly

// CORRECT - Use setQueryData
queryClient.setQueryData(['todos'], (old = []) => [...old, newTodo]); // ✅
```

---

## Summary

TanStack Query is the industry-standard solution for server-state management in React applications. Use it for API data fetching, caching, synchronization, and real-time updates. It eliminates manual state management boilerplate and provides powerful features like automatic background refetching, optimistic updates, pagination, and intelligent cache management.

**Key Takeaways:**
- Use `useQuery` for fetching data with automatic caching
- Use `useMutation` for create/update/delete operations
- Query keys are the foundation of cache management
- Invalidate queries after mutations to keep UI in sync
- Leverage optimistic updates for instant UI feedback
- Use `useInfiniteQuery` for pagination and infinite scroll
- Combine with Zustand for client-state management
- Integrate seamlessly with tRPC, REST, and GraphQL
- Type everything with TypeScript for full type safety
- Test with MSW for realistic API mocking

**Progressive Loading Pattern:**
- **Entry Point**: Quick start and basic setup
- **Intermediate**: Queries, mutations, and cache management
- **Advanced**: Optimistic updates, SSR, integrations, and performance

For additional resources, visit the [official documentation](https://tanstack.com/query/latest).

## Related Skills

When using Tanstack Query, these skills enhance your workflow:
- **react**: React hooks and patterns for integrating TanStack Query
- **nextjs**: TanStack Query with Next.js App Router and Server Components
- **zustand**: Complementary client-state management (use together for hybrid state)
- **test-driven-development**: Testing queries, mutations, and cache behavior

[Full documentation available in these skills if deployed in your bundle]
