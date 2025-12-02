---
name: zod
description: TypeScript-first schema validation library with static type inference for form validation, API validation, and runtime type checking with compile-time types.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  sections:
    - primitives
    - objects_and_arrays
    - type_inference
    - validation_methods
    - schema_composition
    - transformations
    - error_handling
    - async_validation
    - advanced_types
    - integrations
    - best_practices
token_estimates:
  entry: 65
  primitives: 200
  objects_and_arrays: 300
  type_inference: 150
  validation_methods: 250
  schema_composition: 300
  transformations: 400
  error_handling: 250
  async_validation: 200
  advanced_types: 500
  integrations: 1200
  best_practices: 300
  full: 5000
---

# Zod Validation Skill

## Summary
TypeScript-first schema validation library with static type inference. Define schemas once, get runtime validation and compile-time types automatically.

## When to Use
- Form validation with type-safe data
- API request/response validation
- Environment variable validation
- Runtime type checking with TypeScript inference
- tRPC procedure inputs/outputs
- Database schema validation (Drizzle, Prisma)

## Quick Start

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(18),
  role: z.enum(['user', 'admin'])
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validate data
const result = UserSchema.safeParse(data);
if (result.success) {
  const user: User = result.data;
}
```

<!-- SECTION: primitives -->
## Primitive Types

### Basic Types

```typescript
import { z } from 'zod';

// String with validation
const nameSchema = z.string()
  .min(2, "Too short")
  .max(50, "Too long")
  .trim();

const emailSchema = z.string().email();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();
const regexSchema = z.string().regex(/^[A-Z]{3}$/);

// Numbers
const ageSchema = z.number()
  .int("Must be integer")
  .positive()
  .min(0)
  .max(120);

const priceSchema = z.number()
  .positive()
  .multipleOf(0.01); // Currency precision

// Boolean
const isActiveSchema = z.boolean();

// Date
const createdAtSchema = z.date()
  .min(new Date('2020-01-01'))
  .max(new Date());

const dateStringSchema = z.string().datetime(); // ISO 8601
const dateOnlySchema = z.string().date(); // YYYY-MM-DD
```

### Special Types

```typescript
// Literal values
const roleSchema = z.literal('admin');
const statusSchema = z.literal('pending');

// Enums
const ColorEnum = z.enum(['red', 'green', 'blue']);
type Color = z.infer<typeof ColorEnum>; // 'red' | 'green' | 'blue'

const NativeEnum = z.nativeEnum(MyEnum); // For TypeScript enums

// Nullable and Optional
const optionalString = z.string().optional(); // string | undefined
const nullableString = z.string().nullable(); // string | null
const nullishString = z.string().nullish(); // string | null | undefined

// Default values
const countSchema = z.number().default(0);
const settingsSchema = z.object({
  theme: z.string().default('light'),
  notifications: z.boolean().default(true)
});
```

<!-- SECTION: objects_and_arrays -->
## Objects and Arrays

### Object Schemas

```typescript
// Basic object
const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string(),
  age: z.number().optional()
});

// Nested objects
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  country: z.string(),
  zipCode: z.string()
});

const PersonSchema = z.object({
  name: z.string(),
  address: AddressSchema,
  contacts: z.object({
    email: z.string().email(),
    phone: z.string().optional()
  })
});

// Strict vs Passthrough
const strictSchema = z.object({ name: z.string() }).strict();
// Rejects unknown keys

const passthroughSchema = z.object({ name: z.string() }).passthrough();
// Allows unknown keys

const stripSchema = z.object({ name: z.string() }).strip();
// Removes unknown keys (default)
```

### Array Schemas

```typescript
// Simple arrays
const stringArray = z.array(z.string());
const numberArray = z.array(z.number()).min(1).max(10);

// Array of objects
const UsersSchema = z.array(UserSchema);

// Non-empty arrays
const tagSchema = z.array(z.string()).nonempty("At least one tag required");

// Fixed-length arrays (tuples)
const coordinateSchema = z.tuple([z.number(), z.number()]);
type Coordinate = z.infer<typeof coordinateSchema>; // [number, number]

// Tuple with rest
const csvRowSchema = z.tuple([z.string(), z.number()]).rest(z.string());
// [string, number, ...string[]]
```

### Records and Maps

```typescript
// Record (object with dynamic keys)
const userRolesSchema = z.record(
  z.string(), // key type
  z.enum(['admin', 'user', 'guest']) // value type
);
type UserRoles = z.infer<typeof userRolesSchema>;
// { [key: string]: 'admin' | 'user' | 'guest' }

