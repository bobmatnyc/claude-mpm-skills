# Testing State Machine Skills

## Unit Testing Transitions

```typescript
import { createActor } from 'xstate';
import { describe, test, expect, vi } from 'vitest';
import { toggleMachine } from './toggleMachine';

describe('toggleMachine', () => {
  test('starts in inactive state', () => {
    const actor = createActor(toggleMachine);
    actor.start();
    
    expect(actor.getSnapshot().value).toBe('inactive');
    expect(actor.getSnapshot().context.count).toBe(0);
  });
  
  test('transitions to active on TOGGLE', () => {
    const actor = createActor(toggleMachine);
    actor.start();
    
    actor.send({ type: 'TOGGLE' });
    
    expect(actor.getSnapshot().value).toBe('active');
    expect(actor.getSnapshot().context.count).toBe(1);
  });
  
  test('transitions back to inactive on second TOGGLE', () => {
    const actor = createActor(toggleMachine);
    actor.start();
    
    actor.send({ type: 'TOGGLE' });
    actor.send({ type: 'TOGGLE' });
    
    expect(actor.getSnapshot().value).toBe('inactive');
    expect(actor.getSnapshot().context.count).toBe(2);
  });
  
  test('ignores invalid events', () => {
    const actor = createActor(toggleMachine);
    actor.start();
    
    // @ts-expect-error Testing invalid event
    actor.send({ type: 'INVALID_EVENT' });
    
    expect(actor.getSnapshot().value).toBe('inactive');
  });
});
```

## Testing Guards

```typescript
import { createActor } from 'xstate';
import { formMachine } from './formMachine';

describe('formMachine guards', () => {
  test('blocks submission with invalid email', () => {
    const actor = createActor(formMachine);
    actor.start();
    
    actor.send({ type: 'UPDATE_EMAIL', value: 'invalid-email' });
    actor.send({ type: 'SUBMIT' });
    
    // Should stay in editing state due to guard
    expect(actor.getSnapshot().value).toBe('editing');
    expect(actor.getSnapshot().context.errors.email).toBeDefined();
  });
  
  test('allows submission with valid email', () => {
    const actor = createActor(formMachine);
    actor.start();
    
    actor.send({ type: 'UPDATE_EMAIL', value: 'test@example.com' });
    actor.send({ type: 'UPDATE_NAME', value: 'John Doe' });
    actor.send({ type: 'SUBMIT' });
    
    expect(actor.getSnapshot().value).toBe('submitting');
  });
});
```

## Testing Async Actors with Mocks

```typescript
import { createActor } from 'xstate';
import { fromPromise } from 'xstate';
import { describe, test, expect, vi, beforeEach } from 'vitest';
import { fetchMachine } from './fetchMachine';

describe('fetchMachine async behavior', () => {
  test('handles successful API response', async () => {
    const mockData = { id: 1, name: 'Test User' };
    const mockFetch = vi.fn().mockResolvedValue(mockData);
    
    // Override the actor with mock
    const testMachine = fetchMachine.provide({
      actors: {
        fetchUser: fromPromise(mockFetch)
      }
    });
    
    const actor = createActor(testMachine);
    actor.start();
    
    actor.send({ type: 'FETCH', userId: '123' });
    
    // Wait for async completion
    await vi.waitFor(() => {
      expect(actor.getSnapshot().value).toBe('success');
    });
    
    expect(actor.getSnapshot().context.data).toEqual(mockData);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.objectContaining({ input: { userId: '123' } })
    );
  });
  
  test('handles API errors gracefully', async () => {
    const mockError = new Error('Network failure');
    const mockFetch = vi.fn().mockRejectedValue(mockError);
    
    const testMachine = fetchMachine.provide({
      actors: {
        fetchUser: fromPromise(mockFetch)
      }
    });
    
    const actor = createActor(testMachine);
    actor.start();
    
    actor.send({ type: 'FETCH', userId: '123' });
    
    await vi.waitFor(() => {
      expect(actor.getSnapshot().value).toBe('failure');
    });
    
    expect(actor.getSnapshot().context.error?.message).toBe('Network failure');
  });
  
  test('retries on failure when retries available', async () => {
    const mockFetch = vi.fn()
      .mockRejectedValueOnce(new Error('First failure'))
      .mockRejectedValueOnce(new Error('Second failure'))
      .mockResolvedValue({ id: 1 });
    
    const testMachine = fetchMachine.provide({
      actors: {
        fetchUser: fromPromise(mockFetch)
      }
    });
    
    const actor = createActor(testMachine, {
      input: { url: '/api/user', retries: 3 }
    });
    actor.start();
    
    actor.send({ type: 'FETCH' });
    
    await vi.waitFor(() => {
      expect(actor.getSnapshot().value).toBe('success');
    });
    
    expect(mockFetch).toHaveBeenCalledTimes(3);
  });
});
```

