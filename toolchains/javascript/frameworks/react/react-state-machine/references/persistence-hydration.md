# Persistence and Hydration Patterns

## LocalStorage Persistence

### Basic Persistence Pattern

```typescript
import { setup, assign, createActor } from 'xstate';

const STORAGE_KEY = 'app_state';

export const persistedMachine = setup({
  types: {
    context: {} as { count: number; user: User | null },
    events: {} as
      | { type: 'INCREMENT' }
      | { type: 'SET_USER'; user: User }
  },
  actions: {
    persistState: ({ context }) => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(context));
      } catch (error) {
        console.error('Failed to persist state:', error);
      }
    }
  }
}).createMachine({
  id: 'persisted',
  initial: 'active',
  context: { count: 0, user: null },
  states: {
    active: {
      on: {
        INCREMENT: {
          actions: [
            assign({ count: ({ context }) => context.count + 1 }),
            'persistState'
          ]
        },
        SET_USER: {
          actions: [
            assign({ user: ({ event }) => event.user }),
            'persistState'
          ]
        }
      }
    }
  }
});

// Load persisted state
function loadPersistedState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : undefined;
  } catch (error) {
    console.error('Failed to load persisted state:', error);
    return undefined;
  }
}

// Create actor with persisted state
const actor = createActor(persistedMachine, {
  snapshot: loadPersistedState()
});
```

### React Hook for Persisted Machine

```typescript
import { useMachine } from '@xstate/react';
import { useEffect } from 'react';

export function usePersistedMachine(machine, storageKey: string) {
  // Load initial state from localStorage
  const initialSnapshot = useMemo(() => {
    try {
      const stored = localStorage.getItem(storageKey);
      return stored ? JSON.parse(stored) : undefined;
    } catch {
      return undefined;
    }
  }, [storageKey]);
  
  const [snapshot, send, actorRef] = useMachine(machine, {
    snapshot: initialSnapshot
  });
  
  // Persist on every state change
  useEffect(() => {
    const subscription = actorRef.subscribe((state) => {
      try {
        localStorage.setItem(storageKey, JSON.stringify(state));
      } catch (error) {
        console.error('Failed to persist:', error);
      }
    });
    
    return () => subscription.unsubscribe();
  }, [actorRef, storageKey]);
  
  return [snapshot, send, actorRef] as const;
}

// Usage
function App() {
  const [snapshot, send] = usePersistedMachine(appMachine, 'app_state');
  // State automatically persists and restores
}
```

### Selective Persistence (Don't Persist Everything)

```typescript
interface AppContext {
  // Persist these
  user: User | null;
  preferences: Preferences;
  
  // Don't persist these (transient state)
  isLoading: boolean;
  error: Error | null;
  tempData: any;
}

function serializeForPersistence(context: AppContext) {
  return {
    user: context.user,
    preferences: context.preferences
    // Omit transient fields
  };
}

const persistedMachine = setup({
  actions: {
    persistState: ({ context }) => {
      const serialized = serializeForPersistence(context);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(serialized));
    }
  }
});
```

### Versioned Persistence (Handle Schema Changes)

```typescript
const STORAGE_VERSION = 2;

interface PersistedState {
  version: number;
  data: any;
  timestamp: number;
}

function saveState(context: any) {
  const state: PersistedState = {
    version: STORAGE_VERSION,
    data: context,
    timestamp: Date.now()
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function loadState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return undefined;
    
    const parsed: PersistedState = JSON.parse(stored);
    
    // Check version
    if (parsed.version !== STORAGE_VERSION) {
      console.warn('State version mismatch, migrating...');
      return migrateState(parsed);
    }
    
    // Check if stale (older than 7 days)
    const sevenDays = 7 * 24 * 60 * 60 * 1000;
    if (Date.now() - parsed.timestamp > sevenDays) {
      console.warn('State is stale, discarding');
      return undefined;
    }
    
    return parsed.data;
  } catch (error) {
    console.error('Failed to load state:', error);
    return undefined;
  }
}

function migrateState(old: PersistedState): any {
  // Migrate from v1 to v2
  if (old.version === 1) {
    return {
      ...old.data,
      newField: 'default value'
    };
  }
  return undefined;
}
```

