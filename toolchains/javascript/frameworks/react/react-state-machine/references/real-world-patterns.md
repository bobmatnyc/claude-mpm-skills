# Real-World State Machine Patterns

## Complete Authentication Flow

### Machine Definition

```typescript
import { setup, assign, fromPromise } from 'xstate';

interface User {
  id: string;
  email: string;
  name: string;
  token: string;
  refreshToken: string;
}

interface AuthContext {
  user: User | null;
  error: string | null;
  sessionExpiry: number | null;
}

type AuthEvent =
  | { type: 'LOGIN'; email: string; password: string }
  | { type: 'LOGOUT' }
  | { type: 'REFRESH_SESSION' }
  | { type: 'SESSION_EXPIRED' }
  | { type: 'RETRY' };

export const authMachine = setup({
  types: {
    context: {} as AuthContext,
    events: {} as AuthEvent
  },
  actors: {
    loginUser: fromPromise(async ({ input }: { input: { email: string; password: string } }) => {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Login failed');
      }
      
      return response.json() as Promise<User>;
    }),
    
    refreshSession: fromPromise(async ({ input }: { input: { refreshToken: string } }) => {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken: input.refreshToken })
      });
      
      if (!response.ok) throw new Error('Session refresh failed');
      return response.json() as Promise<User>;
    }),
    
    logoutUser: fromPromise(async ({ input }: { input: { token: string } }) => {
      await fetch('/api/auth/logout', {
        method: 'POST',
        headers: { Authorization: `Bearer ${input.token}` }
      });
    })
  },
  actions: {
    setUser: assign({
      user: ({ event }) => event.output,
      error: null,
      sessionExpiry: () => Date.now() + 3600000 // 1 hour
    }),
    
    clearUser: assign({
      user: null,
      error: null,
      sessionExpiry: null
    }),
    
    setError: assign({
      error: ({ event }) => event.error.message
    }),
    
    persistSession: ({ context }) => {
      if (context.user) {
        localStorage.setItem('auth_token', context.user.token);
        localStorage.setItem('refresh_token', context.user.refreshToken);
      }
    },
    
    clearSession: () => {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
  },
  guards: {
    hasRefreshToken: ({ context }) => !!context.user?.refreshToken
  }
}).createMachine({
  id: 'auth',
  initial: 'checkingSession',
  context: {
    user: null,
    error: null,
    sessionExpiry: null
  },
  states: {
    checkingSession: {
      always: [
        { target: 'authenticated', guard: ({ context }) => !!context.user },
        { target: 'unauthenticated' }
      ]
    },
    
    unauthenticated: {
      on: {
        LOGIN: 'authenticating'
      }
    },
    
    authenticating: {
      invoke: {
        src: 'loginUser',
        input: ({ event }) => ({
          email: event.email,
          password: event.password
        }),
        onDone: {
          target: 'authenticated',
          actions: ['setUser', 'persistSession']
        },
        onError: {
          target: 'authenticationFailed',
          actions: 'setError'
        }
      }
    },
    
    authenticationFailed: {
      on: {
        RETRY: 'unauthenticated',
        LOGIN: 'authenticating'
      }
    },
    
    authenticated: {
      // Auto-refresh before expiry
      after: {
        3300000: { // 55 minutes
          target: 'refreshing',
          guard: 'hasRefreshToken'
        }
      },
      on: {
        LOGOUT: 'loggingOut',
        SESSION_EXPIRED: 'sessionExpired',
        REFRESH_SESSION: 'refreshing'
      }
    },
    
    refreshing: {
      invoke: {
        src: 'refreshSession',
        input: ({ context }) => ({
          refreshToken: context.user!.refreshToken
        }),
        onDone: {
          target: 'authenticated',
          actions: ['setUser', 'persistSession']
        },
        onError: 'sessionExpired'
      }
    },
    
    sessionExpired: {
      entry: 'clearSession',
      on: {
        LOGIN: 'authenticating'
      }
    },
    
    loggingOut: {
      invoke: {
        src: 'logoutUser',
        input: ({ context }) => ({
          token: context.user!.token
        }),
        onDone: {
          target: 'unauthenticated',
          actions: ['clearUser', 'clearSession']
        },
        onError: {
          target: 'unauthenticated',
          actions: ['clearUser', 'clearSession']
        }
      }
    }
  }
});
```

### React Integration

