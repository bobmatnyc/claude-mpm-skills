# Next.js Routing Patterns

Dynamic routes, parallel routes, intercepting routes, route groups, and middleware.

## Route Fundamentals

### File-System Routing

```
app/
├── page.tsx              → /
├── about/page.tsx        → /about
├── blog/
│   ├── page.tsx          → /blog
│   └── [slug]/page.tsx   → /blog/:slug
└── api/
    └── users/route.ts    → /api/users
```

### Dynamic Segments

```typescript
// app/posts/[slug]/page.tsx
type Props = {
  params: Promise<{ slug: string }>;
};

export default async function PostPage({ params }: Props) {
  const { slug } = await params;
  const post = await getPost(slug);
  return <Post post={post} />;
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({ slug: post.slug }));
}
```

### Catch-All Segments

```typescript
// app/docs/[...slug]/page.tsx
// Matches /docs/a, /docs/a/b, /docs/a/b/c, etc.
type Props = {
  params: Promise<{ slug: string[] }>;
};

export default async function DocsPage({ params }: Props) {
  const { slug } = await params;
  // slug = ['a', 'b', 'c'] for /docs/a/b/c
  const path = slug.join('/');
  return <Documentation path={path} />;
}

// Optional catch-all: [[...slug]]
// Also matches /docs (slug = undefined)
```

## Route Groups

### Organizing Without URL Impact

```
app/
├── (marketing)/
│   ├── layout.tsx        # Marketing layout
│   ├── page.tsx          → /
│   └── about/page.tsx    → /about
├── (shop)/
│   ├── layout.tsx        # Shop layout
│   ├── products/page.tsx → /products
│   └── cart/page.tsx     → /cart
└── (auth)/
    ├── layout.tsx        # Auth layout
    ├── login/page.tsx    → /login
    └── signup/page.tsx   → /signup
```

### Multiple Root Layouts

```typescript
// app/(marketing)/layout.tsx
export default function MarketingLayout({ children }) {
  return (
    <html>
      <body>
        <MarketingHeader />
        {children}
        <MarketingFooter />
      </body>
    </html>
  );
}

// app/(shop)/layout.tsx
export default function ShopLayout({ children }) {
  return (
    <html>
      <body>
        <ShopHeader />
        <CartProvider>
          {children}
        </CartProvider>
        <ShopFooter />
      </body>
    </html>
  );
}
```

## Parallel Routes

### Basic Setup

```
app/
├── layout.tsx
├── page.tsx
├── @analytics/
│   └── page.tsx
└── @sidebar/
    ├── page.tsx
    └── default.tsx    # Required fallback
```

```typescript
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  sidebar,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  sidebar: React.ReactNode;
}) {
  return (
    <div className="layout">
      <aside>{sidebar}</aside>
      <main>{children}</main>
      <div className="analytics">{analytics}</div>
    </div>
  );
}
```

### Conditional Rendering

```typescript
// app/@auth/page.tsx
import { auth } from '@/lib/auth';

export default async function AuthSlot() {
  const session = await auth();
  
  if (!session) {
    return <LoginPrompt />;
  }
  
  return <UserMenu user={session.user} />;
}
```

### Default Fallback (Required in Next.js 16)

```typescript
// app/@sidebar/default.tsx
export default function Default() {
  return null; // Or a loading skeleton
}
```

## Intercepting Routes

### Modal Pattern

```
app/
├── feed/
│   └── page.tsx              # Feed page
├── photo/
│   └── [id]/
│       └── page.tsx          # Full photo page
└── @modal/
    ├── default.tsx
    └── (.)photo/
        └── [id]/
            └── page.tsx      # Photo modal
```

```typescript
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from '@/components/modal';

export default async function PhotoModal({ params }) {
  const { id } = await params;
  const photo = await getPhoto(id);
  
  return (
    <Modal>
      <PhotoView photo={photo} />
    </Modal>
  );
}
```

### Interception Conventions

```
(.)  - Same level
(..) - One level up
(..)(..) - Two levels up
(...) - Root level
```

### Modal Component

```typescript
'use client';

import { useRouter } from 'next/navigation';
import { useCallback, useRef, useEffect } from 'react';

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const overlayRef = useRef<HTMLDivElement>(null);
  
  const onDismiss = useCallback(() => {
    router.back();
  }, [router]);
  
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onDismiss();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onDismiss]);
  
  return (
    <div
      ref={overlayRef}
      className="modal-overlay"
      onClick={(e) => {
        if (e.target === overlayRef.current) onDismiss();
      }}
    >
      <div className="modal-content">
        <button onClick={onDismiss} className="modal-close">×</button>
        {children}
      </div>
    </div>
  );
}
```

