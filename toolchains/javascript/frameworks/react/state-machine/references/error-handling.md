# Error Handling and Recovery Patterns

## Error Boundaries Integration

### Error Boundary with State Machine

```typescript
import { Component, ErrorInfo, ReactNode } from 'react';
import { createActor } from 'xstate';
import { errorBoundaryMachine } from './errorBoundaryMachine';

interface Props {
  children: ReactNode;
  fallback?: (error: Error, reset: () => void) => ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class StateMachineErrorBoundary extends Component<Props, State> {
  private actor = createActor(errorBoundaryMachine);
  
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  componentDidMount() {
    this.actor.start();
    this.actor.subscribe((snapshot) => {
      this.setState({
        hasError: snapshot.matches('error'),
        error: snapshot.context.error
      });
    });
  }
  
  componentWillUnmount() {
    this.actor.stop();
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.actor.send({ type: 'ERROR_CAUGHT', error, errorInfo });
  }
  
  handleReset = () => {
    this.actor.send({ type: 'RESET' });
    this.setState({ hasError: false, error: null });
  };
  
  render() {
    if (this.state.hasError && this.state.error) {
      return this.props.fallback?.(this.state.error, this.handleReset) || (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error.message}</pre>
          </details>
          <button onClick={this.handleReset}>Try again</button>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

### Error Boundary Machine

```typescript
import { setup, assign } from 'xstate';

interface ErrorContext {
  error: Error | null;
  errorInfo: any;
  errorCount: number;
  lastErrorTime: number | null;
}

type ErrorEvent =
  | { type: 'ERROR_CAUGHT'; error: Error; errorInfo: any }
  | { type: 'RESET' }
  | { type: 'REPORT_ERROR' };

export const errorBoundaryMachine = setup({
  types: {
    context: {} as ErrorContext,
    events: {} as ErrorEvent
  },
  actions: {
    captureError: assign({
      error: ({ event }) => event.error,
      errorInfo: ({ event }) => event.errorInfo,
      errorCount: ({ context }) => context.errorCount + 1,
      lastErrorTime: () => Date.now()
    }),
    
    resetError: assign({
      error: null,
      errorInfo: null
    }),
    
    reportError: ({ context }) => {
      // Send to error tracking service
      if (context.error) {
        console.error('Error reported:', context.error, context.errorInfo);
        // Example: Sentry.captureException(context.error);
      }
    }
  },
  guards: {
    isCriticalError: ({ context }) => {
      // Too many errors in short time = critical
      const fiveMinutes = 5 * 60 * 1000;
      const recentErrors = context.errorCount > 3;
      const withinTimeWindow = context.lastErrorTime
        ? Date.now() - context.lastErrorTime < fiveMinutes
        : false;
      return recentErrors && withinTimeWindow;
    }
  }
}).createMachine({
  id: 'errorBoundary',
  initial: 'idle',
  context: {
    error: null,
    errorInfo: null,
    errorCount: 0,
    lastErrorTime: null
  },
  states: {
    idle: {
      on: {
        ERROR_CAUGHT: {
          target: 'error',
          actions: ['captureError', 'reportError']
        }
      }
    },
    
    error: {
      always: [
        {
          target: 'critical',
          guard: 'isCriticalError'
        }
      ],
      on: {
        RESET: {
          target: 'idle',
          actions: 'resetError'
        },
        ERROR_CAUGHT: {
          actions: ['captureError', 'reportError']
        }
      }
    },
    
    critical: {
      // Prevent further resets - requires page reload
      entry: () => {
        console.error('Critical error state - too many errors');
      }
    }
  }
});
```

## Retry Strategies

### Exponential Backoff

```typescript
import { setup, assign, fromPromise } from 'xstate';

interface RetryContext {
  data: any;
  error: Error | null;
  retryCount: number;
  maxRetries: number;
  baseDelay: number;
}

