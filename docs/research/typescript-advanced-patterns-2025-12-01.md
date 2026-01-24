# Advanced TypeScript Patterns: Moderate to Difficult Use Cases

**Research Date:** 2025-12-01
**Focus:** Type system mastery, runtime validation, framework integration, and design patterns
**Complexity Level:** Moderate to Advanced

---

## Table of Contents

1. [Advanced Type System](#1-advanced-type-system)
2. [Generic Programming](#2-generic-programming)
3. [Design Patterns](#3-design-patterns)
4. [API & Data Handling](#4-api--data-handling)
5. [Framework Integration](#5-framework-integration)
6. [Best Practices & Anti-Patterns](#6-best-practices--anti-patterns)

---

## 1. Advanced Type System

### 1.1 Conditional Types with Distributive Behavior

**Complexity:** ⭐⭐⭐⭐
**Problem:** Need to transform union types while maintaining individual type information

**Pattern:**
```typescript
// Distributive conditional type
type ToArray<T> = T extends unknown ? T[] : never;

type Result = ToArray<string | number>;
// Result: string[] | number[] (NOT (string | number)[])

// Prevent distribution with tuple wrapping
type ToArrayNonDistributive<T> = [T] extends [unknown] ? T[] : never;

type UnionResult = ToArrayNonDistributive<string | number>;
// Result: (string | number)[]
```

**Type Safety Benefits:**
- Maintains type precision in union transformations
- Enables type-level programming with unions
- Prevents accidental type widening

**Common Mistakes:**
- ❌ Forgetting conditional types distribute over unions by default
- ❌ Using `[T]` wrapping without understanding distribution

**Best Practices:**
- Use distributive behavior for individual type transformation
- Use tuple wrapping when you need to treat union as single entity
- Document when distribution is intentional vs. prevented

---

### 1.2 The `infer` Keyword - Advanced Extraction

**Complexity:** ⭐⭐⭐⭐⭐
**Problem:** Extract types from complex structures without manual type definitions

**Pattern:**
```typescript
// Extract return type from function
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;

// Extract Promise resolution type recursively
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

// Extract first function argument
type FirstArg<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;

// Multiple infer positions
type ExtractEventPayload<T> = T extends {
  type: infer Type;
  payload: infer Payload
} ? { type: Type; payload: Payload } : never;

// Practical example: API response unwrapping
type UnwrapResponse<T> = T extends { data: infer D; success: true }
  ? D
  : T extends { error: infer E; success: false }
    ? never
    : never;

interface SuccessResponse<T> {
  data: T;
  success: true;
}

interface ErrorResponse {
  error: string;
  success: false;
}

type UserData = UnwrapResponse<SuccessResponse<{ id: string; name: string }>>;
// Result: { id: string; name: string }
```

**Type Safety Benefits:**
- Eliminates need for manual type extraction
- Enables building complex type utilities
- Automatically adapts to source type changes

**Common Mistakes:**
- ❌ Using `infer` outside conditional types
- ❌ Not handling the `never` case for non-matching types
- ❌ Overcomplicating with nested `infer` when simpler patterns exist

**Best Practices:**
- Always provide a fallback type (often `never`)
- Combine with distributive conditional types for union handling
- Use built-in utility types before creating custom ones

---

### 1.3 Template Literal Types - Route Parameter Extraction

**Complexity:** ⭐⭐⭐⭐
**Problem:** Type-safe route parameters without runtime parsing

**Pattern:**
```typescript
// Extract route parameters
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

// Create params object type
type RouteParams<T extends string> = {
  [K in ExtractRouteParams<T>]: string
};

// Usage
type UserPostRoute = "/users/:userId/posts/:postId";
type Params = RouteParams<UserPostRoute>;
// Result: { userId: string; postId: string }

// Advanced: Extract with query params
type ExtractWithQuery<T extends string> =
  T extends `${infer Path}?${infer Query}`
    ? { path: ExtractRouteParams<Path>; query: ExtractQueryParams<Query> }
    : { path: ExtractRouteParams<T>; query: never };

type ExtractQueryParams<T extends string> =
  T extends `${infer Key}=${string}&${infer Rest}`
    ? Key | ExtractQueryParams<Rest>
    : T extends `${infer Key}=${string}`
      ? Key
      : never;

// Practical: Type-safe route handler
function createRoute<T extends string>(route: T) {
  return {
    path: route,
    handler: (params: RouteParams<T>) => {
      // params is fully typed!
      return params;
    }
  };
}

const userRoute = createRoute("/users/:userId/posts/:postId");
userRoute.handler({ userId: "123", postId: "456" }); // ✅
userRoute.handler({ userId: "123" }); // ❌ Type error: missing postId
```

**Type Safety Benefits:**
- Compile-time route validation
- Auto-completion for route parameters
- Prevents missing or typo'd parameters

**Common Mistakes:**
- ❌ Not handling edge cases (no params, trailing slashes)
- ❌ Over-recursion causing "Type instantiation is excessively deep"

**Best Practices:**
- Set recursion limits or use iterative patterns for deeply nested routes
- Normalize route format before extraction (remove trailing slashes)
- Combine with branded types for additional safety

---

### 1.4 Recursive Types - Deep Object Path Access

**Complexity:** ⭐⭐⭐⭐⭐
**Problem:** Type-safe nested object access with dot notation

**Pattern:**
```typescript
// Depth limiter to prevent infinite recursion
type Prev = [never, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Extract all possible paths
type Paths<T, D extends number = 10> = [D] extends [never]
  ? never
  : T extends object
    ? {
        [K in keyof T]-?: K extends string | number
          ? `${K}` | `${K}.${Paths<T[K], Prev[D]>}`
          : never;
      }[keyof T]
    : never;

// Get value by path
type Get<T, P extends string> = P extends `${infer K}.${infer Rest}`
  ? K extends keyof T
    ? Get<T[K], Rest>
    : never
  : P extends keyof T
    ? T[P]
    : never;

// Set value by path (immutable)
type Set<T, P extends string, V> = P extends `${infer K}.${infer Rest}`
  ? K extends keyof T
    ? { [Key in keyof T]: Key extends K ? Set<T[Key], Rest, V> : T[Key] }
    : never
  : P extends keyof T
    ? { [Key in keyof T]: Key extends P ? V : T[Key] }
    : never;

// Usage example
interface User {
  name: string;
  address: {
    city: string;
    zip: { code: string; plus4?: string };
  };
  preferences: {
    theme: "light" | "dark";
    notifications: boolean;
  };
}

type UserPaths = Paths<User>;
// "name" | "address" | "address.city" | "address.zip" | "address.zip.code" | ...

type City = Get<User, "address.city">; // string
type ZipCode = Get<User, "address.zip.code">; // string

// Type-safe getter function
function get<T, P extends Paths<T>>(obj: T, path: P): Get<T, P> {
  const keys = path.split('.');
  let result: any = obj;
  for (const key of keys) {
    result = result[key];
  }
  return result as Get<T, P>;
}

const user: User = {
  name: "Alice",
  address: {
    city: "NYC",
    zip: { code: "10001" }
  },
  preferences: {
    theme: "dark",
    notifications: true
  }
};

const city = get(user, "address.city"); // Type: string, Value: "NYC"
const invalid = get(user, "address.invalid"); // ❌ Type error
```

**Type Safety Benefits:**
- Compile-time path validation
- Auto-completion for nested paths
- Prevents runtime errors from invalid paths

**Common Mistakes:**
- ❌ Not limiting recursion depth (causes compiler crash)
- ❌ Forgetting to handle optional properties
- ❌ Not using `-?` modifier to handle optional keys

**Best Practices:**
- Always use depth limiter for recursive types
- Consider performance impact on large object types
- Use simpler patterns for shallow objects (Pick, Omit)

---

### 1.5 Mapped Types with Key Remapping

**Complexity:** ⭐⭐⭐⭐
**Problem:** Transform object keys while maintaining type safety

**Pattern:**
```typescript
// Create getter methods from properties
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};

type User = { name: string; age: number };
type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number }

// Filter properties by type
type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K]
};

type Mixed = { id: number; name: string; email: string; active: boolean };
type StringProps = OnlyStrings<Mixed>;
// { name: string; email: string }

// Omit by value type
type OmitByType<T, U> = {
  [K in keyof T as T[K] extends U ? never : K]: T[K]
};

type NoFunctions = OmitByType<Mixed & { log: () => void }, Function>;
// { id: number; name: string; email: string; active: boolean }

// Create event handlers
type EventHandlers<T> = {
  [K in keyof T as `on${Capitalize<string & K>}Change`]: (value: T[K]) => void
};

type Form = { name: string; email: string; age: number };
type FormHandlers = EventHandlers<Form>;
// {
//   onNameChange: (value: string) => void;
//   onEmailChange: (value: string) => void;
//   onAgeChange: (value: number) => void;
// }

// Practical example: Redux-like actions
type ActionsFromState<T, Prefix extends string = "set"> = {
  [K in keyof T as `${Prefix}${Capitalize<string & K>}`]: (value: T[K]) => void
};

type State = { count: number; user: User | null; loading: boolean };
type Actions = ActionsFromState<State>;
// {
//   setCount: (value: number) => void;
//   setUser: (value: User | null) => void;
//   setLoading: (value: boolean) => void;
// }
```

**Type Safety Benefits:**
- Automatically generate related types from single source
- Maintain consistency between types
- Reduce manual type definition duplication

**Common Mistakes:**
- ❌ Forgetting `string &` intersection to ensure string keys
- ❌ Not handling symbol or number keys when they exist
- ❌ Creating too many derived types (impacts compile time)

**Best Practices:**
- Use for auto-generating related interfaces (getters, setters, events)
- Combine with template literal types for naming patterns
- Consider codegen for very large types

---

### 1.6 Branded Types for Type Safety

**Complexity:** ⭐⭐⭐
**Problem:** Prevent primitive type misuse (e.g., userId vs postId both as string)

**Pattern:**
```typescript
// Brand type helper
type Brand<T, B> = T & { __brand: B };

// Create branded types
type UserId = Brand<string, "UserId">;
type PostId = Brand<string, "PostId">;
type Email = Brand<string, "Email">;

// Constructor functions with validation
function UserId(id: string): UserId {
  if (!id.match(/^user_[a-zA-Z0-9]+$/)) {
    throw new Error("Invalid user ID format");
  }
  return id as UserId;
}

function PostId(id: string): PostId {
  if (!id.match(/^post_[0-9]+$/)) {
    throw new Error("Invalid post ID format");
  }
  return id as PostId;
}

function Email(email: string): Email {
  if (!email.includes("@")) {
    throw new Error("Invalid email format");
  }
  return email as Email;
}

// Usage
function getUser(id: UserId): Promise<User> {
  // Implementation
  return Promise.resolve({} as User);
}

function getPost(id: PostId): Promise<Post> {
  // Implementation
  return Promise.resolve({} as Post);
}

const userId = UserId("user_abc123");
const postId = PostId("post_456");

getUser(userId); // ✅
getUser(postId); // ❌ Type error: PostId not assignable to UserId
getUser("user_abc123"); // ❌ Type error: string not assignable to UserId

// Advanced: Numeric brands
type Positive = Brand<number, "Positive">;
type Percentage = Brand<number, "Percentage">;

function Positive(n: number): Positive {
  if (n <= 0) throw new Error("Must be positive");
  return n as Positive;
}

function Percentage(n: number): Percentage {
  if (n < 0 || n > 100) throw new Error("Must be 0-100");
  return n as Percentage;
}

function setOpacity(opacity: Percentage): void {
  // Implementation
}

setOpacity(Percentage(50)); // ✅
setOpacity(Positive(50)); // ❌ Type error
setOpacity(50); // ❌ Type error

// Combine with Zod for validation
import { z } from 'zod';

const UserIdSchema = z.string()
  .regex(/^user_[a-zA-Z0-9]+$/)
  .transform(id => id as UserId);

type UserIdFromSchema = z.infer<typeof UserIdSchema>; // UserId
```

**Type Safety Benefits:**
- Prevents accidentally mixing similar primitive types
- Enforces validation at type boundaries
- Self-documenting code (types indicate intent)

**Common Mistakes:**
- ❌ Forgetting to create constructor functions (allows bypassing validation)
- ❌ Using branded types for internal-only functions (over-engineering)
- ❌ Not integrating with runtime validation libraries

**Best Practices:**
- Use for domain-critical IDs and values
- Combine with Zod or other validators
- Export constructor functions alongside types
- Consider performance impact (runtime checks on hot paths)

---

## 2. Generic Programming

### 2.1 Generic Constraints with `extends`

**Complexity:** ⭐⭐⭐
**Problem:** Ensure generic types have specific properties or capabilities

**Pattern:**
```typescript
// Constraint requiring specific properties
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // ✅ Type: string
const invalid = getProperty(user, "invalid"); // ❌ Type error

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

// Constraint with interface
interface Identifiable {
  id: string;
}

function findById<T extends Identifiable>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Usage
const users = [
  { id: "1", name: "Alice" },
  { id: "2", name: "Bob" }
];
const found = findById(users, "1"); // Type: { id: string; name: string } | undefined

// Advanced: Conditional constraints
type Prettify<T> = {
  [K in keyof T]: T[K]
} & {};

function process<T extends string | number>(
  value: T
): T extends string ? string[] : number[] {
  if (typeof value === "string") {
    return value.split("") as any;
  }
  return [value] as any;
}

const strResult = process("hello"); // Type: string[]
const numResult = process(42); // Type: number[]
```

**Type Safety Benefits:**
- Ensures generic types meet minimum requirements
- Enables better IDE auto-completion
- Prevents runtime errors from missing properties

**Common Mistakes:**
- ❌ Over-constraining (makes generic too specific)
- ❌ Forgetting constraints allow subtypes (may have extra properties)
- ❌ Using `any` as constraint (defeats purpose)

**Best Practices:**
- Use minimal necessary constraints
- Prefer interface constraints over type unions for clarity
- Combine with `keyof` for property access patterns

---

### 2.2 Variadic Tuple Types

**Complexity:** ⭐⭐⭐⭐
**Problem:** Type-safe function composition and currying

**Pattern:**
```typescript
// Function composition with full type inference
type Fn<T = any, R = any> = (arg: T) => R;

function compose<A, B, C>(
  f: Fn<B, C>,
  g: Fn<A, B>
): Fn<A, C> {
  return (arg: A) => f(g(arg));
}

// Variadic compose (arbitrary number of functions)
type Last<T extends any[]> = T extends [...infer _, infer L] ? L : never;
type First<T extends any[]> = T extends [infer F, ...infer _] ? F : never;

function pipe<T extends Fn[], R = ReturnType<Last<T>>>(
  ...fns: T
): Fn<Parameters<First<T>>[0], R> {
  return (input) => fns.reduce((acc, fn) => fn(acc), input) as R;
}

// Usage
const addOne = (n: number) => n + 1;
const double = (n: number) => n * 2;
const toString = (n: number) => n.toString();

const transform = pipe(addOne, double, toString);
const result = transform(5); // Type: string, Value: "12"

// Advanced: Type-safe curry
type Curry<P extends any[], R> =
  P extends [infer Head, ...infer Tail]
    ? (arg: Head) => Curry<Tail, R>
    : R;

function curry<P extends any[], R>(
  fn: (...args: P) => R
): Curry<P, R> {
  return function curried(...args: any[]): any {
    if (args.length >= fn.length) {
      return fn(...args as P);
    }
    return (...nextArgs: any[]) => curried(...args, ...nextArgs);
  } as Curry<P, R>;
}

// Usage
const add = (a: number, b: number, c: number) => a + b + c;
const curriedAdd = curry(add);

const result1 = curriedAdd(1)(2)(3); // Type: number, Value: 6
const result2 = curriedAdd(1, 2)(3); // Type: number, Value: 6

// Practical: Event emitter with typed events
type EventMap = Record<string, any[]>;

class TypedEmitter<T extends EventMap> {
  private listeners: { [K in keyof T]?: Array<(...args: T[K]) => void> } = {};

  on<K extends keyof T>(event: K, handler: (...args: T[K]) => void): void {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(handler);
  }

  emit<K extends keyof T>(event: K, ...args: T[K]): void {
    const handlers = this.listeners[event];
    if (handlers) {
      handlers.forEach(handler => handler(...args));
    }
  }
}

// Usage with full type safety
interface MyEvents {
  userLogin: [userId: string, timestamp: Date];
  userLogout: [userId: string];
  dataUpdate: [data: { id: string; value: number }];
}

const emitter = new TypedEmitter<MyEvents>();

emitter.on("userLogin", (userId, timestamp) => {
  // userId: string, timestamp: Date (fully typed!)
  console.log(`User ${userId} logged in at ${timestamp}`);
});

emitter.emit("userLogin", "user123", new Date()); // ✅
emitter.emit("userLogin", "user123"); // ❌ Type error: missing timestamp
emitter.emit("userLogin", 123, new Date()); // ❌ Type error: userId not string
```

**Type Safety Benefits:**
- Full type inference through function chains
- Prevents argument order mistakes
- Enables complex functional patterns with safety

**Common Mistakes:**
- ❌ Losing type information in reduce/fold operations
- ❌ Not handling edge cases (empty arrays, single element)
- ❌ Using `any` instead of proper inference

**Best Practices:**
- Use tuple types for fixed-length argument lists
- Leverage `Parameters` and `ReturnType` utilities
- Test complex generic functions with type-level tests

---

### 2.3 Generic Factory Pattern

**Complexity:** ⭐⭐⭐⭐
**Problem:** Create type-safe factories with dependency injection

**Pattern:**
```typescript
// Generic factory interface
interface Factory<T> {
  create(...args: any[]): T;
}

// Type-safe builder pattern
class Builder<T> {
  private data: Partial<T> = {};

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.data[key] = value;
    return this;
  }

  build(defaults: T): T {
    return { ...defaults, ...this.data };
  }
}

// Usage
interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
}

const userDefaults: User = {
  id: "",
  name: "",
  email: "",
  role: "user"
};

const user = new Builder<User>()
  .set("id", "123")
  .set("name", "Alice")
  .set("email", "alice@example.com")
  .build(userDefaults);

// Advanced: Type-safe required fields
type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K
}[keyof T];

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never
}[keyof T];

class StrictBuilder<T> {
  private data: Partial<T> = {};

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.data[key] = value;
    return this;
  }

  build(this: StrictBuilder<T> & { data: Pick<T, RequiredKeys<T>> }): T {
    return this.data as T;
  }
}

// This approach requires all required fields before build() succeeds
// Note: Full implementation requires more advanced type-level programming

// Practical: Dependency injection container
class Container {
  private services = new Map<string, any>();
  private factories = new Map<string, () => any>();

  register<T>(name: string, factory: () => T): void {
    this.factories.set(name, factory);
  }

  get<T>(name: string): T {
    if (this.services.has(name)) {
      return this.services.get(name);
    }

    const factory = this.factories.get(name);
    if (!factory) {
      throw new Error(`Service ${name} not registered`);
    }

    const instance = factory();
    this.services.set(name, instance);
    return instance;
  }
}

// Type-safe version
type ServiceMap = {
  userService: UserService;
  emailService: EmailService;
  logger: Logger;
};

class TypedContainer<T extends Record<string, any>> {
  private services = new Map<keyof T, any>();
  private factories = new Map<keyof T, () => any>();

  register<K extends keyof T>(name: K, factory: () => T[K]): void {
    this.factories.set(name, factory);
  }

  get<K extends keyof T>(name: K): T[K] {
    if (this.services.has(name)) {
      return this.services.get(name)!;
    }

    const factory = this.factories.get(name);
    if (!factory) {
      throw new Error(`Service ${String(name)} not registered`);
    }

    const instance = factory();
    this.services.set(name, instance);
    return instance;
  }
}

// Usage
const container = new TypedContainer<ServiceMap>();

container.register("userService", () => new UserService());
container.register("logger", () => new Logger());

const userService = container.get("userService"); // Type: UserService
const invalid = container.get("invalidService"); // ❌ Type error
```

**Type Safety Benefits:**
- Type-safe service registration and retrieval
- Compile-time dependency checking
- Prevents missing or mismatched dependencies

**Common Mistakes:**
- ❌ Allowing circular dependencies (runtime error)
- ❌ Not handling async factory functions
- ❌ Losing type information in deeply nested factories

**Best Practices:**
- Use interface-based design for testability
- Implement lifecycle hooks (onCreate, onDestroy)
- Consider using existing DI libraries (tsyringe, InversifyJS) for production

---

## 3. Design Patterns

### 3.1 Observer/PubSub with Type Safety

**Complexity:** ⭐⭐⭐
**Problem:** Type-safe event system with multiple event types

**Pattern:**
```typescript
// Event map definition
type EventMap = Record<string, any>;

// Type-safe event emitter
class EventEmitter<Events extends EventMap> {
  private listeners: {
    [K in keyof Events]?: Set<(data: Events[K]) => void>
  } = {};

  on<K extends keyof Events>(
    event: K,
    handler: (data: Events[K]) => void
  ): () => void {
    if (!this.listeners[event]) {
      this.listeners[event] = new Set();
    }
    this.listeners[event]!.add(handler);

    // Return unsubscribe function
    return () => {
      this.listeners[event]?.delete(handler);
    };
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    const handlers = this.listeners[event];
    if (handlers) {
      handlers.forEach(handler => handler(data));
    }
  }

  once<K extends keyof Events>(
    event: K,
    handler: (data: Events[K]) => void
  ): void {
    const wrappedHandler = (data: Events[K]) => {
      handler(data);
      this.off(event, wrappedHandler);
    };
    this.on(event, wrappedHandler);
  }

  off<K extends keyof Events>(
    event: K,
    handler: (data: Events[K]) => void
  ): void {
    this.listeners[event]?.delete(handler);
  }
}

// Usage
interface AppEvents {
  "user:login": { userId: string; timestamp: Date };
  "user:logout": { userId: string };
  "data:update": { key: string; value: unknown };
  "error": { message: string; code: number };
}

const events = new EventEmitter<AppEvents>();

// Fully typed subscription
events.on("user:login", (data) => {
  // data: { userId: string; timestamp: Date }
  console.log(`User ${data.userId} logged in`);
});

// Typed emission
events.emit("user:login", {
  userId: "123",
  timestamp: new Date()
}); // ✅

events.emit("user:login", { userId: "123" }); // ❌ Type error: missing timestamp

// Unsubscribe pattern
const unsubscribe = events.on("data:update", (data) => {
  console.log(`Data updated: ${data.key}`);
});

// Later...
unsubscribe();

// Advanced: Async event handlers
class AsyncEventEmitter<Events extends EventMap> {
  private listeners: {
    [K in keyof Events]?: Set<(data: Events[K]) => Promise<void> | void>
  } = {};

  on<K extends keyof Events>(
    event: K,
    handler: (data: Events[K]) => Promise<void> | void
  ): () => void {
    if (!this.listeners[event]) {
      this.listeners[event] = new Set();
    }
    this.listeners[event]!.add(handler);

    return () => {
      this.listeners[event]?.delete(handler);
    };
  }

  async emit<K extends keyof Events>(event: K, data: Events[K]): Promise<void> {
    const handlers = this.listeners[event];
    if (handlers) {
      await Promise.all(
        Array.from(handlers).map(handler => handler(data))
      );
    }
  }
}
```

**Type Safety Benefits:**
- Compile-time event name validation
- Type-safe event payloads
- Auto-completion for event names and payloads

**Common Mistakes:**
- ❌ Forgetting to unsubscribe (memory leaks)
- ❌ Not handling async errors in listeners
- ❌ Creating too many event types (consider using discriminated unions)

**Best Practices:**
- Return unsubscribe functions from `on()` methods
- Use `once()` for single-use listeners
- Consider using RxJS for complex event streams
- Implement error boundaries for async handlers

---

### 3.2 State Machine with Type Guards

**Complexity:** ⭐⭐⭐⭐
**Problem:** Type-safe state transitions with compile-time validation

**Pattern:**
```typescript
// State definitions with discriminated union
type State =
  | { status: "idle" }
  | { status: "loading"; progress: number }
  | { status: "success"; data: string }
  | { status: "error"; error: Error };

// Valid transition map
type ValidTransitions = {
  idle: "loading";
  loading: "success" | "error" | "idle";
  success: "idle";
  error: "idle";
};

// Type-safe state machine
class StateMachine<S extends { status: string }> {
  constructor(private state: S) {}

  getState(): S {
    return this.state;
  }

  // Transition with validation
  transition<NewStatus extends S["status"]>(
    newState: Extract<S, { status: NewStatus }>
  ): void {
    // Runtime validation would go here
    this.state = newState as S;
  }

  // Type guard helpers
  is<Status extends S["status"]>(
    status: Status
  ): this is StateMachine<Extract<S, { status: Status }>> {
    return this.state.status === status;
  }
}

// Usage
const machine = new StateMachine<State>({ status: "idle" });

machine.transition({ status: "loading", progress: 0 }); // ✅

if (machine.is("loading")) {
  console.log(machine.getState().progress); // ✅ progress exists
}

machine.transition({ status: "success", data: "result" }); // ✅

if (machine.is("success")) {
  console.log(machine.getState().data); // ✅ data exists
  // machine.getState().progress; // ❌ Type error: progress doesn't exist on success
}

// Advanced: XState-style type-safe transitions
type Event =
  | { type: "FETCH" }
  | { type: "RESOLVE"; data: string }
  | { type: "REJECT"; error: Error }
  | { type: "RESET" };

type TransitionMap = {
  idle: { FETCH: "loading" };
  loading: { RESOLVE: "success"; REJECT: "error"; RESET: "idle" };
  success: { RESET: "idle" };
  error: { RESET: "idle" };
};

class AdvancedStateMachine<
  S extends { status: string },
  E extends { type: string }
> {
  constructor(
    private state: S,
    private transitions: Record<string, Record<string, string>>
  ) {}

  send(event: E): void {
    const currentStatus = this.state.status;
    const eventType = event.type;

    const nextStatus = this.transitions[currentStatus]?.[eventType];

    if (!nextStatus) {
      throw new Error(
        `Invalid transition: ${currentStatus} -> ${eventType}`
      );
    }

    // Update state based on event
    this.state = { status: nextStatus, ...event } as S;
  }

  getState(): S {
    return this.state;
  }
}

// Usage
const fetchMachine = new AdvancedStateMachine<State, Event>(
  { status: "idle" },
  {
    idle: { FETCH: "loading" },
    loading: { RESOLVE: "success", REJECT: "error", RESET: "idle" },
    success: { RESET: "idle" },
    error: { RESET: "idle" }
  }
);

fetchMachine.send({ type: "FETCH" });
fetchMachine.send({ type: "RESOLVE", data: "result" });
fetchMachine.send({ type: "RESET" });
```

**Type Safety Benefits:**
- Compile-time state transition validation
- Type narrowing within state checks
- Impossible states are unrepresentable

**Common Mistakes:**
- ❌ Not using discriminated unions (loses type narrowing)
- ❌ Allowing invalid transitions at runtime
- ❌ Forgetting to handle all states (use exhaustiveness checking)

**Best Practices:**
- Use XState for complex state machines
- Implement exhaustiveness checking with `never` type
- Separate state definition from transition logic
- Add visual diagrams for complex state graphs

---

### 3.3 Result Type Pattern (Railway-Oriented Programming)

**Complexity:** ⭐⭐⭐⭐
**Problem:** Type-safe error handling without exceptions

**Pattern:**
```typescript
// Result type definition
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Helper constructors
function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Utility functions
function map<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return result.ok ? Ok(fn(result.value)) : result;
}

function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return result.ok ? fn(result.value) : result;
}

function mapError<T, E, F>(
  result: Result<T, E>,
  fn: (error: E) => F
): Result<T, F> {
  return result.ok ? result : Err(fn(result.error));
}

// Unwrap with default
function unwrapOr<T, E>(result: Result<T, E>, defaultValue: T): T {
  return result.ok ? result.value : defaultValue;
}

// Async result
type AsyncResult<T, E = Error> = Promise<Result<T, E>>;

async function tryCatch<T>(
  fn: () => Promise<T>
): Promise<Result<T, Error>> {
  try {
    const value = await fn();
    return Ok(value);
  } catch (error) {
    return Err(error instanceof Error ? error : new Error(String(error)));
  }
}

// Practical example: API client with Result type
interface User {
  id: string;
  name: string;
  email: string;
}

interface ApiError {
  code: string;
  message: string;
  statusCode: number;
}

async function fetchUser(id: string): AsyncResult<User, ApiError> {
  const response = await fetch(`/api/users/${id}`);

  if (!response.ok) {
    return Err({
      code: "FETCH_ERROR",
      message: response.statusText,
      statusCode: response.status
    });
  }

  try {
    const data = await response.json();
    return Ok(data);
  } catch (error) {
    return Err({
      code: "PARSE_ERROR",
      message: "Failed to parse JSON",
      statusCode: response.status
    });
  }
}

// Usage with chaining
async function getUserEmail(id: string): AsyncResult<string, ApiError> {
  const userResult = await fetchUser(id);
  return map(userResult, user => user.email);
}

// Railway-oriented programming
async function processUser(id: string): AsyncResult<string, ApiError> {
  return flatMap(
    await fetchUser(id),
    async (user) => {
      // Additional processing
      return Ok(`Processed: ${user.name}`);
    }
  );
}

// Pattern matching helper
function match<T, E, R>(
  result: Result<T, E>,
  onOk: (value: T) => R,
  onErr: (error: E) => R
): R {
  return result.ok ? onOk(result.value) : onErr(result.error);
}

// Usage
const result = await fetchUser("123");

const message = match(
  result,
  (user) => `Hello, ${user.name}`,
  (error) => `Error: ${error.message}`
);

// Collect multiple results
function collect<T, E>(results: Result<T, E>[]): Result<T[], E> {
  const values: T[] = [];

  for (const result of results) {
    if (!result.ok) {
      return result;
    }
    values.push(result.value);
  }

  return Ok(values);
}

// Usage
const users = collect([
  await fetchUser("1"),
  await fetchUser("2"),
  await fetchUser("3")
]);

if (users.ok) {
  console.log("All users fetched:", users.value);
} else {
  console.error("Failed to fetch users:", users.error);
}
```

**Type Safety Benefits:**
- Forces explicit error handling
- No silent exceptions
- Type-safe error and success paths

**Common Mistakes:**
- ❌ Not handling error cases (forgetting to check `.ok`)
- ❌ Overusing for simple cases (adds boilerplate)
- ❌ Mixing Result and exception-based error handling

**Best Practices:**
- Use for domain logic and API boundaries
- Combine with Zod validation for runtime safety
- Consider using libraries like `neverthrow` for production
- Use `match()` for exhaustive handling

---

## 4. API & Data Handling

### 4.1 Type-Safe API Client with Zod

**Complexity:** ⭐⭐⭐⭐
**Problem:** Runtime validation with compile-time type safety for external APIs

**Pattern:**
```typescript
import { z } from "zod";

// API schema definitions
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(["admin", "user", "guest"]),
  createdAt: z.string().datetime().transform(s => new Date(s)),
});

const PostSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1),
  content: z.string(),
  authorId: z.string().uuid(),
  published: z.boolean(),
  createdAt: z.string().datetime().transform(s => new Date(s)),
});

type User = z.infer<typeof UserSchema>;
type Post = z.infer<typeof PostSchema>;

// Generic API client with validation
class ApiClient {
  constructor(private baseUrl: string) {}

  async get<T>(
    path: string,
    schema: z.ZodSchema<T>
  ): Promise<Result<T, ApiError>> {
    try {
      const response = await fetch(`${this.baseUrl}${path}`);

      if (!response.ok) {
        return Err({
          code: "HTTP_ERROR",
          message: response.statusText,
          statusCode: response.status
        });
      }

      const json = await response.json();
      const result = schema.safeParse(json);

      if (!result.success) {
        return Err({
          code: "VALIDATION_ERROR",
          message: result.error.message,
          statusCode: response.status,
          zodError: result.error
        });
      }

      return Ok(result.data);
    } catch (error) {
      return Err({
        code: "NETWORK_ERROR",
        message: error instanceof Error ? error.message : "Unknown error",
        statusCode: 0
      });
    }
  }

  async post<T, B>(
    path: string,
    body: B,
    responseSchema: z.ZodSchema<T>,
    bodySchema?: z.ZodSchema<B>
  ): Promise<Result<T, ApiError>> {
    try {
      // Validate request body
      if (bodySchema) {
        const bodyResult = bodySchema.safeParse(body);
        if (!bodyResult.success) {
          return Err({
            code: "REQUEST_VALIDATION_ERROR",
            message: "Invalid request body",
            statusCode: 400,
            zodError: bodyResult.error
          });
        }
      }

      const response = await fetch(`${this.baseUrl}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        return Err({
          code: "HTTP_ERROR",
          message: response.statusText,
          statusCode: response.status
        });
      }

      const json = await response.json();
      const result = responseSchema.safeParse(json);

      if (!result.success) {
        return Err({
          code: "VALIDATION_ERROR",
          message: result.error.message,
          statusCode: response.status,
          zodError: result.error
        });
      }

      return Ok(result.data);
    } catch (error) {
      return Err({
        code: "NETWORK_ERROR",
        message: error instanceof Error ? error.message : "Unknown error",
        statusCode: 0
      });
    }
  }
}

// Type-safe API endpoints
class UserApi {
  constructor(private client: ApiClient) {}

  async getUser(id: string): AsyncResult<User, ApiError> {
    return this.client.get(`/users/${id}`, UserSchema);
  }

  async getUsers(): AsyncResult<User[], ApiError> {
    return this.client.get("/users", z.array(UserSchema));
  }

  async createUser(
    data: Omit<User, "id" | "createdAt">
  ): AsyncResult<User, ApiError> {
    const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });
    return this.client.post("/users", data, UserSchema, CreateUserSchema);
  }
}

