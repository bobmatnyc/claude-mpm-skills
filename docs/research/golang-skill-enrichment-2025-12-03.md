# Go/Golang Skill Enrichment Research

**Research Date**: 2025-12-03
**Researcher**: Research Agent
**Objective**: Identify high-quality Go skill topics to enrich claude-mpm-skills library

---

## Executive Summary

This research identifies authoritative Go development resources and recommends 5 high-priority skills to complement our existing `golang-engineer` agent. The current agent provides strong foundation in concurrency patterns and idiomatic Go, but lacks coverage of specialized domains like testing strategies, database patterns, HTTP frameworks, CLI tools, and observability.

**Key Findings**:
- Official Go documentation remains authoritative but dated (Effective Go from 2009)
- Google's Go Style Guide and recent 2025 community resources provide current best practices
- Go ecosystem in 2025 emphasizes simplicity, productivity, and cloud-native patterns
- Major gaps in current coverage: testing frameworks, database integration, HTTP routers, CLI tools, observability

**Recommended Priority Skills**:
1. **Go Testing & Quality Assurance** (HIGHEST PRIORITY)
2. **Go Database Patterns & Migrations** (HIGH PRIORITY)
3. **Go HTTP APIs & Web Frameworks** (HIGH PRIORITY)
4. **Go CLI Development with Cobra/Viper** (MEDIUM PRIORITY)
5. **Go Observability & Monitoring** (MEDIUM PRIORITY)

---

## 1. Authoritative Go Sources (2025)

### Official Go Resources

#### Primary Documentation
- **Effective Go** (go.dev/doc/effective_go)
  - Status: Classic guide, written in 2009, not significantly updated
  - Limitation: Doesn't cover modules, generics, or modern ecosystem
  - Use: Core language understanding, foundational patterns

- **Official Go Documentation** (go.dev/doc/)
  - Status: Current and maintained
  - Coverage: Language spec, tutorials, module management
  - Strength: Authoritative source for language features

- **Go Blog** (go.dev/blog/)
  - Status: Actively updated with new patterns
  - Notable: "Pipelines and cancellation" for concurrency patterns
  - Strength: Deep dives into specific features and patterns

#### Google's Go Style Guide
- **Go Style Guide** (google.github.io/styleguide/go/)
  - Status: Current, actively maintained
  - Coverage: Style decisions, best practices, patterns evolved at Google
  - Strength: Production-tested patterns from large-scale Go usage
  - Note: Not canonical but highly recommended

### Community Resources (2025)

#### Respected Authors & Books

**Jon Bodner**
- Book: "Learning Go, 2nd Edition" (January 2024)
- Role: Staff Engineer at Datadog
- Focus: Design patterns, idiomatic approaches, generics
- Audience: 150,000+ blog readers
- Authority: Frequent Go conference speaker

**Dave Cheney**
- Website: dave.cheney.net/practical-go
- Role: Open source contributor, Go project member
- Focus: Practical Go patterns, performance
- Recent: Content from February 2024 and November 2025

#### Recent 2025 Resources

**JetBrains Go Blog**
- "The Go Ecosystem in 2025: Key Trends in Frameworks, Tools, and Developer Practices" (November 2025)
- Coverage: Framework trends, tooling evolution, developer practices
- Insight: Go remains stable, mature, focused on backend/infrastructure/cloud-native

**Leapcell Medium Articles**
- "Go Coding Official Standards and Best Practices" (August 2025)
- Coverage: Official standards, formatting, community conventions
- Strength: Synthesizes official docs with community consensus

**Community Guides (2025)**
- "Go Concurrency 2025: Goroutines, Channels & Clean Patterns" (DEV Community)
- "7 Powerful Golang Concurrency Patterns That Will Transform Your Code in 2025" (March 2025)
- "Mastering Concurrency in Go" (November 2025)

---

## 2. Current golang-engineer Agent Analysis

### Location
- **File**: `.claude/agents/golang_engineer.md`
- **Type**: Engineer agent (not skill)
- **Version**: 1.0.0
- **Last Updated**: 2025-10-17

### Coverage Strengths

The current agent provides excellent coverage of:

#### Core Language Features
- Go 1.23-1.24 modern features
- Interface-based design and composition
- Error handling with errors.Is/As
- Type system and generics (basic)