// Map
const configMapSchema = z.map(
  z.string(), // key
  z.number()  // value
);

// Set
const uniqueTagsSchema = z.set(z.string());
```

<!-- SECTION: type_inference -->
## Type Inference

```typescript
import { z } from 'zod';

// Infer output type
const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  age: z.number()
});

type User = z.infer<typeof UserSchema>;
// { id: string; email: string; age: number }

// Infer input type (before transforms)
const TransformSchema = z.object({
  date: z.string().transform(s => new Date(s))
});

type Input = z.input<typeof TransformSchema>;
// { date: string }

type Output = z.output<typeof TransformSchema>;
// { date: Date }

// Using inferred types in functions
function createUser(data: User): void {
  // data is type-safe
}

function validateAndCreate(data: unknown): User | null {
  const result = UserSchema.safeParse(data);
  return result.success ? result.data : null;
}
```

<!-- SECTION: validation_methods -->
## Validation Methods

### Parse vs SafeParse

```typescript
// parse() - Throws on failure
try {
  const user = UserSchema.parse(data);
  // user is type User
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error(error.issues);
  }
}

// safeParse() - Returns result object
const result = UserSchema.safeParse(data);

if (result.success) {
  const user = result.data; // type User
} else {
  const errors = result.error.issues;
  errors.forEach(err => {
    console.log(`${err.path}: ${err.message}`);
  });
}

// parseAsync() - For async refinements
const asyncResult = await UserSchema.parseAsync(data);

// safeParseAsync() - Safe async version
const asyncSafeResult = await UserSchema.safeParseAsync(data);
```

### Partial Validation

```typescript
// Check if data matches schema without throwing
const isValid = UserSchema.safeParse(data).success;

// Custom type guards
function isUser(data: unknown): data is User {
  return UserSchema.safeParse(data).success;
}

if (isUser(unknownData)) {
  // TypeScript knows unknownData is User
  console.log(unknownData.email);
}
```

<!-- SECTION: schema_composition -->
## Schema Composition

### Extending and Merging

```typescript
// Extend (add fields)
const BaseUserSchema = z.object({
  id: z.string(),
  email: z.string()
});

const AdminUserSchema = BaseUserSchema.extend({
  role: z.literal('admin'),
  permissions: z.array(z.string())
});

// Merge (combine schemas)
const NameSchema = z.object({ name: z.string() });
const AgeSchema = z.object({ age: z.number() });

const PersonSchema = NameSchema.merge(AgeSchema);
// { name: string; age: number }

// Pick (select fields)
const UserIdEmail = UserSchema.pick({ id: true, email: true });

// Omit (exclude fields)
const UserWithoutId = UserSchema.omit({ id: true });

// Partial (make all fields optional)
const PartialUser = UserSchema.partial();

// DeepPartial (recursive partial)
const DeepPartialUser = UserSchema.deepPartial();

// Required (make all fields required)
const RequiredUser = UserSchema.required();
```

### Union and Intersection

```typescript
// Union (OR)
const StringOrNumber = z.union([z.string(), z.number()]);
// Shorthand
const StringOrNumberAlt = z.string().or(z.number());

// Discriminated Union (tagged union)
const SuccessResponse = z.object({
  status: z.literal('success'),
  data: z.any()
});

const ErrorResponse = z.object({
  status: z.literal('error'),
  message: z.string()
});

const ApiResponse = z.discriminatedUnion('status', [
  SuccessResponse,
  ErrorResponse
]);

// Intersection (AND)
const User = z.object({ name: z.string() });
const Timestamps = z.object({
  createdAt: z.date(),
  updatedAt: z.date()
});

const UserWithTimestamps = z.intersection(User, Timestamps);
// Shorthand
const UserWithTimestampsAlt = User.and(Timestamps);
```

<!-- SECTION: transformations -->
## Transformations and Refinements

### Transform

```typescript
// Transform data after validation
const StringToNumber = z.string().transform(val => parseInt(val, 10));

const DateSchema = z.string().transform(str => new Date(str));

// Chaining transforms
const TrimmedLowercase = z.string()
  .transform(s => s.trim())
  .transform(s => s.toLowerCase());