// Usage
const api = new UserApi(new ApiClient("https://api.example.com"));

const userResult = await api.getUser("123");

if (userResult.ok) {
  const user = userResult.value;
  console.log(user.name); // Type: string
  console.log(user.createdAt); // Type: Date (transformed!)
} else {
  console.error(userResult.error.message);
}

// Advanced: Caching with type safety
class CachedApiClient extends ApiClient {
  private cache = new Map<string, { data: unknown; expiry: number }>();

  async get<T>(
    path: string,
    schema: z.ZodSchema<T>,
    ttl: number = 60000
  ): Promise<Result<T, ApiError>> {
    const cached = this.cache.get(path);

    if (cached && Date.now() < cached.expiry) {
      // Validate cached data still matches schema
      const result = schema.safeParse(cached.data);
      if (result.success) {
        return Ok(result.data);
      }
      // Cache invalidated by schema change
      this.cache.delete(path);
    }

    const result = await super.get(path, schema);

    if (result.ok) {
      this.cache.set(path, {
        data: result.value,
        expiry: Date.now() + ttl
      });
    }

    return result;
  }
}
```

**Type Safety Benefits:**
- Runtime validation catches API contract violations
- Type transformations (string dates → Date objects)
- Compile-time and runtime safety combined

**Common Mistakes:**
- ❌ Not validating API responses (trusting external data)
- ❌ Duplicating types (define schema once, infer type)
- ❌ Ignoring Zod validation errors (losing useful error details)

**Best Practices:**
- Always validate external data sources
- Use Zod transformations for data normalization
- Combine with Result type for error handling
- Cache validated responses, not raw JSON

---

### 4.2 Database Layer with Type Safety (Prisma/Drizzle)

**Complexity:** ⭐⭐⭐⭐
**Problem:** End-to-end type safety from database to application

**Pattern (using Drizzle ORM):**
```typescript
import { pgTable, text, timestamp, uuid, boolean } from "drizzle-orm/pg-core";
import { drizzle } from "drizzle-orm/node-postgres";
import { eq, and } from "drizzle-orm";
import { z } from "zod";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";

