# React 19 Platform Hooks & APIs

> Source of truth: [use()](https://react.dev/reference/react/use), [useActionState](https://react.dev/reference/react/useActionState), [useOptimistic](https://react.dev/reference/react/useOptimistic), [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus), [<form>](https://react.dev/reference/react-dom/components/form), and the [React 19 release notes](https://react.dev/blog/2024/12/05/react-19). This reference applies that guidance.

## The `use()` Hook

`use()` reads the value of a promise or a context. Unlike every other hook, it may be called **conditionally** — after early returns, inside branches — a deliberate exception to the Rules of Hooks. When given a promise, it suspends the component until the promise resolves, integrating with the nearest Suspense boundary.

```tsx
function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  // Legal after an early return — `use` is exempt from the top-level rule.
  const comments = use(commentsPromise);
  return <ul>{comments.map((c) => <li key={c.id}>{c.text}</li>)}</ul>;
}

function ThemedButton() {
  const theme = use(ThemeContext); // also reads context, conditionally if needed
  return <button className={theme}>Save</button>;
}
```

### Rules and pitfalls

- **Never wrap `use()` in `try/catch`.** A suspended promise is not a thrown synchronous error; rejections surface through an **Error Boundary**, not `catch`.
- **Do not create the promise during render on the client.** A promise created in the render body is a new promise every render, which defeats caching and can loop. Create it high in the tree, in an event handler, or on the server, and pass it down.

```tsx
// BAD: new promise each render → re-suspends endlessly on the client.
function Profile({ id }: { id: string }) {
  const user = use(fetchUser(id));
  return <h1>{user.name}</h1>;
}
```

```tsx
// GOOD: the promise is created once by a parent/server and passed down.
function Profile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <h1>{user.name}</h1>;
}
```

## Actions

Actions are React's built-in async-mutation model. They provide pending, error, and optimistic handling at the React level, independent of any framework.

### `useActionState`

Runs an action function, tracks pending state, and threads the previous result forward. It replaces the canary `useFormState` (same idea, renamed and moved to `react`).

```tsx
function UpdateName({ save }: { save: (name: string) => Promise<{ error?: string }> }) {
  const [state, formAction, isPending] = useActionState(
    async (_prev: { error?: string }, formData: FormData) => {
      const res = await save(formData.get('name') as string);
      return res.error ? { error: res.error } : {};
    },
    {},
  );

  return (
    <form action={formAction}>
      <input name="name" disabled={isPending} />
      <button disabled={isPending}>Save</button>
      {state.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

### `useOptimistic`

Renders an optimistic value while an action is in flight, reverting automatically when the action settles.

```tsx
function Likes({ count, like }: { count: number; like: () => Promise<void> }) {
  const [optimisticCount, addOptimistic] = useOptimistic(count, (c) => c + 1);

  async function onLike() {
    addOptimistic(null);  // show +1 immediately
    await like();         // reverts to real `count` if this throws
  }

  return <button onClick={onLike}>♥ {optimisticCount}</button>;
}
```

### `useFormStatus`

Reads the pending state of the enclosing `<form>` from a child component, with no props threaded through.

```tsx
function SubmitButton() {
  const { pending } = useFormStatus(); // reads the parent <form>, not its own state
  return <button disabled={pending}>{pending ? 'Saving…' : 'Save'}</button>;
}
```

### `<form action={fn}>`

A function passed to a form's `action` runs on submit, receiving the `FormData`. React resets an uncontrolled form automatically on success (use `requestFormReset` to opt out). Individual buttons may override with `formAction`.

## React 19 Ergonomic Changes

### `ref` as a plain prop

`forwardRef` is deprecated. A function component receives `ref` like any other prop. A codemod migrates existing `forwardRef` usage.

```tsx
// BEFORE (React 18)
const TextInput = forwardRef<HTMLInputElement, Props>((props, ref) => (
  <input ref={ref} {...props} />
));
```

```tsx
// AFTER (React 19): ref is just a prop
function TextInput({ ref, ...props }: Props & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

`useImperativeHandle` still customizes the exposed handle; it now reads the `ref` prop directly.

### `<Context value>` as provider

`<Context.Provider>` is legacy. Render the context itself with a `value`.

```tsx
// BEFORE
<ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
```

```tsx
// AFTER
<ThemeContext value={theme}>{children}</ThemeContext>
```

### Native document metadata

`<title>`, `<meta>`, and `<link>` rendered anywhere in the tree hoist to `<head>` automatically — `react-helmet` is no longer needed.

```tsx
function ArticlePage({ article }: { article: Article }) {
  return (
    <article>
      <title>{article.title}</title>
      <meta name="description" content={article.summary} />
      <h1>{article.title}</h1>
    </article>
  );
}
```

Resource hints — `preload`, `preinit`, `preconnect`, `prefetchDNS` from `react-dom` — let a component declare what the browser should fetch early.

## Migration Notes from 17/18

| 17/18 idiom | React 19 replacement |
|---|---|
| `forwardRef((props, ref) => …)` | `ref` as a prop; codemod available |
| `<Context.Provider value>` | `<Context value>` |
| `react-helmet` for `<head>` tags | Native metadata hoisting |
| `useFormState` (canary) | `useActionState` (from `react`) |
| Manual pending/error state around fetch-in-event | `useActionState` + `useOptimistic` |
| Fetch in `useEffect`, store in state | Pass a promise to `use()` under Suspense |

## Sources

- https://react.dev/reference/react/use
- https://react.dev/reference/react/useActionState
- https://react.dev/reference/react/useOptimistic
- https://react.dev/reference/react-dom/hooks/useFormStatus
- https://react.dev/reference/react-dom/components/form
- https://react.dev/reference/react/forwardRef
- https://react.dev/reference/react/useImperativeHandle
- https://react.dev/reference/react/createContext
- https://react.dev/reference/react-dom/components/meta
- https://react.dev/blog/2024/12/05/react-19
