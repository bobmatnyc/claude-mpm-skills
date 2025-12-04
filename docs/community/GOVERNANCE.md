# Claude MPM Skills - Governance Model

## Repository Purpose

This repository contains reusable Claude Code skills for the Claude Multi-Agent Project Manager ecosystem.

## Branch Protection

**Main Branch Protection Rules:**
- ✅ Require pull request reviews before merging
- ✅ Require review from Code Owners (@bobmatnyc)
- ✅ Require status checks to pass (skill validation CI)
- ✅ Require branches to be up to date before merging
- ❌ Do not allow force pushes
- ❌ Do not allow deletions

## Merge Authority

**Only the following can merge to main:**
- @bobmatnyc (Repository Owner)
- Approved maintainers (designated by owner)

## Contribution Process

1. **Fork** the repository
2. **Create feature branch** from main
3. **Add/modify skills** following CONTRIBUTING.md
4. **Submit PR** with clear description
5. **Wait for review** from @bobmatnyc or maintainer
6. **Address feedback** if requested
7. **Merge approval** required before merge

## Skill Review Criteria

All skills must pass:
- ✅ **Format validation** (SKILL.md structure)
- ✅ **Metadata completeness** (metadata.json present)
- ✅ **Progressive disclosure** (30-50 token entry point)
- ✅ **Clear documentation** (purpose, usage, examples)
- ✅ **No sensitive data** (API keys, credentials)
- ✅ **Testing** (skill works as described)

## Code of Conduct

We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).

## Questions?

Open an issue or contact @bobmatnyc directly.