// Schema definition
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  role: text("role", { enum: ["admin", "user", "guest"] }).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const posts = pgTable("posts", {
  id: uuid("id").primaryKey().defaultRandom(),
  title: text("title").notNull(),
  content: text("content").notNull(),
  published: boolean("published").default(false).notNull(),
  authorId: uuid("author_id").notNull().references(() => users.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Infer types from schema
type User = typeof users.$inferSelect;
type NewUser = typeof users.$inferInsert;

type Post = typeof posts.$inferSelect;
type NewPost = typeof posts.$inferInsert;

// Generate Zod schemas from Drizzle
const insertUserSchema = createInsertSchema(users, {
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

const selectUserSchema = createSelectSchema(users);

// Type-safe repository pattern
class UserRepository {
  constructor(private db: ReturnType<typeof drizzle>) {}

  async findById(id: string): Promise<User | null> {
    const [user] = await this.db
      .select()
      .from(users)
      .where(eq(users.id, id))
      .limit(1);

    return user ?? null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const [user] = await this.db
      .select()
      .from(users)
      .where(eq(users.email, email))
      .limit(1);

    return user ?? null;
  }

  async create(data: NewUser): Promise<User> {
    // Validate with Zod before insert
    const validated = insertUserSchema.parse(data);

    const [user] = await this.db
      .insert(users)
      .values(validated)
      .returning();

    return user!;
  }

  async update(id: string, data: Partial<NewUser>): Promise<User | null> {
    const [user] = await this.db
      .update(users)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(users.id, id))
      .returning();

    return user ?? null;
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.db
      .delete(users)
      .where(eq(users.id, id));

    return result.rowCount > 0;
  }

  // Complex query with joins
  async findWithPosts(id: string): Promise<(User & { posts: Post[] }) | null> {
    const user = await this.findById(id);
    if (!user) return null;

    const userPosts = await this.db
      .select()
      .from(posts)
      .where(eq(posts.authorId, id));

    return { ...user, posts: userPosts };
  }
}

// Transaction support
class PostService {
  constructor(
    private db: ReturnType<typeof drizzle>,
    private userRepo: UserRepository
  ) {}

  async createPost(
    authorId: string,
    data: Omit<NewPost, "authorId">
  ): AsyncResult<Post, Error> {
    try {
      return await this.db.transaction(async (tx) => {
        // Verify user exists
        const user = await this.userRepo.findById(authorId);
        if (!user) {
          return Err(new Error("User not found"));
        }

        const [post] = await tx
          .insert(posts)
          .values({ ...data, authorId })
          .returning();

        return Ok(post!);
      });
    } catch (error) {
      return Err(error instanceof Error ? error : new Error("Unknown error"));
    }
  }
}

// Usage
const db = drizzle(/* connection */);
const userRepo = new UserRepository(db);
const postService = new PostService(db, userRepo);

// Fully type-safe queries
const user = await userRepo.findById("123");
if (user) {
  console.log(user.name); // Type: string
  console.log(user.createdAt); // Type: Date
}

// Type-safe inserts
const newUser = await userRepo.create({
  name: "Alice",
  email: "alice@example.com",
  role: "user"
});

// Invalid data caught at compile-time
const invalid = await userRepo.create({
  name: "Bob",
  email: "invalid-email", // ✅ Compiles but Zod validation catches at runtime
  role: "superadmin" // ❌ Type error: role must be "admin" | "user" | "guest"
});
```

**Type Safety Benefits:**
- Schema-first development with generated types
- Compile-time query validation
- Runtime validation with Zod integration

**Common Mistakes:**
- ❌ Not using transactions for multi-step operations
- ❌ Bypassing Zod validation on user input
- ❌ Not handling database errors (constraints, unique violations)

**Best Practices:**
- Use repository pattern for testability
- Combine Drizzle types with Zod validation
- Implement soft deletes for audit trails
- Use database migrations for schema evolution

---

## 5. Framework Integration

### 5.1 Next.js App Router - Type-Safe Server Actions

**Complexity:** ⭐⭐⭐⭐
**Problem:** End-to-end type safety from client to server with validation

**Pattern:**
```typescript
// lib/safe-action.ts
import { createSafeActionClient } from "next-safe-action";
import { auth } from "@/lib/auth";

export const actionClient = createSafeActionClient({
  handleServerError(e) {
    console.error("Action error:", e.message);
    return "Something went wrong";
  },
});

// With authentication
export const authActionClient = actionClient.use(async ({ next }) => {
  const session = await auth();

  if (!session?.user) {
    throw new Error("Unauthorized");
  }

  return next({ ctx: { session, userId: session.user.id } });
});

// actions/create-post.ts
"use server";

import { z } from "zod";
import { authActionClient } from "@/lib/safe-action";
import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10).max(10000),
  published: z.boolean().default(false),
});

export const createPost = authActionClient
  .schema(createPostSchema)
  .action(async ({ parsedInput, ctx }) => {
    const post = await db.posts.create({
      data: {
        ...parsedInput,
        authorId: ctx.userId,
      },
    });

    revalidatePath("/posts");
    return { post };
  });

// Client component usage
"use client";

import { useAction } from "next-safe-action/hooks";
import { createPost } from "@/actions/create-post";

export function CreatePostForm() {
  const { execute, status, result } = useAction(createPost);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    execute({
      title: formData.get("title") as string,
      content: formData.get("content") as string,
      published: formData.get("published") === "on",
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="title" required />
      <textarea name="content" required />
      <input type="checkbox" name="published" />

      <button type="submit" disabled={status === "executing"}>
        {status === "executing" ? "Creating..." : "Create Post"}
      </button>

      {result.data && <p>Post created: {result.data.post.id}</p>}
      {result.serverError && <p>Error: {result.serverError}</p>}
      {result.validationErrors && (
        <ul>
          {Object.entries(result.validationErrors).map(([field, errors]) => (
            <li key={field}>{field}: {errors?.join(", ")}</li>
          ))}
        </ul>
      )}
    </form>
  );
}

// Advanced: File upload action
"use server";

const uploadFileSchema = z.object({
  file: z.instanceof(File).refine(
    (file) => file.size <= 5 * 1024 * 1024,
    "File must be less than 5MB"
  ),
  folder: z.string().optional(),
});

export const uploadFile = authActionClient
  .schema(uploadFileSchema)
  .action(async ({ parsedInput, ctx }) => {
    const { file, folder } = parsedInput;

    const buffer = await file.arrayBuffer();
    const key = `${folder ?? "uploads"}/${ctx.userId}/${file.name}`;

    // Upload to S3/storage
    const url = await uploadToStorage(key, Buffer.from(buffer));

    return { url };
  });
```

**Type Safety Benefits:**
- Compile-time validation of action inputs/outputs
- Zod runtime validation
- Type-safe context (auth, sessions)

**Common Mistakes:**
- ❌ Not using `"use server"` directive
- ❌ Forgetting to revalidate cache after mutations
- ❌ Not handling loading/error states on client

**Best Practices:**
- Use next-safe-action for production apps
- Separate action logic from business logic
- Implement optimistic updates for better UX
- Use middleware for cross-cutting concerns (auth, logging)

---

### 5.2 React - Generic Components with TypeScript

**Complexity:** ⭐⭐⭐⭐
**Problem:** Reusable components that maintain type safety

**Pattern:**
```typescript
// Generic Table component
interface Column<T> {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
}

function Table<T extends Record<string, any>>({
  data,
  columns,
  onRowClick,
}: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)}>{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} onClick={() => onRowClick?.(row)}>
            {columns.map((col) => (
              <td key={String(col.key)}>
                {col.render ? col.render(row[col.key], row) : String(row[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage with full type inference
interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
}

const users: User[] = [
  { id: "1", name: "Alice", email: "alice@example.com", role: "admin" },
  { id: "2", name: "Bob", email: "bob@example.com", role: "user" },
];

function UserTable() {
  return (
    <Table
      data={users}
      columns={[
        { key: "name", header: "Name" },
        { key: "email", header: "Email" },
        {
          key: "role",
          header: "Role",
          render: (role) => (
            <span className={role === "admin" ? "text-red-500" : ""}>
              {role}
            </span>
          ),
        },
      ]}
      onRowClick={(user) => {
        console.log(user.name); // Fully typed!
      }}
    />
  );
}

// Advanced: Generic Form component with Zod
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

interface FormProps<T extends z.ZodType> {
  schema: T;
  onSubmit: (data: z.infer<T>) => void | Promise<void>;
  children: (props: {
    register: ReturnType<typeof useForm>["register"];
    errors: ReturnType<typeof useForm>["formState"]["errors"];
    isSubmitting: boolean;
  }) => React.ReactNode;
}

function Form<T extends z.ZodType>({
  schema,
  onSubmit,
  children,
}: FormProps<T>) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<z.infer<T>>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {children({ register, errors, isSubmitting })}
    </form>
  );
}

// Usage
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function LoginForm() {
  return (
    <Form
      schema={loginSchema}
      onSubmit={(data) => {
        // data is fully typed: { email: string; password: string }
        console.log(data.email);
      }}
    >
      {({ register, errors, isSubmitting }) => (
        <>
          <input {...register("email")} />
          {errors.email && <span>{errors.email.message}</span>}

          <input type="password" {...register("password")} />
          {errors.password && <span>{errors.password.message}</span>}

          <button type="submit" disabled={isSubmitting}>
            Login
          </button>
        </>
      )}
    </Form>
  );
}

// Generic Context Provider
interface ContextProviderProps<T> {
  value: T;
  children: React.ReactNode;
}

function createTypedContext<T>() {
  const Context = React.createContext<T | undefined>(undefined);

  function Provider({ value, children }: ContextProviderProps<T>) {
    return <Context.Provider value={value}>{children}</Context.Provider>;
  }

  function useContext() {
    const context = React.useContext(Context);
    if (context === undefined) {
      throw new Error("useContext must be used within Provider");
    }
    return context;
  }

  return { Provider, useContext };
}

// Usage
interface UserContext {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const { Provider: UserProvider, useContext: useUser } = createTypedContext<UserContext>();

function App() {
  const [user, setUser] = React.useState<User | null>(null);

  const contextValue: UserContext = {
    user,
    login: async (email, password) => {
      // Implementation
      const user = await loginApi(email, password);
      setUser(user);
    },
    logout: () => setUser(null),
  };

  return (
    <UserProvider value={contextValue}>
      <AppContent />
    </UserProvider>
  );
}

function AppContent() {
  const { user, logout } = useUser(); // Fully typed!

  if (!user) {
    return <LoginForm />;
  }

  return (
    <div>
      <p>Welcome, {user.name}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

**Type Safety Benefits:**
- Generic components maintain full type inference
- Compile-time prop validation
- Type-safe render props and callbacks

**Common Mistakes:**
- ❌ Using `any` for generic constraints (loses type safety)
- ❌ Not constraining generics (allows invalid types)
- ❌ Over-engineering simple components with generics

**Best Practices:**
- Use generics for truly reusable components
- Constrain generics with `extends` for better errors
- Combine with Zod for runtime validation
- Export helper functions alongside generic components

---

## 6. Best Practices & Anti-Patterns

### 6.1 Compiler Configuration Best Practices

**tsconfig.json 2025 Baseline:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

**Key Options:**
- `noUncheckedIndexedAccess`: Forces null checks on array/object access (prevents runtime errors)
- `exactOptionalPropertyTypes`: Distinguishes `undefined` from missing properties
- `verbatimModuleSyntax`: Enforces explicit `type` imports (ESM compatibility)
- `isolatedModules`: Required for bundlers (Vite, esbuild)

---

### 6.2 Anti-Patterns to Avoid

**❌ Using `any` instead of `unknown`:**
```typescript
// BAD
function processData(data: any) {
  return data.value; // No type safety
}

// GOOD
function processData(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as { value: unknown }).value;
  }
  throw new Error("Invalid data");
}
```

**❌ Type assertions without validation:**
```typescript
// BAD
const user = response.json() as User; // No runtime check!

// GOOD
const user = UserSchema.parse(response.json()); // Runtime validation
```

**❌ Disabling strict mode:**
```typescript
// BAD
{
  "compilerOptions": {
    "strict": false // ❌ Loses all type safety
  }
}

// GOOD
{
  "compilerOptions": {
    "strict": true, // ✅ Full type safety
    "skipLibCheck": true // Only skip checking node_modules
  }
}
```

**❌ Index access without null checks:**
```typescript
// BAD (without noUncheckedIndexedAccess)
const first = array[0]; // Type: T (but could be undefined!)
const value = obj[key]; // Type: V (but could be undefined!)

// GOOD (with noUncheckedIndexedAccess)
const first = array[0]; // Type: T | undefined
if (first) {
  // Type narrowed to T
  console.log(first);
}
```

---

### 6.3 Migration Patterns from JavaScript

**Gradual Adoption Strategy:**

1. **Add TypeScript with `allowJs`:**
```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,
    "strict": false
  }
}
```

2. **Enable `checkJs` for JSDoc:**
```javascript
/**
 * @param {string} name
 * @param {number} age
 * @returns {{ name: string; age: number }}
 */
function createUser(name, age) {
  return { name, age };
}
```

3. **Convert file-by-file:**
```bash
# Rename .js → .ts
mv file.js file.ts

# Fix type errors incrementally
```

4. **Enable strict mode:**
```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

---

## Summary

This research document compiles **moderate to advanced TypeScript patterns** from the `claude-mpm-skills` repository, focusing on:

1. **Advanced Type System**: Conditional types, `infer` keyword, template literals, recursive types, mapped types, and branded types
2. **Generic Programming**: Generic constraints, variadic tuples, and factory patterns
3. **Design Patterns**: Observer/PubSub, state machines, Result types
4. **API & Data Handling**: Type-safe API clients with Zod, database layers with Drizzle
5. **Framework Integration**: Next.js Server Actions, React generic components

**Key Takeaways:**
- Combine compile-time type safety with runtime validation (Zod, TypeBox, Valibot)
- Use branded types for domain-critical values
- Leverage discriminated unions for state management
- Prefer `unknown` over `any` for truly unknown types
- Enable strict compiler options (`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`)

**Resources Analyzed:**
- `/toolchains/typescript/core/SKILL.md`
- `/toolchains/typescript/core/references/advanced-types.md`
- `/toolchains/typescript/core/references/runtime-validation.md`
- `/toolchains/nextjs/core/references/server-actions.md`

**Complexity Levels:**
- ⭐⭐⭐ Moderate (conditional types, generics, patterns)
- ⭐⭐⭐⭐ Advanced (recursive types, state machines, API clients)
- ⭐⭐⭐⭐⭐ Expert (deep type-level programming, complex inference)
