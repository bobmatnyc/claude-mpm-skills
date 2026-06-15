# React Hooks Performance Optimization

## Memoization Strategies

### useMemo: Expensive Computations

```typescript
function UserDashboard({ users }: { users: User[] }) {
  // Expensive computation - only recalculate when users change
  const statistics = useMemo(() => {
    return {
      totalUsers: users.length,
      activeUsers: users.filter(u => u.active).length,
      averageAge: users.reduce((sum, u) => sum + u.age, 0) / users.length,
      topRegions: calculateTopRegions(users), // Expensive function
    };
  }, [users]);

  return <StatisticsDisplay stats={statistics} />;
}
```

### useCallback: Stable Function References

```typescript
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState<Item[]>([]);

  // Without useCallback, this function recreates on every render
  // causing child components to re-render unnecessarily
  const handleItemClick = useCallback((itemId: string) => {
    console.log('Item clicked:', itemId);
    // Function body can reference count without including it in deps
    // if you only need the latest value
  }, []); // Empty deps = function never changes

  const handleItemUpdate = useCallback((itemId: string, newData: Partial<Item>) => {
    setItems(prev => prev.map(item =>
      item.id === itemId ? { ...item, ...newData } : item
    ));
  }, []); // setItems is stable, so no deps needed

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>

      {/* These children won't re-render when count changes */}
      {items.map(item => (
        <ItemComponent
          key={item.id}
          item={item}
          onClick={handleItemClick}
          onUpdate={handleItemUpdate}
        />
      ))}
    </div>
  );
}

// Child component must be memoized to benefit
const ItemComponent = memo(function ItemComponent({
  item,
  onClick,
  onUpdate,
}: {
  item: Item;
  onClick: (id: string) => void;
  onUpdate: (id: string, data: Partial<Item>) => void;
}) {
  return (
    <div onClick={() => onClick(item.id)}>
      {item.name}
    </div>
  );
});
```

## React.memo: Prevent Component Re-renders

### Pattern: Memoize Expensive Components

```typescript
interface ExpensiveChartProps {
  data: DataPoint[];
  config: ChartConfig;
}

// Without memo, re-renders every time parent re-renders
const ExpensiveChart = memo(function ExpensiveChart({
  data,
  config
}: ExpensiveChartProps) {
  // Expensive rendering logic
  return <ComplexChart data={data} config={config} />;
}, (prevProps, nextProps) => {
  // Custom comparison function
  return (
    prevProps.data === nextProps.data &&
    prevProps.config.theme === nextProps.config.theme
  );
});
```

### Pattern: Stable Props with useMemo

```typescript
function Dashboard() {
  const [filters, setFilters] = useState<Filters>({});
  const [data, setData] = useState<DataPoint[]>([]);

  // Create stable config object
  const chartConfig = useMemo(() => ({
    theme: 'dark',
    animation: true,
    responsive: true,
  }), []); // Config never changes

  // Create stable filtered data
  const filteredData = useMemo(() => {
    return applyFilters(data, filters);
  }, [data, filters]);

  // ExpensiveChart only re-renders when data or config actually changes
  return (
    <ExpensiveChart
      data={filteredData}
      config={chartConfig}
    />
  );
}
```

## Context Optimization

### Pattern: Split Contexts by Update Frequency

```typescript
// Fast-changing state
const UserInteractionContext = createContext<{
  mousePosition: { x: number; y: number };
  scrollPosition: number;
} | undefined>(undefined);

// Slow-changing state
const UserDataContext = createContext<{
  user: User | null;
  preferences: UserPreferences;
} | undefined>(undefined);

function AppProvider({ children }: { children: ReactNode }) {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [scrollPosition, setScrollPosition] = useState(0);
  const [user, setUser] = useState<User | null>(null);
  const [preferences, setPreferences] = useState<UserPreferences>({});

  // Fast-changing value
  const interactionValue = useMemo(() => ({
    mousePosition,
    scrollPosition,
  }), [mousePosition, scrollPosition]);

  // Slow-changing value
  const dataValue = useMemo(() => ({
    user,
    preferences,
  }), [user, preferences]);

  return (
    <UserDataContext.Provider value={dataValue}>
      <UserInteractionContext.Provider value={interactionValue}>
        {children}
      </UserInteractionContext.Provider>
    </UserDataContext.Provider>
  );
}
```

### Pattern: Context Selectors with useSyncExternalStore

```typescript
import { useSyncExternalStore } from 'react';

interface Store {
  users: User[];
  posts: Post[];
  comments: Comment[];
}

class StoreManager {
  private state: Store = { users: [], posts: [], comments: [] };
  private listeners = new Set<() => void>();

  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  };

  getSnapshot = () => this.state;

  updateUsers(users: User[]) {
    this.state = { ...this.state, users };
    this.listeners.forEach(listener => listener());
  }
}

const store = new StoreManager();

// Custom hook that only subscribes to users
function useUsers() {
  const state = useSyncExternalStore(
    store.subscribe,
    store.getSnapshot,
    store.getSnapshot
  );

  return state.users;
}

// Component only re-renders when users change, not posts or comments
function UserList() {
  const users = useUsers();
  return <div>{users.map(u => <div key={u.id}>{u.name}</div>)}</div>;
}
```

