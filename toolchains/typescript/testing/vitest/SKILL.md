---
name: vitest
description: Vitest - Modern TypeScript testing framework with Vite-native performance, ESM support, and TypeScript-first design
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Modern TypeScript testing with Vitest: Vite-native, ESM-first, instant HMR, built-in TypeScript support, React/Vue component testing"
    when_to_use: "Testing TypeScript/JavaScript projects, React/Vue components, Vite-based projects, when migrating from Jest, when fast test execution is needed"
    quick_start: "1. npm install -D vitest 2. Create vitest.config.ts 3. Write *.test.ts files 4. Run: npx vitest"
context_limit: 700
tags:
  - testing
  - vitest
  - vite
  - typescript
  - unit-testing
  - component-testing
  - esm
requires_tools: []
---

# Vitest - Modern TypeScript Testing

## Overview

Vitest is a next-generation test framework powered by Vite, designed for modern TypeScript/JavaScript projects. It provides blazing-fast test execution through HMR-based test running, native ESM support, and first-class TypeScript integration.

**Key Features**:
- ⚡ **Vite-native**: Instant HMR-based test execution (10-100x faster than Jest)
- 🎯 **TypeScript-first**: Built-in TypeScript support, no configuration needed
- 🔄 **ESM-native**: Native ES modules, async/await, top-level await
- 🧪 **Jest-compatible**: Compatible API for easy migration
- 📸 **Snapshot testing**: Built-in snapshot support
- 🎨 **Component testing**: React Testing Library, Vue Test Utils integration
- 📊 **Coverage**: Built-in v8/c8 coverage (faster than Istanbul)
- 🌐 **UI mode**: Beautiful web UI for test debugging

**Installation**:
```bash
npm install -D vitest
# TypeScript types (usually auto-detected)
npm install -D @vitest/ui  # Optional: UI mode
```

## Basic Setup

### 1. Configure Vitest

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,           // Use describe/it/expect globally
    environment: 'node',     // or 'jsdom' for DOM testing
    coverage: {
      provider: 'v8',        // or 'istanbul'
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.test.ts',
        '**/*.spec.ts',
      ],
    },
    include: ['**/*.{test,spec}.{ts,tsx}'],
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
  },
});
```

### 2. TypeScript Configuration

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]  // For global describe/it/expect
  }
}
```

**Alternative (without globals)**:
```typescript
import { describe, it, expect } from 'vitest';
```

### 3. Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",              // CI mode (single run)
    "test:watch": "vitest",            // Watch mode (default)
    "test:ui": "vitest --ui",          // UI mode
    "test:coverage": "vitest run --coverage"
  }
}
```

## Core Testing Patterns

### Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  it('adds two numbers correctly', () => {
    const result = calculator.add(2, 3);
    expect(result).toBe(5);
  });

  it('handles negative numbers', () => {
    expect(calculator.add(-5, 3)).toBe(-2);
  });
});
```

### TypeScript Type Testing

```typescript
import { describe, it, expectTypeOf, assertType } from 'vitest';

interface User {
  id: number;
  name: string;
  email: string;
}

describe('Type Safety', () => {
  it('ensures correct types', () => {
    const user: User = {
      id: 1,
      name: 'Alice',
      email: 'alice@example.com',
    };

    // Type assertions
    expectTypeOf(user.id).toBeNumber();
    expectTypeOf(user.name).toBeString();
    expectTypeOf(user).toMatchTypeOf<User>();

    // Assert type at compile time
    assertType<User>(user);
  });

  it('checks function return types', () => {
    function getUser(): User {
      return { id: 1, name: 'Bob', email: 'bob@example.com' };
    }

    expectTypeOf(getUser).returns.toMatchTypeOf<User>();
  });
});
```

## Mocking and Spies

### vi.mock for Module Mocking

```typescript
import { describe, it, expect, vi } from 'vitest';
import { fetchUser } from './api';
import { UserService } from './UserService';

// Mock entire module
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}));

describe('UserService', () => {
  it('fetches user data', async () => {
    const mockUser = { id: 1, name: 'Alice' };
    vi.mocked(fetchUser).mockResolvedValue(mockUser);

    const service = new UserService();
    const user = await service.getUser(1);

    expect(fetchUser).toHaveBeenCalledWith(1);
    expect(user).toEqual(mockUser);
  });
});
```

### vi.spyOn for Method Spying

```typescript
import { describe, it, expect, vi } from 'vitest';

class Logger {
  log(message: string) {
    console.log(message);
  }
}

describe('Logger Spy', () => {
  it('tracks method calls', () => {
    const logger = new Logger();
    const spy = vi.spyOn(logger, 'log');

    logger.log('Hello');
    logger.log('World');

    expect(spy).toHaveBeenCalledTimes(2);
    expect(spy).toHaveBeenCalledWith('Hello');
    expect(spy).toHaveBeenLastCalledWith('World');

    spy.mockRestore(); // Restore original implementation
  });
});
```

