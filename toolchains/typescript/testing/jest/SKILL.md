---
name: jest-typescript
description: Jest with TypeScript - Industry standard testing framework with 70% market share, mature ecosystem, React Testing Library integration
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "TypeScript testing with Jest - industry standard testing framework with mature ecosystem, React Testing Library, snapshot testing, built-in coverage"
    when_to_use: "Testing existing Jest projects, React/Node.js with TypeScript, using Jest ecosystem tools, migrating from JavaScript to TypeScript, legacy project support"
    quick_start: "1. npm install -D jest @types/jest ts-jest 2. npx ts-jest config:init 3. Create *.test.ts files 4. npm test"
context_limit: 700
tags:
  - testing
  - jest
  - typescript
  - react-testing-library
  - legacy
requires_tools: []
---

# Jest + TypeScript - Industry Standard Testing

## Overview

Jest is the industry-standard testing framework with 70% market share, providing a mature, battle-tested ecosystem for TypeScript projects. It offers comprehensive testing capabilities with built-in snapshot testing, mocking, and coverage reporting.

**Key Features**:
- 🏆 **Industry Standard**: 70% market share, widely adopted
- 📦 **All-in-One**: Test runner, assertions, mocks, coverage in one package
- 📸 **Snapshot Testing**: Built-in snapshot support for UI testing
- 🧪 **React Integration**: React Testing Library, enzyme compatibility
- 🔧 **Mature Ecosystem**: Extensive plugins, tooling, and community support
- 🎯 **TypeScript Support**: Full type safety via ts-jest
- 🔍 **Coverage Reports**: Built-in Istanbul coverage
- 🌐 **Multi-Platform**: Node.js, browser (jsdom), React Native

**Installation**:
```bash
npm install -D jest @types/jest ts-jest
npm install -D @testing-library/react @testing-library/jest-dom  # For React
```

## Basic Setup

### 1. Initialize Jest Configuration

```bash
npx ts-jest config:init
```

This creates **jest.config.js**:
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
};
```

### 2. Manual Configuration

**jest.config.ts** (TypeScript config):
```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/__tests__/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};

export default config;
```

### 3. TypeScript Configuration

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "types": ["jest", "@testing-library/jest-dom"],
    "esModuleInterop": true
  }
}
```

**tsconfig.test.json** (test-specific):
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "types": ["jest", "node", "@testing-library/jest-dom"]
  },
  "include": ["src/**/*.test.ts", "src/**/*.spec.ts", "src/**/__tests__/**"]
}
```

### 4. Package.json Scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2"
  }
}
```

## Core Testing Patterns

### Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  afterEach(() => {
    // Cleanup
  });

  it('adds two numbers correctly', () => {
    const result = calculator.add(2, 3);
    expect(result).toBe(5);
  });

  it('handles negative numbers', () => {
    expect(calculator.add(-5, 3)).toBe(-2);
  });

  it.each([
    [1, 1, 2],
    [2, 3, 5],
    [10, -5, 5],
  ])('adds %i + %i to equal %i', (a, b, expected) => {
    expect(calculator.add(a, b)).toBe(expected);
  });
});
```

### TypeScript Type-Safe Tests

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

describe('User Service', () => {
  it('creates user with correct types', () => {
    const user: User = {
      id: 1,
      name: 'Alice',
      email: 'alice@example.com',
      role: 'admin',
    };

    // Type-safe assertions
    expect(user.id).toEqual(expect.any(Number));
    expect(user.name).toEqual(expect.any(String));
    expect(user.role).toMatch(/^(admin|user)$/);
  });

  it('validates user object shape', () => {
    const user = createUser('Bob', 'bob@example.com');

    expect(user).toMatchObject({
      id: expect.any(Number),
      name: 'Bob',
      email: 'bob@example.com',
    });
  });
});
```

## Mocking with TypeScript

### jest.mock for Module Mocking

