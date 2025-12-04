# Voice Consistency Fixes - Progress Report

## Summary
- **Initial errors**: 130 second-person voice violations
- **Current errors**: 61 second-person voice violations
- **Progress**: 69 errors fixed (53% reduction)
- **Remaining**: 61 errors across 17+ files

## Completed Fixes (Committed: 7ea1331)

### Universal Skills Fixed
1. ✅ universal-testing-testing-anti-patterns (3 errors)
2. ✅ universal-debugging-verification-before-completion (3 errors)
3. ✅ universal-debugging-systematic-debugging (2 errors)
4. ✅ universal-debugging-root-cause-tracing (1 error)
5. ✅ universal-collaboration-dispatching-parallel-agents (1 error)
6. ✅ universal-collaboration-git-workflow (1 error)
7. ✅ universal-collaboration-requesting-code-review (1 error)
8. ✅ universal-collaboration-stacked-prs (1 error)
9. ✅ universal-architecture-software-patterns (1 error)
10. ✅ universal-main-mcp-builder (2 errors)
11. ✅ universal-main-skill-creator (1 error)

### Toolchain Skills Fixed
1. ✅ toolchains-ai-frameworks-dspy (1 error)
2. ✅ toolchains-python-frameworks-flask (1 error)
3. ✅ toolchains-typescript-testing-vitest (1 error)
4. ✅ toolchains-typescript-data-prisma (1 error)
5. ✅ toolchains-platforms-backend-supabase (1 error)
6. ✅ toolchains-rust-desktop-applications (1 error)
7. ✅ toolchains-php-frameworks-espocrm (1 error)
8. ✅ toolchains-javascript-frameworks-svelte (1 error in both .claude/skills and toolchains/)

## Remaining Errors by File (61 total)

### .claude/skills/ directory (to fix):
1. toolchains-javascript-build-vite (1 error) - line 14
2. toolchains-javascript-testing-playwright (2 errors) - lines 13-15
3. toolchains-platforms-database-neon (2 errors) - lines 13-15
4. toolchains-platforms-deployment-netlify (2 errors) - lines 13-15
5. toolchains-platforms-deployment-vercel (2 errors) - lines 13-15
6. toolchains-python-data-sqlalchemy (2 errors) - lines 13-15
7. toolchains-python-frameworks-django (3 errors) - lines 8, 14-15
8. toolchains-python-tooling-pyright (2 errors) - lines 13-15
9. toolchains-typescript-frameworks-nodejs-backend (1 error)
10. universal-collaboration-brainstorming (1 error)
11. universal-infrastructure-env-manager (1 error)

### Duplicated locations (toolchains/ and universal/ directories):
The same files exist in both `.claude/skills/` and old `toolchains/`/`universal/` directories.
Fixes need to be synced to both locations.

## Common Patterns Fixed

### "when you" → "when X is needed"
```diff
- when you need flexibility over batteries-included frameworks
+ when flexibility over batteries-included frameworks is needed
```

### "you're" → imperative/active voice
```diff
- If you're accessing Container directly
+ Accessing Container directly violates architecture
```

### "If you catch yourself" → "STOP when"
```diff
- If you catch yourself:
+ STOP when:
```

### "you must" → imperative
```diff
- you must rebase dependent PRs
+ rebase dependent PRs
```

## Next Steps

1. **Fix remaining .claude/skills/ files** (11 files, ~22 errors)
2. **Sync fixes to duplicate locations** (toolchains/ and universal/ directories)
3. **Verify with check script**: `python3 scripts/check_voice_consistency.py`
4. **Target**: 0 second-person voice errors

## Commands for Verification

```bash
# Check current status
python3 scripts/check_voice_consistency.py --format text | head -20

# Find specific file errors
python3 scripts/check_voice_consistency.py --format text 2>&1 | grep -A 3 "toolchains-javascript-build-vite"

# Count remaining errors
python3 scripts/check_voice_consistency.py --format text 2>&1 | grep "Errors:" | head -1
```

## Notes

- Most remaining errors are in metadata `when_to_use` fields (lines 13-16)
- Pattern: description fields with "when you need X" constructions
- The `.claude/skills/` directory is gitignored (by design)
- Files in `toolchains/` and `universal/` are tracked and committed
- Need to maintain consistency between `.claude/skills/` and tracked directories