#### Concurrency Patterns (COMPREHENSIVE)
- ✅ Fan-out/fan-in patterns
- ✅ Worker pools with controlled concurrency
- ✅ Pipeline patterns for streaming
- ✅ Context cancellation and timeout propagation
- ✅ Goroutine lifecycle management
- ✅ Channel patterns (buffered/unbuffered, direction)
- ✅ Sync primitives (WaitGroup, Mutex, RWMutex, Once, errgroup)

#### Development Practices
- ✅ Table-driven tests (mentioned)
- ✅ Race detector usage
- ✅ Benchmarking (mentioned)
- ✅ Standard project layout reference
- ✅ Code quality standards (gofmt, golangci-lint)
- ✅ Performance profiling with pprof

### Coverage Gaps (HIGH PRIORITY)

#### 1. Testing Frameworks & Strategies ❌
**Missing**:
- Testify assertions and suite patterns
- Gomock and mockery for interface mocking
- Table-driven test structure details
- Integration testing patterns
- Test fixtures and setup/teardown
- Coverage reporting and CI integration

**Current**: Only mentions "table-driven tests" without implementation details

#### 2. Database Patterns ❌
**Missing**:
- sqlx extensions for database/sql
- pgx driver patterns for PostgreSQL
- Migration tools (golang-migrate, goose, sql-migrate)
- Connection pooling and lifecycle
- Transaction patterns and error handling
- Query building patterns
- Repository pattern implementation

**Current**: No database coverage at all

#### 3. HTTP Frameworks & Routers ❌
**Missing**:
- Chi, Gin, Echo, Fiber framework comparison
- Middleware patterns and chains
- Request validation with struct tags
- Response serialization patterns
- Route grouping and versioning
- HTTP client best practices
- REST API design patterns

**Current**: No web framework guidance

#### 4. CLI Development ❌
**Missing**:
- Cobra command structure and patterns
- Viper configuration management
- Flag binding and environment variables
- Subcommand organization
- Shell completion generation
- CLI testing strategies

**Current**: No CLI tooling coverage

#### 5. Observability & Monitoring ❌
**Missing**:
- OpenTelemetry instrumentation
- Prometheus metrics integration
- Distributed tracing patterns
- Structured logging practices
- Health check endpoints
- Graceful shutdown patterns

**Current**: Mentions "logging for debugging" but no structured approach

#### 6. Error Handling Deep Dive ⚠️
**Partial Coverage**:
- ✅ errors.Is/As basics mentioned
- ❌ Custom error types design
- ❌ Error wrapping patterns with %w
- ❌ Sentinel errors vs. type assertions
- ❌ Error handling in concurrent code

#### 7. Context Package Patterns ⚠️
**Partial Coverage**:
- ✅ Context cancellation mentioned
- ❌ WithValue best practices and anti-patterns
- ❌ Deadline vs. Timeout distinction
- ❌ Context propagation in middleware
- ❌ Testing with contexts

#### 8. Generics Best Practices ⚠️
**Minimal Coverage**:
- Mentioned as "Go 1.23-1.24" feature
- ❌ Type parameters and constraints
- ❌ When to use vs. interfaces
- ❌ Generic data structures
- ❌ Constraint composition

#### 9. Standard Library Mastery ⚠️
**Basic Coverage**:
- ✅ Mentions sync package
- ❌ net/http patterns (Go 1.22+ routing)
- ❌ encoding/json best practices
- ❌ time package patterns
- ❌ io.Reader/Writer patterns

#### 10. Project Structure & Organization ⚠️
**Minimal Coverage**:
- ✅ Links to golang-standards/project-layout
- ❌ When to use cmd/ vs. internal/ vs. pkg/
- ❌ Module organization for libraries vs. applications
- ❌ Mono-repo vs. multi-repo patterns
- ❌ Dependency management with go.mod

---

## 3. High-Quality Skill Topics (Prioritized)

### Priority 1: Go Testing & Quality Assurance (CRITICAL GAP)

**Rationale**: Testing is fundamental to Go development, but current agent only mentions it in passing.

#### Coverage Should Include:

**Table-Driven Tests (Deep Dive)**
- Struct slice pattern for test cases
- Subtest organization with t.Run()
- Parallel test execution with t.Parallel()
- Test helpers and setup functions
- Golden file testing patterns

**Testing Frameworks**
- **Testify**: Assertions, suites, mocks
  - assert vs. require package differences
  - Suite setup/teardown patterns
  - Mock expectations and verification
