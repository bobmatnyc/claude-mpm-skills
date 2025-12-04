---
name: nodejs-backend-typescript
description: Node.js backend development with TypeScript, Express/Fastify servers, routing, middleware, and database integration. Use when building REST APIs with TypeScript, creating Express/Fastify servers, or implementing microservices architectures.
---

# Node.js Backend Development with TypeScript

---
progressive_disclosure:
  entry_point:
    summary: "TypeScript backend patterns with Express/Fastify, routing, middleware, database integration"
    when_to_use:
      - "When building REST APIs with TypeScript"
      - "When creating Express/Fastify servers"
      - "When needing server-side TypeScript"
      - "When building microservices"
    quick_start:
      - "npm init -y && npm install -D typescript @types/node tsx"
      - "npm install express @types/express zod"
      - "Create tsconfig.json with strict mode"
      - "npm run dev"
  token_estimate:
    entry: 75
    full: 4700
---

## TypeScript Setup

### Essential Configuration

**tsconfig.json** (strict mode recommended):
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "types": ["node"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**package.json scripts**:
```json
{
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "test": "vitest"
  }
}
```

### Development Dependencies
```bash
npm install -D typescript @types/node tsx vitest
npm install -D @types/express  # or @types/node (Fastify has built-in types)
```

## Express Patterns

### Basic Express Server

**src/server.ts**:
```typescript
import express, { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Type-safe request handlers
interface TypedRequest<T> extends Request {
  body: T;
}

// Routes
app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

### Router Pattern

**src/routes/users.ts**:
```typescript
import { Router } from 'express';
import { z } from 'zod';
import { validateRequest } from '../middleware/validation';

const router = Router();

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  age: z.number().int().positive().optional(),
});

router.post(
  '/users',
  validateRequest(createUserSchema),
  async (req, res, next) => {
    try {
      const userData = req.body; // Type-safe after validation
      // Database insert logic
      res.status(201).json({ id: 1, ...userData });
    } catch (error) {
      next(error);
    }
  }
);

export default router;
```

### Middleware Patterns

**src/middleware/validation.ts**:
```typescript
import { Request, Response, NextFunction } from 'express';
import { z, ZodSchema } from 'zod';

export const validateRequest = (schema: ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      } else {
        next(error);
      }
    }
  };
};
```

**src/middleware/auth.ts**:
```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface JwtPayload {
  userId: string;
  email: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}

export const authenticate = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

### Error Handling

**src/middleware/errorHandler.ts**:
```typescript
import { Request, Response, NextFunction } from 'express';

export class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public isOperational = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    });
  }

  console.error('Unexpected error:', err);
  res.status(500).json({
    error: 'Internal server error',
    ...(process.env.NODE_ENV === 'development' && {
      message: err.message,
      stack: err.stack,
    }),
  });
};
```

## Fastify Patterns

### Basic Fastify Server

**src/server.ts**:
```typescript
import Fastify from 'fastify';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import { Type } from '@sinclair/typebox';

const fastify = Fastify({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
  },
}).withTypeProvider<TypeBoxTypeProvider>();

// Type-safe route with schema validation
fastify.route({
  method: 'POST',
  url: '/users',
  schema: {
    body: Type.Object({
      email: Type.String({ format: 'email' }),
      name: Type.String({ minLength: 2 }),
      age: Type.Optional(Type.Integer({ minimum: 0 })),
    }),
    response: {
      201: Type.Object({
        id: Type.Number(),
        email: Type.String(),
        name: Type.String(),
      }),
    },
  },
  handler: async (request, reply) => {
    const { email, name, age } = request.body;
    // Auto-typed and validated
    return reply.status(201).send({ id: 1, email, name });
  },
});

const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: '0.0.0.0' });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
```

### Plugin Pattern

**src/plugins/database.ts**:
```typescript
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

declare module 'fastify' {
  interface FastifyInstance {
    db: ReturnType<typeof drizzle>;
  }
}

const databasePlugin: FastifyPluginAsync = async (fastify) => {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
  });

  const db = drizzle(pool);
  fastify.decorate('db', db);

  fastify.addHook('onClose', async () => {
    await pool.end();
  });
};

export default fp(databasePlugin);
```

### Hooks Pattern

**src/hooks/auth.ts**:
```typescript
import { FastifyRequest, FastifyReply } from 'fastify';
import jwt from 'jsonwebtoken';

declare module 'fastify' {
  interface FastifyRequest {
    user?: {
      userId: string;
      email: string;
    };
  }
}

export const authHook = async (
  request: FastifyRequest,
  reply: FastifyReply
) => {
  const token = request.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return reply.status(401).send({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as {
      userId: string;
      email: string;
    };
    request.user = decoded;
  } catch (error) {
    return reply.status(401).send({ error: 'Invalid token' });
  }
};
```

## Request Validation

### Zod with Express

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  profile: z.object({
    firstName: z.string(),
    lastName: z.string(),
    age: z.number().int().positive(),
  }),
  tags: z.array(z.string()).optional(),
});

