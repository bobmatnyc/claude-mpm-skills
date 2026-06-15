# Java Robustness & Changeability Anti-Patterns

A focused set of code-quality defects that recur in Spring Boot services, controllers,
and exception handlers. These are **robustness** (correctness/reliability) and
**changeability** (readability/maintainability) issues — they are orthogonal to the
framework patterns (DI, REST, Spring Data) covered in the main skill. Most are caught
by a good static analyzer or a careful reviewer; the value here is knowing *why* each
matters and *what the compliant shape looks like* in idiomatic Java.

> **Source note:** The defect families below are derived from CAST Highlight code
> quality indicators (https://doc.casthighlight.com/), cross-referenced with the
> primary sources CAST itself cites (SonarSource RSPEC rules, the SEI CERT Java
> guidelines, and MISRA). Patterns are paraphrased with original Spring-flavored
> examples; severities are review guidance, not CAST's proprietary calibration.

This is a *statistical* lens: a single occurrence is rarely fatal, but a high density
of these across a service signals reliability and maintenance risk. Apply an ~80%
confidence filter — flag the clear cases, ask a question on the borderline ones.

---

## 1. Nested `try`/`catch` blocks

**Family: Robustness — Severity: MEDIUM**

A `try` block containing another `try`/`catch` makes it hard to reason about which
handler catches which failure, and it usually means two unrelated concerns have been
crammed into one method.

**Non-compliant:**
```java
public Report build(Long userId) {
    try {
        User user = userRepository.findById(userId).orElseThrow();
        if (user.isActive()) {
            try {                                  // nested try — VIOLATION
                return reportClient.fetch(user);
            } catch (IOException e) {
                throw new ReportUnavailableException(userId, e);
            }
        }
        return Report.empty();
    } catch (Exception e) {
        throw new ReportUnavailableException(userId, e);
    }
}
```

**Compliant — extract the inner concern into its own method:**
```java
public Report build(Long userId) {
    User user = userRepository.findById(userId).orElseThrow();
    return user.isActive() ? fetchReport(user) : Report.empty();
}

private Report fetchReport(User user) {
    try {
        return reportClient.fetch(user);
    } catch (IOException e) {
        throw new ReportUnavailableException(user.getId(), e);
    }
}
```

**False-positive filter:** Two sequential (not nested) try blocks are fine. A single
try-with-resources whose body calls a method that itself has a try is not "nested" at
the syntactic level worth flagging — focus on a `try` lexically inside another `try`.

---

## 2. Overly generic `catch (Exception ...)` / `catch (Throwable ...)`

**Family: Robustness — Severity: MEDIUM (HIGH at a boundary that swallows)**

Catching `Exception` or `Throwable` captures failures you never anticipated —
`NullPointerException`, `ClassCastException`, even `Error` subtypes — and routes them
through one handler. It hides the failure surface: when a called method later throws a
*new* checked exception, the compiler will not remind you to handle it differently.

**Non-compliant:**
```java
try {
    parsePayload(body);          // throws ParseException
    validate(body);              // throws ValidationException
    persist(body);               // throws DataAccessException
} catch (Exception e) {          // VIOLATION — one bucket for everything
    log.error("failed", e);
}
```

**Compliant — catch the specific types you can actually handle:**
```java
try {
    parsePayload(body);
    validate(body);
    persist(body);
} catch (ParseException | ValidationException e) {
    throw new BadRequestException(e.getMessage(), e);
} catch (DataAccessException e) {
    throw new StorageException("persist failed", e);
}
```

**Legitimate exception:** A *top-level boundary* deliberately catches broadly to keep a
batch job or a request thread alive (this is exactly what Spring's
`@RestControllerAdvice` catch-all handler does — see the main skill). That is acceptable
**when it is the outermost layer, logs the cause, and is commented as intentional**. The
same `catch (Exception)` buried in a service method is a violation.

---

## 3. Catch clauses that only rethrow

**Family: Robustness — Severity: LOW (noise / misleading)**

A catch whose only statement rethrows the same exception is equivalent to not catching
at all — except it adds code and makes a reader stop to check whether something subtle
is happening. Either remove the clause or give it real work (wrap, enrich, log-and-translate).

**Non-compliant:**
```java
try {
    return service.charge(order);
} catch (PaymentException e) {
    throw e;                      // VIOLATION — adds nothing
}
```

**Compliant — either drop the try entirely:**
```java
return service.charge(order);     // let PaymentException propagate
```

**…or make the catch earn its place by adding context:**
```java
try {
    return service.charge(order);
} catch (PaymentException e) {
    throw new OrderFailedException(order.getId(), e);   // translation + context
}
```

**False-positive filter:** A catch that rethrows *a different* type, or rethrows after
logging / cleanup / metric increment, is not a violation — it is doing real work.

---

## 4. Throwing raw system exceptions

**Family: Robustness — Severity: MEDIUM**

Throwing `java.lang.RuntimeException` or `java.lang.Error` (or `new Exception(...)`)
forces every caller into a generic catch (see #2) and conveys no semantic meaning.
Applications should throw their own typed exceptions so callers can distinguish a
not-found from a conflict from a validation failure — which is also how Spring's
`@ExceptionHandler` routing decides the HTTP status.

**Non-compliant:**
```java
public Account load(Long id) {
    Account a = repo.findById(id).orElse(null);
    if (a == null) {
        throw new RuntimeException("no account " + id);   // VIOLATION
    }
    return a;
}
```

**Compliant — a domain exception the advice layer maps to 404:**
```java
public Account load(Long id) {
    return repo.findById(id)
        .orElseThrow(() -> new AccountNotFoundException(id));
}
```

**False-positive filter:** Framework-mandated unchecked throws and genuinely
programmer-error guards (`throw new IllegalArgumentException(...)` for a contract
violation) are idiomatic and not flagged — the target is *opaque* `RuntimeException` /
`Exception` used as a lazy signal.

---

## 5. Collapsible nested `if`

**Family: Changeability — Severity: LOW**

Two nested `if` statements, neither with an `else`, where the inner `if` is the only
statement in the outer, should be a single combined condition. Collapsing improves
readability and reduces nesting depth.

**Non-compliant:**
```java
if (file != null) {
    if (file.isFile() || file.isDirectory()) {   // VIOLATION — collapsible
        process(file);
    }
}
```

**Compliant:**
```java
if (file != null && (file.isFile() || file.isDirectory())) {
    process(file);
}
```

**False-positive filter:** Does **not** apply when the outer `if` has an `else`, when the
inner `if` has an `else`, or when the inner `if` is not the sole statement of the outer
(e.g., other statements follow it). Also do not collapse when an early-return guard
(`if (file == null) return;`) reads more clearly than a compound condition — that is a
different, often-preferable pattern.

---

## 6. `if … else if` without a final `else`

**Family: Robustness — Severity: MEDIUM**

A chain of `if … else if` that lacks a terminal `else` silently does nothing for any
input the author did not enumerate. Defensive programming requires a final `else` that
either handles the residual case or carries a comment stating why no action is correct.
This mirrors the "switch needs a default" rule (#8).

**Non-compliant:**
```java
if (status == Status.PENDING) {
    enqueue(order);
} else if (status == Status.PAID) {
    ship(order);
}
// unhandled: CANCELLED, REFUNDED, ... fall through silently — VIOLATION
```

**Compliant:**
```java
if (status == Status.PENDING) {
    enqueue(order);
} else if (status == Status.PAID) {
    ship(order);
} else {
    throw new IllegalStateException("unhandled order status: " + status);
}
```

**False-positive filter:** When every branch ends in `return`/`throw`, the code after the
chain already behaves as the implicit `else`, so a missing trailing `else` is acceptable.
Modern Java often replaces the whole chain with an exhaustive `switch` expression over an
`enum`/sealed type, which the compiler checks for completeness — prefer that where it fits.

---

## 7. Loop counter modified inside the loop body

**Family: Robustness — Severity: MEDIUM**

Reassigning a `for` loop's counter inside the body (beyond the loop's own update
clause) makes iteration count hard to predict and is a classic source of off-by-N and
skip/infinite-loop bugs. Logical control flags may be updated in the body; the *counter*
should not be.

**Non-compliant:**
```java
for (int i = 0; i < items.size(); i++) {
    handle(items.get(i));
    if (items.get(i).isBatchBoundary()) {
        i += 2;                     // VIOLATION — counter mutated in body
    }
}
```

**Compliant — model the skip explicitly, or use a higher-level construct:**
```java
for (int i = 0; i < items.size(); i++) {
    Item item = items.get(i);
    if (shouldSkip(item)) {
        continue;                   // intent is explicit; counter untouched
    }
    handle(item);
}
// or, when no index is needed:
items.stream().filter(this::shouldProcess).forEach(this::handle);
```

**False-positive filter:** Updating a *separate* control variable (a `boolean done`
flag tested in the condition) is permitted. Genuinely index-driven algorithms that must
advance irregularly (parsers, sliding windows) may need manual index control — prefer a
`while` loop there so the manual advancement is not disguised as a `for`.

---

## 8. Switch hygiene: missing `default` and missing `break`

**Family: Robustness — Severity: MEDIUM**

Two related defects:

- **No `default` clause** — like a missing final `else` (#6), unenumerated values pass
  through unhandled. CWE-478 ("missing default case") links this to cascading failures.
- **Fall-through from a non-empty case** — a `case` with statements but no terminating
  `break`/`return`/`throw`/`continue` falls into the next case, usually unintentionally.

**Non-compliant:**
```java
switch (plan) {
    case FREE:
        applyFreeLimits(account);
        // VIOLATION: no break — falls into PRO
    case PRO:
        applyProLimits(account);
        break;
    // VIOLATION: no default — ENTERPRISE silently unhandled
}
```

**Compliant — terminate every non-empty case and always provide a default:**
```java
switch (plan) {
    case FREE -> applyFreeLimits(account);     // arrow form: no fall-through possible
    case PRO -> applyProLimits(account);
    case ENTERPRISE -> applyEnterpriseLimits(account);
    default -> throw new IllegalStateException("unknown plan: " + plan);
}
```

**Guidance:** Prefer the **arrow `switch`** (Java 14+) — it cannot fall through and, over
an `enum` or sealed type, the compiler enforces exhaustiveness so a `default` may even be
unnecessary. Stacked labels sharing one body (`case A: case B: doX(); break;`) are
*empty* intermediate cases and are not fall-through violations.

---

## 9. Nested `switch` statements

**Family: Transferability — Severity: LOW**

A `switch` inside another `switch` is easy to misread — a reader can mistake an inner
`case` for an outer one. Extract the inner switch into a well-named method.

**Non-compliant:**
```java
switch (region) {
    case US:
        switch (state) {            // VIOLATION — nested switch
            case CA: return californiaRate();
            default: return usDefaultRate();
        }
    default:
        return globalRate();
}
```

**Compliant:**
```java
switch (region) {
    case US -> usStateRate(state);   // inner switch lives in its own method
    default -> globalRate();
}
```

**False-positive filter:** A single, shallow nested switch over a small fixed set may be
clearer inline than split. Flag it as a readability question, not a hard finding —
weight it by nesting depth and case count.

---

## How these affect a Spring Boot review

These items are predominantly **MEDIUM/LOW** and do not, by themselves, block a merge.
Their value is as a density signal: a service class carrying several of them (generic
catches + rethrow-only catches + raw `RuntimeException` throws) is a reliability hotspot
worth refactoring before adding features. Two of them interlock with framework design:
typed domain exceptions (#4) drive `@RestControllerAdvice` status mapping, and the
deliberate top-level catch-all (#2 exception) is the *one* place a broad catch is correct.
Record MEDIUM findings in the review handoff; fix LOW ones opportunistically while the
code is already open.