## Testing with Subscriptions

```typescript
test('tracks all state transitions', async () => {
  const transitions: string[] = [];
  
  const actor = createActor(workflowMachine);
  
  actor.subscribe((snapshot) => {
    transitions.push(String(snapshot.value));
  });
  
  actor.start();
  actor.send({ type: 'START' });
  
  await vi.waitFor(() => {
    expect(transitions).toEqual([
      'idle',
      'processing',
      'success'
    ]);
  });
});
```

## Testing Parallel States

```typescript
describe('videoPlayerMachine parallel states', () => {
  test('can be playing and muted simultaneously', () => {
    const actor = createActor(videoPlayerMachine);
    actor.start();
    
    actor.send({ type: 'LOADED' });
    actor.send({ type: 'PLAY' });
    actor.send({ type: 'MUTE' });
    
    const snapshot = actor.getSnapshot();
    
    // Check parallel state combination
    expect(snapshot.matches({ 
      ready: { 
        playback: 'playing', 
        volume: 'muted' 
      } 
    })).toBe(true);
  });
  
  test('playback and volume are independent', () => {
    const actor = createActor(videoPlayerMachine);
    actor.start();
    actor.send({ type: 'LOADED' });
    
    // Muting doesn't affect playback
    actor.send({ type: 'MUTE' });
    expect(actor.getSnapshot().matches({ 
      ready: { playback: 'paused' } 
    })).toBe(true);
    
    // Playing doesn't affect volume
    actor.send({ type: 'PLAY' });
    expect(actor.getSnapshot().matches({ 
      ready: { volume: 'muted' } 
    })).toBe(true);
  });
});
```

## Testing Spawned Actors

```typescript
describe('taskManagerMachine with spawned actors', () => {
  test('spawns task actors on ADD_TASK', () => {
    const actor = createActor(taskManagerMachine);
    actor.start();
    
    actor.send({ 
      type: 'ADD_TASK', 
      taskId: 'task-1',
      title: 'First task' 
    });
    
    const snapshot = actor.getSnapshot();
    expect(snapshot.context.tasks).toHaveLength(1);
    expect(snapshot.context.tasks[0].id).toBe('task-task-1');
  });
  
  test('communicates with spawned actors', () => {
    const actor = createActor(taskManagerMachine);
    actor.start();
    
    actor.send({ 
      type: 'ADD_TASK', 
      taskId: 'task-1',
      title: 'Test task' 
    });
    
    // Send event to spawned actor
    actor.send({ type: 'TASK_COMPLETED', taskId: 'task-task-1' });
    
    const taskActor = actor.getSnapshot().context.tasks[0];
    expect(taskActor.getSnapshot().value).toBe('completed');
  });
  
  test('stops spawned actors on removal', () => {
    const actor = createActor(taskManagerMachine);
    actor.start();
    
    actor.send({ type: 'ADD_TASK', taskId: 'task-1', title: 'Test' });
    
    const taskActor = actor.getSnapshot().context.tasks[0];
    const stopSpy = vi.spyOn(taskActor, 'stop');
    
    actor.send({ type: 'REMOVE_TASK', taskId: 'task-task-1' });
    
    expect(stopSpy).toHaveBeenCalled();
    expect(actor.getSnapshot().context.tasks).toHaveLength(0);
  });
});
```