```typescript
import { useMachine } from '@xstate/react';
import { authMachine } from './authMachine';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [snapshot, send] = useMachine(authMachine);
  
  return (
    <AuthContext.Provider value={{ snapshot, send }}>
      {children}
    </AuthContext.Provider>
  );
}

export function LoginForm() {
  const { snapshot, send } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    send({ type: 'LOGIN', email, password });
  };
  
  if (snapshot.matches('authenticated')) {
    return <Navigate to="/dashboard" />;
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      
      {snapshot.matches('authenticationFailed') && (
        <div className="error">{snapshot.context.error}</div>
      )}
      
      <button
        type="submit"
        disabled={snapshot.matches('authenticating')}
      >
        {snapshot.matches('authenticating') ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

## File Upload with Progress

### Machine Definition

```typescript
import { setup, assign, fromPromise, fromCallback } from 'xstate';

interface UploadContext {
  file: File | null;
  progress: number;
  uploadedUrl: string | null;
  error: string | null;
  abortController: AbortController | null;
}

type UploadEvent =
  | { type: 'SELECT_FILE'; file: File }
  | { type: 'START_UPLOAD' }
  | { type: 'CANCEL' }
  | { type: 'RETRY' }
  | { type: 'RESET' };

export const fileUploadMachine = setup({
  types: {
    context: {} as UploadContext,
    events: {} as UploadEvent
  },
  actors: {
    uploadFile: fromCallback(({ sendBack, receive, input }) => {
      const { file } = input as { file: File };
      const abortController = new AbortController();

      const xhr = new XMLHttpRequest();

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const progress = Math.round((e.loaded / e.total) * 100);
          sendBack({ type: 'PROGRESS_UPDATE', progress });
        }
      });

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          const response = JSON.parse(xhr.responseText);
          sendBack({ type: 'UPLOAD_SUCCESS', url: response.url });
        } else {
          sendBack({ type: 'UPLOAD_ERROR', error: 'Upload failed' });
        }
      });

      xhr.addEventListener('error', () => {
        sendBack({ type: 'UPLOAD_ERROR', error: 'Network error' });
      });

      xhr.addEventListener('abort', () => {
        sendBack({ type: 'UPLOAD_CANCELLED' });
      });

      // Handle cancel from parent
      receive((event) => {
        if (event.type === 'CANCEL') {
          xhr.abort();
        }
      });

      const formData = new FormData();
      formData.append('file', file);

      xhr.open('POST', '/api/upload');
      xhr.send(formData);

      return () => xhr.abort();
    })
  },
  actions: {
    setFile: assign({
      file: ({ event }) => event.file,
      error: null
    }),

    updateProgress: assign({
      progress: ({ event }) => event.progress
    }),

    setUploadedUrl: assign({
      uploadedUrl: ({ event }) => event.url,
      progress: 100
    }),

    setError: assign({
      error: ({ event }) => event.error
    }),

    resetUpload: assign({
      file: null,
      progress: 0,
      uploadedUrl: null,
      error: null,
      abortController: null
    })
  },
  guards: {
    hasFile: ({ context }) => context.file !== null,
    isValidFileSize: ({ context }) => {
      const maxSize = 10 * 1024 * 1024; // 10MB
      return context.file ? context.file.size <= maxSize : false;
    },
    isValidFileType: ({ context }) => {
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
      return context.file ? allowedTypes.includes(context.file.type) : false;
    }
  }
}).createMachine({
  id: 'fileUpload',
  initial: 'idle',
  context: {
    file: null,
    progress: 0,
    uploadedUrl: null,
    error: null,
    abortController: null
  },
  states: {
    idle: {
      on: {
        SELECT_FILE: {
          target: 'validating',
          actions: 'setFile'
        }
      }
    },

    validating: {
      always: [
        {
          target: 'invalid',
          guard: ({ context }) => !context.file,
          actions: assign({ error: 'No file selected' })
        },
        {
          target: 'invalid',
          guard: ({ context }) => {
            const maxSize = 10 * 1024 * 1024;
            return context.file ? context.file.size > maxSize : true;
          },
          actions: assign({ error: 'File too large (max 10MB)' })
        },
        {
          target: 'invalid',
          guard: ({ context }) => {
            const allowed = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
            return context.file ? !allowed.includes(context.file.type) : true;
          },
          actions: assign({ error: 'Invalid file type' })
        },
        { target: 'ready' }
      ]
    },

    invalid: {
      on: {
        SELECT_FILE: {
          target: 'validating',
          actions: 'setFile'
        },
        RESET: {
          target: 'idle',
          actions: 'resetUpload'
        }
      }
    },

    ready: {
      on: {
        START_UPLOAD: 'uploading',
        SELECT_FILE: {
          target: 'validating',
          actions: 'setFile'
        },
        RESET: {
          target: 'idle',
          actions: 'resetUpload'
        }
      }
    },

    uploading: {
      invoke: {
        src: 'uploadFile',
        input: ({ context }) => ({ file: context.file! })
      },
      on: {
        PROGRESS_UPDATE: {
          actions: 'updateProgress'
        },
        UPLOAD_SUCCESS: {
          target: 'success',
          actions: 'setUploadedUrl'
        },
        UPLOAD_ERROR: {
          target: 'failed',
          actions: 'setError'
        },
        UPLOAD_CANCELLED: 'cancelled',
        CANCEL: 'cancelling'
      }
    },

    cancelling: {
      after: {
        100: 'cancelled'
      }
    },

    cancelled: {
      on: {
        RETRY: 'ready',
        RESET: {
          target: 'idle',
          actions: 'resetUpload'
        }
      }
    },

    failed: {
      on: {
        RETRY: 'uploading',
        RESET: {
          target: 'idle',
          actions: 'resetUpload'
        }
      }
    },

    success: {
      on: {
        RESET: {
          target: 'idle',
          actions: 'resetUpload'
        }
      }
    }
  }
});
```

### React Component

```typescript
import { useMachine } from '@xstate/react';
import { fileUploadMachine } from './fileUploadMachine';

