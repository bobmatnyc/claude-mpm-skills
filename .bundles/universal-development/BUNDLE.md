# Universal Development

**Version:** 1.0.0
**Category:** Universal
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Language-agnostic development methodologies and best practices applicable to any programming project. Essential practices for quality, debugging, and professional development workflows across all technology stacks.

## Included Skills

- **test-driven-development** (universal/testing/test-driven-development) - TDD methodology
- **systematic-debugging** (universal/debugging/systematic-debugging) - Root cause analysis
- **verification-before-completion** (universal/debugging/verification-before-completion) - Quality gates
- **software-patterns** (universal/architecture/software-patterns) - Design patterns and anti-patterns
- **git-workflow** (universal/collaboration/git-workflow) - Branch strategies and conventions
- **writing-plans** (universal/collaboration/writing-plans) - Technical planning documents

## Use Cases

**When to Deploy This Bundle:**
- Starting any new software project (language-independent)
- Onboarding junior developers to best practices
- Establishing team development standards
- Projects requiring formal planning and documentation
- Teams struggling with technical debt or bugs

**What You Get:**
- Test-driven development red-green-refactor cycles
- Systematic debugging methodologies
- Pre-deployment verification checklists
- Common design patterns (Factory, Strategy, Observer, etc.)
- Git branching strategies (GitFlow, trunk-based)
- Technical planning templates

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| test-driven-development | ✅ Yes | 🚀 Enhanced | None (methodology) |
| systematic-debugging | ✅ Yes | 🚀 Enhanced | None (methodology) |
| verification-before-completion | ✅ Yes | 🚀 Enhanced | None (methodology) |
| software-patterns | ✅ Yes | 🚀 Enhanced | None (architecture) |
| git-workflow | ✅ Yes | 🚀 Enhanced | None (process) |
| writing-plans | ✅ Yes | 🚀 Enhanced | None (documentation) |

**Bundle Synergies:**
- TDD + systematic-debugging: Test failures guide debugging
- software-patterns + TDD: Design patterns emerge from refactoring
- git-workflow + writing-plans: Branch-per-plan workflow
- verification-before-completion + TDD: Quality gates before merge

## Integration Example

```bash
# TDD + Git Workflow
git checkout -b feature/user-authentication

# Red: Write failing test
pytest tests/test_auth.py::test_login  # FAIL

# Green: Implement minimal code
# Edit src/auth.py
pytest tests/test_auth.py::test_login  # PASS

# Refactor: Apply software patterns
# Extract Strategy pattern for auth providers
pytest tests/test_auth.py  # All PASS

# Verification before completion
./scripts/verify.sh  # Run all checks

# Commit and push
git add .
git commit -m "feat: add user authentication"
git push origin feature/user-authentication
```

## Workflow Integration

1. **Planning Phase**: Use `writing-plans` to document architecture
2. **Development Phase**: Apply `test-driven-development` for implementation
3. **Debugging Phase**: Use `systematic-debugging` for root cause analysis
4. **Review Phase**: Apply `software-patterns` to identify improvements
5. **Pre-Merge**: Use `verification-before-completion` checklist
6. **Collaboration**: Follow `git-workflow` for branching strategy

## Version History

- **1.0.0** (2025-11-30): Initial release with 6 universal development skills
