---
name: express-production
description: Production-ready Express.js development covering middleware architecture, error handling, security hardening, testing strategies, and deployment patterns
skill_version: 2.0.0
updated_at: 2025-12-03T00:00:00Z
tags: [express, nodejs, production, middleware, security, testing, deployment, backend]
progressive_disclosure:
  entry_point:
    summary: "Production-ready Express.js framework with comprehensive middleware, security, testing, and deployment patterns"
    when_to_use: "Building production REST APIs, microservices, web applications requiring robust middleware architecture, security hardening, and comprehensive testing"
    quick_start: "1. npm install express 2. Create app.js with middleware stack 3. Implement error handling 4. Add security middleware 5. Deploy with PM2"
  references:
    - references/middleware-patterns.md
    - references/security-hardening.md
    - references/testing-strategies.md
    - references/production-deployment.md
context_limit: 800
---

# Express.js - Production Web Framework

## Overview

Express is a minimal and flexible Node.js web application framework providing a robust set of features for web and mobile applications. This skill covers **production-ready** Express development including middleware architecture, structured error handling, security hardening, comprehensive testing, and deployment strategies.

**Key Features**:
- Flexible middleware architecture with composition patterns
- Centralized error handling with async support
- Security hardening (Helmet, CORS, rate limiting, input validation)
- Comprehensive testing with Supertest
- Production deployment with PM2 clustering
- Environment-based configuration
- Structured logging and monitoring
- Graceful shutdown patterns
- Zero-downtime deployments

**Installation**:
```bash
# Basic Express
npm install express

# Production stack
npm install express helmet cors express-rate-limit express-validator
npm install morgan winston compression
npm install dotenv

# Development tools
npm install -D nodemon supertest jest

# Optional: Database and auth
npm install mongoose jsonwebtoken bcrypt
```

## When to Use This Skill

Use this comprehensive Express skill when:
- Building production REST APIs
- Creating microservices architectures
- Implementing secure web applications
- Need flexible middleware composition
- Require comprehensive error handling
- Building systems requiring extensive testing
- Deploying high-availability services
- Need granular control over request/response lifecycle

**Express vs Other Frameworks**:
- **Express**: Maximum flexibility, unopinionated, extensive ecosystem
- **Fastify**: Performance-focused, schema-based validation
- **Koa**: Modern async/await, minimalist
- **NestJS**: TypeScript-first, opinionated, enterprise patterns

## Quick Start

### Minimal Express Server

```javascript
// server.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Hello World' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
```

**Run Development Server**:
```bash
# Install nodemon
npm install -D nodemon

# Run with nodemon
npx nodemon server.js

# Or add to package.json
npm run dev
```

### Production-Ready Server Structure

```
project/
├── src/
│   ├── app.js              # Express app factory
│   ├── server.js           # Server entry point
│   ├── config/
│   │   ├── index.js        # Configuration management
│   │   └── logger.js       # Winston logger setup
│   ├── middleware/
│   │   ├── errorHandler.js # Centralized error handling
│   │   ├── validation.js   # Input validation
│   │   ├── auth.js         # Authentication middleware
│   │   └── rateLimiter.js  # Rate limiting
│   ├── routes/
│   │   ├── index.js        # Route aggregator
│   │   ├── users.js        # User routes
│   │   └── api/            # API versioning
│   ├── controllers/
│   │   ├── userController.js
│   │   └── authController.js
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── utils/
│   │   ├── AppError.js     # Custom error class
│   │   └── catchAsync.js   # Async wrapper
│   └── tests/
│       ├── unit/
│       └── integration/
├── ecosystem.config.js     # PM2 configuration
├── .env.example            # Environment template
├── nodemon.json            # Nodemon config
└── package.json
```

## Middleware Architecture

### Understanding Middleware

Middleware functions are functions that have access to the request object (`req`), response object (`res`), and the next middleware function (`next`).

**Middleware Types**:
1. **Application-level**: `app.use()` or `app.METHOD()`
2. **Router-level**: `router.use()` or `router.METHOD()`
3. **Error-handling**: Four parameters `(err, req, res, next)`
4. **Built-in**: `express.json()`, `express.static()`
5. **Third-party**: `helmet`, `cors`, `morgan`

### Proper Middleware Order

✅ **Correct Order**:
```javascript
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const app = express();

// 1. Security headers (FIRST)
app.use(helmet());

// 2. CORS configuration
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// 3. Rate limiting (before parsing)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});
app.use('/api/', limiter);

// 4. Request parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 5. Compression
app.use(compression());

// 6. Logging
if (process.env.NODE_ENV !== 'production') {
  app.use(morgan('dev'));
} else {
  app.use(morgan('combined'));
}

// 7. Static files (if needed)
app.use(express.static('public'));

// 8. Custom middleware
app.use(require('./middleware/requestId'));
app.use(require('./middleware/timing'));

// 9. Routes
app.use('/api/v1/users', require('./routes/users'));
app.use('/api/v1/posts', require('./routes/posts'));

// 10. 404 handler (after all routes)
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// 11. Error handling (LAST)
app.use(require('./middleware/errorHandler'));
```