## Lazy Initialization

### Pattern: Lazy Initial State

```typescript
function ExpensiveComponent({ userId }: { userId: string }) {
  // BAD: Expensive computation runs on every render
  const [data, setData] = useState(expensiveComputation(userId));

  // GOOD: Expensive computation runs only once
  const [data, setData] = useState(() => expensiveComputation(userId));

  return <div>{data}</div>;
}
```

### Pattern: Lazy Component Loading

```typescript
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const ComplexEditor = lazy(() => import('./ComplexEditor'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>
        Show Chart
      </button>

      {showChart && (
        <Suspense fallback={<Spinner />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

## Debouncing and Throttling

### Pattern: Debounced Input

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchInput() {
  const [input, setInput] = useState('');
  const debouncedInput = useDebounce(input, 500);

  // API call only fires 500ms after user stops typing
  const { data } = useSWR(
    debouncedInput ? `/api/search?q=${debouncedInput}` : null
  );

  return (
    <input
      value={input}
      onChange={(e) => setInput(e.target.value)}
    />
  );
}
```

### Pattern: Throttled Event Handler

```typescript
function useThrottle<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): T {
  const lastRan = useRef(Date.now());

  return useCallback(
    ((...args) => {
      const now = Date.now();

      if (now - lastRan.current >= delay) {
        callback(...args);
        lastRan.current = now;
      }
    }) as T,
    [callback, delay]
  );
}

// Usage
function ScrollTracker() {
  const handleScroll = useThrottle(() => {
    console.log('Scroll position:', window.scrollY);
  }, 200); // Max once per 200ms

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  return <div>Scroll me</div>;
}
```

## List Rendering Optimization

### Pattern: Virtualized Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualizedList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated item height
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ItemComponent item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Pattern: Keyed Reconciliation

```typescript
// BAD: Using index as key
function BadList({ items }: { items: Item[] }) {
  return (
    <div>
      {items.map((item, index) => (
        <div key={index}>{item.name}</div>
      ))}
    </div>
  );
}

// GOOD: Using stable unique ID
function GoodList({ items }: { items: Item[] }) {
  return (
    <div>
      {items.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}
```

## Conditional Rendering Optimization

### Pattern: Early Return

```typescript
function UserProfile({ userId }: { userId: string | null }) {
  const { data: user, isLoading } = useUser(userId);

  // Early returns prevent unnecessary hook calls
  if (!userId) {
    return <div>Please select a user</div>;
  }

  if (isLoading) {
    return <Spinner />;
  }

  if (!user) {
    return <div>User not found</div>;
  }

  // Main render only when we have data
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

## Custom Hook Optimization

### Pattern: Composable Optimized Hooks

```typescript
// Base hook with minimal dependencies
function useUserData(userId: string) {
  const { data, error, isLoading } = useSWR(`/api/users/${userId}`);
  return { data, error, isLoading };
}

// Derived hook with memoization
function useUserStats(userId: string) {
  const { data: user } = useUserData(userId);

  const stats = useMemo(() => {
    if (!user) return null;

    return {
      totalPosts: user.posts.length,
      totalLikes: user.posts.reduce((sum, p) => sum + p.likes, 0),
      avgLikesPerPost: user.posts.length
        ? user.posts.reduce((sum, p) => sum + p.likes, 0) / user.posts.length
        : 0,
    };
  }, [user]);

  return stats;
}

// Composed hook for complete user profile
function useUserProfile(userId: string) {
  const userData = useUserData(userId);
  const userStats = useUserStats(userId);

  return useMemo(() => ({
    ...userData,
    stats: userStats,
  }), [userData, userStats]);
}
```

## Profiling and Debugging

### Pattern: Performance Monitoring

```typescript
function usePerformanceMonitor(componentName: string) {
  const renderCount = useRef(0);
  const lastRenderTime = useRef(Date.now());

  useEffect(() => {
    renderCount.current += 1;
    const now = Date.now();
    const timeSinceLastRender = now - lastRenderTime.current;

    console.log(`[${componentName}] Render #${renderCount.current}`, {
      timeSinceLastRender,
      timestamp: now,
    });

    lastRenderTime.current = now;
  });
}

// Usage
function MyComponent() {
  usePerformanceMonitor('MyComponent');

  return <div>Content</div>;
}
```

### Pattern: Why Did You Render

```typescript
function useWhyDidYouUpdate(name: string, props: Record<string, any>) {
  const previousProps = useRef<Record<string, any>>();

  useEffect(() => {
    if (previousProps.current) {
      const allKeys = Object.keys({ ...previousProps.current, ...props });
      const changedProps: Record<string, { from: any; to: any }> = {};

      allKeys.forEach(key => {
        if (previousProps.current![key] !== props[key]) {
          changedProps[key] = {
            from: previousProps.current![key],
            to: props[key],
          };
        }
      });

      if (Object.keys(changedProps).length > 0) {
        console.log(`[${name}] Changed props:`, changedProps);
      }
    }

    previousProps.current = props;
  });
}

// Usage
function MyComponent(props: MyProps) {
  useWhyDidYouUpdate('MyComponent', props);

  return <div>Content</div>;
}
```