```typescript
import { jest } from '@jest/globals';
import { UserService } from './UserService';
import * as userApi from './api/userApi';

// Mock entire module
jest.mock('./api/userApi');

describe('UserService with Mocks', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('fetches user data', async () => {
    const mockUser = { id: 1, name: 'Alice', email: 'alice@example.com' };

    // Type-safe mock
    const mockedFetchUser = jest.mocked(userApi.fetchUser);
    mockedFetchUser.mockResolvedValue(mockUser);

    const service = new UserService();
    const user = await service.getUser(1);

    expect(mockedFetchUser).toHaveBeenCalledWith(1);
    expect(user).toEqual(mockUser);
  });
});
```

### jest.spyOn for Method Spying

```typescript
import { jest } from '@jest/globals';

class Logger {
  log(message: string): void {
    console.log(message);
  }

  error(message: string): void {
    console.error(message);
  }
}

describe('Logger Spy', () => {
  let logger: Logger;
  let logSpy: jest.SpyInstance;

  beforeEach(() => {
    logger = new Logger();
    logSpy = jest.spyOn(logger, 'log');
  });

  afterEach(() => {
    logSpy.mockRestore();
  });

  it('tracks method calls', () => {
    logger.log('Hello');
    logger.log('World');

    expect(logSpy).toHaveBeenCalledTimes(2);
    expect(logSpy).toHaveBeenCalledWith('Hello');
    expect(logSpy).toHaveBeenLastCalledWith('World');
  });

  it('provides custom implementation', () => {
    logSpy.mockImplementation((msg: string) => {
      console.log(`[CUSTOM] ${msg}`);
    });

    logger.log('Test');
    expect(logSpy).toHaveBeenCalledWith('Test');
  });
});
```

### Type-Safe Mock Functions

```typescript
import { jest } from '@jest/globals';

interface ApiResponse<T> {
  data: T;
  status: number;
}

type FetchUserFn = (id: number) => Promise<ApiResponse<User>>;

describe('Type-Safe Mocks', () => {
  it('creates typed mock function', async () => {
    const mockFetchUser = jest.fn<FetchUserFn>()
      .mockResolvedValue({
        data: { id: 1, name: 'Alice', email: 'alice@example.com', role: 'user' },
        status: 200,
      });

    const result = await mockFetchUser(1);

    expect(result.data.name).toBe('Alice');
    expect(result.status).toBe(200);
    expect(mockFetchUser).toHaveBeenCalledWith(1);
  });

  it('uses mock implementation', () => {
    const mockCalculate = jest.fn<(x: number, y: number) => number>()
      .mockImplementation((x, y) => x + y);

    expect(mockCalculate(5, 3)).toBe(8);
    expect(mockCalculate).toHaveBeenCalledWith(5, 3);
  });
});
```

### Mocking Timers

```typescript
import { jest } from '@jest/globals';

describe('Timer Mocking', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('fast-forwards time', () => {
    const callback = jest.fn();
    setTimeout(callback, 1000);

    jest.advanceTimersByTime(500);
    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(500);
    expect(callback).toHaveBeenCalledTimes(1);
  });

  it('runs all timers', () => {
    const callback = jest.fn();
    setTimeout(callback, 1000);
    setTimeout(callback, 2000);

    jest.runAllTimers();
    expect(callback).toHaveBeenCalledTimes(2);
  });

  it('handles intervals', () => {
    const callback = jest.fn();
    setInterval(callback, 1000);

    jest.advanceTimersByTime(3500);
    expect(callback).toHaveBeenCalledTimes(3);

    jest.clearAllTimers();
  });
});
```

## React Testing Library + TypeScript

### Setup for React

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D jest-environment-jsdom
```

**jest.config.ts** (React):
```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react-jsx',
      },
    }],
  },
};

export default config;
```

**src/test/setup.ts**:
```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from '@jest/globals';

afterEach(() => {
  cleanup();
});
```

### React Component Testing

```typescript
import { render, screen, waitFor } from '@testing-library/react';
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

  it('calls onChange callback with correct value', async () => {
    const onChange = jest.fn();
    const user = userEvent.setup();

    render(<Counter initialCount={5} onChange={onChange} />);

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(onChange).toHaveBeenCalledWith(6);
    expect(onChange).toHaveBeenCalledTimes(1);
  });

  it('disables button when max count reached', () => {
    render(<Counter initialCount={10} maxCount={10} />);

    const button = screen.getByRole('button', { name: /increment/i });
    expect(button).toBeDisabled();
  });
});
```

### Testing Hooks

```typescript
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

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(12);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