// Transform with validation
const PositiveStringNumber = z.string()
  .transform(val => parseInt(val, 10))
  .refine(n => n > 0, "Must be positive");

// Complex transformations
const UserInputSchema = z.object({
  name: z.string().transform(s => s.trim()),
  email: z.string().email().transform(s => s.toLowerCase()),
  birthDate: z.string().transform(s => new Date(s)),
  tags: z.string().transform(s => s.split(',').map(t => t.trim()))
});

type UserInput = z.input<typeof UserInputSchema>;
// { name: string; email: string; birthDate: string; tags: string }

type User = z.output<typeof UserInputSchema>;
// { name: string; email: string; birthDate: Date; tags: string[] }
```

### Refine (Custom Validation)

```typescript
// Simple refinement
const PasswordSchema = z.string()
  .min(8)
  .refine(
    val => /[A-Z]/.test(val),
    "Must contain uppercase letter"
  )
  .refine(
    val => /[0-9]/.test(val),
    "Must contain number"
  );

// Refinement with custom error
const UniqueEmailSchema = z.string().email().refine(
  async (email) => {
    const exists = await checkEmailExists(email);
    return !exists;
  },
  { message: "Email already taken" }
);

// Object-level refinement
const PasswordMatchSchema = z.object({
  password: z.string(),
  confirmPassword: z.string()
}).refine(
  data => data.password === data.confirmPassword,
  {
    message: "Passwords don't match",
    path: ["confirmPassword"] // Error location
  }
);

// Multiple field validation
const DateRangeSchema = z.object({
  startDate: z.date(),
  endDate: z.date()
}).refine(
  data => data.endDate > data.startDate,
  {
    message: "End date must be after start date",
    path: ["endDate"]
  }
);
```

### SuperRefine (Advanced)

```typescript
// Access to Zod context for complex validation
const ComplexSchema = z.object({
  type: z.enum(['email', 'phone']),
  value: z.string()
}).superRefine((data, ctx) => {
  if (data.type === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.value)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Invalid email format",
        path: ["value"]
      });
    }
  } else if (data.type === 'phone') {
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    if (!phoneRegex.test(data.value)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Invalid phone format",
        path: ["value"]
      });
    }
  }
});

// Multiple issues
const RegistrationSchema = z.object({
  username: z.string(),
  email: z.string(),
  age: z.number()
}).superRefine(async (data, ctx) => {
  // Check username availability
  if (await usernameTaken(data.username)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Username taken",
      path: ["username"]
    });
  }

  // Check email availability
  if (await emailTaken(data.email)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Email already registered",
      path: ["email"]
    });
  }

  // Age restriction
  if (data.age < 18) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Must be 18 or older",
      path: ["age"]
    });
  }
});
```

<!-- SECTION: error_handling -->
## Error Handling

### Custom Error Messages

```typescript
// Field-level messages
const UserSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  age: z.number({
    required_error: "Age is required",
    invalid_type_error: "Age must be a number"
  }).min(18, { message: "Must be 18 or older" })
});

// Global error map
import { z } from 'zod';

const customErrorMap: z.ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === "string") {
      return { message: "This field must be text" };
    }
  }
  if (issue.code === z.ZodIssueCode.too_small) {
    if (issue.type === "string") {
      return { message: `Minimum ${issue.minimum} characters required` };
    }
  }
  return { message: ctx.defaultError };
};

z.setErrorMap(customErrorMap);
```

### Processing Errors

```typescript
// Flatten errors for forms
const result = UserSchema.safeParse(data);

if (!result.success) {
  const flatErrors = result.error.flatten();

  console.log(flatErrors.formErrors); // Top-level errors
  console.log(flatErrors.fieldErrors);
  // { email: ["Invalid email"], age: ["Must be 18+"] }
}

// Format for API response
function formatZodError(error: z.ZodError) {
  return error.issues.map(issue => ({
    field: issue.path.join('.'),
    message: issue.message
  }));
}

// Example usage
const result = UserSchema.safeParse(data);
if (!result.success) {
  return res.status(400).json({
    errors: formatZodError(result.error)
  });
}
```

<!-- SECTION: async_validation -->
## Async Validation

```typescript
import { z } from 'zod';

// Async refinement
const UsernameSchema = z.string().refine(
  async (username) => {
    const available = await checkUsernameAvailable(username);
    return available;
  },
  { message: "Username already taken" }
);

