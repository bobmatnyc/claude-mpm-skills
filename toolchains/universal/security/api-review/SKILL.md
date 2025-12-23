---
name: api-security-review
description: API security checklist for reviewing endpoints before deployment. Use when creating or modifying API routes to ensure proper authentication, authorization, and input validation.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_checklist
  sections:
    - authentication
    - authorization
    - input_validation
    - output_safety
    - logging
    - example_secure_endpoint
    - framework_patterns
    - common_vulnerabilities
---

# API Security Review Skill

## Summary
Comprehensive security checklist for API endpoint development. Ensures proper authentication, authorization, input validation, output safety, and security logging are implemented before deployment.

## When to Use
- Before merging any PR with API changes
- When creating new API endpoints
- When modifying authentication/authorization logic
- During security audits
- Code review of API routes

## Quick Checklist

### Pre-Deployment Security Audit
- [ ] **Authentication**: Route requires valid user identity
- [ ] **Authorization**: Ownership/permission checks implemented
- [ ] **Input Validation**: All inputs validated with schema (Zod/Joi/etc.)
- [ ] **Output Safety**: No sensitive data exposed in responses
- [ ] **Logging**: Security events logged appropriately
- [ ] **Rate Limiting**: Protection against abuse configured
- [ ] **Error Handling**: No system information leaked in errors

---

## Authentication

### Requirements
Every API endpoint must verify the user's identity before processing requests.

### Next.js (App Router) with Clerk
```typescript
import { auth } from '@clerk/nextjs';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  // 1. Authenticate request
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json(
      { error: "Unauthorized" },
      { status: 401 }
    );
  }

  // Continue with authenticated request...
}
```

### Express.js with JWT
```typescript
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

function authenticateToken(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.sendStatus(401);
  }

  jwt.verify(token, process.env.JWT_SECRET!, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

app.get('/api/protected', authenticateToken, (req, res) => {
  // Request is authenticated
});
```

### FastAPI with OAuth2
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/api/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user": current_user.email}
```

### Django REST Framework
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    # request.user is authenticated
    return Response({'user': request.user.email})
```

---

## Authorization

### Resource Ownership Verification

Authentication proves WHO the user is. Authorization proves the user has permission to access the resource.

### Next.js Example
```typescript
import { auth } from '@clerk/nextjs';
import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { eq } from 'drizzle-orm';

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  // 1. Authenticate
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // 2. Fetch resource
  const resource = await db.query.resources.findFirst({
    where: eq(resources.id, params.id)
  });

  if (!resource) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  // 3. Authorize - Check ownership
  if (resource.ownerId !== userId) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  // 4. Return authorized data
  return NextResponse.json(resource);
}
```

### Role-Based Access Control (RBAC)
```typescript
enum Role {
  USER = 'user',
  ADMIN = 'admin',
  MODERATOR = 'moderator'
}

function requireRole(allowedRoles: Role[]) {
  return async (request: Request) => {
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const user = await db.query.users.findFirst({
      where: eq(users.clerkId, userId)
    });

    if (!user || !allowedRoles.includes(user.role)) {
      return NextResponse.json({ error: "Forbidden" }, { status: 403 });
    }

    return null; // Authorized
  };
}

export async function DELETE(request: Request) {
  const authError = await requireRole([Role.ADMIN, Role.MODERATOR])(request);
  if (authError) return authError;

  // User is authorized as admin or moderator
}
```

### Multi-Tenant Data Isolation
```typescript
// CRITICAL: Prevent cross-tenant data leaks

// ❌ WRONG - No tenant check
const orders = await db.query.orders.findMany({
  where: eq(orders.userId, userId)
});

// ✅ CORRECT - Tenant isolation
const user = await db.query.users.findFirst({
  where: eq(users.clerkId, userId)
});

const orders = await db.query.orders.findMany({
  where: and(
    eq(orders.userId, userId),
    eq(orders.tenantId, user.tenantId) // CRITICAL: tenant boundary
  )
});
```

---

## Input Validation