type CreateUserInput = z.infer<typeof userSchema>;

router.post('/users', async (req, res) => {
  const result = userSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(400).json({
      error: 'Validation failed',
      details: result.error.format(),
    });
  }

  const user: CreateUserInput = result.data;
  // Type-safe user object
});
```

### TypeBox with Fastify

```typescript
import { Type, Static } from '@sinclair/typebox';

const UserSchema = Type.Object({
  email: Type.String({ format: 'email' }),
  password: Type.String({ minLength: 8 }),
  profile: Type.Object({
    firstName: Type.String(),
    lastName: Type.String(),
    age: Type.Integer({ minimum: 0 }),
  }),
  tags: Type.Optional(Type.Array(Type.String())),
});

type User = Static<typeof UserSchema>;

fastify.post('/users', {
  schema: { body: UserSchema },
  handler: async (request, reply) => {
    const user: User = request.body; // Auto-validated
    return { id: 1, ...user };
  },
});
```

## Authentication

### JWT Authentication

**src/services/auth.ts**:
```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

interface TokenPayload {
  userId: string;
  email: string;
}

export class AuthService {
  private static JWT_SECRET = process.env.JWT_SECRET!;
  private static JWT_EXPIRES_IN = '7d';

  static async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }

  static async comparePassword(
    password: string,
    hash: string
  ): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }

  static generateToken(payload: TokenPayload): string {
    return jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRES_IN,
    });
  }

  static verifyToken(token: string): TokenPayload {
    return jwt.verify(token, this.JWT_SECRET) as TokenPayload;
  }
}
```

### Session-based Auth (Express)

```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({
  url: process.env.REDIS_URL,
});
redisClient.connect();

app.use(
  session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: process.env.NODE_ENV === 'production',
      httpOnly: true,
      maxAge: 1000 * 60 * 60 * 24 * 7, // 7 days
    },
  })
);

declare module 'express-session' {
  interface SessionData {
    userId: string;
  }
}
```

## Database Integration

### Drizzle ORM

**src/db/schema.ts**:
```typescript
import { pgTable, serial, varchar, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 255 }).notNull(),
  passwordHash: varchar('password_hash', { length: 255 }).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
```

**src/db/client.ts**:
```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const db = drizzle(pool, { schema });
```

**src/repositories/userRepository.ts**:
```typescript
import { eq } from 'drizzle-orm';
import { db } from '../db/client';
import { users, NewUser } from '../db/schema';

export class UserRepository {
  static async create(data: NewUser) {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  }

  static async findByEmail(email: string) {
    return db.query.users.findFirst({
      where: eq(users.email, email),
    });
  }

  static async findById(id: number) {
    return db.query.users.findFirst({
      where: eq(users.id, id),
    });
  }

  static async list(limit = 10, offset = 0) {
    return db.query.users.findMany({
      limit,
      offset,
      columns: {
        passwordHash: false, // Exclude sensitive fields
      },
    });
  }
}
```

### Prisma

**prisma/schema.prisma**:
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id           Int      @id @default(autoincrement())
  email        String   @unique
  name         String
  passwordHash String   @map("password_hash")
  createdAt    DateTime @default(now()) @map("created_at")
  posts        Post[]

  @@map("users")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  Int      @map("author_id")
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now()) @map("created_at")

  @@map("posts")
}
```

**src/services/userService.ts**:
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export class UserService {
  static async createUser(data: { email: string; name: string; password: string }) {
    const passwordHash = await AuthService.hashPassword(data.password);

    return prisma.user.create({
      data: {
        email: data.email,
        name: data.name,
        passwordHash,
      },
      select: {
        id: true,
        email: true,
        name: true,
        createdAt: true,
      },
    });
  }

  static async getUserWithPosts(userId: number) {
    return prisma.user.findUnique({
      where: { id: userId },
      include: {
        posts: {
          where: { published: true },
          orderBy: { createdAt: 'desc' },
        },
      },
    });
  }
}
```

## API Design

### REST API Patterns

**Pagination**:
```typescript
import { z } from 'zod';

const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
});

router.get('/users', async (req, res) => {
  const { page, limit } = paginationSchema.parse(req.query);
  const offset = (page - 1) * limit;

  const [users, total] = await Promise.all([
    UserRepository.list(limit, offset),
    UserRepository.count(),
  ]);

  res.json({
    data: users,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  });
});
```

**Filtering and Sorting**:
```typescript
const filterSchema = z.object({
  status: z.enum(['active', 'inactive']).optional(),
  search: z.string().optional(),
  sortBy: z.enum(['createdAt', 'name', 'email']).default('createdAt'),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
});