- **Gomock**: Interface mocking
  - EXPECT() patterns and call ordering
  - Combining with table-driven tests
  - Custom matchers
- **Mockery**: Automatic mock generation

**Test Organization**
- Test file naming conventions (*_test.go)
- Internal tests vs. external tests (package vs. package_test)
- Test fixtures and data setup
- Integration vs. unit test separation
- Test coverage tools and reporting

**Advanced Testing**
- Benchmark tests with b.N loops
- Fuzz testing (Go 1.18+)
- Race detector integration
- httptest package for HTTP testing
- testcontainers for integration testing

**CI/CD Integration**
- Coverage reporting (go test -cover)
- Test result formats (JSON, JUnit)
- Parallel test execution in CI
- Test caching strategies

**Key Resources**:
- "Go Unit Testing: Structure & Best Practices" (November 2025)
- Official Go Wiki: TableDrivenTests
- Testify documentation and examples
- Gomock integration patterns

**Use Cases**:
- Writing comprehensive test suites for Go libraries
- Setting up CI/CD testing pipelines
- Mocking external dependencies in tests
- Performance benchmarking critical paths
- Ensuring race-free concurrent code

---

### Priority 2: Go Database Patterns & Migrations (CRITICAL GAP)

**Rationale**: Database integration is essential for most Go applications, but completely absent from current coverage.

#### Coverage Should Include:

**Database Libraries**
- **database/sql** standard library patterns
  - Connection pooling configuration
  - Prepared statements and query patterns
  - Transaction handling with Begin/Commit/Rollback
  - Context integration for timeouts
- **sqlx** extensions
  - Named queries and StructScan
  - Get/Select convenience methods
  - IN clause expansion
  - Transaction helpers
- **pgx** for PostgreSQL
  - Native driver vs. database/sql compatibility
  - Connection pool management (pgxpool)
  - Advanced PostgreSQL features (COPY, LISTEN/NOTIFY)
  - Performance optimization

**Migration Tools**
- **golang-migrate** CLI and library
  - Migration file structure (up/down)
  - Versioning strategies
  - Rollback patterns
- **goose** migration framework
  - SQL vs. Go migrations
  - Custom migration functions
- **sql-migrate** with sqlx integration

**Common Patterns**
- Repository pattern implementation
  - Interface-based data access
  - Dependency injection for testing
  - Mock repositories for unit tests
- Query builders (squirrel, goqu)
- Error handling strategies
  - sql.ErrNoRows handling
  - Constraint violation detection
  - Retry logic for transient failures
- Connection lifecycle management
- NULL handling with sql.Null* types

**Best Practices**
- Avoiding SQL injection with parameter binding
- Transaction isolation levels
- Connection pooling tuning (max open, max idle, max lifetime)
- Prepared statement caching
- Context propagation for query cancellation

**Key Resources**:
- sqlx illustrated guide (jmoiron.github.io/sqlx/)
- golang-migrate documentation
- PostgreSQL-specific patterns with pgx
- Repository pattern examples

**Use Cases**:
- Building CRUD operations with type safety
- Managing database schema evolution
- Implementing data access layers
- Testing database code with mocks
- Handling concurrent database access

---

### Priority 3: Go HTTP APIs & Web Frameworks (CRITICAL GAP)

**Rationale**: Web services are a primary Go use case, but current agent has no framework guidance.

#### Coverage Should Include:

**Framework Comparison**
- **net/http** standard library
  - Go 1.22+ pattern routing in ServeMux
  - Middleware pattern implementation
  - When to use vs. frameworks
- **Chi**: Lightweight, stdlib-compatible
  - Middleware chains
  - Route grouping and nesting
  - URLParam and context integration
- **Gin**: High performance, batteries-included
  - Binding and validation
  - JSON rendering
  - Middleware ecosystem
- **Echo**: Type-safe, enterprise-focused
  - Middleware architecture
  - Error handling middleware
  - OpenAPI/Swagger integration
- **Fiber**: Express.js-inspired
  - WebSocket support
  - Performance characteristics
  - Migration considerations

**HTTP Patterns**
- Request validation with struct tags
  - Custom validators
  - Error response formatting
- Response serialization
  - JSON encoding best practices
  - Content negotiation
  - Streaming responses
- Middleware design
  - Logging middleware
  - Authentication/authorization
  - CORS handling
  - Rate limiting
