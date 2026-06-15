# Type-Safe Server Actions

Complete patterns for Server Actions with validation, middleware, and optimistic updates.

## next-safe-action Setup

### Installation

```bash
npm install next-safe-action zod
```

### Action Client Configuration

```typescript
// lib/safe-action.ts
import { createSafeActionClient } from 'next-safe-action';

export const actionClient = createSafeActionClient({
  // Global error handler
  handleServerError(e) {
    console.error('Action error:', e.message);
    return 'Something went wrong';
  },
});

// With authentication middleware
export const authActionClient = actionClient.use(async ({ next }) => {
  const session = await auth();
  
  if (!session?.user) {
    throw new Error('Unauthorized');
  }
  
  return next({ ctx: { session, userId: session.user.id } });
});

// With rate limiting
export const rateLimitedClient = authActionClient.use(async ({ next, ctx }) => {
  const { success } = await rateLimit.check(ctx.userId);
  
  if (!success) {
    throw new Error('Rate limit exceeded');
  }
  
  return next({ ctx });
});
```

## Action Definitions

### Basic Action

```typescript
// actions/create-post.ts
'use server';

import { z } from 'zod';
import { authActionClient } from '@/lib/safe-action';
import { revalidatePath } from 'next/cache';

const schema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10).max(10000),
  published: z.boolean().default(false),
});

export const createPost = authActionClient
  .schema(schema)
  .action(async ({ parsedInput, ctx }) => {
    const post = await db.posts.create({
      data: {
        ...parsedInput,
        authorId: ctx.userId,
      },
    });
    
    revalidatePath('/posts');
    return { post };
  });
```

### Action with Bind Args

```typescript
// Partial application for dynamic params
const updatePostSchema = z.object({
  title: z.string().min(1),
  content: z.string(),
});

export const updatePost = authActionClient
  .schema(updatePostSchema)
  .bindArgsSchemas<[postId: z.ZodString]>([z.string().uuid()])
  .action(async ({ parsedInput, bindArgsParsedInputs: [postId], ctx }) => {
    // Verify ownership
    const post = await db.posts.findUnique({ where: { id: postId } });
    if (post?.authorId !== ctx.userId) {
      throw new Error('Forbidden');
    }
    
    return db.posts.update({
      where: { id: postId },
      data: parsedInput,
    });
  });

// Usage with bound postId
const boundAction = updatePost.bind(null, postId);
```

### File Upload Action

```typescript
const uploadSchema = z.object({
  file: z.instanceof(File).refine(
    (file) => file.size <= 5 * 1024 * 1024,
    'File must be less than 5MB'
  ),
  folder: z.string().optional(),
});

export const uploadFile = authActionClient
  .schema(uploadSchema)
  .action(async ({ parsedInput, ctx }) => {
    const { file, folder } = parsedInput;
    
    const buffer = await file.arrayBuffer();
    const key = `${folder ?? 'uploads'}/${ctx.userId}/${file.name}`;
    
    await s3.putObject({
      Bucket: process.env.S3_BUCKET,
      Key: key,
      Body: Buffer.from(buffer),
      ContentType: file.type,
    });
    
    return { url: `https://cdn.example.com/${key}` };
  });
```

## Client Integration

### useAction Hook

```typescript
'use client';

import { useAction } from 'next-safe-action/hooks';
import { createPost } from '@/actions/create-post';

export function CreatePostForm() {
  const { execute, result, status, reset } = useAction(createPost);
  
  const handleSubmit = async (formData: FormData) => {
    await execute({
      title: formData.get('title') as string,
      content: formData.get('content') as string,
      published: formData.get('published') === 'on',
    });
  };
  
  return (
    <form action={handleSubmit}>
      <input name="title" required />
      <textarea name="content" required />
      <label>
        <input name="published" type="checkbox" />
        Publish immediately
      </label>
      
      <button type="submit" disabled={status === 'executing'}>
        {status === 'executing' ? 'Creating...' : 'Create Post'}
      </button>
      
      {result.validationErrors && (
        <ul className="errors">
          {Object.entries(result.validationErrors).map(([field, errors]) => (
            <li key={field}>{field}: {errors?.join(', ')}</li>
          ))}
        </ul>
      )}
      
      {result.serverError && (
        <p className="error">{result.serverError}</p>
      )}
      
      {result.data?.post && (
        <p className="success">Post created: {result.data.post.title}</p>
      )}
    </form>
  );
}
```

### useOptimisticAction Hook

```typescript
'use client';

import { useOptimisticAction } from 'next-safe-action/hooks';
import { toggleLike } from '@/actions/toggle-like';

