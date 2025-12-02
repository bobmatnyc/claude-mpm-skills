# Go Advanced Patterns & Best Practices (2025)

**Document Version:** 1.0
**Last Updated:** December 1, 2025
**Go Version:** 1.21+
**Focus:** Production-ready patterns for moderate to difficult use cases

---

## Table of Contents

1. [Concurrency Patterns](#1-concurrency-patterns)
2. [Error Handling](#2-error-handling)
3. [Design Patterns](#3-design-patterns)
4. [HTTP & API Development](#4-http--api-development)
5. [Performance & Best Practices](#5-performance--best-practices)
6. [Common Mistakes to Avoid](#6-common-mistakes-to-avoid)

---

## 1. Concurrency Patterns

### 1.1 Worker Pool with Context Cancellation

**Pattern:** Control concurrent operations with a fixed pool of workers that respect context cancellation.

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Job represents work to be processed
type Job struct {
    ID   int
    Data string
}

// Result represents processing outcome
type Result struct {
    JobID int
    Value string
    Err   error
}

// WorkerPool manages concurrent job processing
type WorkerPool struct {
    workerCount int
    jobs        chan Job
    results     chan Result
    wg          sync.WaitGroup
}

// NewWorkerPool creates a pool with specified number of workers
func NewWorkerPool(workerCount int) *WorkerPool {
    return &WorkerPool{
        workerCount: workerCount,
        jobs:        make(chan Job, workerCount*2), // Buffered for efficiency
        results:     make(chan Result, workerCount*2),
    }
}

// Start launches worker goroutines
func (wp *WorkerPool) Start(ctx context.Context) {
    for i := 0; i < wp.workerCount; i++ {
        wp.wg.Add(1)
        go wp.worker(ctx, i)
    }
}

// worker processes jobs until context is cancelled or jobs channel closes
func (wp *WorkerPool) worker(ctx context.Context, id int) {
    defer wp.wg.Done()

    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d: context cancelled\n", id)
            return
        case job, ok := <-wp.jobs:
            if !ok {
                fmt.Printf("Worker %d: jobs channel closed\n", id)
                return
            }

            // Simulate work with context awareness
            result := wp.processJob(ctx, job)

            // Send result if context is still valid
            select {
            case wp.results <- result:
            case <-ctx.Done():
                return
            }
        }
    }
}

// processJob simulates job processing with context timeout
func (wp *WorkerPool) processJob(ctx context.Context, job Job) Result {
    // Create timeout for individual job
    jobCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
    defer cancel()

    resultCh := make(chan Result, 1)

    go func() {
        // Simulate work
        time.Sleep(100 * time.Millisecond)
        resultCh <- Result{
            JobID: job.ID,
            Value: fmt.Sprintf("Processed: %s", job.Data),
        }
    }()

    select {
    case result := <-resultCh:
        return result
    case <-jobCtx.Done():
        return Result{
            JobID: job.ID,
            Err:   fmt.Errorf("job timeout: %w", jobCtx.Err()),
        }
    }
}

// Submit adds a job to the queue (blocks if queue is full)
func (wp *WorkerPool) Submit(ctx context.Context, job Job) error {
    select {
    case wp.jobs <- job:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

// Close signals no more jobs and waits for completion
func (wp *WorkerPool) Close() {
    close(wp.jobs)
    wp.wg.Wait()
    close(wp.results)
}

// Results returns the results channel
func (wp *WorkerPool) Results() <-chan Result {
    return wp.results
}

// Example usage
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    pool := NewWorkerPool(3)
    pool.Start(ctx)

    // Submit jobs
    go func() {
        for i := 0; i < 10; i++ {
            job := Job{ID: i, Data: fmt.Sprintf("task-%d", i)}
            if err := pool.Submit(ctx, job); err != nil {
                fmt.Printf("Failed to submit job %d: %v\n", i, err)
                break
            }
        }
        pool.Close()
    }()

    // Collect results
    for result := range pool.Results() {
        if result.Err != nil {
            fmt.Printf("Job %d failed: %v\n", result.JobID, result.Err)
        } else {
            fmt.Printf("Job %d: %s\n", result.JobID, result.Value)
        }
    }
}
```

**Key Points:**
- Use buffered channels (size = 2x worker count) to reduce blocking
- Always pass `context.Context` as first parameter
- Use `select` with `ctx.Done()` for cancellation awareness
- Close jobs channel to signal completion, wait for workers with `WaitGroup`
- Use timeout contexts for individual job processing

---

### 1.2 Fan-Out/Fan-In Pattern

**Pattern:** Distribute work across multiple goroutines (fan-out) and merge results (fan-in).

```go
package main

import (
    "context"
    "fmt"
    "sync"
)

// FanOut distributes input across multiple workers
func FanOut(ctx context.Context, input <-chan int, workerCount int) []<-chan int {
    channels := make([]<-chan int, workerCount)

    for i := 0; i < workerCount; i++ {
        channels[i] = worker(ctx, input, i)
    }

    return channels
}

// worker processes input and returns processed output
func worker(ctx context.Context, input <-chan int, id int) <-chan int {
    out := make(chan int)

    go func() {
        defer close(out)

        for {
            select {
            case <-ctx.Done():
                return
            case val, ok := <-input:
                if !ok {
                    return
                }

                // Process value (simulate work)
                result := val * 2

                select {
                case out <- result:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()

    return out
}

// FanIn merges multiple channels into single output channel
func FanIn(ctx context.Context, channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    // Start goroutine for each input channel
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()

            for {
                select {
                case <-ctx.Done():
                    return
                case val, ok := <-c:
                    if !ok {
                        return
                    }

                    select {
                    case out <- val:
                    case <-ctx.Done():
                        return
                    }
                }
            }
        }(ch)
    }

    // Close output channel when all inputs are done
    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

// Example usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Create input channel
    input := make(chan int)

    // Generate input data
    go func() {
        defer close(input)
        for i := 1; i <= 10; i++ {
            select {
            case input <- i:
            case <-ctx.Done():
                return
            }
        }
    }()

    // Fan-out to 3 workers
    workers := FanOut(ctx, input, 3)

    // Fan-in results
    results := FanIn(ctx, workers...)

    // Consume results
    for result := range results {
        fmt.Printf("Result: %d\n", result)
    }
}
```

**Key Points:**
- Fan-out distributes work to leverage parallelism
- Fan-in merges results maintaining order independence
- Always use `select` with `ctx.Done()` in both directions
- Close channels properly to prevent goroutine leaks
- Use `sync.WaitGroup` to coordinate multiple goroutines

---

### 1.3 Pipeline Pattern with Context

**Pattern:** Chain processing stages with proper cancellation propagation.

```go
package main

import (
    "context"
    "fmt"
)

// Pipeline stage functions
type StageFunc func(context.Context, <-chan int) <-chan int

// Generate creates input stream
func Generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)

    go func() {
        defer close(out)

        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()

    return out
}

// Square multiplies each number by itself
func Square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)

    go func() {
        defer close(out)

        for {
            select {
            case n, ok := <-in:
                if !ok {
                    return
                }

                result := n * n

                select {
                case out <- result:
                case <-ctx.Done():
                    return
                }
            case <-ctx.Done():
                return
            }
        }
    }()

    return out
}

// Filter removes numbers not matching predicate
func Filter(ctx context.Context, in <-chan int, predicate func(int) bool) <-chan int {
    out := make(chan int)

    go func() {
        defer close(out)

        for {
            select {
            case n, ok := <-in:
                if !ok {
                    return
                }

                if predicate(n) {
                    select {
                    case out <- n:
                    case <-ctx.Done():
                        return
                    }
                }
            case <-ctx.Done():
                return
            }
        }
    }()

    return out
}

// Pipeline chains stages together
func Pipeline(ctx context.Context, stages ...StageFunc) StageFunc {
    return func(ctx context.Context, in <-chan int) <-chan int {
        c := in
        for _, stage := range stages {
            c = stage(ctx, c)
        }
        return c
    }
}

// Example usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Create pipeline: Generate -> Square -> Filter (keep even numbers)
    pipeline := Pipeline(
        ctx,
        func(ctx context.Context, in <-chan int) <-chan int {
            return Square(ctx, in)
        },
        func(ctx context.Context, in <-chan int) <-chan int {
            return Filter(ctx, in, func(n int) bool {
                return n%2 == 0
            })
        },
    )

    // Generate input
    input := Generate(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    // Execute pipeline
    output := pipeline(ctx, input)

    // Consume results
    for result := range output {
        fmt.Printf("Result: %d\n", result)
    }
}
```

**Key Points:**
- Each stage is a function that receives and returns channels
- Context propagates through all stages for coordinated cancellation
- Use generator pattern for input creation
- Close channels in defer to prevent leaks
- Compose stages using higher-order functions

---

### 1.4 Select with Timeout and Default

**Pattern:** Non-blocking channel operations with timeout handling.

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// ChannelOperations demonstrates advanced select patterns
type ChannelOperations struct{}

// TryReceive attempts non-blocking receive with timeout
func (co *ChannelOperations) TryReceive(ch <-chan string, timeout time.Duration) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()

    select {
    case val := <-ch:
        return val, nil
    case <-ctx.Done():
        return "", fmt.Errorf("receive timeout after %v", timeout)
    }
}

// TrySend attempts non-blocking send with timeout
func (co *ChannelOperations) TrySend(ctx context.Context, ch chan<- string, val string, timeout time.Duration) error {
    sendCtx, cancel := context.WithTimeout(ctx, timeout)
    defer cancel()

    select {
    case ch <- val:
        return nil
    case <-sendCtx.Done():
        return fmt.Errorf("send timeout after %v", timeout)
    }
}

// MultiChannelSelect demonstrates selecting from multiple sources
func (co *ChannelOperations) MultiChannelSelect(ctx context.Context, ch1, ch2 <-chan string) (string, string) {
    for {
        select {
        case msg1 := <-ch1:
            return msg1, "channel1"
        case msg2 := <-ch2:
            return msg2, "channel2"
        case <-ctx.Done():
            return "", "cancelled"
        case <-time.After(1 * time.Second):
            // Default case after timeout - prevents infinite blocking
            return "", "timeout"
        }
    }
}

// PrioritySelect demonstrates priority channel selection
func (co *ChannelOperations) PrioritySelect(ctx context.Context, priority, normal <-chan string) string {
    for {
        select {
        case msg := <-priority:
            return msg
        default:
            // Check normal channel only if priority is empty
            select {
            case msg := <-priority:
                return msg
            case msg := <-normal:
                return msg
            case <-ctx.Done():
                return "cancelled"
            }
        }
    }
}

// Example usage
func main() {
    co := &ChannelOperations{}
    ctx := context.Background()

    // Example 1: Try receive with timeout
    ch := make(chan string, 1)
    ch <- "hello"

    if val, err := co.TryReceive(ch, 100*time.Millisecond); err == nil {
        fmt.Printf("Received: %s\n", val)
    }

    // Example 2: Try send with timeout
    sendCh := make(chan string, 1)
    if err := co.TrySend(ctx, sendCh, "world", 100*time.Millisecond); err == nil {
        fmt.Println("Send successful")
    }

    // Example 3: Multi-channel select
    ch1 := make(chan string, 1)
    ch2 := make(chan string, 1)
    ch1 <- "from ch1"

    val, source := co.MultiChannelSelect(ctx, ch1, ch2)
    fmt.Printf("Received '%s' from %s\n", val, source)
}
```

**Key Points:**
- Use `time.After()` for timeout in select (creates timer channel)
- Default case makes select non-blocking
- Priority selection uses nested select with default case
- Always include `ctx.Done()` case for cancellation
- Be aware: `time.After()` creates new timer each select iteration (use `time.NewTimer()` for loops)

---

## 2. Error Handling

### 2.1 errors.Is and errors.As (Go 1.13+)

**Pattern:** Type-safe error checking with error wrapping support.

```go
package main

import (
    "errors"
    "fmt"
    "io"
    "os"
)

// Sentinel errors - use for simple error conditions
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
    ErrTimeout      = errors.New("operation timeout")
)

// Custom error type with additional context
type ValidationError struct {
    Field   string
    Message string
    Err     error // Wrapped error
}

func (e *ValidationError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("validation error [%s]: %s: %v", e.Field, e.Message, e.Err)
    }
    return fmt.Sprintf("validation error [%s]: %s", e.Field, e.Message)
}

// Unwrap enables errors.Is and errors.As to work
func (e *ValidationError) Unwrap() error {
    return e.Err
}

// NetworkError with structured information
type NetworkError struct {
    Op     string
    URL    string
    Status int
    Err    error
}

func (e *NetworkError) Error() string {
    return fmt.Sprintf("network error during %s [%s]: status=%d: %v", e.Op, e.URL, e.Status, e.Err)
}

func (e *NetworkError) Unwrap() error {
    return e.Err
}

// Example: Database operation with error wrapping
func fetchUser(id string) error {
    // Simulate database error
    if id == "" {
        // Wrap sentinel error with context
        return fmt.Errorf("fetchUser: %w", ErrNotFound)
    }

    if id == "invalid" {
        // Wrap custom error type
        return &ValidationError{
            Field:   "id",
            Message: "invalid format",
            Err:     errors.New("expected UUID format"),
        }
    }

    return nil
}

// Example: Network request with error wrapping
func makeRequest(url string) error {
    if url == "" {
        return &NetworkError{
            Op:     "GET",
            URL:    url,
            Status: 400,
            Err:    errors.New("empty URL"),
        }
    }

    return nil
}

// HandleError demonstrates errors.Is and errors.As usage
func HandleError(err error) {
    if err == nil {
        return
    }

    // Check for sentinel error using errors.Is (works with wrapped errors)
    if errors.Is(err, ErrNotFound) {
        fmt.Println("Resource not found - returning 404")
        return
    }

    if errors.Is(err, io.EOF) {
        fmt.Println("End of file reached")
        return
    }

    // Extract custom error type using errors.As
    var validationErr *ValidationError
    if errors.As(err, &validationErr) {
        fmt.Printf("Validation failed: field=%s, message=%s\n",
            validationErr.Field, validationErr.Message)
        return
    }

    // Extract network error
    var netErr *NetworkError
    if errors.As(err, &netErr) {
        fmt.Printf("Network error: op=%s, url=%s, status=%d\n",
            netErr.Op, netErr.URL, netErr.Status)
        return
    }

    // Check for OS-specific errors
    var pathErr *os.PathError
    if errors.As(err, &pathErr) {
        fmt.Printf("Path error: op=%s, path=%s, err=%v\n",
            pathErr.Op, pathErr.Path, pathErr.Err)
        return
    }

    // Generic error
    fmt.Printf("Unknown error: %v\n", err)
}

// Example usage
func main() {
    // Test sentinel error
    err1 := fetchUser("")
    fmt.Printf("Error: %v\n", err1)
    HandleError(err1)

    // Test custom error type
    err2 := fetchUser("invalid")
    fmt.Printf("\nError: %v\n", err2)
    HandleError(err2)

    // Test network error
    err3 := makeRequest("")
    fmt.Printf("\nError: %v\n", err3)
    HandleError(err3)
}
```

**Key Points:**
- Use `errors.Is()` for sentinel errors (compares values)
- Use `errors.As()` for custom error types (type assertion)
- Implement `Unwrap()` method to enable error chain traversal
- Use `fmt.Errorf()` with `%w` verb to wrap errors
- Prefer `errors.Is()` over `==` for error comparison
- Prefer `errors.As()` over type assertion for error types

---

### 2.2 Error Wrapping with Context

**Pattern:** Preserve error chain while adding context at each layer.

```go
package main

import (
    "database/sql"
    "errors"
    "fmt"
)

// Domain errors
var (
    ErrUserNotFound    = errors.New("user not found")
    ErrInvalidInput    = errors.New("invalid input")
    ErrDatabaseFailure = errors.New("database operation failed")
)

// Repository layer - lowest level
type UserRepository struct {
    db *sql.DB
}

func (r *UserRepository) GetByID(id string) error {
    // Simulate database error
    if id == "1" {
        // Wrap low-level error with context
        return fmt.Errorf("UserRepository.GetByID(id=%s): %w", id, sql.ErrNoRows)
    }
    return nil
}

func (r *UserRepository) Update(id string, data map[string]interface{}) error {
    if len(data) == 0 {
        return fmt.Errorf("UserRepository.Update: %w", ErrInvalidInput)
    }
    return nil
}

// Service layer - business logic
type UserService struct {
    repo *UserRepository
}

func (s *UserService) GetUser(id string) error {
    err := s.repo.GetByID(id)
    if err != nil {
        // Check if it's a "not found" error and wrap with domain error
        if errors.Is(err, sql.ErrNoRows) {
            return fmt.Errorf("UserService.GetUser: %w", ErrUserNotFound)
        }
        // Wrap unexpected errors
        return fmt.Errorf("UserService.GetUser: failed to fetch user: %w", err)
    }
    return nil
}

func (s *UserService) UpdateUser(id string, data map[string]interface{}) error {
    // Validate input at service layer
    if id == "" {
        return fmt.Errorf("UserService.UpdateUser: %w: user ID is required", ErrInvalidInput)
    }

    err := s.repo.Update(id, data)
    if err != nil {
        return fmt.Errorf("UserService.UpdateUser(id=%s): %w", id, err)
    }
    return nil
}

// HTTP handler layer - presentation
type UserHandler struct {
    service *UserService
}

func (h *UserHandler) HandleGetUser(id string) error {
    err := h.service.GetUser(id)
    if err != nil {
        // Unwrap to find root cause for HTTP status code mapping
        if errors.Is(err, ErrUserNotFound) {
            return fmt.Errorf("HTTP 404: %w", err)
        }
        if errors.Is(err, ErrInvalidInput) {
            return fmt.Errorf("HTTP 400: %w", err)
        }
        // Unexpected error
        return fmt.Errorf("HTTP 500: internal server error: %w", err)
    }
    return nil
}

// ErrorChain prints the full error chain
func ErrorChain(err error) {
    fmt.Printf("Error chain:\n")
    for err != nil {
        fmt.Printf("  - %v\n", err)
        err = errors.Unwrap(err)
    }
}

// Example usage
func main() {
    // Setup
    repo := &UserRepository{}
    service := &UserService{repo: repo}
    handler := &UserHandler{service: service}

    // Test case 1: Not found error
    fmt.Println("Test 1: User not found")
    err := handler.HandleGetUser("1")
    if err != nil {
        fmt.Printf("Final error: %v\n\n", err)
        ErrorChain(err)
    }

    // Test case 2: Invalid input
    fmt.Println("\nTest 2: Invalid input")
    err = service.UpdateUser("", map[string]interface{}{})
    if err != nil {
        fmt.Printf("Final error: %v\n\n", err)
        ErrorChain(err)
    }
}
```

**Key Points:**
- Wrap errors with `fmt.Errorf()` and `%w` at each layer
- Add contextual information (function name, parameters)
- Map low-level errors to domain errors at service boundaries
- Use `errors.Is()` to check wrapped errors
- Error messages should read naturally from outer to inner
- Don't lose the error chain - always use `%w` not `%v`

---

### 2.3 Error Handling in Concurrent Code

**Pattern:** Aggregate and return errors from multiple goroutines.

```go
package main

import (
    "context"
    "errors"
    "fmt"
    "sync"
    "time"
)

// MultiError aggregates multiple errors (Go 1.20+)
type MultiError struct {
    errors []error
}

func (m *MultiError) Error() string {
    if len(m.errors) == 0 {
        return "no errors"
    }
    if len(m.errors) == 1 {
        return m.errors[0].Error()
    }
    return fmt.Sprintf("%d errors occurred: %v", len(m.errors), m.errors)
}

func (m *MultiError) Add(err error) {
    if err != nil {
        m.errors = append(m.errors, err)
    }
}

func (m *MultiError) Err() error {
    if len(m.errors) == 0 {
        return nil
    }
    return m
}

// Using errors.Join (Go 1.20+) - recommended approach
func ProcessConcurrentWithJoin(ctx context.Context, items []int) error {
    errCh := make(chan error, len(items))
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()

            // Simulate processing
            if n%3 == 0 {
                errCh <- fmt.Errorf("item %d: failed processing", n)
                return
            }

            select {
            case <-ctx.Done():
                errCh <- fmt.Errorf("item %d: %w", n, ctx.Err())
            case <-time.After(100 * time.Millisecond):
                // Success
            }
        }(item)
    }

    // Wait for all goroutines
    wg.Wait()
    close(errCh)

    // Collect all errors
    var errs []error
    for err := range errCh {
        errs = append(errs, err)
    }

    // Join errors (Go 1.20+)
    if len(errs) > 0 {
        return errors.Join(errs...)
    }

    return nil
}

// Error handling with first-error-wins pattern
func ProcessFirstError(ctx context.Context, items []int) error {
    ctx, cancel := context.WithCancel(ctx)
    defer cancel()

    errCh := make(chan error, 1) // Buffered to prevent goroutine leak
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()

            if n%2 == 0 {
                // Non-blocking send of first error
                select {
                case errCh <- fmt.Errorf("item %d failed", n):
                    cancel() // Cancel other goroutines
                default:
                    // Another error already sent
                }
                return
            }

            select {
            case <-ctx.Done():
                return
            case <-time.After(100 * time.Millisecond):
                // Success
            }
        }(item)
    }

    // Wait for completion
    go func() {
        wg.Wait()
        close(errCh)
    }()

    // Return first error or nil
    return <-errCh
}

// Error handling with structured result
type Result struct {
    Value int
    Err   error
}

func ProcessWithResults(ctx context.Context, items []int) ([]Result, error) {
    results := make([]Result, len(items))
    var wg sync.WaitGroup
    var mu sync.Mutex

    for i, item := range items {
        wg.Add(1)
        go func(idx, n int) {
            defer wg.Done()

            // Simulate processing
            time.Sleep(50 * time.Millisecond)

            result := Result{Value: n * 2}
            if n%3 == 0 {
                result.Err = fmt.Errorf("item %d: processing failed", n)
            }

            mu.Lock()
            results[idx] = result
            mu.Unlock()
        }(i, item)
    }

    wg.Wait()

    // Check if any results have errors
    var hasErrors bool
    for _, r := range results {
        if r.Err != nil {
            hasErrors = true
            break
        }
    }

    if hasErrors {
        return results, fmt.Errorf("some items failed processing")
    }

    return results, nil
}

// Example usage
func main() {
    ctx := context.Background()
    items := []int{1, 2, 3, 4, 5, 6}

    // Test 1: Join all errors
    fmt.Println("Test 1: Aggregate all errors")
    if err := ProcessConcurrentWithJoin(ctx, items); err != nil {
        fmt.Printf("Errors: %v\n\n", err)
    }

    // Test 2: First error wins
    fmt.Println("Test 2: First error wins")
    if err := ProcessFirstError(ctx, items); err != nil {
        fmt.Printf("Error: %v\n\n", err)
    }

    // Test 3: Structured results
    fmt.Println("Test 3: Structured results")
    results, err := ProcessWithResults(ctx, items)
    if err != nil {
        fmt.Printf("Processing completed with errors:\n")
        for i, r := range results {
            if r.Err != nil {
                fmt.Printf("  Item %d: %v\n", i, r.Err)
            } else {
                fmt.Printf("  Item %d: value=%d\n", i, r.Value)
            }
        }
    }
}
```

**Key Points:**
- Use `errors.Join()` (Go 1.20+) to aggregate multiple errors
- Use buffered error channel with size 1 for first-error pattern
- Cancel context to stop other goroutines on first error
- Return structured results when you need both errors and values
- Always close error channels after goroutines complete
- Use mutex when collecting results in shared slice

---

## 3. Design Patterns

### 3.1 Functional Options Pattern

**Pattern:** Configure structs with optional parameters using functions.

```go
package main

import (
    "fmt"
    "time"
)

// Server configuration
type Server struct {
    host         string
    port         int
    timeout      time.Duration
    maxConns     int
    tls          bool
    certFile     string
    keyFile      string
    readTimeout  time.Duration
    writeTimeout time.Duration
}

// Option is a functional option type
type Option func(*Server)

// WithHost sets the server host
func WithHost(host string) Option {
    return func(s *Server) {
        s.host = host
    }
}

// WithPort sets the server port
func WithPort(port int) Option {
    return func(s *Server) {
        s.port = port
    }
}

// WithTimeout sets the connection timeout
func WithTimeout(timeout time.Duration) Option {
    return func(s *Server) {
        s.timeout = timeout
    }
}

// WithMaxConnections sets maximum concurrent connections
func WithMaxConnections(max int) Option {
    return func(s *Server) {
        s.maxConns = max
    }
}

// WithTLS enables TLS with certificate files
func WithTLS(certFile, keyFile string) Option {
    return func(s *Server) {
        s.tls = true
        s.certFile = certFile
        s.keyFile = keyFile
    }
}

// WithReadTimeout sets read timeout
func WithReadTimeout(timeout time.Duration) Option {
    return func(s *Server) {
        s.readTimeout = timeout
    }
}

// WithWriteTimeout sets write timeout
func WithWriteTimeout(timeout time.Duration) Option {
    return func(s *Server) {
        s.writeTimeout = timeout
    }
}

// NewServer creates a server with functional options
func NewServer(opts ...Option) *Server {
    // Default configuration
    server := &Server{
        host:         "localhost",
        port:         8080,
        timeout:      30 * time.Second,
        maxConns:     100,
        tls:          false,
        readTimeout:  10 * time.Second,
        writeTimeout: 10 * time.Second,
    }

    // Apply options
    for _, opt := range opts {
        opt(server)
    }

    return server
}

// Start demonstrates using the configured server
func (s *Server) Start() error {
    fmt.Printf("Starting server on %s:%d\n", s.host, s.port)
    fmt.Printf("Configuration:\n")
    fmt.Printf("  Timeout: %v\n", s.timeout)
    fmt.Printf("  Max Connections: %d\n", s.maxConns)
    fmt.Printf("  TLS Enabled: %v\n", s.tls)
    if s.tls {
        fmt.Printf("  Cert: %s, Key: %s\n", s.certFile, s.keyFile)
    }
    fmt.Printf("  Read Timeout: %v\n", s.readTimeout)
    fmt.Printf("  Write Timeout: %v\n", s.writeTimeout)
    return nil
}

// Advanced: Option with validation
type validatedOption func(*Server) error

// WithValidatedPort sets port with validation
func WithValidatedPort(port int) validatedOption {
    return func(s *Server) error {
        if port < 1 || port > 65535 {
            return fmt.Errorf("invalid port: %d (must be 1-65535)", port)
        }
        s.port = port
        return nil
    }
}

// NewServerWithValidation creates server with validated options
func NewServerWithValidation(opts ...validatedOption) (*Server, error) {
    server := &Server{
        host:    "localhost",
        port:    8080,
        timeout: 30 * time.Second,
    }

    for _, opt := range opts {
        if err := opt(server); err != nil {
            return nil, err
        }
    }

    return server, nil
}

// Example usage
func main() {
    // Example 1: Minimal configuration (all defaults)
    server1 := NewServer()
    server1.Start()

    fmt.Println()

    // Example 2: Custom configuration
    server2 := NewServer(
        WithHost("0.0.0.0"),
        WithPort(9000),
        WithTimeout(60*time.Second),
        WithMaxConnections(500),
    )
    server2.Start()

    fmt.Println()

    // Example 3: TLS-enabled server
    server3 := NewServer(
        WithHost("api.example.com"),
        WithPort(443),
        WithTLS("/path/to/cert.pem", "/path/to/key.pem"),
        WithReadTimeout(5*time.Second),
        WithWriteTimeout(5*time.Second),
    )
    server3.Start()

    fmt.Println()

    // Example 4: Validated options
    server4, err := NewServerWithValidation(
        WithValidatedPort(8443),
    )
    if err != nil {
        fmt.Printf("Failed to create server: %v\n", err)
        return
    }
    server4.Start()
}
```

**Key Points:**
- Define option type as `func(*T)`
- Provide constructor accepting variadic options
- Set sensible defaults before applying options
- Each option function modifies specific fields
- Options can be combined and reused
- For validation, return errors from option functions
- Pattern scales well (adding options doesn't break API)

---

### 3.2 Interface-Based Dependency Injection

**Pattern:** Use interfaces for loose coupling and testability.

```go
package main

import (
    "context"
    "errors"
    "fmt"
    "time"
)

// Domain models
type User struct {
    ID    string
    Email string
    Name  string
}

// Interfaces define contracts (keep them small)

// UserRepository defines data access interface
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
}

// EmailSender defines notification interface
type EmailSender interface {
    Send(ctx context.Context, to, subject, body string) error
}

// Logger defines logging interface
type Logger interface {
    Info(msg string, fields ...interface{})
    Error(msg string, err error, fields ...interface{})
}

// UserService contains business logic
type UserService struct {
    repo   UserRepository
    email  EmailSender
    logger Logger
}

// NewUserService creates service with dependencies injected
func NewUserService(repo UserRepository, email EmailSender, logger Logger) *UserService {
    return &UserService{
        repo:   repo,
        email:  email,
        logger: logger,
    }
}

// RegisterUser demonstrates using injected dependencies
func (s *UserService) RegisterUser(ctx context.Context, email, name string) error {
    s.logger.Info("registering user", "email", email)

    user := &User{
        ID:    generateID(),
        Email: email,
        Name:  name,
    }

    if err := s.repo.Create(ctx, user); err != nil {
        s.logger.Error("failed to create user", err, "email", email)
        return fmt.Errorf("register user: %w", err)
    }

    // Send welcome email
    if err := s.email.Send(ctx, email, "Welcome!", "Thanks for registering"); err != nil {
        s.logger.Error("failed to send welcome email", err, "email", email)
        // Don't fail registration if email fails
    }

    s.logger.Info("user registered successfully", "id", user.ID, "email", email)
    return nil
}

// Real implementations

// PostgresRepository is production database implementation
type PostgresRepository struct {
    connString string
}

func NewPostgresRepository(connString string) *PostgresRepository {
    return &PostgresRepository{connString: connString}
}

func (r *PostgresRepository) GetByID(ctx context.Context, id string) (*User, error) {
    // Real database query here
    return &User{ID: id, Email: "user@example.com", Name: "John Doe"}, nil
}

func (r *PostgresRepository) Create(ctx context.Context, user *User) error {
    // Real database insert here
    fmt.Printf("PostgresRepository: Created user %s in database\n", user.ID)
    return nil
}

func (r *PostgresRepository) Update(ctx context.Context, user *User) error {
    // Real database update here
    return nil
}

// SMTPEmailSender is production email implementation
type SMTPEmailSender struct {
    host string
    port int
}

func NewSMTPEmailSender(host string, port int) *SMTPEmailSender {
    return &SMTPEmailSender{host: host, port: port}
}

func (s *SMTPEmailSender) Send(ctx context.Context, to, subject, body string) error {
    // Real SMTP sending here
    fmt.Printf("SMTPEmailSender: Sent email to %s: %s\n", to, subject)
    return nil
}

// ConsoleLogger is production logger implementation
type ConsoleLogger struct{}

func (l *ConsoleLogger) Info(msg string, fields ...interface{}) {
    fmt.Printf("[INFO] %s %v\n", msg, fields)
}

func (l *ConsoleLogger) Error(msg string, err error, fields ...interface{}) {
    fmt.Printf("[ERROR] %s: %v %v\n", msg, err, fields)
}

// Test implementations (mocks)

// InMemoryRepository is test implementation
type InMemoryRepository struct {
    users map[string]*User
}

func NewInMemoryRepository() *InMemoryRepository {
    return &InMemoryRepository{
        users: make(map[string]*User),
    }
}

func (r *InMemoryRepository) GetByID(ctx context.Context, id string) (*User, error) {
    user, ok := r.users[id]
    if !ok {
        return nil, errors.New("user not found")
    }
    return user, nil
}

func (r *InMemoryRepository) Create(ctx context.Context, user *User) error {
    r.users[user.ID] = user
    return nil
}

func (r *InMemoryRepository) Update(ctx context.Context, user *User) error {
    r.users[user.ID] = user
    return nil
}

// MockEmailSender records sent emails for testing
type MockEmailSender struct {
    SentEmails []string
}

func (m *MockEmailSender) Send(ctx context.Context, to, subject, body string) error {
    m.SentEmails = append(m.SentEmails, fmt.Sprintf("%s: %s", to, subject))
    return nil
}

// NoOpLogger is silent logger for tests
type NoOpLogger struct{}

func (l *NoOpLogger) Info(msg string, fields ...interface{})              {}
func (l *NoOpLogger) Error(msg string, err error, fields ...interface{}) {}

// Helper
func generateID() string {
    return fmt.Sprintf("user-%d", time.Now().UnixNano())
}

// Example usage
func main() {
    ctx := context.Background()

    // Production setup
    fmt.Println("=== Production Setup ===")
    prodRepo := NewPostgresRepository("postgres://localhost/mydb")
    prodEmail := NewSMTPEmailSender("smtp.example.com", 587)
    prodLogger := &ConsoleLogger{}
    prodService := NewUserService(prodRepo, prodEmail, prodLogger)

    if err := prodService.RegisterUser(ctx, "alice@example.com", "Alice"); err != nil {
        fmt.Printf("Registration failed: %v\n", err)
    }

    fmt.Println()

    // Test setup
    fmt.Println("=== Test Setup ===")
    testRepo := NewInMemoryRepository()
    testEmail := &MockEmailSender{}
    testLogger := &NoOpLogger{}
    testService := NewUserService(testRepo, testEmail, testLogger)

    if err := testService.RegisterUser(ctx, "bob@example.com", "Bob"); err != nil {
        fmt.Printf("Registration failed: %v\n", err)
    }

    fmt.Printf("Emails sent in test: %v\n", testEmail.SentEmails)
}
```

**Key Points:**
- Define small, focused interfaces (Interface Segregation Principle)
- Inject dependencies via constructor (constructor injection)
- Depend on interfaces, not concrete types
- Test implementations are easy to create
- Production and test code use same interface
- Mock implementations can record calls for assertions
- Interfaces should be defined by consumer, not provider

---

### 3.3 Middleware Pattern (HTTP)

**Pattern:** Chain request processing with composable middleware.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "time"
)

// Middleware type definition
type Middleware func(http.Handler) http.Handler

// Chain composes multiple middleware into one
func Chain(middlewares ...Middleware) Middleware {
    return func(final http.Handler) http.Handler {
        for i := len(middlewares) - 1; i >= 0; i-- {
            final = middlewares[i](final)
        }
        return final
    }
}

// LoggingMiddleware logs request details
func LoggingMiddleware(logger *log.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()

            // Wrap ResponseWriter to capture status code
            wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

            next.ServeHTTP(wrapped, r)

            logger.Printf(
                "%s %s %d %v",
                r.Method,
                r.URL.Path,
                wrapped.statusCode,
                time.Since(start),
            )
        })
    }
}

// responseWriter wraps http.ResponseWriter to capture status code
type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

// AuthMiddleware validates authentication
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")

        if token == "" {
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return
        }

        // Validate token (simplified)
        if token != "Bearer valid-token" {
            http.Error(w, "invalid token", http.StatusUnauthorized)
            return
        }

        // Add user info to context
        ctx := context.WithValue(r.Context(), "userID", "user-123")
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// RecoveryMiddleware recovers from panics
func RecoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                log.Printf("panic recovered: %v", err)
                http.Error(w, "internal server error", http.StatusInternalServerError)
            }
        }()

        next.ServeHTTP(w, r)
    })
}