## Testing Delayed Transitions

```typescript
describe('modalMachine delayed transitions', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  
  afterEach(() => {
    vi.useRealTimers();
  });
  
  test('auto-closes after animation delay', async () => {
    const actor = createActor(modalMachine);
    actor.start();
    
    actor.send({ type: 'OPEN' });
    expect(actor.getSnapshot().value).toBe('opening');
    
    // Advance past opening animation
    await vi.advanceTimersByTimeAsync(300);
    expect(actor.getSnapshot().value).toBe('open');
    
    actor.send({ type: 'CLOSE' });
    expect(actor.getSnapshot().value).toBe('closing');
    
    // Advance past closing animation
    await vi.advanceTimersByTimeAsync(300);
    expect(actor.getSnapshot().value).toBe('closed');
  });
});
```

## Testing with Input

```typescript
describe('parameterized machines', () => {
  test('initializes context from input', () => {
    const actor = createActor(fetchMachine, {
      input: {
        url: '/api/custom',
        retries: 5
      }
    });
    actor.start();
    
    const context = actor.getSnapshot().context;
    expect(context.url).toBe('/api/custom');
    expect(context.maxRetries).toBe(5);
  });
  
  test('different inputs create different behaviors', () => {
    const strictActor = createActor(fetchMachine, {
      input: { url: '/api/data', retries: 0 }
    });
    
    const lenientActor = createActor(fetchMachine, {
      input: { url: '/api/data', retries: 10 }
    });
    
    strictActor.start();
    lenientActor.start();
    
    expect(strictActor.getSnapshot().context.maxRetries).toBe(0);
    expect(lenientActor.getSnapshot().context.maxRetries).toBe(10);
  });
});
```

## Visualization for Debugging

### Stately Studio Integration

```typescript
// In development, enable inspector
import { inspect } from '@xstate/inspect';

if (process.env.NODE_ENV === 'development') {
  inspect({
    url: 'https://stately.ai/viz?inspect',
    iframe: false // Opens in new tab
  });
}

// Create actor with inspection enabled
const actor = createActor(complexMachine, {
  inspect: true
});
```

### Console Logging for CI

```typescript
function createTestActor(machine) {
  const actor = createActor(machine);
  
  actor.subscribe({
    next: (snapshot) => {
      console.log(`State: ${JSON.stringify(snapshot.value)}`);
      console.log(`Context: ${JSON.stringify(snapshot.context)}`);
    },
    error: (err) => console.error('Actor error:', err),
    complete: () => console.log('Actor completed')
  });
  
  return actor;
}
```

## Integration Testing with React

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SignUpForm } from './SignUpForm';

describe('SignUpForm integration', () => {
  test('completes multi-step flow', async () => {
    const user = userEvent.setup();
    render(<SignUpForm />);
    
    // Step 1: Personal info
    await user.type(screen.getByPlaceholderText('Name'), 'John Doe');
    await user.click(screen.getByText('Next'));
    
    // Step 2: Credentials
    await user.type(screen.getByPlaceholderText('Password'), 'secure123');
    await user.click(screen.getByText('Next'));
    
    // Step 3: Plan selection
    await user.click(screen.getByText('Pro Plan'));
    await user.click(screen.getByText('Next'));
    
    // Step 4: Confirmation
    expect(screen.getByText('Confirm your details')).toBeInTheDocument();
    
    await user.click(screen.getByText('Submit'));
    
    await waitFor(() => {
      expect(screen.getByText('Welcome!')).toBeInTheDocument();
    });
  });
  
  test('shows validation errors', async () => {
    const user = userEvent.setup();
    render(<SignUpForm />);
    
    // Try to proceed without filling name
    await user.click(screen.getByText('Next'));
    
    expect(screen.getByText('Name must be at least 2 characters')).toBeInTheDocument();
  });
});
```