❌ **Wrong Order**:
```javascript
// DON'T: Routes before security
app.use('/api/users', userRoutes); // Routes first
app.use(helmet()); // Security too late!

// DON'T: Error handler before routes
app.use(errorHandler); // Error handler first
app.use('/api/users', userRoutes); // Routes won't be caught

// DON'T: Parsing after routes
app.use('/api/users', userRoutes);
app.use(express.json()); // Too late to parse!
```

### Custom Middleware Patterns

**Request ID Middleware**:
```javascript
// middleware/requestId.js
const { v4: uuidv4 } = require('uuid');

module.exports = function requestId(req, res, next) {
  req.id = req.headers['x-request-id'] || uuidv4();
  res.setHeader('X-Request-ID', req.id);
  next();
};
```

**Request Timing Middleware**:
```javascript
// middleware/timing.js
module.exports = function timing(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${duration}ms`);
  });

  next();
};
```

**Authentication Middleware**:
```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');
const AppError = require('../utils/AppError');

exports.authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return next(new AppError('No token provided', 401));
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    next(new AppError('Invalid token', 401));
  }
};

exports.authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return next(new AppError('Not authenticated', 401));
    }

    if (!roles.includes(req.user.role)) {
      return next(new AppError('Insufficient permissions', 403));
    }

    next();
  };
};
```

**Usage**:
```javascript
const { authenticate, authorize } = require('./middleware/auth');

// Public route
app.get('/api/posts', getPosts);

// Authenticated route
app.get('/api/profile', authenticate, getProfile);

// Role-based authorization
app.delete('/api/users/:id',
  authenticate,
  authorize('admin', 'moderator'),
  deleteUser
);
```

### Async Middleware

✅ **Correct Async Handling**:
```javascript
// utils/catchAsync.js
module.exports = (fn) => {
  return (req, res, next) => {
    fn(req, res, next).catch(next);
  };
};

// Usage
const catchAsync = require('../utils/catchAsync');

app.get('/users', catchAsync(async (req, res) => {
  const users = await User.find();
  res.json({ users });
}));
```

❌ **Wrong: No Error Handling**:
```javascript
// DON'T: Async without catch
app.get('/users', async (req, res) => {
  const users = await User.find(); // Unhandled rejection!
  res.json({ users });
});
```

### Middleware Composition

**Compose Multiple Middleware**:
```javascript
// middleware/compose.js
const compose = (...middleware) => {
  return (req, res, next) => {
    let index = 0;

    const dispatch = (i) => {
      if (i >= middleware.length) return next();

      const fn = middleware[i];
      try {
        fn(req, res, () => dispatch(i + 1));
      } catch (err) {
        next(err);
      }
    };

    dispatch(0);
  };
};

// Usage
const adminOnly = compose(
  authenticate,
  authorize('admin'),
  validateRequest
);

app.delete('/api/users/:id', adminOnly, deleteUser);
```

**Conditional Middleware**:
```javascript
// Apply middleware conditionally
const conditionalMiddleware = (condition, middleware) => {
  return (req, res, next) => {
    if (condition(req)) {
      return middleware(req, res, next);
    }
    next();
  };
};

// Only log in development
app.use(conditionalMiddleware(
  (req) => process.env.NODE_ENV === 'development',
  morgan('dev')
));
```

## Structured Error Handling

### Custom Error Classes

```javascript
// utils/AppError.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);

    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = AppError;
```

**Error Hierarchy**:
```javascript
// utils/errors.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

class ValidationError extends AppError {
  constructor(message, errors = []) {
    super(message, 400);
    this.errors = errors;
  }
}

class AuthenticationError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 401);
  }
}

class AuthorizationError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(message, 403);
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404);
  }
}

class ConflictError extends AppError {
  constructor(message = 'Resource conflict') {
    super(message, 409);
  }
}

module.exports = {
  AppError,
  ValidationError,
  AuthenticationError,
  AuthorizationError,
  NotFoundError,
  ConflictError
};
```

### Centralized Error Handler

```javascript
// middleware/errorHandler.js
const logger = require('../config/logger');