// TimeoutMiddleware adds request timeout
func TimeoutMiddleware(timeout time.Duration) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            ctx, cancel := context.WithTimeout(r.Context(), timeout)
            defer cancel()

            done := make(chan struct{})

            go func() {
                next.ServeHTTP(w, r.WithContext(ctx))
                close(done)
            }()

            select {
            case <-done:
                return
            case <-ctx.Done():
                http.Error(w, "request timeout", http.StatusRequestTimeout)
            }
        })
    }
}

// RateLimitMiddleware implements simple rate limiting
func RateLimitMiddleware(requestsPerSecond int) Middleware {
    limiter := time.NewTicker(time.Second / time.Duration(requestsPerSecond))

    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            select {
            case <-limiter.C:
                next.ServeHTTP(w, r)
            default:
                http.Error(w, "rate limit exceeded", http.StatusTooManyRequests)
            }
        })
    }
}

// CORSMiddleware adds CORS headers
func CORSMiddleware(allowedOrigins []string) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            origin := r.Header.Get("Origin")

            // Check if origin is allowed
            allowed := false
            for _, o := range allowedOrigins {
                if o == "*" || o == origin {
                    allowed = true
                    break
                }
            }

            if allowed {
                w.Header().Set("Access-Control-Allow-Origin", origin)
                w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
                w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
            }

            if r.Method == "OPTIONS" {
                w.WriteHeader(http.StatusOK)
                return
            }

            next.ServeHTTP(w, r)
        })
    }
}