export const exponentialBackoffMachine = setup({
  types: {
    context: {} as RetryContext,
    events: {} as
      | { type: 'FETCH' }
      | { type: 'RETRY' }
      | { type: 'CANCEL' }
  },
  actors: {
    fetchData: fromPromise(async ({ input }) => {
      const response = await fetch(input.url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
  },
  actions: {
    incrementRetry: assign({
      retryCount: ({ context }) => context.retryCount + 1
    }),
    
    setData: assign({
      data: ({ event }) => event.output,
      error: null,
      retryCount: 0
    }),
    
    setError: assign({
      error: ({ event }) => event.error
    })
  },
  guards: {
    canRetry: ({ context }) => context.retryCount < context.maxRetries,
    
    shouldRetry: ({ context, event }) => {
      // Don't retry on client errors (4xx)
      const error = event.error as any;
      if (error.message?.includes('HTTP 4')) return false;
      return context.retryCount < context.maxRetries;
    }
  },
  delays: {
    exponentialDelay: ({ context }) => {
      // 2^retryCount * baseDelay with jitter
      const exponential = Math.pow(2, context.retryCount) * context.baseDelay;
      const jitter = Math.random() * 1000; // Add randomness
      return Math.min(exponential + jitter, 30000); // Max 30s
    }
  }
}).createMachine({
  id: 'exponentialBackoff',
  initial: 'idle',
  context: {
    data: null,
    error: null,
    retryCount: 0,
    maxRetries: 5,
    baseDelay: 1000
  },
  states: {
    idle: {
      on: {
        FETCH: 'loading'
      }
    },
    
    loading: {
      invoke: {
        src: 'fetchData',
        input: { url: '/api/data' },
        onDone: {
          target: 'success',
          actions: 'setData'
        },
        onError: [
          {
            target: 'retrying',
            guard: 'shouldRetry',
            actions: ['setError', 'incrementRetry']
          },
          {
            target: 'failure',
            actions: 'setError'
          }
        ]
      },
      on: {
        CANCEL: 'idle'
      }
    },
    
    retrying: {
      after: {
        exponentialDelay: 'loading'
      },
      on: {
        CANCEL: 'idle'
      }
    },
    
    success: {
      on: {
        FETCH: 'loading'
      }
    },
    
    failure: {
      on: {
        RETRY: {
          target: 'loading',
          actions: assign({ retryCount: 0 })
        }
      }
    }
  }
});
```

### Circuit Breaker Pattern

```typescript
import { setup, assign, fromPromise } from 'xstate';

interface CircuitBreakerContext {
  failureCount: number;
  successCount: number;
  lastFailureTime: number | null;
  threshold: number;
  timeout: number;
  data: any;
  error: Error | null;
}

export const circuitBreakerMachine = setup({
  types: {
    context: {} as CircuitBreakerContext,
    events: {} as
      | { type: 'CALL' }
      | { type: 'RESET' }
  },
  actors: {
    makeRequest: fromPromise(async ({ input }) => {
      const response = await fetch(input.url);
      if (!response.ok) throw new Error('Request failed');
      return response.json();
    })
  },
  actions: {
    incrementFailure: assign({
      failureCount: ({ context }) => context.failureCount + 1,
      lastFailureTime: () => Date.now()
    }),

    incrementSuccess: assign({
      successCount: ({ context }) => context.successCount + 1,
      failureCount: 0
    }),

    setData: assign({
      data: ({ event }) => event.output,
      error: null
    }),

    setError: assign({
      error: ({ event }) => event.error
    }),

    resetCircuit: assign({
      failureCount: 0,
      successCount: 0,
      lastFailureTime: null,
      error: null
    })
  },
  guards: {
    thresholdReached: ({ context }) => {
      return context.failureCount >= context.threshold;
    },

    timeoutElapsed: ({ context }) => {
      if (!context.lastFailureTime) return false;
      return Date.now() - context.lastFailureTime >= context.timeout;
    },

    successThresholdReached: ({ context }) => {
      return context.successCount >= 3;
    }
  }
}).createMachine({
  id: 'circuitBreaker',
  initial: 'closed',
  context: {
    failureCount: 0,
    successCount: 0,
    lastFailureTime: null,
    threshold: 5,
    timeout: 60000,
    data: null,
    error: null
  },
  states: {
    closed: {
      on: {
        CALL: 'calling'
      }
    },

    calling: {
      invoke: {
        src: 'makeRequest',
        input: { url: '/api/data' },
        onDone: {
          target: 'closed',
          actions: ['setData', 'incrementSuccess']
        },
        onError: [
          {
            target: 'open',
            guard: 'thresholdReached',
            actions: ['setError', 'incrementFailure']
          },
          {
            target: 'closed',
            actions: ['setError', 'incrementFailure']
          }
        ]
      }
    },

    open: {
      entry: () => console.warn('Circuit breaker OPEN'),
      after: {
        timeout: 'halfOpen'
      },
      on: {
        CALL: {
          actions: () => {
            throw new Error('Circuit breaker is OPEN');
          }
        },
        RESET: {
          target: 'closed',
          actions: 'resetCircuit'
        }
      }
    },

    halfOpen: {
      on: {
        CALL: 'testing'
      }
    },

    testing: {
      invoke: {
        src: 'makeRequest',
        input: { url: '/api/data' },
        onDone: [
          {
            target: 'closed',
            guard: 'successThresholdReached',
            actions: ['setData', 'incrementSuccess', 'resetCircuit']
          },
          {
            target: 'halfOpen',
            actions: ['setData', 'incrementSuccess']
          }
        ],
        onError: {
          target: 'open',
          actions: ['setError', 'incrementFailure']
        }
      }
    }
  }
});
```

## Graceful Degradation

### Feature Fallback Machine

```typescript
import { setup, assign, fromPromise } from 'xstate';

interface FeatureContext {
  primaryAvailable: boolean;
  fallbackAvailable: boolean;
  data: any;
  error: Error | null;
  mode: 'primary' | 'fallback' | 'offline';
}

export const gracefulDegradationMachine = setup({
  types: {
    context: {} as FeatureContext,
    events: {} as
      | { type: 'LOAD' }
      | { type: 'RETRY_PRIMARY' }
  },
  actors: {
    loadPrimary: fromPromise(async () => {
      const response = await fetch('/api/v2/data');
      if (!response.ok) throw new Error('Primary API failed');
      return response.json();
    }),

    loadFallback: fromPromise(async () => {
      const response = await fetch('/api/v1/data');
      if (!response.ok) throw new Error('Fallback API failed');
      return response.json();
    }),

    loadOffline: fromPromise(async () => {
      const cached = localStorage.getItem('cached_data');
      if (!cached) throw new Error('No cached data');
      return JSON.parse(cached);
    })
  },
  actions: {
    setPrimaryData: assign({
      data: ({ event }) => event.output,
      primaryAvailable: true,
      mode: 'primary',
      error: null
    }),

    setFallbackData: assign({
      data: ({ event }) => event.output,
      fallbackAvailable: true,
      mode: 'fallback',
      error: null
    }),

    setOfflineData: assign({
      data: ({ event }) => event.output,
      mode: 'offline',
      error: null
    }),

    setError: assign({
      error: ({ event }) => event.error
    })
  }
}).createMachine({
  id: 'gracefulDegradation',
  initial: 'loading',
  context: {
    primaryAvailable: false,
    fallbackAvailable: false,
    data: null,
    error: null,
    mode: 'primary'
  },
  states: {
    loading: {
      invoke: {
        src: 'loadPrimary',
        onDone: {
          target: 'success',
          actions: 'setPrimaryData'
        },
        onError: 'tryingFallback'
      }
    },

    tryingFallback: {
      invoke: {
        src: 'loadFallback',
        onDone: {
          target: 'success',
          actions: 'setFallbackData'
        },
        onError: 'tryingOffline'
      }
    },

    tryingOffline: {
      invoke: {
        src: 'loadOffline',
        onDone: {
          target: 'success',
          actions: 'setOfflineData'
        },
        onError: {
          target: 'failure',
          actions: 'setError'
        }
      }
    },

    success: {
      on: {
        RETRY_PRIMARY: {
          target: 'loading',
          guard: ({ context }) => context.mode !== 'primary'
        }
      }
    },

    failure: {
      on: {
        RETRY_PRIMARY: 'loading'
      }
    }
  }
});
```

### React Component with Degradation UI

```typescript
import { useMachine } from '@xstate/react';
import { gracefulDegradationMachine } from './gracefulDegradationMachine';

export function DataDisplay() {
  const [snapshot, send] = useMachine(gracefulDegradationMachine);
  const { data, mode, error } = snapshot.context;

  return (
    <div>
      {mode === 'fallback' && (
        <div className="warning">
          Using legacy API. Some features may be limited.
          <button onClick={() => send({ type: 'RETRY_PRIMARY' })}>
            Retry
          </button>
        </div>
      )}

      {mode === 'offline' && (
        <div className="warning">
          Offline mode. Showing cached data.
          <button onClick={() => send({ type: 'RETRY_PRIMARY' })}>
            Reconnect
          </button>
        </div>
      )}

      {snapshot.matches('success') && data && (
        <div className="data-display">
          {mode === 'primary' && <AdvancedFeatures data={data} />}
          {mode === 'fallback' && <BasicFeatures data={data} />}
          {mode === 'offline' && <ReadOnlyView data={data} />}
        </div>
      )}

      {snapshot.matches('failure') && (
        <div className="error">
          <p>Unable to load data: {error?.message}</p>
          <button onClick={() => send({ type: 'RETRY_PRIMARY' })}>
            Retry
          </button>
        </div>
      )}
    </div>
  );
}
```

## Best Practices Summary

### Error Handling Checklist

✅ **Use error boundaries** for component-level error isolation
✅ **Implement retry logic** with exponential backoff for transient failures
✅ **Add circuit breakers** for failing external services
✅ **Provide fallbacks** for degraded functionality
✅ **Log errors** to monitoring services (Sentry, LogRocket, etc.)
✅ **Show user-friendly messages** instead of technical errors
✅ **Allow manual retry** when automatic retry fails
✅ **Cache data** for offline scenarios
✅ **Test error states** as thoroughly as success states
✅ **Monitor error rates** to detect systemic issues

### When to Use Each Pattern

| Pattern | Use Case |
|---------|----------|
| Error Boundary | Isolate component failures, prevent full app crash |
| Exponential Backoff | Transient network errors, rate limiting |
| Circuit Breaker | Protect against cascading failures, failing services |
| Graceful Degradation | Provide reduced functionality when primary fails |
| Retry with Jitter | Prevent thundering herd problem |
| Timeout | Prevent indefinite waiting |