function errorHandler(err, req, res, next) {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';

  // Log error
  logger.error({
    message: err.message,
    statusCode: err.statusCode,
    stack: err.stack,
    path: req.path,
    method: req.method,
    ip: req.ip,
    userId: req.user?.id
  });

  // Development: send full error
  if (process.env.NODE_ENV === 'development') {
    return res.status(err.statusCode).json({
      status: err.status,
      error: err,
      message: err.message,
      stack: err.stack
    });
  }

  // Production: sanitize errors
  if (err.isOperational) {
    // Operational, trusted error: send to client
    return res.status(err.statusCode).json({
      status: err.status,
      message: err.message,
      ...(err.errors && { errors: err.errors })
    });
  }

  // Programming or unknown error: don't leak details
  console.error('ERROR 💥', err);
  return res.status(500).json({
    status: 'error',
    message: 'Something went wrong'
  });
}

module.exports = errorHandler;
```

### Handling Specific Error Types

```javascript
// middleware/errorHandler.js (extended)
function handleCastError(err) {
  const message = `Invalid ${err.path}: ${err.value}`;
  return new AppError(message, 400);
}

function handleDuplicateFields(err) {
  const field = Object.keys(err.keyValue)[0];
  const message = `Duplicate field value: ${field}. Please use another value`;
  return new AppError(message, 400);
}

function handleValidationError(err) {
  const errors = Object.values(err.errors).map(el => el.message);
  const message = `Invalid input data. ${errors.join('. ')}`;
  return new AppError(message, 400);
}

function handleJWTError() {
  return new AppError('Invalid token. Please log in again', 401);
}

function handleJWTExpiredError() {
  return new AppError('Your token has expired. Please log in again', 401);
}

module.exports = (err, req, res, next) => {
  let error = { ...err };
  error.message = err.message;

  // Mongoose bad ObjectId
  if (err.name === 'CastError') error = handleCastError(error);

  // Mongoose duplicate key
  if (err.code === 11000) error = handleDuplicateFields(error);

  // Mongoose validation error
  if (err.name === 'ValidationError') error = handleValidationError(error);

  // JWT errors
  if (err.name === 'JsonWebTokenError') error = handleJWTError();
  if (err.name === 'TokenExpiredError') error = handleJWTExpiredError();

  // Send response
  sendErrorResponse(error, req, res);
};
```

### Async Error Handling

```javascript
// utils/catchAsync.js
const catchAsync = (fn) => {
  return (req, res, next) => {
    fn(req, res, next).catch(next);
  };
};

module.exports = catchAsync;

// Usage in controllers
const catchAsync = require('../utils/catchAsync');
const User = require('../models/User');
const { NotFoundError } = require('../utils/errors');

exports.getUser = catchAsync(async (req, res, next) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    return next(new NotFoundError('User'));
  }

  res.json({ user });
});

exports.createUser = catchAsync(async (req, res, next) => {
  const user = await User.create(req.body);
  res.status(201).json({ user });
});
```

### Unhandled Rejections

```javascript
// server.js
const app = require('./app');

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION! 💥 Shutting down...');
  console.error(err.name, err.message);

  server.close(() => {
    process.exit(1);
  });
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  console.error('UNCAUGHT EXCEPTION! 💥 Shutting down...');
  console.error(err.name, err.message);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('👋 SIGTERM RECEIVED. Shutting down gracefully');
  server.close(() => {
    console.log('💥 Process terminated!');
  });
});
```

## Security Hardening

### Helmet.js Configuration

```javascript
// config/security.js
const helmet = require('helmet');

const securityConfig = helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },

  // Strict Transport Security
  hsts: {
    maxAge: 31536000, // 1 year
    includeSubDomains: true,
    preload: true
  },

  // X-Frame-Options
  frameguard: {
    action: 'deny'
  },

  // X-Content-Type-Options
  noSniff: true,

  // X-XSS-Protection
  xssFilter: true,

  // Referrer-Policy
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  }
});

module.exports = securityConfig;
```

**Usage**:
```javascript
// app.js
const securityConfig = require('./config/security');

app.use(securityConfig);
```

### CORS Configuration

```javascript
// config/cors.js
const cors = require('cors');

const whitelist = process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'];

const corsOptions = {
  origin: function (origin, callback) {
    // Allow requests with no origin (mobile apps, Postman)
    if (!origin) return callback(null, true);

    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
  exposedHeaders: ['X-Total-Count', 'X-Page-Number'],
  maxAge: 86400 // 24 hours
};

module.exports = cors(corsOptions);
```

### Rate Limiting

```javascript
// middleware/rateLimiter.js
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

// Redis client for distributed rate limiting
const redisClient = redis.createClient({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

// General rate limiter
exports.generalLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:general:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later',
  standardHeaders: true, // Return rate limit info in RateLimit-* headers
  legacyHeaders: false // Disable X-RateLimit-* headers
});

// Strict rate limiter for auth endpoints
exports.authLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // limit each IP to 5 login attempts per windowMs
  message: 'Too many login attempts, please try again later',
  skipSuccessfulRequests: true // Don't count successful requests
});