// Example handlers
func publicHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Public endpoint - no auth required\n")
}

func protectedHandler(w http.ResponseWriter, r *http.Request) {
    userID := r.Context().Value("userID")
    fmt.Fprintf(w, "Protected endpoint - user: %v\n", userID)
}

func slowHandler(w http.ResponseWriter, r *http.Request) {
    time.Sleep(2 * time.Second)
    fmt.Fprintf(w, "Slow endpoint completed\n")
}

// Example usage
func main() {
    logger := log.New(log.Writer(), "[HTTP] ", log.LstdFlags)

    // Global middleware applied to all routes
    globalMiddleware := Chain(
        RecoveryMiddleware,
        LoggingMiddleware(logger),
        CORSMiddleware([]string{"*"}),
    )

    // Auth middleware for protected routes
    authChain := Chain(
        globalMiddleware,
        AuthMiddleware,
    )

    // Timeout middleware for slow routes
    timeoutChain := Chain(
        globalMiddleware,
        TimeoutMiddleware(1*time.Second),
    )

    mux := http.NewServeMux()

    // Public routes
    mux.Handle("/public", globalMiddleware(http.HandlerFunc(publicHandler)))

    // Protected routes
    mux.Handle("/protected", authChain(http.HandlerFunc(protectedHandler)))

    // Slow route with timeout
    mux.Handle("/slow", timeoutChain(http.HandlerFunc(slowHandler)))

    fmt.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", mux))
}
```

**Key Points:**
- Middleware has signature `func(http.Handler) http.Handler`
- Chain middleware from outer to inner (reverse order)
- Use context to pass values between middleware
- Wrap `ResponseWriter` to capture status codes
- Recovery middleware should be outermost
- Middleware is composable and reusable
- Each middleware decides whether to call `next.ServeHTTP()`

---

### 3.4 Table-Driven Tests

**Pattern:** Use slice of test cases for comprehensive testing.

```go
package main