### Zod Schema Validation (TypeScript)
```typescript
import { z } from 'zod';
import { NextResponse } from 'next/server';

const updateUserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email().optional(),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(['user', 'admin', 'moderator']).optional(),
});

export async function PATCH(request: Request) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Parse and validate input
  const body = await request.json();
  const result = updateUserSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json({
      error: "Validation failed",
      details: result.error.issues
    }, { status: 400 });
  }

  // Safe to use validated data
  const validatedData = result.data;
  // ... update logic
}
```

### Pydantic Validation (Python)
```python
from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import HTTPException

class UpdateUser(BaseModel):
    id: str = Field(..., regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    email: EmailStr | None = None
    age: int | None = Field(None, ge=0, le=150)
    role: str | None = Field(None, regex=r'^(user|admin|moderator)$')

    @validator('email')
    def email_must_not_be_disposable(cls, v):
        if v and any(domain in v for domain in ['tempmail.com', '10minutemail.com']):
            raise ValueError('Disposable email addresses not allowed')
        return v

@app.patch("/api/users")
async def update_user(user_data: UpdateUser, current_user: User = Depends(get_current_user)):
    # user_data is validated
    return {"status": "updated"}
```

### SQL Injection Prevention
```typescript
// ❌ NEVER: Raw SQL with string interpolation
const userId = request.params.id;
const query = `SELECT * FROM users WHERE id = '${userId}'`; // VULNERABLE!
db.execute(query);

// ✅ ALWAYS: Use ORM or parameterized queries
import { eq } from 'drizzle-orm';
const user = await db.query.users.findFirst({
  where: eq(users.id, userId)
});

// ✅ OR: Parameterized raw query
const [user] = await db.execute(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);
```

### File Upload Validation
```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif'];

export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get('file') as File;

  if (!file) {
    return NextResponse.json({ error: "No file provided" }, { status: 400 });
  }

  // Validate file size
  if (file.size > MAX_FILE_SIZE) {
    return NextResponse.json({
      error: "File too large. Max 5MB"
    }, { status: 400 });
  }

  // Validate file type
  if (!ALLOWED_TYPES.includes(file.type)) {
    return NextResponse.json({
      error: "Invalid file type. Only JPEG, PNG, GIF allowed"
    }, { status: 400 });
  }

  // Process file...
}
```

---

## Output Safety

### Remove Sensitive Data from Responses
```typescript
// ❌ WRONG - Exposing sensitive fields
const user = await db.query.users.findFirst({
  where: eq(users.id, userId)
});
return NextResponse.json(user); // Includes password hash, internal IDs, etc.

// ✅ CORRECT - Explicitly select safe fields
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
  columns: {
    id: true,
    email: true,
    name: true,
    createdAt: true,
    // Exclude: passwordHash, internalNotes, apiKey, etc.
  }
});
return NextResponse.json(user);

// ✅ BETTER - Use DTOs
interface PublicUserDTO {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

function toPublicUser(user: User): PublicUserDTO {
  return {
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt
  };
}

return NextResponse.json(toPublicUser(user));
```

### Mask PII in Logs
```typescript
function sanitizeForLogging(data: any) {
  const sanitized = { ...data };

  // Mask email
  if (sanitized.email) {
    const [local, domain] = sanitized.email.split('@');
    sanitized.email = `${local.slice(0, 2)}***@${domain}`;
  }

  // Mask SSN
  if (sanitized.ssn) {
    sanitized.ssn = `***-**-${sanitized.ssn.slice(-4)}`;
  }

  // Remove sensitive fields
  delete sanitized.passwordHash;
  delete sanitized.apiKey;

  return sanitized;
}

console.log('User updated:', sanitizeForLogging(user));
```

### Safe Error Messages
```typescript
// ❌ WRONG - Leaking system information
try {
  await db.execute(query);
} catch (error) {
  return NextResponse.json({
    error: error.message, // Might expose SQL, file paths, etc.
    stack: error.stack     // NEVER expose in production
  }, { status: 500 });
}

// ✅ CORRECT - Generic error with logging
try {
  await db.execute(query);
} catch (error) {
  console.error('Database error:', error); // Log full error internally
  return NextResponse.json({
    error: "An error occurred processing your request"
  }, { status: 500 });
}
```