// API key limiter (higher limits for authenticated users)
exports.apiKeyLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 1000,
  keyGenerator: (req) => req.headers['x-api-key'] || req.ip,
  skip: (req) => !req.headers['x-api-key']
});
```

**Usage**:
```javascript
const { generalLimiter, authLimiter } = require('./middleware/rateLimiter');

// Apply to all routes
app.use('/api/', generalLimiter);

// Strict limiting for auth
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);
```

### Input Validation and Sanitization

```javascript
// middleware/validation.js
const { body, param, query, validationResult } = require('express-validator');
const { ValidationError } = require('../utils/errors');

// Validation middleware
exports.validate = (req, res, next) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    const extractedErrors = errors.array().map(err => ({
      field: err.param,
      message: err.msg,
      value: err.value
    }));

    return next(new ValidationError('Validation failed', extractedErrors));
  }

  next();
};

// User validation rules
exports.createUserRules = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Must be a valid email'),
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain uppercase, lowercase, and number'),
  body('name')
    .trim()
    .notEmpty()
    .withMessage('Name is required')
    .isLength({ max: 100 })
    .withMessage('Name too long')
    .escape(), // XSS protection
  body('age')
    .optional()
    .isInt({ min: 0, max: 150 })
    .withMessage('Age must be between 0 and 150')
];

exports.updateUserRules = [
  param('id')
    .isMongoId()
    .withMessage('Invalid user ID'),
  body('email')
    .optional()
    .isEmail()
    .normalizeEmail(),
  body('name')
    .optional()
    .trim()
    .notEmpty()
    .escape()
];

// Usage
const { createUserRules, validate } = require('./middleware/validation');

app.post('/api/users', createUserRules, validate, createUser);
```

### SQL Injection Prevention

```javascript
// DON'T: String concatenation
const query = `SELECT * FROM users WHERE email = '${req.body.email}'`; // Vulnerable!

// DO: Parameterized queries
const query = 'SELECT * FROM users WHERE email = ?';
connection.query(query, [req.body.email], (err, results) => {
  // Safe from SQL injection
});

// DO: ORM/Query Builder
const user = await User.findOne({ email: req.body.email }); // Mongoose
const user = await db('users').where('email', req.body.email).first(); // Knex
```

### XSS Protection

```javascript
// Install: npm install xss-clean
const xss = require('xss-clean');

// Apply XSS sanitization
app.use(xss());

// Additional: HTML escaping in templates
const escapeHtml = (unsafe) => {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
};
```

### Environment Variable Security

```javascript
// config/index.js
require('dotenv').config();

const requiredEnvVars = [
  'NODE_ENV',
  'PORT',
  'DATABASE_URL',
  'JWT_SECRET',
  'REDIS_HOST'
];

// Validate required environment variables
requiredEnvVars.forEach((envVar) => {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
});

// Validate JWT_SECRET strength
if (process.env.JWT_SECRET.length < 32) {
  throw new Error('JWT_SECRET must be at least 32 characters');
}

module.exports = {
  env: process.env.NODE_ENV,
  port: parseInt(process.env.PORT, 10),
  database: {
    url: process.env.DATABASE_URL
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '7d'
  },
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT, 10) || 6379
  }
};
```

## Testing with Supertest

### Test Setup

```javascript
// tests/setup.js
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');

let mongoServer;

// Setup before all tests
beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const mongoUri = mongoServer.getUri();

  await mongoose.connect(mongoUri);
});

// Cleanup after each test
afterEach(async () => {
  const collections = mongoose.connection.collections;

  for (const key in collections) {
    await collections[key].deleteMany();
  }
});

// Teardown after all tests
afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});
```

### Integration Testing

```javascript
// tests/integration/users.test.js
const request = require('supertest');
const app = require('../../src/app');
const User = require('../../src/models/User');