## SSR and Hydration

### Next.js Server-Side Rendering

```typescript
// app/page.tsx (Next.js App Router)
import { createActor } from 'xstate';
import { appMachine } from './machines/appMachine';

export default async function Page() {
  // Create actor on server
  const actor = createActor(appMachine);
  actor.start();

  // Fetch initial data
  const data = await fetchInitialData();
  actor.send({ type: 'SET_DATA', data });

  // Get snapshot for client hydration
  const snapshot = actor.getSnapshot();
  actor.stop();

  return (
    <ClientComponent initialSnapshot={snapshot} />
  );
}
```

```typescript
// ClientComponent.tsx
'use client';

import { useMachine } from '@xstate/react';
import { appMachine } from './machines/appMachine';

export function ClientComponent({ initialSnapshot }) {
  const [snapshot, send] = useMachine(appMachine, {
    snapshot: initialSnapshot // Hydrate from server
  });

  return (
    <div>
      {/* Component renders with server data immediately */}
      <pre>{JSON.stringify(snapshot.context, null, 2)}</pre>
    </div>
  );
}
```

### Next.js Pages Router with getServerSideProps

```typescript
// pages/dashboard.tsx
import { GetServerSideProps } from 'next';
import { createActor } from 'xstate';
import { dashboardMachine } from '../machines/dashboardMachine';

export const getServerSideProps: GetServerSideProps = async (context) => {
  const actor = createActor(dashboardMachine);
  actor.start();

  // Fetch user data
  const user = await fetchUser(context.req.cookies.token);
  actor.send({ type: 'SET_USER', user });

  // Get serializable snapshot
  const snapshot = actor.getSnapshot();
  actor.stop();

  return {
    props: {
      initialSnapshot: JSON.parse(JSON.stringify(snapshot))
    }
  };
};

export default function Dashboard({ initialSnapshot }) {
  const [snapshot, send] = useMachine(dashboardMachine, {
    snapshot: initialSnapshot
  });

  return <div>{/* ... */}</div>;
}
```

### Handling Non-Serializable Data

```typescript
// Problem: Functions, Dates, etc. can't be serialized
interface Context {
  user: User;
  createdAt: Date; // ❌ Not serializable
  callback: () => void; // ❌ Not serializable
}

// Solution: Serialize/deserialize with custom logic
function serializeSnapshot(snapshot: any) {
  return {
    ...snapshot,
    context: {
      ...snapshot.context,
      createdAt: snapshot.context.createdAt?.toISOString(),
      // Omit functions
      callback: undefined
    }
  };
}

function deserializeSnapshot(serialized: any) {
  return {
    ...serialized,
    context: {
      ...serialized.context,
      createdAt: serialized.context.createdAt
        ? new Date(serialized.context.createdAt)
        : null,
      // Restore functions
      callback: () => console.log('Restored callback')
    }
  };
}

// Server
export const getServerSideProps: GetServerSideProps = async () => {
  const actor = createActor(machine);
  actor.start();
  const snapshot = serializeSnapshot(actor.getSnapshot());
  actor.stop();

  return { props: { snapshot } };
};

// Client
function Component({ snapshot }) {
  const [state, send] = useMachine(machine, {
    snapshot: deserializeSnapshot(snapshot)
  });
}
```

### Preventing Hydration Mismatches

```typescript
'use client';

import { useMachine } from '@xstate/react';
import { useState, useEffect } from 'react';

export function HydratedComponent({ initialSnapshot }) {
  const [isHydrated, setIsHydrated] = useState(false);
  const [snapshot, send] = useMachine(machine, {
    snapshot: initialSnapshot
  });

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  // Show server-rendered content until hydrated
  if (!isHydrated) {
    return <ServerRenderedFallback snapshot={initialSnapshot} />;
  }

  // Now safe to show client-specific content
  return <InteractiveContent snapshot={snapshot} send={send} />;
}
```

## Snapshot Serialization

### Deep Serialization with Circular References