router.get('/users', async (req, res) => {
  const filters = filterSchema.parse(req.query);

  const users = await db.query.users.findMany({
    where: and(
      filters.status && eq(users.status, filters.status),
      filters.search && ilike(users.name, `%${filters.search}%`)
    ),
    orderBy: [
      filters.sortOrder === 'asc'
        ? asc(users[filters.sortBy])
        : desc(users[filters.sortBy]),
    ],
  });

  res.json({ data: users });
});
```

### Error Response Format

```typescript
interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
  details?: unknown;
  timestamp: string;
  path: string;
}

export const formatError = (
  err: AppError,
  req: Request
): ErrorResponse => ({
  error: err.name,
  message: err.message,
  statusCode: err.statusCode,
  ...(err.details && { details: err.details }),
  timestamp: new Date().toISOString(),
  path: req.path,
});
```

## Environment Configuration

### Type-safe Environment Variables

**src/config/env.ts**:
```typescript
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

export type Env = z.infer<typeof envSchema>;

export const env = envSchema.parse(process.env);
```

**Usage**:
```typescript
import { env } from './config/env';

const port = env.PORT; // Type-safe, validated
```

## Testing

### Vitest Setup

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    setupFiles: ['./src/tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

### Integration Tests with Supertest

**src/tests/users.test.ts**:
```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../server';
import { db } from '../db/client';

describe('User API', () => {
  beforeAll(async () => {
    // Setup test database
    await db.delete(users);
  });

  afterAll(async () => {
    // Cleanup
  });

  it('should create a new user', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123',
      })
      .expect(201);

    expect(response.body).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
    expect(response.body).toHaveProperty('id');
    expect(response.body).not.toHaveProperty('passwordHash');
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        email: 'invalid-email',
        name: 'Test User',
        password: 'password123',
      })
      .expect(400);

    expect(response.body).toHaveProperty('error');
  });
});
```

### Unit Tests

**src/services/auth.test.ts**:
```typescript
import { describe, it, expect } from 'vitest';
import { AuthService } from './auth';

describe('AuthService', () => {
  it('should hash password correctly', async () => {
    const password = 'mySecurePassword123';
    const hash = await AuthService.hashPassword(password);

    expect(hash).not.toBe(password);
    expect(hash.length).toBeGreaterThan(50);
  });

  it('should verify password correctly', async () => {
    const password = 'mySecurePassword123';
    const hash = await AuthService.hashPassword(password);

    const isValid = await AuthService.comparePassword(password, hash);
    expect(isValid).toBe(true);

    const isInvalid = await AuthService.comparePassword('wrongPassword', hash);
    expect(isInvalid).toBe(false);
  });

  it('should generate valid JWT token', () => {
    const token = AuthService.generateToken({
      userId: '123',
      email: 'test@example.com',
    });

    expect(token).toBeTruthy();

    const decoded = AuthService.verifyToken(token);
    expect(decoded).toMatchObject({
      userId: '123',
      email: 'test@example.com',
    });
  });
});
```

## Production Deployment

### Docker Setup

**Dockerfile**:
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY --from=builder /app/dist ./dist

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "dist/server.js"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### PM2 Clustering

**ecosystem.config.js**:
```javascript
module.exports = {
  apps: [{
    name: 'api',
    script: './dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
  }],
};
```

## Best Practices

### Project Structure
```
src/
├── server.ts              # Entry point
├── config/
│   └── env.ts            # Environment config
├── routes/
│   ├── index.ts          # Route aggregator
│   ├── users.ts
│   └── posts.ts
├── middleware/
│   ├── auth.ts
│   ├── validation.ts
│   └── errorHandler.ts
├── services/
│   ├── auth.ts
│   └── user.ts
├── repositories/
│   └── userRepository.ts
├── db/
│   ├── client.ts
│   └── schema.ts
├── types/
│   └── index.ts
└── tests/
    ├── setup.ts
    ├── users.test.ts
    └── auth.test.ts
```

### Key Principles
- **Separation of Concerns**: Routes → Controllers → Services → Repositories
- **Type Safety**: Use TypeScript strict mode, Zod for runtime validation
- **Error Handling**: Centralized error handler, custom error classes
- **Security**: Helmet, rate limiting, input validation, CORS
- **Logging**: Structured logging (pino, winston), request IDs
- **Testing**: Unit tests for services, integration tests for APIs
- **Documentation**: OpenAPI/Swagger for API documentation

### Express vs Fastify

**Use Express when**:
- Large ecosystem of middleware needed
- Team familiarity is priority
- Prototype/MVP development
- Legacy codebase compatibility

**Use Fastify when**:
- Performance is critical (2-3x faster)
- Type safety is important (built-in TypeScript support)
- Schema validation required (JSON Schema built-in)
- Modern async/await patterns preferred
- Plugin architecture needed

### Performance Tips
- Use connection pooling for databases
- Implement caching (Redis, in-memory)
- Enable compression (gzip, brotli)
- Use clustering for CPU-intensive tasks
- Implement rate limiting
- Optimize database queries (indexes, query analysis)
- Use CDN for static assets
- Enable HTTP/2 in production