describe('User API', () => {
  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: 'Password123'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect('Content-Type', /json/)
        .expect(201);

      expect(response.body).toHaveProperty('user');
      expect(response.body.user.email).toBe(userData.email);
      expect(response.body.user).not.toHaveProperty('password');
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          name: 'Test User',
          password: 'Password123'
        })
        .expect(400);

      expect(response.body).toHaveProperty('errors');
    });

    it('should return 409 for duplicate email', async () => {
      const userData = {
        email: 'duplicate@example.com',
        name: 'Test User',
        password: 'Password123'
      };

      // Create first user
      await User.create(userData);

      // Try to create duplicate
      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(409);

      expect(response.body.message).toMatch(/duplicate/i);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should get user by ID', async () => {
      const user = await User.create({
        email: 'get@example.com',
        name: 'Get User',
        password: 'Password123'
      });

      const response = await request(app)
        .get(`/api/users/${user._id}`)
        .expect(200);

      expect(response.body.user._id).toBe(user._id.toString());
    });

    it('should return 404 for non-existent user', async () => {
      const fakeId = '507f1f77bcf86cd799439011';

      await request(app)
        .get(`/api/users/${fakeId}`)
        .expect(404);
    });
  });

  describe('PUT /api/users/:id', () => {
    it('should update user', async () => {
      const user = await User.create({
        email: 'update@example.com',
        name: 'Update User',
        password: 'Password123'
      });

      const response = await request(app)
        .put(`/api/users/${user._id}`)
        .send({ name: 'Updated Name' })
        .expect(200);

      expect(response.body.user.name).toBe('Updated Name');
    });
  });

  describe('DELETE /api/users/:id', () => {
    it('should delete user', async () => {
      const user = await User.create({
        email: 'delete@example.com',
        name: 'Delete User',
        password: 'Password123'
      });

      await request(app)
        .delete(`/api/users/${user._id}`)
        .expect(204);

      const deletedUser = await User.findById(user._id);
      expect(deletedUser).toBeNull();
    });
  });
});
```

### Authentication Testing

```javascript
// tests/integration/auth.test.js
const request = require('supertest');
const app = require('../../src/app');
const User = require('../../src/models/User');

describe('Authentication', () => {
  let authToken;
  let testUser;

  beforeEach(async () => {
    // Create test user
    testUser = await User.create({
      email: 'auth@example.com',
      name: 'Auth User',
      password: 'Password123'
    });

    // Login to get token
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'auth@example.com',
        password: 'Password123'
      });

    authToken = response.body.token;
  });

  describe('POST /api/auth/login', () => {
    it('should login with valid credentials', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'auth@example.com',
          password: 'Password123'
        })
        .expect(200);

      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('user');
    });

    it('should reject invalid credentials', async () => {
      await request(app)
        .post('/api/auth/login')
        .send({
          email: 'auth@example.com',
          password: 'WrongPassword'
        })
        .expect(401);
    });
  });

  describe('GET /api/auth/me', () => {
    it('should get current user with valid token', async () => {
      const response = await request(app)
        .get('/api/auth/me')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.user.email).toBe('auth@example.com');
    });

    it('should reject request without token', async () => {
      await request(app)
        .get('/api/auth/me')
        .expect(401);
    });

    it('should reject request with invalid token', async () => {
      await request(app)
        .get('/api/auth/me')
        .set('Authorization', 'Bearer invalid-token')
        .expect(401);
    });
  });
});
```

### Test Factories and Fixtures

```javascript
// tests/factories/userFactory.js
const User = require('../../src/models/User');

let userCount = 0;

exports.createUser = async (overrides = {}) => {
  userCount++;

  const defaultData = {
    email: `user${userCount}@example.com`,
    name: `User ${userCount}`,
    password: 'Password123'
  };

  return User.create({ ...defaultData, ...overrides });
};

exports.createUsers = async (count, overrides = {}) => {
  const users = [];
  for (let i = 0; i < count; i++) {
    users.push(await exports.createUser(overrides));
  }
  return users;
};
```

**Usage**:
```javascript
const { createUser, createUsers } = require('../factories/userFactory');

