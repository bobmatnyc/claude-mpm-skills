# Testing React Hooks

## Testing Custom Hooks with React Testing Library

### Pattern: Basic Hook Testing

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  it('should debounce value updates', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 500 }
      }
    );

    expect(result.current).toBe('initial');

    // Update value
    rerender({ value: 'updated', delay: 500 });

    // Value should not change immediately
    expect(result.current).toBe('initial');

    // Fast-forward time
    jest.advanceTimersByTime(500);

    // Now value should be updated
    expect(result.current).toBe('updated');
  });

  it('should cancel previous debounce on rapid updates', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'first' } }
    );

    rerender({ value: 'second' });
    jest.advanceTimersByTime(300);

    rerender({ value: 'third' });
    jest.advanceTimersByTime(300);

    // Should still be initial
    expect(result.current).toBe('first');

    // Complete the debounce
    jest.advanceTimersByTime(200);

    // Should be final value
    expect(result.current).toBe('third');
  });
});
```

### Pattern: Testing SWR Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { SWRConfig } from 'swr';
import { useUserData } from './useUserData';

// Mock fetch
global.fetch = jest.fn();

describe('useUserData', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch user data', async () => {
    const mockUser = { id: '1', name: 'John Doe', email: 'john@example.com' };

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <SWRConfig value={{ provider: () => new Map() }}>
        {children}
      </SWRConfig>
    );

    const { result } = renderHook(() => useUserData('1'), { wrapper });

    // Initially loading
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBeUndefined();

    // Wait for data
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual(mockUser);
    expect(global.fetch).toHaveBeenCalledWith('/api/users/1');
  });

  it('should not fetch when userId is null', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <SWRConfig value={{ provider: () => new Map() }}>
        {children}
      </SWRConfig>
    );

    const { result } = renderHook(() => useUserData(null), { wrapper });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.data).toBeUndefined();
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('should handle errors', async () => {
    const mockError = new Error('Network error');

    (global.fetch as jest.Mock).mockRejectedValueOnce(mockError);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <SWRConfig value={{ provider: () => new Map() }}>
        {children}
      </SWRConfig>
    );

    const { result } = renderHook(() => useUserData('1'), { wrapper });

    await waitFor(() => {
      expect(result.current.error).toBeDefined();
    });

    expect(result.current.data).toBeUndefined();
  });
});
```

### Pattern: Testing Context Hooks

```typescript
import { renderHook, act } from '@testing-library/react';
import { UserLocationProvider, useUserLocation } from './UserLocationContext';

describe('useUserLocation', () => {
  it('should provide initial location', () => {
    const initialLocation = {
      latitude: 37.7749,
      longitude: -122.4194,
      accuracy: 'coarse' as const,
    };

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <UserLocationProvider location={initialLocation}>
        {children}
      </UserLocationProvider>
    );

    const { result } = renderHook(() => useUserLocation(), { wrapper });

    expect(result.current.location).toEqual(initialLocation);
  });

  it('should request precise location', async () => {
    const mockGeolocation = {
      getCurrentPosition: jest.fn(),
    };

    Object.defineProperty(global.navigator, 'geolocation', {
      value: mockGeolocation,
      configurable: true,
    });

    mockGeolocation.getCurrentPosition.mockImplementation((success) => {
      success({
        coords: {
          latitude: 37.7749,
          longitude: -122.4194,
          accuracy: 10,
        },
      });
    });

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <UserLocationProvider>
        {children}
      </UserLocationProvider>
    );

    const { result } = renderHook(() => useUserLocation(), { wrapper });

    let newLocation: any;

    await act(async () => {
      newLocation = await result.current.requestPreciseLocation();
    });

    expect(newLocation).toEqual({
      latitude: 37.7749,
      longitude: -122.4194,
      accuracy: 'precise',
    });

    expect(result.current.location).toEqual(newLocation);
  });

  it('should throw error when used outside provider', () => {
    // Suppress console.error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

    expect(() => {
      renderHook(() => useUserLocation());
    }).toThrow('useUserLocation must be used within UserLocationProvider');

    consoleSpy.mockRestore();
  });
});
```

## Testing Async State Machines

### Pattern: Testing State Transitions

```typescript
import { renderHook, act } from '@testing-library/react';
import { useAsyncOperation } from './useAsyncOperation';

describe('useAsyncOperation', () => {
  it('should transition through states correctly', async () => {
    const mockOperation = jest.fn().mockResolvedValue({ data: 'success' });

    const { result } = renderHook(() => useAsyncOperation(mockOperation));

    // Initial state
    expect(result.current.state).toEqual({ status: 'idle' });

    // Execute operation
    act(() => {
      result.current.execute();
    });

    // Should be loading
    expect(result.current.state).toEqual({ status: 'loading' });

    // Wait for success
    await waitFor(() => {
      expect(result.current.state.status).toBe('success');
    });

    expect(result.current.state).toEqual({
      status: 'success',
      data: { data: 'success' },
    });
  });

  it('should handle errors', async () => {
    const mockError = new Error('Operation failed');
    const mockOperation = jest.fn().mockRejectedValue(mockError);

    const { result } = renderHook(() => useAsyncOperation(mockOperation));

    act(() => {
      result.current.execute();
    });

    await waitFor(() => {
      expect(result.current.state.status).toBe('error');
    });

    expect(result.current.state).toEqual({
      status: 'error',
      error: mockError,
    });
  });

  it('should reset state', async () => {
    const mockOperation = jest.fn().mockResolvedValue({ data: 'success' });

    const { result } = renderHook(() => useAsyncOperation(mockOperation));

    // Execute and wait for success
    await act(async () => {
      await result.current.execute();
    });

    expect(result.current.state.status).toBe('success');

    // Reset
    act(() => {
      result.current.reset();
    });

    expect(result.current.state).toEqual({ status: 'idle' });
  });
});
```