export function FileUploader() {
  const [snapshot, send] = useMachine(fileUploadMachine);
  const { file, progress, uploadedUrl, error } = snapshot.context;

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      send({ type: 'SELECT_FILE', file: selectedFile });
    }
  };

  return (
    <div className="file-uploader">
      {snapshot.matches('idle') && (
        <div>
          <input
            type="file"
            onChange={handleFileSelect}
            accept="image/*,.pdf"
          />
        </div>
      )}

      {snapshot.matches('invalid') && (
        <div className="error">
          {error}
          <button onClick={() => send({ type: 'RESET' })}>Try Again</button>
        </div>
      )}

      {snapshot.matches('ready') && file && (
        <div>
          <p>Selected: {file.name} ({(file.size / 1024).toFixed(2)} KB)</p>
          <button onClick={() => send({ type: 'START_UPLOAD' })}>Upload</button>
          <button onClick={() => send({ type: 'RESET' })}>Cancel</button>
        </div>
      )}

      {snapshot.matches('uploading') && (
        <div>
          <p>Uploading {file?.name}...</p>
          <progress value={progress} max={100} />
          <span>{progress}%</span>
          <button onClick={() => send({ type: 'CANCEL' })}>Cancel Upload</button>
        </div>
      )}

      {snapshot.matches('failed') && (
        <div className="error">
          <p>Upload failed: {error}</p>
          <button onClick={() => send({ type: 'RETRY' })}>Retry</button>
          <button onClick={() => send({ type: 'RESET' })}>Start Over</button>
        </div>
      )}

      {snapshot.matches('success') && uploadedUrl && (
        <div className="success">
          <p>Upload successful!</p>
          <a href={uploadedUrl} target="_blank" rel="noopener noreferrer">View File</a>
          <button onClick={() => send({ type: 'RESET' })}>Upload Another</button>
        </div>
      )}
    </div>
  );
}
```

## Undo/Redo Pattern

### Machine Definition

```typescript
import { setup, assign } from 'xstate';

interface HistoryContext<T> {
  past: T[];
  present: T;
  future: T[];
  canUndo: boolean;
  canRedo: boolean;
}

type HistoryEvent<T> =
  | { type: 'UPDATE'; value: T }
  | { type: 'UNDO' }
  | { type: 'REDO' }
  | { type: 'CLEAR_HISTORY' };