describe('User operations', () => {
  it('should list all users', async () => {
    await createUsers(5);

    const response = await request(app)
      .get('/api/users')
      .expect(200);

    expect(response.body.users).toHaveLength(5);
  });

  it('should create admin user', async () => {
    const admin = await createUser({ role: 'admin' });
    expect(admin.role).toBe('admin');
  });
});
```

### Test Coverage

```javascript
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:unit": "jest tests/unit",
    "test:integration": "jest tests/integration"
  },
  "jest": {
    "testEnvironment": "node",
    "coveragePathIgnorePatterns": ["/node_modules/"],
    "collectCoverageFrom": [
      "src/**/*.js",
      "!src/tests/**"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Production Operations

### Environment Configuration

```javascript
// config/index.js
require('dotenv').config();

const config = {
  // Environment
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT, 10) || 3000,

  // Database
  database: {
    url: process.env.DATABASE_URL,
    poolMin: parseInt(process.env.DB_POOL_MIN, 10) || 2,
    poolMax: parseInt(process.env.DB_POOL_MAX, 10) || 10
  },

  // Redis
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT, 10) || 6379,
    password: process.env.REDIS_PASSWORD
  },

  // JWT
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '30d'
  },

  // CORS
  cors: {
    origins: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000']
  },

  // Rate Limiting
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS, 10) || 900000,
    max: parseInt(process.env.RATE_LIMIT_MAX, 10) || 100
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    file: process.env.LOG_FILE || 'logs/app.log'
  }
};

// Validate required configuration
const requiredConfig = [
  'database.url',
  'jwt.secret'
];

requiredConfig.forEach(key => {
  const value = key.split('.').reduce((obj, k) => obj?.[k], config);
  if (!value) {
    throw new Error(`Missing required configuration: ${key}`);
  }
});

module.exports = config;
```

**.env.example**:
```bash
# Environment
NODE_ENV=production
PORT=3000

# Database
DATABASE_URL=mongodb://localhost:27017/myapp
DB_POOL_MIN=2
DB_POOL_MAX=10

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT
JWT_SECRET=your-super-secret-jwt-key-min-32-chars
JWT_EXPIRES_IN=7d
JWT_REFRESH_EXPIRES_IN=30d

# CORS
ALLOWED_ORIGINS=https://example.com,https://www.example.com

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100

# Logging
LOG_LEVEL=info
LOG_FILE=logs/app.log
```

### Structured Logging

```javascript
// config/logger.js
const winston = require('winston');
const path = require('path');

const logLevels = {
  error: 0,
  warn: 1,
  info: 2,
  http: 3,
  debug: 4
};

const logColors = {
  error: 'red',
  warn: 'yellow',
  info: 'green',
  http: 'magenta',
  debug: 'blue'
};

winston.addColors(logColors);

const format = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json()
);

const transports = [
  // Error logs
  new winston.transports.File({
    filename: path.join('logs', 'error.log'),
    level: 'error',
    maxsize: 5242880, // 5MB
    maxFiles: 5
  }),

  // Combined logs
  new winston.transports.File({
    filename: path.join('logs', 'combined.log'),
    maxsize: 5242880,
    maxFiles: 5
  })
];

// Console transport in development
if (process.env.NODE_ENV !== 'production') {
  transports.push(
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize({ all: true }),
        winston.format.printf(
          (info) => `${info.timestamp} ${info.level}: ${info.message}`
        )
      )
    })
  );
}

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  levels: logLevels,
  format,
  transports
});

module.exports = logger;
```

**Usage**:
```javascript
const logger = require('./config/logger');

logger.info('Server started', { port: 3000 });
logger.error('Database connection failed', { error: err.message });
logger.debug('User data', { userId: user.id, email: user.email });
```

**Request Logging Middleware**:
```javascript
// middleware/requestLogger.js
const logger = require('../config/logger');

module.exports = (req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;

    logger.http('Request completed', {
      method: req.method,
      url: req.url,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userAgent: req.get('user-agent'),
      userId: req.user?.id
    });
  });

  next();
};
```

### Health Check Endpoints

```javascript
// routes/health.js
const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const redis = require('redis');

const redisClient = redis.createClient();

// Basic health check
router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Detailed health check
router.get('/health/detailed', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    services: {}
  };

  // Check MongoDB
  try {
    const mongoState = mongoose.connection.readyState;
    health.services.mongodb = {
      status: mongoState === 1 ? 'connected' : 'disconnected',
      state: mongoState
    };
  } catch (error) {
    health.services.mongodb = {
      status: 'error',
      error: error.message
    };
    health.status = 'degraded';
  }

  // Check Redis
  try {
    await redisClient.ping();
    health.services.redis = {
      status: 'connected'
    };
  } catch (error) {
    health.services.redis = {
      status: 'error',
      error: error.message
    };
    health.status = 'degraded';
  }

  // Memory usage
  const memUsage = process.memoryUsage();
  health.memory = {
    rss: `${Math.round(memUsage.rss / 1024 / 1024)}MB`,
    heapUsed: `${Math.round(memUsage.heapUsed / 1024 / 1024)}MB`,
    heapTotal: `${Math.round(memUsage.heapTotal / 1024 / 1024)}MB`
  };

  const statusCode = health.status === 'ok' ? 200 : 503;
  res.status(statusCode).json(health);
});

// Readiness check (Kubernetes)
router.get('/ready', async (req, res) => {
  try {
    // Check if app can serve requests
    await mongoose.connection.db.admin().ping();
    res.status(200).json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

// Liveness check (Kubernetes)
router.get('/live', (req, res) => {
  res.status(200).json({ status: 'alive' });
});

module.exports = router;
```

### Graceful Shutdown

```javascript
// server.js
const app = require('./app');
const logger = require('./config/logger');
const mongoose = require('./config/database');
const redis = require('./config/redis');

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

// Graceful shutdown function
async function gracefulShutdown(signal) {
  logger.info(`${signal} received, starting graceful shutdown`);

  // Stop accepting new connections
  server.close(async () => {
    logger.info('HTTP server closed');

    try {
      // Close database connections
      await mongoose.connection.close(false);
      logger.info('MongoDB connection closed');

      // Close Redis connection
      await redis.quit();
      logger.info('Redis connection closed');

      // Close any other resources
      // await closeOtherResources();

      logger.info('Graceful shutdown completed');
      process.exit(0);
    } catch (error) {
      logger.error('Error during shutdown', { error: error.message });
      process.exit(1);
    }
  });

  // Force shutdown after timeout
  setTimeout(() => {
    logger.error('Forcing shutdown after timeout');
    process.exit(1);
  }, 30000); // 30 seconds
}

// Handle termination signals
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Handle uncaught errors
process.on('uncaughtException', (error) => {
  logger.error('Uncaught exception', { error: error.message, stack: error.stack });
  gracefulShutdown('uncaughtException');
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled rejection', { reason, promise });
  gracefulShutdown('unhandledRejection');
});

module.exports = server;
```

### PM2 Clustering

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'express-api',
    script: './src/server.js',

    // Clustering
    instances: 'max', // Use all CPU cores
    exec_mode: 'cluster',

    // Environment variables
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 8080
    },

    // Restart policies
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s',
    max_memory_restart: '500M',

    // Graceful shutdown
    kill_timeout: 5000,
    wait_ready: true,
    listen_timeout: 10000,

    // Logging
    error_file: './logs/pm2-error.log',
    out_file: './logs/pm2-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,

    // Monitoring
    instance_var: 'INSTANCE_ID',

    // Watch (development only)
    watch: false
  }],

  // Deploy configuration
  deploy: {
    production: {
      user: 'deploy',
      host: 'production.example.com',
      ref: 'origin/main',
      repo: 'git@github.com:username/repo.git',
      path: '/var/www/production',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production'
    }
  }
};
```

**PM2 Commands**:
```bash
# Start cluster
pm2 start ecosystem.config.js --env production

