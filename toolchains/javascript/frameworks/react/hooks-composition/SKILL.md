---
name: react-hooks-composition
description: Advanced React hooks composition patterns - SWR integration, debounced search, memoized contexts, state machines, and performance optimization
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Master React hooks composition: custom hooks with SWR, debounced state, memoized contexts, type-safe patterns"
    when_to_use: "Building data-fetching hooks, search interfaces, context providers, async UI states, performance-critical components"
    quick_start: "1. Compose SWR with conditional keys 2. Add debounce with dual loading states 3. Memoize context values 4. Use state machines for UI states"
context_limit: 700
tags:
  - react
  - hooks
  - composition
  - swr
  - performance
  - typescript
  - custom-hooks
  - useMemo
  - useCallback
  - context
  - debounce
  - state-machine
requires_tools: []
---

# React Hooks Composition Patterns

## Overview

Advanced patterns for composing React hooks to create maintainable, performant, and type-safe custom hooks. Covers SWR integration, debounced search, memoized contexts, and state machine patterns.

**Key Concepts**:
- Conditional SWR fetching with null keys
- Debounced state with dual loading indicators
- Memoized context providers to prevent re-renders
- State machine pattern for predictable UI states
- Pure helper functions for testability

## Pattern 1: SWR Hook Composition with Conditional Fetching

### The Pattern

Compose SWR with conditional logic, data transformation, and pure helper functions.

```typescript
import useSWR from 'swr';
import { useMemo } from 'react';

// Type definitions
interface MapboxSuggestion {
  name: string;
  mapbox_id: string;
  context?: {
    country?: {
      country_code: string;
    };
  };
}

interface MapboxSuggestResponse {
  suggestions: MapboxSuggestion[];
}

interface LocationSuggestion {
  id: string;
  displayName: string;
  region: string;
}

// Custom hook with conditional fetching
export function useMapboxLocationSuggestions(
  inputValue: string | null | undefined
) {
  const sessionId = useSessionId();

  // Conditional SWR key - null disables fetching
  const { data, error, isLoading } = useSWR<MapboxSuggestResponse>(
    // Key is null (no fetch) unless all conditions met
    sessionId &&
    process.env.NEXT_PUBLIC_MAPBOX_API_KEY &&
    isValidSearchQuery(inputValue)
      ? `https://api.mapbox.com/search/searchbox/v1/suggest?q=${encodeURIComponent(inputValue!)}&session_token=${sessionId}&access_token=${process.env.NEXT_PUBLIC_MAPBOX_API_KEY}`
      : null
  );

  // Transform data with useMemo for performance
  const mappedData = useMemo(() => {
    if (!data) return undefined;

    return data.suggestions
      .filter(isUsState)
      .map(formatMapboxLocation);
  }, [data]);

  return {
    data: mappedData,
    error,
    isLoading
  };
}

// Pure helper functions (outside component/hook)
const isValidSearchQuery = (
  value: string | null | undefined
): value is string => {
  return typeof value === 'string' && value.trim().length >= 2;
};

const isUsState = (suggestion: MapboxSuggestion): boolean => {
  return suggestion.context?.country?.country_code === 'us';
};

const formatMapboxLocation = (
  suggestion: MapboxSuggestion
): LocationSuggestion => ({
  id: suggestion.mapbox_id,
  displayName: suggestion.name,
  region: 'US',
});
```

### Why This Works

**Conditional Fetching**:
- SWR doesn't fetch when key is `null`
- All conditions checked before constructing URL
- Type guard `isValidSearchQuery` ensures type safety
- Prevents unnecessary API calls on empty input

**Data Transformation**:
- `useMemo` prevents recomputation on every render
- Dependency array `[data]` only recomputes when data changes
- Filter and map operations are pure and testable

**Testability**:
- Pure functions can be tested independently
- No React context needed for helper functions
- Type guards provide runtime validation

### Common Triggers

Use this pattern when:
- "fetch data based on user input"
- "conditional API calls with SWR"
- "transform API response data"
- "prevent fetching on empty search"
- "type-safe data fetching hooks"

## Pattern 2: Debounced Search with Dual Loading States

### The Pattern

Combine debounced input with SWR fetching, tracking both debouncing and network loading states.

```typescript
import { useState } from 'react';
import useSWR from 'swr';

// Debounce hook
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

