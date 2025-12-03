# Advanced Middleware Patterns

> Progressive disclosure reference for Express middleware architecture

## Middleware Composition Patterns

### Sequential Composition

Execute middleware in strict order:

```javascript
const sequence = (...middleware) => {
  return async (req, res, next) => {
    let index = 0;

    const runNext = async () => {
      if (index >= middleware.length) return next();

      const current = middleware[index++];
      await current(req, res, runNext);
    };

    try {
      await runNext();
    } catch (error) {
      next(error);
    }
  };
};

// Usage
app.use('/admin', sequence(
  authenticate,
  requireAdmin,
  auditLog,
  rateLimit
));
```

### Conditional Middleware

```javascript
const when = (condition, middleware) => {
  return (req, res, next) => {
    if (condition(req, res)) {
      return middleware(req, res, next);
    }
    next();
  };
};

const unless = (condition, middleware) => {
  return when((req) => !condition(req), middleware);
};

// Usage
app.use(when(
  (req) => req.path.startsWith('/api'),
  rateLimit
));

app.use(unless(
  (req) => req.path === '/health',
  authenticate
));
```

### Parallel Middleware

Execute independent middleware concurrently:

```javascript
const parallel = (...middleware) => {
  return async (req, res, next) => {
    try {
      await Promise.all(
        middleware.map(fn =>
          new Promise((resolve, reject) => {
            fn(req, res, (err) => {
              if (err) reject(err);
              else resolve();
            });
          })
        )
      );
      next();
    } catch (error) {
      next(error);
    }
  };
};

// Usage - load user and permissions in parallel
app.use('/dashboard', parallel(
  loadUser,
  loadPermissions,
  loadSettings
));
```

## Advanced Authentication Patterns

### Multi-Strategy Authentication

```javascript
// middleware/multiAuth.js
const strategies = {
  jwt: (req) => {
    const token = req.headers.authorization?.split(' ')[1];
    return verifyJWT(token);
  },

  apiKey: (req) => {
    const key = req.headers['x-api-key'];
    return verifyApiKey(key);
  },

  session: (req) => {
    return req.session?.user;
  }
};

exports.authenticate = (allowedStrategies = ['jwt']) => {
  return async (req, res, next) => {
    for (const strategy of allowedStrategies) {
      try {
        const user = await strategies[strategy](req);
        if (user) {
          req.user = user;
          req.authStrategy = strategy;
          return next();
        }
      } catch (error) {
        // Try next strategy
        continue;
      }
    }

    next(new AuthenticationError('Authentication required'));
  };
};

// Usage
app.get('/api/data',
  authenticate(['jwt', 'apiKey']),
  getData
);
```

### Permission-Based Authorization

```javascript
// middleware/permissions.js
const permissions = {
  'users:read': ['admin', 'user', 'guest'],
  'users:write': ['admin', 'user'],
  'users:delete': ['admin'],
  'posts:publish': ['admin', 'editor']
};

exports.can = (permission) => {
  return (req, res, next) => {
    if (!req.user) {
      return next(new AuthenticationError());
    }

    const allowedRoles = permissions[permission];
    if (!allowedRoles || !allowedRoles.includes(req.user.role)) {
      return next(new AuthorizationError(
        `Permission denied: ${permission}`
      ));
    }

    next();
  };
};

// Usage
app.delete('/users/:id',
  authenticate,
  can('users:delete'),
  deleteUser
);
```

## Request Context and Tracing

### Request Context Middleware

```javascript
// middleware/context.js
const { AsyncLocalStorage } = require('async_hooks');
const asyncLocalStorage = new AsyncLocalStorage();

exports.contextMiddleware = (req, res, next) => {
  const context = {
    requestId: req.id,
    userId: req.user?.id,
    timestamp: Date.now(),
    method: req.method,
    path: req.path
  };

  asyncLocalStorage.run(context, () => {
    next();
  });
};

exports.getContext = () => {
  return asyncLocalStorage.getStore();
};

// Usage in any module
const { getContext } = require('./middleware/context');

function someFunction() {
  const ctx = getContext();
  logger.info('Processing request', { requestId: ctx.requestId });
}
```

### Distributed Tracing

```javascript
// middleware/tracing.js
const opentelemetry = require('@opentelemetry/api');

exports.tracingMiddleware = (req, res, next) => {
  const tracer = opentelemetry.trace.getTracer('express-app');

  const span = tracer.startSpan(`${req.method} ${req.path}`, {
    attributes: {
      'http.method': req.method,
      'http.url': req.url,
      'http.target': req.path,
      'http.user_agent': req.get('user-agent')
    }
  });

  req.span = span;

  res.on('finish', () => {
    span.setAttribute('http.status_code', res.statusCode);
    span.end();
  });

  next();
};
```

## Caching Middleware

### Response Caching