export function createHistoryMachine<T>(initialValue: T) {
  return setup({
    types: {
      context: {} as HistoryContext<T>,
      events: {} as HistoryEvent<T>
    },
    actions: {
      updateValue: assign({
        past: ({ context, event }) => [...context.past, context.present],
        present: ({ event }) => event.value,
        future: [], // Clear future on new action
        canUndo: true,
        canRedo: false
      }),

      undo: assign({
        past: ({ context }) => context.past.slice(0, -1),
        present: ({ context }) => context.past[context.past.length - 1],
        future: ({ context }) => [context.present, ...context.future],
        canUndo: ({ context }) => context.past.length > 1,
        canRedo: true
      }),

      redo: assign({
        past: ({ context }) => [...context.past, context.present],
        present: ({ context }) => context.future[0],
        future: ({ context }) => context.future.slice(1),
        canUndo: true,
        canRedo: ({ context }) => context.future.length > 1
      }),

      clearHistory: assign({
        past: [],
        future: [],
        canUndo: false,
        canRedo: false
      })
    },
    guards: {
      canUndo: ({ context }) => context.past.length > 0,
      canRedo: ({ context }) => context.future.length > 0
    }
  }).createMachine({
    id: 'history',
    initial: 'idle',
    context: {
      past: [],
      present: initialValue,
      future: [],
      canUndo: false,
      canRedo: false
    },
    states: {
      idle: {
        on: {
          UPDATE: {
            actions: 'updateValue'
          },
          UNDO: {
            guard: 'canUndo',
            actions: 'undo'
          },
          REDO: {
            guard: 'canRedo',
            actions: 'redo'
          },
          CLEAR_HISTORY: {
            actions: 'clearHistory'
          }
        }
      }
    }
  });
}
```

### React Integration (Drawing App Example)

```typescript
import { useMachine } from '@xstate/react';
import { createHistoryMachine } from './historyMachine';

interface DrawingState {
  paths: Path[];
  color: string;
  strokeWidth: number;
}

export function DrawingApp() {
  const [snapshot, send] = useMachine(
    createHistoryMachine<DrawingState>({
      paths: [],
      color: '#000000',
      strokeWidth: 2
    })
  );

  const { present, canUndo, canRedo } = snapshot.context;

  const addPath = (path: Path) => {
    send({
      type: 'UPDATE',
      value: {
        ...present,
        paths: [...present.paths, path]
      }
    });
  };

  const changeColor = (color: string) => {
    send({
      type: 'UPDATE',
      value: { ...present, color }
    });
  };

  return (
    <div>
      <div className="toolbar">
        <button
          onClick={() => send({ type: 'UNDO' })}
          disabled={!canUndo}
        >
          Undo
        </button>
        <button
          onClick={() => send({ type: 'REDO' })}
          disabled={!canRedo}
        >
          Redo
        </button>
        <input
          type="color"
          value={present.color}
          onChange={(e) => changeColor(e.target.value)}
        />
      </div>

      <Canvas
        paths={present.paths}
        color={present.color}
        strokeWidth={present.strokeWidth}
        onPathComplete={addPath}
      />
    </div>
  );
}
```

## Multi-Step Wizard/Stepper Pattern

### Machine Definition

```typescript
import { setup, assign } from 'xstate';

interface WizardStep {
  id: string;
  title: string;
  isValid: (data: any) => boolean;
}

interface WizardContext {
  currentStep: number;
  totalSteps: number;
  data: Record<string, any>;
  errors: Record<string, string>;
  steps: WizardStep[];
}

type WizardEvent =
  | { type: 'NEXT' }
  | { type: 'PREVIOUS' }
  | { type: 'GO_TO_STEP'; step: number }
  | { type: 'UPDATE_DATA'; field: string; value: any }
  | { type: 'SUBMIT' }
  | { type: 'RESET' };