import (
    "errors"
    "testing"
)

// Function to test
func Add(a, b int) int {
    return a + b
}

func Divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// TestAdd demonstrates basic table-driven test
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a        int
        b        int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -2, -3},
        {"zero", 0, 0, 0},
        {"mixed signs", -5, 10, 5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// TestDivide demonstrates error handling in table-driven tests
func TestDivide(t *testing.T) {
    tests := []struct {
        name        string
        a           float64
        b           float64
        expected    float64
        expectError bool
        errorMsg    string
    }{
        {"simple division", 10.0, 2.0, 5.0, false, ""},
        {"division by zero", 5.0, 0.0, 0.0, true, "division by zero"},
        {"negative divisor", 10.0, -2.0, -5.0, false, ""},
        {"zero dividend", 0.0, 5.0, 0.0, false, ""},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Divide(tt.a, tt.b)

            // Check error expectation
            if tt.expectError {
                if err == nil {
                    t.Errorf("Divide(%f, %f) expected error but got nil", tt.a, tt.b)
                    return
                }
                if err.Error() != tt.errorMsg {
                    t.Errorf("Divide(%f, %f) error = %q; want %q", tt.a, tt.b, err.Error(), tt.errorMsg)
                }
                return
            }

            // Check success case
            if err != nil {
                t.Errorf("Divide(%f, %f) unexpected error: %v", tt.a, tt.b, err)
                return
            }

            if result != tt.expected {
                t.Errorf("Divide(%f, %f) = %f; want %f", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// TestWithSetupTeardown demonstrates test helpers
func TestWithSetupTeardown(t *testing.T) {
    tests := []struct {
        name  string
        input int
        want  int
    }{
        {"case 1", 1, 2},
        {"case 2", 2, 4},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Setup
            t.Logf("Setting up test: %s", tt.name)

            // Cleanup
            t.Cleanup(func() {
                t.Logf("Cleaning up test: %s", tt.name)
            })

            // Test logic
            result := tt.input * 2
            if result != tt.want {
                t.Errorf("got %d; want %d", result, tt.want)
            }
        })
    }
}

// TestParallel demonstrates parallel test execution
func TestParallel(t *testing.T) {
    tests := []struct {
        name  string
        input int
    }{
        {"test 1", 1},
        {"test 2", 2},
        {"test 3", 3},
    }

    for _, tt := range tests {
        tt := tt // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Run subtests in parallel

            // Simulate work
            result := tt.input * 2
            t.Logf("Result: %d", result)
        })
    }
}

// Benchmark with table-driven approach
func BenchmarkAdd(b *testing.B) {
    tests := []struct {
        name string
        a    int
        b    int
    }{
        {"small", 1, 2},
        {"medium", 100, 200},
        {"large", 10000, 20000},
    }

    for _, tt := range tests {
        b.Run(tt.name, func(b *testing.B) {
            for i := 0; i < b.N; i++ {
                Add(tt.a, tt.b)
            }
        })
    }
}

// TestHelpers demonstrates test helper functions
func TestHelpers(t *testing.T) {
    assertEqual := func(t *testing.T, got, want int) {
        t.Helper() // Marks function as test helper
        if got != want {
            t.Errorf("got %d; want %d", got, want)
        }
    }

    tests := []struct {
        name string
        a    int
        b    int
        want int
    }{
        {"add positive", 1, 2, 3},
        {"add negative", -1, -1, -2},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            assertEqual(t, result, tt.want)
        })
    }
}
```

**Key Points:**
- Use anonymous struct slice for test cases
- Name each test case with descriptive string
- Use `t.Run()` for subtests (enables parallel execution)
- Capture range variable for parallel tests (`tt := tt`)
- Use `t.Helper()` in helper functions for better error messages
- Include both success and error cases
- Use `t.Cleanup()` for test teardown
- Table-driven benchmarks with `b.Run()`

---

## 4. HTTP & API Development

### 4.1 Graceful Shutdown

**Pattern:** Cleanly shutdown HTTP server with context timeout.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

type Server struct {
    httpServer *http.Server
    logger     *log.Logger
}

func NewServer(addr string) *Server {
    mux := http.NewServeMux()
    mux.HandleFunc("/", handleRoot)
    mux.HandleFunc("/slow", handleSlow)

    return &Server{
        httpServer: &http.Server{
            Addr:         addr,
            Handler:      mux,
            ReadTimeout:  10 * time.Second,
            WriteTimeout: 10 * time.Second,
            IdleTimeout:  120 * time.Second,
        },
        logger: log.New(os.Stdout, "[Server] ", log.LstdFlags),
    }
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, World!\n")
}

func handleSlow(w http.ResponseWriter, r *http.Request) {
    // Simulate slow operation
    time.Sleep(5 * time.Second)
    fmt.Fprintf(w, "Slow operation completed\n")
}

// Start begins serving HTTP requests
func (s *Server) Start() error {
    s.logger.Printf("Starting server on %s", s.httpServer.Addr)

    // Start server in goroutine
    go func() {
        if err := s.httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            s.logger.Fatalf("Server failed: %v", err)
        }
    }()

    return nil
}

// Shutdown gracefully stops the server
func (s *Server) Shutdown(ctx context.Context) error {
    s.logger.Println("Shutting down server...")

    // Stop accepting new connections and wait for existing ones to complete
    if err := s.httpServer.Shutdown(ctx); err != nil {
        s.logger.Printf("Server shutdown error: %v", err)
        return err
    }

    s.logger.Println("Server stopped gracefully")
    return nil
}

// Run starts server and blocks until shutdown signal
func (s *Server) Run() error {
    // Start server
    if err := s.Start(); err != nil {
        return err
    }

    // Setup signal handling
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // Block until signal received
    sig := <-quit
    s.logger.Printf("Received signal: %v", sig)

    // Create shutdown context with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // Attempt graceful shutdown
    return s.Shutdown(ctx)
}

// Advanced: Server with background workers
type WorkerServer struct {
    *Server
    workerCtx    context.Context
    workerCancel context.CancelFunc
    workerDone   chan struct{}
}

func NewWorkerServer(addr string) *WorkerServer {
    ctx, cancel := context.WithCancel(context.Background())

    ws := &WorkerServer{
        Server:       NewServer(addr),
        workerCtx:    ctx,
        workerCancel: cancel,
        workerDone:   make(chan struct{}),
    }

    return ws
}

// startBackgroundWorker simulates background processing
func (ws *WorkerServer) startBackgroundWorker() {
    go func() {
        defer close(ws.workerDone)

        ticker := time.NewTicker(2 * time.Second)
        defer ticker.Stop()

        for {
            select {
            case <-ticker.C:
                ws.logger.Println("Background worker processing...")
            case <-ws.workerCtx.Done():
                ws.logger.Println("Background worker stopping...")
                return
            }
        }
    }()
}

// Run starts server with background workers
func (ws *WorkerServer) Run() error {
    // Start background workers
    ws.startBackgroundWorker()

    // Start HTTP server
    if err := ws.Start(); err != nil {
        return err
    }

    // Setup signal handling
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // Block until signal received
    sig := <-quit
    ws.logger.Printf("Received signal: %v", sig)

    // Shutdown sequence
    // 1. Cancel worker context
    ws.workerCancel()

    // 2. Wait for workers to stop (with timeout)
    workerTimeout := time.After(10 * time.Second)
    select {
    case <-ws.workerDone:
        ws.logger.Println("Background workers stopped")
    case <-workerTimeout:
        ws.logger.Println("Background workers did not stop in time")
    }

    // 3. Shutdown HTTP server
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    return ws.Shutdown(ctx)
}

func main() {
    // Example 1: Simple graceful shutdown
    // server := NewServer(":8080")
    // if err := server.Run(); err != nil {
    //     log.Fatalf("Server error: %v", err)
    // }

    // Example 2: Server with background workers
    server := NewWorkerServer(":8080")
    if err := server.Run(); err != nil {
        log.Fatalf("Server error: %v", err)
    }
}
```