---

## Logging

### Security Event Logging
```typescript
enum SecurityEvent {
  AUTH_FAILURE = 'auth_failure',
  UNAUTHORIZED_ACCESS = 'unauthorized_access',
  PERMISSION_DENIED = 'permission_denied',
  RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded',
  INVALID_INPUT = 'invalid_input'
}

function logSecurityEvent(event: SecurityEvent, details: any) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    event,
    userId: details.userId || 'anonymous',
    ip: details.ip,
    endpoint: details.endpoint,
    details: sanitizeForLogging(details)
  }));
}

// Usage
export async function GET(request: Request) {
  const { userId } = await auth();

  if (!userId) {
    logSecurityEvent(SecurityEvent.AUTH_FAILURE, {
      ip: request.headers.get('x-forwarded-for'),
      endpoint: request.url
    });
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
}
```

### Request Tracing
```typescript
import { v4 as uuidv4 } from 'uuid';

export async function middleware(request: Request) {
  const requestId = uuidv4();

  console.log(JSON.stringify({
    requestId,
    method: request.method,
    url: request.url,
    timestamp: new Date().toISOString()
  }));

  // Pass request ID through headers
  const response = await fetch(request.url, {
    headers: {
      ...request.headers,
      'X-Request-ID': requestId
    }
  });

  return response;
}
```

---

## Example Secure Endpoint

### Complete Next.js API Route
```typescript
import { auth } from '@clerk/nextjs';
import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import { eq, and } from 'drizzle-orm';
import { z } from 'zod';
import { ratelimit } from '@/lib/ratelimit';

// 1. Input validation schema
const updateResourceSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  isPublic: z.boolean().optional()
});

// 2. DTO for safe output
interface ResourceDTO {
  id: string;
  name: string;
  description: string;
  isPublic: boolean;
  createdAt: Date;
}

function toResourceDTO(resource: any): ResourceDTO {
  return {
    id: resource.id,
    name: resource.name,
    description: resource.description,
    isPublic: resource.isPublic,
    createdAt: resource.createdAt
    // Exclude: ownerId, internalNotes, etc.
  };
}

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    // 3. Rate limiting
    const { success } = await ratelimit.limit(request.headers.get('x-forwarded-for') || 'anonymous');
    if (!success) {
      return NextResponse.json({ error: "Too many requests" }, { status: 429 });
    }

    // 4. Authentication
    const { userId } = await auth();
    if (!userId) {
      console.log('Auth failure:', { endpoint: request.url });
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // 5. Input validation
    const body = await request.json();
    const result = updateResourceSchema.safeParse(body);

    if (!result.success) {
      return NextResponse.json({
        error: "Validation failed",
        details: result.error.issues
      }, { status: 400 });
    }

    // 6. Fetch and verify existence
    const resource = await db.query.resources.findFirst({
      where: eq(resources.id, params.id)
    });

    if (!resource) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    // 7. Authorization check
    if (resource.ownerId !== userId) {
      console.log('Permission denied:', { userId, resourceId: params.id });
      return NextResponse.json({ error: "Forbidden" }, { status: 403 });
    }

    // 8. Update resource
    const [updatedResource] = await db.update(resources)
      .set({
        ...result.data,
        updatedAt: new Date()
      })
      .where(eq(resources.id, params.id))
      .returning();

    // 9. Return safe response
    return NextResponse.json(toResourceDTO(updatedResource));

  } catch (error) {
    // 10. Safe error handling
    console.error('Error updating resource:', error);
    return NextResponse.json({
      error: "An error occurred"
    }, { status: 500 });
  }
}
```

---

## Framework Patterns

