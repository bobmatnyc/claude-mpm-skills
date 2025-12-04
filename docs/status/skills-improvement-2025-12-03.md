# Claude MPM Skills – Improvement & Gap Report

Date: 2025-12-03  
Author: Codex (external review)

## Scope
- Reviewed repository structure (STRUCTURE.md), manifest.json, and representative skills (web-performance-optimization, express-local-dev).
- Consulted status docs (docs/IMPLEMENTATION_STATUS.md, docs/DOCUMENTATION_STATUS.md, docs/research/skills-documentation-analysis-2025-12-02.md) and user-facing docs (docs/USER_GUIDE.md).

## High-Priority Findings
1) Manifest accuracy and freshness  
   - manifest.json still points to flattened filenames (e.g., `web-performance-optimization.md`, `express-local-dev.md`) that do not match current paths (e.g., `universal/web/web-performance-optimization/SKILL.md`, `toolchains/javascript/frameworks/express-local-dev/SKILL.md`).  
   - `updated` timestamps remain 2025-11-21 while several skills (e.g., web-performance-optimization updated 2025-12-02) have moved ahead.  
   - Impact: auto-discovery/selection can fail or load stale content; token estimates also outdated.  
   - Action: regenerate manifest from filesystem (crawl for SKILL.md + metadata.json) and refresh entry/full token counts and updated dates.

2) API design patterns skill missing  
   - docs/IMPLEMENTATION_STATUS.md flags a missing `universal/web/api-design-patterns` skill covering REST, GraphQL, gRPC, versioning, pagination, and rate limiting. Directory is absent (only api-documentation exists).  
   - Action: create the skill with progressive disclosure, cross-link to api-documentation, and add to manifest.

3) Express skill depth gap  
   - express-local-dev (toolchains/javascript/frameworks/express-local-dev/SKILL.md) remains a local-dev/PM2 primer. Implementation status calls for Flask-level depth: advanced middleware composition, structured error handling, security hardening, comprehensive testing (supertest), and production ops patterns.  
   - Action: expand skill sections and references to match Flask skill depth and update metadata.

## Medium-Priority Findings
4) Voice consistency and example format enforcement  
   - Implementation status calls for a script to detect second-person voice drift and to enforce the ✅/❌ example pattern. No script exists under scripts/ and no automated check is referenced.  
   - Action: add a linting script (e.g., scripts/check_voice_consistency.py) and wire it into CI or PR checklist; document the ✅/❌ standard in the skill creator guide.

5) Testing anti-patterns coverage across languages  
   - Current testing-anti-patterns content is TypeScript/Jest-centric. The plan notes adding Python/pytest coverage or language tabs. No Python-specific variant found.  
   - Action: either add a pytest section with idiomatic examples or create `testing-anti-patterns-python` and reference it from manifest and docs.

6) Decision trees and troubleshooting depth  
   - Status doc lists missing decision trees (TypeScript core, database migration) and troubleshooting sections for complex skills. Many skills still lack these navigational aids.  
   - Action: add concise “Choose X vs Y” trees and “Common failures + fixes” sections to the named skills, then mark completion in IMPLEMENTATION_STATUS.

7) Documentation alignment and freshness  
   - docs/research/skills-documentation-analysis-2025-12-02.md still labels user-facing documentation as largely missing; a substantial docs/USER_GUIDE.md now exists with troubleshooting. Status docs have not been updated to reflect this progress.  
   - Action: reconcile research/status docs with current state, enumerate remaining user-doc gaps (if any), and date-stamp progress to avoid stale guidance.

## Recommended Next Steps (suggested order)
1) Regenerate manifest.json from current filesystem, then spot-check a sample skill load in Claude Code to verify paths and token counts.  
2) Author `universal/web/api-design-patterns` skill and add to manifest.  
3) Deepen express-local-dev skill (middleware, error/security patterns, supertest suite, PM2/containers in prod).  
4) Add voice/example linting script and hook into CI or contributor checklist.  
5) Add Python-focused testing anti-patterns (new skill or language tabs).  
6) Insert decision trees and troubleshooting sections into TypeScript core and database migration skills; update IMPLEMENTATION_STATUS accordingly.  
7) Refresh status/research docs to reflect completed user-facing docs and new progress metrics.
