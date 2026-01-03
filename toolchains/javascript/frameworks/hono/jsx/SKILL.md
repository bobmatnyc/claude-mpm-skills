---
name: hono-jsx
description: Hono JSX - server-side rendering, streaming, async components, and HTML generation patterns
skill_version: 1.0.0
updated_at: 2025-01-03T00:00:00Z
tags: [hono, jsx, ssr, streaming, html, components, suspense]
progressive_disclosure:
  entry_point:
    summary: "Server-side JSX rendering with streaming, Suspense, and async components"
    when_to_use: "Rendering HTML on server, building SSR apps, streaming responses, or creating HTML templates"
    quick_start: "1. Configure tsconfig jsxImportSource 2. Create .tsx components 3. Render with c.html()"
  references: []
context_limit: 800
---

# Hono JSX - Server-Side Rendering

## Overview

Hono provides a built-in JSX renderer for server-side HTML generation. It supports async components, streaming with Suspense, and integrates seamlessly with Hono's response system.

**Key Features**:
- Server-side JSX rendering
- Async component support
- Streaming with Suspense
- Automatic head hoisting
- Error boundaries
- Context API
- Zero client-side hydration overhead

## When to Use This Skill

Use Hono JSX when:
- Building server-rendered HTML pages
- Creating email templates
- Generating static HTML
- Streaming large HTML responses
- Building MPA (Multi-Page Applications)

**Not for**: Interactive SPAs (use React/Vue/Svelte instead)

## Configuration

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx"
  }
}
```

### Alternative: Pragma Comments

```tsx
/** @jsx jsx */
/** @jsxImportSource hono/jsx */
```

### Deno Configuration

```json
// deno.json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "npm:hono/jsx"
  }
}
```

## Basic Usage

### Simple Rendering

```tsx
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.html(
    <html>
      <head>
        <title>Hello Hono</title>
      </head>
      <body>
        <h1>Hello, World!</h1>
      </body>
    </html>
  )
})
```

### Components

```tsx
import { Hono } from 'hono'
import type { FC } from 'hono/jsx'

// Define props type
type GreetingProps = {
  name: string
  age?: number
}

// Functional component
const Greeting: FC<GreetingProps> = ({ name, age }) => {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      {age && <p>You are {age} years old.</p>}
    </div>
  )
}

const app = new Hono()

app.get('/hello/:name', (c) => {
  const name = c.req.param('name')
  return c.html(<Greeting name={name} />)
})
```

### Layout Components

```tsx
import type { FC, PropsWithChildren } from 'hono/jsx'

const Layout: FC<PropsWithChildren<{ title: string }>> = ({ title, children }) => {
  return (
    <html>
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
        <link rel="stylesheet" href="/styles.css" />
      </head>
      <body>
        <header>
          <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
          </nav>
        </header>
        <main>{children}</main>
        <footer>
          <p>&copy; 2025 My App</p>
        </footer>
      </body>
    </html>
  )
}

