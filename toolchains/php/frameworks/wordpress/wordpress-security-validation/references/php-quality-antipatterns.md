# PHP Code-Quality Anti-Patterns (Security & Robustness)

The main skill covers the three-layer model (sanitize → validate → escape) and the big
attack classes (XSS, CSRF, SQLi). This reference adds a complementary set of **PHP
code-quality defects** that create reliability and *information-disclosure* risk even
when the three-layer model is otherwise applied. They are the kind of finding a security
reviewer flags that a feature checklist misses.

> **Source note:** The defect families below are derived from CAST Highlight code
> quality indicators (https://doc.casthighlight.com/), cross-referenced with the primary
> sources CAST cites (MITRE/CWE, PSR coding standards). Patterns are paraphrased with
> original WordPress/PHP examples; severities are review guidance, not CAST's proprietary
> calibration.

---

## 1. `phpinfo()` (and friends) left in production code

**Family: Security — Severity: HIGH**

`phpinfo()` dumps the full PHP configuration: loaded extensions, absolute paths, OS and
version details, environment variables, and sometimes secrets. Reachable in production it
is a reconnaissance gift to an attacker mapping the server. The same applies to other
debug-leak surfaces in WordPress.

**Non-compliant:**
```php
// in a plugin file that ships to production
add_action('admin_menu', function () {
    add_menu_page('Diag', 'Diag', 'manage_options', 'diag', function () {
        phpinfo();                       // VIOLATION — exposes server internals
    });
});
```

**Compliant — gate any diagnostic behind an explicit debug constant, never ship it on:**
```php
if (defined('WP_DEBUG') && WP_DEBUG && current_user_can('manage_options')) {
    // local-only diagnostics; still capability-gated
    error_log('php version: ' . PHP_VERSION);
}
```

**Related leaks to flag the same way:** `var_dump()`/`print_r()` to the page,
`define('WP_DEBUG_DISPLAY', true)` in production, `error_reporting(E_ALL)` with display,
and committed `define('WP_DEBUG', true)`. Production should run `WP_DEBUG = false` and
log to file, not screen (this is already on the skill's Code-Quality checklist).

---

## 2. Empty `catch` blocks

**Family: Robustness / Security — Severity: MEDIUM (HIGH when it hides a security failure)**

A `catch` with no body swallows the exception: the program continues as if nothing went
wrong, masking the error. From a security standpoint this is dangerous — a failed
signature check, a failed capability lookup, or a failed remote validation can be
silently ignored, and the code proceeds down the "success" path.

**Non-compliant:**
```php
try {
    $verified = verify_remote_signature($payload, $signature);
} catch (SignatureException $e) {
    // VIOLATION — empty catch; $verified is now undefined and we fall through
}
if ($verified) {              // may evaluate stale/undefined state
    process($payload);
}
```

**Compliant — handle, translate, or at minimum log and fail closed:**
```php
try {
    $verified = verify_remote_signature($payload, $signature);
} catch (SignatureException $e) {
    error_log('signature verification error: ' . $e->getMessage());
    wp_die(esc_html__('Could not verify request.', 'my-plugin'));   // fail closed
}
```

**False-positive filter:** A catch that is genuinely empty *by design* must say so with a
comment explaining why ignoring is safe (e.g., a best-effort cache warm where failure is
acceptable). An unannotated empty catch is the violation. Never use an empty catch on a
security-relevant operation.

---

## 3. `switch` without a `default` case

**Family: Security — Severity: MEDIUM**

CWE-478 ("missing default case in a multiple condition expression") ties this to
cascading failures: when not every value of a variable is handled, downstream decisions
run on incomplete information. In access-control or routing code this can fail *open*.

**Non-compliant:**
```php
switch ($action) {
    case 'view':
        if (current_user_can('read')) { render(); }
        break;
    case 'edit':
        if (current_user_can('edit_posts')) { edit(); }
        break;
    // VIOLATION — an unexpected $action silently does nothing (or worse, falls through)
}
```

**Compliant — always specify a default that handles the unexpected explicitly:**
```php
switch ($action) {
    case 'view':
        if (current_user_can('read')) { render(); }
        break;
    case 'edit':
        if (current_user_can('edit_posts')) { edit(); }
        break;
    default:
        wp_die(esc_html__('Unknown action.', 'my-plugin'), 400);   // fail closed
}
```

**Guidance:** A `default` used merely to stand in for an "assumed" valid option is, per
MITRE, as weak as omitting it — the default should treat unexpected input as invalid, not
as a happy-path fallback.

---

## How these fit the security review

These three are the highest-signal PHP code-quality defects with a direct security
dimension, which is why they belong alongside the three-layer model rather than in a
general style guide. Add them to the Code-Quality block of the skill's Security Checklist:

- [ ] No `phpinfo()` / `var_dump()` / `print_r()` reachable in production
- [ ] No empty `catch` blocks on security-relevant operations (fail closed, log the cause)
- [ ] Every `switch` over user-controlled or access-control input has a fail-closed `default`

For purely stylistic PHP rules (uppercase control keywords, PHP4 constructor naming,
`goto`), see the EspoCRM skill's quality reference — those are changeability/robustness
concerns without a direct attack surface.
