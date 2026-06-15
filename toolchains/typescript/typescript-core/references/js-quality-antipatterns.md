# JavaScript / TypeScript Quality Anti-Patterns

## Overview

TypeScript's type system catches *type* errors, but a large class of JavaScript defects
are **runtime/AST-level** issues the compiler does not flag: scope leaks, mutation of
builtins, loose equality, dynamic code execution, and readability traps. These survive
into emitted JS and into plain-JS portions of a codebase. This reference collects the
high-signal ones with compliant/non-compliant examples, severities, and false-positive
filters.

> **Source note:** These anti-patterns are derived from CAST Highlight's JavaScript code
> quality indicators (https://doc.casthighlight.com/), paraphrased with original examples.
> Where CAST defers to open standards, the primary source is cited: SonarSource RSPEC
> (https://rules.sonarsource.com/) and the ESLint core rules
> (https://eslint.org/docs/latest/rules/). Severities are guidance for review triage, not
> CAST's proprietary calibration.

Severity legend: **HIGH** = correctness/security risk; **MEDIUM** = reliability/maintenance
risk; **LOW** = consistency/readability. Apply the 80% confidence filter — flag only when
the pattern is clearly the defect, not a deliberate, commented exception.

---

## 1. Loose equality / implied typecasting (`==` vs `===`)

**Severity: HIGH** (Resiliency / Security)

`==` and `!=` coerce operands before comparing, producing surprising truthiness
(`0 == ""`, `null == undefined`, `"\t\n" == 0`) that leads to data-handling bugs and, on
auth/authorization paths, security flaws. Use strict `===` / `!==`.

**Non-compliant:**
```javascript
if (userInput == 0) grantAccess();      // "" , "0x0", false, [] all coerce to 0
if (role != null) { /* also true for undefined — sometimes unintended */ }
```

**Compliant:**
```javascript
if (userInput === 0) grantAccess();
if (role !== null && role !== undefined) { /* explicit */ }
// or, when "null or undefined" is genuinely intended, document it:
if (role == null) { /* intentional: null OR undefined */ }  // commented exception
```

**False-positive filter:** `x == null` is an idiomatic, widely-accepted shorthand for
"null or undefined." Flag the *other* loose comparisons; accept `== null` when commented
or clearly intentional. Mirrors ESLint `eqeqeq` (with `"smart"` allowing `== null`) and
SonarSource RSPEC.

---

## 2. Dynamic code execution (`eval`, `new Function`, string `setTimeout`)

**Severity: HIGH** (Security)

`eval()` (and `new Function(str)`, `setTimeout("code", …)`) executes arbitrary strings as
code. If any part of the string is influenced by input, it is an injection vector; even
when "safe," it defeats the optimizer and is almost never necessary — arithmetic and
property access have direct syntax.

**Non-compliant:**
```javascript
const result = eval(`${a} + ${b}`);        // injectable, slow, unnecessary
const fn = new Function("return " + expr);  // same family
```

**Compliant:**
```javascript
const result = a + b;
const value = obj[dynamicKey];              // dynamic property access, no eval
```

**False-positive filter:** Genuine, sandboxed interpreters (a math-expression evaluator
library, a controlled plugin host) are out of scope — but should never use raw `eval`.
Mirrors ESLint `no-eval` / `no-implied-eval`.

---

## 3. Modifying builtin objects (`Object`/`Array`/`Function.prototype`)

**Severity: HIGH** (Reliability)

Mutating `Object.prototype`, `Array.prototype`, or `Function.prototype` breaks
assumptions across the entire runtime — notably it pollutes `for…in` and the
object-as-hash-table pattern, producing bugs that are extremely hard to trace because the
cause is in a different module.

**Non-compliant:**
```javascript
Object.prototype.toMap = function () { /* ... */ };   // pollutes every for…in
Array.prototype.last = function () { return this[this.length - 1]; };
```

**Compliant:**
```javascript
function lastOf(arr) { return arr[arr.length - 1]; }   // free function
class TypedMap extends Map { /* extend, don't mutate builtins */ }
```

**False-positive filter:** Well-known, scoped polyfills that conditionally add a *standard*
method when absent (`if (!Array.prototype.flat) { … }`) are acceptable. Flag mutation that
adds *non-standard* members to builtins. Mirrors ESLint `no-extend-native`.

---

## 4. Variable shadowing

**Severity: MEDIUM** (Changeability / Security)

An inner declaration that reuses an outer name silently hides the outer binding, making it
easy to read or write the wrong variable. It is a frequent source of "why didn't my change
take effect" bugs.

**Non-compliant:**
```javascript
const items = getItems();
list.forEach((items) => {            // shadows outer `items`
  process(items);                    // which `items`? confusing
});
```

**Compliant:**
```javascript
const items = getItems();
list.forEach((item) => {
  process(item);
});
```

**False-positive filter:** Short, conventional callback params in tiny scopes are low-risk;
flag shadowing that spans a non-trivial body or shadows a module-level binding. Mirrors
ESLint `no-shadow`.

---

## 5. Use `let`/`const`, never `var` (and prefer `const`)

**Severity: MEDIUM** (Changeability)

`var` is function-scoped and hoisted, leaking out of blocks and enabling
declare-after-use. `const`/`let` are block-scoped and express mutability intent.

**Non-compliant:**
```javascript
for (var i = 0; i < n; i++) { /* ... */ }
console.log(i);                      // `i` leaks past the loop
```

**Compliant:**
```javascript
for (let i = 0; i < n; i++) { /* ... */ }
const TOTAL = computeTotal();        // const for never-reassigned bindings
```

**False-positive filter:** None worth keeping in modern code — `var` in new TS/JS is
essentially always a finding. Legacy files migrating incrementally are the only context to
defer. Mirrors ESLint `no-var` / `prefer-const`.

---

## 6. Logical OR in `switch` case labels

**Severity: MEDIUM** (Reliability)

`case 1 || 2:` does **not** match 1 or 2 — `1 || 2` evaluates to `1`, so only `1` is
handled and `2` silently falls to `default`. The intent is expressed with stacked case
labels (fall-through).

**Non-compliant:**
```javascript
switch (x) {
  case 1 || 2:          // only matches 1; `2` hits default
    doSomething(x); break;
  default:
    boom();             // fires for x === 2, unexpectedly
}
```

**Compliant:**
```javascript
switch (x) {
  case 1:
  case 2:               // intentional fall-through groups both
    doSomething(x); break;
  default:
    boom();
}
```

**False-positive filter:** None — a logical operator in a case label is always the bug.
Mirrors SonarSource RSPEC-3616.

---

## 7. Repetitive access to deep nested members

**Severity: MEDIUM** (Efficiency / Elegance)

Re-resolving a deep member chain (`window.location.href`, `config.a.b.c.d`,
`document.querySelector(...)`) on every use forces the engine to walk the resolution path
— and for DOM access this is genuinely expensive. Cache the resolved value in a local when
read more than once in a scope.

**Non-compliant:**
```javascript
if (config.services.auth.tokens.refresh.enabled) {
  schedule(config.services.auth.tokens.refresh.ttl);   // path walked twice
}
```

**Compliant:**
```javascript
const refresh = config.services.auth.tokens.refresh;
if (refresh.enabled) {
  schedule(refresh.ttl);
}
```

**False-positive filter:** A path read once, or reads separated by a mutation that could
change the value, are not violations. Flag the same path read 2+ times with no intervening
write. (See also `code-review-standards` Efficiency criterion 3 — greedy data access.)

---

## 8. Non-wrapped immediately-invoked function expressions (IIFE)

**Severity: LOW** (Changeability)

Wrap an immediately-invoked function in parentheses so the reader sees the value is the
*result* of the call, not the function itself, and to avoid parser ambiguity.

**Non-compliant:**
```javascript
const config = function () { return load(); }();    // ambiguous to readers/parsers
```

**Compliant:**
```javascript
const config = (function () { return load(); })();
// modern: just use an arrow or a named function — IIFEs are rarely needed with modules
const config = (() => load())();
```

**False-positive filter:** With ES modules, IIFEs are largely obsolete; prefer module
scope. Flag the un-wrapped form when an IIFE is genuinely used. Mirrors ESLint
`wrap-iife`.

---

## 9. Multiline string literals via backslash line-continuation

**Severity: LOW** (Reliability)

A `\` at end of line to continue a string is not part of ECMAScript proper, and trailing
whitespace after the `\` causes tricky, invisible errors. Use template literals or string
concatenation.

**Non-compliant:**
```javascript
const msg = 'a long message \
that continues';                     // whitespace after `\` breaks silently
```

**Compliant:**
```javascript
const msg = `a long message
that continues`;                     // template literal
const msg2 = 'a long message ' +
  'that continues';                  // explicit concatenation
```

**False-positive filter:** None — prefer template literals. Mirrors SonarSource RSPEC-3616.

---

## 10. Array literals over `new Array()`

**Severity: LOW** (Reliability)

`new Array(3)` does **not** create `[3]` — it creates an array of *length* 3 with no
elements, a well-known trap. The literal syntax is shorter and unambiguous.

**Non-compliant:**
```javascript
const a = new Array(1, 2, 3);        // works, but verbose
const b = new Array(3);              // length 3, no elements — surprising
```

**Compliant:**
```javascript
const a = [1, 2, 3];
const b = Array.from({ length: 3 }, () => 0);   // explicit when you want fixed length
```

**False-positive filter:** `Array.from` / `Array.of` for intentional length/iterable
construction are fine. Flag `new Array(...)`. Mirrors ESLint `no-array-constructor`.

---

## 11. Using functions before their declaration

**Severity: LOW** (Changeability)

Hoisting lets you call a `function` declaration before it appears, but readers scan
top-to-bottom; calling before declaring forces them to scroll to understand. Declare
before use (and with `const`-bound arrow functions, hoisting won't save you anyway).

**Non-compliant:**
```javascript
render();                            // works via hoisting, but reads backwards
function render() { /* ... */ }
```

**Compliant:**
```javascript
function render() { /* ... */ }
render();
```

**False-positive filter:** Mutually-recursive functions and intentional
declaration-at-bottom modules are acceptable when consistent. Mirrors ESLint
`no-use-before-define`.

---

## How these map to scoring

In the `code-quality-scoring` skill's Software Health model: items 1–3, 6, 9, 10 feed
**Resiliency**; items 4, 5, 8, 11 feed **Agility**; item 7 feeds **Elegance**. Counting
these at scale gives a per-dimension signal, not just a fix list.

## References

- CAST Highlight JavaScript code quality indicators — https://doc.casthighlight.com/
- ESLint core rules — https://eslint.org/docs/latest/rules/
- SonarSource RSPEC (TypeScript/JavaScript) — https://rules.sonarsource.com/