// Search component with dual loading states
export function SearchComponent() {
  const [searchInput, setSearchInput] = useState('');
  const debouncedSearchInput = useDebounce(searchInput, 300);

  // Track if we're still debouncing (user is typing)
  const isDebouncing = searchInput !== debouncedSearchInput;

  // Fetch with debounced value
  const { data = [], isLoading } = useLocationSuggestions(debouncedSearchInput);

  // Combined loading state: debouncing OR fetching
  const suggestionsLoading = isDebouncing || isLoading;

  return (
    <SearchInput
      value={searchInput}
      onChange={setSearchInput}
      loading={suggestionsLoading}
      suggestions={data}
      placeholder="Search locations..."
    />
  );
}
```

### Why This Works

**Dual Loading States**:
- `isDebouncing`: Indicates user is still typing
- `isLoading`: Indicates network request in progress
- Combined state provides smooth UX feedback

**Performance**:
- API calls only fire after 300ms of inactivity
- Reduces unnecessary requests while typing
- SWR caches results for instant display

**User Experience**:
- Loading indicator appears immediately on typing
- Prevents result flashing between debounce intervals
- Clear feedback during both input and fetch phases

### Common Triggers

Use this pattern when:
- "debounced search with loading state"
- "prevent too many API calls while typing"
- "show loading indicator during debounce"
- "smooth search experience"
- "combine debounce with data fetching"

## Pattern 3: Memoized Context Provider

### The Pattern

Create context providers with memoized values to prevent unnecessary re-renders of consumers.

```typescript
import { createContext, useContext, useState, useCallback, useMemo, ReactNode } from 'react';

// Context value type
interface LocationContextValue {
  location: UserLocation | null;
  requestPreciseLocation: () => Promise<UserLocation | null>;
}

interface UserLocation {
  latitude: number;
  longitude: number;
  accuracy: 'coarse' | 'precise';
}

// Create context with undefined default
const UserLocationContext = createContext<LocationContextValue | undefined>(
  undefined
);

// Provider component
export const UserLocationProvider = ({
  location: initialLocation = null,
  children
}: {
  location?: UserLocation | null;
  children: ReactNode;
}) => {
  const [preciseLocation, setPreciseLocation] = useState<UserLocation | null>(null);

  // Stable callback reference with useCallback
  const requestPreciseLocation = useCallback(async () => {
    try {
      const coords = await getUserCoordinates();
      const location = coords
        ? {
            latitude: coords.latitude,
            longitude: coords.longitude,
            accuracy: 'precise' as const
          }
        : null;

      setPreciseLocation(location);
      return location;
    } catch (error) {
      console.error('Failed to get precise location:', error);
      return null;
    }
  }, []); // No dependencies - function is stable

  // Memoized context value prevents unnecessary re-renders
  const contextValue = useMemo<LocationContextValue>(() => ({
    location: preciseLocation || initialLocation,
    requestPreciseLocation,
  }), [initialLocation, preciseLocation, requestPreciseLocation]);

  return (
    <UserLocationContext.Provider value={contextValue}>
      {children}
    </UserLocationContext.Provider>
  );
};

// Type-safe hook for consuming context
export const useUserLocation = (): LocationContextValue => {
  const context = useContext(UserLocationContext);

  if (context === undefined) {
    throw new Error('useUserLocation must be used within UserLocationProvider');
  }

  return context;
};

// Helper function (can be in separate file)
async function getUserCoordinates(): Promise<GeolocationCoordinates | null> {
  return new Promise((resolve) => {
    navigator.geolocation.getCurrentPosition(
      (position) => resolve(position.coords),
      () => resolve(null),
      { enableHighAccuracy: true }
    );
  });
}
```

### Why This Works

**Memoization Prevents Re-renders**:
- `useMemo` for context value object
- Only recreates when dependencies change
- Consumers only re-render when values actually change

**Stable References**:
- `useCallback` ensures `requestPreciseLocation` reference is stable
- No dependencies means function never changes
- Internal state updates don't recreate function

**Type Safety**:
- Context hook throws if used outside provider
- TypeScript enforces correct usage
- Clear error messages for misuse

**Best Practices**:
- Context value is an object with multiple properties
- Provider manages both props and internal state
- Custom hook abstracts context consumption

### Common Triggers

Use this pattern when:
- "context causing too many re-renders"
- "optimize context provider performance"
- "stable callback in context"
- "memoized context value"
- "prevent unnecessary renders from context"

## Pattern 4: State Machine for UI States

### The Pattern

Use discriminated unions and state machines for predictable UI state management.

```typescript
import { useState } from 'react';