- Error handling strategies
  - Custom error types
  - HTTP status code mapping
  - Error response standards

**REST API Design**
- Resource naming conventions
- HTTP method usage (GET, POST, PUT, PATCH, DELETE)
- Query parameter handling
- Pagination patterns
- Versioning strategies (URL vs. header)

**HTTP Client Patterns**
- http.Client configuration
  - Timeouts and context
  - Connection pooling
  - Retry logic with backoff
- Request building and signing
- Response handling and error detection

**Testing**
- httptest.Server for integration tests
- Request/response mocking
- Testing middleware chains

**Key Resources**:
- "The Standard Go net/http is all you need" (Medium, 2025)
- "A Deep Dive into Gin, Chi, and Mux in Go" (Medium)
- Chi framework documentation
- Google's HTTP best practices

**Use Cases**:
- Building RESTful APIs with Go
- Choosing appropriate framework for project scale
- Implementing authentication middleware
- Testing HTTP handlers and routes
- Optimizing API performance

---

### Priority 4: Go CLI Development with Cobra/Viper (MEDIUM PRIORITY)

**Rationale**: CLI tools are a major Go strength (Kubernetes, Docker, GitHub CLI all use Cobra/Viper).

#### Coverage Should Include:

**Cobra Framework**
- Command structure pattern: `APPNAME VERB NOUN --FLAG`
- Root command and subcommand organization
- Persistent vs. local flags
- PreRun/PostRun hooks
- Shell completion generation (bash, zsh, fish, PowerShell)

**Viper Configuration**
- Configuration priority: flags > env vars > config file > defaults
- Config file formats (YAML, JSON, TOML)
- Binding flags to config keys
- Environment variable mapping
  - Prefix + parameter naming
  - Dot notation to double underscore
- Remote config sources (etcd, Consul)

**Integration Patterns**
- Cobra + Viper plumbing (critical understanding)
  - Viper as single source of truth
  - PersistentPreRun for config loading
- Flag binding strategies
- Configuration validation

**CLI Best Practices**
- User-friendly error messages
- Progress indicators and spinners
- Interactive prompts (survey, promptui)
- Output formatting (table, JSON, YAML)
- Logging vs. user output separation

**Testing CLI Applications**
- Command execution in tests
- Capturing stdout/stderr
- Testing interactive prompts
- Integration tests for workflows

**Key Resources**:
- "Building CLI Apps in Go with Cobra & Viper" (November 2025)
- Official Cobra documentation
- "The Cobra & Viper Journey" learning resources
- Production examples: kubectl, docker, gh CLI

**Use Cases**:
- Building developer tools and utilities
- Creating project generators and scaffolding tools
- Implementing admin CLIs for services
- DevOps automation scripts
- Configuration management tools

---

### Priority 5: Go Observability & Monitoring (MEDIUM PRIORITY)

**Rationale**: Production Go services require monitoring, but current agent has minimal observability coverage.

#### Coverage Should Include:

**OpenTelemetry Integration**
- Distributed tracing fundamentals
  - Spans, traces, and context propagation
  - Instrumentation best practices
  - Auto-instrumentation vs. manual
- Metrics collection
  - Counter, UpDownCounter, Gauge, Histogram
  - Metric naming conventions
  - Cardinality management
- Logging integration
  - Structured logging with slog (Go 1.21+)
  - Log levels and context
  - Correlation IDs across logs/traces/metrics

**Prometheus Patterns**
- Metric types (Counter, Gauge, Histogram, Summary)
- Prometheus client library
- HTTP /metrics endpoint
- Metric naming and labels
- Alerting rules and expressions

**Distributed Tracing**
- Jaeger integration
- Trace sampling strategies
- Span attributes and events
- Performance impact mitigation

**Structured Logging**
- slog standard library (Go 1.21+)
- Log levels and handlers
- Context propagation in logs
- JSON vs. text formatting
- Log aggregation (Loki, ELK)

**Application Instrumentation**
- HTTP middleware instrumentation
  - Request duration metrics
  - Error rate tracking
  - Active request gauges
- gRPC instrumentation
- Database query tracing
- Background job monitoring

**Health Checks & Graceful Shutdown**
- /health and /readiness endpoints
- Dependency health checks
- Graceful shutdown with signal handling
- Connection draining patterns

**Developer Wishlist (2025)**
- Auto-instrumentation for HTTP/gRPC
- Span coverage tools
- Minimal code pollution
- Control without boilerplate