### Express.js Middleware Pattern
```typescript
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

// Validation middleware factory
function validateSchema(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues
      });
    }
    req.body = result.data;
    next();
  };
}

// Authorization middleware
async function requireOwnership(req: Request, res: Response, next: NextFunction) {
  const resource = await db.resources.findById(req.params.id);

  if (!resource) {
    return res.status(404).json({ error: 'Not found' });
  }

  if (resource.ownerId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  req.resource = resource;
  next();
}

// Usage
const updateSchema = z.object({ name: z.string() });
app.patch('/api/resources/:id',
  authenticate,
  validateSchema(updateSchema),
  requireOwnership,
  async (req, res) => {
    // All checks passed
    const updated = await updateResource(req.resource, req.body);
    res.json(toDTO(updated));
  }
);
```

### FastAPI Dependency Injection
```python
from fastapi import Depends, HTTPException
from typing import Annotated

async def verify_ownership(
    resource_id: str,
    current_user: User = Depends(get_current_user)
):
    resource = await db.resources.get(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Not found")
    if resource.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return resource

@app.patch("/api/resources/{resource_id}")
async def update_resource(
    data: UpdateResourceSchema,
    resource: Resource = Depends(verify_ownership)
):
    # Resource ownership verified
    updated = await resource.update(data.dict())
    return ResourceDTO.from_orm(updated)
```

---

## Common Vulnerabilities

### OWASP Top 10 API Security

#### 1. Broken Object Level Authorization (BOLA)
```typescript
// ❌ VULNERABLE
export async function GET(request: Request) {
  const { userId } = await auth();
  const resourceId = new URL(request.url).searchParams.get('id');

  // Missing ownership check!
  const resource = await db.query.resources.findFirst({
    where: eq(resources.id, resourceId)
  });

  return NextResponse.json(resource);
}

// ✅ FIXED
export async function GET(request: Request) {
  const { userId } = await auth();
  const resourceId = new URL(request.url).searchParams.get('id');

  const resource = await db.query.resources.findFirst({
    where: and(
      eq(resources.id, resourceId),
      eq(resources.ownerId, userId) // Ownership check
    )
  });

  if (!resource) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json(resource);
}
```

#### 2. Mass Assignment
```typescript
// ❌ VULNERABLE - User can set any field
export async function PATCH(request: Request) {
  const body = await request.json();

  // User could send: { role: 'admin', isVerified: true }
  await db.update(users)
    .set(body) // DANGEROUS!
    .where(eq(users.id, userId));
}

// ✅ FIXED - Explicit allowed fields
const allowedFields = z.object({
  name: z.string().optional(),
  bio: z.string().optional()
  // role, isVerified NOT allowed
});

export async function PATCH(request: Request) {
  const body = await request.json();
  const validated = allowedFields.parse(body);

  await db.update(users)
    .set(validated)
    .where(eq(users.id, userId));
}
```

#### 3. Excessive Data Exposure
```typescript
// ❌ VULNERABLE
return NextResponse.json(user); // All fields exposed

// ✅ FIXED
return NextResponse.json({
  id: user.id,
  name: user.name,
  email: user.email
  // passwordHash, resetToken, etc. excluded
});
```

#### 4. Rate Limiting
```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export async function POST(request: Request) {
  const identifier = request.headers.get('x-forwarded-for') || 'anonymous';
  const { success } = await ratelimit.limit(identifier);

  if (!success) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }

  // Process request...
}
```

---

## Summary

### Security Checklist Template
```markdown
## Security Review for [Endpoint Name]

### Authentication
- [ ] User identity verified before processing
- [ ] Invalid tokens rejected with 401
- [ ] Token expiration checked

### Authorization
- [ ] Resource ownership verified
- [ ] Role/permission checks implemented
- [ ] Cross-tenant data isolation enforced

### Input Validation
- [ ] All inputs validated with schema (Zod/Pydantic)
- [ ] File uploads size/type limited
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevention in place

### Output Safety
- [ ] Sensitive fields excluded from responses
- [ ] PII masked in logs
- [ ] Error messages don't leak system info

### Rate Limiting
- [ ] Rate limits configured per endpoint
- [ ] DDoS protection in place

### Logging
- [ ] Failed auth attempts logged
- [ ] Permission denials logged
- [ ] Request IDs for traceability
```

Use this skill during code reviews and before deploying API changes to ensure comprehensive security coverage.
