---
name: spring-boot
description: Spring Boot 3.x - Java framework for production-ready applications with dependency injection, REST APIs, data access, security, and actuator monitoring
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Modern Java framework for building production-ready microservices and web applications with auto-configuration, DI, REST APIs, and Spring Data"
    when_to_use: "Building Java microservices, REST APIs, enterprise applications, when need production-ready features like health checks, metrics, and security"
    quick_start: "1. Create project with start.spring.io 2. Add @SpringBootApplication 3. Create @RestController 4. Run with ./mvnw spring-boot:run"
context_limit: 700
tags:
  - java
  - spring-boot
  - spring
  - microservices
  - rest-api
  - dependency-injection
  - jpa
  - security
  - actuator
requires_tools: []
---

# Spring Boot 3.x - Production-Ready Java Framework

## Overview

Spring Boot is an opinionated Java framework for building production-ready applications with minimal configuration. It provides auto-configuration, embedded servers, and production-ready features like health checks and metrics.

**Key Features**:
- Auto-configuration (sensible defaults)
- Embedded servers (Tomcat, Jetty, Undertow)
- Dependency Injection with @Autowired
- Spring Data JPA for database access
- Spring Security for authentication/authorization
- Actuator for production monitoring
- Built-in testing support

**Requirements**:
- Java 17+ (Spring Boot 3.x requires Java 17 minimum)
- Maven or Gradle

**Quick Start**:
```bash
# Create project from Spring Initializr
curl https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=3.2.0 \
  -d dependencies=web,data-jpa,postgresql,lombok,actuator \
  -d name=myapp \
  -o myapp.zip && unzip myapp.zip

# Run the application
cd myapp
./mvnw spring-boot:run
```

## Project Structure

```
src/
├── main/
│   ├── java/com/example/myapp/
│   │   ├── MyappApplication.java      # Main class
│   │   ├── config/                    # @Configuration classes
│   │   ├── controller/                # @RestController classes
│   │   ├── service/                   # @Service classes
│   │   ├── repository/                # @Repository interfaces
│   │   ├── model/                     # Entity classes
│   │   ├── dto/                       # Data Transfer Objects
│   │   └── exception/                 # Exception handlers
│   └── resources/
│       ├── application.yml            # Configuration
│       └── application-{profile}.yml  # Profile-specific config
└── test/
    └── java/com/example/myapp/        # Test classes
```

## Core Annotations

### Application Setup

```java
// Main application class
@SpringBootApplication  // Combines @Configuration, @EnableAutoConfiguration, @ComponentScan
public class MyappApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyappApplication.class, args);
    }
}
```

### Dependency Injection

```java
// Constructor injection (recommended)
@Service
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    // @Autowired optional on single constructor (Spring 4.3+)
    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }
}

// With Lombok
@Service
@RequiredArgsConstructor  // Generates constructor for final fields
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
}

// Field injection (avoid in production code)
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;  // Harder to test
}
```

### Component Stereotypes

```java
@Component      // Generic component
@Service        // Business logic layer
@Repository     // Data access layer (enables exception translation)
@Controller     // MVC controller (returns views)
@RestController // REST API controller (returns JSON)
@Configuration  // Configuration class with @Bean methods
```

## REST Controllers

### Basic Controller

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    // GET /api/v1/users
    @GetMapping
    public ResponseEntity<List<UserDto>> getAllUsers() {
        return ResponseEntity.ok(userService.findAll());
    }

    // GET /api/v1/users/{id}
    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUserById(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // POST /api/v1/users
    @PostMapping
    public ResponseEntity<UserDto> createUser(@Valid @RequestBody CreateUserRequest request) {
        UserDto created = userService.create(request);
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(created.getId())
            .toUri();
        return ResponseEntity.created(location).body(created);
    }

    // PUT /api/v1/users/{id}
    @PutMapping("/{id}")
    public ResponseEntity<UserDto> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        return ResponseEntity.ok(userService.update(id, request));
    }

    // DELETE /api/v1/users/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }

    // GET /api/v1/users/search?email=test@example.com
    @GetMapping("/search")
    public ResponseEntity<List<UserDto>> searchUsers(
            @RequestParam(required = false) String email,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ResponseEntity.ok(userService.search(email, page, size));
    }
}
```

### Request/Response DTOs

```java
// Request DTO with validation
@Data
public class CreateUserRequest {
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;
}