**Key Resources**:
- "Observability in Go: What Real Engineers Are Saying in 2025" (Quesma Blog)
- OpenTelemetry Go documentation
- "Monitoring Go Apps with OpenTelemetry Metrics" (Better Stack, 2025)
- Prometheus best practices

**Use Cases**:
- Instrumenting microservices for observability
- Setting up distributed tracing
- Creating operational dashboards
- Debugging production issues
- Performance monitoring and optimization

---

## 4. Skill Descriptions & Key Patterns

### Skill 1: Go Testing & Quality Assurance

**Name**: `golang-testing-strategies`
**Category**: `toolchains-golang-testing`

**Description**:
Comprehensive Go testing strategies including table-driven tests, testify assertions, gomock interface mocking, benchmark testing, and CI/CD integration. Use when writing test suites, setting up testing infrastructure, or ensuring code quality.

**Key Patterns**:

1. **Table-Driven Test Structure**
   ```go
   func TestUserValidation(t *testing.T) {
       tests := []struct {
           name    string
           user    User
           wantErr bool
       }{
           {"valid user", User{Name: "Alice", Age: 30}, false},
           {"empty name", User{Name: "", Age: 30}, true},
           {"negative age", User{Name: "Bob", Age: -5}, true},
       }
       for _, tt := range tests {
           t.Run(tt.name, func(t *testing.T) {
               err := ValidateUser(tt.user)
               if (err != nil) != tt.wantErr {
                   t.Errorf("ValidateUser() error = %v, wantErr %v", err, tt.wantErr)
               }
           })
       }
   }
   ```

2. **Testify Assertions**
   ```go
   import "github.com/stretchr/testify/assert"

   func TestCalculation(t *testing.T) {
       result := Calculate(10, 5)
       assert.Equal(t, 15, result)
       assert.NotNil(t, result)
   }
   ```

3. **Gomock Interface Mocking**
   ```go
   // Generate mocks: mockgen -source=interface.go -destination=mocks/mock.go
   func TestService(t *testing.T) {
       ctrl := gomock.NewController(t)
       defer ctrl.Finish()

       mockRepo := mocks.NewMockRepository(ctrl)
       mockRepo.EXPECT().GetUser(1).Return(User{ID: 1}, nil)

       service := NewService(mockRepo)
       user, err := service.FetchUser(1)
       assert.NoError(t, err)
       assert.Equal(t, 1, user.ID)
   }
   ```

**Decision Trees**:
- Choose testify when: Need readable assertions and test suites
- Choose gomock when: Testing code with interface dependencies
- Use benchmarks when: Optimizing performance-critical code
- Use httptest when: Testing HTTP handlers and clients

---

### Skill 2: Go Database Patterns & Migrations

**Name**: `golang-database-patterns`
**Category**: `toolchains-golang-data`

**Description**:
Go database integration patterns using sqlx, pgx, and migration tools like golang-migrate. Covers repository pattern, connection pooling, transaction handling, and schema evolution. Use when building data access layers or managing database schemas.

**Key Patterns**:

1. **Repository Pattern with Interface**
   ```go
   type UserRepository interface {
       Create(ctx context.Context, user *User) error
       GetByID(ctx context.Context, id int) (*User, error)
       Update(ctx context.Context, user *User) error
   }

   type postgresUserRepo struct {
       db *sqlx.DB
   }

   func (r *postgresUserRepo) GetByID(ctx context.Context, id int) (*User, error) {
       var user User
       query := "SELECT id, name, email FROM users WHERE id = $1"
       err := r.db.GetContext(ctx, &user, query, id)
       if err == sql.ErrNoRows {
           return nil, ErrUserNotFound
       }
       return &user, err
   }
   ```

2. **Transaction Pattern**
   ```go
   func (r *postgresUserRepo) UpdateWithHistory(ctx context.Context, user *User) error {
       tx, err := r.db.BeginTxx(ctx, nil)
       if err != nil {
           return err
       }
       defer tx.Rollback()

       if err := r.updateUser(ctx, tx, user); err != nil {
           return err
       }
       if err := r.insertHistory(ctx, tx, user); err != nil {
           return err
       }

       return tx.Commit()
   }
   ```

3. **Migration with golang-migrate**
   ```go
   // migrations/000001_create_users.up.sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   // migrations/000001_create_users.down.sql
   DROP TABLE users;
   ```

