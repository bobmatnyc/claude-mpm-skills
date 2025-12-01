# React Ecosystem

**Version:** 1.0.0
**Category:** JavaScript/TypeScript
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Complete React development stack with modern state management, server state caching, and comprehensive testing. Optimized for production React applications with complex state requirements and performance demands.

## Included Skills

- **react** (toolchains/typescript/frameworks/react) - Hooks, context, performance optimization
- **zustand** (toolchains/typescript/state/zustand) - Minimal client state management
- **tanstack-query** (toolchains/typescript/state/tanstack-query) - Server state and caching
- **jest** (toolchains/typescript/testing/jest) - TypeScript testing framework
- **vitest** (toolchains/typescript/testing/vitest) - Modern testing with React
- **test-driven-development** (universal/testing/test-driven-development) - TDD methodology

## Use Cases

**When to Deploy This Bundle:**
- Building complex React applications
- Projects with client and server state separation
- Applications requiring optimistic updates
- Teams adopting modern React patterns (hooks-first)
- Projects with strict testing requirements

**What You Get:**
- React hooks patterns and performance optimization
- Zustand for client state (UI, forms, preferences)
- TanStack Query for server state (API data, caching)
- Jest and Vitest configuration for React testing
- TDD workflow with React components

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| react | ✅ Yes | 🚀 Enhanced | None |
| zustand | ✅ Yes | 🚀 Enhanced | React (recommended) |
| tanstack-query | ✅ Yes | 🚀 Enhanced | React (required) |
| jest | ✅ Yes | 🚀 Enhanced | None |
| vitest | ✅ Yes | 🚀 Enhanced | None |
| test-driven-development | ✅ Yes | 🚀 Enhanced | None (methodology) |

**Bundle Synergies:**
- React + Zustand: Client state with hooks
- React + TanStack Query: Server state with automatic caching
- Zustand + TanStack Query: Clear separation of concerns
- Jest/Vitest + React: Component testing with React Testing Library

**State Management Philosophy:**
- **Zustand**: Client state (theme, sidebar open, form data)
- **TanStack Query**: Server state (API responses, cache, refetch)
- Avoid mixing concerns - keep server data in TanStack Query

## Integration Example

```typescript
// Zustand for client state
import { create } from 'zustand';

const useUIStore = create((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}));

// TanStack Query for server state
import { useQuery } from '@tanstack/react-query';

function Users() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  const theme = useUIStore((s) => s.theme);

  // Clear separation: theme from Zustand, users from TanStack Query
}

// Vitest component test
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

describe('Users', () => {
  it('renders user list', () => {
    render(<Users />);
    expect(screen.getByText('Users')).toBeInTheDocument();
  });
});
```

## Version History

- **1.0.0** (2025-11-30): Initial release with 6 React ecosystem skills