### Mock Implementation

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('Mock Implementation', () => {
  it('provides custom mock implementation', () => {
    const mockFn = vi.fn((x: number) => x * 2);

    expect(mockFn(5)).toBe(10);
    expect(mockFn).toHaveBeenCalledWith(5);

    // Change implementation
    mockFn.mockImplementation((x: number) => x + 10);
    expect(mockFn(5)).toBe(15);

    // One-time implementation
    mockFn.mockImplementationOnce((x: number) => 100);
    expect(mockFn(5)).toBe(100);
    expect(mockFn(5)).toBe(15); // Back to default
  });
});
```

### Mocking Timers

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('Timer Mocking', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('fast-forwards time', () => {
    const callback = vi.fn();
    setTimeout(callback, 1000);

    vi.advanceTimersByTime(500);
    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(500);
    expect(callback).toHaveBeenCalledTimes(1);
  });

  it('runs all timers', async () => {
    const callback = vi.fn();
    setTimeout(callback, 1000);
    setTimeout(callback, 2000);

    await vi.runAllTimersAsync();
    expect(callback).toHaveBeenCalledTimes(2);
  });
});
```

## React Testing Integration

### Setup React Testing Library

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D jsdom  # For DOM environment
```

**vitest.config.ts** (React):
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
});
```

**src/test/setup.ts**:
```typescript
import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});
```

### React Component Testing

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter Component', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={0} />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('increments counter on button click', async () => {
    const user = userEvent.setup();
    render(<Counter initialCount={0} />);

    const button = screen.getByRole('button', { name: /increment/i });
    await user.click(button);

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('calls onChange callback', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();

    render(<Counter initialCount={0} onChange={onChange} />);

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(onChange).toHaveBeenCalledWith(1);
  });
});
```

### Testing Hooks

```typescript
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter Hook', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter(0));
    expect(result.current.count).toBe(0);
  });

  it('increments counter', () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('resets counter', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

## Vue Testing Integration

### Setup Vue Test Utils

```bash
npm install -D @vue/test-utils @vitejs/plugin-vue
npm install -D happy-dom  # Faster alternative to jsdom
```

**vitest.config.ts** (Vue):
```typescript
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: './src/test/setup.ts',
  },
});
```

### Vue Component Testing

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Counter from './Counter.vue';

describe('Counter.vue', () => {
  it('renders initial count', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 5 },
    });

    expect(wrapper.text()).toContain('Count: 5');
  });

  it('increments on button click', async () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 0 },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.text()).toContain('Count: 1');
  });

  it('emits update event', async () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 0 },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.emitted('update')).toBeTruthy();
    expect(wrapper.emitted('update')?.[0]).toEqual([1]);
  });
});
```

## Async Testing

### Testing Promises

```typescript
import { describe, it, expect } from 'vitest';

describe('Async Operations', () => {
  it('resolves promises', async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });

  it('rejects promises', async () => {
    await expect(Promise.reject(new Error('Failed'))).rejects.toThrow('Failed');
  });

  it('uses resolves matcher', async () => {
    await expect(Promise.resolve(42)).resolves.toBe(42);
  });
});
```

### Testing Async Functions

```typescript
import { describe, it, expect, vi } from 'vitest';

async function fetchData(id: number): Promise<string> {
  const response = await fetch(`/api/data/${id}`);
  return response.json();
}

describe('Async Functions', () => {
  it('fetches data successfully', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve('data'),
      } as Response)
    );

    const data = await fetchData(1);
    expect(data).toBe('data');
    expect(fetch).toHaveBeenCalledWith('/api/data/1');
  });

  it('handles fetch errors', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('Network error')));

    await expect(fetchData(1)).rejects.toThrow('Network error');
  });
});
```

## Snapshot Testing

### Basic Snapshots

```typescript
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard Snapshots', () => {
  it('matches snapshot', () => {
    const { container } = render(
      <UserCard name="Alice" email="alice@example.com" />
    );

    expect(container.firstChild).toMatchSnapshot();
  });

  it('matches inline snapshot', () => {
    const user = { id: 1, name: 'Bob' };
    expect(user).toMatchInlineSnapshot(`
      {
        "id": 1,
        "name": "Bob",
      }
    `);
  });
});
```

### Snapshot Serializers

```typescript
import { describe, it, expect } from 'vitest';

expect.addSnapshotSerializer({
  test: (val) => val && typeof val.toISOString === 'function',
  print: (val) => `Date(${(val as Date).toISOString()})`,
});