// Response DTO
@Data
@Builder
public class UserDto {
    private Long id;
    private String email;
    private String name;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static UserDto fromEntity(User user) {
        return UserDto.builder()
            .id(user.getId())
            .email(user.getEmail())
            .name(user.getName())
            .createdAt(user.getCreatedAt())
            .updatedAt(user.getUpdatedAt())
            .build();
    }
}
```

## Service Layer

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)  // Default to read-only transactions
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public List<UserDto> findAll() {
        return userRepository.findAll().stream()
            .map(UserDto::fromEntity)
            .collect(Collectors.toList());
    }

    public Optional<UserDto> findById(Long id) {
        return userRepository.findById(id)
            .map(UserDto::fromEntity);
    }

    @Transactional  // Read-write transaction
    public UserDto create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException(request.getEmail());
        }

        User user = User.builder()
            .email(request.getEmail())
            .name(request.getName())
            .passwordHash(passwordEncoder.encode(request.getPassword()))
            .build();

        return UserDto.fromEntity(userRepository.save(user));
    }

    @Transactional
    public UserDto update(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));

        if (request.getName() != null) {
            user.setName(request.getName());
        }
        if (request.getEmail() != null) {
            user.setEmail(request.getEmail());
        }

        return UserDto.fromEntity(userRepository.save(user));
    }

    @Transactional
    public void delete(Long id) {
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException(id);
        }
        userRepository.deleteById(id);
    }

    public List<UserDto> search(String email, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        Page<User> users = email != null
            ? userRepository.findByEmailContainingIgnoreCase(email, pageable)
            : userRepository.findAll(pageable);

        return users.stream()
            .map(UserDto::fromEntity)
            .collect(Collectors.toList());
    }
}
```

## Repository Layer (Spring Data JPA)

### Basic Repository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Derived query methods
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    List<User> findByNameContainingIgnoreCase(String name);

    // Paginated queries
    Page<User> findByEmailContainingIgnoreCase(String email, Pageable pageable);

    // Custom JPQL query
    @Query("SELECT u FROM User u WHERE u.createdAt > :date AND u.active = true")
    List<User> findActiveUsersCreatedAfter(@Param("date") LocalDateTime date);

    // Native SQL query
    @Query(value = "SELECT * FROM users WHERE email ILIKE %:email%", nativeQuery = true)
    List<User> searchByEmail(@Param("email") String email);

    // Modifying query
    @Modifying
    @Query("UPDATE User u SET u.active = false WHERE u.lastLoginAt < :date")
    int deactivateInactiveUsers(@Param("date") LocalDateTime date);
}
```

### Entity Class

```java
@Entity
@Table(name = "users")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Column(nullable = false)
    @Builder.Default
    private boolean active = true;

    @Column(name = "created_at", nullable = false, updatable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // Relationships
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<Post> posts = new ArrayList<>();

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    @Builder.Default
    private Set<Role> roles = new HashSet<>();
}
```

## Configuration

### application.yml

```yaml
spring:
  application:
    name: myapp

  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:password}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000

  jpa:
    hibernate:
      ddl-auto: validate  # none, validate, update, create, create-drop
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        default_schema: public

  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

server:
  port: ${PORT:8080}
  servlet:
    context-path: /api

# Actuator endpoints
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when_authorized

# Custom properties
app:
  jwt:
    secret: ${JWT_SECRET:your-secret-key}
    expiration-ms: 86400000
```

### Profile-Specific Configuration

```yaml
# application-dev.yml
spring:
  jpa:
    show-sql: true
  h2:
    console:
      enabled: true

logging:
  level:
    com.example.myapp: DEBUG
    org.springframework.web: DEBUG

---
# application-prod.yml
spring:
  jpa:
    show-sql: false
    properties:
      hibernate:
        generate_statistics: false

logging:
  level:
    com.example.myapp: INFO
    org.springframework.web: WARN
```

### Configuration Properties Class

```java
@Configuration
@ConfigurationProperties(prefix = "app.jwt")
@Data
public class JwtProperties {
    private String secret;
    private long expirationMs;
}

// Usage
@Service
@RequiredArgsConstructor
public class JwtService {
    private final JwtProperties jwtProperties;

    public String generateToken(User user) {
        return Jwts.builder()
            .setSubject(user.getEmail())
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + jwtProperties.getExpirationMs()))
            .signWith(Keys.hmacShaKeyFor(jwtProperties.getSecret().getBytes()))
            .compact();
    }
}
```

## Exception Handling

### Global Exception Handler

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    // Handle validation errors
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(error -> error.getField() + ": " + error.getDefaultMessage())
            .collect(Collectors.toList());

        ErrorResponse response = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .message("Validation failed")
            .errors(errors)
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.badRequest().body(response);
    }

    // Handle not found exceptions
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        ErrorResponse response = ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
    }

    // Handle business logic exceptions
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {
        ErrorResponse response = ErrorResponse.builder()
            .status(HttpStatus.CONFLICT.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.status(HttpStatus.CONFLICT).body(response);
    }

    // Catch-all handler
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleAllExceptions(Exception ex) {
        log.error("Unexpected error occurred", ex);

        ErrorResponse response = ErrorResponse.builder()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .message("An unexpected error occurred")
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}

// Error response DTO
@Data
@Builder
public class ErrorResponse {
    private int status;
    private String message;
    private List<String> errors;
    private LocalDateTime timestamp;
}

// Custom exceptions
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String resource, Long id) {
        super(String.format("%s not found with id: %d", resource, id));
    }
}

public class UserNotFoundException extends ResourceNotFoundException {
    public UserNotFoundException(Long id) {
        super("User", id);
    }
}
```

