# Composition Patterns: Building Complex Systems

## Actor Communication

### Parent-Child Communication with sendTo

```typescript
import { setup, assign, sendTo } from 'xstate';

// Child machine
const childMachine = setup({
  types: {
    context: {} as { count: number },
    events: {} as
      | { type: 'INCREMENT' }
      | { type: 'RESET' }
  }
}).createMachine({
  id: 'child',
  initial: 'active',
  context: { count: 0 },
  states: {
    active: {
      on: {
        INCREMENT: {
          actions: assign({ count: ({ context }) => context.count + 1 })
        },
        RESET: {
          actions: assign({ count: 0 })
        }
      }
    }
  }
});

// Parent machine
const parentMachine = setup({
  types: {
    events: {} as
      | { type: 'INCREMENT_CHILD' }
      | { type: 'RESET_CHILD' }
  },
  actors: {
    child: childMachine
  }
}).createMachine({
  id: 'parent',
  initial: 'active',
  states: {
    active: {
      invoke: {
        id: 'childActor',
        src: 'child'
      },
      on: {
        INCREMENT_CHILD: {
          actions: sendTo('childActor', { type: 'INCREMENT' })
        },
        RESET_CHILD: {
          actions: sendTo('childActor', { type: 'RESET' })
        }
      }
    }
  }
});
```

### Child-to-Parent Communication with sendParent

```typescript
import { setup, sendParent } from 'xstate';

// Child notifies parent
const notifyingChildMachine = setup({
  types: {
    events: {} as { type: 'COMPLETE_TASK' }
  }
}).createMachine({
  id: 'notifyingChild',
  initial: 'working',
  states: {
    working: {
      on: {
        COMPLETE_TASK: {
          target: 'done',
          actions: sendParent({ type: 'CHILD_COMPLETED' })
        }
      }
    },
    done: {
      type: 'final'
    }
  }
});

// Parent listens for child events
const listeningParentMachine = setup({
  types: {
    context: {} as { completedTasks: number },
    events: {} as { type: 'CHILD_COMPLETED' }
  },
  actors: {
    task: notifyingChildMachine
  }
}).createMachine({
  id: 'listeningParent',
  initial: 'active',
  context: { completedTasks: 0 },
  states: {
    active: {
      invoke: {
        id: 'taskActor',
        src: 'task'
      },
      on: {
        CHILD_COMPLETED: {
          actions: assign({
            completedTasks: ({ context }) => context.completedTasks + 1
          })
        }
      }
    }
  }
});
```

### Bidirectional Communication

```typescript
import { setup, assign, sendTo, sendParent } from 'xstate';

// Worker machine
const workerMachine = setup({
  types: {
    context: {} as { workload: number },
    events: {} as
      | { type: 'ASSIGN_WORK'; amount: number }
      | { type: 'COMPLETE_WORK' }
  }
}).createMachine({
  id: 'worker',
  initial: 'idle',
  context: { workload: 0 },
  states: {
    idle: {
      on: {
        ASSIGN_WORK: {
          target: 'working',
          actions: assign({ workload: ({ event }) => event.amount })
        }
      }
    },
    working: {
      on: {
        COMPLETE_WORK: {
          target: 'idle',
          actions: [
            assign({ workload: 0 }),
            sendParent({ type: 'WORK_COMPLETED' })
          ]
        }
      }
    }
  }
});

// Manager machine
const managerMachine = setup({
  types: {
    context: {} as { completedWork: number },
    events: {} as
      | { type: 'ASSIGN_TASK' }
      | { type: 'WORK_COMPLETED' }
  },
  actors: {
    worker: workerMachine
  }
}).createMachine({
  id: 'manager',
  initial: 'managing',
  context: { completedWork: 0 },
  states: {
    managing: {
      invoke: {
        id: 'workerActor',
        src: 'worker'
      },
      on: {
        ASSIGN_TASK: {
          actions: sendTo('workerActor', { type: 'ASSIGN_WORK', amount: 10 })
        },
        WORK_COMPLETED: {
          actions: assign({
            completedWork: ({ context }) => context.completedWork + 1
          })
        }
      }
    }
  }
});
```

## Machine Composition

### Hierarchical Composition (Parent-Child)