describe('Custom Serializers', () => {
  it('serializes dates consistently', () => {
    const data = {
      timestamp: new Date('2024-01-01T00:00:00.000Z'),
      user: 'Alice',
    };

    expect(data).toMatchSnapshot();
  });
});
```

## Coverage Configuration

### Advanced Coverage Setup

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.test.ts',
        '**/*.spec.ts',
        '**/*.config.ts',
        '**/types/',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
      all: true,  // Include untested files in coverage report
    },
  },
});
```

### Running Coverage

```bash
# Generate coverage
npx vitest run --coverage

# Coverage with UI
npx vitest --coverage --ui

# Specific threshold enforcement
npx vitest run --coverage --coverage.lines=90
```

## Migration from Jest

### API Compatibility

Vitest provides Jest-compatible API:

```typescript
// Jest syntax works in Vitest
import { describe, it, expect, jest } from 'vitest';

// Note: Use 'vi' instead of 'jest' for new code
import { describe, it, expect, vi } from 'vitest';

// Both work, but vi is preferred
const mockFn = vi.fn();  // Preferred
const mockFn2 = jest.fn();  // Also works
```

### Migration Checklist

**1. Update Dependencies**:
```bash
npm uninstall jest @types/jest ts-jest
npm install -D vitest @vitest/ui
```

**2. Update package.json**:
```json
{
  "scripts": {
    "test": "vitest run",  // Was: jest
    "test:watch": "vitest"  // Was: jest --watch
  }
}
```

**3. Replace jest.config.js with vitest.config.ts**:
```typescript
// Old: jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
};

// New: vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
});
```

**4. Update Test Files**:
```typescript
// Change imports
- import { jest } from '@jest/globals';
+ import { vi } from 'vitest';

// Update mocks
- jest.fn()
+ vi.fn()

- jest.spyOn()
+ vi.spyOn()

- jest.mock()
+ vi.mock()
```

## Advanced Patterns

### Concurrent Testing

```typescript
import { describe, it, expect } from 'vitest';

describe.concurrent('Parallel Tests', () => {
  it('test 1', async () => {
    await slowOperation();
    expect(true).toBe(true);
  });

  it('test 2', async () => {
    await slowOperation();
    expect(true).toBe(true);
  });

  // Both tests run in parallel
});
```

### Test Context

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

interface TestContext {
  user: { id: number; name: string };
  api: ApiClient;
}

describe<TestContext>('With Context', () => {
  beforeEach((context) => {
    context.user = { id: 1, name: 'Alice' };
    context.api = new ApiClient();
  });

  it<TestContext>('uses context', ({ user, api }) => {
    expect(user.name).toBe('Alice');
    expect(api).toBeDefined();
  });
});
```

### Custom Matchers

```typescript
import { expect } from 'vitest';

expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be within range ${floor} - ${ceiling}`
          : `expected ${received} to be within range ${floor} - ${ceiling}`,
    };
  },
});

// Usage
expect(100).toBeWithinRange(90, 110);
```

## Best Practices

1. **Use globals: true** - Simpler imports, Jest-compatible
2. **Prefer vi over jest** - Use Vitest-native API for new code
3. **Use v8 coverage** - Faster than Istanbul, works with native ESM
4. **Test in isolation** - Each test should be independent
5. **Mock external dependencies** - Network, file system, timers
6. **Use TypeScript** - Full type safety in tests
7. **Run tests in CI mode** - Use `vitest run` for CI, not watch mode
8. **Leverage UI mode** - Debug failing tests visually
9. **Use describe.concurrent** - Parallelize independent tests
10. **Keep tests focused** - One assertion per test when possible

## Common Pitfalls

❌ **Not using CI mode in CI/CD**:
```json
// WRONG - watch mode hangs in CI
"test": "vitest"

// CORRECT - single run
"test": "vitest run"
```

✅ **Correct approach**:
```json
{
  "scripts": {
    "test": "vitest run",       // CI-safe
    "test:watch": "vitest",     // Development
    "test:ui": "vitest --ui"    // Debugging
  }
}
```

❌ **Forgetting to await async tests**:
```typescript
// WRONG - test passes before assertion
it('fetches data', () => {
  fetchData().then(data => {
    expect(data).toBeDefined();  // Never runs!
  });
});

// CORRECT
it('fetches data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});
```

❌ **Not cleaning up mocks**:
```typescript
// WRONG - mocks leak between tests
it('test 1', () => {
  vi.spyOn(console, 'log');
  // No cleanup!
});

// CORRECT
import { afterEach } from 'vitest';

afterEach(() => {
  vi.restoreAllMocks();
});
```

❌ **Using wrong environment**:
```typescript
// WRONG - testing DOM in node environment
test: {
  environment: 'node',  // Can't test React components!
}

// CORRECT
test: {
  environment: 'jsdom',  // For React/Vue components
}
```