```typescript
import { createActor } from 'xstate';

function serializeSnapshot(snapshot: any): string {
  const seen = new WeakSet();

  return JSON.stringify(snapshot, (key, value) => {
    // Handle circular references
    if (typeof value === 'object' && value !== null) {
      if (seen.has(value)) {
        return '[Circular]';
      }
      seen.add(value);
    }

    // Handle special types
    if (value instanceof Date) {
      return { __type: 'Date', value: value.toISOString() };
    }

    if (value instanceof Map) {
      return {
        __type: 'Map',
        value: Array.from(value.entries())
      };
    }

    if (value instanceof Set) {
      return {
        __type: 'Set',
        value: Array.from(value)
      };
    }

    return value;
  });
}

function deserializeSnapshot(json: string): any {
  return JSON.parse(json, (key, value) => {
    if (value && typeof value === 'object') {
      // Restore special types
      if (value.__type === 'Date') {
        return new Date(value.value);
      }

      if (value.__type === 'Map') {
        return new Map(value.value);
      }

      if (value.__type === 'Set') {
        return new Set(value.value);
      }
    }

    return value;
  });
}
```

### Compression for Large States

```typescript
import pako from 'pako';

function compressSnapshot(snapshot: any): string {
  const json = JSON.stringify(snapshot);
  const compressed = pako.deflate(json);
  return btoa(String.fromCharCode(...compressed));
}

function decompressSnapshot(compressed: string): any {
  const binary = atob(compressed);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  const decompressed = pako.inflate(bytes, { to: 'string' });
  return JSON.parse(decompressed);
}

// Usage
const actor = createActor(machine);
actor.start();

// Save compressed
const compressed = compressSnapshot(actor.getSnapshot());
localStorage.setItem('state', compressed);

// Load compressed
const loaded = decompressSnapshot(localStorage.getItem('state')!);
const restoredActor = createActor(machine, { snapshot: loaded });
```

## IndexedDB for Large State

```typescript
import { openDB, DBSchema } from 'idb';

interface StateDB extends DBSchema {
  snapshots: {
    key: string;
    value: {
      id: string;
      snapshot: any;
      timestamp: number;
    };
  };
}

class StatePersistence {
  private db: Promise<IDBDatabase>;

  constructor() {
    this.db = openDB<StateDB>('state-db', 1, {
      upgrade(db) {
        db.createObjectStore('snapshots', { keyPath: 'id' });
      }
    });
  }

  async saveSnapshot(id: string, snapshot: any) {
    const db = await this.db;
    await db.put('snapshots', {
      id,
      snapshot,
      timestamp: Date.now()
    });
  }

  async loadSnapshot(id: string) {
    const db = await this.db;
    const record = await db.get('snapshots', id);
    return record?.snapshot;
  }

  async clearOldSnapshots(maxAge: number = 7 * 24 * 60 * 60 * 1000) {
    const db = await this.db;
    const tx = db.transaction('snapshots', 'readwrite');
    const store = tx.objectStore('snapshots');
    const all = await store.getAll();

    const now = Date.now();
    for (const record of all) {
      if (now - record.timestamp > maxAge) {
        await store.delete(record.id);
      }
    }
  }
}

// Usage
const persistence = new StatePersistence();

// Save
const actor = createActor(machine);
actor.subscribe((snapshot) => {
  persistence.saveSnapshot('app-state', snapshot);
});

// Load
const snapshot = await persistence.loadSnapshot('app-state');
const actor = createActor(machine, { snapshot });
```

## Best Practices

### Persistence Checklist

✅ **Version your state** to handle schema changes
✅ **Don't persist transient state** (loading, errors)
✅ **Handle serialization errors** gracefully
✅ **Set expiration** for stale data
✅ **Compress large states** to save space
✅ **Use IndexedDB** for large datasets
✅ **Test hydration** in development
✅ **Handle missing data** on load
✅ **Clear old data** periodically
✅ **Validate loaded state** before using

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Persisting everything | Bloated storage, slow loads | Selective persistence |
| No versioning | Breaks on schema changes | Version + migration |
| Circular references | JSON.stringify fails | Custom serializer |
| Large localStorage | 5-10MB limit | Use IndexedDB |
| Hydration mismatch | React warnings | Match server/client |
| Stale data | Using outdated state | Add timestamps |