## Mocking SWR

### Pattern: Custom SWR Provider for Tests

```typescript
import { SWRConfig, Cache } from 'swr';

export function createTestSWRConfig(initialData: Map<string, any> = new Map()) {
  const cache = new Map(initialData);

  return {
    value: {
      provider: () => cache as Cache,
      dedupingInterval: 0,
    },
  };
}

// Usage in tests
describe('Component with SWR', () => {
  it('should render with cached data', () => {
    const mockData = { id: '1', name: 'Test User' };
    const config = createTestSWRConfig(
      new Map([['/api/users/1', mockData]])
    );

    const { result } = renderHook(
      () => useUserData('1'),
      {
        wrapper: ({ children }) => (
          <SWRConfig {...config}>
            {children}
          </SWRConfig>
        ),
      }
    );

    // Data available immediately from cache
    expect(result.current.data).toEqual(mockData);
    expect(result.current.isLoading).toBe(false);
  });
});
```

## Testing Component Integration

### Pattern: Testing Components with Custom Hooks

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SearchComponent } from './SearchComponent';

jest.mock('swr', () => ({
  __esModule: true,
  default: jest.fn(),
}));

import useSWR from 'swr';

describe('SearchComponent', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  it('should debounce search input', async () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: [],
      isLoading: false,
      error: null,
    });

    const user = userEvent.setup({ delay: null });

    render(<SearchComponent />);

    const input = screen.getByPlaceholderText('Search...');

    // Type quickly
    await user.type(input, 'test');

    // Should not fetch yet
    expect(useSWR).toHaveBeenCalledWith(null);

    // Fast-forward debounce delay
    act(() => {
      jest.advanceTimersByTime(300);
    });

    // Now should fetch
    await waitFor(() => {
      expect(useSWR).toHaveBeenCalledWith(
        expect.stringContaining('test')
      );
    });
  });

  it('should show loading state while debouncing', async () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      isLoading: false,
      error: null,
    });

    const user = userEvent.setup({ delay: null });

    render(<SearchComponent />);

    const input = screen.getByPlaceholderText('Search...');

    await user.type(input, 'test');

    // Should show loading indicator
    expect(screen.getByRole('status')).toBeInTheDocument();

    // Complete debounce
    act(() => {
      jest.advanceTimersByTime(300);
    });

    // Loading indicator should persist if fetching
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    });
  });
});
```

## Testing Performance Optimizations

### Pattern: Verifying Memo Behavior

```typescript
import { render } from '@testing-library/react';
import { ExpensiveComponent } from './ExpensiveComponent';

describe('ExpensiveComponent memo behavior', () => {
  it('should not re-render when props do not change', () => {
    const renderSpy = jest.fn();

    function TestComponent({ data }: { data: any }) {
      renderSpy();
      return <ExpensiveComponent data={data} />;
    }

    const { rerender } = render(<TestComponent data={{ id: 1 }} />);

    expect(renderSpy).toHaveBeenCalledTimes(1);

    // Re-render with same props reference
    const sameData = { id: 1 };
    rerender(<TestComponent data={sameData} />);

    // Should re-render once for parent, memo should prevent child re-render
    expect(renderSpy).toHaveBeenCalledTimes(2);
  });
});
```

### Pattern: Testing useCallback Stability

```typescript
import { renderHook } from '@testing-library/react';

describe('useCallback stability', () => {
  it('should maintain callback reference', () => {
    const { result, rerender } = renderHook(
      ({ count }) => {
        const [localState, setLocalState] = useState(0);

        const stableCallback = useCallback(() => {
          console.log('callback');
        }, []);

        return { stableCallback, localState, setLocalState };
      },
      { initialProps: { count: 0 } }
    );

    const firstCallback = result.current.stableCallback;

    // Change unrelated prop
    rerender({ count: 1 });

    // Callback reference should be same
    expect(result.current.stableCallback).toBe(firstCallback);

    // Change local state
    act(() => {
      result.current.setLocalState(1);
    });

    // Callback reference should still be same
    expect(result.current.stableCallback).toBe(firstCallback);
  });
});
```

## Snapshot Testing for Hook Output

### Pattern: Hook Output Snapshots

```typescript
import { renderHook } from '@testing-library/react';

describe('useUserStats snapshots', () => {
  it('should match snapshot for user stats', () => {
    const mockUser = {
      id: '1',
      name: 'John Doe',
      posts: [
        { id: '1', likes: 10 },
        { id: '2', likes: 20 },
      ],
    };

    const { result } = renderHook(() => useUserStats(mockUser));

    expect(result.current).toMatchSnapshot();
  });
});
```

## End-to-End Testing with Playwright

### Pattern: Testing Complete User Flow

```typescript
import { test, expect } from '@playwright/test';

test.describe('Search with debounce', () => {
  test('should debounce search and show results', async ({ page }) => {
    await page.goto('/search');

    const searchInput = page.locator('input[placeholder="Search..."]');
    const loadingIndicator = page.locator('[role="status"]');

    // Type search query
    await searchInput.fill('test query');

    // Loading indicator should appear immediately
    await expect(loadingIndicator).toBeVisible();

    // Wait for debounce and results
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();

    // Should show results
    await expect(page.locator('[data-testid="result-item"]')).toHaveCount(5);
  });
});
```