# Zero-downtime reload
pm2 reload express-api

# Monitor
pm2 monit

# View logs
pm2 logs express-api

# Scale instances
pm2 scale express-api 4

# Stop
pm2 stop express-api

# Restart
pm2 restart express-api

# Delete
pm2 delete express-api

# Save process list
pm2 save

# Startup script
pm2 startup

# Deploy
pm2 deploy production
```

## Development Workflow

### Nodemon Configuration

```json
{
  "watch": ["src"],
  "ext": "js,json",
  "ignore": [
    "src/**/*.test.js",
    "src/**/*.spec.js",
    "node_modules/**/*",
    "logs/**/*"
  ],
  "exec": "node src/server.js",
  "env": {
    "NODE_ENV": "development",
    "PORT": "3000"
  },
  "delay": 1000,
  "verbose": false,
  "restartable": "rs",
  "signal": "SIGTERM"
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "nodemon src/server.js",
    "dev:debug": "nodemon --inspect src/server.js",
    "start": "node src/server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/**/*.js",
    "lint:fix": "eslint src/**/*.js --fix",
    "format": "prettier --write \"src/**/*.js\"",
    "prod": "pm2 start ecosystem.config.js --env production",
    "reload": "pm2 reload express-api",
    "stop": "pm2 stop express-api",
    "logs": "pm2 logs express-api"
  }
}
```

## Decision Trees

### Middleware Selection

```
Need middleware?
├─ Security?
│  ├─ Headers → helmet
│  ├─ CORS → cors
│  ├─ Rate limiting → express-rate-limit
│  └─ Input validation → express-validator
├─ Parsing?
│  ├─ JSON → express.json()
│  ├─ Form data → express.urlencoded()
│  └─ Multipart → multer
├─ Logging?
│  ├─ Development → morgan('dev')
│  └─ Production → winston + morgan('combined')
├─ Compression?
│  └─ Response compression → compression()
└─ Authentication?
   ├─ Session-based → express-session + connect-redis
   └─ Token-based → jsonwebtoken
```

### Error Handling Strategy

```
Error occurred?
├─ Operational error? (Known error)
│  ├─ Validation error → 400 with details
│  ├─ Authentication error → 401
│  ├─ Authorization error → 403
│  ├─ Not found error → 404
│  └─ Conflict error → 409
├─ Programming error? (Bug)
│  ├─ Development → Send full error + stack
│  └─ Production → Log error, send generic message
└─ External service error?
   ├─ Retry → Exponential backoff
   └─ Circuit breaker → Fail fast
```

### Testing Approach

```
What to test?
├─ API endpoints?
│  └─ Integration tests → Supertest
├─ Business logic?
│  └─ Unit tests → Jest
├─ Database operations?
│  └─ Integration tests → MongoMemoryServer
├─ Authentication?
│  └─ Integration tests → Test token flow
└─ Error handling?
   └─ Unit + Integration tests → Test error cases
```

### Deployment Pattern

```
Deployment target?
├─ Local development?
│  └─ Nodemon
├─ Single server?
│  ├─ Small app → node server.js
│  └─ Production → PM2 (single instance)
├─ Multi-core server?
│  └─ PM2 cluster mode
├─ Container?
│  ├─ Single container → Docker + node
│  └─ Orchestrated → Docker + Kubernetes
└─ Serverless?
   └─ AWS Lambda + API Gateway