### Testing Async Components

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';
import * as api from './api';

jest.mock('./api');

describe('UserProfile Async', () => {
  it('loads and displays user data', async () => {
    const mockUser = { id: 1, name: 'Alice', email: 'alice@example.com' };
    jest.mocked(api.fetchUser).mockResolvedValue(mockUser);

    render(<UserProfile userId={1} />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
    });

    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
  });

  it('displays error on fetch failure', async () => {
    jest.mocked(api.fetchUser).mockRejectedValue(new Error('Network error'));

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

## Snapshot Testing

### Component Snapshots

```typescript
import { render } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard Snapshots', () => {
  it('matches snapshot for regular user', () => {
    const { container } = render(
      <UserCard
        name="Alice"
        email="alice@example.com"
        role="user"
      />
    );

    expect(container.firstChild).toMatchSnapshot();
  });

  it('matches snapshot for admin user', () => {
    const { container } = render(
      <UserCard
        name="Bob"
        email="bob@example.com"
        role="admin"
      />
    );

    expect(container.firstChild).toMatchSnapshot();
  });

  it('uses inline snapshot', () => {
    const user = { id: 1, name: 'Charlie', role: 'user' };

    expect(user).toMatchInlineSnapshot(`
      {
        "id": 1,
        "name": "Charlie",
        "role": "user",
      }
    `);
  });
});
```

### Updating Snapshots

```bash
# Update all snapshots
jest --updateSnapshot
jest -u

# Update snapshots for specific test file
jest UserCard.test.tsx -u

# Interactive snapshot update
jest --watch
# Press 'u' to update failing snapshots
```

### Custom Snapshot Serializers

```typescript
// __tests__/serializers/dateSerializer.ts
export default {
  test: (val: any) => val instanceof Date,
  print: (val: Date) => `Date(${val.toISOString()})`,
};
```

**jest.config.ts**:
```typescript
const config: Config = {
  snapshotSerializers: ['<rootDir>/__tests__/serializers/dateSerializer.ts'],
};
```

## Async Testing

### Testing Promises

```typescript
import { fetchData, saveData } from './api';

describe('Async Operations', () => {
  it('resolves with data', async () => {
    const data = await fetchData(1);
    expect(data).toBeDefined();
    expect(data.id).toBe(1);
  });

  it('handles promise rejection', async () => {
    await expect(fetchData(-1)).rejects.toThrow('Invalid ID');
  });

  it('uses resolves matcher', async () => {
    await expect(fetchData(1)).resolves.toHaveProperty('id', 1);
  });

  it('tests multiple async operations', async () => {
    const [user, posts] = await Promise.all([
      fetchUser(1),
      fetchPosts(1),
    ]);

    expect(user.id).toBe(1);
    expect(posts).toHaveLength(expect.any(Number));
  });
});
```

### Testing Callbacks

```typescript
describe('Callback Testing', () => {
  it('calls callback with correct arguments', (done) => {
    function fetchWithCallback(id: number, callback: (data: any) => void) {
      setTimeout(() => {
        callback({ id, name: 'Test' });
      }, 100);
    }

    fetchWithCallback(1, (data) => {
      try {
        expect(data.id).toBe(1);
        expect(data.name).toBe('Test');
        done();
      } catch (error) {
        done(error);
      }
    });
  });
});
```

## Coverage Configuration

### Advanced Coverage Setup

**jest.config.ts**:
```typescript
const config: Config = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageProvider: 'v8', // or 'babel' for compatibility
  coverageReporters: ['text', 'lcov', 'html', 'json'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/__tests__/**',
    '!src/index.ts',
    '!src/types/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    './src/core/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
  },
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/__tests__/',
  ],
};
```

### Running Coverage

```bash
# Generate coverage report
npm test -- --coverage

# Coverage with watch mode
npm test -- --coverage --watch

# Coverage for specific files
npm test -- --coverage --collectCoverageFrom="src/components/**/*.tsx"

# View HTML report
open coverage/lcov-report/index.html
```

## Migration from Vitest

### Key Differences

**API Changes**:
```typescript
// Vitest
import { vi } from 'vitest';
const mockFn = vi.fn();
vi.spyOn(obj, 'method');

// Jest
import { jest } from '@jest/globals';
const mockFn = jest.fn();
jest.spyOn(obj, 'method');
```

### Migration Checklist

**1. Update Dependencies**:
```bash
npm uninstall vitest @vitest/ui
npm install -D jest @types/jest ts-jest
```

**2. Update package.json**:
```json
{
  "scripts": {
    "test": "jest",           // Was: vitest run
    "test:watch": "jest --watch"  // Was: vitest
  }
}
```

**3. Replace vitest.config.ts with jest.config.ts**:
```typescript
// Old: vitest.config.ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
  },
});

// New: jest.config.ts
import type { Config } from 'jest';
const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  globals: {
    'ts-jest': {
      isolatedModules: true,
    },
  },
};
export default config;
```

**4. Update Test Files**:
```typescript
// Change imports
- import { vi } from 'vitest';
+ import { jest } from '@jest/globals';

// Update mocks
- vi.fn()
+ jest.fn()

- vi.spyOn()
+ jest.spyOn()

- vi.mock()
+ jest.mock()

// Timer mocks
- vi.useFakeTimers()
+ jest.useFakeTimers()

- vi.advanceTimersByTime()
+ jest.advanceTimersByTime()
```

**5. Update tsconfig.json**:
```json
{
  "compilerOptions": {
    "types": ["jest", "@testing-library/jest-dom"]  // Was: vitest/globals
  }
}
```

## Jest vs Vitest Comparison

### Performance

**Jest**:
- Slower initial startup (no HMR)
- Sequential test execution by default
- 1-5 seconds for medium projects

**Vitest**:
- Instant HMR-based execution
- Parallel by default
- 100-500ms for same projects

### Ecosystem

**Jest**:
- ✅ 70% market share
- ✅ Mature ecosystem (8+ years)
- ✅ More Stack Overflow answers
- ✅ Better corporate support

**Vitest**:
- ✅ Modern, growing adoption
- ✅ Vite-native integration
- ⚠️ Smaller ecosystem
- ⚠️ Fewer resources

### TypeScript Support

**Jest**:
- Requires ts-jest configuration
- Extra transform step
- Slower compilation

**Vitest**:
- Built-in TypeScript support
- No configuration needed
- Faster through Vite

### When to Use Jest

Choose Jest for:
- ✅ Existing projects already using Jest
- ✅ Corporate environments requiring proven tools
- ✅ Projects requiring extensive ecosystem support
- ✅ React projects with Create React App
- ✅ Non-Vite build systems (Webpack, Rollup)

Choose Vitest for:
- ✅ New projects with modern tooling
- ✅ Vite-based applications
- ✅ Performance-critical test suites
- ✅ ESM-first projects

## Best Practices

1. **Use TypeScript Configuration**: Type-safe tests prevent runtime errors
2. **Mock External Dependencies**: Network, file system, databases
3. **Isolate Tests**: Each test should be independent
4. **Use describe Blocks**: Group related tests logically
5. **Clear Mock State**: Use `jest.clearAllMocks()` in `beforeEach`
6. **Test Edge Cases**: Empty arrays, null, undefined, errors
7. **Use .each for Data-Driven Tests**: Test multiple inputs efficiently
8. **Avoid Testing Implementation**: Test behavior, not internal structure
9. **Keep Tests Fast**: Mock slow operations, use parallel execution
10. **Maintain Coverage Thresholds**: Enforce minimum coverage in CI

## Common Pitfalls

❌ **Not clearing mocks between tests**:
```typescript
// WRONG - mocks leak between tests
it('test 1', () => {
  jest.spyOn(api, 'fetch');
  // No cleanup!
});

// CORRECT
afterEach(() => {
  jest.restoreAllMocks();
});
```

❌ **Forgetting to await async tests**:
```typescript
// WRONG - test completes before assertion
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

❌ **Using wrong test environment**:
```typescript
// WRONG - testing DOM without jsdom
// jest.config.ts
testEnvironment: 'node',  // Can't test React!

// CORRECT
testEnvironment: 'jsdom',
```

❌ **Not using TypeScript types for mocks**:
```typescript
// WRONG - no type safety
const mockFn = jest.fn();

// CORRECT
const mockFn = jest.fn<(id: number) => Promise<User>>();
```

## Resources

- **Documentation**: https://jestjs.io/docs/getting-started
- **TypeScript Guide**: https://jestjs.io/docs/getting-started#using-typescript
- **ts-jest**: https://kulshekhar.github.io/ts-jest/
- **React Testing Library**: https://testing-library.com/docs/react-testing-library/intro/
- **Jest DOM Matchers**: https://github.com/testing-library/jest-dom

## Related Skills

When using Jest, consider these complementary skills:

- **typescript-core**: Advanced TypeScript patterns, tsconfig optimization, and type safety
- **react**: React component testing patterns with Testing Library
- **vitest**: Modern alternative with Vite-native performance and faster execution

### Quick TypeScript Type Safety Reference (Inlined for Standalone Use)

```typescript
// Type-safe test helpers with generics
function createMockUser<T extends Partial<User>>(overrides: T): User & T {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  };
}

// Usage with type inference
const adminUser = createMockUser({ role: 'admin' });
// Type: User & { role: string }

// Type-safe mock functions
const mockFetch = jest.fn<typeof fetch>();
mockFetch.mockResolvedValue(new Response('{}'));

// Const type parameters for literal types
const createConfig = <const T extends Record<string, unknown>>(config: T): T => config;
const testConfig = createConfig({ environment: 'test', debug: true });
// Type: { environment: "test"; debug: true } (literals preserved)
```

### Quick React Testing Patterns (Inlined for Standalone Use)

```typescript
// React Testing Library with Jest
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';

// Component testing pattern
describe('UserProfile', () => {
  it('should display user information', () => {
    const user = { id: 1, name: 'Alice', email: 'alice@example.com' };
    render(<UserProfile user={user} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
  });

  it('should handle user interactions', async () => {
    const onSubmit = jest.fn();
    render(<UserForm onSubmit={onSubmit} />);

    // User interactions
    await userEvent.type(screen.getByLabelText('Name'), 'Bob');
    await userEvent.click(screen.getByRole('button', { name: 'Submit' }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({ name: 'Bob' });
    });
  });
});

// Hook testing
import { renderHook, act } from '@testing-library/react';

test('useCounter hook', () => {
  const { result } = renderHook(() => useCounter(0));

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});

// Context and Provider testing
const wrapper = ({ children }: { children: React.ReactNode }) => (
  <AuthProvider>{children}</AuthProvider>
);

test('useAuth hook with context', () => {
  const { result } = renderHook(() => useAuth(), { wrapper });
  expect(result.current.user).toBeDefined();
});
```

### Quick Vitest Comparison (Inlined for Standalone Use)

**When to Choose Vitest over Jest:**
- New Vite/Vite-based projects (Next.js with Turbopack, SvelteKit)
- Need faster test execution (10-100x faster)
- ESM-first architecture
- Hot Module Replacement for tests

**When to Stick with Jest:**
- Existing large codebases with Jest already configured
- Corporate environments with established Jest workflows
- Need mature ecosystem and extensive plugins
- React apps with Create React App (default Jest setup)

**Migration Snippet (Jest → Vitest):**
```typescript
// Jest: import from '@testing-library/jest-dom'
import '@testing-library/jest-dom';

// Vitest: import from vitest globals
import { expect, test, describe } from 'vitest';
import { screen } from '@testing-library/react';

// Most Jest syntax works in Vitest unchanged
test('component renders', () => {
  render(<Component />);
  expect(screen.getByText('Hello')).toBeTruthy();
});
```

[Full TypeScript, React, and Vitest patterns available in respective skills if deployed together]

## Summary

- **Jest** is the industry standard with 70% market share
- **TypeScript support** via ts-jest with full type safety
- **All-in-one solution**: Test runner, assertions, mocks, coverage
- **React Testing Library** integration for component testing
- **Mature ecosystem** with extensive tooling and support
- **Snapshot testing** for UI regression testing
- **Migration path** from Vitest with compatible API
- **Perfect for**: Existing projects, corporate environments, React apps, legacy support
- **Trade-off**: Slower than Vitest but more mature and widely supported