## Route Handlers

### HTTP Methods

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = searchParams.get('page') ?? '1';
  
  const posts = await getPosts(parseInt(page));
  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const post = await createPost(body);
  return NextResponse.json(post, { status: 201 });
}
```

### Dynamic Route Handlers

```typescript
// app/api/posts/[id]/route.ts
type Context = { params: Promise<{ id: string }> };

export async function GET(request: NextRequest, context: Context) {
  const { id } = await context.params;
  const post = await getPost(id);
  
  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  
  return NextResponse.json(post);
}

export async function PUT(request: NextRequest, context: Context) {
  const { id } = await context.params;
  const body = await request.json();
  const post = await updatePost(id, body);
  return NextResponse.json(post);
}

export async function DELETE(request: NextRequest, context: Context) {
  const { id } = await context.params;
  await deletePost(id);
  return new NextResponse(null, { status: 204 });
}
```

### CORS Headers

```typescript
// app/api/public/route.ts
export async function GET(request: NextRequest) {
  const data = await getData();
  
  return NextResponse.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

export async function OPTIONS() {
  return new NextResponse(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
```

## Middleware (proxy.ts in Next.js 16)

### Basic Middleware

```typescript
// proxy.ts (middleware.ts in Next.js 15)
import { NextRequest, NextResponse } from 'next/server';

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Redirect
  if (pathname === '/old-page') {
    return NextResponse.redirect(new URL('/new-page', request.url));
  }
  
  // Rewrite (internal)
  if (pathname.startsWith('/api/v1')) {
    return NextResponse.rewrite(new URL(pathname.replace('/v1', '/v2'), request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### Authentication Middleware

```typescript
// proxy.ts
import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

const protectedRoutes = ['/dashboard', '/settings', '/profile'];
const authRoutes = ['/login', '/signup'];

export async function proxy(request: NextRequest) {
  const token = await getToken({ req: request });
  const { pathname } = request.nextUrl;
  
  // Redirect authenticated users away from auth pages
  if (token && authRoutes.some(route => pathname.startsWith(route))) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  
  // Protect routes
  if (!token && protectedRoutes.some(route => pathname.startsWith(route))) {
    const url = new URL('/login', request.url);
    url.searchParams.set('callbackUrl', pathname);
    return NextResponse.redirect(url);
  }
  
  return NextResponse.next();
}
```

### Geolocation & Headers

```typescript
export function proxy(request: NextRequest) {
  const country = request.geo?.country ?? 'US';
  const city = request.geo?.city ?? 'Unknown';
  
  const response = NextResponse.next();
  
  // Add custom headers
  response.headers.set('x-country', country);
  response.headers.set('x-city', city);
  
  return response;
}
```

## Navigation

### Link Component

```typescript
import Link from 'next/link';

// Basic
<Link href="/about">About</Link>

// Dynamic
<Link href={`/posts/${post.slug}`}>{post.title}</Link>

// With query params
<Link href={{ pathname: '/search', query: { q: 'next.js' } }}>
  Search
</Link>

// Prefetch (default: true)
<Link href="/heavy-page" prefetch={false}>Heavy Page</Link>

// Replace history (no back)
<Link href="/login" replace>Login</Link>
```

### useRouter

```typescript
'use client';

import { useRouter } from 'next/navigation';

export function NavigationButtons() {
  const router = useRouter();
  
  return (
    <>
      <button onClick={() => router.push('/dashboard')}>Dashboard</button>
      <button onClick={() => router.replace('/home')}>Home (replace)</button>
      <button onClick={() => router.back()}>Back</button>
      <button onClick={() => router.forward()}>Forward</button>
      <button onClick={() => router.refresh()}>Refresh</button>
      <button onClick={() => router.prefetch('/heavy-page')}>Prefetch</button>
    </>
  );
}
```

### usePathname & useSearchParams

```typescript
'use client';

import { usePathname, useSearchParams } from 'next/navigation';

export function CurrentRoute() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  
  const query = searchParams.get('q');
  
  return (
    <div>
      <p>Path: {pathname}</p>
      <p>Search: {query}</p>
    </div>
  );
}
```

## Best Practices

1. **Use route groups** for layout organization without URL impact
2. **Implement default.tsx** for all parallel routes (required in Next.js 16)
3. **Prefer Server Components** for data fetching in pages
4. **Use intercepting routes** for modal patterns
5. **Keep middleware lean** - heavy logic belongs in route handlers
6. **Match middleware carefully** - exclude static assets
7. **Prefetch strategically** - disable for rarely visited pages