```

## Common Problems & Solutions

### Problem 1: Port Already in Use

**Symptoms**:
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution**:
```bash
# Find and kill process on port
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev

# Or add cleanup script
{
  "scripts": {
    "predev": "kill-port 3000 || true",
    "dev": "nodemon server.js"
  }
}
```

### Problem 2: Middleware Order Issues

**Symptom**: Routes not working, errors not caught, CORS failures

**Solution**: Follow correct middleware order:
1. Security (helmet, cors)
2. Rate limiting
3. Parsing (json, urlencoded)
4. Compression
5. Logging
6. Custom middleware
7. Routes
8. 404 handler
9. Error handler (last!)

### Problem 3: Unhandled Promise Rejections

**Symptom**: `UnhandledPromiseRejectionWarning`

**Solution**:
```javascript
// Use catchAsync wrapper
const catchAsync = require('./utils/catchAsync');

app.get('/users', catchAsync(async (req, res) => {
  const users = await User.find();
  res.json({ users });
}));

// Or handle at process level
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION!', err);
  server.close(() => process.exit(1));
});
```

### Problem 4: Sessions Not Working in Cluster Mode

**Symptom**: User logged in but subsequent requests show logged out

**Solution**: Use Redis session store
```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const redis = require('redis');

const redisClient = redis.createClient();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}));
```

### Problem 5: Memory Leaks

**Symptoms**: Memory usage grows over time, server crashes

**Solution**:
```bash
# Monitor memory with PM2
pm2 start server.js --max-memory-restart 500M

# Profile with Node
node --inspect server.js
# Then use Chrome DevTools

# Use clinic.js
npm install -g clinic
clinic doctor -- node server.js
```

## Anti-Patterns

### ❌ Don't: Mix Concerns

```javascript
// WRONG: Business logic in routes
app.post('/users', async (req, res) => {
  const user = new User(req.body);
  user.password = await bcrypt.hash(req.body.password, 10);
  await user.save();
  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET);
  res.json({ user, token });
});
```

✅ **Do: Separate Concerns**:
```javascript
// CORRECT: Use controllers and services
app.post('/users',
  validate(createUserRules),
  userController.create
);

// controller
exports.create = catchAsync(async (req, res) => {
  const user = await userService.createUser(req.body);
  const token = authService.generateToken(user);
  res.status(201).json({ user, token });
});
```

### ❌ Don't: Sync Operations

```javascript
// WRONG
const data = fs.readFileSync('./data.json');
```

✅ **Do: Async Operations**:
```javascript
// CORRECT
const data = await fs.promises.readFile('./data.json');
```

### ❌ Don't: Trust User Input

```javascript
// WRONG
app.post('/users', (req, res) => {
  User.create(req.body); // Dangerous!
});
```

✅ **Do: Validate and Sanitize**:
```javascript
// CORRECT
app.post('/users',
  validate(createUserRules),
  userController.create
);
```

## Quick Reference

### Essential Middleware Stack

```javascript
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const app = express();

// Minimal production stack
app.use(helmet());
app.use(cors());
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(compression());
app.use(morgan('combined'));

// Routes
app.use('/api/v1', require('./routes'));

// Error handler
app.use(require('./middleware/errorHandler'));
```

### Essential Commands

```bash
# Development
npm run dev                    # Start with nodemon
npm test                       # Run tests
npm run test:watch             # Watch mode
npm run lint                   # Lint code

# Production
npm start                      # Start production
pm2 start ecosystem.config.js  # Start with PM2
pm2 reload app                 # Zero-downtime reload
pm2 logs app                   # View logs
pm2 monit                      # Monitor

# Testing
npm test                       # All tests
npm run test:unit              # Unit tests
npm run test:integration       # Integration tests
npm run test:coverage          # Coverage report
```

## Related Skills

- **nodejs-backend** - Node.js backend development patterns
- **fastify-production** - Fastify framework (performance-focused alternative)
- **typescript-core** - TypeScript with Express
- **docker-containerization** - Containerized Express deployment
- **systematic-debugging** - Advanced debugging techniques

## Progressive Disclosure

For detailed implementation guides, see:
- [Middleware Patterns](references/middleware-patterns.md) - Advanced middleware composition and patterns
- [Security Hardening](references/security-hardening.md) - Comprehensive security checklist
- [Testing Strategies](references/testing-strategies.md) - Complete testing guide
- [Production Deployment](references/production-deployment.md) - Deployment architectures and strategies

---

**Version**: Express 4.x, PM2 5.x, Node.js 18+
**Last Updated**: December 2025
**License**: MIT