export const wizardMachine = setup({
  types: {
    context: {} as WizardContext,
    events: {} as WizardEvent
  },
  actions: {
    updateData: assign({
      data: ({ context, event }) => ({
        ...context.data,
        [event.field]: event.value
      }),
      errors: ({ context, event }) => {
        const { [event.field]: _, ...rest } = context.errors;
        return rest;
      }
    }),

    nextStep: assign({
      currentStep: ({ context }) => Math.min(context.currentStep + 1, context.totalSteps - 1)
    }),

    previousStep: assign({
      currentStep: ({ context }) => Math.max(context.currentStep - 1, 0)
    }),

    goToStep: assign({
      currentStep: ({ event }) => event.step
    }),

    setValidationError: assign({
      errors: ({ context, event }) => ({
        ...context.errors,
        [event.field]: event.message
      })
    }),

    resetWizard: assign({
      currentStep: 0,
      data: {},
      errors: {}
    })
  },
  guards: {
    isCurrentStepValid: ({ context }) => {
      const currentStepDef = context.steps[context.currentStep];
      return currentStepDef.isValid(context.data);
    },

    isNotFirstStep: ({ context }) => context.currentStep > 0,

    isNotLastStep: ({ context }) => context.currentStep < context.totalSteps - 1,

    canGoToStep: ({ context, event }) => {
      // Can only go to visited steps or next unvisited step
      return event.step <= context.currentStep + 1 && event.step >= 0;
    }
  }
}).createMachine({
  id: 'wizard',
  initial: 'editing',
  context: ({ input }: { input: { steps: WizardStep[] } }) => ({
    currentStep: 0,
    totalSteps: input.steps.length,
    data: {},
    errors: {},
    steps: input.steps
  }),
  states: {
    editing: {
      on: {
        UPDATE_DATA: {
          actions: 'updateData'
        },
        NEXT: [
          {
            guard: 'isCurrentStepValid',
            actions: 'nextStep'
          },
          {
            actions: 'setValidationError'
          }
        ],
        PREVIOUS: {
          guard: 'isNotFirstStep',
          actions: 'previousStep'
        },
        GO_TO_STEP: {
          guard: 'canGoToStep',
          actions: 'goToStep'
        },
        SUBMIT: {
          guard: 'isCurrentStepValid',
          target: 'submitting'
        }
      }
    },

    submitting: {
      invoke: {
        src: 'submitWizard',
        input: ({ context }) => context.data,
        onDone: 'success',
        onError: {
          target: 'editing',
          actions: assign({
            errors: ({ event }) => ({ submit: event.error.message })
          })
        }
      }
    },

    success: {
      on: {
        RESET: {
          target: 'editing',
          actions: 'resetWizard'
        }
      }
    }
  }
});
```

### React Component

```typescript
import { useMachine } from '@xstate/react';
import { wizardMachine } from './wizardMachine';

const steps = [
  {
    id: 'personal',
    title: 'Personal Information',
    isValid: (data) => data.name && data.email
  },
  {
    id: 'address',
    title: 'Address',
    isValid: (data) => data.street && data.city && data.zip
  },
  {
    id: 'payment',
    title: 'Payment',
    isValid: (data) => data.cardNumber && data.cvv
  },
  {
    id: 'review',
    title: 'Review',
    isValid: () => true
  }
];

export function Wizard() {
  const [snapshot, send] = useMachine(wizardMachine, {
    input: { steps }
  });

  const { currentStep, totalSteps, data, errors } = snapshot.context;
  const currentStepDef = steps[currentStep];

  return (
    <div className="wizard">
      {/* Progress Indicator */}
      <div className="wizard-progress">
        {steps.map((step, index) => (
          <div
            key={step.id}
            className={`step ${index === currentStep ? 'active' : ''} ${
              index < currentStep ? 'completed' : ''
            }`}
            onClick={() => send({ type: 'GO_TO_STEP', step: index })}
          >
            <div className="step-number">{index + 1}</div>
            <div className="step-title">{step.title}</div>
          </div>
        ))}
      </div>

      {/* Step Content */}
      <div className="wizard-content">
        {currentStep === 0 && (
          <PersonalInfoStep
            data={data}
            errors={errors}
            onChange={(field, value) =>
              send({ type: 'UPDATE_DATA', field, value })
            }
          />
        )}

        {currentStep === 1 && (
          <AddressStep
            data={data}
            errors={errors}
            onChange={(field, value) =>
              send({ type: 'UPDATE_DATA', field, value })
            }
          />
        )}

        {currentStep === 2 && (
          <PaymentStep
            data={data}
            errors={errors}
            onChange={(field, value) =>
              send({ type: 'UPDATE_DATA', field, value })
            }
          />
        )}

        {currentStep === 3 && <ReviewStep data={data} />}
      </div>

      {/* Navigation */}
      <div className="wizard-actions">
        {currentStep > 0 && (
          <button onClick={() => send({ type: 'PREVIOUS' })}>
            Previous
          </button>
        )}

        {currentStep < totalSteps - 1 && (
          <button onClick={() => send({ type: 'NEXT' })}>
            Next
          </button>
        )}

        {currentStep === totalSteps - 1 && (
          <button
            onClick={() => send({ type: 'SUBMIT' })}
            disabled={snapshot.matches('submitting')}
          >
            {snapshot.matches('submitting') ? 'Submitting...' : 'Submit'}
          </button>
        )}
      </div>
    </div>
  );
}
```