## Resources

- **Documentation**: https://vitest.dev
- **API Reference**: https://vitest.dev/api/
- **Migration Guide**: https://vitest.dev/guide/migration.html
- **Examples**: https://github.com/vitest-dev/vitest/tree/main/examples
- **UI Mode**: https://vitest.dev/guide/ui.html

## Related Skills

When using Vitest, consider these complementary skills:

- **typescript-core**: Advanced TypeScript type patterns, tsconfig, and runtime validation
- **react**: React component testing with Testing Library integration
- **test-driven-development**: Complete TDD workflow (RED/GREEN/REFACTOR cycle)

### Quick TypeScript Type Patterns (Inlined for Standalone Use)

```typescript
// Type-safe test factories with generics
function createMockData<T extends Record<string, unknown>>(
  defaults: T,
  overrides?: Partial<T>
): T {
  return { ...defaults, ...overrides };
}

const mockUser = createMockData(
  { id: 1, name: 'Test', email: 'test@example.com' },
  { name: 'Alice' }
);

// Runtime validation with Zod in tests
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
});

test('API returns valid user', async () => {
  const response = await fetch('/api/user/1');
  const data = await response.json();

  // Runtime validation + type inference
  const user = UserSchema.parse(data);
  expect(user.email).toContain('@');
});

// Const type parameters for literal inference
const createTestConfig = <const T extends Record<string, unknown>>(config: T): T => config;
const testEnv = createTestConfig({ mode: 'test', debug: false });
// Type: { mode: "test"; debug: false } (literals preserved)
```

### Quick React Testing Patterns (Inlined for Standalone Use)

```typescript
// React Testing Library with Vitest
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { describe, test, expect, vi } from 'vitest';

// Component testing
describe('UserProfile', () => {
  test('renders user information', () => {
    const user = { id: 1, name: 'Alice', email: 'alice@example.com' };
    render(<UserProfile user={user} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
  });

  test('handles form submission', async () => {
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    const user = userEvent.setup();
    await user.type(screen.getByLabelText('Name'), 'Bob');
    await user.click(screen.getByRole('button', { name: 'Submit' }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({ name: 'Bob' });
    });
  });
});

// Hook testing
import { renderHook, act } from '@testing-library/react';

test('useCounter hook increments', () => {
  const { result } = renderHook(() => useCounter(0));

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

### Quick TDD Workflow Reference (Inlined for Standalone Use)

**RED → GREEN → REFACTOR Cycle:**

1. **RED Phase: Write Failing Test**
   ```typescript
   test('should authenticate user with valid credentials', () => {
     const user = { username: 'alice', password: 'secret123' };
     const result = authenticate(user);
     expect(result.isAuthenticated).toBe(true);
     // This fails because authenticate() doesn't exist yet
   });
   ```

2. **GREEN Phase: Make It Pass**
   ```typescript
   function authenticate(user: User): AuthResult {
     // Minimum code to pass the test
     if (user.username === 'alice' && user.password === 'secret123') {
       return { isAuthenticated: true };
     }
     return { isAuthenticated: false };
   }
   ```

3. **REFACTOR Phase: Improve Code**
   ```typescript
   function authenticate(user: User): AuthResult {
     // Clean up while keeping tests green
     const hashed = hashPassword(user.password);
     const storedUser = database.getUser(user.username);
     return {
       isAuthenticated: storedUser?.passwordHash === hashed
     };
   }
   ```

**Test Structure: Arrange-Act-Assert (AAA)**
```typescript
test('creates user successfully', async () => {
  // Arrange: Set up test data
  const userData = { username: 'alice', email: 'alice@example.com' };

  // Act: Perform the action
  const user = await createUser(userData);

  // Assert: Verify outcome
  expect(user.username).toBe('alice');
  expect(user.email).toBe('alice@example.com');
});
```

**Vitest-Specific TDD Features:**
```typescript
// Watch mode with HMR (instant feedback)
// vitest --watch

// UI mode for visual debugging
// vitest --ui

// Run only changed tests
// vitest --changed

// Benchmark mode for performance testing
import { bench } from 'vitest';

bench('authenticate performance', () => {
  authenticate({ username: 'alice', password: 'secret' });
});
```

[Full TypeScript, React, and TDD workflows available in respective skills if deployed together]

## Summary

- **Vitest** is the modern standard for TypeScript testing
- **10-100x faster** than Jest through Vite-native HMR
- **ESM-first** with native module support
- **Jest-compatible** API for easy migration
- **TypeScript-first** with built-in type support
- **Component testing** for React and Vue
- **v8 coverage** faster than Istanbul
- **UI mode** for visual test debugging
- **Perfect for**: Modern TypeScript projects, Vite-based apps, React/Vue components