**Decision Trees**:
- Use database/sql when: Working with any SQL database, need standard interface
- Use sqlx when: Want convenience methods, struct scanning, named queries
- Use pgx when: PostgreSQL-specific, need maximum performance
- Use golang-migrate when: Need version control for schema changes

---

### Skill 3: Go HTTP APIs & Web Frameworks

**Name**: `golang-http-frameworks`
**Category**: `toolchains-golang-web`

**Description**:
Go HTTP API development with framework comparison (net/http, Chi, Gin, Echo, Fiber), middleware patterns, request validation, and REST API design. Use when building web services, choosing frameworks, or implementing HTTP middleware.

**Key Patterns**:

1. **Chi Router with Middleware**
   ```go
   r := chi.NewRouter()
   r.Use(middleware.Logger)
   r.Use(middleware.Recoverer)
   r.Use(middleware.Timeout(60 * time.Second))

   r.Route("/api/v1", func(r chi.Router) {
       r.Use(AuthMiddleware)
       r.Get("/users/{id}", GetUser)
       r.Post("/users", CreateUser)
   })
   ```

2. **Gin with Validation**
   ```go
   type CreateUserRequest struct {
       Name  string `json:"name" binding:"required,min=3"`
       Email string `json:"email" binding:"required,email"`
   }

   func CreateUser(c *gin.Context) {
       var req CreateUserRequest
       if err := c.ShouldBindJSON(&req); err != nil {
           c.JSON(400, gin.H{"error": err.Error()})
           return
       }
       // Process valid request
       c.JSON(200, gin.H{"status": "created"})
   }
   ```

3. **Custom Middleware**
   ```go
   func LoggingMiddleware(next http.Handler) http.Handler {
       return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
           start := time.Now()
           next.ServeHTTP(w, r)
           log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
       })
   }
   ```

**Decision Trees**:
- Use net/http when: Simple API, no complex routing, want stdlib only
- Use Chi when: Need lightweight router, stdlib compatibility important
- Use Gin when: Performance critical, want batteries-included framework
- Use Echo when: Enterprise features, OpenAPI integration needed
- Use Fiber when: Coming from Node.js/Express, need WebSocket support

---

### Skill 4: Go CLI Development with Cobra/Viper

**Name**: `golang-cli-cobra-viper`
**Category**: `toolchains-golang-cli`

**Description**:
Building production-quality CLI tools with Cobra command framework and Viper configuration management. Covers command structure, flag binding, environment variables, and shell completion. Use when creating developer tools, admin CLIs, or DevOps utilities.

**Key Patterns**:

1. **Cobra Command Structure**
   ```go
   var rootCmd = &cobra.Command{
       Use:   "myapp",
       Short: "A powerful CLI tool",
       Long:  "Detailed description of your application",
   }

   var deployCmd = &cobra.Command{
       Use:   "deploy [environment]",
       Short: "Deploy application",
       Args:  cobra.ExactArgs(1),
       RunE: func(cmd *cobra.Command, args []string) error {
           env := args[0]
           return deploy(env)
       },
   }

   func init() {
       rootCmd.AddCommand(deployCmd)
       deployCmd.Flags().StringP("region", "r", "us-east-1", "AWS region")
   }
   ```

2. **Viper Configuration Integration**
   ```go
   func initConfig() {
       viper.SetConfigName("config")
       viper.SetConfigType("yaml")
       viper.AddConfigPath("$HOME/.myapp")
       viper.AddConfigPath(".")

       viper.SetEnvPrefix("MYAPP")
       viper.AutomaticEnv()

       if err := viper.ReadInConfig(); err == nil {
           log.Println("Using config file:", viper.ConfigFileUsed())
       }
   }

   func init() {
       cobra.OnInitialize(initConfig)
       rootCmd.PersistentFlags().String("config", "", "config file path")
       viper.BindPFlag("config", rootCmd.PersistentFlags().Lookup("config"))
   }
   ```

3. **Shell Completion**
   ```go
   var completionCmd = &cobra.Command{
       Use:   "completion [bash|zsh|fish|powershell]",
       Short: "Generate completion script",
       Args:  cobra.ExactArgs(1),
       RunE: func(cmd *cobra.Command, args []string) error {
           switch args[0] {
           case "bash":
               return cmd.Root().GenBashCompletion(os.Stdout)
           case "zsh":
               return cmd.Root().GenZshCompletion(os.Stdout)
           // ... other shells
           }
       },
   }
   ```