**Key Points:**
- Use `signal.Notify()` to catch SIGINT/SIGTERM
- Call `Shutdown()` with timeout context (typically 30s)
- `Shutdown()` stops accepting new connections
- Existing connections complete before shutdown
- Cancel background workers before HTTP shutdown
- Use channels to coordinate worker completion
- Set appropriate timeouts for all operations

---

### 4.2 HTTP Client with Retry Logic

**Pattern:** Resilient HTTP client with exponential backoff and context.

```go
package main

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "time"
)

// RetryConfig defines retry behavior
type RetryConfig struct {
    MaxRetries     int
    InitialBackoff time.Duration
    MaxBackoff     time.Duration
    Multiplier     float64
}

// DefaultRetryConfig provides sensible defaults
func DefaultRetryConfig() RetryConfig {
    return RetryConfig{
        MaxRetries:     3,
        InitialBackoff: 100 * time.Millisecond,
        MaxBackoff:     10 * time.Second,
        Multiplier:     2.0,
    }
}

// HTTPClient wraps http.Client with retry logic
type HTTPClient struct {
    client *http.Client
    retry  RetryConfig
}

// NewHTTPClient creates client with timeout and retry config
func NewHTTPClient(timeout time.Duration, retry RetryConfig) *HTTPClient {
    return &HTTPClient{
        client: &http.Client{
            Timeout: timeout,
            Transport: &http.Transport{
                MaxIdleConns:        100,
                MaxIdleConnsPerHost: 10,
                IdleConnTimeout:     90 * time.Second,
            },
        },
        retry: retry,
    }
}

// Do executes request with retry logic
func (c *HTTPClient) Do(ctx context.Context, req *http.Request) (*http.Response, error) {
    var resp *http.Response
    var err error

    backoff := c.retry.InitialBackoff

    for attempt := 0; attempt <= c.retry.MaxRetries; attempt++ {
        // Clone request for retry (body can only be read once)
        reqClone := req.Clone(ctx)

        // Execute request
        resp, err = c.client.Do(reqClone)

        // Success
        if err == nil && !c.shouldRetry(resp.StatusCode) {
            return resp, nil
        }

        // Last attempt - return error
        if attempt == c.retry.MaxRetries {
            if err != nil {
                return nil, fmt.Errorf("max retries exceeded: %w", err)
            }
            return resp, fmt.Errorf("max retries exceeded: status %d", resp.StatusCode)
        }

        // Close response body before retry
        if resp != nil {
            io.Copy(io.Discard, resp.Body)
            resp.Body.Close()
        }

        // Wait with exponential backoff
        select {
        case <-time.After(backoff):
            // Increase backoff for next attempt
            backoff = time.Duration(float64(backoff) * c.retry.Multiplier)
            if backoff > c.retry.MaxBackoff {
                backoff = c.retry.MaxBackoff
            }
        case <-ctx.Done():
            return nil, ctx.Err()
        }
    }

    return resp, err
}

// shouldRetry determines if request should be retried based on status code
func (c *HTTPClient) shouldRetry(statusCode int) bool {
    // Retry on server errors and rate limiting
    switch statusCode {
    case http.StatusTooManyRequests,     // 429
        http.StatusInternalServerError,  // 500
        http.StatusBadGateway,           // 502
        http.StatusServiceUnavailable,   // 503
        http.StatusGatewayTimeout:       // 504
        return true
    }
    return false
}

// Get performs GET request with retry
func (c *HTTPClient) Get(ctx context.Context, url string) (*http.Response, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return nil, err
    }
    return c.Do(ctx, req)
}

// Post performs POST request with retry
func (c *HTTPClient) Post(ctx context.Context, url string, body io.Reader) (*http.Response, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, body)
    if err != nil {
        return nil, err
    }
    req.Header.Set("Content-Type", "application/json")
    return c.Do(ctx, req)
}

// Example usage
func main() {
    // Create client with 5s timeout and custom retry config
    client := NewHTTPClient(5*time.Second, RetryConfig{
        MaxRetries:     3,
        InitialBackoff: 200 * time.Millisecond,
        MaxBackoff:     5 * time.Second,
        Multiplier:     2.0,
    })

    // Create context with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // Make request
    resp, err := client.Get(ctx, "https://api.example.com/data")
    if err != nil {
        fmt.Printf("Request failed: %v\n", err)
        return
    }
    defer resp.Body.Close()

    // Read response
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("Failed to read response: %v\n", err)
        return
    }

    fmt.Printf("Response: %s\n", body)
}
```

