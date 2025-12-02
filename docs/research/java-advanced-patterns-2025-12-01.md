# Java Advanced Patterns: Production-Ready Guide (2025)

**Focus:** Java 17-21+ | Spring Boot 3.x | Reactive Programming | Modern Concurrency
**Target Audience:** Intermediate to Advanced Java Developers
**Last Updated:** December 2025

---

## Table of Contents

1. [Modern Java (17-21+)](#modern-java-17-21)
2. [Spring Boot Advanced Patterns](#spring-boot-advanced-patterns)
3. [Reactive Programming](#reactive-programming)
4. [Concurrency & Performance](#concurrency--performance)
5. [Testing & Quality](#testing--quality)

---

## Modern Java (17-21+)

### 1. Records for Immutable Data Transfer Objects

**Use Case:** Replace verbose POJOs with concise, immutable data carriers

```java
// Traditional approach (verbose)
public final class CustomerDTO {
    private final String id;
    private final String name;
    private final String email;

    public CustomerDTO(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }

    @Override
    public boolean equals(Object o) { /* ... */ }
    @Override
    public int hashCode() { /* ... */ }
    @Override
    public String toString() { /* ... */ }
}

// Modern Record (Java 17+)
public record CustomerDTO(String id, String name, String email) {
    // Custom validation in compact constructor
    public CustomerDTO {
        Objects.requireNonNull(id, "id cannot be null");
        Objects.requireNonNull(email, "email cannot be null");
        if (!email.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }

    // Derived properties
    public String displayName() {
        return name != null ? name : email.split("@")[0];
    }
}

// Usage in Spring Boot
@RestController
@RequestMapping("/api/customers")
public class CustomerController {

    @PostMapping
    public ResponseEntity<CustomerDTO> createCustomer(@RequestBody CustomerDTO dto) {
        // Records work seamlessly with Jackson
        Customer customer = customerService.create(dto);
        return ResponseEntity.ok(toDTO(customer));
    }
}
```

**Production Benefits:**
- 70% less boilerplate code
- Immutability by default (thread-safe)
- Built-in equals(), hashCode(), toString()
- Perfect for DTOs, API responses, event payloads

**Testing Pattern:**
```java
@Test
void recordsShouldValidateInput() {
    assertThrows(IllegalArgumentException.class,
        () -> new CustomerDTO("123", "John", "invalid-email"));
}

@Test
void recordsShouldSerializeCorrectly() throws Exception {
    CustomerDTO dto = new CustomerDTO("1", "Jane", "jane@example.com");
    String json = objectMapper.writeValueAsString(dto);
    CustomerDTO deserialized = objectMapper.readValue(json, CustomerDTO.class);
    assertEquals(dto, deserialized);
}
```

---

### 2. Sealed Classes for Domain Modeling

**Use Case:** Restrict inheritance hierarchies for type-safe domain models

```java
// Payment domain with sealed types (Java 17+)
public sealed interface Payment
    permits CreditCardPayment, PayPalPayment, BankTransferPayment {

    BigDecimal amount();
    String transactionId();
    PaymentStatus process();
}

public final record CreditCardPayment(
    String cardNumber,
    String cvv,
    YearMonth expiry,
    BigDecimal amount,
    String transactionId
) implements Payment {

    @Override
    public PaymentStatus process() {
        // Credit card specific processing
        return PaymentStatus.PENDING;
    }
}

public final record PayPalPayment(
    String email,
    String paypalId,
    BigDecimal amount,
    String transactionId
) implements Payment {

    @Override
    public PaymentStatus process() {
        // PayPal specific processing
        return PaymentStatus.COMPLETED;
    }
}

public final record BankTransferPayment(
    String accountNumber,
    String routingNumber,
    BigDecimal amount,
    String transactionId
) implements Payment {

    @Override
    public PaymentStatus process() {
        // Bank transfer specific processing
        return PaymentStatus.PROCESSING;
    }
}

// Spring Boot Service with pattern matching
@Service
public class PaymentService {

    public PaymentResponse processPayment(Payment payment) {
        // Exhaustive pattern matching (Java 21+)
        return switch (payment) {
            case CreditCardPayment cc -> {
                validateCreditCard(cc);
                yield new PaymentResponse(cc.transactionId(), cc.process());
            }
            case PayPalPayment pp -> {
                validatePayPal(pp);
                yield new PaymentResponse(pp.transactionId(), pp.process());
            }
            case BankTransferPayment bt -> {
                validateBankAccount(bt);
                yield new PaymentResponse(bt.transactionId(), bt.process());
            }
            // Compiler ensures all cases covered
        };
    }
}
```

**Production Benefits:**
- Compiler-enforced exhaustive pattern matching
- Prevents unexpected subclasses
- Clear domain boundaries
- Type-safe polymorphism

**Testing Pattern:**
```java
@ParameterizedTest
@MethodSource("paymentProvider")
void shouldProcessAllPaymentTypes(Payment payment) {
    PaymentResponse response = paymentService.processPayment(payment);
    assertNotNull(response);
    assertNotNull(response.status());
}

static Stream<Payment> paymentProvider() {
    return Stream.of(
        new CreditCardPayment("4111111111111111", "123",
            YearMonth.of(2025, 12), new BigDecimal("100.00"), "TX1"),
        new PayPalPayment("user@example.com", "PP123",
            new BigDecimal("50.00"), "TX2"),
        new BankTransferPayment("123456789", "987654321",
            new BigDecimal("200.00"), "TX3")
    );
}
```

---

### 3. Pattern Matching for instanceof

**Use Case:** Simplify type checks and casts in polymorphic code

```java
// Old approach (verbose)
public String formatNotification(Notification notification) {
    if (notification instanceof EmailNotification) {
        EmailNotification email = (EmailNotification) notification;
        return "Email to: " + email.getRecipient();
    } else if (notification instanceof SmsNotification) {
        SmsNotification sms = (SmsNotification) notification;
        return "SMS to: " + sms.getPhoneNumber();
    } else if (notification instanceof PushNotification) {
        PushNotification push = (PushNotification) notification;
        return "Push to device: " + push.getDeviceId();
    }
    return "Unknown notification";
}

// Modern approach with pattern matching (Java 17+)
public String formatNotification(Notification notification) {
    if (notification instanceof EmailNotification email) {
        return "Email to: " + email.recipient();
    } else if (notification instanceof SmsNotification sms) {
        return "SMS to: " + sms.phoneNumber();
    } else if (notification instanceof PushNotification push) {
        return "Push to device: " + push.deviceId();
    }
    return "Unknown notification";
}

// Best approach with switch pattern matching (Java 21+)
public String formatNotification(Notification notification) {
    return switch (notification) {
        case EmailNotification email ->
            "Email to: " + email.recipient();
        case SmsNotification sms ->
            "SMS to: " + sms.phoneNumber();
        case PushNotification push ->
            "Push to device: " + push.deviceId();
        case null ->
            "Notification is null";
        default ->
            "Unknown notification type";
    };
}

// Advanced: Guard patterns (Java 21+)
public NotificationPriority calculatePriority(Notification notification, User user) {
    return switch (notification) {
        case EmailNotification e when e.isUrgent() ->
            NotificationPriority.HIGH;
        case EmailNotification e ->
            NotificationPriority.NORMAL;
        case SmsNotification s when user.hasPhoneVerified() ->
            NotificationPriority.HIGH;
        case SmsNotification s ->
            NotificationPriority.MEDIUM;
        case PushNotification p when p.isTimeSensitive() ->
            NotificationPriority.CRITICAL;
        default ->
            NotificationPriority.LOW;
    };
}
```

**Production Benefits:**
- Eliminates redundant casts
- More readable type-based logic
- Compiler-verified type safety
- Guard patterns for complex conditions

---

### 4. Virtual Threads (Project Loom - Java 21+)

**Use Case:** Handle massive concurrency without traditional thread pool overhead

```java
// Traditional thread pool approach
@Configuration
public class ThreadPoolConfig {
    @Bean
    public ExecutorService threadPool() {
        return Executors.newFixedThreadPool(200); // Limited threads
    }
}

// Virtual threads approach (Java 21+)
@Configuration
public class VirtualThreadConfig {

    @Bean
    public ExecutorService virtualThreadExecutor() {
        return Executors.newVirtualThreadPerTaskExecutor();
    }

    // Spring Boot 3.2+ automatic virtual threads
    @Bean
    public TomcatProtocolHandlerCustomizer<?> protocolHandlerVirtualThreadExecutorCustomizer() {
        return protocolHandler -> {
            protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
        };
    }
}

// Service using virtual threads
@Service
public class OrderProcessingService {

    private final ExecutorService virtualThreadExecutor;

    public OrderProcessingService(ExecutorService virtualThreadExecutor) {
        this.virtualThreadExecutor = virtualThreadExecutor;
    }

    public CompletableFuture<OrderResult> processOrder(Order order) {
        return CompletableFuture.supplyAsync(() -> {
            // This runs on a virtual thread
            validateOrder(order);           // May block on DB
            checkInventory(order);          // May block on external API
            processPayment(order);          // May block on payment gateway
            sendConfirmation(order);        // May block on email service
            return new OrderResult(order.id(), OrderStatus.COMPLETED);
        }, virtualThreadExecutor);
    }

    public List<OrderResult> processBatchOrders(List<Order> orders) {
        // Process 100,000+ orders concurrently with virtual threads
        List<CompletableFuture<OrderResult>> futures = orders.stream()
            .map(this::processOrder)
            .toList();

        return futures.stream()
            .map(CompletableFuture::join)
            .toList();
    }
}

// Structured concurrency pattern (Java 21+)
public OrderSummary fetchOrderDetails(String orderId) throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {

        Supplier<Order> orderTask = scope.fork(() -> orderRepository.findById(orderId));
        Supplier<Customer> customerTask = scope.fork(() -> customerService.getCustomer(orderId));
        Supplier<List<Item>> itemsTask = scope.fork(() -> itemService.getItems(orderId));
        Supplier<Payment> paymentTask = scope.fork(() -> paymentService.getPayment(orderId));

        scope.join();           // Wait for all tasks
        scope.throwIfFailed();  // Propagate exceptions

        return new OrderSummary(
            orderTask.get(),
            customerTask.get(),
            itemsTask.get(),
            paymentTask.get()
        );
    }
}
```

**Production Benefits:**
- Handle millions of concurrent requests
- Simplified blocking I/O code (no callbacks)
- Lower memory footprint vs platform threads
- Better resource utilization

**Testing Pattern:**
```java
@Test
void shouldHandleMassiveConcurrency() throws Exception {
    int numOrders = 100_000;
    List<Order> orders = generateTestOrders(numOrders);

    long startTime = System.currentTimeMillis();
    List<OrderResult> results = orderService.processBatchOrders(orders);
    long duration = System.currentTimeMillis() - startTime;

    assertEquals(numOrders, results.size());
    assertTrue(duration < 30_000, "Should process 100k orders in < 30s");
}
```

---

## Spring Boot Advanced Patterns

### 1. Hexagonal Architecture (Ports & Adapters)

**Use Case:** Decouple business logic from infrastructure concerns

```java
// Domain Layer (core business logic, framework-agnostic)
package com.example.order.domain;

public class Order {
    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderItem> items;
    private OrderStatus status;

    public Order(OrderId id, CustomerId customerId, List<OrderItem> items) {
        this.id = id;
        this.customerId = customerId;
        this.items = new ArrayList<>(items);
        this.status = OrderStatus.PENDING;
    }

    public void complete() {
        if (status != OrderStatus.PENDING) {
            throw new InvalidOrderStateException("Cannot complete non-pending order");
        }
        this.status = OrderStatus.COMPLETED;
    }

    public BigDecimal calculateTotal() {
        return items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}

// Application Layer (use cases / ports)
package com.example.order.application.port.in;

public interface CreateOrderUseCase {
    OrderResponse createOrder(CreateOrderCommand command);
}

package com.example.order.application.port.out;

public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(OrderId id);
}

public interface PaymentGateway {
    PaymentResult processPayment(PaymentRequest request);
}

public interface NotificationService {
    void sendOrderConfirmation(Order order);
}

// Application Service (orchestrates use cases)
package com.example.order.application.service;

@Service
@Transactional
public class OrderService implements CreateOrderUseCase {

    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    public OrderService(OrderRepository orderRepository,
                       PaymentGateway paymentGateway,
                       NotificationService notificationService) {
        this.orderRepository = orderRepository;
        this.paymentGateway = paymentGateway;
        this.notificationService = notificationService;
    }

    @Override
    public OrderResponse createOrder(CreateOrderCommand command) {
        // Domain logic
        Order order = new Order(
            OrderId.generate(),
            command.customerId(),
            command.items()
        );

        // Persist through port
        Order savedOrder = orderRepository.save(order);

        // Process payment through port
        PaymentResult payment = paymentGateway.processPayment(
            new PaymentRequest(savedOrder.getId(), savedOrder.calculateTotal())
        );

        if (payment.isSuccessful()) {
            savedOrder.complete();
            orderRepository.save(savedOrder);
            notificationService.sendOrderConfirmation(savedOrder);
        }

        return OrderResponse.from(savedOrder);
    }
}

// Infrastructure Layer (adapters)
package com.example.order.infrastructure.persistence;

@Repository
public class JpaOrderRepository implements OrderRepository {

    private final JpaOrderEntityRepository jpaRepository;
    private final OrderMapper mapper;

    @Override
    public Order save(Order order) {
        OrderEntity entity = mapper.toEntity(order);
        OrderEntity saved = jpaRepository.save(entity);
        return mapper.toDomain(saved);
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepository.findById(id.value())
            .map(mapper::toDomain);
    }
}

package com.example.order.infrastructure.payment;

@Component
public class StripePaymentAdapter implements PaymentGateway {

    private final StripeClient stripeClient;

    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        try {
            ChargeResponse response = stripeClient.charge(
                request.amount(),
                request.orderId().value()
            );
            return PaymentResult.success(response.id());
        } catch (StripeException e) {
            return PaymentResult.failure(e.getMessage());
        }
    }
}

// Presentation Layer (REST adapter)
package com.example.order.infrastructure.web;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final CreateOrderUseCase createOrderUseCase;

    public OrderController(CreateOrderUseCase createOrderUseCase) {
        this.createOrderUseCase = createOrderUseCase;
    }

    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
        CreateOrderCommand command = new CreateOrderCommand(
            request.customerId(),
            request.items()
        );
        OrderResponse response = createOrderUseCase.createOrder(command);
        return ResponseEntity.ok(response);
    }
}
```

**Production Benefits:**
- Business logic independent of frameworks
- Easy to test (mock adapters)
- Swap implementations without changing core
- Clear separation of concerns

**Testing Pattern:**
```java
@Test
void shouldCreateOrderWithMockAdapters() {
    // Arrange
    OrderRepository mockRepo = mock(OrderRepository.class);
    PaymentGateway mockPayment = mock(PaymentGateway.class);
    NotificationService mockNotification = mock(NotificationService.class);

    when(mockRepo.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));
    when(mockPayment.processPayment(any())).thenReturn(PaymentResult.success("PAY123"));

    OrderService service = new OrderService(mockRepo, mockPayment, mockNotification);

    // Act
    CreateOrderCommand command = new CreateOrderCommand(
        new CustomerId("CUST1"),
        List.of(new OrderItem("ITEM1", 2, new BigDecimal("10.00")))
    );
    OrderResponse response = service.createOrder(command);

    // Assert
    assertNotNull(response);
    verify(mockRepo, times(2)).save(any(Order.class));
    verify(mockPayment).processPayment(any(PaymentRequest.class));
    verify(mockNotification).sendOrderConfirmation(any(Order.class));
}
```

---

### 2. Constructor Injection & Dependency Management

**Use Case:** Immutable, testable dependencies with clear contracts

```java
// Anti-pattern: Field injection
@Service
public class BadOrderService {
    @Autowired
    private OrderRepository orderRepository; // Mutable, hard to test

    @Autowired
    private PaymentService paymentService;

    // Cannot enforce required dependencies
}

// Best Practice: Constructor injection
@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final NotificationService notificationService;

    // Single constructor - @Autowired optional in Spring Boot
    public OrderService(
            OrderRepository orderRepository,
            PaymentService paymentService,
            NotificationService notificationService) {
        this.orderRepository = Objects.requireNonNull(orderRepository);
        this.paymentService = Objects.requireNonNull(paymentService);
        this.notificationService = Objects.requireNonNull(notificationService);
    }

    public Order createOrder(CreateOrderRequest request) {
        Order order = Order.from(request);
        Order saved = orderRepository.save(order);

        PaymentResult payment = paymentService.processPayment(saved);
        if (payment.isSuccessful()) {
            notificationService.sendConfirmation(saved);
        }

        return saved;
    }
}

// Optional dependencies pattern
@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final Optional<CacheService> cacheService;

    public ProductService(
            ProductRepository productRepository,
            Optional<CacheService> cacheService) { // Optional for conditional beans
        this.productRepository = productRepository;
        this.cacheService = cacheService;
    }

    public Product findById(String id) {
        return cacheService
            .flatMap(cache -> cache.get(id, Product.class))
            .orElseGet(() -> {
                Product product = productRepository.findById(id)
                    .orElseThrow(() -> new ProductNotFoundException(id));
                cacheService.ifPresent(cache -> cache.put(id, product));
                return product;
            });
    }
}

// Configuration with constructor injection
@Configuration
public class ServiceConfiguration {

    @Bean
    public OrderService orderService(
            OrderRepository orderRepository,
            PaymentService paymentService,
            NotificationService notificationService) {
        return new OrderService(orderRepository, paymentService, notificationService);
    }

    @Bean
    @ConditionalOnProperty(name = "cache.enabled", havingValue = "true")
    public CacheService cacheService(CacheProperties properties) {
        return new RedisCacheService(properties);
    }
}

// Qualifier pattern for multiple implementations
@Service
public class PaymentProcessingService {

    private final PaymentGateway primaryGateway;
    private final PaymentGateway fallbackGateway;

    public PaymentProcessingService(
            @Qualifier("stripe") PaymentGateway primaryGateway,
            @Qualifier("paypal") PaymentGateway fallbackGateway) {
        this.primaryGateway = primaryGateway;
        this.fallbackGateway = fallbackGateway;
    }

    public PaymentResult processPayment(PaymentRequest request) {
        try {
            return primaryGateway.process(request);
        } catch (PaymentException e) {
            log.warn("Primary gateway failed, using fallback", e);
            return fallbackGateway.process(request);
        }
    }
}

@Configuration
public class PaymentGatewayConfig {

    @Bean
    @Qualifier("stripe")
    public PaymentGateway stripeGateway(StripeProperties properties) {
        return new StripePaymentGateway(properties);
    }

    @Bean
    @Qualifier("paypal")
    public PaymentGateway paypalGateway(PayPalProperties properties) {
        return new PayPalPaymentGateway(properties);
    }
}
```

**Production Benefits:**
- Immutable dependencies (thread-safe)
- Explicit dependency contracts
- Easy to test (pass mocks in constructor)
- Compiler-enforced required dependencies

**Testing Pattern:**
```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private PaymentService paymentService;

    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private OrderService orderService;

    @Test
    void shouldCreateOrderSuccessfully() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(/*...*/);
        Order order = Order.from(request);
        when(orderRepository.save(any(Order.class))).thenReturn(order);
        when(paymentService.processPayment(any(Order.class)))
            .thenReturn(PaymentResult.success());

        // When
        Order result = orderService.createOrder(request);

        // Then
        assertNotNull(result);
        verify(notificationService).sendConfirmation(order);
    }
}
```

---

### 3. @Transactional Boundaries and Propagation

**Use Case:** Control transaction scope and behavior for data consistency

```java
// Service layer - transaction boundaries
@Service
@Transactional(readOnly = true) // Default read-only for queries
public class OrderService {

    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final AuditService auditService;

    // Write operation - override class-level transaction
    @Transactional(
        propagation = Propagation.REQUIRED,
        isolation = Isolation.READ_COMMITTED,
        timeout = 30,
        rollbackFor = Exception.class
    )
    public Order createOrder(CreateOrderRequest request) {
        Order order = new Order(request);
        Order saved = orderRepository.save(order);

        // This runs in the same transaction
        paymentService.processPayment(saved);

        // Audit in separate transaction (see below)
        auditService.logOrderCreation(saved);

        return saved;
    }

    // Read-only uses class-level @Transactional(readOnly = true)
    public Order findById(String orderId) {
        return orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }

    public List<Order> findOrdersByCustomer(String customerId, Pageable pageable) {
        return orderRepository.findByCustomerId(customerId, pageable);
    }
}

// Payment service - participates in caller's transaction
@Service
public class PaymentService {

    private final PaymentGateway paymentGateway;
    private final PaymentRepository paymentRepository;

    @Transactional(propagation = Propagation.REQUIRED) // Join existing transaction
    public PaymentResult processPayment(Order order) {
        PaymentResult result = paymentGateway.charge(order.getTotal());

        Payment payment = new Payment(order.getId(), result);
        paymentRepository.save(payment);

        if (!result.isSuccessful()) {
            // This will rollback both payment and order creation
            throw new PaymentFailedException("Payment declined");
        }

        return result;
    }
}

// Audit service - independent transaction
@Service
public class AuditService {

    private final AuditLogRepository auditRepository;

    @Transactional(propagation = Propagation.REQUIRES_NEW) // Always new transaction
    public void logOrderCreation(Order order) {
        AuditLog log = new AuditLog(
            "ORDER_CREATED",
            order.getId(),
            LocalDateTime.now()
        );
        auditRepository.save(log);

        // Even if outer transaction rolls back, audit log persists
    }
}

// Complex propagation scenarios
@Service
public class OrderBatchService {

    private final OrderService orderService;
    private final NotificationService notificationService;

    @Transactional(propagation = Propagation.REQUIRED)
    public BatchResult processBatch(List<CreateOrderRequest> requests) {
        List<Order> successfulOrders = new ArrayList<>();
        List<String> failures = new ArrayList<>();

        for (CreateOrderRequest request : requests) {
            try {
                // Each order in separate transaction - failures don't affect others
                Order order = orderService.createOrderInNewTransaction(request);
                successfulOrders.add(order);
            } catch (Exception e) {
                failures.add("Order failed: " + e.getMessage());
            }
        }

        return new BatchResult(successfulOrders, failures);
    }
}

@Service
public class OrderService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public Order createOrderInNewTransaction(CreateOrderRequest request) {
        // This runs in its own transaction, isolated from caller
        return createOrder(request);
    }
}

// Programmatic transaction control
@Service
public class AdvancedOrderService {

    private final TransactionTemplate transactionTemplate;
    private final OrderRepository orderRepository;

    public AdvancedOrderService(PlatformTransactionManager transactionManager,
                               OrderRepository orderRepository) {
        this.transactionTemplate = new TransactionTemplate(transactionManager);
        this.transactionTemplate.setIsolationLevel(TransactionDefinition.ISOLATION_SERIALIZABLE);
        this.orderRepository = orderRepository;
    }

    public Order createOrderWithCustomControl(CreateOrderRequest request) {
        return transactionTemplate.execute(status -> {
            try {
                Order order = new Order(request);
                Order saved = orderRepository.save(order);

                if (!validateOrder(saved)) {
                    status.setRollbackOnly(); // Manual rollback
                    return null;
                }

                return saved;
            } catch (Exception e) {
                status.setRollbackOnly();
                throw e;
            }
        });
    }
}
```

**Propagation Levels Quick Reference:**

| Propagation | Behavior | Use Case |
|-------------|----------|----------|
| REQUIRED (default) | Join existing or create new | Most operations |
| REQUIRES_NEW | Always create new transaction | Audit logs, independent operations |
| SUPPORTS | Join if exists, non-transactional otherwise | Read operations |
| MANDATORY | Must have existing transaction | Enforced transactional context |
| NOT_SUPPORTED | Suspend current transaction | Performance-critical reads |
| NEVER | Fail if transaction exists | Pure non-transactional code |
| NESTED | Create nested savepoint | Partial rollback scenarios |

**Production Benefits:**
- Prevent data inconsistency
- Control transaction scope precisely
- Handle failures gracefully
- Optimize read-only queries

**Testing Pattern:**
```java
@SpringBootTest
@Transactional // Test transactions auto-rollback
class OrderServiceTransactionTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private PaymentService paymentService;

    @Test
    void shouldRollbackOrderWhenPaymentFails() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(/*...*/);

        // Simulate payment failure
        doThrow(new PaymentFailedException("Declined"))
            .when(paymentService).processPayment(any());

        // When/Then
        assertThrows(PaymentFailedException.class,
            () -> orderService.createOrder(request));

        // Verify transaction rolled back
        List<Order> orders = orderRepository.findAll();
        assertTrue(orders.isEmpty());
    }

    @Test
    void shouldPersistAuditLogEvenWhenOrderRollsBack() {
        // REQUIRES_NEW propagation test
        // (requires specific test configuration)
    }
}
```

---

### 4. Spring Data JPA Optimization Patterns

**Use Case:** Avoid N+1 queries, optimize fetching, improve performance

```java
// Entity with fetch optimization
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY) // Always use LAZY by default
    @JoinColumn(name = "customer_id")
    private Customer customer;

    @OneToMany(
        mappedBy = "order",
        cascade = CascadeType.ALL,
        orphanRemoval = true,
        fetch = FetchType.LAZY
    )
    private List<OrderItem> items = new ArrayList<>();

    private LocalDateTime createdAt;
    private OrderStatus status;
}

// Repository with fetch joins
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // Anti-pattern: Causes N+1 queries
    List<Order> findByStatus(OrderStatus status);

    // Optimized: Fetch order with customer in single query
    @Query("SELECT o FROM Order o JOIN FETCH o.customer WHERE o.status = :status")
    List<Order> findByStatusWithCustomer(@Param("status") OrderStatus status);

    // Optimized: Fetch order with items in single query
    @Query("SELECT DISTINCT o FROM Order o " +
           "LEFT JOIN FETCH o.items " +
           "WHERE o.status = :status")
    List<Order> findByStatusWithItems(@Param("status") OrderStatus status);

    // Multiple fetch joins (careful with cartesian product)
    @Query("SELECT DISTINCT o FROM Order o " +
           "LEFT JOIN FETCH o.customer " +
           "LEFT JOIN FETCH o.items " +
           "WHERE o.id = :id")
    Optional<Order> findByIdWithAssociations(@Param("id") Long id);

    // Entity graph approach (alternative to JOIN FETCH)
    @EntityGraph(attributePaths = {"customer", "items"})
    @Query("SELECT o FROM Order o WHERE o.status = :status")
    List<Order> findByStatusWithEntityGraph(@Param("status") OrderStatus status);

    // Pagination with fetch join
    @Query(value = "SELECT DISTINCT o FROM Order o " +
                   "LEFT JOIN FETCH o.customer " +
                   "WHERE o.status = :status",
           countQuery = "SELECT COUNT(DISTINCT o) FROM Order o WHERE o.status = :status")
    Page<Order> findByStatusWithCustomerPaged(
        @Param("status") OrderStatus status,
        Pageable pageable
    );

    // Projection for read-only DTOs (best performance)
    @Query("SELECT new com.example.dto.OrderSummaryDTO(" +
           "o.id, o.createdAt, o.status, c.name, SIZE(o.items)) " +
           "FROM Order o JOIN o.customer c WHERE o.status = :status")
    List<OrderSummaryDTO> findOrderSummaries(@Param("status") OrderStatus status);

    // Spring Data Projection interface
    interface OrderProjection {
        Long getId();
        LocalDateTime getCreatedAt();
        OrderStatus getStatus();
        CustomerProjection getCustomer();

        interface CustomerProjection {
            String getName();
            String getEmail();
        }
    }

    List<OrderProjection> findByStatusOrderByCreatedAtDesc(OrderStatus status);
}

// Service layer optimization patterns
@Service
@Transactional(readOnly = true)
public class OrderQueryService {

    private final OrderRepository orderRepository;

    public List<OrderDTO> findActiveOrders() {
        // Use projection for best performance
        return orderRepository.findOrderSummaries(OrderStatus.ACTIVE)
            .stream()
            .map(OrderDTO::from)
            .toList();
    }

    public OrderDetailDTO findOrderDetails(Long orderId) {
        // Fetch all associations in single query
        Order order = orderRepository.findByIdWithAssociations(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        return OrderDetailDTO.from(order);
    }
}

// Batch operations optimization
@Service
@Transactional
public class OrderBatchService {

    private final EntityManager entityManager;

    public void createOrdersBatch(List<CreateOrderRequest> requests) {
        int batchSize = 50;

        for (int i = 0; i < requests.size(); i++) {
            Order order = new Order(requests.get(i));
            entityManager.persist(order);

            if (i % batchSize == 0 && i > 0) {
                // Flush and clear every 50 inserts
                entityManager.flush();
                entityManager.clear();
            }
        }

        entityManager.flush();
        entityManager.clear();
    }
}

// application.yml configuration
/*
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
          batch_versioned_data: true
        order_inserts: true
        order_updates: true
        query:
          in_clause_parameter_padding: true
    show-sql: false
    open-in-view: false  # Disable OSIV for clear transaction boundaries
*/
```

**Common N+1 Query Problems and Solutions:**

```java
// Problem: N+1 query
@GetMapping("/orders")
public List<OrderDTO> getOrders() {
    List<Order> orders = orderRepository.findAll(); // 1 query
    return orders.stream()
        .map(order -> {
            String customerName = order.getCustomer().getName(); // N queries
            int itemCount = order.getItems().size(); // N more queries
            return new OrderDTO(order.getId(), customerName, itemCount);
        })
        .toList();
}

// Solution 1: JOIN FETCH
@GetMapping("/orders")
public List<OrderDTO> getOrders() {
    List<Order> orders = orderRepository.findAllWithCustomerAndItems(); // 1 query
    return orders.stream()
        .map(order -> new OrderDTO(
            order.getId(),
            order.getCustomer().getName(),
            order.getItems().size()
        ))
        .toList();
}

// Solution 2: DTO Projection (best performance)
@GetMapping("/orders")
public List<OrderSummaryDTO> getOrders() {
    return orderRepository.findOrderSummaries(); // 1 query, no entities loaded
}
```

**Production Benefits:**
- Eliminate N+1 queries
- Reduce database roundtrips
- Lower memory consumption
- Faster response times

**Testing Pattern:**
```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class OrderRepositoryTest {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void shouldFetchOrderWithAssociationsInSingleQuery() {
        // Given
        Customer customer = new Customer("John Doe");
        entityManager.persist(customer);

        Order order = new Order(customer);
        order.addItem(new OrderItem("Item 1", 2));
        order.addItem(new OrderItem("Item 2", 1));
        entityManager.persistAndFlush(order);
        entityManager.clear(); // Clear persistence context

        // When
        Optional<Order> result = orderRepository.findByIdWithAssociations(order.getId());

        // Then
        assertTrue(result.isPresent());

        // Access associations outside transaction - should work due to fetch join
        assertEquals("John Doe", result.get().getCustomer().getName());
        assertEquals(2, result.get().getItems().size());
    }
}
```

---

## Reactive Programming

### 1. Project Reactor Core Patterns

**Use Case:** Non-blocking, backpressure-aware stream processing

```java
// Basic reactive patterns
@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final PriceService priceService;

    // Mono - single value or empty
    public Mono<Product> findById(String productId) {
        return productRepository.findById(productId)
            .switchIfEmpty(Mono.error(new ProductNotFoundException(productId)))
            .doOnSuccess(product -> log.info("Found product: {}", product.getName()))
            .doOnError(error -> log.error("Error finding product", error));
    }

    // Flux - 0..N values
    public Flux<Product> findByCategory(String category) {
        return productRepository.findByCategory(category)
            .filter(Product::isActive)
            .map(this::enrichWithPricing)
            .sort(Comparator.comparing(Product::getPrice))
            .take(10); // Limit to top 10
    }

    // Combining reactive streams
    public Mono<OrderSummary> createOrderSummary(String orderId) {
        Mono<Order> orderMono = orderRepository.findById(orderId);
        Mono<Customer> customerMono = orderMono.flatMap(order ->
            customerRepository.findById(order.getCustomerId())
        );
        Flux<Product> productsFlux = orderMono.flatMapMany(order ->
            Flux.fromIterable(order.getProductIds())
                .flatMap(productRepository::findById)
        );

        return Mono.zip(orderMono, customerMono, productsFlux.collectList())
            .map(tuple -> new OrderSummary(
                tuple.getT1(), // Order
                tuple.getT2(), // Customer
                tuple.getT3()  // List<Product>
            ));
    }

    // Error handling patterns
    public Mono<Product> findProductWithFallback(String productId) {
        return productRepository.findById(productId)
            .onErrorResume(error -> {
                log.warn("Primary lookup failed, trying cache", error);
                return cacheRepository.findById(productId);
            })
            .onErrorReturn(Product.defaultProduct())
            .timeout(Duration.ofSeconds(5))
            .retry(3);
    }

    // Parallel processing
    public Flux<ProcessedOrder> processOrdersParallel(Flux<Order> orders) {
        return orders
            .parallel(4) // Split into 4 parallel rails
            .runOn(Schedulers.parallel())
            .map(this::processOrder)
            .ordered((o1, o2) -> o1.getId().compareTo(o2.getId()))
            .doOnNext(order -> log.info("Processed: {}", order.getId()));
    }
}

// WebFlux Controller
@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Product>> getProduct(@PathVariable String id) {
        return productService.findById(id)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @GetMapping
    public Flux<Product> getProducts(
            @RequestParam String category,
            @RequestParam(defaultValue = "10") int limit) {
        return productService.findByCategory(category)
            .take(limit);
    }

    // Server-Sent Events
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Product> streamProducts() {
        return productService.watchProductUpdates()
            .delayElements(Duration.ofSeconds(1));
    }

    // Handling backpressure
    @PostMapping("/batch")
    public Mono<BatchResult> processBatch(@RequestBody Flux<CreateProductRequest> requests) {
        return requests
            .buffer(100) // Process in chunks of 100
            .flatMap(batch -> productService.createProductsBatch(batch))
            .reduce(BatchResult.empty(), BatchResult::merge);
    }
}

// Advanced operators
@Service
public class AdvancedReactiveService {

    // Combining multiple sources
    public Flux<PriceUpdate> mergePriceFeeds() {
        Flux<PriceUpdate> internalFeed = internalPriceService.watch();
        Flux<PriceUpdate> externalFeed = externalPriceService.watch();

        return Flux.merge(internalFeed, externalFeed)
            .distinct(PriceUpdate::getProductId)
            .window(Duration.ofSeconds(10))
            .flatMap(window -> window.reduce(
                new HashMap<String, PriceUpdate>(),
                (map, update) -> {
                    map.put(update.getProductId(), update);
                    return map;
                }
            ))
            .flatMapIterable(Map::values);
    }

    // Rate limiting
    public Flux<ApiResponse> callExternalApiWithRateLimit(Flux<ApiRequest> requests) {
        return requests
            .delayElements(Duration.ofMillis(100)) // 10 requests per second
            .flatMap(request ->
                webClient.post()
                    .uri("/api/endpoint")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(ApiResponse.class)
                    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)))
            );
    }

    // Buffering and batching
    public Mono<Void> processBatchedEvents(Flux<Event> events) {
        return events
            .bufferTimeout(100, Duration.ofSeconds(5)) // Batch by count or time
            .flatMap(batch -> {
                log.info("Processing batch of {} events", batch.size());
                return eventRepository.saveAll(batch);
            })
            .then();
    }
}
```

**Production Benefits:**
- Non-blocking I/O (handle more requests)
- Built-in backpressure support
- Composable async operations
- Efficient resource utilization

**Testing Pattern:**
```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductService productService;

    @Test
    void shouldReturnProductById() {
        // Given
        Product product = new Product("123", "Test Product");
        when(productRepository.findById("123")).thenReturn(Mono.just(product));

        // When
        Mono<Product> result = productService.findById("123");

        // Then
        StepVerifier.create(result)
            .expectNext(product)
            .verifyComplete();
    }

    @Test
    void shouldHandleNotFound() {
        // Given
        when(productRepository.findById("999")).thenReturn(Mono.empty());

        // When
        Mono<Product> result = productService.findById("999");

        // Then
        StepVerifier.create(result)
            .expectError(ProductNotFoundException.class)
            .verify();
    }

    @Test
    void shouldProcessMultipleProducts() {
        // Given
        Flux<Product> products = Flux.just(
            new Product("1", "Product 1"),
            new Product("2", "Product 2"),
            new Product("3", "Product 3")
        );
        when(productRepository.findByCategory("electronics")).thenReturn(products);

        // When
        Flux<Product> result = productService.findByCategory("electronics");

        // Then
        StepVerifier.create(result)
            .expectNextCount(3)
            .verifyComplete();
    }
}
```

---

### 2. WebFlux vs WebMVC Decision Matrix

**Use Case:** Choose the right web stack for your application needs

```java
// WebMVC (Traditional blocking I/O)
@RestController
@RequestMapping("/api/orders")
public class OrderControllerMVC {

    private final OrderService orderService;
    private final RestTemplate restTemplate; // Blocking HTTP client

    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrder(@PathVariable String id) {
        // Blocking database call
        Order order = orderService.findById(id);

        // Blocking external API call
        Customer customer = restTemplate.getForObject(
            "http://customer-service/customers/" + order.getCustomerId(),
            Customer.class
        );

        order.setCustomer(customer);
        return ResponseEntity.ok(order);
    }

    // Each request ties up a thread while waiting for I/O
    // Good for: Traditional apps, JDBC databases, blocking libraries
}

// WebFlux (Reactive non-blocking I/O)
@RestController
@RequestMapping("/api/orders")
public class OrderControllerWebFlux {

    private final OrderService orderService;
    private final WebClient webClient; // Non-blocking HTTP client

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Order>> getOrder(@PathVariable String id) {
        return orderService.findById(id) // Non-blocking DB call (R2DBC)
            .flatMap(order ->
                webClient.get()
                    .uri("http://customer-service/customers/" + order.getCustomerId())
                    .retrieve()
                    .bodyToMono(Customer.class)
                    .map(customer -> {
                        order.setCustomer(customer);
                        return ResponseEntity.ok(order);
                    })
            );
    }

    // Thread released while waiting for I/O
    // Good for: High concurrency, streaming, reactive systems
}
```

**Decision Matrix:**

| Factor | WebMVC | WebFlux |
|--------|--------|---------|
| **Database** | JDBC (blocking) | R2DBC (reactive) |
| **Concurrency** | Thread-per-request | Event loop (fewer threads) |
| **Libraries** | Mature blocking ecosystem | Reactive libraries required |
| **Learning Curve** | Familiar (synchronous) | Steep (async thinking) |
| **Performance** | Good for CPU-bound | Excellent for I/O-bound |
| **Debugging** | Easier stack traces | Complex async stack traces |
| **Use Cases** | Traditional CRUD, heavy computation | Microservices, streaming, high concurrency |

**When to use WebMVC:**
- Using JDBC/JPA (no reactive drivers available)
- Team unfamiliar with reactive programming
- Application is CPU-bound, not I/O-bound
- Need to use blocking libraries (security, payment gateways)

**When to use WebFlux:**
- Building microservices with service-to-service calls
- Streaming large datasets or Server-Sent Events
- High concurrency requirements (10,000+ concurrent requests)
- All dependencies support reactive (R2DBC, reactive clients)

**Hybrid Approach (use blocking in WebFlux):**
```java
@Service
public class HybridService {

    private final Scheduler jdbcScheduler = Schedulers.boundedElastic();
    private final JdbcTemplate jdbcTemplate;
    private final WebClient webClient;

    // Wrap blocking JDBC call in reactive stream
    public Mono<Order> findOrderWithBlockingDb(String orderId) {
        return Mono.fromCallable(() ->
            // Blocking JDBC call
            jdbcTemplate.queryForObject(
                "SELECT * FROM orders WHERE id = ?",
                new Object[]{orderId},
                Order.class
            )
        )
        .subscribeOn(jdbcScheduler); // Run on dedicated thread pool
    }

    // Combine blocking DB with non-blocking HTTP
    public Mono<OrderDetails> getOrderDetails(String orderId) {
        Mono<Order> orderMono = findOrderWithBlockingDb(orderId);

        return orderMono.flatMap(order ->
            webClient.get()
                .uri("/customers/" + order.getCustomerId())
                .retrieve()
                .bodyToMono(Customer.class)
                .map(customer -> new OrderDetails(order, customer))
        );
    }
}
```

---

### 3. Backpressure Handling

**Use Case:** Prevent overwhelming consumers with data

```java
@Service
public class BackpressureService {

    // Problem: Fast producer, slow consumer
    public Flux<LogEntry> streamLogs() {
        return Flux.interval(Duration.ofMillis(1)) // 1000 items/second
            .map(i -> new LogEntry("Log " + i, LocalDateTime.now()));
    }

    // Solution 1: Buffer with size limit
    public Flux<List<LogEntry>> streamLogsBuffered() {
        return streamLogs()
            .buffer(100) // Collect 100 items before emitting
            .doOnNext(batch -> log.info("Processing batch of {}", batch.size()));
    }

    // Solution 2: Buffer with time window
    public Flux<List<LogEntry>> streamLogsBufferedByTime() {
        return streamLogs()
            .bufferTimeout(100, Duration.ofSeconds(5)) // Max 100 items OR 5 seconds
            .doOnNext(batch -> log.info("Processing batch of {}", batch.size()));
    }

    // Solution 3: Sample (drop intermediate values)
    public Flux<LogEntry> streamLogsSampled() {
        return streamLogs()
            .sample(Duration.ofSeconds(1)) // Emit only latest value per second
            .doOnNext(log -> log.info("Sampled: {}", log));
    }

    // Solution 4: onBackpressureBuffer with strategy
    public Flux<LogEntry> streamLogsWithBackpressureBuffer() {
        return streamLogs()
            .onBackpressureBuffer(
                1000, // Buffer size
                dropped -> log.warn("Dropped log entry: {}", dropped),
                BufferOverflowStrategy.DROP_OLDEST
            );
    }

    // Solution 5: onBackpressureDrop
    public Flux<LogEntry> streamLogsWithDrop() {
        return streamLogs()
            .onBackpressureDrop(dropped ->
                log.warn("Dropped log entry: {}", dropped)
            );
    }

    // Solution 6: onBackpressureLatest (keep only latest)
    public Flux<LogEntry> streamLogsWithLatest() {
        return streamLogs()
            .onBackpressureLatest()
            .doOnNext(log -> log.info("Processing: {}", log));
    }
}

// Real-world example: Processing order events
@Service
public class OrderEventProcessor {

    private final OrderRepository orderRepository;
    private final NotificationService notificationService;

    public Flux<OrderEvent> processOrderEvents(Flux<OrderEvent> events) {
        return events
            // 1. Buffer incoming events
            .bufferTimeout(50, Duration.ofSeconds(2))

            // 2. Process batches in parallel
            .flatMap(batch ->
                Flux.fromIterable(batch)
                    .parallel(4)
                    .runOn(Schedulers.parallel())
                    .flatMap(this::processEvent)
                    .sequential()
            )

            // 3. Handle backpressure from downstream
            .onBackpressureBuffer(
                1000,
                dropped -> log.error("Dropped event: {}", dropped.getId()),
                BufferOverflowStrategy.DROP_LATEST
            );
    }

    private Mono<OrderEvent> processEvent(OrderEvent event) {
        return orderRepository.save(event.toOrder())
            .flatMap(order ->
                notificationService.sendOrderUpdate(order)
                    .thenReturn(event)
            )
            .timeout(Duration.ofSeconds(10))
            .onErrorResume(error -> {
                log.error("Failed to process event: {}", event.getId(), error);
                return Mono.empty();
            });
    }
}

// WebFlux endpoint with backpressure
@RestController
@RequestMapping("/api/events")
public class EventStreamController {

    private final EventService eventService;

    @GetMapping(produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<EventDTO>> streamEvents() {
        return eventService.watchEvents()
            .map(event -> ServerSentEvent.builder(event)
                .id(event.getId())
                .event("order-update")
                .build())
            .onBackpressureLatest() // Client can't keep up? Send only latest
            .doOnCancel(() -> log.info("Client disconnected"));
    }
}
```

**Backpressure Strategies:**

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `buffer()` | Collect items, emit in batches | Batch processing |
| `onBackpressureBuffer()` | Queue items with size limit | Temporary spikes |
| `onBackpressureDrop()` | Drop items if consumer slow | Lossy streams (metrics) |
| `onBackpressureLatest()` | Keep only latest item | Real-time updates |
| `sample()` | Emit periodically | Rate limiting |
| `bufferTimeout()` | Batch by count or time | Flexible batching |

**Production Benefits:**
- Prevent memory exhaustion
- Handle varying consumer speeds
- Graceful degradation under load
- Control resource consumption

---

## Concurrency & Performance

### 1. CompletableFuture Patterns

**Use Case:** Async programming with composable futures

```java
@Service
public class OrderProcessingService {

    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;
    private final ExecutorService executor;

    // Sequential processing (slow)
    public Order processOrderSequential(CreateOrderRequest request) {
        Order order = orderRepository.save(new Order(request)); // 100ms
        PaymentResult payment = paymentService.process(order); // 500ms
        InventoryResult inventory = inventoryService.reserve(order); // 300ms
        notificationService.send(order); // 200ms
        return order; // Total: 1100ms
    }

    // Parallel processing with CompletableFuture (fast)
    public CompletableFuture<Order> processOrderAsync(CreateOrderRequest request) {
        return CompletableFuture.supplyAsync(() ->
            orderRepository.save(new Order(request)), executor
        )
        .thenCompose(order -> {
            // Run payment and inventory in parallel
            CompletableFuture<PaymentResult> paymentFuture =
                CompletableFuture.supplyAsync(() ->
                    paymentService.process(order), executor
                );

            CompletableFuture<InventoryResult> inventoryFuture =
                CompletableFuture.supplyAsync(() ->
                    inventoryService.reserve(order), executor
                );

            return CompletableFuture.allOf(paymentFuture, inventoryFuture)
                .thenApply(v -> {
                    PaymentResult payment = paymentFuture.join();
                    InventoryResult inventory = inventoryFuture.join();

                    if (payment.isSuccessful() && inventory.isSuccessful()) {
                        order.setStatus(OrderStatus.CONFIRMED);
                    } else {
                        order.setStatus(OrderStatus.FAILED);
                    }

                    return order;
                });
        })
        .thenApply(order -> {
            notificationService.send(order);
            return order;
        })
        .exceptionally(ex -> {
            log.error("Order processing failed", ex);
            return Order.failed();
        }); // Total: ~500ms (parallelized)
    }

    // Combining multiple futures
    public CompletableFuture<OrderSummary> getOrderSummary(String orderId) {
        CompletableFuture<Order> orderFuture =
            CompletableFuture.supplyAsync(() ->
                orderRepository.findById(orderId), executor
            );

        CompletableFuture<Customer> customerFuture = orderFuture
            .thenCompose(order ->
                CompletableFuture.supplyAsync(() ->
                    customerService.findById(order.getCustomerId()), executor
                )
            );

        CompletableFuture<List<Item>> itemsFuture = orderFuture
            .thenCompose(order ->
                CompletableFuture.supplyAsync(() ->
                    itemService.findByOrderId(order.getId()), executor
                )
            );

        return CompletableFuture.allOf(orderFuture, customerFuture, itemsFuture)
            .thenApply(v -> new OrderSummary(
                orderFuture.join(),
                customerFuture.join(),
                itemsFuture.join()
            ));
    }

    // Timeout and fallback
    public CompletableFuture<PriceQuote> getPriceWithTimeout(String productId) {
        return CompletableFuture.supplyAsync(() ->
            externalPriceService.getQuote(productId), executor
        )
        .orTimeout(3, TimeUnit.SECONDS)
        .exceptionally(ex -> {
            log.warn("Price service timeout, using cached price", ex);
            return cacheService.getCachedPrice(productId);
        });
    }

    // Race multiple suppliers
    public CompletableFuture<ShippingQuote> getBestShippingQuote(Order order) {
        CompletableFuture<ShippingQuote> fedexFuture =
            CompletableFuture.supplyAsync(() ->
                fedexService.getQuote(order), executor
            );

        CompletableFuture<ShippingQuote> upsFuture =
            CompletableFuture.supplyAsync(() ->
                upsService.getQuote(order), executor
            );

        CompletableFuture<ShippingQuote> dhlFuture =
            CompletableFuture.supplyAsync(() ->
                dhlService.getQuote(order), executor
            );

        return CompletableFuture.anyOf(fedexFuture, upsFuture, dhlFuture)
            .thenApply(result -> (ShippingQuote) result);
    }

    // Error handling patterns
    public CompletableFuture<Order> processWithRetry(CreateOrderRequest request) {
        return CompletableFuture.supplyAsync(() ->
            processOrder(request), executor
        )
        .handle((result, ex) -> {
            if (ex != null) {
                log.warn("First attempt failed, retrying...", ex);
                return processOrder(request);
            }
            return result;
        })
        .exceptionally(ex -> {
            log.error("All attempts failed", ex);
            return Order.failed();
        });
    }
}

// Spring Boot async configuration
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}

// Controller with async endpoints
@RestController
@RequestMapping("/api/orders")
public class AsyncOrderController {

    private final OrderProcessingService orderService;

    @PostMapping
    public CompletableFuture<ResponseEntity<Order>> createOrder(
            @RequestBody CreateOrderRequest request) {
        return orderService.processOrderAsync(request)
            .thenApply(ResponseEntity::ok)
            .exceptionally(ex ->
                ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build()
            );
    }

    @GetMapping("/{id}/summary")
    public DeferredResult<ResponseEntity<OrderSummary>> getOrderSummary(
            @PathVariable String id) {
        DeferredResult<ResponseEntity<OrderSummary>> deferredResult =
            new DeferredResult<>(5000L); // 5s timeout

        orderService.getOrderSummary(id)
            .thenAccept(summary ->
                deferredResult.setResult(ResponseEntity.ok(summary))
            )
            .exceptionally(ex -> {
                deferredResult.setErrorResult(ex);
                return null;
            });

        return deferredResult;
    }
}
```

**Production Benefits:**
- Parallel execution reduces latency
- Non-blocking async operations
- Composable future chains
- Built-in error handling

**Testing Pattern:**
```java
@SpringBootTest
class OrderProcessingServiceTest {

    @Autowired
    private OrderProcessingService orderService;

    @Test
    void shouldProcessOrderAsync() throws Exception {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(/*...*/);

        // When
        CompletableFuture<Order> future = orderService.processOrderAsync(request);
        Order order = future.get(10, TimeUnit.SECONDS);

        // Then
        assertNotNull(order);
        assertEquals(OrderStatus.CONFIRMED, order.getStatus());
    }

    @Test
    void shouldHandleAsyncErrors() {
        // Given
        CreateOrderRequest invalidRequest = new CreateOrderRequest(/*invalid data*/);

        // When
        CompletableFuture<Order> future = orderService.processOrderAsync(invalidRequest);

        // Then
        Order result = future.join(); // Won't throw due to exceptionally()
        assertEquals(OrderStatus.FAILED, result.getStatus());
    }
}
```

---

### 2. Virtual Threads vs Traditional Threads

**Use Case:** Choosing optimal concurrency model for your workload

```java
// Traditional platform threads (Java < 21)
@Configuration
public class TraditionalThreadConfig {

    @Bean
    public ExecutorService platformThreadPool() {
        return new ThreadPoolExecutor(
            10,     // corePoolSize
            100,    // maxPoolSize
            60L,    // keepAliveTime
            TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(1000),
            new ThreadPoolExecutor.CallerRunsPolicy()
        );
    }
}

// Virtual threads (Java 21+)
@Configuration
public class VirtualThreadConfig {

    @Bean
    public ExecutorService virtualThreadPool() {
        return Executors.newVirtualThreadPerTaskExecutor();
    }

    // Spring Boot 3.2+ supports virtual threads natively
    @Bean
    @ConditionalOnProperty(name = "spring.threads.virtual.enabled", havingValue = "true")
    public TomcatProtocolHandlerCustomizer<?> protocolHandlerVirtualThreadExecutorCustomizer() {
        return protocolHandler -> {
            protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
        };
    }
}

// Comparison: Processing I/O-bound tasks
@Service
public class DataFetchService {

    // Platform threads - limited concurrency
    public List<DataResponse> fetchDataPlatformThreads(List<String> urls) {
        ExecutorService executor = Executors.newFixedThreadPool(100);

        List<Future<DataResponse>> futures = urls.stream()
            .map(url -> executor.submit(() -> fetchFromUrl(url)))
            .toList();

        return futures.stream()
            .map(future -> {
                try {
                    return future.get();
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            })
            .toList();
    }

    // Virtual threads - unlimited concurrency
    public List<DataResponse> fetchDataVirtualThreads(List<String> urls) {
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<DataResponse>> futures = urls.stream()
                .map(url -> executor.submit(() -> fetchFromUrl(url)))
                .toList();

            return futures.stream()
                .map(future -> {
                    try {
                        return future.get();
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                })
                .toList();
        }
    }

    private DataResponse fetchFromUrl(String url) {
        // Blocking I/O call - virtual threads handle this efficiently
        return restTemplate.getForObject(url, DataResponse.class);
    }
}

// Real-world comparison: Web service
@RestController
@RequestMapping("/api/data")
public class DataController {

    private final DataService dataService;

    // Platform threads: ~200 concurrent requests (thread pool limit)
    // Virtual threads: ~1,000,000+ concurrent requests
    @GetMapping("/aggregate")
    public AggregateResponse aggregateData(@RequestParam List<String> sources) {
        // Each source call blocks for I/O
        List<DataResponse> responses = sources.stream()
            .map(dataService::fetchFromSource) // Blocking call
            .toList();

        return new AggregateResponse(responses);
    }
}
```

**Performance Characteristics:**

| Aspect | Platform Threads | Virtual Threads |
|--------|-----------------|-----------------|
| **Creation Cost** | ~1ms, 2MB stack | ~1μs, few KB stack |
| **Max Concurrent** | Thousands | Millions |
| **Blocking I/O** | Wastes thread | Unmounts, frees carrier |
| **CPU-bound** | Good | No benefit (same carriers) |
| **Memory** | ~2MB per thread | ~10KB per thread |
| **Scheduling** | OS scheduler | JVM scheduler |
| **Best For** | CPU-heavy, long-running | I/O-heavy, many concurrent |

**When to Use Virtual Threads:**
- High concurrency I/O operations (database, HTTP calls)
- Microservices with many service-to-service calls
- Request handlers with blocking I/O
- Simplify async code (no callbacks/futures)

**When to Use Platform Threads:**
- CPU-bound computation (calculations, encryption)
- Long-running background tasks
- Pinning concerns (synchronized blocks, JNI)
- Legacy code with ThreadLocal dependencies

**Migration Example:**
```java
// Before: Platform threads
@Service
public class OldOrderService {

    private final ExecutorService executor = Executors.newFixedThreadPool(50);

    public List<Order> processOrders(List<CreateOrderRequest> requests) {
        List<CompletableFuture<Order>> futures = requests.stream()
            .map(request -> CompletableFuture.supplyAsync(() ->
                processOrder(request), executor
            ))
            .toList();

        return futures.stream()
            .map(CompletableFuture::join)
            .toList();
    }
}

// After: Virtual threads (Java 21+)
@Service
public class NewOrderService {

    private final ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

    public List<Order> processOrders(List<CreateOrderRequest> requests) {
        // Same code, but can handle 100x more concurrent requests
        List<CompletableFuture<Order>> futures = requests.stream()
            .map(request -> CompletableFuture.supplyAsync(() ->
                processOrder(request), executor
            ))
            .toList();

        return futures.stream()
            .map(CompletableFuture::join)
            .toList();
    }
}

// Simplified with structured concurrency (Java 21+)
@Service
public class StructuredOrderService {

    public List<Order> processOrders(List<CreateOrderRequest> requests) throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            List<Supplier<Order>> tasks = requests.stream()
                .map(request -> scope.fork(() -> processOrder(request)))
                .toList();

            scope.join();
            scope.throwIfFailed();

            return tasks.stream()
                .map(Supplier::get)
                .toList();
        }
    }
}
```

---

### 3. Concurrent Collections Best Practices

**Use Case:** Thread-safe collections without external synchronization

```java
@Service
public class ConcurrentCollectionService {

    // ConcurrentHashMap - thread-safe, high-performance
    private final ConcurrentMap<String, UserSession> activeSessions =
        new ConcurrentHashMap<>();

    public void addSession(String sessionId, UserSession session) {
        // Atomic put-if-absent
        activeSessions.putIfAbsent(sessionId, session);
    }

    public UserSession getOrCreateSession(String sessionId) {
        // Atomic compute-if-absent
        return activeSessions.computeIfAbsent(sessionId, id ->
            new UserSession(id, LocalDateTime.now())
        );
    }

    public void updateSessionActivity(String sessionId) {
        // Atomic update
        activeSessions.computeIfPresent(sessionId, (id, session) -> {
            session.setLastActivity(LocalDateTime.now());
            return session;
        });
    }

    public void removeExpiredSessions() {
        LocalDateTime expiryTime = LocalDateTime.now().minusMinutes(30);

        // Safe removal during iteration
        activeSessions.entrySet().removeIf(entry ->
            entry.getValue().getLastActivity().isBefore(expiryTime)
        );
    }

    // CopyOnWriteArrayList - thread-safe for read-heavy workloads
    private final List<EventListener> listeners = new CopyOnWriteArrayList<>();

    public void registerListener(EventListener listener) {
        listeners.add(listener); // Copy-on-write: safe but slow for writes
    }

    public void notifyListeners(Event event) {
        // Fast iteration, no locking
        listeners.forEach(listener -> listener.onEvent(event));
    }

    // ConcurrentLinkedQueue - lock-free queue
    private final Queue<Task> taskQueue = new ConcurrentLinkedQueue<>();

    public void enqueueTask(Task task) {
        taskQueue.offer(task); // Lock-free, fast
    }

    public Task pollTask() {
        return taskQueue.poll(); // Lock-free, returns null if empty
    }

    // BlockingQueue - producer-consumer pattern
    private final BlockingQueue<Order> orderQueue =
        new LinkedBlockingQueue<>(1000);

    public void submitOrder(Order order) throws InterruptedException {
        orderQueue.put(order); // Blocks if queue is full
    }

    public Order takeOrder() throws InterruptedException {
        return orderQueue.take(); // Blocks if queue is empty
    }

    // ConcurrentSkipListMap - sorted concurrent map
    private final ConcurrentSkipListMap<Long, PriceUpdate> priceUpdates =
        new ConcurrentSkipListMap<>();

    public void addPriceUpdate(Long timestamp, PriceUpdate update) {
        priceUpdates.put(timestamp, update);
    }

    public List<PriceUpdate> getRecentUpdates(int count) {
        return priceUpdates.descendingMap()
            .values()
            .stream()
            .limit(count)
            .toList();
    }
}

// Producer-Consumer Pattern with BlockingQueue
@Service
public class OrderProcessingPipeline {

    private final BlockingQueue<Order> incomingOrders = new LinkedBlockingQueue<>(1000);
    private final BlockingQueue<Order> validatedOrders = new LinkedBlockingQueue<>(1000);
    private final ExecutorService executorService;

    @PostConstruct
    public void startPipeline() {
        // Start validator threads
        for (int i = 0; i < 5; i++) {
            executorService.submit(this::validateOrders);
        }

        // Start processor threads
        for (int i = 0; i < 10; i++) {
            executorService.submit(this::processOrders);
        }
    }

    private void validateOrders() {
        while (true) {
            try {
                Order order = incomingOrders.take(); // Blocks until available
                if (isValid(order)) {
                    validatedOrders.put(order); // Blocks if queue full
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    private void processOrders() {
        while (true) {
            try {
                Order order = validatedOrders.take();
                processOrder(order);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}

// Cache with ConcurrentHashMap and weak references
@Service
public class CacheService {

    private final ConcurrentMap<String, CachedValue> cache = new ConcurrentHashMap<>();

    public <T> T get(String key, Class<T> type) {
        CachedValue cached = cache.get(key);

        if (cached != null && !cached.isExpired()) {
            return type.cast(cached.getValue());
        }

        // Remove expired entry
        cache.remove(key);
        return null;
    }

    public void put(String key, Object value, Duration ttl) {
        CachedValue cached = new CachedValue(
            value,
            LocalDateTime.now().plus(ttl)
        );
        cache.put(key, cached);
    }

    @Scheduled(fixedRate = 60000) // Every minute
    public void evictExpired() {
        cache.entrySet().removeIf(entry -> entry.getValue().isExpired());
    }

    private static class CachedValue {
        private final Object value;
        private final LocalDateTime expiryTime;

        public CachedValue(Object value, LocalDateTime expiryTime) {
            this.value = value;
            this.expiryTime = expiryTime;
        }

        public boolean isExpired() {
            return LocalDateTime.now().isAfter(expiryTime);
        }

        public Object getValue() {
            return value;
        }
    }
}
```

**Collection Selection Guide:**

| Collection | Thread-Safety | Performance | Use Case |
|-----------|---------------|-------------|----------|
| `ConcurrentHashMap` | Yes | High | General concurrent map |
| `CopyOnWriteArrayList` | Yes | Read: High, Write: Low | Read-heavy lists |
| `ConcurrentLinkedQueue` | Yes | High (lock-free) | Non-blocking queue |
| `LinkedBlockingQueue` | Yes | Medium (blocking) | Producer-consumer |
| `ConcurrentSkipListMap` | Yes | Medium | Sorted concurrent map |
| `HashMap` | No | High | Single-threaded only |
| `ArrayList` | No | High | Single-threaded only |

**Production Benefits:**
- No external synchronization needed
- Better performance than synchronized collections
- Atomic operations (putIfAbsent, computeIfPresent)
- Lock-free algorithms for high throughput

---

## Testing & Quality

### 1. JUnit 5 Advanced Features

**Use Case:** Comprehensive testing with modern JUnit 5

```java
// Nested tests for logical grouping
@SpringBootTest
@DisplayName("Order Service Tests")
class OrderServiceTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderRepository orderRepository;

    @Nested
    @DisplayName("Create Order")
    class CreateOrderTests {

        @Test
        @DisplayName("should create order successfully with valid input")
        void shouldCreateOrderSuccessfully() {
            // Given
            CreateOrderRequest request = new CreateOrderRequest(
                "customer123",
                List.of(new OrderItem("item1", 2, new BigDecimal("10.00")))
            );

            // When
            Order order = orderService.createOrder(request);

            // Then
            assertNotNull(order);
            assertNotNull(order.getId());
            assertEquals(OrderStatus.PENDING, order.getStatus());
        }

        @Test
        @DisplayName("should fail when customer ID is null")
        void shouldFailWithNullCustomerId() {
            // Given
            CreateOrderRequest request = new CreateOrderRequest(null, List.of());

            // When/Then
            assertThrows(IllegalArgumentException.class, () ->
                orderService.createOrder(request)
            );
        }
    }

    @Nested
    @DisplayName("Find Order")
    class FindOrderTests {

        private Order existingOrder;

        @BeforeEach
        void setUp() {
            existingOrder = orderRepository.save(new Order("customer1"));
        }

        @Test
        @DisplayName("should find order by ID")
        void shouldFindOrderById() {
            Optional<Order> found = orderService.findById(existingOrder.getId());
            assertTrue(found.isPresent());
            assertEquals(existingOrder.getId(), found.get().getId());
        }

        @Test
        @DisplayName("should return empty for non-existent order")
        void shouldReturnEmptyForNonExistentOrder() {
            Optional<Order> found = orderService.findById("non-existent");
            assertTrue(found.isEmpty());
        }
    }
}

// Parameterized tests
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class OrderValidationTest {

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "   "})
    @DisplayName("should reject blank customer IDs")
    void shouldRejectBlankCustomerIds(String customerId) {
        CreateOrderRequest request = new CreateOrderRequest(customerId, List.of());
        assertThrows(IllegalArgumentException.class, () ->
            orderService.createOrder(request)
        );
    }

    @ParameterizedTest
    @CsvSource({
        "1, 10.00, 10.00",
        "2, 10.00, 20.00",
        "3, 15.50, 46.50",
        "10, 5.99, 59.90"
    })
    @DisplayName("should calculate total correctly")
    void shouldCalculateTotalCorrectly(int quantity, BigDecimal price, BigDecimal expectedTotal) {
        OrderItem item = new OrderItem("item1", quantity, price);
        BigDecimal total = item.calculateSubtotal();
        assertEquals(0, expectedTotal.compareTo(total));
    }

    @ParameterizedTest
    @MethodSource("orderStatusProvider")
    @DisplayName("should transition to allowed states")
    void shouldTransitionToAllowedStates(OrderStatus from, OrderStatus to, boolean expected) {
        Order order = new Order("customer1");
        order.setStatus(from);

        boolean canTransition = order.canTransitionTo(to);
        assertEquals(expected, canTransition);
    }

    static Stream<Arguments> orderStatusProvider() {
        return Stream.of(
            Arguments.of(OrderStatus.PENDING, OrderStatus.CONFIRMED, true),
            Arguments.of(OrderStatus.PENDING, OrderStatus.CANCELLED, true),
            Arguments.of(OrderStatus.CONFIRMED, OrderStatus.SHIPPED, true),
            Arguments.of(OrderStatus.SHIPPED, OrderStatus.PENDING, false),
            Arguments.of(OrderStatus.CANCELLED, OrderStatus.SHIPPED, false)
        );
    }

    @ParameterizedTest
    @EnumSource(value = OrderStatus.class, names = {"PENDING", "CONFIRMED"})
    @DisplayName("should allow cancellation for specific statuses")
    void shouldAllowCancellationForSpecificStatuses(OrderStatus status) {
        Order order = new Order("customer1");
        order.setStatus(status);

        assertDoesNotThrow(() -> order.cancel());
        assertEquals(OrderStatus.CANCELLED, order.getStatus());
    }
}

// Test lifecycle and execution order
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class OrderIntegrationTest {

    private static String orderId;

    @Test
    @Order(1)
    @DisplayName("Step 1: Create order")
    void step1CreateOrder() {
        Order order = orderService.createOrder(new CreateOrderRequest(/*...*/));
        orderId = order.getId();
        assertNotNull(orderId);
    }

    @Test
    @Order(2)
    @DisplayName("Step 2: Process payment")
    void step2ProcessPayment() {
        assertNotNull(orderId, "Order must be created first");
        PaymentResult result = paymentService.processPayment(orderId);
        assertTrue(result.isSuccessful());
    }

    @Test
    @Order(3)
    @DisplayName("Step 3: Ship order")
    void step3ShipOrder() {
        assertNotNull(orderId, "Order must be created first");
        shippingService.ship(orderId);

        Order order = orderService.findById(orderId).orElseThrow();
        assertEquals(OrderStatus.SHIPPED, order.getStatus());
    }
}

// Conditional test execution
@SpringBootTest
class ConditionalTests {

    @Test
    @EnabledOnOs(OS.LINUX)
    @DisplayName("runs only on Linux")
    void testOnLinux() {
        // Linux-specific test
    }

    @Test
    @EnabledOnJre(JRE.JAVA_21)
    @DisplayName("runs only on Java 21")
    void testOnJava21() {
        // Java 21-specific features
    }

    @Test
    @EnabledIfSystemProperty(named = "test.integration", matches = "true")
    @DisplayName("runs only if system property set")
    void testWithSystemProperty() {
        // Integration test
    }

    @Test
    @EnabledIfEnvironmentVariable(named = "ENV", matches = "dev")
    @DisplayName("runs only in dev environment")
    void testInDevEnvironment() {
        // Dev-specific test
    }
}

// Dynamic tests
class DynamicOrderTests {

    @TestFactory
    Stream<DynamicTest> dynamicTestsFromStream() {
        List<CreateOrderRequest> requests = List.of(
            new CreateOrderRequest("customer1", List.of(/*items*/)),
            new CreateOrderRequest("customer2", List.of(/*items*/)),
            new CreateOrderRequest("customer3", List.of(/*items*/))
        );

        return requests.stream()
            .map(request -> DynamicTest.dynamicTest(
                "Test order for " + request.customerId(),
                () -> {
                    Order order = orderService.createOrder(request);
                    assertNotNull(order);
                }
            ));
    }
}

// Timeout and performance tests
class PerformanceTests {

    @Test
    @Timeout(value = 5, unit = TimeUnit.SECONDS)
    @DisplayName("should complete within 5 seconds")
    void shouldCompleteWithinTimeout() {
        orderService.processBatchOrders(generateLargeOrderBatch());
    }

    @Test
    @DisplayName("should handle concurrent requests")
    void shouldHandleConcurrentRequests() throws Exception {
        int numThreads = 100;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);

        List<Future<Order>> futures = new ArrayList<>();

        for (int i = 0; i < numThreads; i++) {
            futures.add(executor.submit(() -> {
                try {
                    latch.countDown();
                    latch.await(); // Start all threads simultaneously
                    return orderService.createOrder(new CreateOrderRequest(/*...*/));
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }));
        }

        // Verify all orders created successfully
        for (Future<Order> future : futures) {
            Order order = future.get();
            assertNotNull(order);
        }

        executor.shutdown();
    }
}
```

**Production Benefits:**
- Organized test structure with @Nested
- Reduce test duplication with @ParameterizedTest
- Clear test descriptions with @DisplayName
- Conditional execution for environment-specific tests
- Dynamic test generation for data-driven tests

---

### 2. Mockito Best Practices & TestContainers

**Use Case:** Effective mocking and integration testing

```java
// Unit testing with Mockito
@ExtendWith(MockitoExtension.class)
class OrderServiceUnitTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private PaymentService paymentService;

    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private OrderService orderService;

    @Captor
    private ArgumentCaptor<Order> orderCaptor;

    @Test
    void shouldCreateOrderAndProcessPayment() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest("customer1", List.of());
        Order order = new Order(request);

        when(orderRepository.save(any(Order.class))).thenReturn(order);
        when(paymentService.processPayment(any(Order.class)))
            .thenReturn(PaymentResult.success("PAY123"));

        // When
        Order result = orderService.createOrder(request);

        // Then
        assertNotNull(result);
        verify(orderRepository, times(1)).save(any(Order.class));
        verify(paymentService, times(1)).processPayment(any(Order.class));
        verify(notificationService, times(1)).sendOrderConfirmation(any(Order.class));

        // Verify order saved with correct status
        verify(orderRepository).save(orderCaptor.capture());
        Order capturedOrder = orderCaptor.getValue();
        assertEquals(OrderStatus.CONFIRMED, capturedOrder.getStatus());
    }

    @Test
    void shouldRollbackOnPaymentFailure() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest("customer1", List.of());

        when(orderRepository.save(any(Order.class))).thenAnswer(i -> i.getArgument(0));
        when(paymentService.processPayment(any(Order.class)))
            .thenThrow(new PaymentException("Payment declined"));

        // When/Then
        assertThrows(PaymentException.class, () -> orderService.createOrder(request));

        // Verify notification not sent on failure
        verify(notificationService, never()).sendOrderConfirmation(any(Order.class));
    }

    @Test
    void shouldUseDefaultBehaviorForNewProducts() {
        // Given - using BDD style
        given(productRepository.findById("new-product")).willReturn(Optional.empty());

        // When
        Product result = productService.getOrDefault("new-product");

        // Then
        then(productRepository).should().findById("new-product");
        assertNotNull(result);
        assertEquals("default-name", result.getName());
    }
}

// Integration testing with TestContainers
@SpringBootTest
@Testcontainers
class OrderServiceIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
        .withExposedPorts(6379);

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.redis.host", redis::getHost);
        registry.add("spring.redis.port", () -> redis.getMappedPort(6379));
    }

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderRepository orderRepository;

    @Test
    void shouldPersistOrderToDatabase() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(
            "customer123",
            List.of(new OrderItem("item1", 2, new BigDecimal("10.00")))
        );

        // When
        Order order = orderService.createOrder(request);

        // Then
        Optional<Order> found = orderRepository.findById(order.getId());
        assertTrue(found.isPresent());
        assertEquals("customer123", found.get().getCustomerId());
    }
}

// API integration testing with TestContainers and MockMVC
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
@AutoConfigureMockMvc
class OrderControllerIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldCreateOrderViaAPI() throws Exception {
        // Given
        CreateOrderRequest request = new CreateOrderRequest(
            "customer123",
            List.of(new OrderItem("item1", 2, new BigDecimal("10.00")))
        );

        // When/Then
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").exists())
            .andExpect(jsonPath("$.customerId").value("customer123"))
            .andExpect(jsonPath("$.status").value("PENDING"));
    }

    @Test
    void shouldReturnBadRequestForInvalidOrder() throws Exception {
        // Given - invalid request (null customer ID)
        CreateOrderRequest request = new CreateOrderRequest(null, List.of());

        // When/Then
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isBadRequest());
    }
}

// Advanced mocking patterns
@ExtendWith(MockitoExtension.class)
class AdvancedMockingTest {

    @Mock
    private ExternalApiClient apiClient;

    @InjectMocks
    private ProductService productService;

    @Test
    void shouldRetryOnTransientFailure() {
        // Given - fail twice, then succeed
        when(apiClient.fetchProductData("prod1"))
            .thenThrow(new TransientException("Temporary failure"))
            .thenThrow(new TransientException("Still failing"))
            .thenReturn(new ProductData("prod1", "Product 1"));

        // When
        ProductData result = productService.fetchWithRetry("prod1");

        // Then
        assertNotNull(result);
        assertEquals("Product 1", result.getName());
        verify(apiClient, times(3)).fetchProductData("prod1");
    }

    @Test
    void shouldUseCustomAnswer() {
        // Given - custom behavior
        when(orderRepository.save(any(Order.class))).thenAnswer(invocation -> {
            Order order = invocation.getArgument(0);
            order.setId(UUID.randomUUID().toString());
            order.setCreatedAt(LocalDateTime.now());
            return order;
        });

        // When
        Order order = new Order("customer1");
        Order saved = orderRepository.save(order);

        // Then
        assertNotNull(saved.getId());
        assertNotNull(saved.getCreatedAt());
    }

    @Test
    void shouldVerifyInteractionOrder() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest("customer1", List.of());

        // When
        orderService.createOrder(request);

        // Then - verify order of method calls
        InOrder inOrder = inOrder(orderRepository, paymentService, notificationService);
        inOrder.verify(orderRepository).save(any(Order.class));
        inOrder.verify(paymentService).processPayment(any(Order.class));
        inOrder.verify(notificationService).sendOrderConfirmation(any(Order.class));
    }
}
```

**Production Benefits:**
- Isolated unit tests with Mockito
- Real database testing with TestContainers
- Full API integration tests
- Avoid flaky tests with controlled environments
- Fast feedback loop in CI/CD

---

### 3. Test-Driven Development Patterns

**Use Case:** Writing tests first, driving design through tests

```java
// Step 1: Write failing test
@Test
void shouldCalculateOrderTotal() {
    // Given
    Order order = new Order("customer1");
    order.addItem(new OrderItem("item1", 2, new BigDecimal("10.00")));
    order.addItem(new OrderItem("item2", 1, new BigDecimal("15.50")));

    // When
    BigDecimal total = order.calculateTotal();

    // Then
    assertEquals(new BigDecimal("35.50"), total);
}

// Step 2: Write minimal implementation
public class Order {
    private List<OrderItem> items = new ArrayList<>();

    public void addItem(OrderItem item) {
        items.add(item);
    }

    public BigDecimal calculateTotal() {
        return items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}

// Step 3: Refactor and add more tests
@Test
void shouldApplyDiscountToTotal() {
    // Given
    Order order = new Order("customer1");
    order.addItem(new OrderItem("item1", 2, new BigDecimal("10.00")));
    order.applyDiscount(new BigDecimal("0.10")); // 10% discount

    // When
    BigDecimal total = order.calculateTotal();

    // Then
    assertEquals(new BigDecimal("18.00"), total);
}

// Red-Green-Refactor cycle example
@Nested
@DisplayName("Order discount logic")
class OrderDiscountTest {

    @Test
    @DisplayName("RED: should apply percentage discount")
    void shouldApplyPercentageDiscount() {
        Order order = new Order("customer1");
        order.addItem(new OrderItem("item1", 1, new BigDecimal("100.00")));

        order.applyPercentageDiscount(10); // 10%

        assertEquals(new BigDecimal("90.00"), order.calculateTotal());
    }

    // GREEN: Implement just enough to pass
    public void applyPercentageDiscount(int percentage) {
        this.discountPercentage = percentage;
    }

    public BigDecimal calculateTotal() {
        BigDecimal subtotal = items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal discount = subtotal
            .multiply(BigDecimal.valueOf(discountPercentage))
            .divide(BigDecimal.valueOf(100));

        return subtotal.subtract(discount);
    }

    @Test
    @DisplayName("REFACTOR: should apply fixed discount")
    void shouldApplyFixedDiscount() {
        Order order = new Order("customer1");
        order.addItem(new OrderItem("item1", 1, new BigDecimal("100.00")));

        order.applyFixedDiscount(new BigDecimal("15.00"));

        assertEquals(new BigDecimal("85.00"), order.calculateTotal());
    }

    // REFACTOR: Extract discount strategy
    public void applyDiscount(DiscountStrategy strategy) {
        this.discountStrategy = strategy;
    }

    public BigDecimal calculateTotal() {
        BigDecimal subtotal = calculateSubtotal();
        return discountStrategy != null
            ? discountStrategy.apply(subtotal)
            : subtotal;
    }
}
```

**TDD Benefits:**
- Tests drive API design
- High test coverage by default
- Confidence in refactoring
- Clear requirements from tests

---

## Summary

This document covers **20+ advanced Java patterns** across 5 critical areas:

### Modern Java (17-21+) - 4 Patterns
1. Records for immutable DTOs
2. Sealed classes for domain modeling
3. Pattern matching with instanceof and switch
4. Virtual threads (Project Loom)

### Spring Boot Advanced - 4 Patterns
1. Hexagonal architecture (Ports & Adapters)
2. Constructor injection best practices
3. @Transactional boundaries and propagation
4. Spring Data JPA optimization (N+1 queries, fetch joins, projections)

### Reactive Programming - 3 Patterns
1. Project Reactor core patterns (Mono, Flux, operators)
2. WebFlux vs WebMVC decision matrix
3. Backpressure handling strategies

### Concurrency & Performance - 3 Patterns
1. CompletableFuture async patterns
2. Virtual threads vs traditional threads comparison
3. Concurrent collections (ConcurrentHashMap, BlockingQueue, etc.)

### Testing & Quality - 3 Patterns
1. JUnit 5 advanced features (@Nested, @ParameterizedTest, dynamic tests)
2. Mockito best practices + TestContainers integration
3. Test-Driven Development (TDD) workflow

**Key Takeaways:**
- Focus on Java 17+ LTS features (records, sealed classes, pattern matching)
- Spring Boot 3.x with constructor injection and clear transaction boundaries
- Virtual threads (Java 21+) for I/O-heavy workloads
- Reactive programming for high-concurrency microservices
- Comprehensive testing with JUnit 5, Mockito, and TestContainers
- Always optimize database access (avoid N+1 queries)
- Use concurrent collections for thread-safe operations

**Production-Ready Focus:**
- All examples include error handling
- Testing strategies for each pattern
- Performance considerations documented
- Spring Boot integration demonstrated
- Real-world use cases highlighted