**Decision Trees**:
- Use Cobra when: Building multi-command CLI with subcommands
- Use Viper when: Need flexible configuration (files + env vars + flags)
- Add completion when: CLI used frequently by developers
- Use persistent flags when: Flag applies to all subcommands

---

### Skill 5: Go Observability & Monitoring

**Name**: `golang-observability-opentelemetry`
**Category**: `toolchains-golang-observability`

**Description**:
Instrumenting Go applications with OpenTelemetry for distributed tracing, Prometheus for metrics, and structured logging with slog. Covers auto-instrumentation, health checks, and graceful shutdown. Use when adding observability to microservices or debugging production issues.

**Key Patterns**:

1. **OpenTelemetry Tracing**
   ```go
   import (
       "go.opentelemetry.io/otel"
       "go.opentelemetry.io/otel/trace"
   )

   func ProcessOrder(ctx context.Context, order Order) error {
       tracer := otel.Tracer("order-service")
       ctx, span := tracer.Start(ctx, "ProcessOrder")
       defer span.End()

       span.SetAttributes(
           attribute.String("order.id", order.ID),
           attribute.Int("order.items", len(order.Items)),
       )

       if err := validateOrder(ctx, order); err != nil {
           span.RecordError(err)
           return err
       }

       return fulfillOrder(ctx, order)
   }
   ```

2. **Prometheus Metrics**
   ```go
   import "github.com/prometheus/client_golang/prometheus"

   var (
       httpDuration = prometheus.NewHistogramVec(
           prometheus.HistogramOpts{
               Name:    "http_request_duration_seconds",
               Help:    "HTTP request duration",
               Buckets: prometheus.DefBuckets,
           },
           []string{"method", "path", "status"},
       )
   )

   func MetricsMiddleware(next http.Handler) http.Handler {
       return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
           start := time.Now()
           next.ServeHTTP(w, r)
           duration := time.Since(start).Seconds()

           httpDuration.WithLabelValues(
               r.Method, r.URL.Path, strconv.Itoa(w.StatusCode),
           ).Observe(duration)
       })
   }
   ```

3. **Structured Logging with slog**
   ```go
   import "log/slog"

   func HandleRequest(ctx context.Context, req Request) {
       logger := slog.With(
           "request_id", req.ID,
           "user_id", req.UserID,
       )

       logger.Info("processing request",
           "method", req.Method,
           "path", req.Path,
       )

       if err := process(ctx, req); err != nil {
           logger.Error("request failed",
               "error", err,
               "duration_ms", time.Since(req.StartTime).Milliseconds(),
           )
           return
       }

       logger.Info("request completed successfully")
   }
   ```

**Decision Trees**:
- Use OpenTelemetry when: Need distributed tracing across services
- Use Prometheus when: Need metrics collection and alerting
- Use slog when: Go 1.21+, want structured logging with stdlib
- Add health checks when: Running in Kubernetes or containerized environment

---

## 5. Additional Recommended Topics (Future Consideration)

These topics are valuable but lower priority than the top 5:

### 6. Go Error Handling Deep Dive
**Category**: `toolchains-golang-errors`
**Focus**: Custom error types, wrapping with %w, errors.Is/As advanced usage, sentinel errors, error chains
**Gap**: Current agent has basic coverage, needs deep dive
**Priority**: Low (covered at basic level)

### 7. Go Context Patterns
**Category**: `toolchains-golang-context`
**Focus**: WithValue anti-patterns, deadline vs. timeout, context in middleware, testing with contexts
**Gap**: Mentioned but not detailed
**Priority**: Low (often learned through practice)

### 8. Go Generics Best Practices
**Category**: `toolchains-golang-generics`
**Focus**: Type parameters, constraints design, when to use vs. interfaces, generic data structures
**Gap**: Only mentioned as "Go 1.23-1.24 feature"
**Priority**: Low (generics still evolving, not universally needed)

### 9. Go Standard Library Mastery
**Category**: `toolchains-golang-stdlib`
**Focus**: net/http 1.22+ routing, encoding/json patterns, io.Reader/Writer, time package
**Gap**: Partially covered
**Priority**: Low (well-documented in official docs)

