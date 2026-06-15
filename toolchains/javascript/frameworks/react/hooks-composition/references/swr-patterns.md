# SWR Patterns and Best Practices

## Conditional Fetching Strategies

### Pattern: Query Parameter Dependencies

```typescript
function useUserData(userId: string | null, includeDetails: boolean) {
  const { data, error, isLoading } = useSWR(
    userId && includeDetails
      ? `/api/users/${userId}?details=true`
      : userId
      ? `/api/users/${userId}`
      : null
  );

  return { user: data, error, isLoading };
}
```

### Pattern: Authentication-Gated Fetching

```typescript
function useProtectedResource(resourceId: string) {
  const { user } = useAuth();

  const { data, error } = useSWR(
    user?.token
      ? [`/api/resources/${resourceId}`, user.token]
      : null,
    ([url, token]) => fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(r => r.json())
  );

  return { data, error };
}
```

## Data Transformation Patterns

### Pattern: Filtering and Mapping Response

```typescript
function useActiveUsers() {
  const { data, error, isLoading } = useSWR<User[]>('/api/users');

  const activeUsers = useMemo(() => {
    if (!data) return [];

    return data
      .filter(user => user.status === 'active')
      .map(user => ({
        id: user.id,
        name: user.fullName,
        email: user.emailAddress,
      }));
  }, [data]);

  return { users: activeUsers, error, isLoading };
}
```

### Pattern: Normalized Data Structure

```typescript
interface ApiUser {
  id: string;
  attributes: {
    firstName: string;
    lastName: string;
    email: string;
  };
}

interface NormalizedUser {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
}

function useNormalizedUsers() {
  const { data, error, isLoading } = useSWR<ApiUser[]>('/api/users');

  const normalizedUsers = useMemo(() => {
    if (!data) return [];

    return data.map(user => ({
      id: user.id,
      ...user.attributes,
    }));
  }, [data]);

  return { users: normalizedUsers, error, isLoading };
}
```

## Pagination Patterns

### Pattern: Infinite Loading with SWR

```typescript
import useSWRInfinite from 'swr/infinite';

function useInfiniteUsers(pageSize = 20) {
  const getKey = (pageIndex: number, previousPageData: any) => {
    // Reached the end
    if (previousPageData && !previousPageData.hasMore) return null;

    // First page
    return `/api/users?page=${pageIndex + 1}&limit=${pageSize}`;
  };

  const { data, error, size, setSize, isLoading } = useSWRInfinite(getKey);

  const users = useMemo(() => {
    return data ? data.flatMap(page => page.users) : [];
  }, [data]);

  const hasMore = data?.[data.length - 1]?.hasMore ?? false;

  const loadMore = () => {
    setSize(size + 1);
  };

  return {
    users,
    error,
    isLoading,
    hasMore,
    loadMore,
  };
}
```

## Error Handling Patterns

### Pattern: Retry with Exponential Backoff

```typescript
function useResilientFetch<T>(url: string | null) {
  const { data, error, isLoading } = useSWR<T>(
    url,
    {
      onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
        // Don't retry on 404
        if (error.status === 404) return;

        // Max 5 retries
        if (retryCount >= 5) return;

        // Exponential backoff
        setTimeout(() => {
          revalidate({ retryCount });
        }, 1000 * Math.pow(2, retryCount));
      }
    }
  );

  return { data, error, isLoading };
}
```

### Pattern: Fallback Data

```typescript
function useUserWithFallback(userId: string) {
  const { data, error, isLoading } = useSWR(
    `/api/users/${userId}`,
    {
      fallbackData: {
        id: userId,
        name: 'Loading...',
        email: '',
      }
    }
  );

  return { user: data, error, isLoading };
}
```

## Optimistic Updates

### Pattern: Optimistic Mutation

```typescript
function useTodoList() {
  const { data: todos, mutate } = useSWR<Todo[]>('/api/todos');

  const addTodo = async (title: string) => {
    const newTodo = {
      id: `temp-${Date.now()}`,
      title,
      completed: false,
    };

    // Optimistically update local data
    mutate([...(todos || []), newTodo], false);

    try {
      // Send request to API
      const created = await fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify({ title }),
      }).then(r => r.json());

      // Update with server response
      mutate();
    } catch (error) {
      // Rollback on error
      mutate();
      throw error;
    }
  };

  return { todos, addTodo };
}
```

## Dependent Queries

### Pattern: Sequential Data Fetching

```typescript
function useUserProfile(userId: string) {
  // First query
  const { data: user } = useSWR(`/api/users/${userId}`);

  // Second query depends on first
  const { data: posts } = useSWR(
    user?.id ? `/api/users/${user.id}/posts` : null
  );

  // Third query depends on second
  const { data: comments } = useSWR(
    posts?.length ? `/api/posts/${posts[0].id}/comments` : null
  );

  return { user, posts, comments };
}
```

## Polling and Revalidation

### Pattern: Real-time Updates

```typescript
function useLiveData(endpoint: string, intervalMs = 5000) {
  const { data, error, isLoading } = useSWR(
    endpoint,
    {
      refreshInterval: intervalMs,
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  );

  return { data, error, isLoading };
}
```

### Pattern: Conditional Polling

```typescript
function useConditionalPolling(enabled: boolean) {
  const { data, error } = useSWR(
    '/api/status',
    {
      refreshInterval: enabled ? 1000 : 0,
    }
  );

  return { data, error };
}
```

## Type-Safe SWR Keys

### Pattern: Typed SWR Keys

```typescript
type ApiKey =
  | ['user', string]
  | ['posts', { userId: string; page: number }]
  | ['comments', string];

function useTypedSWR<T>(key: ApiKey) {
  return useSWR<T>(key, {
    fetcher: async (key) => {
      const [resource, params] = key;

      switch (resource) {
        case 'user':
          return fetch(`/api/users/${params}`).then(r => r.json());
        case 'posts':
          return fetch(
            `/api/posts?userId=${params.userId}&page=${params.page}`
          ).then(r => r.json());
        case 'comments':
          return fetch(`/api/comments/${params}`).then(r => r.json());
      }
    }
  });
}

// Usage
const { data: user } = useTypedSWR<User>(['user', '123']);
const { data: posts } = useTypedSWR<Post[]>(['posts', { userId: '123', page: 1 }]);
```

## Performance Optimization

### Pattern: Deduplicate Requests

```typescript
function useDeduplicatedFetch<T>(url: string) {
  const { data, error, isLoading } = useSWR<T>(
    url,
    {
      dedupingInterval: 2000, // Deduplicate requests within 2s
    }
  );

  return { data, error, isLoading };
}
```

### Pattern: Prefetching

```typescript
import { mutate } from 'swr';

function prefetchUser(userId: string) {
  // Prefetch user data
  mutate(
    `/api/users/${userId}`,
    fetch(`/api/users/${userId}`).then(r => r.json())
  );
}

// Usage in component
function UserList({ users }: { users: User[] }) {
  return (
    <div>
      {users.map(user => (
        <div
          key={user.id}
          onMouseEnter={() => prefetchUser(user.id)}
        >
          <Link to={`/users/${user.id}`}>{user.name}</Link>
        </div>
      ))}
    </div>
  );
}
```