export function LikeButton({ postId, initialLiked, initialCount }) {
  const { execute, optimisticState } = useOptimisticAction(toggleLike, {
    currentState: { liked: initialLiked, count: initialCount },
    updateFn: (state, input) => ({
      liked: !state.liked,
      count: state.liked ? state.count - 1 : state.count + 1,
    }),
  });
  
  return (
    <button onClick={() => execute({ postId })}>
      {optimisticState.liked ? '❤️' : '🤍'} {optimisticState.count}
    </button>
  );
}
```

### Form with React Hook Form

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAction } from 'next-safe-action/hooks';
import { createPost, createPostSchema } from '@/actions/create-post';

type FormData = z.infer<typeof createPostSchema>;

export function PostForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(createPostSchema),
  });
  
  const { execute, status } = useAction(createPost, {
    onSuccess: () => {
      // Handle success
    },
    onError: (error) => {
      // Handle error
    },
  });
  
  return (
    <form onSubmit={handleSubmit((data) => execute(data))}>
      <input {...register('title')} />
      {errors.title && <span>{errors.title.message}</span>}
      
      <textarea {...register('content')} />
      {errors.content && <span>{errors.content.message}</span>}
      
      <button type="submit" disabled={status === 'executing'}>
        Submit
      </button>
    </form>
  );
}
```

## Native Server Actions (Without Library)

### Basic Pattern

```typescript
// actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContact(prevState: any, formData: FormData) {
  const result = schema.safeParse({
    email: formData.get('email'),
    message: formData.get('message'),
  });
  
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
      message: 'Validation failed',
    };
  }
  
  try {
    await sendEmail(result.data);
    revalidatePath('/contact');
    return { message: 'Message sent successfully' };
  } catch (error) {
    return { message: 'Failed to send message' };
  }
}
```

### With useActionState

```typescript
'use client';

import { useActionState } from 'react';
import { submitContact } from './actions';

export function ContactForm() {
  const [state, action, pending] = useActionState(submitContact, {});
  
  return (
    <form action={action}>
      <input name="email" type="email" disabled={pending} />
      {state.errors?.email && <span>{state.errors.email}</span>}
      
      <textarea name="message" disabled={pending} />
      {state.errors?.message && <span>{state.errors.message}</span>}
      
      <button type="submit" disabled={pending}>
        {pending ? 'Sending...' : 'Send'}
      </button>
      
      {state.message && <p>{state.message}</p>}
    </form>
  );
}
```

## Error Handling Patterns

### Typed Error Responses

```typescript
type ActionResult<T> = 
  | { success: true; data: T }
  | { success: false; error: string; code: string };

export const createUser = authActionClient
  .schema(userSchema)
  .action(async ({ parsedInput }): Promise<ActionResult<User>> => {
    try {
      const user = await db.users.create({ data: parsedInput });
      return { success: true, data: user };
    } catch (error) {
      if (error.code === 'P2002') {
        return { 
          success: false, 
          error: 'Email already exists', 
          code: 'DUPLICATE_EMAIL' 
        };
      }
      throw error; // Re-throw unexpected errors
    }
  });
```

### Global Error Boundary

```typescript
// lib/safe-action.ts
export const actionClient = createSafeActionClient({
  handleServerError(e) {
    // Log to monitoring service
    Sentry.captureException(e);
    
    // Return user-friendly message
    if (e instanceof AuthError) {
      return 'Please sign in to continue';
    }
    if (e instanceof RateLimitError) {
      return 'Too many requests. Please wait a moment.';
    }
    return 'An unexpected error occurred';
  },
});
```

## Testing Server Actions

```typescript
// __tests__/actions/create-post.test.ts
import { createPost } from '@/actions/create-post';

// Mock auth
jest.mock('@/lib/auth', () => ({
  auth: jest.fn(() => Promise.resolve({ user: { id: 'user-1' } })),
}));

describe('createPost', () => {
  it('creates a post with valid input', async () => {
    const result = await createPost({
      title: 'Test Post',
      content: 'This is test content that is long enough.',
      published: true,
    });
    
    expect(result.data?.post).toBeDefined();
    expect(result.data?.post.title).toBe('Test Post');
  });
  
  it('returns validation errors for invalid input', async () => {
    const result = await createPost({
      title: '',
      content: 'short',
      published: false,
    });
    
    expect(result.validationErrors).toBeDefined();
    expect(result.validationErrors?.title).toBeDefined();
  });
});
```

## Best Practices

1. **Always validate input** - Use Zod schemas for all actions
2. **Type the return value** - Define explicit return types
3. **Handle errors gracefully** - Return structured errors, don't expose internals
4. **Revalidate appropriately** - Use revalidatePath/revalidateTag after mutations
5. **Use middleware** - Extract auth, rate limiting, logging into reusable middleware
6. **Prefer next-safe-action** - Better DX than raw Server Actions for complex apps
7. **Test actions** - Unit test business logic, integration test with database