**Key Points:**
- Use `context.Context` for request cancellation
- Clone request for retry (body can only be read once)
- Implement exponential backoff with max limit
- Retry on specific status codes (429, 500-504)
- Close response body between retries
- Set timeout on client and context
- Configure connection pool settings

---

### 4.3 HTTP Handler Testing

**Pattern:** Test HTTP handlers with httptest package.

```go
package main

import (
    "encoding/json"
    "io"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

// User model
type User struct {
    ID    string `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

// Handler functions to test
func handleGetUser(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
        return
    }

    userID := r.URL.Query().Get("id")
    if userID == "" {
        http.Error(w, "missing user id", http.StatusBadRequest)
        return
    }

    // Simulate database fetch
    user := User{
        ID:    userID,
        Name:  "John Doe",
        Email: "john@example.com",
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func handleCreateUser(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var user User
    if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    if user.Email == "" {
        http.Error(w, "email required", http.StatusBadRequest)
        return
    }

    user.ID = "generated-id"

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}

// Tests

func TestHandleGetUser(t *testing.T) {
    tests := []struct {
        name           string
        queryParams    string
        expectedStatus int
        expectedBody   string
    }{
        {
            name:           "success",
            queryParams:    "?id=123",
            expectedStatus: http.StatusOK,
            expectedBody:   `{"id":"123","name":"John Doe","email":"john@example.com"}`,
        },
        {
            name:           "missing id",
            queryParams:    "",
            expectedStatus: http.StatusBadRequest,
            expectedBody:   "missing user id\n",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Create request
            req := httptest.NewRequest(http.MethodGet, "/user"+tt.queryParams, nil)

            // Create response recorder
            rr := httptest.NewRecorder()

            // Call handler
            handleGetUser(rr, req)

            // Check status code
            if rr.Code != tt.expectedStatus {
                t.Errorf("handler returned wrong status: got %v want %v", rr.Code, tt.expectedStatus)
            }

            // Check response body
            body := strings.TrimSpace(rr.Body.String())
            expectedBody := strings.TrimSpace(tt.expectedBody)
            if body != expectedBody {
                t.Errorf("handler returned wrong body:\ngot  %v\nwant %v", body, expectedBody)
            }
        })
    }
}