```typescript
import { setup } from 'xstate';

// Reusable form field machine
const fieldMachine = setup({
  types: {
    context: {} as { value: string; error: string | null },
    events: {} as
      | { type: 'CHANGE'; value: string }
      | { type: 'BLUR' }
      | { type: 'VALIDATE' }
  },
  guards: {
    isValid: ({ context }) => context.value.length > 0
  }
}).createMachine({
  id: 'field',
  initial: 'pristine',
  context: { value: '', error: null },
  states: {
    pristine: {
      on: {
        CHANGE: {
          target: 'dirty',
          actions: assign({ value: ({ event }) => event.value })
        }
      }
    },
    dirty: {
      on: {
        CHANGE: {
          actions: assign({ value: ({ event }) => event.value })
        },
        BLUR: 'validating'
      }
    },
    validating: {
      always: [
        { target: 'valid', guard: 'isValid' },
        {
          target: 'invalid',
          actions: assign({ error: 'Field is required' })
        }
      ]
    },
    valid: {
      on: {
        CHANGE: 'dirty'
      }
    },
    invalid: {
      on: {
        CHANGE: 'dirty'
      }
    }
  }
});

// Form machine composes multiple fields
const formMachine = setup({
  actors: {
    field: fieldMachine
  }
}).createMachine({
  id: 'form',
  type: 'parallel',
  states: {
    nameField: {
      invoke: {
        id: 'name',
        src: 'field'
      }
    },
    emailField: {
      invoke: {
        id: 'email',
        src: 'field'
      }
    },
    submission: {
      initial: 'idle',
      states: {
        idle: {
          on: {
            SUBMIT: {
              target: 'submitting',
              // Check all fields are valid
              guard: ({ context }) => {
                // Access child actors to check validity
                return true; // Simplified
              }
            }
          }
        },
        submitting: {},
        success: {},
        failure: {}
      }
    }
  }
});
```

### Spawning Dynamic Actors

```typescript
import { setup, assign, spawn } from 'xstate';

// Task machine (spawned dynamically)
const taskMachine = setup({
  types: {
    context: {} as { id: string; title: string; completed: boolean },
    input: {} as { id: string; title: string }
  }
}).createMachine({
  id: 'task',
  initial: 'active',
  context: ({ input }) => ({
    id: input.id,
    title: input.title,
    completed: false
  }),
  states: {
    active: {
      on: {
        COMPLETE: {
          actions: assign({ completed: true })
        }
      }
    }
  }
});

// Todo list machine that spawns tasks
const todoListMachine = setup({
  types: {
    context: {} as {
      tasks: Map<string, ActorRefFrom<typeof taskMachine>>;
      nextId: number;
    },
    events: {} as
      | { type: 'ADD_TASK'; title: string }
      | { type: 'REMOVE_TASK'; id: string }
      | { type: 'COMPLETE_TASK'; id: string }
  },
  actors: {
    task: taskMachine
  }
}).createMachine({
  id: 'todoList',
  initial: 'active',
  context: {
    tasks: new Map(),
    nextId: 0
  },
  states: {
    active: {
      on: {
        ADD_TASK: {
          actions: assign({
            tasks: ({ context, event, spawn }) => {
              const id = `task-${context.nextId}`;
              const taskRef = spawn('task', {
                id,
                input: { id, title: event.title }
              });
              const newTasks = new Map(context.tasks);
              newTasks.set(id, taskRef);
              return newTasks;
            },
            nextId: ({ context }) => context.nextId + 1
          })
        },
        REMOVE_TASK: {
          actions: assign({
            tasks: ({ context, event }) => {
              const newTasks = new Map(context.tasks);
              const taskRef = newTasks.get(event.id);
              if (taskRef) {
                taskRef.stop();
                newTasks.delete(event.id);
              }
              return newTasks;
            }
          })
        },
        COMPLETE_TASK: {
          actions: ({ context, event }) => {
            const taskRef = context.tasks.get(event.id);
            if (taskRef) {
              taskRef.send({ type: 'COMPLETE' });
            }
          }
        }
      }
    }
  }
});
```

## Higher-Order Machines

### Machine Factory Pattern