// Must use parseAsync or safeParseAsync
const result = await UsernameSchema.safeParseAsync("john_doe");

// Complex async validation
const RegistrationSchema = z.object({
  username: z.string().refine(
    async (val) => !(await usernameTaken(val)),
    "Username taken"
  ),
  email: z.string().email().refine(
    async (val) => !(await emailTaken(val)),
    "Email already registered"
  ),
  inviteCode: z.string().refine(
    async (code) => await validateInviteCode(code),
    "Invalid invite code"
  )
});

// Validate
const userData = await RegistrationSchema.parseAsync(input);

// With error handling
const result = await RegistrationSchema.safeParseAsync(input);
if (!result.success) {
  // Handle validation errors
}
```

<!-- SECTION: advanced_types -->
## Advanced Types

### Recursive Types

```typescript
// Self-referential schemas
type Category = {
  name: string;
  subcategories: Category[];
};

const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema)
  })
);

// Tree structure
type TreeNode = {
  value: number;
  left?: TreeNode;
  right?: TreeNode;
};

const TreeNodeSchema: z.ZodType<TreeNode> = z.lazy(() =>
  z.object({
    value: z.number(),
    left: TreeNodeSchema.optional(),
    right: TreeNodeSchema.optional()
  })
);
```

### Discriminated Unions

```typescript
// Type-safe union based on discriminator field
const Circle = z.object({
  kind: z.literal('circle'),
  radius: z.number()
});

const Rectangle = z.object({
  kind: z.literal('rectangle'),
  width: z.number(),
  height: z.number()
});

const Triangle = z.object({
  kind: z.literal('triangle'),
  base: z.number(),
  height: z.number()
});

const Shape = z.discriminatedUnion('kind', [
  Circle,
  Rectangle,
  Triangle
]);

type Shape = z.infer<typeof Shape>;

