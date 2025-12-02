# Advanced Rust Patterns: Moderate to Difficult Use Cases
**Research Date:** 2025-12-01
**Focus:** Ownership, Traits, Async, Error Handling, Type-Safe Design
**Complexity Level:** Moderate to Difficult

---

## Table of Contents
1. [Ownership & Borrowing Mastery](#1-ownership--borrowing-mastery)
2. [Trait System](#2-trait-system)
3. [Async/Concurrency](#3-asyncconcurrency)
4. [Error Handling](#4-error-handling)
5. [Type-Safe Design](#5-type-safe-design)

---

## 1. Ownership & Borrowing Mastery

### 1.1 Advanced Lifetime Patterns

**Pattern Name:** Explicit Lifetime Annotations with Multiple References
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Prevents dangling references, ensures memory safety

#### Problem Solved
When a method receives two references with potentially different lifetimes and returns a reference, the compiler needs explicit lifetime annotations to determine which input lifetime the output is tied to.

#### Code Example

```rust
struct ContentManager {
    content: String,
}

impl ContentManager {
    // Explicit lifetime annotation required
    fn get_content_or_default<'a, 'b>(
        &'a self,
        default: &'b str,
    ) -> &'a str
    where
        'b: 'a, // 'b must outlive 'a
    {
        if self.content.is_empty() {
            // Cannot return default here due to lifetime mismatch
            // This forces us to return from self
            &self.content
        } else {
            &self.content
        }
    }

    // Better pattern: return owned when necessary
    fn get_content_or_default_owned(&self, default: &str) -> String {
        if self.content.is_empty() {
            default.to_string()
        } else {
            self.content.clone()
        }
    }
}

// Advanced: Generic lifetime bounds with traits
trait Cache<'a, T> {
    fn get(&'a self, key: &str) -> Option<&'a T>;
}

struct MemoryCache<T> {
    data: std::collections::HashMap<String, T>,
}

impl<'a, T> Cache<'a, T> for MemoryCache<T> {
    fn get(&'a self, key: &str) -> Option<&'a T> {
        self.data.get(key)
    }
}
```

#### Lifetime Elision Rules

**Rule 1:** Each reference parameter gets its own lifetime
```rust
fn foo(x: &i32, y: &i32) // becomes
fn foo<'a, 'b>(x: &'a i32, y: &'b i32)
```

**Rule 2:** If there is one input lifetime, it's assigned to all outputs
```rust
fn process(input: &str) -> &str // becomes
fn process<'a>(input: &'a str) -> &'a str
```

**Rule 3:** If there are multiple input lifetimes but one is `&self`, the output gets `self`'s lifetime
```rust
impl Foo {
    fn method(&self, other: &str) -> &str // becomes
    fn method<'a, 'b>(&'a self, other: &'b str) -> &'a str
}
```

**When to Use:**
- When returning references from structs with multiple lifetime dependencies
- When elision rules cannot infer the correct lifetime relationship
- When building generic cache or reference-holding data structures

**Borrow Checker Issues Solved:**
- "borrowed value does not live long enough"
- "cannot infer an appropriate lifetime"
- "lifetime may not live long enough"

**Performance:** Zero-cost abstraction - lifetimes are compile-time only

---

### 1.2 Interior Mutability Patterns

**Pattern Name:** RefCell<T> and Cell<T> for Single-Threaded Interior Mutability
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Runtime borrow checking, single-threaded safety

#### Problem Solved
Allows mutation through shared references when the compiler cannot prove safety at compile time, enabling patterns like multiple owners with mutation or circular references.

#### Code Example

```rust
use std::cell::{Cell, RefCell};
use std::rc::Rc;

// Example 1: Graph with RefCell for interior mutability
#[derive(Debug)]
struct Node {
    value: i32,
    neighbors: RefCell<Vec<Rc<Node>>>,
}

impl Node {
    fn new(value: i32) -> Rc<Self> {
        Rc::new(Node {
            value,
            neighbors: RefCell::new(Vec::new()),
        })
    }

    fn add_neighbor(&self, neighbor: Rc<Node>) {
        // Mutate through shared reference
        self.neighbors.borrow_mut().push(neighbor);
    }

    fn neighbors_count(&self) -> usize {
        self.neighbors.borrow().len()
    }
}

// Example 2: Mock object pattern with RefCell
struct MockDatabase {
    call_count: RefCell<usize>,
    responses: RefCell<Vec<String>>,
}

impl MockDatabase {
    fn new() -> Self {
        MockDatabase {
            call_count: RefCell::new(0),
            responses: RefCell::new(Vec::new()),
        }
    }

    fn query(&self, _sql: &str) -> String {
        // Mutate call count through shared reference
        *self.call_count.borrow_mut() += 1;

        // Return mock response
        self.responses
            .borrow_mut()
            .pop()
            .unwrap_or_else(|| "default".to_string())
    }

    fn times_called(&self) -> usize {
        *self.call_count.borrow()
    }
}

// Example 3: Cell for Copy types
struct Metrics {
    request_count: Cell<u64>,
    error_count: Cell<u64>,
}

impl Metrics {
    fn new() -> Self {
        Metrics {
            request_count: Cell::new(0),
            error_count: Cell::new(0),
        }
    }

    fn record_request(&self) {
        // No borrow_mut needed for Cell
        self.request_count.set(self.request_count.get() + 1);
    }

    fn record_error(&self) {
        self.error_count.set(self.error_count.get() + 1);
    }
}
```

#### RefCell vs Cell vs Mutex

| Type | Thread Safety | Borrow Check | Copy Types Only | Runtime Cost |
|------|--------------|--------------|-----------------|--------------|
| `Cell<T>` | ❌ No | No borrowing | ✅ Yes | Lowest |
| `RefCell<T>` | ❌ No | ✅ Runtime | ❌ No | Low (runtime checks) |
| `Mutex<T>` | ✅ Yes | ✅ Runtime | ❌ No | Higher (locking) |

**When to Use:**
- **Cell<T>:** For Copy types (integers, booleans) that need mutation through shared references
- **RefCell<T>:** For non-Copy types in single-threaded scenarios (UI, tests, graphs)
- **Rc<RefCell<T>>:** Multiple ownership + interior mutability (graphs, trees)

**Borrow Checker Issues Solved:**
- "cannot borrow as mutable" when only shared reference available
- Circular reference patterns (with Weak to prevent leaks)
- Mock objects in tests that need mutation

**Performance:**
- Cell<T>: Zero overhead
- RefCell<T>: Small runtime cost for borrow tracking
- Panics at runtime if borrow rules violated

**Common Pitfall:**
```rust
// DANGER: This will panic!
let data = RefCell::new(vec![1, 2, 3]);
let borrow1 = data.borrow_mut(); // OK
let borrow2 = data.borrow_mut(); // PANIC: already borrowed
```

---

### 1.3 Smart Pointer Patterns: Arc<Mutex<T>> vs Arc<RwLock<T>>

**Pattern Name:** Thread-Safe Shared Ownership with Controlled Mutation
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Thread-safe sharing, prevents data races

#### Problem Solved
Enables multiple threads to share and mutate data safely, choosing the right synchronization primitive based on read/write ratio.

#### Code Example

```rust
use std::sync::{Arc, Mutex, RwLock};
use std::thread;
use std::time::Duration;

// Example 1: Arc<Mutex<T>> for balanced read/write
#[derive(Clone)]
struct Counter {
    value: Arc<Mutex<u64>>,
}

impl Counter {
    fn new() -> Self {
        Counter {
            value: Arc::new(Mutex::new(0)),
        }
    }

    fn increment(&self) {
        let mut val = self.value.lock().unwrap();
        *val += 1;
    }

    fn get(&self) -> u64 {
        *self.value.lock().unwrap()
    }
}

// Example 2: Arc<RwLock<T>> for read-heavy workloads
#[derive(Clone)]
struct Cache {
    data: Arc<RwLock<std::collections::HashMap<String, String>>>,
}

impl Cache {
    fn new() -> Self {
        Cache {
            data: Arc::new(RwLock::new(std::collections::HashMap::new())),
        }
    }

    // Many threads can read simultaneously
    fn get(&self, key: &str) -> Option<String> {
        let read_guard = self.data.read().unwrap();
        read_guard.get(key).cloned()
    }

    // Only one thread can write
    fn set(&self, key: String, value: String) {
        let mut write_guard = self.data.write().unwrap();
        write_guard.insert(key, value);
    }
}

// Example 3: Practical multi-threaded server pattern
struct Server {
    connections: Arc<RwLock<Vec<String>>>,
    stats: Arc<Mutex<ServerStats>>,
}

struct ServerStats {
    requests: u64,
    errors: u64,
}

impl Server {
    fn new() -> Self {
        Server {
            connections: Arc::new(RwLock::new(Vec::new())),
            stats: Arc::new(Mutex::new(ServerStats {
                requests: 0,
                errors: 0,
            })),
        }
    }

    fn add_connection(&self, conn: String) {
        let mut conns = self.connections.write().unwrap();
        conns.push(conn);
    }

    fn get_connection_count(&self) -> usize {
        // Read lock allows multiple concurrent reads
        self.connections.read().unwrap().len()
    }

    fn record_request(&self) {
        let mut stats = self.stats.lock().unwrap();
        stats.requests += 1;
    }

    fn spawn_workers(&self, count: usize) {
        for i in 0..count {
            let stats = Arc::clone(&self.stats);
            thread::spawn(move || {
                for _ in 0..100 {
                    let mut s = stats.lock().unwrap();
                    s.requests += 1;
                    thread::sleep(Duration::from_millis(10));
                }
            });
        }
    }
}
```

#### Performance Characteristics

**Mutex:**
- Consistent performance for reads and writes
- Lower overhead for single operation
- Better for write-heavy or balanced workloads
- No writer starvation

**RwLock:**
- Excellent for read-heavy workloads (90%+ reads)
- Higher overhead per operation
- Multiple concurrent readers
- Can suffer from writer starvation
- Performance degrades significantly with many writes

**Benchmark Results (typical):**
```
Workload: 90% reads, 10% writes
- Arc<Mutex<T>>:   ~500ns per operation
- Arc<RwLock<T>>:  ~100ns per operation (5x faster)

Workload: 50% reads, 50% writes
- Arc<Mutex<T>>:   ~500ns per operation
- Arc<RwLock<T>>:  ~600ns per operation (slower)
```

**When to Use:**

**Arc<Mutex<T>>:**
- Default choice for shared mutable state
- Balanced read/write ratio (>20% writes)
- Simple shared counters or flags
- When in doubt, start here

**Arc<RwLock<T>>:**
- Read-heavy workloads (>80% reads)
- Shared caches
- Configuration data that rarely changes
- Large data structures where read operations are expensive

**Arc<Atomic*>:**
- Simple atomic types (integers, booleans)
- Lock-free counters
- Highest performance for simple values

**Borrow Checker Issues Solved:**
- "cannot move out of shared reference"
- "cannot borrow as mutable in multiple threads"
- Data race prevention at compile time

**Common Pitfalls:**

```rust
// DEADLOCK: Don't lock multiple mutexes in different orders
let lock1 = mutex1.lock().unwrap();
let lock2 = mutex2.lock().unwrap(); // Thread A
// vs
let lock2 = mutex2.lock().unwrap();
let lock1 = mutex1.lock().unwrap(); // Thread B - DEADLOCK!

// POISON: Handle panics in locked sections
match mutex.lock() {
    Ok(guard) => { /* use guard */ },
    Err(poisoned) => {
        // Mutex poisoned due to panic while locked
        let guard = poisoned.into_inner(); // Recover if safe
    }
}
```

---

## 2. Trait System

### 2.1 Associated Types vs Generic Parameters

**Pattern Name:** Type Projection vs Parameterization
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Type-safe abstraction, prevents ambiguous implementations

#### Problem Solved
Distinguishes between traits that should have multiple implementations per type (generics) versus single canonical implementation (associated types).

#### Code Example

```rust
// GENERIC TYPE PARAMETER: Multiple implementations possible
trait From<T> {
    fn from(value: T) -> Self;
}

// Can implement From for many types
impl From<u8> for u32 {
    fn from(value: u8) -> u32 {
        value as u32
    }
}

impl From<u16> for u32 {
    fn from(value: u16) -> u32 {
        value as u32
    }
}

// ASSOCIATED TYPE: Only one implementation per type
trait Iterator {
    type Item; // Associated type

    fn next(&mut self) -> Option<Self::Item>;
}

// Counter can only iterate over one type
struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32; // Can't implement Iterator<String> for Counter

    fn next(&mut self) -> Option<Self::Item> {
        self.count += 1;
        Some(self.count)
    }
}

// Example: Choosing between approaches
// BAD: Iterator with generic would allow nonsense
trait BadIterator<T> {
    fn next(&mut self) -> Option<T>;
}

// This compiles but makes no sense:
// impl BadIterator<String> for Counter { ... }
// impl BadIterator<u32> for Counter { ... }
// Now counter.next() is ambiguous!

// Example: Conversion trait with associated type
trait TryParse {
    type Output;
    type Error;

    fn try_parse(s: &str) -> Result<Self::Output, Self::Error>;
}

struct JsonParser;

impl TryParse for JsonParser {
    type Output = serde_json::Value;
    type Error = serde_json::Error;

    fn try_parse(s: &str) -> Result<Self::Output, Self::Error> {
        serde_json::from_str(s)
    }
}

// Advanced: Generic + associated type combo
trait Graph {
    type Node;
    type Edge;

    fn neighbors(&self, node: &Self::Node) -> Vec<Self::Edge>;
}

trait GenericGraph<N, E> {
    fn neighbors(&self, node: &N) -> Vec<E>;
}

// Associated types better: each graph has one node/edge type
// Generic would allow Graph<String, i32> AND Graph<u32, String> for same type
```

#### Decision Matrix

| Use Associated Types When | Use Generic Parameters When |
|---------------------------|----------------------------|
| ✅ Only one logical implementation per type | ✅ Multiple implementations make sense |
| ✅ Output type determined by input type | ✅ Caller chooses the type |
| ✅ Trait represents identity/capability | ✅ Trait represents conversion/transformation |
| Example: `Iterator::Item` | Example: `From<T>` |
| Example: `Deref::Target` | Example: `Add<Rhs>` |

**When to Use:**
- **Associated Types:** Iterator, Deref, Future (one obvious output type)
- **Generic Parameters:** From/Into, Add/Sub (multiple conversions make sense)

**Borrow Checker Issues Solved:**
- Prevents ambiguous type inference
- Enforces "one true implementation" at type level
- Cleaner APIs without turbofish (`::<>`) syntax

**Performance:** Zero-cost - both approaches are compile-time only

---

### 2.2 Trait Objects (dyn Trait)

**Pattern Name:** Dynamic Dispatch with Type Erasure
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Object-safe traits, runtime polymorphism

#### Problem Solved
Enables heterogeneous collections and runtime polymorphism when concrete types aren't known at compile time.

#### Code Example

```rust
// Example 1: Object-safe trait for plugin system
trait Plugin: Send + Sync {
    fn name(&self) -> &str;
    fn execute(&self, input: &str) -> String;
}

struct UppercasePlugin;
impl Plugin for UppercasePlugin {
    fn name(&self) -> &str { "uppercase" }
    fn execute(&self, input: &str) -> String {
        input.to_uppercase()
    }
}

struct ReversePlugin;
impl Plugin for ReversePlugin {
    fn name(&self) -> &str { "reverse" }
    fn execute(&self, input: &str) -> String {
        input.chars().rev().collect()
    }
}

struct PluginManager {
    plugins: Vec<Box<dyn Plugin>>,
}

impl PluginManager {
    fn new() -> Self {
        PluginManager { plugins: Vec::new() }
    }

    fn register(&mut self, plugin: Box<dyn Plugin>) {
        self.plugins.push(plugin);
    }

    fn execute_all(&self, input: &str) -> Vec<String> {
        self.plugins
            .iter()
            .map(|p| p.execute(input))
            .collect()
    }
}

// Example 2: GUI rendering with trait objects
trait Drawable {
    fn draw(&self, canvas: &mut Canvas);
    fn bounds(&self) -> Rectangle;
}

struct Circle { x: f64, y: f64, radius: f64 }
struct Rectangle { x: f64, y: f64, width: f64, height: f64 }

impl Drawable for Circle {
    fn draw(&self, canvas: &mut Canvas) {
        canvas.draw_circle(self.x, self.y, self.radius);
    }
    fn bounds(&self) -> Rectangle {
        Rectangle {
            x: self.x - self.radius,
            y: self.y - self.radius,
            width: self.radius * 2.0,
            height: self.radius * 2.0,
        }
    }
}

struct Scene {
    objects: Vec<Box<dyn Drawable>>,
}

impl Scene {
    fn render(&self, canvas: &mut Canvas) {
        for obj in &self.objects {
            obj.draw(canvas); // Dynamic dispatch
        }
    }
}

// Example 3: Object-safe vs NOT object-safe
// OBJECT-SAFE ✅
trait Logger {
    fn log(&self, message: &str);
}

// NOT OBJECT-SAFE ❌
trait BadTrait {
    fn generic_method<T>(&self, value: T); // ❌ Generic methods
    fn returns_self() -> Self; // ❌ Returns Self
    fn sized_bound(&self) where Self: Sized; // ❌ Sized bound
}

// Can't do: Box<dyn BadTrait> - Compile error!

// Example 4: Trait object with lifetime bounds
trait Handler<'a> {
    fn handle(&self, data: &'a str) -> String;
}

struct Processor {
    handlers: Vec<Box<dyn for<'a> Handler<'a>>>, // Higher-rank trait bound
}
```

#### Object Safety Rules

A trait is **object-safe** if:
1. ✅ No generic methods
2. ✅ No associated functions that return `Self`
3. ✅ No `Self: Sized` bounds
4. ✅ Methods use `&self`, `&mut self`, or `Box<Self>`

**Static vs Dynamic Dispatch:**

```rust
// Static dispatch (monomorphization)
fn process_static<T: Plugin>(plugin: &T, input: &str) -> String {
    plugin.execute(input) // Inlined, fast, larger binary
}

// Dynamic dispatch (vtable)
fn process_dynamic(plugin: &dyn Plugin, input: &str) -> String {
    plugin.execute(input) // Pointer indirection, smaller binary
}
```

**Performance Characteristics:**

| Aspect | Static Dispatch | Dynamic Dispatch |
|--------|----------------|------------------|
| Call overhead | None (inlined) | Vtable lookup |
| Binary size | Larger (copies) | Smaller |
| Flexibility | Compile-time only | Runtime composition |
| Speed | Faster (~2-3ns) | Slower (~5-7ns) |

**When to Use:**
- Heterogeneous collections (different types in same Vec)
- Plugin systems
- Dependency injection
- GUI frameworks
- When you can't know types at compile time

**Alternatives:**
- Enum dispatch (faster, but closed set of types)
- Generic parameters (fastest, but monomorphizes)

---

### 2.3 Newtype Pattern and Orphan Rule

**Pattern Name:** Type Wrapper for Trait Implementation
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Orphan rule compliance, type safety

#### Problem Solved
Allows implementing foreign traits on foreign types by wrapping them in a local newtype, bypassing the orphan rule while maintaining type safety.

#### Code Example

```rust
use std::fmt;

// PROBLEM: Can't implement foreign trait on foreign type
// impl fmt::Display for Vec<i32> {} // ❌ Orphan rule violation!

// SOLUTION: Newtype pattern
struct MyVec(Vec<i32>);

impl fmt::Display for MyVec {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[")?;
        for (i, item) in self.0.iter().enumerate() {
            if i > 0 { write!(f, ", ")?; }
            write!(f, "{}", item)?;
        }
        write!(f, "]")
    }
}

// Example 2: Deref for transparent access
use std::ops::Deref;

impl Deref for MyVec {
    type Target = Vec<i32>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// Now MyVec can use Vec methods!
let mut vec = MyVec(vec![1, 2, 3]);
vec.push(4); // Works via Deref coercion

// Example 3: Stronger type safety with newtype
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct UserId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct PostId(u64);

fn get_user(id: UserId) -> User { /* ... */ }
fn get_post(id: PostId) -> Post { /* ... */ }

// Type safety prevents bugs:
let user_id = UserId(42);
let post_id = PostId(42);

get_user(user_id); // ✅ OK
// get_user(post_id); // ❌ Compile error!

// Example 4: Zero-cost newtype with transparent representation
#[repr(transparent)]
struct Meters(f64);

impl Meters {
    fn to_feet(&self) -> f64 {
        self.0 * 3.28084
    }
}

// Example 5: Implementing standard traits for ergonomics
impl From<Vec<i32>> for MyVec {
    fn from(vec: Vec<i32>) -> Self {
        MyVec(vec)
    }
}

impl From<MyVec> for Vec<i32> {
    fn from(wrapper: MyVec) -> Self {
        wrapper.0
    }
}

// Now conversions are easy
let vec = vec![1, 2, 3];
let my_vec: MyVec = vec.into();
let back: Vec<i32> = my_vec.into();
```

#### Orphan Rule Explained

**Rule:** You can implement a trait for a type only if either:
- The trait is defined in your crate, OR
- The type is defined in your crate

**Examples:**

```rust
// ✅ ALLOWED: Our trait, foreign type
trait MyTrait {}
impl MyTrait for Vec<i32> {}

// ✅ ALLOWED: Foreign trait, our type
struct MyType;
impl std::fmt::Display for MyType { /* ... */ }

// ❌ FORBIDDEN: Foreign trait, foreign type
// impl std::fmt::Display for Vec<i32> {} // Orphan rule!

// ✅ WORKAROUND: Newtype pattern
struct Wrapper(Vec<i32>);
impl std::fmt::Display for Wrapper { /* ... */ }
```

**When to Use:**
- Implementing foreign traits on foreign types
- Type-safe wrappers (UserId vs raw integers)
- Domain modeling with stronger types
- Adding trait implementations to external types

**Performance:**
- `#[repr(transparent)]` guarantees zero-cost
- Deref coercion provides transparent access
- No runtime overhead

---

### 2.4 Blanket Implementations

**Pattern Name:** Generic Trait Implementation for All Matching Types
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Coherence, automatic implementations

#### Problem Solved
Provides automatic trait implementations for any type that satisfies certain constraints, reducing code duplication and enabling powerful abstractions.

#### Code Example

```rust
// Example 1: Classic From/Into blanket implementation
// From standard library:
impl<T, U> Into<U> for T
where
    U: From<T>,
{
    fn into(self) -> U {
        U::from(self)
    }
}

// This means: implement From, get Into for free!
struct Meters(f64);
struct Feet(f64);

impl From<Meters> for Feet {
    fn from(m: Meters) -> Feet {
        Feet(m.0 * 3.28084)
    }
}

// Automatically available:
let meters = Meters(10.0);
let feet: Feet = meters.into(); // Works via blanket impl!

// Example 2: Custom blanket implementation
trait ToJson {
    fn to_json(&self) -> String;
}

// Blanket impl for all types that implement Display
impl<T: std::fmt::Display> ToJson for T {
    fn to_json(&self) -> String {
        format!("\"{}\"", self)
    }
}

// Now all Display types get to_json for free
let num = 42;
println!("{}", num.to_json()); // "42"

// Example 3: Reference blanket implementations
trait Processable {
    fn process(&self) -> String;
}

struct Data(String);

impl Processable for Data {
    fn process(&self) -> String {
        self.0.to_uppercase()
    }
}

// Blanket impl for references
impl<T: Processable> Processable for &T {
    fn process(&self) -> String {
        (*self).process()
    }
}

// Blanket impl for boxes
impl<T: Processable> Processable for Box<T> {
    fn process(&self) -> String {
        (**self).process()
    }
}

// Example 4: Advanced - conditional blanket implementation
trait Summarize {
    fn summarize(&self) -> String;
}

// Only implement for types that are Debug + Clone
impl<T> Summarize for T
where
    T: std::fmt::Debug + Clone,
{
    fn summarize(&self) -> String {
        format!("{:?}", self)
    }
}

// Example 5: Coherence rules prevent conflicts
trait MyTrait {
    fn do_thing(&self);
}

// ❌ CONFLICT: Can't have overlapping blanket impls
// impl<T> MyTrait for T { ... }
// impl<T: Clone> MyTrait for T { ... } // Compile error!

// ✅ OK: Non-overlapping implementations
impl MyTrait for i32 { /* ... */ }
impl MyTrait for String { /* ... */ }
```

#### Coherence Rules

**Rust enforces coherence:** For any trait + type combination, there must be **at most one** implementation.

**Key Rules:**
1. No two blanket implementations may overlap
2. Specific implementations override blanket implementations
3. Foreign trait + foreign type = can't implement (orphan rule)

**Common Blanket Implementation Patterns:**

```rust
// Pattern 1: Implement for references
impl<T: MyTrait + ?Sized> MyTrait for &T { /* ... */ }
impl<T: MyTrait + ?Sized> MyTrait for &mut T { /* ... */ }
impl<T: MyTrait + ?Sized> MyTrait for Box<T> { /* ... */ }

// Pattern 2: Error conversion
impl<T, E> From<E> for Result<T, E> {
    fn from(err: E) -> Self {
        Err(err)
    }
}

// Pattern 3: Optional conversion
impl<T> From<T> for Option<T> {
    fn from(val: T) -> Self {
        Some(val)
    }
}
```

**When to Use:**
- Automatic trait propagation (From → Into)
- Implementing for reference types (&T, &mut T, Box<T>)
- Generic conversions and utilities
- Framework-level abstractions

**Performance:** Zero-cost - resolved at compile time

---

## 3. Async/Concurrency

### 3.1 Tokio Runtime Patterns

**Pattern Name:** Async Runtime Management and Task Spawning
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Send + Sync enforcement, structured concurrency

#### Problem Solved
Provides efficient cooperative multitasking for I/O-bound operations with proper async/await patterns and runtime management.

#### Code Example

```rust
use tokio::runtime::Runtime;
use tokio::task;
use std::time::Duration;

// Example 1: Different runtime configurations
fn main() {
    // Multi-threaded runtime (default)
    let rt = Runtime::new().unwrap();

    rt.block_on(async {
        println!("Running on multi-threaded runtime");
    });

    // Current thread runtime (single-threaded)
    let rt = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    rt.block_on(async {
        println!("Single-threaded runtime");
    });

    // Custom configured runtime
    let rt = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .thread_name("my-pool")
        .thread_stack_size(3 * 1024 * 1024)
        .enable_all()
        .build()
        .unwrap();
}

// Example 2: Task spawning patterns
#[tokio::main]
async fn main() {
    // Spawn tasks with JoinHandle
    let handle1 = task::spawn(async {
        tokio::time::sleep(Duration::from_secs(1)).await;
        "task 1 complete"
    });

    let handle2 = task::spawn(async {
        tokio::time::sleep(Duration::from_secs(2)).await;
        "task 2 complete"
    });

    // Wait for both
    let (result1, result2) = tokio::join!(handle1, handle2);
    println!("{:?}, {:?}", result1, result2);
}

// Example 3: Blocking task pattern
#[tokio::main]
async fn main() {
    // DON'T block the async runtime
    // ❌ task::spawn(async { std::thread::sleep(...) }); // Blocks thread!

    // ✅ Use spawn_blocking for CPU-intensive work
    let result = task::spawn_blocking(|| {
        // This runs on a dedicated thread pool
        expensive_cpu_work()
    }).await.unwrap();

    println!("Result: {}", result);
}

fn expensive_cpu_work() -> u64 {
    (0..1_000_000).sum()
}

// Example 4: Practical async server pattern
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("Server listening on port 8080");

    loop {
        let (mut socket, addr) = listener.accept().await?;

        // Spawn a task per connection
        task::spawn(async move {
            let mut buf = [0; 1024];

            match socket.read(&mut buf).await {
                Ok(n) if n == 0 => return, // Connection closed
                Ok(n) => {
                    // Echo back
                    if let Err(e) = socket.write_all(&buf[0..n]).await {
                        eprintln!("Failed to write to {}: {}", addr, e);
                    }
                }
                Err(e) => {
                    eprintln!("Failed to read from {}: {}", addr, e);
                }
            }
        });
    }
}

// Example 5: JoinSet for dynamic task collection
use tokio::task::JoinSet;

#[tokio::main]
async fn main() {
    let mut set = JoinSet::new();

    // Dynamically spawn tasks
    for i in 0..10 {
        set.spawn(async move {
            tokio::time::sleep(Duration::from_millis(i * 100)).await;
            i * 2
        });
    }

    // Collect results as they complete
    while let Some(res) = set.join_next().await {
        match res {
            Ok(value) => println!("Task completed: {}", value),
            Err(e) => eprintln!("Task failed: {}", e),
        }
    }
}
```

#### Runtime Selection Guide

| Runtime Type | Use Case | Thread Count | Overhead |
|--------------|----------|--------------|----------|
| `#[tokio::main]` | Default choice | CPU count | Medium |
| `new_multi_thread()` | High concurrency | Configurable | Medium |
| `new_current_thread()` | Tests, simple apps | 1 | Low |
| `spawn_blocking()` | CPU-bound work | Dedicated pool | Higher |

**When to Use:**
- **Multi-threaded:** I/O-bound servers, network apps
- **Current thread:** Tests, single-threaded environments, WASM
- **spawn_blocking:** File I/O, CPU-intensive computation, synchronous APIs

**Performance Characteristics:**
- Task spawning: ~1-2μs overhead
- Context switching: ~50-100ns
- Much lighter than OS threads (can spawn 100k+ tasks)

---

### 3.2 Graceful Shutdown Patterns

**Pattern Name:** Coordinated Async Task Termination
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** No data loss, clean resource cleanup

#### Problem Solved
Coordinates shutdown of multiple async tasks, ensures cleanup operations complete, and prevents data loss during application termination.

#### Code Example

```rust
use tokio::signal;
use tokio::sync::broadcast;
use tokio_util::sync::CancellationToken;
use std::time::Duration;

// Example 1: Signal-based shutdown
#[tokio::main]
async fn main() {
    let (shutdown_tx, mut shutdown_rx) = broadcast::channel(1);

    // Spawn worker tasks
    for i in 0..5 {
        let mut shutdown = shutdown_tx.subscribe();
        tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = shutdown.recv() => {
                        println!("Worker {} shutting down gracefully", i);
                        // Cleanup operations
                        tokio::time::sleep(Duration::from_millis(100)).await;
                        println!("Worker {} finished cleanup", i);
                        break;
                    }
                    _ = tokio::time::sleep(Duration::from_secs(1)) => {
                        println!("Worker {} doing work", i);
                    }
                }
            }
        });
    }

    // Wait for shutdown signal
    signal::ctrl_c().await.expect("Failed to listen for Ctrl+C");
    println!("Shutdown signal received");

    // Send shutdown signal to all workers
    let _ = shutdown_tx.send(());

    // Wait a bit for cleanup
    tokio::time::sleep(Duration::from_millis(500)).await;
    println!("Application terminated");
}

// Example 2: CancellationToken pattern (recommended)
#[tokio::main]
async fn main() {
    let token = CancellationToken::new();

    // Spawn workers with cloned tokens
    let mut handles = vec![];
    for i in 0..5 {
        let token = token.clone();
        let handle = tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = token.cancelled() => {
                        println!("Worker {} received shutdown", i);
                        // Perform cleanup
                        flush_data(i).await;
                        break;
                    }
                    _ = tokio::time::sleep(Duration::from_secs(1)) => {
                        println!("Worker {} processing", i);
                    }
                }
            }
        });
        handles.push(handle);
    }

    // Wait for signal
    signal::ctrl_c().await.unwrap();
    println!("Initiating graceful shutdown...");

    // Cancel all tasks
    token.cancel();

    // Wait for all workers to finish
    for handle in handles {
        let _ = handle.await;
    }

    println!("All workers shut down cleanly");
}

async fn flush_data(worker_id: usize) {
    tokio::time::sleep(Duration::from_millis(100)).await;
    println!("Worker {} flushed data", worker_id);
}

// Example 3: TaskTracker pattern
use tokio_util::task::TaskTracker;

#[tokio::main]
async fn main() {
    let tracker = TaskTracker::new();

    // Spawn tracked tasks
    for i in 0..10 {
        tracker.spawn(async move {
            tokio::time::sleep(Duration::from_secs(i)).await;
            println!("Task {} completed", i);
        });
    }

    // Close tracker (no new tasks)
    tracker.close();

    // Wait for all tasks
    tracker.wait().await;
    println!("All tasks completed");
}

// Example 4: Complete server with graceful shutdown
use tokio::net::TcpListener;
use tokio::sync::Notify;
use std::sync::Arc;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    let shutdown = Arc::new(Notify::new());

    // Spawn signal handler
    let shutdown_clone = shutdown.clone();
    tokio::spawn(async move {
        signal::ctrl_c().await.expect("Failed to listen for Ctrl+C");
        println!("Shutdown signal received");
        shutdown_clone.notify_waiters();
    });

    let tracker = TaskTracker::new();

    loop {
        tokio::select! {
            // Accept new connections
            result = listener.accept() => {
                let (socket, addr) = result?;
                println!("New connection from {}", addr);

                let shutdown = shutdown.clone();
                tracker.spawn(async move {
                    handle_connection(socket, shutdown).await;
                });
            }

            // Shutdown signal
            _ = shutdown.notified() => {
                println!("No longer accepting connections");
                break;
            }
        }
    }

    // Close tracker and wait for active connections
    tracker.close();
    println!("Waiting for {} active connections...", tracker.len());
    tracker.wait().await;

    println!("All connections closed. Goodbye!");
    Ok(())
}

use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

async fn handle_connection(mut socket: TcpStream, shutdown: Arc<Notify>) {
    let mut buf = [0; 1024];

    loop {
        tokio::select! {
            // Read from socket
            result = socket.read(&mut buf) => {
                match result {
                    Ok(0) => break, // Connection closed
                    Ok(n) => {
                        if socket.write_all(&buf[0..n]).await.is_err() {
                            break;
                        }
                    }
                    Err(_) => break,
                }
            }

            // Shutdown notification
            _ = shutdown.notified() => {
                println!("Connection closing due to shutdown");
                let _ = socket.write_all(b"Server shutting down\n").await;
                break;
            }
        }
    }
}
```

#### Shutdown Pattern Comparison

| Pattern | Complexity | Use Case | Cleanup Support |
|---------|-----------|----------|-----------------|
| `broadcast::channel` | Medium | Simple broadcast | ✅ Yes |
| `CancellationToken` | Low | Recommended default | ✅ Yes |
| `Notify` | Low | Single signal | ✅ Yes |
| `TaskTracker` | Medium | Wait for all tasks | ✅ Yes |

**Best Practices:**

1. **Always handle signals:**
```rust
tokio::select! {
    _ = signal::ctrl_c() => { /* shutdown */ }
    _ = signal::unix::signal(SignalKind::terminate()).unwrap().recv() => { /* shutdown */ }
}
```

2. **Use timeouts for cleanup:**
```rust
tokio::select! {
    _ = cleanup_task() => { /* finished */ }
    _ = tokio::time::sleep(Duration::from_secs(30)) => {
        eprintln!("Cleanup timeout, forcing shutdown");
    }
}
```

3. **Prefer CancellationToken** for most use cases (lightest weight, composable)

**When to Use:**
- Long-running servers
- Background workers
- Data processing pipelines
- Any application with cleanup requirements

**Common Pitfalls:**
```rust
// ❌ BAD: Doesn't wait for cleanup
token.cancel();
// Tasks still running!

// ✅ GOOD: Wait for tasks
token.cancel();
for handle in handles {
    handle.await?;
}
```

---

### 3.3 Channel Patterns

**Pattern Name:** Async Communication Primitives
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Thread-safe message passing, no data races

#### Problem Solved
Enables safe communication between async tasks with different concurrency patterns (one-to-one, many-to-one, many-to-many).

#### Code Example

```rust
use tokio::sync::{mpsc, oneshot, broadcast};
use std::time::Duration;

// Example 1: MPSC (Multi-Producer, Single-Consumer)
#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32); // Buffer size 32

    // Spawn multiple producers
    for i in 0..5 {
        let tx = tx.clone();
        tokio::spawn(async move {
            for j in 0..3 {
                tx.send(format!("Message {} from worker {}", j, i))
                    .await
                    .unwrap();
                tokio::time::sleep(Duration::from_millis(100)).await;
            }
        });
    }

    // Drop original sender so receiver can complete
    drop(tx);

    // Single consumer
    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}

// Example 2: Oneshot (Request-Response Pattern)
#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel();

    // Spawn worker
    tokio::spawn(async move {
        let result = expensive_computation().await;
        let _ = tx.send(result); // Send result back
    });

    // Wait for result
    match rx.await {
        Ok(result) => println!("Got result: {}", result),
        Err(_) => println!("Worker died"),
    }
}

async fn expensive_computation() -> u64 {
    tokio::time::sleep(Duration::from_secs(1)).await;
    42
}

// Example 3: Broadcast (Multi-Producer, Multi-Consumer)
#[tokio::main]
async fn main() {
    let (tx, _rx) = broadcast::channel(16);

    // Spawn multiple consumers
    for i in 0..3 {
        let mut rx = tx.subscribe();
        tokio::spawn(async move {
            while let Ok(msg) = rx.recv().await {
                println!("Consumer {} received: {}", i, msg);
            }
        });
    }

    // Send messages (all consumers receive)
    for i in 0..5 {
        tx.send(format!("Broadcast {}", i)).unwrap();
        tokio::time::sleep(Duration::from_millis(100)).await;
    }
}

// Example 4: Command Pattern (mpsc + oneshot)
enum Command {
    Get { key: String, resp: oneshot::Sender<Option<String>> },
    Set { key: String, value: String, resp: oneshot::Sender<()> },
}

struct Cache {
    rx: mpsc::Receiver<Command>,
    data: std::collections::HashMap<String, String>,
}

impl Cache {
    fn new() -> (CacheHandle, Self) {
        let (tx, rx) = mpsc::channel(32);
        let cache = Cache {
            rx,
            data: std::collections::HashMap::new(),
        };
        (CacheHandle { tx }, cache)
    }

    async fn run(mut self) {
        while let Some(cmd) = self.rx.recv().await {
            match cmd {
                Command::Get { key, resp } => {
                    let value = self.data.get(&key).cloned();
                    let _ = resp.send(value);
                }
                Command::Set { key, value, resp } => {
                    self.data.insert(key, value);
                    let _ = resp.send(());
                }
            }
        }
    }
}

#[derive(Clone)]
struct CacheHandle {
    tx: mpsc::Sender<Command>,
}

impl CacheHandle {
    async fn get(&self, key: String) -> Option<String> {
        let (tx, rx) = oneshot::channel();
        self.tx.send(Command::Get { key, resp: tx }).await.ok()?;
        rx.await.ok()?
    }

    async fn set(&self, key: String, value: String) {
        let (tx, rx) = oneshot::channel();
        let _ = self.tx.send(Command::Set { key, value, resp: tx }).await;
        let _ = rx.await;
    }
}

#[tokio::main]
async fn main() {
    let (handle, cache) = Cache::new();

    // Spawn cache task
    tokio::spawn(cache.run());

    // Use cache from multiple tasks
    let h1 = handle.clone();
    tokio::spawn(async move {
        h1.set("key1".to_string(), "value1".to_string()).await;
    });

    let h2 = handle.clone();
    tokio::spawn(async move {
        if let Some(val) = h2.get("key1".to_string()).await {
            println!("Got value: {}", val);
        }
    });

    tokio::time::sleep(Duration::from_secs(1)).await;
}

// Example 5: Watch (Single-Producer, Multi-Consumer with Latest Value)
use tokio::sync::watch;

#[tokio::main]
async fn main() {
    let (tx, rx) = watch::channel("initial");

    // Spawn watchers
    for i in 0..3 {
        let mut rx = rx.clone();
        tokio::spawn(async move {
            while rx.changed().await.is_ok() {
                println!("Watcher {} saw: {}", i, *rx.borrow());
            }
        });
    }

    // Update value (only latest is kept)
    for i in 0..5 {
        tx.send(format!("value {}", i)).unwrap();
        tokio::time::sleep(Duration::from_millis(100)).await;
    }
}
```

#### Channel Type Selection Guide

| Channel | Producers | Consumers | Buffering | Use Case |
|---------|-----------|-----------|-----------|----------|
| `mpsc` | Many | One | Bounded/Unbounded | Task queue, event stream |
| `oneshot` | One | One | None | Request-response, futures |
| `broadcast` | Many | Many | Bounded | Pub/sub, notifications |
| `watch` | One | Many | Latest only | Configuration, state |

**Performance Characteristics:**

```
Operation costs (approximate):
- mpsc send:      ~50-100ns
- mpsc recv:      ~50-100ns
- oneshot send:   ~20-30ns
- broadcast send: ~100-150ns
- watch send:     ~30-50ns
```

**When to Use Each:**

**MPSC:**
- Background job queue
- Event processing pipeline
- Aggregating results from workers

**Oneshot:**
- Getting return value from spawned task
- Request-response within command pattern
- Futures that resolve once

**Broadcast:**
- Real-time notifications
- Pub/sub systems
- Event broadcasting to multiple listeners

**Watch:**
- Configuration changes
- Application state
- Only care about latest value

**Common Patterns:**

```rust
// Pattern 1: Bounded vs unbounded
let (tx, rx) = mpsc::channel(100);    // Bounded, backpressure
let (tx, rx) = mpsc::unbounded_channel(); // Unbounded, memory risk

// Pattern 2: Graceful close detection
while let Some(msg) = rx.recv().await {
    // Process msg
}
// All senders dropped, channel closed

// Pattern 3: Select multiple channels
tokio::select! {
    Some(msg) = rx1.recv() => { /* handle rx1 */ }
    Some(msg) = rx2.recv() => { /* handle rx2 */ }
    _ = shutdown.recv() => { /* shutdown */ }
}
```

---

## 4. Error Handling

### 4.1 thiserror vs anyhow

**Pattern Name:** Typed vs Dynamic Error Handling
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Type-safe error propagation, clear error contracts

#### Problem Solved
Provides ergonomic error handling with choice between typed errors (libraries) and flexible error aggregation (applications).

#### Code Example

```rust
// Example 1: thiserror for library code (typed errors)
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("Connection failed: {0}")]
    ConnectionFailed(String),

    #[error("Query error: {query}")]
    QueryError { query: String },

    #[error("Record not found with id: {id}")]
    NotFound { id: u64 },

    #[error(transparent)]
    IOError(#[from] std::io::Error),

    #[error(transparent)]
    ParseError(#[from] serde_json::Error),
}

pub fn execute_query(sql: &str) -> Result<Vec<String>, DatabaseError> {
    if sql.is_empty() {
        return Err(DatabaseError::QueryError {
            query: sql.to_string(),
        });
    }

    // Automatic conversion from io::Error via #[from]
    let _file = std::fs::read_to_string("config.json")?;

    Ok(vec!["result".to_string()])
}

// Callers can match on specific errors
fn handle_database() {
    match execute_query("SELECT * FROM users") {
        Ok(results) => println!("Got {} results", results.len()),
        Err(DatabaseError::NotFound { id }) => {
            eprintln!("ID {} not found", id);
        }
        Err(DatabaseError::ConnectionFailed(msg)) => {
            eprintln!("Connection issue: {}", msg);
        }
        Err(e) => eprintln!("Other error: {}", e),
    }
}

// Example 2: anyhow for application code (flexible errors)
use anyhow::{Context, Result, bail, ensure};

fn read_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;

    let config: Config = toml::from_str(&content)
        .context("Failed to parse config file")?;

    ensure!(config.port > 0, "Port must be positive");

    if !config.is_valid() {
        bail!("Invalid configuration");
    }

    Ok(config)
}

struct Config {
    port: u16,
    host: String,
}

impl Config {
    fn is_valid(&self) -> bool {
        !self.host.is_empty()
    }
}

// Example 3: Combining thiserror and anyhow
use anyhow::Result as AnyhowResult;

// Library code uses thiserror
mod database {
    use thiserror::Error;

    #[derive(Error, Debug)]
    pub enum Error {
        #[error("Connection timeout")]
        Timeout,

        #[error("Authentication failed")]
        AuthFailed,
    }

    pub fn connect() -> Result<Connection, Error> {
        Err(Error::Timeout)
    }

    pub struct Connection;
}

// Application code uses anyhow
fn main() -> AnyhowResult<()> {
    let conn = database::connect()
        .context("Failed to connect to database")?;

    // anyhow automatically wraps any error type
    let config = read_config()
        .context("Failed during startup")?;

    Ok(())
}

// Example 4: Custom error with source chain
#[derive(Error, Debug)]
pub enum AppError {
    #[error("Configuration error")]
    Config(#[from] ConfigError),

    #[error("Database error")]
    Database(#[from] DatabaseError),

    #[error("Network error")]
    Network(#[source] std::io::Error),
}

#[derive(Error, Debug)]
#[error("Invalid config: {message}")]
pub struct ConfigError {
    message: String,
}

// Example 5: Error downcasting with anyhow
use anyhow::Error as AnyhowError;

fn process() -> AnyhowResult<()> {
    let err = database::connect().map_err(AnyhowError::from)?;
    Ok(())
}

fn handle_error(err: AnyhowError) {
    // Downcast to specific error type
    if let Some(db_err) = err.downcast_ref::<DatabaseError>() {
        match db_err {
            DatabaseError::NotFound { id } => {
                println!("Record {} not found", id);
            }
            _ => {}
        }
    }

    // Print error chain
    eprintln!("Error: {:?}", err);
    for cause in err.chain() {
        eprintln!("  Caused by: {}", cause);
    }
}
```

#### thiserror vs anyhow Decision Matrix

| Feature | thiserror | anyhow |
|---------|-----------|--------|
| **Use in** | Libraries | Applications |
| **Type safety** | Strong | Dynamic |
| **Pattern matching** | ✅ Yes | ❌ Limited |
| **Context** | Manual | Built-in |
| **Boilerplate** | Low | Minimal |
| **Error chain** | Manual | Automatic |
| **Downcasting** | Not needed | Supported |

**When to Use:**

**thiserror:**
```rust
// ✅ Library public APIs
// ✅ When callers need to match on error variants
// ✅ When you want compile-time error handling
// ✅ Domain-specific error types

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("Not authorized")]
    Unauthorized,
}
```

**anyhow:**
```rust
// ✅ Application entry points
// ✅ When you just propagate errors
// ✅ When you need rich context
// ✅ CLI tools, scripts

fn main() -> Result<()> {
    let config = load_config()
        .context("Failed to load config")?;

    run_app(config)
        .context("Application error")?;

    Ok(())
}
```

**Best Practices:**

1. **Use both together:**
```rust
// Library exposes typed errors
pub mod db {
    #[derive(thiserror::Error, Debug)]
    pub enum Error { /* ... */ }
}

// Application uses anyhow for convenience
fn main() -> anyhow::Result<()> {
    db::connect()?; // Automatically wrapped
    Ok(())
}
```

2. **Add context aggressively:**
```rust
load_file("config.toml")
    .context("Failed to load config")
    .context("During initialization")?;
// Error: During initialization: Failed to load config: No such file
```

3. **Return errors, don't panic:**
```rust
// ❌ BAD
fn parse(s: &str) -> u32 {
    s.parse().unwrap() // Panic!
}

// ✅ GOOD
fn parse(s: &str) -> Result<u32> {
    Ok(s.parse()?)
}
```

**Performance:**
- Both have minimal overhead (~1-2 pointer indirections)
- anyhow uses type erasure (trait object)
- thiserror generates standard enum code

---

### 4.2 Result and Option Combinators

**Pattern Name:** Functional Error Handling
**Complexity:** ⭐⭐⭐ Moderate
**Safety Guarantees:** Explicit error handling, no null pointer exceptions

#### Problem Solved
Enables functional-style error and optional value handling without verbose pattern matching.

#### Code Example

```rust
// Example 1: Option combinators
fn find_user(id: u64) -> Option<User> {
    Some(User { id, name: "Alice".to_string() })
}

struct User {
    id: u64,
    name: String,
}

fn get_user_name(id: u64) -> Option<String> {
    // Chain operations with combinators
    find_user(id)
        .map(|user| user.name)           // Transform inner value
        .filter(|name| name.len() > 3)   // Keep only if predicate true
        .or(Some("Unknown".to_string())) // Provide default
}

// Example 2: Result combinators
fn parse_number(s: &str) -> Result<i32, std::num::ParseIntError> {
    s.parse::<i32>()
}

fn process_input(input: &str) -> Result<String, String> {
    parse_number(input)
        .map(|n| n * 2)                    // Transform success value
        .map_err(|e| e.to_string())        // Transform error
        .and_then(|n| {                    // Chain another Result
            if n > 100 {
                Ok(format!("Large: {}", n))
            } else {
                Err("Too small".to_string())
            }
        })
}

// Example 3: Comprehensive combinator examples
fn combinator_examples() {
    let x: Option<i32> = Some(5);

    // map: Transform inner value
    let doubled = x.map(|n| n * 2); // Some(10)

    // and_then (flatMap): Chain optional operations
    let result = x.and_then(|n| {
        if n > 3 { Some(n) } else { None }
    }); // Some(5)

    // or_else: Provide alternative computation
    let fallback = None.or_else(|| Some(42)); // Some(42)

    // unwrap_or: Provide default value
    let value = None.unwrap_or(0); // 0

    // unwrap_or_else: Lazy default computation
    let lazy = None.unwrap_or_else(|| expensive_default());

    // unwrap_or_default: Use Default trait
    let default: i32 = None.unwrap_or_default(); // 0

    // ok_or: Convert Option to Result
    let res: Result<i32, &str> = Some(5).ok_or("No value");

    // transpose: Swap Option<Result> to Result<Option>
    let opt_res: Option<Result<i32, String>> = Some(Ok(5));
    let res_opt: Result<Option<i32>, String> = opt_res.transpose();
}

fn expensive_default() -> i32 {
    42
}

// Example 4: Result combinators
fn result_combinators() {
    let x: Result<i32, &str> = Ok(5);

    // map: Transform success value
    let doubled = x.map(|n| n * 2); // Ok(10)

    // map_err: Transform error value
    let custom = Err("error").map_err(|e| format!("Failed: {}", e));

    // and_then: Chain Results
    let chained = Ok(5).and_then(|n| {
        if n > 3 { Ok(n * 2) } else { Err("too small") }
    });

    // or_else: Provide alternative Result
    let fallback = Err("error").or_else(|_| Ok(42));

    // unwrap_or: Extract or default
    let value = Err("error").unwrap_or(0);

    // expect: Unwrap with custom panic message
    // let value = x.expect("Failed to get value");
}

// Example 5: Real-world API processing
#[derive(Debug)]
struct ApiResponse {
    status: u16,
    body: String,
}

impl ApiResponse {
    fn parse_json<T: serde::de::DeserializeOwned>(&self) -> Result<T, serde_json::Error> {
        serde_json::from_str(&self.body)
    }
}

fn process_api_response(response: ApiResponse) -> Result<String, String> {
    // Chain multiple operations
    (response.status == 200)
        .then(|| response)                             // Convert bool to Option
        .ok_or("Bad status code".to_string())?        // Convert to Result
        .parse_json::<serde_json::Value>()             // Parse JSON
        .map_err(|e| format!("Parse error: {}", e))?   // Transform error
        .get("name")                                   // Get field
        .and_then(|v| v.as_str())                     // Convert to str
        .map(|s| s.to_string())                       // Convert to String
        .ok_or_else(|| "Missing name field".to_string()) // Handle missing
}

// Example 6: Option and Result interaction
fn get_config_value(key: &str) -> Option<String> {
    std::env::var(key).ok() // Result -> Option
}

fn parse_config_int(key: &str) -> Result<i32, String> {
    get_config_value(key)
        .ok_or_else(|| format!("Missing key: {}", key))?
        .parse()
        .map_err(|e| format!("Parse error: {}", e))
}

// Example 7: Collecting Results
fn process_batch(inputs: Vec<&str>) -> Result<Vec<i32>, String> {
    inputs
        .iter()
        .map(|s| s.parse::<i32>().map_err(|e| e.to_string()))
        .collect() // Collects Result<Vec<i32>, String>

    // Stops at first error and returns it
}

fn process_batch_partial(inputs: Vec<&str>) -> Vec<Result<i32, String>> {
    inputs
        .iter()
        .map(|s| s.parse::<i32>().map_err(|e| e.to_string()))
        .collect() // Keeps all results, including errors
}
```

#### Combinator Cheat Sheet

**Option Combinators:**

| Method | Signature | Use Case | Example |
|--------|-----------|----------|---------|
| `map` | `fn(Option<T>, T -> U) -> Option<U>` | Transform value | `Some(5).map(\|x\| x * 2)` |
| `and_then` | `fn(Option<T>, T -> Option<U>) -> Option<U>` | Chain optionals | `Some(5).and_then(\|x\| if x > 0 { Some(x) } else { None })` |
| `or_else` | `fn(Option<T>, () -> Option<T>) -> Option<T>` | Provide fallback | `None.or_else(\|\| Some(42))` |
| `unwrap_or` | `fn(Option<T>, T) -> T` | Default value | `None.unwrap_or(0)` |
| `filter` | `fn(Option<T>, T -> bool) -> Option<T>` | Keep if true | `Some(5).filter(\|x\| x > &3)` |
| `ok_or` | `fn(Option<T>, E) -> Result<T, E>` | Convert to Result | `Some(5).ok_or("error")` |

**Result Combinators:**

| Method | Signature | Use Case | Example |
|--------|-----------|----------|---------|
| `map` | `fn(Result<T,E>, T -> U) -> Result<U,E>` | Transform success | `Ok(5).map(\|x\| x * 2)` |
| `map_err` | `fn(Result<T,E>, E -> F) -> Result<T,F>` | Transform error | `Err("e").map_err(\|e\| format!("Error: {}", e))` |
| `and_then` | `fn(Result<T,E>, T -> Result<U,E>) -> Result<U,E>` | Chain results | `Ok(5).and_then(\|x\| Ok(x * 2))` |
| `or_else` | `fn(Result<T,E>, E -> Result<T,F>) -> Result<T,F>` | Fallback result | `Err("e").or_else(\|_\| Ok(42))` |
| `unwrap_or` | `fn(Result<T,E>, T) -> T` | Default value | `Err("e").unwrap_or(0)` |

**When to Use:**

- **Combinators:** Functional chains, pipeline processing
- **Pattern matching:** Complex branching, multiple cases
- **?operator:** Simple propagation in functions returning Result

**Performance:** Zero-cost - inlined to same code as pattern matching

---

## 5. Type-Safe Design

### 5.1 Type State Pattern

**Pattern Name:** Compile-Time State Machine
**Complexity:** ⭐⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Invalid state transitions prevented at compile time

#### Problem Solved
Encodes object state in the type system, making invalid state transitions impossible to compile, eliminating runtime state validation.

#### Code Example

```rust
use std::marker::PhantomData;

// Example 1: HTTP connection state machine
struct Disconnected;
struct Connected;
struct Authenticated;

struct HttpClient<State> {
    url: String,
    token: Option<String>,
    _state: PhantomData<State>,
}

// Only Disconnected state can connect
impl HttpClient<Disconnected> {
    fn new(url: String) -> Self {
        HttpClient {
            url,
            token: None,
            _state: PhantomData,
        }
    }

    fn connect(self) -> HttpClient<Connected> {
        println!("Connecting to {}", self.url);
        HttpClient {
            url: self.url,
            token: None,
            _state: PhantomData,
        }
    }
}

// Only Connected state can authenticate
impl HttpClient<Connected> {
    fn authenticate(self, token: String) -> HttpClient<Authenticated> {
        println!("Authenticating...");
        HttpClient {
            url: self.url,
            token: Some(token),
            _state: PhantomData,
        }
    }

    // Can also disconnect without authenticating
    fn disconnect(self) -> HttpClient<Disconnected> {
        HttpClient::new(self.url)
    }
}

// Only Authenticated state can make API calls
impl HttpClient<Authenticated> {
    fn get(&self, path: &str) -> String {
        println!("GET {}{} with token {:?}", self.url, path, self.token);
        "response".to_string()
    }

    fn post(&self, path: &str, body: &str) -> String {
        println!("POST {}{}: {}", self.url, path, body);
        "response".to_string()
    }

    fn disconnect(self) -> HttpClient<Disconnected> {
        HttpClient::new(self.url)
    }
}

// Usage example
fn http_example() {
    let client = HttpClient::new("https://api.example.com".to_string());

    // client.get("/users"); // ❌ Compile error! Not connected

    let client = client.connect();

    // client.get("/users"); // ❌ Compile error! Not authenticated

    let client = client.authenticate("secret_token".to_string());

    client.get("/users"); // ✅ OK!
    client.post("/users", "data"); // ✅ OK!
}

// Example 2: Builder pattern with compile-time validation
struct BuilderStart;
struct HasHost;
struct HasPort;
struct Complete;

struct ServerConfig<State> {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<u64>,
    _state: PhantomData<State>,
}

impl ServerConfig<BuilderStart> {
    fn new() -> Self {
        ServerConfig {
            host: None,
            port: None,
            timeout: None,
            _state: PhantomData,
        }
    }

    fn host(self, host: String) -> ServerConfig<HasHost> {
        ServerConfig {
            host: Some(host),
            port: self.port,
            timeout: self.timeout,
            _state: PhantomData,
        }
    }
}

impl ServerConfig<HasHost> {
    fn port(self, port: u16) -> ServerConfig<Complete> {
        ServerConfig {
            host: self.host,
            port: Some(port),
            timeout: self.timeout,
            _state: PhantomData,
        }
    }
}

impl ServerConfig<Complete> {
    fn timeout(mut self, timeout: u64) -> Self {
        self.timeout = Some(timeout);
        self
    }

    fn build(self) -> Server {
        Server {
            host: self.host.unwrap(),
            port: self.port.unwrap(),
            timeout: self.timeout.unwrap_or(30),
        }
    }
}

struct Server {
    host: String,
    port: u16,
    timeout: u64,
}

// Usage example
fn builder_example() {
    // let server = ServerConfig::new().build(); // ❌ Compile error!

    // Must provide host and port
    let server = ServerConfig::new()
        .host("localhost".to_string())
        .port(8080)
        .timeout(60)
        .build(); // ✅ OK!
}

// Example 3: File handle with guaranteed closure
struct Open;
struct Closed;

struct FileHandle<State> {
    path: String,
    _state: PhantomData<State>,
}

impl FileHandle<Closed> {
    fn open(path: String) -> std::io::Result<FileHandle<Open>> {
        println!("Opening file: {}", path);
        // Actual file opening logic here
        Ok(FileHandle {
            path,
            _state: PhantomData,
        })
    }
}

impl FileHandle<Open> {
    fn read(&self) -> String {
        format!("Contents of {}", self.path)
    }

    fn write(&mut self, data: &str) {
        println!("Writing to {}: {}", self.path, data);
    }

    fn close(self) -> FileHandle<Closed> {
        println!("Closing file: {}", self.path);
        FileHandle {
            path: self.path,
            _state: PhantomData,
        }
    }
}

// Automatically close on drop
impl Drop for FileHandle<Open> {
    fn drop(&mut self) {
        println!("Auto-closing file: {}", self.path);
    }
}

// Example 4: Transaction with commit/rollback
struct TransactionStart;
struct TransactionActive;
struct TransactionComplete;

struct Transaction<State> {
    id: u64,
    operations: Vec<String>,
    _state: PhantomData<State>,
}

impl Transaction<TransactionStart> {
    fn begin(id: u64) -> Transaction<TransactionActive> {
        println!("Beginning transaction {}", id);
        Transaction {
            id,
            operations: Vec::new(),
            _state: PhantomData,
        }
    }
}

impl Transaction<TransactionActive> {
    fn execute(&mut self, operation: String) {
        println!("Executing: {}", operation);
        self.operations.push(operation);
    }

    fn commit(self) -> Transaction<TransactionComplete> {
        println!("Committing transaction {}", self.id);
        Transaction {
            id: self.id,
            operations: self.operations,
            _state: PhantomData,
        }
    }

    fn rollback(self) {
        println!("Rolling back transaction {}", self.id);
        // Operations discarded
    }
}

impl Transaction<TransactionComplete> {
    fn operations(&self) -> &[String] {
        &self.operations
    }
}
```

#### Typestate Pattern Benefits

**Compile-Time Guarantees:**
- ✅ Can't call `get()` before `authenticate()`
- ✅ Can't call `build()` before setting required fields
- ✅ Can't read from closed file
- ✅ Can't commit transaction twice

**IDE Support:**
- Autocomplete shows only valid methods for current state
- Compiler guides you through valid state transitions

**Performance:**
- Zero runtime cost (PhantomData has size 0)
- All checks at compile time
- No runtime state validation needed

**When to Use:**
- Protocol implementations (HTTP, database connections)
- Builder patterns with required fields
- State machines (game states, UI flows)
- Resource lifecycle management (files, transactions)

**Trade-offs:**
- More complex API
- Steeper learning curve
- More generic code to write
- Can't store heterogeneous states in collections

**Alternative: Enum-based state machine:**
```rust
enum ConnectionState {
    Disconnected,
    Connected,
    Authenticated { token: String },
}

// Runtime checks needed
match state {
    ConnectionState::Authenticated { token } => { /* use token */ }
    _ => panic!("Not authenticated!"),
}
```

Typestate moves these runtime checks to compile time.

---

### 5.2 Phantom Types

**Pattern Name:** Zero-Cost Type-Level Programming
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Type-safe units, markers with zero runtime cost

#### Problem Solved
Adds compile-time type information without runtime overhead, enabling type-safe units, protocols, and phantom type parameters.

#### Code Example

```rust
use std::marker::PhantomData;
use std::ops::{Add, Sub, Mul, Div};

// Example 1: Type-safe units of measurement
#[derive(Debug, Clone, Copy, PartialEq)]
struct Unit<T> {
    value: f64,
    _marker: PhantomData<T>,
}

// Unit types (zero-sized)
struct Meter;
struct Foot;
struct Kilogram;
struct Pound;

// Type aliases for convenience
type Meters = Unit<Meter>;
type Feet = Unit<Foot>;
type Kilograms = Unit<Kilogram>;
type Pounds = Unit<Pound>;

impl<T> Unit<T> {
    fn new(value: f64) -> Self {
        Unit {
            value,
            _marker: PhantomData,
        }
    }

    fn value(&self) -> f64 {
        self.value
    }
}

// Can only add units of same type
impl<T> Add for Unit<T> {
    type Output = Unit<T>;

    fn add(self, other: Unit<T>) -> Self::Output {
        Unit::new(self.value + other.value)
    }
}

impl<T> Sub for Unit<T> {
    type Output = Unit<T>;

    fn sub(self, other: Unit<T>) -> Self::Output {
        Unit::new(self.value - other.value)
    }
}

// Scalar multiplication
impl<T> Mul<f64> for Unit<T> {
    type Output = Unit<T>;

    fn mul(self, scalar: f64) -> Self::Output {
        Unit::new(self.value * scalar)
    }
}

// Conversions between units
impl From<Meters> for Feet {
    fn from(m: Meters) -> Feet {
        Feet::new(m.value * 3.28084)
    }
}

impl From<Feet> for Meters {
    fn from(f: Feet) -> Meters {
        Meters::new(f.value / 3.28084)
    }
}

fn units_example() {
    let distance1 = Meters::new(100.0);
    let distance2 = Meters::new(50.0);

    // ✅ Can add meters to meters
    let total = distance1 + distance2; // Meters

    let weight = Kilograms::new(10.0);

    // ❌ Compile error: can't add meters to kilograms
    // let invalid = distance1 + weight;

    // Conversions are explicit
    let in_feet: Feet = distance1.into();
    println!("{} meters = {} feet", distance1.value(), in_feet.value());
}

// Example 2: Phantom type for variance
struct Invariant<T> {
    _marker: PhantomData<fn(T) -> T>,
}

struct Covariant<T> {
    _marker: PhantomData<fn() -> T>,
}

struct Contravariant<T> {
    _marker: PhantomData<fn(T)>,
}

// Example 3: Type-level state without data
struct Initialized;
struct Uninitialized;

struct Memory<State> {
    data: Vec<u8>,
    _state: PhantomData<State>,
}

impl Memory<Uninitialized> {
    fn new(size: usize) -> Self {
        Memory {
            data: Vec::with_capacity(size),
            _state: PhantomData,
        }
    }

    fn initialize(mut self, value: u8) -> Memory<Initialized> {
        self.data.resize(self.data.capacity(), value);
        Memory {
            data: self.data,
            _state: PhantomData,
        }
    }
}

impl Memory<Initialized> {
    fn read(&self, index: usize) -> u8 {
        self.data[index] // Safe: guaranteed to be initialized
    }

    fn write(&mut self, index: usize, value: u8) {
        self.data[index] = value;
    }
}

// Example 4: Phantom type for protocol versioning
struct V1;
struct V2;

struct Message<Version> {
    data: String,
    _version: PhantomData<Version>,
}

impl Message<V1> {
    fn new_v1(data: String) -> Self {
        Message {
            data,
            _version: PhantomData,
        }
    }

    fn upgrade(self) -> Message<V2> {
        Message {
            data: format!("v2:{}", self.data),
            _version: PhantomData,
        }
    }
}

impl Message<V2> {
    fn new_v2(data: String) -> Self {
        Message {
            data,
            _version: PhantomData,
        }
    }

    fn process(&self) {
        println!("Processing V2 message: {}", self.data);
    }
}

// Example 5: Phantom type ownership markers
struct Owned;
struct Borrowed;

struct Data<Ownership> {
    bytes: Vec<u8>,
    _ownership: PhantomData<Ownership>,
}

impl Data<Owned> {
    fn new(bytes: Vec<u8>) -> Self {
        Data {
            bytes,
            _ownership: PhantomData,
        }
    }

    fn borrow(&self) -> Data<Borrowed> {
        Data {
            bytes: self.bytes.clone(),
            _ownership: PhantomData,
        }
    }

    fn consume(self) -> Vec<u8> {
        self.bytes
    }
}

impl Data<Borrowed> {
    fn view(&self) -> &[u8] {
        &self.bytes
    }

    // Can't consume borrowed data
    // fn consume(self) -> Vec<u8> { } // Not implemented!
}
```

#### Phantom Type Patterns

**Pattern 1: Type-Safe Units**
```rust
struct Seconds(f64);
struct Minutes(f64);

// Can't mix up time units
fn sleep(duration: Seconds) { /* ... */ }
```

**Pattern 2: State Markers**
```rust
struct Locked;
struct Unlocked;

struct Mutex<T, State> {
    data: T,
    _state: PhantomData<State>,
}
```

**Pattern 3: Variance Control**
```rust
// PhantomData<T>: covariant
// PhantomData<fn(T)>: contravariant
// PhantomData<fn(T) -> T>: invariant
```

**Pattern 4: Protocol/Version Tags**
```rust
struct HTTP1;
struct HTTP2;

struct Request<Version> {
    headers: Vec<String>,
    _version: PhantomData<Version>,
}
```

**When to Use:**
- Type-safe units of measurement
- Protocol/version markers
- Ownership or lifecycle markers
- Generic parameter constraints
- Variance annotations

**Performance:**
```rust
assert_eq!(std::mem::size_of::<PhantomData<String>>(), 0);
assert_eq!(std::mem::size_of::<Unit<Meter>>(), 8); // Only f64
```

**Zero runtime cost!**

---

### 5.3 Sealed Traits

**Pattern Name:** Controlled Trait Extensibility
**Complexity:** ⭐⭐⭐⭐ Difficult
**Safety Guarantees:** Prevents external implementations, maintains API stability

#### Problem Solved
Prevents external crates from implementing your trait, allowing you to add methods without breaking compatibility.

#### Code Example

```rust
// Example 1: Basic sealed trait pattern
mod private {
    pub trait Sealed {}
}

// Public trait, but can't be implemented externally
pub trait ProtocolMessage: private::Sealed {
    fn encode(&self) -> Vec<u8>;
    fn decode(data: &[u8]) -> Self;
}

// We control all implementations
pub struct TextMessage {
    content: String,
}

impl private::Sealed for TextMessage {}

impl ProtocolMessage for TextMessage {
    fn encode(&self) -> Vec<u8> {
        self.content.as_bytes().to_vec()
    }

    fn decode(data: &[u8]) -> Self {
        TextMessage {
            content: String::from_utf8_lossy(data).to_string(),
        }
    }
}

pub struct BinaryMessage {
    data: Vec<u8>,
}

impl private::Sealed for BinaryMessage {}

impl ProtocolMessage for BinaryMessage {
    fn encode(&self) -> Vec<u8> {
        self.data.clone()
    }

    fn decode(data: &[u8]) -> Self {
        BinaryMessage {
            data: data.to_vec(),
        }
    }
}

// External crate CANNOT do this:
// impl ProtocolMessage for MyType {} // ❌ Compile error: Sealed not in scope!

// Example 2: Sealed trait with future extensibility
mod sealed {
    pub trait Sealed {}
}

pub trait JsonValue: sealed::Sealed {
    fn to_json(&self) -> String;

    // Can safely add methods later without breaking changes!
    // fn validate(&self) -> bool { true }
}

pub struct Number(f64);
impl sealed::Sealed for Number {}
impl JsonValue for Number {
    fn to_json(&self) -> String {
        self.0.to_string()
    }
}

pub struct Boolean(bool);
impl sealed::Sealed for Boolean {}
impl JsonValue for Boolean {
    fn to_json(&self) -> String {
        self.0.to_string()
    }
}

// Example 3: Sealed trait with generic parameters
mod iter_sealed {
    pub trait Sealed<T> {}
}

pub trait CustomIterator<T>: iter_sealed::Sealed<T> {
    fn custom_next(&mut self) -> Option<T>;
}

pub struct RangeIterator {
    current: i32,
    end: i32,
}

impl iter_sealed::Sealed<i32> for RangeIterator {}

impl CustomIterator<i32> for RangeIterator {
    fn custom_next(&mut self) -> Option<i32> {
        if self.current < self.end {
            let value = self.current;
            self.current += 1;
            Some(value)
        } else {
            None
        }
    }
}

// Example 4: Sealed trait for finite set of types
mod ops_sealed {
    pub trait Sealed {}

    impl Sealed for i32 {}
    impl Sealed for i64 {}
    impl Sealed for f32 {}
    impl Sealed for f64 {}
}

pub trait Numeric: ops_sealed::Sealed + Copy {
    fn zero() -> Self;
    fn one() -> Self;
}

impl Numeric for i32 {
    fn zero() -> Self { 0 }
    fn one() -> Self { 1 }
}

impl Numeric for f64 {
    fn zero() -> Self { 0.0 }
    fn one() -> Self { 1.0 }
}

// Users can use the trait but not implement it
fn generic_math<T: Numeric>(x: T, y: T) -> T {
    x // Just an example
}

// Example 5: Real-world pattern from std
// Similar to how std::error::Error is sealed

mod error_sealed {
    pub trait Sealed {}
}

pub trait CustomError: error_sealed::Sealed + std::fmt::Display + std::fmt::Debug {
    fn error_code(&self) -> u32;
}

pub struct NetworkError {
    message: String,
    code: u32,
}

impl std::fmt::Display for NetworkError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.message)
    }
}

impl std::fmt::Debug for NetworkError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "NetworkError({}, {})", self.message, self.code)
    }
}

impl error_sealed::Sealed for NetworkError {}

impl CustomError for NetworkError {
    fn error_code(&self) -> u32 {
        self.code
    }
}
```

#### Sealed Trait Benefits

**API Evolution:**
```rust
// Can add methods without breaking external code
pub trait Sealed: private::Sealed {
    fn method_v1(&self);

    // Added in v2 - safe because trait is sealed!
    fn method_v2(&self) { /* default impl */ }
}
```

**Exhaustive Matching:**
```rust
fn handle_message(msg: &dyn ProtocolMessage) {
    // Compiler knows ALL implementations
    match msg {
        TextMessage => { /* ... */ }
        BinaryMessage => { /* ... */ }
        // No _ needed - exhaustive!
    }
}
```

**Type Safety:**
```rust
// Prevents users from breaking invariants
trait Sealed: private::Sealed {
    fn internal_invariant(&self) -> bool;
}

// External types can't claim to uphold invariant
```

**When to Use:**

✅ **Use sealed traits when:**
- You want to add methods in the future without breaking changes
- You have a closed set of implementations
- You need to maintain internal invariants
- You're designing a public library API

❌ **Don't use sealed traits when:**
- You want extensibility (trait objects, plugin systems)
- Trait is meant for external implementation
- You're building a framework with extension points

**Real-World Examples:**

- `std::error::Error` (sealed in practice via complexity)
- Serde's internal traits
- `FromIterator` for certain types
- Protocol implementation traits in networking libraries

**Performance:** Zero cost - purely compile-time pattern

---

## Summary: When to Use Each Pattern

### Ownership & Borrowing
| Pattern | Complexity | Use Case | Performance |
|---------|-----------|----------|-------------|
| Lifetimes | ⭐⭐⭐ | Multiple references, return references | Zero-cost |
| RefCell | ⭐⭐⭐ | Single-threaded interior mutability | Small runtime cost |
| Arc<Mutex> | ⭐⭐⭐⭐ | Thread-safe shared state | Lock overhead |
| Arc<RwLock> | ⭐⭐⭐⭐ | Read-heavy thread-safe state | Lower for reads |

### Traits
| Pattern | Complexity | Use Case | Performance |
|---------|-----------|----------|-------------|
| Associated Types | ⭐⭐⭐⭐ | One implementation per type | Zero-cost |
| Generic Parameters | ⭐⭐⭐ | Multiple implementations | Zero-cost |
| Trait Objects | ⭐⭐⭐⭐ | Heterogeneous collections | Vtable indirection |
| Newtype | ⭐⭐⭐ | Orphan rule, type safety | Zero-cost |
| Blanket Impl | ⭐⭐⭐⭐ | Automatic implementations | Zero-cost |

### Async
| Pattern | Complexity | Use Case | Performance |
|---------|-----------|----------|-------------|
| Tokio Runtime | ⭐⭐⭐ | Async I/O, network apps | Excellent |
| Graceful Shutdown | ⭐⭐⭐⭐ | Production servers | Minimal overhead |
| Channels | ⭐⭐⭐ | Task communication | Low overhead |

### Error Handling
| Pattern | Complexity | Use Case | Performance |
|---------|-----------|----------|-------------|
| thiserror | ⭐⭐⭐ | Library errors | Zero-cost |
| anyhow | ⭐⭐⭐ | Application errors | Minimal overhead |
| Combinators | ⭐⭐⭐ | Functional error handling | Zero-cost |

### Type-Safe Design
| Pattern | Complexity | Use Case | Performance |
|---------|-----------|----------|-------------|
| Type State | ⭐⭐⭐⭐⭐ | State machines, builders | Zero-cost |
| Phantom Types | ⭐⭐⭐⭐ | Type-safe units, markers | Zero-cost |
| Sealed Traits | ⭐⭐⭐⭐ | Controlled extensibility | Zero-cost |

---

## Recommended Learning Path

1. **Start with:** Lifetimes, Result/Option combinators, basic async
2. **Then learn:** RefCell, Arc<Mutex>, thiserror/anyhow
3. **Advanced:** Type state, phantom types, sealed traits
4. **Master:** Trait bounds, blanket implementations, complex async patterns

---

## Additional Resources

- **Official Rust Book:** https://doc.rust-lang.org/book/
- **Rustonomicon:** https://doc.rust-lang.org/nomicon/ (unsafe Rust)
- **Async Book:** https://rust-lang.github.io/async-book/
- **Tokio Tutorial:** https://tokio.rs/tokio/tutorial
- **Rust by Example:** https://doc.rust-lang.org/rust-by-example/

---

**End of Research Document**
