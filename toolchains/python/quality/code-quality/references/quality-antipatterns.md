# Python Code-Quality Anti-Patterns

High-value Python code-quality anti-patterns to check during review or self-review.
These are correctness- and readability-focused patterns. Several of them (broad
`except`, malformed exception classes, identity-vs-equality bugs) directly cause flaky
or silently-passing tests, so clean code here pays off in testability too.

> **Source note:** These anti-patterns are derived from CAST Highlight's Python code
> quality indicators (https://doc.casthighlight.com/), which in turn reference primary
> standards — chiefly **PEP 8** and the Python data model. Where a rule mirrors PEP 8,
> the PEP is the authoritative source. Examples below are original, written to
> illustrate the underlying principle rather than reproduce CAST's prose.

---

## 1. Custom exceptions must derive from the exception hierarchy

**Why:** Python requires exception classes to inherit (transitively) from
`BaseException`. A class meant to represent an error that does not inherit from
`Exception` cannot be raised or caught as an exception — it fails at runtime and breaks
any `except` clause expecting it. User-defined exceptions should inherit from
`Exception` (never directly from `BaseException`, which also catches `SystemExit` and
`KeyboardInterrupt`).

**Non-compliant:**
```python
class PaymentError(object):          # not an exception at all
    def __init__(self, code, message):
        self.code = code
        self.message = message

raise PaymentError(402, "declined")  # TypeError: exceptions must derive from BaseException
```

**Compliant:**
```python
class PaymentError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
```

**Convention used by static checkers:** a class whose name ends in `Error` or
`Exception` is treated as an exception class and expected to derive from `Exception`.

**How to test:**
```python
def test_payment_error_is_raisable_and_catchable():
    with pytest.raises(PaymentError) as exc_info:
        raise PaymentError(402, "declined")
    assert exc_info.value.code == 402
```

---

## 2. Compare singletons with `is`, not `==` (PEP 8)

**Why:** PEP 8 specifies that comparisons to the singletons `None`, `True`, and `False`
use `is`/`is not`, not `==`/`!=`. Identity comparison is faster, unambiguous, and
immune to objects that override `__eq__` in surprising ways. Conversely, `is` should be
used **only** for singletons — using `is` to compare values (strings, ints) is a bug
waiting to happen because it tests object identity, not equality, and small-int/string
interning makes it appear to work until it doesn't.

**Non-compliant:**
```python
if result == None:        # use `is None`
    ...
if active == True:        # use `if active:`
    ...
if name is "admin":       # BUG: identity check on a str value
    ...
```

**Compliant:**
```python
if result is None:
    ...
if active:                # or `if active is True:` for a strict bool check
    ...
if name == "admin":       # value comparison uses ==
    ...
```

**How to test:** Identity bugs are best caught by a linter (e.g., `ruff`/`pylint`
flag `== None` and `is "literal"`). Add a lint step to CI; for behavioral coverage,
assert that the function treats a non-interned equal value correctly:
```python
def test_matches_equal_but_non_identical_string():
    assert is_admin("".join(["ad", "min"])) is True   # would fail if code used `is`
```

---

## 3. Avoid overly broad / bare `except`

**Why:** A bare `except:` (or `except BaseException:`) swallows *everything* — including
`KeyboardInterrupt` and `SystemExit` — making the program hard to interrupt and hiding
real bugs. Catch the narrowest exception type that you can actually handle. A generic
`except Exception:` is tolerable only as a last resort after specific handlers, and only
when it logs or re-raises meaningfully.

**Non-compliant:**
```python
def divide(a, b):
    try:
        return a / b
    except:              # bare: hides ZeroDivisionError, TypeError, and Ctrl-C
        return None
```

**Compliant:**
```python
def divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        log.warning("division by zero")
        return None
    except TypeError:
        log.exception("non-numeric operand")
        raise
```

**Rule of thumb (from static-analysis convention):** specific handlers first; a generic
`except Exception` only in last position, never a bare `except`.

**How to test:**
```python
def test_divide_by_zero_returns_none():
    assert divide(1, 0) is None

def test_divide_propagates_type_error():
    with pytest.raises(TypeError):
        divide("x", 2)        # ensures the broad-catch didn't swallow it
```

---

## 4. Wildcard imports (`from module import *`) should be avoided

**Why:** Wildcard imports pull every public name from a module into the local namespace.
This (a) makes it impossible to see what the file actually depends on, (b) risks silent
name collisions where one module's symbol shadows another's, and (c) defeats static
analysis and IDE navigation. Import only the specific names you use.

**Non-compliant:**
```python
from os import *
from mypackage.helpers import *   # what did this bring in? what shadows what?

path = join(root, name)           # where did join come from?
```

**Compliant:**
```python
from os.path import join
from mypackage.helpers import normalize, slugify

path = join(root, name)
```

**Exception:** A package's own `__init__.py` re-exporting a curated public API via
`from .submodule import *` guarded by an explicit `__all__` is an accepted pattern —
but prefer explicit re-exports even there.

**How to test:** This is a static/lint concern (`ruff` F403/F405, `flake8`). Gate it in
CI rather than in unit tests:
```bash
ruff check --select F403,F405 src/
```

---

## 5. Magic numbers — name your constants

**Why:** Unexplained numeric literals embedded in logic force readers to reverse-engineer
intent and make changes error-prone (the same value may appear in several places).
Promote them to named, documented constants.

**Non-compliant:**
```python
if retries > 5:                      # why 5?
    raise RetryExhausted
time.sleep(attempt * 0.2)            # what is 0.2?
```

**Compliant:**
```python
MAX_RETRIES = 5                      # caps backoff at ~6s total; see ops runbook
BASE_BACKOFF_SECONDS = 0.2

if retries > MAX_RETRIES:
    raise RetryExhausted
time.sleep(attempt * BASE_BACKOFF_SECONDS)
```

**Not magic:** `0`, `1`, and `-1` in their conventional roles (indexing, increments,
sentinels) are fine. Flag values whose meaning is non-obvious.

**How to test:** Assert behavior at the boundary the constant defines, so the constant's
value is pinned by a test:
```python
def test_retry_exhausted_at_limit():
    with pytest.raises(RetryExhausted):
        attempt_operation(retries=MAX_RETRIES + 1)
```

---

## 6. Remove unused local variables

**Why:** A local that is assigned but never read usually signals an unfinished change or
a stale refactor — the dead assignment misleads readers and occasionally hides a bug
(the value was supposed to be used). Delete it, or use `_` for intentionally discarded
unpacking targets.

**Non-compliant:**
```python
def summarize(rows):
    total = sum(r.amount for r in rows)   # computed but never used
    count = len(rows)
    return count
```

**Compliant:**
```python
def summarize(rows: list[Row]) -> int:
    return len(rows)
```

**How to test:** Static concern — `ruff`/`pyflakes` (F841) detects unused locals. Keep
it in CI lint rather than unit tests.

---

## Where this fits

These are review/self-review checks. Most are enforced cheaply by `ruff`/`pylint`/`mypy`
in CI; the exception-hierarchy and broad-`except` items also have direct behavioral
tests (shown above) because they change runtime behavior. For the project-wide
severity-tagged review checklist that incorporates equivalents of these, see the
`code-review-standards` skill. For testing mechanics (fixtures, parametrization,
mocking), see the `pytest` skill.