func TestHandleCreateUser(t *testing.T) {
    tests := []struct {
        name           string
        requestBody    string
        expectedStatus int
        checkResponse  func(t *testing.T, body string)
    }{
        {
            name:           "success",
            requestBody:    `{"name":"Jane","email":"jane@example.com"}`,
            expectedStatus: http.StatusCreated,
            checkResponse: func(t *testing.T, body string) {
                var user User
                if err := json.Unmarshal([]byte(body), &user); err != nil {
                    t.Errorf("failed to parse response: %v", err)
                }
                if user.ID == "" {
                    t.Error("expected user ID to be set")
                }
                if user.Email != "jane@example.com" {
                    t.Errorf("expected email jane@example.com, got %s", user.Email)
                }
            },
        },
        {
            name:           "invalid json",
            requestBody:    `{invalid}`,
            expectedStatus: http.StatusBadRequest,
            checkResponse:  nil,
        },
        {
            name:           "missing email",
            requestBody:    `{"name":"Jane"}`,
            expectedStatus: http.StatusBadRequest,
            checkResponse:  nil,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Create request with body
            req := httptest.NewRequest(
                http.MethodPost,
                "/user",
                strings.NewReader(tt.requestBody),
            )
            req.Header.Set("Content-Type", "application/json")

            // Create response recorder
            rr := httptest.NewRecorder()

            // Call handler
            handleCreateUser(rr, req)

            // Check status code
            if rr.Code != tt.expectedStatus {
                t.Errorf("handler returned wrong status: got %v want %v", rr.Code, tt.expectedStatus)
            }

            // Run custom response checks
            if tt.checkResponse != nil {
                tt.checkResponse(t, rr.Body.String())
            }
        })
    }
}

