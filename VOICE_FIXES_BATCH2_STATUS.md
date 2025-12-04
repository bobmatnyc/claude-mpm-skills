# Voice Consistency Fixes - Batch 2 Status

## Summary of Work Completed

### Starting Point
- **Initial status**: 61 second-person voice errors remaining (after batch 1 fixed 69)
- **Target**: Fix all remaining 61 second-person voice violations

### Current Status (After Batch 2)
- **Errors fixed**: 36 violations resolved
- **Remaining errors**: 25 second-person voice violations
- **Progress**: 59% reduction in this batch
- **Overall progress**: 130 → 61 → 25 errors (81% total reduction)

## Files Fixed in Batch 2 (Commit: a606256)

### .claude/skills/ and Synced Duplicates

1. ✅ **toolchains-javascript-build-vite** (1 error)
   - Line 14: "When you need X" → "When needing X"

2. ✅ **toolchains-javascript-testing-playwright** (2 errors)
   - Lines 14-16: "When you need X" → "When needing X"

3. ✅ **toolchains-platforms-database-neon** (2 errors)
   - Lines 13-15: "When you need/want X" → "When needing/implementing X"

4. ✅ **toolchains-platforms-deployment-netlify** (2 errors)
   - Lines 15-16: "When you need/want X" → "When needing/requiring X"

5. ✅ **toolchains-platforms-deployment-vercel** (2 errors)
   - Lines 14-15: "When you need/want X" → "When needing/requiring X"

6. ✅ **toolchains-python-data-sqlalchemy** (2 errors)
   - Lines 14-16: "When you need X" → "When needing X"

7. ✅ **toolchains-python-frameworks-django** (3 errors)
   - Lines 14-15: "When you need/want X" → "When needing/using X"
   - Line 28: "so you can focus" → "enabling focus"

8. ✅ **toolchains-python-tooling-pyright** (2 errors)
   - Lines 13-15: "When you need/want X" → "When needing/requiring X"

9. ✅ **toolchains-typescript-frameworks-nodejs-backend** (1 error)
   - Line 15: "When you need X" → "When needing X"

10. ✅ **universal-collaboration-brainstorming** (2 errors - non-imperative mood)
    - Line 57: "should go" → direct imperative "Go"
    - Line 63: "would give" → "gives"

### Transformation Patterns Applied

```diff
# Pattern 1: when_to_use fields
- "When you need X"
+ "When needing X"

- "When you want X"
+ "When requiring X" or "When using X"

# Pattern 2: Non-imperative mood
- "You can and should go backward when:"
+ "Go backward when:"

- "when going backward would give better results"
+ "when going backward gives better results"

# Pattern 3: Prose descriptions
- "so you can focus on writing your app"
+ "enabling focus on writing applications"
```

## Remaining Work (25 errors across 15 files)

### Files Needing Fixes

**Unique files (accounting for duplicates)**:

1. **universal-debugging-systematic-debugging** (3 errors)
   - Line 8: "you must"
   - Additional errors to locate

2. **toolchains-platforms-backend-supabase** (2 errors)
   - Lines to be identified

3. **universal-collaboration-dispatching-parallel-agents** (2 errors)
   - Lines to be identified

4. **universal-main-mcp-builder** (2 errors)
   - Lines to be identified

5. **universal-debugging-verification-before-completion** (1 error)
   - Line to be identified

6. **universal-infrastructure-env-manager** (1 error)
   - Line to be identified

7. **universal-main-skill-creator** (1 error)
   - Line to be identified

8. **toolchains-ai-frameworks-dspy** (1 error - in toolchains/ only, no .claude/skills duplicate)
   - Line to be identified

Note: Several files exist in both `.claude/skills/` and `toolchains/`/`universal/` directories and need syncing.

## Verification Commands

```bash
# Check current error count
python3 scripts/check_voice_consistency.py --format text | grep "Errors:"

# List files with second-person voice errors
python3 scripts/check_voice_consistency.py --format json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for file in data['files']:
    violations = [v for v in file.get('violations', []) if v['type'] == 'second_person_voice']
    if violations:
        print(f\"{len(violations)} errors: {file['path'].split('claude-mpm-skills/')[-1]}\")
"

# Get specific file violations
python3 scripts/check_voice_consistency.py --format text 2>&1 | grep -A 10 "FILENAME"
```

## Next Steps

1. **Fix remaining 25 second-person voice violations**
   - Focus on the 8 unique files (plus their duplicates)
   - Use same transformation patterns as batch 2

2. **Sync all changes to duplicate locations**
   - `.claude/skills/` → `toolchains/` and `universal/`

3. **Final verification**
   - Target: 0 second-person voice errors
   - Run: `python3 scripts/check_voice_consistency.py`

4. **Commit batch 3**
   - Group by category (universal/toolchains)
   - Include before/after stats

## Git Status

```bash
# Current commit
git log --oneline -1
# a606256 fix: resolve 36 second-person voice violations in skill documentation

# Files changed in this batch
git diff --stat HEAD~1
# 11 files changed, 124 insertions(+), 19 deletions(-)

# Modified files (includes duplicates)
git diff --name-only HEAD~1
```

## Notes

- All changes maintain technical accuracy
- Imperative voice improves clarity and directness
- Changes synced between `.claude/skills/` (gitignored) and tracked directories
- Preserves meaning while eliminating second-person constructions
