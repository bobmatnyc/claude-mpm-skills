# PHP Code-Quality Anti-Patterns (EspoCRM)

EspoCRM is modern, strictly-typed PHP. The architectural rules (business logic in
Services, data access via EntityManager, no Container injection) are covered elsewhere
in this skill. This reference adds a set of **language-level code-quality defects** —
robustness and changeability issues that degrade maintainability of custom modules,
hooks, and services regardless of architecture.

> **Source note:** The defect families below are derived from CAST Highlight code
> quality indicators (https://doc.casthighlight.com/), cross-referenced with the primary
> sources CAST cites (the PSR coding standards from php-fig.org, and the PHP migration
> guides). Patterns are paraphrased with original EspoCRM-flavored examples; severities
> are review guidance, not CAST's proprietary calibration.

These are a *statistical* signal: one occurrence is minor, but a high density across a
module marks it as a cleanup target. Apply an ~80% confidence filter.

---

## 1. Deprecated PHP4-style constructor naming

**Family: Robustness — Severity: MEDIUM**

Before PHP 5, a constructor was a method whose name matched the class. Since PHP 5 the
constructor is `__construct()`, and same-named-method constructors were **removed in
PHP 8** — a class relying on one will silently not construct as intended (the method
becomes an ordinary method). In an EspoCRM codebase (PHP 8+) this is a latent bug.

**Non-compliant:**
```php
class InvoiceCalculator
{
    public function InvoiceCalculator(EntityManager $em)   // VIOLATION — PHP4 ctor
    {
        $this->entityManager = $em;
    }
}
```

**Compliant — use `__construct`, with constructor-promoted, injected dependencies:**
```php
class InvoiceCalculator
{
    public function __construct(
        private EntityManager $entityManager
    ) {}
}
```

**How to spot it:** a `public` method bearing the exact class name, or a child calling
`parent::ParentClassName()`. Note this also violates EspoCRM's DI rule if it grabs the
Container instead of typed dependencies.

---

## 2. Uppercased control-structure keywords

**Family: Changeability — Severity: LOW**

PHP keywords are case-insensitive, so `IF`, `FOREACH`, `TRY` all run — but mixed casing
hurts readability and breaks the consistency PSR-2/PSR-12 require (lowercase keywords).
EspoCRM follows PSR coding standards; uppercased control keywords stand out as imported
or legacy code.

**Non-compliant:**
```php
FOREACH ($collection as $entity) {           // VIOLATION
    IF ($entity->get('isActive')) {           // VIOLATION
        $this->process($entity);
    }
}
```

**Compliant:**
```php
foreach ($collection as $entity) {
    if ($entity->get('isActive')) {
        $this->process($entity);
    }
}
```

Applies to `if`, `else`, `elseif`, `for`, `foreach`, `do`, `while`, `try`, `catch`,
`switch`. A formatter (php-cs-fixer with the PSR-12 ruleset) fixes all occurrences
mechanically — prefer running it over hand-editing.

---

## 3. `goto`

**Family: Robustness — Severity: MEDIUM**

`goto` jumps unconditionally to a label, obscuring control flow and decoupling the
static text of the program from its dynamic execution. It defeats a reader's ability to
follow a routine top-to-bottom and is essentially never warranted in EspoCRM service or
hook code.

**Non-compliant:**
```php
function importRows(array $rows): void
{
    $i = 0;
    loop:                                     // VIOLATION — label + goto
    if ($i >= count($rows)) { goto done; }
    $this->importRow($rows[$i]);
    $i++;
    goto loop;
    done:
}
```

**Compliant — use structured loops and early returns:**
```php
function importRows(array $rows): void
{
    foreach ($rows as $row) {
        $this->importRow($row);
    }
}
```

There is no false-positive case here worth carving out: treat any `goto` as a finding and
restructure with loops, `break`/`continue`, extracted methods, or early `return`.

---

## 4. Empty `catch` blocks

**Family: Robustness — Severity: MEDIUM**

A `catch` with an empty body swallows the exception and lets the program continue as
though nothing failed — a frequent source of "it silently did nothing" bugs. In a hook
or service, a swallowed `ORMException` or validation failure can leave an entity in a
half-saved state.

**Non-compliant:**
```php
try {
    $this->entityManager->saveEntity($related);
} catch (\Throwable $e) {
    // VIOLATION — swallowed; caller believes the save succeeded
}
```

**Compliant — log and rethrow (or translate to a domain exception):**
```php
try {
    $this->entityManager->saveEntity($related);
} catch (\Throwable $e) {
    $GLOBALS['log']->error('saveEntity failed: ' . $e->getMessage());
    throw new Error('Could not persist related entity', 0, $e);
}
```

**False-positive filter:** A deliberately best-effort operation may ignore failure, but
only with a comment stating why it is safe. An unannotated empty catch is the violation —
and on EntityManager writes, swallowing is almost always wrong.

---

## How these affect an EspoCRM review

These are mostly **LOW/MEDIUM** changeability and robustness findings; none blocks a
merge on its own. Two carry real bug risk on PHP 8: the PHP4 constructor (#1) will not
initialize the object, and an empty catch around an EntityManager write (#4) can mask a
failed persist. The casing (#2) and `goto` (#3) items are best handled by running
php-cs-fixer / a static analyzer (PHPStan) across the module rather than spot-fixing.
Record findings in the review handoff and clean them up while the file is already open.
For PHP defects with a direct *security* dimension (`phpinfo()` in production, missing
`switch` default in access-control code), see the WordPress security-validation skill's
quality reference.