// TestServerIntegration demonstrates testing with httptest.Server
func TestServerIntegration(t *testing.T) {
    // Create test server
    mux := http.NewServeMux()
    mux.HandleFunc("/user", func(w http.ResponseWriter, r *http.Request) {
        if r.Method == http.MethodGet {
            handleGetUser(w, r)
        } else if r.Method == http.MethodPost {
            handleCreateUser(w, r)
        }
    })

    server := httptest.NewServer(mux)
    defer server.Close()

    // Test GET request
    resp, err := http.Get(server.URL + "/user?id=456")
    if err != nil {
        t.Fatalf("GET request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        t.Errorf("GET status: got %v want %v", resp.StatusCode, http.StatusOK)
    }

    // Test POST request
    postBody := strings.NewReader(`{"name":"Alice","email":"alice@example.com"}`)
    resp, err = http.Post(server.URL+"/user", "application/json", postBody)
    if err != nil {
        t.Fatalf("POST request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusCreated {
        t.Errorf("POST status: got %v want %v", resp.StatusCode, http.StatusCreated)
    }

    body, _ := io.ReadAll(resp.Body)
    var user User
    json.Unmarshal(body, &user)

    if user.ID == "" {
        t.Error("expected user ID to be generated")
    }
}
```

**Key Points:**
- Use `httptest.NewRequest()` to create test requests
- Use `httptest.NewRecorder()` to capture responses
- Use `httptest.NewServer()` for integration tests
- Test both success and error cases
- Validate status codes, headers, and response bodies
- Use table-driven tests for handler testing
- Test with real HTTP client in integration tests

---

## 5. Performance & Best Practices

### 5.1 sync.Pool for Object Reuse

**Pattern:** Reduce GC pressure by reusing objects.

```go
package main

import (
    "bytes"
    "fmt"
    "sync"
)

// Example 1: Buffer pooling for string operations
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

// ProcessString demonstrates buffer reuse
func ProcessString(data string) string {
    // Get buffer from pool
    buf := bufferPool.Get().(*bytes.Buffer)

    // Reset buffer (important!)
    buf.Reset()

    // Return to pool when done
    defer bufferPool.Put(buf)

    // Use buffer
    buf.WriteString("Processed: ")
    buf.WriteString(data)

    return buf.String()
}

// Example 2: Custom struct pooling
type Request struct {
    ID   string
    Data []byte
}

var requestPool = sync.Pool{
    New: func() interface{} {
        return &Request{
            Data: make([]byte, 0, 1024), // Pre-allocate capacity
        }
    },
}

// GetRequest gets a request from pool
func GetRequest() *Request {
    req := requestPool.Get().(*Request)
    req.ID = ""
    req.Data = req.Data[:0] // Reset slice but keep capacity
    return req
}

// PutRequest returns request to pool
func PutRequest(req *Request) {
    // Clear sensitive data
    req.ID = ""
    req.Data = req.Data[:0]
    requestPool.Put(req)
}

// Example 3: Worker with connection pooling
type Connection struct {
    id   int
    conn interface{} // Simplified - would be real connection
}

type ConnectionPool struct {
    pool sync.Pool
}

func NewConnectionPool() *ConnectionPool {
    return &ConnectionPool{
        pool: sync.Pool{
            New: func() interface{} {
                // Create expensive connection
                return &Connection{
                    conn: createConnection(),
                }
            },
        },
    }
}

func createConnection() interface{} {
    // Simulate expensive operation
    return "database-connection"
}

func (p *ConnectionPool) Acquire() *Connection {
    return p.pool.Get().(*Connection)
}

func (p *ConnectionPool) Release(conn *Connection) {
    // Clean up connection state
    p.pool.Put(conn)
}

// Example usage
func main() {
    // Example 1: Buffer pooling
    result1 := ProcessString("hello")
    result2 := ProcessString("world")
    fmt.Printf("%s\n%s\n", result1, result2)

    // Example 2: Request pooling
    req := GetRequest()
    req.ID = "req-123"
    req.Data = append(req.Data, []byte("data")...)
    fmt.Printf("Request: %s\n", req.ID)
    PutRequest(req)

    // Example 3: Connection pooling
    pool := NewConnectionPool()
    conn := pool.Acquire()
    fmt.Printf("Using connection: %v\n", conn.conn)
    pool.Release(conn)
}
```

**Key Points:**
- Use `sync.Pool` for frequently allocated/deallocated objects
- Always reset object state before returning to pool
- Pool is safe for concurrent use
- Objects in pool may be GC'd at any time
- Best for reducing allocation pressure, not guaranteed reuse
- Pre-allocate capacity in `New()` function
- Clear sensitive data before returning to pool

---

### 5.2 Avoiding Goroutine Leaks

**Pattern:** Ensure all goroutines terminate properly.

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// ❌ BAD: Goroutine leak - channel never closed
func badLeakExample() {
    ch := make(chan int)

    go func() {
        for val := range ch {
            fmt.Println(val)
        }
        // This goroutine leaks if ch is never closed
    }()

    // If we forget to close ch, goroutine stays blocked forever
}

// ✅ GOOD: Always close channels
func goodChannelClose() {
    ch := make(chan int)

    go func() {
        for val := range ch {
            fmt.Println(val)
        }
    }()

    ch <- 1
    ch <- 2
    close(ch) // Goroutine will exit after processing

    time.Sleep(100 * time.Millisecond) // Wait for goroutine
}

// ❌ BAD: Goroutine leak - no cancellation
func badNoCancellation() {
    go func() {
        for {
            // Infinite loop with no way to stop
            time.Sleep(1 * time.Second)
            fmt.Println("working...")
        }
    }()
}

// ✅ GOOD: Use context for cancellation
func goodContextCancellation() context.CancelFunc {
    ctx, cancel := context.WithCancel(context.Background())

    go func() {
        for {
            select {
            case <-ctx.Done():
                fmt.Println("goroutine stopped")
                return
            case <-time.After(1 * time.Second):
                fmt.Println("working...")
            }
        }
    }()

    return cancel // Caller can cancel when done
}

// ❌ BAD: Timeout goroutine leak
func badTimeoutLeak() {
    ch := make(chan string)

    go func() {
        // Simulate slow operation
        time.Sleep(5 * time.Second)
        ch <- "result" // May never be received if caller timed out
    }()

    select {
    case result := <-ch:
        fmt.Println(result)
    case <-time.After(1 * time.Second):
        fmt.Println("timeout")
        // Goroutine still running and will leak
    }
}

// ✅ GOOD: Buffered channel prevents sender block
func goodTimeoutWithBuffer() {
    ch := make(chan string, 1) // Buffered channel

    go func() {
        time.Sleep(5 * time.Second)
        ch <- "result" // Won't block even if no receiver
    }()

    select {
    case result := <-ch:
        fmt.Println(result)
    case <-time.After(1 * time.Second):
        fmt.Println("timeout")
        // Goroutine can still send and exit
    }
}

// ✅ GOOD: Context-aware goroutine
func goodTimeoutWithContext() {
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
    defer cancel()

    ch := make(chan string, 1)

    go func() {
        select {
        case <-ctx.Done():
            return // Exit on context cancellation
        case <-time.After(5 * time.Second):
            select {
            case ch <- "result":
            case <-ctx.Done():
            }
        }
    }()

    select {
    case result := <-ch:
        fmt.Println(result)
    case <-ctx.Done():
        fmt.Println("timeout")
    }
}

// Goroutine leak detector pattern
type LeakDetector struct {
    ctx    context.Context
    cancel context.CancelFunc
    done   chan struct{}
}

func NewLeakDetector() *LeakDetector {
    ctx, cancel := context.WithCancel(context.Background())
    return &LeakDetector{
        ctx:    ctx,
        cancel: cancel,
        done:   make(chan struct{}),
    }
}

func (d *LeakDetector) Start(work func(context.Context)) {
    go func() {
        defer close(d.done)
        work(d.ctx)
    }()
}

func (d *LeakDetector) Stop(timeout time.Duration) error {
    d.cancel()

    select {
    case <-d.done:
        return nil
    case <-time.After(timeout):
        return fmt.Errorf("goroutine did not stop within %v", timeout)
    }
}

// Example usage
func main() {
    // Good example: Channel close
    fmt.Println("=== Good: Channel close ===")
    goodChannelClose()

    // Good example: Context cancellation
    fmt.Println("\n=== Good: Context cancellation ===")
    cancel := goodContextCancellation()
    time.Sleep(2 * time.Second)
    cancel()
    time.Sleep(100 * time.Millisecond)

    // Good example: Timeout with buffer
    fmt.Println("\n=== Good: Timeout with buffer ===")
    goodTimeoutWithBuffer()

    // Good example: Leak detector
    fmt.Println("\n=== Good: Leak detector ===")
    detector := NewLeakDetector()
    detector.Start(func(ctx context.Context) {
        for {
            select {
            case <-ctx.Done():
                fmt.Println("Work stopped")
                return
            case <-time.After(500 * time.Millisecond):
                fmt.Println("Working...")
            }
        }
    })

    time.Sleep(2 * time.Second)
    if err := detector.Stop(1 * time.Second); err != nil {
        fmt.Printf("Error: %v\n", err)
    }
}
```

**Key Points:**
- Always provide exit mechanism for goroutines
- Use `context.Context` for cancellation
- Close channels when done sending
- Use buffered channels to prevent sender blocking
- Include `ctx.Done()` in select statements
- Implement timeout patterns with context
- Use leak detector pattern in tests
- Run with `-race` flag to detect issues

---

### 5.3 Effective Interface Design

**Pattern:** Design small, focused interfaces following Go idioms.

```go
package main

import (
    "fmt"
    "io"
    "strings"
)

// ❌ BAD: Large interface with many methods
type BadDatabase interface {
    Connect() error
    Disconnect() error
    Query(sql string) ([]interface{}, error)
    Execute(sql string) error
    BeginTransaction() error
    Commit() error
    Rollback() error
    Ping() error
    Stats() interface{}
}

// ✅ GOOD: Small, focused interfaces
type Querier interface {
    Query(sql string) ([]interface{}, error)
}

type Executor interface {
    Execute(sql string) error
}

type Transactional interface {
    BeginTransaction() error
    Commit() error
    Rollback() error
}

// Compose interfaces when needed
type Database interface {
    Querier
    Executor
    Transactional
}

// ✅ GOOD: Single-method interfaces (idiomatic Go)
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// Compose for specific needs
type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

// Example: Minimal interface for testing
type UserFetcher interface {
    GetUser(id string) (*User, error)
}

type User struct {
    ID   string
    Name string
}

// Service depends on minimal interface
type UserService struct {
    fetcher UserFetcher
}

func (s *UserService) FormatUser(id string) string {
    user, err := s.fetcher.GetUser(id)
    if err != nil {
        return "unknown"
    }
    return user.Name
}

// Production implementation
type DatabaseUserFetcher struct {
    db *Database
}

func (f *DatabaseUserFetcher) GetUser(id string) (*User, error) {
    // Real database query
    return &User{ID: id, Name: "John"}, nil
}

// Test implementation
type MockUserFetcher struct {
    users map[string]*User
}

func (m *MockUserFetcher) GetUser(id string) (*User, error) {
    user, ok := m.users[id]
    if !ok {
        return nil, fmt.Errorf("user not found")
    }
    return user, nil
}

// ✅ GOOD: Accept interfaces, return structs
func ProcessData(r io.Reader) (string, error) {
    data, err := io.ReadAll(r)
    if err != nil {
        return "", err
    }
    return string(data), nil
}

// Returns concrete type
func NewStringReader(s string) *strings.Reader {
    return strings.NewReader(s)
}

// Example: Polymorphism with interfaces
type Shape interface {
    Area() float64
}

type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return 3.14159 * c.Radius * c.Radius
}

type Rectangle struct {
    Width  float64
    Height float64
}

func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

func TotalArea(shapes []Shape) float64 {
    var total float64
    for _, shape := range shapes {
        total += shape.Area()
    }
    return total
}

// Example: Interface satisfaction is implicit
type Logger interface {
    Log(message string)
}

type ConsoleLogger struct{}

func (l ConsoleLogger) Log(message string) {
    fmt.Println(message)
}

// No explicit "implements Logger" declaration needed

func UseLogger(logger Logger) {
    logger.Log("Hello from logger")
}

func main() {
    // Example 1: Service with minimal interface
    service := &UserService{
        fetcher: &MockUserFetcher{
            users: map[string]*User{
                "1": {ID: "1", Name: "Alice"},
            },
        },
    }
    fmt.Println(service.FormatUser("1"))

    // Example 2: Accept interfaces, return structs
    reader := NewStringReader("Hello, World!")
    data, _ := ProcessData(reader)
    fmt.Println(data)

    // Example 3: Polymorphism
    shapes := []Shape{
        Circle{Radius: 5},
        Rectangle{Width: 10, Height: 5},
    }
    fmt.Printf("Total area: %.2f\n", TotalArea(shapes))

    // Example 4: Implicit interface satisfaction
    UseLogger(ConsoleLogger{})
}
```

**Key Points:**
- Keep interfaces small (prefer single-method interfaces)
- Define interfaces at point of use, not implementation
- Accept interfaces, return structs
- Interface satisfaction is implicit (no "implements" keyword)
- Compose interfaces from smaller ones
- Use empty interface `interface{}` sparingly (prefer `any` in Go 1.18+)
- Standard library interfaces (`io.Reader`, `io.Writer`) are excellent examples

---

## 6. Common Mistakes to Avoid

### Concurrency Mistakes

1. **Not closing channels**: Always close channels when done sending
2. **Forgetting buffered channels**: Use buffered channels for fire-and-forget patterns
3. **Ignoring context**: Always pass and respect `context.Context`
4. **Goroutine leaks**: Ensure all goroutines have exit path
5. **Not using `sync.WaitGroup`**: Wait for goroutines before exit

### Error Handling Mistakes

1. **Using `panic` for errors**: Reserve `panic` for truly exceptional situations
2. **Ignoring errors**: Always check and handle errors (`if err != nil`)
3. **Not wrapping errors**: Use `fmt.Errorf()` with `%w` to preserve error chain
4. **Using string comparison**: Use `errors.Is()` and `errors.As()` instead

### Performance Mistakes

1. **Premature optimization**: Profile first, optimize later
2. **Not reusing objects**: Use `sync.Pool` for frequently allocated objects
3. **Unbounded goroutines**: Use worker pools to limit concurrency
4. **Ignoring memory allocations**: Use pprof to identify allocation hotspots
5. **Blocking on channels**: Use `select` with `default` for non-blocking operations

### Design Mistakes

1. **Large interfaces**: Keep interfaces small and focused
2. **Pointer to interface**: Pass interface values, not pointers to interfaces
3. **Not using composition**: Prefer embedding over inheritance-like patterns
4. **Exporting too much**: Only export what's necessary
5. **Not following conventions**: Use `go fmt`, `go vet`, and golangci-lint

---

## Summary

This document covers **20 production-ready Go patterns** across 5 major categories:

**Concurrency** (4 patterns):
- Worker pools with context cancellation
- Fan-out/fan-in for parallelism
- Pipeline pattern with stages
- Advanced select patterns

**Error Handling** (3 patterns):
- errors.Is/errors.As for type-safe checking
- Error wrapping with context preservation
- Concurrent error aggregation

**Design Patterns** (4 patterns):
- Functional options for flexible configuration
- Interface-based dependency injection
- HTTP middleware chains
- Table-driven tests

**HTTP & API** (3 patterns):
- Graceful shutdown with signal handling
- HTTP client with retry logic
- HTTP handler testing with httptest

**Performance** (3 patterns):
- sync.Pool for object reuse
- Goroutine leak prevention
- Effective interface design

All patterns use **Go 1.21+ features**, include **context awareness**, demonstrate **idiomatic Go code**, and are **production-ready** with proper error handling and testing examples.

---

**References:**
- Official Go Blog: https://go.dev/blog/
- Go by Example: https://gobyexample.com/
- Effective Go: https://go.dev/doc/effective_go
- Go Code Review Comments: https://github.com/golang/go/wiki/CodeReviewComments
