---
name: pr-quality-checklist
description: PR quality checklist for ensuring comprehensive, well-documented pull requests. Use before submitting PRs to improve review efficiency and code quality.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_checklist
  sections:
    - pr_title_format
    - pr_description_template
    - size_guidelines
    - refactoring_prs
    - review_checklist
    - common_mistakes
---

# PR Quality Checklist Skill

## Summary
Comprehensive guide for creating high-quality pull requests that are easy to review, well-documented, and follow team standards. Includes templates, size guidelines, and best practices for both authors and reviewers.

## When to Use
- Before creating any pull request
- When reviewing others' PRs
- To establish team PR standards
- During onboarding of new team members
- When PR reviews are taking too long

## Quick Checklist

### Before Creating PR
- [ ] PR title follows convention: `type(scope): description`
- [ ] Description includes summary, related tickets, and test plan
- [ ] Changes are focused and related (single concern)
- [ ] Code is self-reviewed for obvious issues
- [ ] Tests added/updated and passing
- [ ] No debugging code (console.log, debugger, etc.)
- [ ] TypeScript/type errors resolved
- [ ] Documentation updated if needed
- [ ] Screenshots included for UI changes
- [ ] Changeset added (for user-facing changes)

---

## PR Title Format

### Convention
```
{type}({scope}): {short description}
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **docs**: Documentation only
- **style**: Formatting, missing semicolons, etc. (no code change)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates
- **perf**: Performance improvement
- **ci**: CI/CD changes

### Examples
```
feat(auth): add OAuth2 login support
fix(cart): resolve race condition in checkout
refactor(search): extract query param parsing logic
docs(api): update authentication examples
test(payment): add integration tests for Stripe
chore(deps): update Next.js to v15
perf(images): implement lazy loading for gallery
ci(deploy): add staging environment workflow
```

### Scope Guidelines
- Use component/module name: `auth`, `cart`, `search`, `api`
- Be specific but not too granular: `user-profile` not `user-profile-settings-modal`
- Consistent with codebase structure

---

## PR Description Template

### Standard Template
```markdown
## Summary
<!-- 1-3 bullet points describing what changed -->
- Added OAuth2 authentication flow
- Integrated with Auth0 provider
- Updated login UI components

## Related Tickets
<!-- Link to Linear/Jira/GitHub issues -->
- Closes #123
- Related to #456
- Fixes ENG-789

## Changes
<!-- Detailed list of changes -->
### Added
- `src/lib/auth/oauth2.ts` - OAuth2 client implementation
- `src/app/api/auth/callback/route.ts` - Auth callback handler
- `src/components/OAuthButtons.tsx` - OAuth login buttons

### Modified
- `src/components/LoginForm.tsx` - Added OAuth buttons
- `src/lib/auth/index.ts` - Export new auth methods
- `README.md` - Updated setup instructions

### Removed
- `src/lib/auth/legacy.ts` - Deprecated auth code
- `src/components/OldLoginForm.tsx` - Replaced by new form