## Spring Security

### Security Configuration (Spring Security 6.x)

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final UserDetailsService userDetailsService;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .authenticationProvider(authenticationProvider())
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder());
        return provider;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config)
            throws Exception {
        return config.getAuthenticationManager();
    }
}
```

### JWT Filter

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {

        final String authHeader = request.getHeader("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        final String jwt = authHeader.substring(7);
        final String userEmail = jwtService.extractUsername(jwt);

        if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(userEmail);

            if (jwtService.isTokenValid(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities());

                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        filterChain.doFilter(request, response);
    }
}
```

## Actuator Endpoints

```yaml
# Built-in endpoints
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env
      base-path: /actuator
  endpoint:
    health:
      show-details: when_authorized
      probes:
        enabled: true  # Kubernetes liveness/readiness probes
  info:
    env:
      enabled: true

# Application info
info:
  app:
    name: ${spring.application.name}
    version: '@project.version@'
    java:
      version: ${java.version}
```

**Common Actuator Endpoints**:
- `GET /actuator/health` - Application health
- `GET /actuator/health/liveness` - Kubernetes liveness probe
- `GET /actuator/health/readiness` - Kubernetes readiness probe
- `GET /actuator/info` - Application information
- `GET /actuator/metrics` - Metrics list
- `GET /actuator/metrics/{name}` - Specific metric
- `GET /actuator/prometheus` - Prometheus format metrics

## Testing

### Unit Testing Controllers

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldReturnUserById() throws Exception {
        UserDto user = UserDto.builder()
            .id(1L)
            .email("test@example.com")
            .name("Test User")
            .build();

        when(userService.findById(1L)).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }

    @Test
    void shouldReturn404WhenUserNotFound() throws Exception {
        when(userService.findById(999L)).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/v1/users/999"))
            .andExpect(status().isNotFound());
    }

    @Test
    void shouldCreateUser() throws Exception {
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("new@example.com");
        request.setName("New User");
        request.setPassword("password123");

        UserDto created = UserDto.builder()
            .id(1L)
            .email("new@example.com")
            .name("New User")
            .build();

        when(userService.create(any())).thenReturn(created);

        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.email").value("new@example.com"));
    }
}
```

### Integration Testing

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.ANY)
@Transactional
class UserIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldCreateAndRetrieveUser() {
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("integration@test.com");
        request.setName("Integration Test");
        request.setPassword("password123");

        ResponseEntity<UserDto> createResponse = restTemplate.postForEntity(
            "/api/v1/users", request, UserDto.class);

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(createResponse.getBody()).isNotNull();
        assertThat(createResponse.getBody().getEmail()).isEqualTo("integration@test.com");

        Long userId = createResponse.getBody().getId();
        ResponseEntity<UserDto> getResponse = restTemplate.getForEntity(
            "/api/v1/users/" + userId, UserDto.class);

        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().getName()).isEqualTo("Integration Test");
    }
}
```

### Repository Testing

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void shouldFindByEmail() {
        User user = User.builder()
            .email("test@example.com")
            .name("Test")
            .passwordHash("hash")
            .build();
        entityManager.persistAndFlush(user);

        Optional<User> found = userRepository.findByEmail("test@example.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Test");
    }
}
```

## Best Practices

### 1. Use Constructor Injection
```java
// Prefer constructor injection with final fields
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;  // final = immutable
}
```

### 2. Layer Separation
```java
// Controller -> Service -> Repository
// DTOs for API layer, Entities for persistence layer
// Never expose entities directly in REST responses
```

### 3. Transaction Management
```java
@Service
@Transactional(readOnly = true)  // Default read-only
public class UserService {

    @Transactional  // Write transaction
    public void updateUser() { }
}
```

### 4. Configuration Externalization
```yaml
# Use environment variables for secrets
spring:
  datasource:
    password: ${DB_PASSWORD}  # From environment
```

### 5. Error Handling
```java
// Use @RestControllerAdvice for global exception handling
// Return consistent error responses
// Never expose internal details in production
```

## Resources

- **Spring Boot Documentation**: https://docs.spring.io/spring-boot/docs/current/reference/html/
- **Spring Data JPA**: https://docs.spring.io/spring-data/jpa/docs/current/reference/html/
- **Spring Security**: https://docs.spring.io/spring-security/reference/
- **Spring Initializr**: https://start.spring.io/
- **Baeldung Tutorials**: https://www.baeldung.com/spring-boot

## Related Skills

When using Spring Boot, consider these complementary skills:

- **mongodb**: NoSQL database integration with Spring Data MongoDB
- **docker**: Containerizing Spring Boot applications
- **kubernetes**: Deploying Spring Boot microservices
- **postgresql**: Relational database patterns with JPA