### 10. Go Project Structure & Organization
**Category**: `toolchains-golang-architecture`
**Focus**: When to use cmd/internal/pkg/, module organization, mono-repo patterns
**Gap**: Only links to golang-standards/project-layout
**Priority**: Low (controversial topic, no clear consensus)

---

## 6. Implementation Recommendations

### Immediate Actions (Next Sprint)

1. **Create `golang-testing-strategies` skill**
   - Highest impact, critical gap
   - Build on existing "table-driven tests" mention
   - Include testify, gomock, benchmarks
   - Estimated effort: 4-6 hours

2. **Create `golang-database-patterns` skill**
   - Essential for most Go applications
   - Cover sqlx, pgx, golang-migrate
   - Repository pattern examples
   - Estimated effort: 4-6 hours

3. **Create `golang-http-frameworks` skill**
   - High demand, no current coverage
   - Framework comparison matrix
   - Middleware patterns
   - Estimated effort: 5-7 hours

### Short-Term Actions (Next Month)

4. **Create `golang-cli-cobra-viper` skill**
   - Leverages Go's CLI tool strength
   - Cobra/Viper integration patterns
   - Estimated effort: 3-5 hours

5. **Create `golang-observability-opentelemetry` skill**
   - Production-readiness focus
   - OpenTelemetry + Prometheus integration
   - Estimated effort: 4-6 hours

### Skill Structure Template

Each skill should follow the existing skill structure pattern:

```markdown
---
name: skill-name
description: Brief description with use cases
---

# Skill Title

---
progressive_disclosure:
  entry_point:
    summary: "One-line summary"
    when_to_use:
      - "Use case 1"
      - "Use case 2"
    quick_start:
      - "Step 1"
      - "Step 2"
  token_estimate:
    entry: 75
    full: 4000-5000
---

## Core Concepts

## Implementation Patterns

## Best Practices

## Anti-Patterns

## Decision Trees

## Examples

## Resources
```

### Quality Checklist

Before considering a skill complete:
- [ ] Includes decision trees for choosing approaches
- [ ] Provides runnable code examples
- [ ] Covers common anti-patterns
- [ ] Links to authoritative 2025 resources
- [ ] Includes progressive disclosure structure
- [ ] Token estimate under 5000 for full content
- [ ] Use cases clearly defined

---

## 7. Conclusion

The Go ecosystem in 2025 is mature, stable, and focused on simplicity, productivity, and cloud-native development. Our current `golang-engineer` agent provides excellent concurrency pattern coverage but has critical gaps in:

1. **Testing** (testify, gomock, table-driven tests)
2. **Database** (sqlx, pgx, migrations)
3. **Web frameworks** (Chi, Gin, Echo, Fiber)
4. **CLI tools** (Cobra, Viper)
5. **Observability** (OpenTelemetry, Prometheus)

Implementing the recommended 5 skills will:
- Complement existing concurrency expertise
- Cover essential production Go development domains
- Provide actionable guidance for common tasks
- Leverage current (2025) best practices and tools

**Estimated Total Effort**: 20-29 hours for all 5 skills

**Recommended Approach**: Implement in priority order, starting with testing and database patterns, which have the highest immediate impact.

---

## 8. References

### Official Resources
- Go Documentation: https://go.dev/doc/
- Effective Go: https://go.dev/doc/effective_go
- Google Go Style Guide: https://google.github.io/styleguide/go/
- Go Blog (Concurrency): https://go.dev/blog/pipelines

### 2025 Community Resources
- "The Go Ecosystem in 2025" (JetBrains, November 2025)
- "Go Concurrency 2025: Goroutines, Channels & Clean Patterns" (DEV Community)
- "Observability in Go: What Real Engineers Are Saying in 2025" (Quesma)
- "Building CLI Apps in Go with Cobra & Viper" (November 2025)

### Books
- "Learning Go, 2nd Edition" by Jon Bodner (January 2024)
- "Practical Go" by Dave Cheney (dave.cheney.net/practical-go)

### Framework Documentation
- Testify: https://github.com/stretchr/testify
- Gomock: https://github.com/golang/mock
- sqlx: https://jmoiron.github.io/sqlx/
- Chi Router: https://go-chi.io/
- Cobra: https://cobra.dev/
- OpenTelemetry Go: https://opentelemetry.io/docs/languages/go/

---

**Research Completed**: 2025-12-03
**Next Steps**: Review recommendations with skill library maintainers, prioritize implementation schedule, begin with `golang-testing-strategies` skill development.