```typescript
import { setup, fromPromise } from 'xstate';

function createDataFetcherMachine<T>(config: {
  fetchFn: () => Promise<T>;
  retryLimit?: number;
  cacheKey?: string;
}) {
  return setup({
    types: {
      context: {} as {
        data: T | null;
        error: Error | null;
        retryCount: number;
      }
    },
    actors: {
      fetchData: fromPromise(config.fetchFn)
    }
  }).createMachine({
    id: `dataFetcher-${config.cacheKey || 'default'}`,
    initial: 'idle',
    context: {
      data: null,
      error: null,
      retryCount: 0
    },
    states: {
      idle: {
        on: { FETCH: 'loading' }
      },
      loading: {
        invoke: {
          src: 'fetchData',
          onDone: {
            target: 'success',
            actions: assign({ data: ({ event }) => event.output })
          },
          onError: [
            {
              target: 'retrying',
              guard: ({ context }) =>
                context.retryCount < (config.retryLimit || 3),
              actions: assign({
                retryCount: ({ context }) => context.retryCount + 1
              })
            },
            {
              target: 'failure',
              actions: assign({ error: ({ event }) => event.error })
            }
          ]
        }
      },
      retrying: {
        after: { 1000: 'loading' }
      },
      success: {},
      failure: {}
    }
  });
}

// Usage
const userFetcherMachine = createDataFetcherMachine({
  fetchFn: () => fetch('/api/user').then(r => r.json()),
  retryLimit: 5,
  cacheKey: 'user'
});
```

## Receptionist Pattern (systemId)

### Global Actor Registry

```typescript
import { setup } from 'xstate';

// Auth machine
const authMachine = setup({
  types: {
    context: {} as { user: User | null }
  }
}).createMachine({
  id: 'auth',
  initial: 'unauthenticated',
  context: { user: null },
  states: {
    unauthenticated: {},
    authenticated: {}
  }
});

// App machine with systemId
const appMachine = setup({
  actors: {
    auth: authMachine
  }
}).createMachine({
  id: 'app',
  type: 'parallel',
  states: {
    auth: {
      invoke: {
        src: 'auth',
        systemId: 'auth' // Global ID
      }
    },
    dashboard: {
      entry: ({ system }) => {
        const authActor = system.get('auth');
        console.log('Auth state:', authActor.getSnapshot());
      }
    },
    notifications: {
      entry: ({ system }) => {
        const authActor = system.get('auth');
        authActor.subscribe((snapshot) => {
          console.log('Auth changed:', snapshot.context.user);
        });
      }
    }
  }
});
```

## React Integration

### Accessing Child Actors

```typescript
import { useSelector } from '@xstate/react';

function ParentComponent() {
  const actorRef = useActorRef(parentMachine);

  const childSnapshot = useSelector(actorRef, (snapshot) => {
    const childRef = snapshot.children.get('childActor');
    return childRef?.getSnapshot();
  });

  return (
    <div>
      <h2>Parent</h2>
      {childSnapshot && (
        <div>Child: {JSON.stringify(childSnapshot.value)}</div>
      )}
    </div>
  );
}
```

### Context Provider for Composed Machines

```typescript
import { createActorContext } from '@xstate/react';

const RootMachineContext = createActorContext(rootMachine);

function App() {
  return (
    <RootMachineContext.Provider>
      <Dashboard />
      <Notifications />
    </RootMachineContext.Provider>
  );
}

function Dashboard() {
  const actorRef = RootMachineContext.useActorRef();
  const { system } = actorRef;

  const authActor = system.get('auth');
  const user = useSelector(authActor, (s) => s.context.user);

  return <div>Welcome, {user?.name}</div>;
}
```

## Best Practices

### Composition Checklist

✅ **Use sendTo/sendParent** for explicit communication
✅ **Spawn actors dynamically** for variable-length lists
✅ **Use systemId** for global actor registry
✅ **Create machine factories** for reusable patterns
✅ **Compose with parallel states** for orthogonal features
✅ **Keep machines focused** - single responsibility
✅ **Document communication patterns** in comments
✅ **Test composed machines** in isolation first
✅ **Use TypeScript** for type-safe actor references
✅ **Visualize composition** with Stately tools

### When to Compose vs. When to Split

| Scenario | Approach |
|----------|----------|
| Features share state | Compose in parent machine |
| Features are independent | Separate machines, use systemId |
| Dynamic list of items | Spawn actors |
| Reusable behavior | Machine factory or mixin |
| Cross-cutting concerns | Higher-order machine |
| Tight coupling needed | Parent-child with sendTo |
| Loose coupling preferred | Event bus or systemId |