// Discriminated union for request states
type RequestState = 'idle' | 'pending' | 'success' | 'error';

// State-specific configuration
const stateConfig: Record<RequestState, {
  label: string;
  disabled: boolean;
  variant: 'primary' | 'success' | 'danger';
}> = {
  idle: {
    label: 'Click to start',
    disabled: false,
    variant: 'primary',
  },
  pending: {
    label: 'Loading...',
    disabled: true,
    variant: 'primary',
  },
  success: {
    label: 'Complete!',
    disabled: false,
    variant: 'success',
  },
  error: {
    label: 'Failed - try again',
    disabled: false,
    variant: 'danger',
  },
};

// Component using state machine
export function AsyncButton({
  onClick
}: {
  onClick: () => Promise<void>;
}) {
  const [state, setState] = useState<RequestState>('idle');

  const handleClick = async () => {
    // State transition: idle/error → pending
    setState('pending');

    try {
      await onClick();
      // State transition: pending → success
      setState('success');

      // Auto-reset after 2 seconds
      setTimeout(() => setState('idle'), 2000);
    } catch (error) {
      // State transition: pending → error
      setState('error');
    }
  };

  const config = stateConfig[state];

  return (
    <button
      onClick={handleClick}
      disabled={config.disabled}
      className={`btn btn-${config.variant}`}
    >
      {config.label}
    </button>
  );
}
```

### Advanced: Tagged Union with Data

For more complex states with state-specific data:

```typescript
// Tagged union with discriminated state
type AsyncState<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

function useAsyncOperation<T>(
  operation: () => Promise<T>
): {
  state: AsyncState<T>;
  execute: () => Promise<void>;
  reset: () => void;
} {
  const [state, setState] = useState<AsyncState<T>>({ status: 'idle' });

  const execute = async () => {
    setState({ status: 'loading' });

    try {
      const data = await operation();
      setState({ status: 'success', data });
    } catch (error) {
      setState({
        status: 'error',
        error: error instanceof Error ? error : new Error('Unknown error')
      });
    }
  };

  const reset = () => {
    setState({ status: 'idle' });
  };

  return { state, execute, reset };
}

// Usage in component
export function DataFetchButton() {
  const { state, execute, reset } = useAsyncOperation(async () => {
    const response = await fetch('/api/data');
    return response.json();
  });

  return (
    <div>
      <button onClick={execute} disabled={state.status === 'loading'}>
        Fetch Data
      </button>

      {state.status === 'loading' && <Spinner />}

      {state.status === 'success' && (
        <div>
          <pre>{JSON.stringify(state.data, null, 2)}</pre>
          <button onClick={reset}>Reset</button>
        </div>
      )}

      {state.status === 'error' && (
        <div className="error">
          {state.error.message}
          <button onClick={reset}>Try Again</button>
        </div>
      )}
    </div>
  );
}
```

### Why This Works

**Predictable State Transitions**:
- Explicit states prevent impossible states
- Clear state transition logic
- TypeScript ensures all states handled

**Type Safety**:
- Discriminated unions enable exhaustive checking
- State-specific data is type-safe
- Compiler catches missing state handlers

**Maintainability**:
- State configuration in one place
- Easy to add new states
- Clear separation of state and UI

### Common Triggers

Use this pattern when:
- "manage async operation states"
- "predictable UI state machine"
- "loading, success, error states"
- "prevent impossible states"
- "type-safe state management"

## Advanced Composition: Combining Patterns

### Complete Search Component

Combining debounced search, SWR fetching, and state machine:

```typescript
import { useState, useMemo } from 'react';
import useSWR from 'swr';

type SearchState = 'idle' | 'debouncing' | 'fetching' | 'success' | 'error';

