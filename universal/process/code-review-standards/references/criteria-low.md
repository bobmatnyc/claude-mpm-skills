# LOW Criteria — Detailed Explanations

## Overview

LOW findings are noted in the critic report but do not affect the verdict.
An APPROVE with LOW findings is still APPROVE. LOW findings are passed to the
Documentation agent for future reference. Engineers may address them at their
discretion without a re-critic pass.

LOW criteria represent style and cleanliness issues that automated formatters
handle, or issues so minor that the risk of flagging them as anything higher
would create noise that dilutes the signal from genuine problems.

---

## 1. PEP 8 compliance (black + isort handles this automatically)

**What this covers:**
Line length (88 chars for black), whitespace around operators, blank lines between
functions and classes, trailing whitespace.

**Why it's LOW:**
`black` and `isort` are typically run as pre-commit hooks or CI steps. If the
implementation went through the CI pipeline, PEP 8 compliance is automated.
Flagging it manually wastes finding table space.

**When to flag:**
Only flag if PEP 8 issues are so severe they impair readability and the project
clearly does not use an autoformatter. Even then, flag as LOW — the fix is running
`black .` and `isort .`, not a code logic change.

---

## 2. Variable naming is clear and descriptive

**What to check:**
Single-letter variable names outside of:
- Loop indices (`i`, `j`, `k` in short for loops are acceptable)
- Coordinates (`x`, `y`, `z` in geometric code are acceptable)
- Mathematical notation (`n`, `m` in algorithms following a standard formula)

**Violations:**
```python
def process(d: dict, l: list[str]) -> None:  # d, l are unclear
    for i in l:
        d[i] = True
```

**Low-impact:** naming issues rarely cause bugs. Flag as LOW unless the name is
actively misleading (e.g., `result = get_user()` then using `result` as a list of
orders without reassignment — that's a MEDIUM readability issue at most).

---

## 3. No commented-out code left in

**What to check:**
Blocks of code commented out with `#`:
```python
# old_result = fetch_legacy(url)
result = fetch_new(url)
```

**Why it's LOW:**
Commented-out code adds noise and creates confusion about whether the old code
should be restored. Git history preserves deleted code — comments are unnecessary.

**Exception:** Comments that explain why code was removed ("# removed: was causing
OOM on large inputs, see issue #123") are informative and acceptable.

---

## 4. Import ordering is clean

**What to check:**
Standard library imports, third-party imports, and local imports should be in
separate groups, in that order, each group alphabetically sorted.

`isort` handles this automatically. Flag as LOW if isort has clearly not been run.

**Standard order:**
```python
# 1. Standard library
import asyncio
import os
from typing import Any

# 2. Third-party
import httpx
from pydantic import BaseModel

# 3. Local
from myapp.models import User
from myapp.utils import parse
```

---

## When Not to Flag LOW Issues

If the implementation has CRITICAL or HIGH findings, do not fill the finding table
with LOW issues — it buries the important signal. In a BLOCK verdict, limit the
finding table to CRITICAL items only. In a WARN verdict, list HIGH items and
optionally note LOW/MEDIUM in the summary paragraph rather than the table.

LOW issues consume finding table space that should be reserved for actionable findings.
A critic report with 10 LOW findings and 0 HIGH findings looks comprehensive but
is not useful — it suggests the critic spent time on noise rather than substance.

---

## TODO: Expand with language-specific style guides

<!-- TODO: Add TypeScript/ESLint equivalents for each LOW criterion -->
<!-- TODO: Add Go gofmt/goimports equivalents -->
<!-- TODO: Add guidance on when to escalate naming issues to MEDIUM (actively misleading names) -->
<!-- TODO: Add examples of acceptable commented-out code (with issue references) -->