app.get('/', (c) => {
  return c.html(
    <Layout title="Home">
      <h1>Welcome!</h1>
      <p>This is my home page.</p>
    </Layout>
  )
})
```

## Async Components

### Basic Async

```tsx
const AsyncUserList: FC = async () => {
  const users = await fetchUsers()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

app.get('/users', async (c) => {
  return c.html(<AsyncUserList />)
})
```

### Nested Async Components

```tsx
const UserProfile: FC<{ id: string }> = async ({ id }) => {
  const user = await fetchUser(id)

  return (
    <div class="profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <UserPosts userId={id} />
    </div>
  )
}

const UserPosts: FC<{ userId: string }> = async ({ userId }) => {
  const posts = await fetchUserPosts(userId)

  return (
    <div class="posts">
      <h3>Posts</h3>
      {posts.map(post => (
        <article key={post.id}>
          <h4>{post.title}</h4>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  )
}
```

## Streaming with Suspense

### Basic Streaming

```tsx
import { Suspense, renderToReadableStream } from 'hono/jsx/streaming'

const SlowComponent: FC = async () => {
  await new Promise(resolve => setTimeout(resolve, 2000))
  return <div>Loaded after 2 seconds!</div>
}

app.get('/stream', (c) => {
  const stream = renderToReadableStream(
    <html>
      <body>
        <h1>Streaming Demo</h1>
        <Suspense fallback={<div>Loading...</div>}>
          <SlowComponent />
        </Suspense>
      </body>
    </html>
  )

  return c.body(stream, {
    headers: {
      'Content-Type': 'text/html; charset=UTF-8',
      'Transfer-Encoding': 'chunked'
    }
  })
})
```

### Multiple Suspense Boundaries

```tsx
const Page: FC = () => {
  return (
    <Layout title="Dashboard">
      <h1>Dashboard</h1>

      <Suspense fallback={<div>Loading user...</div>}>
        <UserProfile />
      </Suspense>

      <Suspense fallback={<div>Loading stats...</div>}>
        <Statistics />
      </Suspense>

      <Suspense fallback={<div>Loading feed...</div>}>
        <ActivityFeed />
      </Suspense>
    </Layout>
  )
}
```

## Error Boundaries

```tsx
import { ErrorBoundary } from 'hono/jsx'

const RiskyComponent: FC = () => {
  if (Math.random() > 0.5) {
    throw new Error('Random error!')
  }
  return <div>Success!</div>
}

const ErrorFallback: FC<{ error: Error }> = ({ error }) => {
  return (
    <div class="error">
      <h3>Something went wrong</h3>
      <p>{error.message}</p>
    </div>
  )
}

app.get('/risky', (c) => {
  return c.html(
    <Layout title="Risky Page">
      <ErrorBoundary fallback={ErrorFallback}>
        <RiskyComponent />
      </ErrorBoundary>
    </Layout>
  )
})
```

### Async Error Boundaries

```tsx
const AsyncRiskyComponent: FC = async () => {
  const data = await fetchData()

  if (!data) {
    throw new Error('Data not found')
  }

  return <div>{data}</div>
}

// Error boundary catches async errors too
<ErrorBoundary fallback={({ error }) => <p>Error: {error.message}</p>}>
  <AsyncRiskyComponent />
</ErrorBoundary>
```

## Context API

### Creating Context

```tsx
import { createContext, useContext } from 'hono/jsx'

type Theme = 'light' | 'dark'

const ThemeContext = createContext<Theme>('light')

const ThemedButton: FC<{ label: string }> = ({ label }) => {
  const theme = useContext(ThemeContext)
  const className = theme === 'dark' ? 'btn-dark' : 'btn-light'

  return <button class={className}>{label}</button>
}

const App: FC<{ theme: Theme }> = ({ theme, children }) => {
  return (
    <ThemeContext.Provider value={theme}>
      <div class={`app theme-${theme}`}>
        {children}
      </div>
    </ThemeContext.Provider>
  )
}

app.get('/', (c) => {
  const theme = c.req.query('theme') as Theme || 'light'

  return c.html(
    <App theme={theme}>
      <ThemedButton label="Click me" />
    </App>
  )
})
```

## Head Hoisting

Tags like `<title>`, `<meta>`, `<link>`, and `<script>` are automatically hoisted to `<head>`:

```tsx
const Page: FC<{ title: string }> = ({ title, children }) => {
  return (
    <html>
      <head>
        {/* Base head content */}
      </head>
      <body>
        {/* These will be hoisted to head! */}
        <title>{title}</title>
        <meta name="description" content="Page description" />
        <link rel="stylesheet" href="/page.css" />

        <div>{children}</div>
      </body>
    </html>
  )
}

// Even from nested components
const SEO: FC<{ title: string; description: string }> = ({ title, description }) => {
  return (
    <>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
    </>
  )
}

const Article: FC<{ article: Article }> = ({ article }) => {
  return (
    <div>
      <SEO title={article.title} description={article.excerpt} />
      <h1>{article.title}</h1>
      <div>{article.content}</div>
    </div>
  )
}
```

## Raw HTML

### dangerouslySetInnerHTML

```tsx
const RawHtml: FC<{ html: string }> = ({ html }) => {
  return <div dangerouslySetInnerHTML={{ __html: html }} />
}

// Usage
const markdown = await renderMarkdown(content)
<RawHtml html={markdown} />
```

### Raw Helper

```tsx
import { raw } from 'hono/html'

const Page: FC = () => {
  return (
    <html>
      <body>
        {raw('<script>console.log("Hello")</script>')}
      </body>
    </html>
  )
}
```

## Fragments

```tsx
import { Fragment } from 'hono/jsx'

// Using Fragment
const List: FC = () => {
  return (
    <Fragment>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </Fragment>
  )
}

// Using short syntax
const List2: FC = () => {
  return (
    <>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </>
  )
}
```

## Memoization

```tsx
import { memo } from 'hono/jsx'

// Expensive to compute
const ExpensiveComponent: FC<{ data: string[] }> = ({ data }) => {
  const processed = data.map(item => item.toUpperCase()).join(', ')
  return <div>{processed}</div>
}

// Memoize the result
const MemoizedExpensive = memo(ExpensiveComponent)

// Won't recompute if data is the same
<MemoizedExpensive data={['a', 'b', 'c']} />
```

## Integration Patterns

### With HTMX

```tsx
const TodoList: FC<{ todos: Todo[] }> = ({ todos }) => {
  return (
    <ul id="todo-list">
      {todos.map(todo => (
        <li key={todo.id}>
          <span>{todo.text}</span>
          <button
            hx-delete={`/todos/${todo.id}`}
            hx-target="closest li"
            hx-swap="outerHTML"
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  )
}

app.get('/todos', async (c) => {
  const todos = await getTodos()

  return c.html(
    <Layout title="Todos">
      <script src="https://unpkg.com/htmx.org@1.9.10"></script>
      <h1>Todos</h1>
      <TodoList todos={todos} />
      <form hx-post="/todos" hx-target="#todo-list" hx-swap="beforeend">
        <input name="text" placeholder="New todo" />
        <button type="submit">Add</button>
      </form>
    </Layout>
  )
})

app.post('/todos', async (c) => {
  const { text } = await c.req.parseBody()
  const todo = await createTodo(text as string)

  return c.html(
    <li>
      <span>{todo.text}</span>
      <button
        hx-delete={`/todos/${todo.id}`}
        hx-target="closest li"
        hx-swap="outerHTML"
      >
        Delete
      </button>
    </li>
  )
})
```

### With Tailwind CSS

```tsx
const Button: FC<{ variant: 'primary' | 'secondary' }> = ({ variant, children }) => {
  const baseClasses = 'px-4 py-2 rounded font-medium transition-colors'
  const variantClasses = variant === 'primary'
    ? 'bg-blue-600 text-white hover:bg-blue-700'
    : 'bg-gray-200 text-gray-800 hover:bg-gray-300'

  return (
    <button class={`${baseClasses} ${variantClasses}`}>
      {children}
    </button>
  )
}
```

## Quick Reference

### Key Imports

```tsx
import type { FC, PropsWithChildren } from 'hono/jsx'
import { Fragment, createContext, useContext, memo } from 'hono/jsx'
import { Suspense, renderToReadableStream } from 'hono/jsx/streaming'
import { ErrorBoundary } from 'hono/jsx'
import { raw } from 'hono/html'
```

### Response Methods

```tsx
// Direct render
c.html(<Component />)

// Streaming
c.body(renderToReadableStream(<Component />), {
  headers: { 'Content-Type': 'text/html; charset=UTF-8' }
})
```

### Component Types

```tsx
// Basic
const Comp: FC = () => <div>Hello</div>

// With props
const Comp: FC<{ name: string }> = ({ name }) => <div>{name}</div>

// With children
const Comp: FC<PropsWithChildren> = ({ children }) => <div>{children}</div>

// Async
const Comp: FC = async () => {
  const data = await fetch()
  return <div>{data}</div>
}
```

## Related Skills

- **hono-core** - Framework fundamentals
- **hono-middleware** - Middleware patterns
- **hono-cloudflare** - Edge deployment

---

**Version**: Hono 4.x
**Last Updated**: January 2025
**License**: MIT
