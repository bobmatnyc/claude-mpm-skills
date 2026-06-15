# Authentication in Next.js

Auth.js (NextAuth.js v5) integration, protected routes, and session handling.

## Auth.js Setup

### Installation

```bash
npm install next-auth@beta
```

### Configuration

```typescript
// auth.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(db),
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
    Google({
      clientId: process.env.GOOGLE_ID,
      clientSecret: process.env.GOOGLE_SECRET,
    }),
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      authorize: async (credentials) => {
        const user = await db.users.findUnique({
          where: { email: credentials.email as string },
        });
        
        if (!user || !user.password) return null;
        
        const valid = await bcrypt.compare(
          credentials.password as string,
          user.password
        );
        
        if (!valid) return null;
        
        return { id: user.id, email: user.email, name: user.name };
      },
    }),
  ],
  session: { strategy: 'jwt' },
  pages: {
    signIn: '/login',
    error: '/auth/error',
  },
  callbacks: {
    authorized: async ({ auth }) => {
      return !!auth;
    },
    jwt: async ({ token, user }) => {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    session: async ({ session, token }) => {
      if (token) {
        session.user.id = token.id as string;
      }
      return session;
    },
  },
});
```

### Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';

export const { GET, POST } = handlers;
```

## Session Access

### Server Components

```typescript
// app/dashboard/page.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();
  
  if (!session) {
    redirect('/login');
  }
  
  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### Server Actions

```typescript
// actions/profile.ts
'use server';

import { auth } from '@/auth';

export async function updateProfile(formData: FormData) {
  const session = await auth();
  
  if (!session) {
    throw new Error('Unauthorized');
  }
  
  await db.users.update({
    where: { id: session.user.id },
    data: {
      name: formData.get('name') as string,
    },
  });
}
```

### Client Components

```typescript
'use client';

import { useSession } from 'next-auth/react';

export function UserMenu() {
  const { data: session, status } = useSession();
  
  if (status === 'loading') {
    return <Skeleton />;
  }
  
  if (!session) {
    return <LoginButton />;
  }
  
  return (
    <div>
      <img src={session.user.image} alt={session.user.name} />
      <span>{session.user.name}</span>
      <SignOutButton />
    </div>
  );
}
```

### Session Provider

```typescript
// app/providers.tsx
'use client';

import { SessionProvider } from 'next-auth/react';

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Protected Routes

### Middleware Protection

```typescript
// proxy.ts (middleware.ts in Next.js 15)
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isAuthPage = req.nextUrl.pathname.startsWith('/login');
  const isProtected = req.nextUrl.pathname.startsWith('/dashboard');
  
  if (isAuthPage && isLoggedIn) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }
  
  if (isProtected && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
  
  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Layout-Level Protection

```typescript
// app/(protected)/layout.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  
  if (!session) {
    redirect('/login');
  }
  
  return <>{children}</>;
}
```

### Component-Level Protection

```typescript
// components/protected.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export async function Protected({ children }: { children: React.ReactNode }) {
  const session = await auth();
  
  if (!session) {
    redirect('/login');
  }
  
  return <>{children}</>;
}

// Usage
export default function AdminPage() {
  return (
    <Protected>
      <AdminDashboard />
    </Protected>
  );
}
```

## Sign In / Sign Out

### Sign In Form

```typescript
// app/login/page.tsx
import { signIn } from '@/auth';
import { redirect } from 'next/navigation';

export default function LoginPage() {
  return (
    <div className="login-container">
      <h1>Sign In</h1>
      
      {/* OAuth Providers */}
      <form
        action={async () => {
          'use server';
          await signIn('github');
        }}
      >
        <button type="submit">Sign in with GitHub</button>
      </form>
      
      <form
        action={async () => {
          'use server';
          await signIn('google');
        }}
      >
        <button type="submit">Sign in with Google</button>
      </form>
      
      {/* Credentials Form */}
      <form
        action={async (formData) => {
          'use server';
          const result = await signIn('credentials', {
            email: formData.get('email'),
            password: formData.get('password'),
            redirect: false,
          });
          
          if (result?.error) {
            // Handle error
            return;
          }
          
          redirect('/dashboard');
        }}
      >
        <input name="email" type="email" placeholder="Email" required />
        <input name="password" type="password" placeholder="Password" required />
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}
```

### Sign Out Button

```typescript
// components/sign-out-button.tsx
import { signOut } from '@/auth';

export function SignOutButton() {
  return (
    <form
      action={async () => {
        'use server';
        await signOut();
      }}
    >
      <button type="submit">Sign Out</button>
    </form>
  );
}

// Client-side alternative
'use client';

import { signOut } from 'next-auth/react';

export function ClientSignOutButton() {
  return (
    <button onClick={() => signOut({ callbackUrl: '/' })}>
      Sign Out
    </button>
  );
}
```

## Role-Based Access Control

### Extended Session Type

```typescript
// types/next-auth.d.ts
import { DefaultSession } from 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      id: string;
      role: 'user' | 'admin' | 'moderator';
    } & DefaultSession['user'];
  }
  
  interface User {
    role: 'user' | 'admin' | 'moderator';
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    id: string;
    role: 'user' | 'admin' | 'moderator';
  }
}
```

### Role Callbacks

```typescript
// auth.ts
callbacks: {
  jwt: async ({ token, user }) => {
    if (user) {
      token.id = user.id;
      token.role = user.role;
    }
    return token;
  },
  session: async ({ session, token }) => {
    if (token) {
      session.user.id = token.id;
      session.user.role = token.role;
    }
    return session;
  },
}
```

### Role-Based Component

```typescript
// components/require-role.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

type Role = 'user' | 'admin' | 'moderator';

export async function RequireRole({
  children,
  role,
}: {
  children: React.ReactNode;
  role: Role | Role[];
}) {
  const session = await auth();
  
  if (!session) {
    redirect('/login');
  }
  
  const allowedRoles = Array.isArray(role) ? role : [role];
  
  if (!allowedRoles.includes(session.user.role)) {
    redirect('/unauthorized');
  }
  
  return <>{children}</>;
}

// Usage
export default function AdminPage() {
  return (
    <RequireRole role="admin">
      <AdminDashboard />
    </RequireRole>
  );
}
```

## Database Session Strategy

### Prisma Schema

```prisma
// prisma/schema.prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String?   @unique
  emailVerified DateTime?
  image         String?
  password      String?
  role          String    @default("user")
  accounts      Account[]
  sessions      Session[]
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}
```

### Database Session Config

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: 'database' }, // Use database sessions
  // ... rest of config
});
```

## Best Practices

1. **Use JWT for serverless** - Database sessions don't scale well
2. **Extend types properly** - Use module augmentation for custom fields
3. **Protect at multiple levels** - Middleware + component checks
4. **Handle loading states** - Show skeletons during auth checks
5. **Secure credentials** - Hash passwords, validate input
6. **Implement RBAC** - Role-based access for admin features
7. **Use secure cookies** - Auth.js handles this by default
8. **Log auth events** - Monitor sign-ins, failures, and suspicious activity