export function AdvancedSearch() {
  const [searchInput, setSearchInput] = useState('');
  const debouncedInput = useDebounce(searchInput, 300);

  // Determine current state
  const isDebouncing = searchInput !== debouncedInput;

  // Conditional SWR fetching
  const { data, error, isLoading } = useSWR(
    debouncedInput.length >= 2
      ? `/api/search?q=${encodeURIComponent(debouncedInput)}`
      : null
  );

  // Compute search state
  const searchState = useMemo<SearchState>(() => {
    if (error) return 'error';
    if (isDebouncing) return 'debouncing';
    if (isLoading) return 'fetching';
    if (data) return 'success';
    return 'idle';
  }, [isDebouncing, isLoading, data, error]);

  // State-specific UI
  const showSpinner = searchState === 'debouncing' || searchState === 'fetching';
  const showResults = searchState === 'success';
  const showError = searchState === 'error';

  return (
    <div>
      <input
        type="text"
        value={searchInput}
        onChange={(e) => setSearchInput(e.target.value)}
        placeholder="Search..."
      />

      {showSpinner && <Spinner />}

      {showResults && (
        <SearchResults results={data.results} />
      )}

      {showError && (
        <ErrorMessage>Failed to fetch results</ErrorMessage>
      )}
    </div>
  );
}
```

## Anti-Patterns to Avoid

### ❌ Don't: Create New Objects in Render

```typescript
// BAD: New object on every render causes unnecessary re-renders
function MyProvider({ children }) {
  const [state, setState] = useState(null);

  return (
    <MyContext.Provider value={{ state, setState }}>
      {children}
    </MyContext.Provider>
  );
}
```

```typescript
// GOOD: Memoize the context value
function MyProvider({ children }) {
  const [state, setState] = useState(null);

  const value = useMemo(() => ({ state, setState }), [state]);

  return (
    <MyContext.Provider value={value}>
      {children}
    </MyContext.Provider>
  );
}
```

### ❌ Don't: Forget SWR Conditional Fetching

```typescript
// BAD: Fetches even with empty input
function useSearch(query: string) {
  const { data } = useSWR(`/api/search?q=${query}`);
  return data;
}
```

```typescript
// GOOD: Only fetch when query is valid
function useSearch(query: string) {
  const { data } = useSWR(
    query.trim().length >= 2 ? `/api/search?q=${query}` : null
  );
  return data;
}
```

### ❌ Don't: Ignore Debounce vs Loading State

```typescript
// BAD: Only shows loading during network request
function Search() {
  const [input, setInput] = useState('');
  const debounced = useDebounce(input, 300);
  const { data, isLoading } = useSWR(`/api?q=${debounced}`);

  // Spinner disappears while debouncing!
  return <>{isLoading && <Spinner />}</>;
}
```

```typescript
// GOOD: Show loading during both debounce and fetch
function Search() {
  const [input, setInput] = useState('');
  const debounced = useDebounce(input, 300);
  const { data, isLoading } = useSWR(`/api?q=${debounced}`);

  const isDebouncing = input !== debounced;
  const loading = isDebouncing || isLoading;

  return <>{loading && <Spinner />}</>;
}
```

### ❌ Don't: Use String States Without Type Safety

```typescript
// BAD: Easy to typo, no autocomplete
function Component() {
  const [status, setStatus] = useState('idel'); // Typo!

  if (status === 'idle') { // Won't match
    return <div>Ready</div>;
  }
}
```

```typescript
// GOOD: Use discriminated union
type Status = 'idle' | 'loading' | 'success' | 'error';

function Component() {
  const [status, setStatus] = useState<Status>('idle');

  if (status === 'idle') { // Type-safe
    return <div>Ready</div>;
  }
}
```

## Best Practices Summary

1. **Conditional SWR Keys**: Use `null` to prevent fetching when conditions aren't met
2. **Memoize Transformations**: Use `useMemo` for expensive data transformations
3. **Stable Callbacks**: Use `useCallback` for functions in context or dependencies
4. **Memoize Context Values**: Prevent unnecessary re-renders of context consumers
5. **Dual Loading States**: Track both debouncing and network loading separately
6. **Pure Helper Functions**: Extract logic outside components for testability
7. **Type-Safe States**: Use discriminated unions for state machines
8. **Explicit State Transitions**: Make state changes predictable and clear

## Related Patterns

See the `react-state-machine` skill for more advanced state machine patterns with XState.

## References

- [SWR Documentation](https://swr.vercel.app/)
- [React Hooks Documentation](https://react.dev/reference/react)
- [TypeScript Discriminated Unions](https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html#discriminating-unions)