```javascript
// middleware/cache.js
const redis = require('redis');
const client = redis.createClient();

exports.cacheMiddleware = (duration = 300) => {
  return async (req, res, next) => {
    // Only cache GET requests
    if (req.method !== 'GET') {
      return next();
    }

    const key = `cache:${req.url}`;

    try {
      const cached = await client.get(key);
      if (cached) {
        res.setHeader('X-Cache', 'HIT');
        return res.json(JSON.parse(cached));
      }
    } catch (error) {
      // Cache miss, continue
    }

    // Capture original json method
    const originalJson = res.json.bind(res);

    res.json = (data) => {
      // Cache the response
      client.setEx(key, duration, JSON.stringify(data))
        .catch(err => console.error('Cache error:', err));

      res.setHeader('X-Cache', 'MISS');
      return originalJson(data);
    };

    next();
  };
};

// Usage
app.get('/api/posts',
  cacheMiddleware(600), // 10 minutes
  getPosts
);
```

### Conditional Caching

```javascript
// middleware/conditionalCache.js
exports.conditionalCache = (options = {}) => {
  const {
    duration = 300,
    condition = () => true,
    keyGenerator = (req) => req.url
  } = options;

  return async (req, res, next) => {
    if (!condition(req, res)) {
      return next();
    }

    const key = `cache:${keyGenerator(req)}`;

    // Check cache
    const cached = await redis.get(key);
    if (cached) {
      return res.json(JSON.parse(cached));
    }

    // Intercept response
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      redis.setEx(key, duration, JSON.stringify(data));
      return originalJson(data);
    };

    next();
  };
};

// Usage
app.get('/api/users',
  conditionalCache({
    duration: 300,
    condition: (req) => !req.user?.isAdmin,
    keyGenerator: (req) => `users:${req.query.page || 1}`
  }),
  getUsers
);
```

## Request Transformation

### Body Transformation Middleware

```javascript
// middleware/transform.js
exports.transformRequest = (transformer) => {
  return (req, res, next) => {
    if (req.body) {
      req.body = transformer(req.body);
    }
    next();
  };
};

exports.transformResponse = (transformer) => {
  return (req, res, next) => {
    const originalJson = res.json.bind(res);

    res.json = (data) => {
      const transformed = transformer(data);
      return originalJson(transformed);
    };

    next();
  };
};

// Usage
const camelCaseKeys = require('camelcase-keys');
const snakeCaseKeys = require('snakecase-keys');

// Transform incoming snake_case to camelCase
app.use(transformRequest(camelCaseKeys));

// Transform outgoing camelCase to snake_case for API consumers
app.use(transformResponse(snakeCaseKeys));
```

## Error Handling Middleware

### Typed Error Handler

```javascript
// middleware/typedErrorHandler.js
const errorHandlers = new Map();

errorHandlers.set('ValidationError', (err, req, res) => {
  res.status(400).json({
    error: 'Validation failed',
    details: err.details
  });
});

errorHandlers.set('UnauthorizedError', (err, req, res) => {
  res.status(401).json({
    error: 'Authentication required',
    message: err.message
  });
});

errorHandlers.set('ForbiddenError', (err, req, res) => {
  res.status(403).json({
    error: 'Access denied',
    message: err.message
  });
});

errorHandlers.set('NotFoundError', (err, req, res) => {
  res.status(404).json({
    error: 'Resource not found',
    resource: err.resource
  });
});

module.exports = (err, req, res, next) => {
  const handler = errorHandlers.get(err.name);

  if (handler) {
    return handler(err, req, res);
  }

  // Default error handler
  console.error(err);
  res.status(500).json({
    error: 'Internal server error'
  });
};
```

## Performance Middleware

### Request Throttling

```javascript
// middleware/throttle.js
const bottleneck = require('bottleneck');

exports.throttle = (options = {}) => {
  const limiter = new bottleneck({
    maxConcurrent: options.maxConcurrent || 10,
    minTime: options.minTime || 100
  });

  return (req, res, next) => {
    limiter.schedule(() => {
      return new Promise((resolve) => {
        res.on('finish', resolve);
        next();
      });
    });
  };
};

// Usage - limit concurrent database queries
app.use('/api/heavy-query',
  throttle({ maxConcurrent: 5, minTime: 200 }),
  heavyQueryHandler
);
```

### Request Timeout

```javascript
// middleware/timeout.js
exports.timeout = (ms = 30000) => {
  return (req, res, next) => {
    const timer = setTimeout(() => {
      if (!res.headersSent) {
        res.status(503).json({
          error: 'Request timeout',
          timeout: ms
        });
      }
    }, ms);

    res.on('finish', () => clearTimeout(timer));
    next();
  };
};

// Usage
app.use('/api/slow-endpoint',
  timeout(5000), // 5 second timeout
  slowHandler
);
```

## Related Patterns

- [Security Hardening](./security-hardening.md) - Security-focused middleware
- [Testing Strategies](./testing-strategies.md) - Testing middleware
- [Production Deployment](./production-deployment.md) - Production middleware patterns
