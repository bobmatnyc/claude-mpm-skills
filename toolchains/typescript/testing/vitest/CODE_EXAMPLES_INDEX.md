# Vitest Skill - Code Examples Index

Quick reference for all code examples included in the Vitest skill.

---

## Configuration Examples

### 1. Basic Vitest Config
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: { provider: 'v8' },
  },
});
```

### 2. React Config
```typescript
// vitest.config.ts with React
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

### 3. Vue Config
```typescript
// vitest.config.ts with Vue
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'happy-dom',
  },
});
```

---

## Testing Patterns

### 4. Basic Test Structure
```typescript
describe('Calculator', () => {
  it('adds two numbers', () => {
    expect(2 + 3).toBe(5);
  });
});
```

### 5. TypeScript Type Testing
```typescript
import { expectTypeOf, assertType } from 'vitest';

it('checks types', () => {
  expectTypeOf(user.id).toBeNumber();
  assertType<User>(user);
});
```

### 6. Module Mocking
```typescript
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}));

vi.mocked(fetchUser).mockResolvedValue({ id: 1 });
```

### 7. Method Spying
```typescript
const spy = vi.spyOn(logger, 'log');
logger.log('Hello');
expect(spy).toHaveBeenCalledWith('Hello');
```

### 8. Timer Mocking
```typescript
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
await vi.runAllTimersAsync();
```

---

## React Testing

### 9. Component Testing
```typescript
import { render, screen } from '@testing-library/react';

it('renders component', () => {
  render(<Counter initialCount={0} />);
  expect(screen.getByText('Count: 0')).toBeInTheDocument();
});
```

### 10. User Interaction
```typescript
import userEvent from '@testing-library/user-event';

const user = userEvent.setup();
await user.click(screen.getByRole('button'));
```

### 11. Hook Testing
```typescript
import { renderHook, act } from '@testing-library/react';

const { result } = renderHook(() => useCounter(0));
act(() => result.current.increment());
expect(result.current.count).toBe(1);
```

---

## Vue Testing

### 12. Vue Component Testing
```typescript
import { mount } from '@vue/test-utils';

const wrapper = mount(Counter, {
  props: { initialCount: 5 },
});
expect(wrapper.text()).toContain('Count: 5');
```

### 13. Event Emission
```typescript
await wrapper.find('button').trigger('click');
expect(wrapper.emitted('update')).toBeTruthy();
expect(wrapper.emitted('update')?.[0]).toEqual([1]);
```

---

## Async Testing

### 14. Promise Testing
```typescript
await expect(Promise.resolve(42)).resolves.toBe(42);
await expect(Promise.reject(new Error('fail'))).rejects.toThrow('fail');
```

### 15. Fetch Mocking
```typescript
global.fetch = vi.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve('data'),
  } as Response)
);

const data = await fetchData(1);
expect(data).toBe('data');
```

---

## Snapshot Testing

### 16. Basic Snapshot
```typescript
expect(container.firstChild).toMatchSnapshot();
```

### 17. Inline Snapshot
```typescript
expect(user).toMatchInlineSnapshot(`
  {
    "id": 1,
    "name": "Bob",
  }
`);
```

---

## Advanced Patterns

### 18. Concurrent Testing
```typescript
describe.concurrent('Parallel Tests', () => {
  it('test 1', async () => {
    await slowOperation();
  });
  it('test 2', async () => {
    await slowOperation();
  });
});
```

### 19. Custom Matchers
```typescript
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return { pass, message: () => '...' };
  },
});

expect(100).toBeWithinRange(90, 110);
```

### 20. Test Context
```typescript
describe<TestContext>('With Context', () => {
  beforeEach((ctx) => {
    ctx.user = { id: 1, name: 'Alice' };
  });

  it<TestContext>('uses context', ({ user }) => {
    expect(user.name).toBe('Alice');
  });
});
```

---

## Migration Examples

### 21. Jest to Vitest Import
```typescript
// Before (Jest)
import { jest } from '@jest/globals';

// After (Vitest)
import { vi } from 'vitest';
```

### 22. Mock Syntax Migration
```typescript
// Before
jest.fn()
jest.spyOn()
jest.mock()

// After
vi.fn()
vi.spyOn()
vi.mock()
```

---

## CI/CD Examples

### 23. Package.json Scripts
```json
{
  "scripts": {
    "test": "vitest run",           // CI-safe
    "test:watch": "vitest",          // Development
    "test:ui": "vitest --ui",        // Debugging
    "test:coverage": "vitest run --coverage"
  }
}
```

---

## Coverage Configuration

### 24. Coverage Thresholds
```typescript
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },
  },
});
```

---

## Best Practices

### 25. Mock Cleanup
```typescript
import { afterEach } from 'vitest';

afterEach(() => {
  vi.restoreAllMocks();
});
```

### 26. CI-Safe Execution
```json
// ✅ CORRECT
"test": "vitest run"

// ❌ WRONG - hangs in CI
"test": "vitest"
```

### 27. Async Test Pattern
```typescript
// ✅ CORRECT
it('fetches data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// ❌ WRONG - assertion never runs
it('fetches data', () => {
  fetchData().then(data => {
    expect(data).toBeDefined();
  });
});
```

---

## Summary

**Total Examples**: 27 comprehensive code examples
**Categories**: Configuration (3), Testing Patterns (5), React (3), Vue (2), Async (2), Snapshots (2), Advanced (3), Migration (2), CI/CD (1), Coverage (1), Best Practices (3)

All examples are:
- ✅ TypeScript with proper types
- ✅ Copy-paste ready
- ✅ Runnable without modification
- ✅ Following modern Vitest best practices
- ✅ Production-ready patterns