## Screenshots
<!-- Required for UI changes -->
### Desktop
![Desktop view](https://imgur.com/desktop.png)

### Mobile
![Mobile view](https://imgur.com/mobile.png)

### Before/After (if applicable)
| Before | After |
|--------|-------|
| ![Before](before.png) | ![After](after.png) |

## Testing
<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested on Chrome, Firefox, Safari
- [ ] Mobile responsive (tested on iOS/Android)
- [ ] Edge cases tested (empty state, error states, loading)

## Breaking Changes
<!-- If any breaking changes -->
⚠️ **Breaking Change**: The `login()` function signature has changed.

**Before:**
```typescript
login(username: string, password: string)
```

**After:**
```typescript
login({ username: string, password: string, provider?: 'local' | 'oauth' })
```

**Migration:**
```typescript
// Old
await login('user', 'pass');

// New
await login({ username: 'user', password: 'pass' });
```

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] Changeset added (if user-facing change)
- [ ] No console.log/debugger statements left
- [ ] No TypeScript errors
- [ ] Tests pass locally
- [ ] Build succeeds
```

### Minimal Template (for small changes)
```markdown
## Summary
Brief description of the change.

## Changes
- Modified `file.ts` to fix XYZ

## Testing
- [ ] Tests pass
- [ ] Verified manually
```

---

## Size Guidelines

### Ideal PR Size
- **Lines changed**: < 300 (excluding generated files)
- **Files changed**: < 15
- **Review time**: < 30 minutes
- **Commits**: 1-5 logical commits

### Size Categories
| Size | Lines | Files | Review Time | Recommendation |
|------|-------|-------|-------------|----------------|
| **XS** | < 50 | 1-3 | 5 min | ✅ Ideal for hotfixes |
| **S** | 50-150 | 3-8 | 15 min | ✅ Good size |
| **M** | 150-300 | 8-15 | 30 min | ⚠️ Consider splitting |
| **L** | 300-500 | 15-25 | 1 hour | ❌ Should split |
| **XL** | 500+ | 25+ | 2+ hours | ❌ Must split |

### When to Split PRs

#### 1. By Feature Phase
```
PR #1: MVP implementation (core functionality)
PR #2: Polish and edge cases
PR #3: Additional features
```

#### 2. By Layer
```
PR #1: Database schema changes
PR #2: Backend API implementation
PR #3: Frontend UI integration
PR #4: Tests and documentation
```

#### 3. By Concern
```
PR #1: Refactoring (no behavior change)
PR #2: New feature (builds on refactored code)
PR #3: Tests for new feature
```

#### 4. By Risk Level
```
PR #1: High-risk changes (need careful review)
PR #2: Low-risk changes (routine updates)
```

### Exceptions to Size Limits
- Generated code (migrations, API clients, types)
- Renaming/moving files (show with `git mv`)
- Bulk formatting changes (separate PR, pre-approved)
- Third-party library integration (well-documented)

---

## Refactoring PRs

### Refactoring Template
```markdown
## Summary
Refactoring and cleanup for [area]

**Goal**: Improve code maintainability without changing behavior

## Motivation
- Reduce code duplication (3 similar functions → 1 reusable utility)
- Improve type safety (any → specific types)
- Remove dead code identified during feature work

## Related Tickets
- ENG-XXX: Improve [area] maintainability
- ENG-YYY: Remove deprecated [feature]

## Stats
- **Lines added**: +91
- **Lines removed**: -1,330
- **Net**: -1,239 ✅
- **Files changed**: 23

## Changes

### Removed (Dead Code)
- `/api/old-endpoint` - unused, replaced by `/api/new-endpoint` in v2.0
- `useDeprecatedHook.ts` - replaced by `useNewHook.ts` (ENG-234)
- `legacy-utils.ts` - functions no longer called anywhere

### Refactored
- **Extracted common logic**: Query param parsing now in `lib/url-utils.ts`
- **Consolidated validation**: 3 duplicate Zod schemas → 1 shared schema
- **Improved types**: Replaced 12 `any` types with proper interfaces

### No Behavior Changes
- [ ] All tests pass (no test modifications needed)
- [ ] Same inputs → same outputs
- [ ] No user-facing changes

## Testing
- [ ] Full test suite passes (no new tests needed)
- [ ] Manual smoke test completed
- [ ] No regressions identified

## Review Focus
- Verify removed code is truly unused (checked with `rg` search)
- Confirm refactored logic is equivalent
- Check no subtle behavior changes introduced
```

### Refactoring Best Practices
- **Separate refactoring from features**: Never mix
- **Verify zero behavior change**: Tests should not need updates
- **Document removed code**: Explain why safe to remove
- **Search thoroughly**: Use `rg`/`grep` to verify no usage
- **Celebrate negative LOC**: Highlight code reduction

---

## Review Checklist

### For Authors (Self-Review)
Before requesting review, check:

#### Code Quality
- [ ] Code is DRY (no obvious duplication)
- [ ] Functions are single-purpose and focused
- [ ] Variable names are clear and descriptive
- [ ] No magic numbers or hardcoded values
- [ ] Error handling is comprehensive
- [ ] Edge cases are handled

#### Testing
- [ ] Tests cover new functionality
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases are tested
- [ ] Error conditions are tested
- [ ] No flaky tests introduced

#### Documentation
- [ ] Complex logic has comments
- [ ] Public APIs have JSDoc/docstrings
- [ ] README updated (if setup changed)
- [ ] Migration guide (if breaking changes)

#### Performance
- [ ] No obvious performance issues
- [ ] Database queries are efficient (indexes considered)
- [ ] No N+1 queries
- [ ] Large datasets handled appropriately

#### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Authorization checks in place
- [ ] No SQL injection vulnerabilities
- [ ] Sensitive data not logged

---

### For Reviewers

#### First Pass (5 minutes)
- [ ] PR description is clear
- [ ] Changes align with stated goal
- [ ] Size is reasonable (< 300 LOC preferred)
- [ ] No obvious red flags

#### Code Review (15-30 minutes)
- [ ] Logic is correct
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Code is readable and maintainable
- [ ] No performance issues
- [ ] Security considerations addressed

#### Testing Review
- [ ] Tests cover the changes
- [ ] Tests are meaningful
- [ ] No flaky tests
- [ ] Edge cases tested

#### Documentation Review
- [ ] PR description matches changes
- [ ] Comments explain "why" not "what"
- [ ] Breaking changes documented
- [ ] Migration guide provided (if needed)

#### Approval Criteria
```
✅ Approve: Code is good, minor nits only
💬 Comment: Suggestions but not blockers
🔄 Request Changes: Issues must be fixed before merge
```

---

## Common Mistakes

### 1. Vague PR Titles
```
❌ "Fix bug"
❌ "Updates"
❌ "WIP"
❌ "Changes from code review"

✅ "fix(auth): prevent duplicate login requests"
✅ "feat(cart): add coupon code support"
```

### 2. Missing Context
```
❌ "Changed the function"
Why? What was wrong? What's the impact?

✅ "Refactored parseQueryParams to handle nested objects

Previously failed when query params contained dots (e.g., user.name).
Now correctly parses nested structures using qs library.

Fixes ENG-456"
```

### 3. Too Large
```
❌ 2,000 lines changed across 50 files
❌ "Implement entire authentication system"

✅ Split into:
  - PR #1: Add database schema for auth (150 LOC)
  - PR #2: Implement JWT utilities (100 LOC)
  - PR #3: Create login endpoint (200 LOC)
  - PR #4: Add login UI (250 LOC)
```

### 4. Mixed Concerns
```
❌ Single PR with:
  - Feature implementation
  - Dependency updates
  - Refactoring
  - Bug fixes
  - Formatting changes

✅ Separate PRs:
  - PR #1: feat(feature)
  - PR #2: chore(deps)
  - PR #3: refactor(component)
```

### 5. No Screenshots for UI Changes
```
❌ "Updated the header design"
(No screenshots)

✅ "Updated the header design"
[Desktop screenshot]
[Mobile screenshot]
[Before/After comparison]
```

### 6. Incomplete Testing Notes
```
❌ "Tested locally"
How? What scenarios? What browsers?

✅ "Testing completed:
- Unit tests: All 47 tests pass
- Manual testing: Tested login flow on Chrome, Firefox, Safari
- Edge cases: Tested expired tokens, invalid credentials, network errors
- Mobile: Verified on iOS Safari and Android Chrome"
```

### 7. Leaving Debug Code
```
❌ console.log('user data:', user);
❌ debugger;
❌ // TODO: fix this later
❌ import { test } from './test-utils'; (unused)

✅ Clean code without debugging artifacts
```

### 8. No Changeset (for User-Facing Changes)
```
❌ New feature shipped without changelog entry

✅ .changeset/new-feature.md:
---
"@myapp/web": minor
---

Add OAuth2 login support with Auth0 integration
```

---

## Summary

### Quick Reference

#### PR Title Formula
```
{type}({scope}): {clear, concise description}
```

#### Ideal PR Characteristics
- **Size**: < 300 LOC, < 15 files
- **Focus**: Single concern, related changes only
- **Documentation**: Clear description, test plan, screenshots (if UI)
- **Quality**: Self-reviewed, tested, no debugging code
- **Timeline**: Ready to merge, not WIP

#### Review Mindset
**As Author**:
- Make reviewer's job easy
- Provide context and reasoning
- Test thoroughly before requesting review
- Respond promptly to feedback

**As Reviewer**:
- Be constructive and specific
- Focus on correctness and maintainability
- Ask questions when unclear
- Acknowledge good practices

#### Red Flags
- 🚩 No description or "WIP" title
- 🚩 Over 500 LOC changed
- 🚩 Mixed concerns (feature + refactor + deps)
- 🚩 No tests or only changing tests
- 🚩 "Trust me, it works"
- 🚩 Console.log/debugger statements
- 🚩 TypeScript errors ignored
- 🚩 No screenshots for UI changes

Use this skill to maintain high PR quality standards and streamline code review processes.