// TypeScript can narrow based on discriminator
function calculateArea(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    case 'triangle':
      return (shape.base * shape.height) / 2;
  }
}
```

### Preprocess

```typescript
// Transform before validation
const NumberFromString = z.preprocess(
  (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
  z.number()
);

// Clean data before validation
const TrimmedString = z.preprocess(
  (val) => (typeof val === 'string' ? val.trim() : val),
  z.string()
);

// Parse JSON strings
const JsonSchema = z.preprocess(
  (val) => (typeof val === 'string' ? JSON.parse(val) : val),
  z.object({
    name: z.string(),
    age: z.number()
  })
);

// Form data preprocessing
const FormDataSchema = z.preprocess(
  (data) => {
    // Convert FormData to object
    if (data instanceof FormData) {
      return Object.fromEntries(data.entries());
    }
    return data;
  },
  z.object({
    name: z.string(),
    email: z.string().email()
  })
);
```

### Branded Types

```typescript
// Create nominal types
const UserId = z.string().uuid().brand<'UserId'>();
type UserId = z.infer<typeof UserId>;

const Email = z.string().email().brand<'Email'>();
type Email = z.infer<typeof Email>;

// Prevents mixing similar types
function getUserById(id: UserId) { /* ... */ }
function sendEmail(to: Email) { /* ... */ }

const userId = UserId.parse('123e4567-e89b-12d3-a456-426614174000');
const email = Email.parse('user@example.com');

getUserById(userId); // ✓
getUserById(email);  // ✗ Type error
```

<!-- SECTION: integrations -->
## Integrations

### React Hook Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const FormSchema = z.object({
  username: z.string().min(3, "Minimum 3 characters"),
  email: z.string().email("Invalid email"),
  age: z.number().min(18, "Must be 18+")
});

type FormData = z.infer<typeof FormSchema>;

function MyForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormData>({
    resolver: zodResolver(FormSchema)
  });

  const onSubmit = (data: FormData) => {
    // data is validated and typed
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('username')} />
      {errors.username && <span>{errors.username.message}</span>}

      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

### tRPC

```typescript
import { z } from 'zod';
import { initTRPC } from '@trpc/server';

const t = initTRPC.create();

const router = t.router;
const publicProcedure = t.procedure;

// Input/output validation
const appRouter = router({
  userById: publicProcedure
    .input(z.object({
      id: z.string().uuid()
    }))
    .output(z.object({
      id: z.string().uuid(),
      name: z.string(),
      email: z.string().email()
    }))
    .query(async ({ input }) => {
      const user = await db.user.findUnique({
        where: { id: input.id }
      });
      return user; // Type-checked against output schema
    }),

  createUser: publicProcedure
    .input(z.object({
      name: z.string().min(2),
      email: z.string().email(),
      age: z.number().min(18)
    }))
    .mutation(async ({ input }) => {
      return await db.user.create({ data: input });
    })
});

export type AppRouter = typeof appRouter;
```

### Next.js API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  age: z.number().min(18).optional()
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = CreateUserSchema.parse(body);

    // validatedData is typed and validated
    const user = await createUser(validatedData);

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { errors: error.flatten().fieldErrors },
        { status: 400 }
      );
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Query parameter validation
const SearchParamsSchema = z.object({
  page: z.string().transform(Number).pipe(z.number().min(1)).default('1'),
  limit: z.string().transform(Number).pipe(z.number().max(100)).default('10'),
  sort: z.enum(['asc', 'desc']).default('asc')
});

export async function GET(request: NextRequest) {
  const searchParams = Object.fromEntries(
    request.nextUrl.searchParams.entries()
  );

  const params = SearchParamsSchema.parse(searchParams);
  // params is { page: number, limit: number, sort: 'asc' | 'desc' }

  const users = await getUsers(params);
  return NextResponse.json(users);
}
```

### Express Middleware

```typescript
import express from 'express';
import { z } from 'zod';

// Validation middleware
const validate = (schema: z.ZodSchema) => {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          errors: error.flatten().fieldErrors
        });
      }
      next(error);
    }
  };
};

const CreateUserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  age: z.number().min(18)
});

app.post('/users', validate(CreateUserSchema), async (req, res) => {
  // req.body is validated (not typed in Express)
  const user = await createUser(req.body);
  res.json(user);
});

// Validate params, query, body
const validateRequest = (schema: {
  params?: z.ZodSchema;
  query?: z.ZodSchema;
  body?: z.ZodSchema;
}) => {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
      if (schema.params) {
        req.params = schema.params.parse(req.params);
      }
      if (schema.query) {
        req.query = schema.query.parse(req.query);
      }
      if (schema.body) {
        req.body = schema.body.parse(req.body);
      }
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ errors: error.issues });
      }
      next(error);
    }
  };
};

app.get(
  '/users/:id',
  validateRequest({
    params: z.object({ id: z.string().uuid() }),
    query: z.object({ include: z.string().optional() })
  }),
  async (req, res) => {
    // Validated params and query
  }
);
```

### Drizzle ORM

```typescript
import { z } from 'zod';
import { pgTable, serial, text, integer } from 'drizzle-orm/pg-core';
import { createInsertSchema, createSelectSchema } from 'drizzle-zod';

// Define table
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  age: integer('age')
});

// Auto-generate schemas
export const insertUserSchema = createInsertSchema(users);
export const selectUserSchema = createSelectSchema(users);

// Customize validation
export const customInsertUserSchema = createInsertSchema(users, {
  email: z.string().email(),
  age: z.number().min(18).optional()
});

// Use in application
type NewUser = z.infer<typeof insertUserSchema>;
type User = z.infer<typeof selectUserSchema>;

function createUser(data: unknown) {
  const validatedData = insertUserSchema.parse(data);
  return db.insert(users).values(validatedData);
}
```

### Environment Variables

```typescript
// env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(32),
  PORT: z.string().transform(Number).pipe(z.number().min(1024)),
  REDIS_HOST: z.string().default('localhost'),
  REDIS_PORT: z.string().transform(Number).default('6379'),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info')
});

// Validate on startup
export const env = envSchema.parse(process.env);

// Type-safe environment variables
export type Env = z.infer<typeof envSchema>;

// Usage
console.log(`Server running on port ${env.PORT}`);
// env.PORT is number, not string
```

<!-- SECTION: best_practices -->
## Best Practices

### Schema Organization

```typescript
// schemas/user.schema.ts
import { z } from 'zod';

// Reusable primitives
export const emailSchema = z.string().email();
export const uuidSchema = z.string().uuid();
export const passwordSchema = z.string()
  .min(8)
  .regex(/[A-Z]/, "Must contain uppercase")
  .regex(/[0-9]/, "Must contain number");

// Base schemas
export const baseUserSchema = z.object({
  id: uuidSchema,
  email: emailSchema,
  name: z.string().min(2)
});

// Extended schemas
export const createUserSchema = baseUserSchema.omit({ id: true }).extend({
  password: passwordSchema,
  confirmPassword: z.string()
}).refine(
  data => data.password === data.confirmPassword,
  { message: "Passwords must match", path: ["confirmPassword"] }
);

export const updateUserSchema = baseUserSchema.partial().omit({ id: true });

// Export types
export type User = z.infer<typeof baseUserSchema>;
export type CreateUser = z.infer<typeof createUserSchema>;
export type UpdateUser = z.infer<typeof updateUserSchema>;
```

### Performance Optimization

```typescript
// Cache parsed schemas
const userSchemaCache = new Map<string, z.ZodSchema>();

function getCachedSchema(key: string, factory: () => z.ZodSchema) {
  if (!userSchemaCache.has(key)) {
    userSchemaCache.set(key, factory());
  }
  return userSchemaCache.get(key)!;
}

// Lazy validation for large objects
const lazyUserSchema = z.lazy(() => z.object({
  // Only validated when accessed
  profile: complexProfileSchema,
  settings: complexSettingsSchema
}));

// Streaming validation for arrays
async function validateLargeArray(items: unknown[]) {
  const errors: z.ZodError[] = [];

  for (const item of items) {
    const result = ItemSchema.safeParse(item);
    if (!result.success) {
      errors.push(result.error);
    }
  }

  return errors;
}
```

### Testing Schemas

```typescript
import { describe, it, expect } from 'vitest';

describe('UserSchema', () => {
  it('validates correct user data', () => {
    const validUser = {
      email: 'user@example.com',
      name: 'John Doe',
      age: 25
    };

    expect(() => UserSchema.parse(validUser)).not.toThrow();
  });

  it('rejects invalid email', () => {
    const invalidUser = {
      email: 'not-an-email',
      name: 'John',
      age: 25
    };

    const result = UserSchema.safeParse(invalidUser);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].path).toEqual(['email']);
    }
  });

  it('applies transforms correctly', () => {
    const input = {
      name: '  JOHN DOE  ',
      email: 'USER@EXAMPLE.COM'
    };

    const result = UserSchema.parse(input);
    expect(result.name).toBe('john doe');
    expect(result.email).toBe('user@example.com');
  });
});
```

### Common Patterns

```typescript
// Conditional validation
const ConditionalSchema = z.object({
  type: z.enum(['personal', 'business']),
  data: z.any()
}).transform((val) => {
  if (val.type === 'personal') {
    return {
      type: val.type,
      data: PersonalDataSchema.parse(val.data)
    };
  } else {
    return {
      type: val.type,
      data: BusinessDataSchema.parse(val.data)
    };
  }
});

// Pagination schema
export const paginationSchema = z.object({
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(100).default(20),
  sort: z.string().optional(),
  order: z.enum(['asc', 'desc']).default('asc')
});

// Filter schema
export const filterSchema = z.object({
  search: z.string().optional(),
  status: z.enum(['active', 'inactive', 'pending']).optional(),
  dateFrom: z.string().datetime().optional(),
  dateTo: z.string().datetime().optional()
});

// API response wrapper
export const apiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema.optional(),
    error: z.string().optional(),
    timestamp: z.string().datetime()
  });

const userResponseSchema = apiResponseSchema(UserSchema);
```

### Migration from Yup/Joi

```typescript
// Yup -> Zod
// Yup
const yupSchema = yup.object({
  email: yup.string().email().required(),
  age: yup.number().min(18).required()
});

// Zod equivalent
const zodSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18)
});

// Joi -> Zod
// Joi
const joiSchema = Joi.object({
  email: Joi.string().email().required(),
  age: Joi.number().min(18).required()
});

// Zod equivalent (same as above)
const zodSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18)
});

// Key differences:
// 1. Zod fields are required by default
// 2. Zod has first-class TypeScript integration
// 3. Zod schemas are immutable
// 4. Zod has better tree-shaking
```

## Additional Resources

- [Zod Documentation](https://zod.dev)
- [Zod GitHub](https://github.com/colinhacks/zod)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [tRPC + Zod](https://trpc.io/docs/server/validators)
- [React Hook Form + Zod](https://react-hook-form.com/get-started#SchemaValidation)
