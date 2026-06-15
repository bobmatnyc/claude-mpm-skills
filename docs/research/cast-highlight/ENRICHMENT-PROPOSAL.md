# CAST Highlight Knowledgebase — Skill Enrichment Proposal

**Date:** 2026-06-15
**Status:** Awaiting approval — do not edit skill files until green-lit
**CAST KB size:** 335 pages (322 rules + 13 methodology), crawled 2026-06-15

---

## 1. Executive Summary

The CAST Highlight knowledgebase is a well-curated, production-grade catalog of
language-specific and language-agnostic code-quality rules. Its primary value for our
skills is **not** the individual rules themselves (which are already covered by linters
like Pylint, ESLint, Checkstyle, etc.) but:

1. **The quality family taxonomy** (Changeability, Robustness, Efficiency,
   Transferability, Security) maps cleanly onto checklist sections that are currently
   missing or underweighted in our skills.
2. **The _multi (language-agnostic) rules** (105 rules) can enrich universal cross-
   language skills with battle-tested patterns that transcend any single language.
3. **The methodology layer** (Software Health scoring, Technical Debt estimation,
   Open Source Safety) fills a genuine gap: we have no skill that helps developers
   reason about portfolio-level code health or communicate technical debt in business
   terms.
4. **Python quality rules** (44 rules) are the richest single-language trove relative
   to the sophistication of our current Python skills, making Python the highest-ROI
   enrichment target.

**Top 5 highest-leverage opportunities:**

| # | Opportunity | Why High-Leverage |
|---|-------------|-------------------|
| 1 | NEW universal skill: `universal/quality/code-quality-scoring` | Methodology layer is entirely uncovered; 13 pages of scoring frameworks with no analogue in our skills |
| 2 | Enrich `universal/process/code-review-standards` with CAST quality-family framework | Adds Efficiency + Transferability dimensions currently absent from checklist |
| 3 | Enrich `toolchains/python/` skills with 44 Python-specific CAST rules | Highest rule density relative to skill coverage; rules are actionable and PEP-aligned |
| 4 | Enrich `toolchains/java/frameworks/spring-boot` with 88 Java robustness/changeability rules | Java has the largest CAST rule corpus; Spring Boot skill is currently pattern-light on code quality |
| 5 | Enrich `toolchains/universal/dependency/audit` + `universal/security/security-scanning` with CAST Open Source Safety methodology | License-risk profiles and CVE weighting framework adds concrete scoring not currently in either skill |

---

## 2. Prioritized Enrichment Table

> Effort: **S** = 1–2 hours (add a section or reference), **M** = half-day (add
> structured reference doc), **L** = full day+ (new skill or major restructure).
> Priority: **High** = blocks a common use case or fills a critical gap; **Med** =
> useful but not urgent; **Low** = nice-to-have.

| # | Opportunity | Target Skill (or NEW) | Quality Family / Language | What Would Be Added | Example CAST Rule Slugs | Additive vs Overlap | Effort | Priority |
|---|-------------|----------------------|--------------------------|---------------------|------------------------|---------------------|--------|----------|
| 1 | NEW: Code Quality Scoring skill | NEW `universal/quality/code-quality-scoring` | All families + methodology | Full new skill covering Software Health (Resiliency/Agility/Elegance), Agility, Elegance, Cloud Maturity, Tech Debt estimation, Open Source Safety scoring | `software-health`, `software-agility`, `cloud-maturity`, `technical-debt-estimates-stats-technology` | Fully additive — no existing skill covers scoring/metrics | L | **High** |
| 2 | Expand code-review-standards checklist with Efficiency + Transferability dimensions | `universal/process/code-review-standards` | Efficiency (37), Transferability (36) | New MEDIUM/LOW checklist items derived from CAST Efficiency (nested loops, cursor-in-loop, greedy data access) and Transferability (no dead code, naming consistency, switch nesting) families | `alt_nestedforloop`, `alt_largeswitchcase`, `alt_nbfiles`, `alt_deadcode` | Additive — current checklist covers Security/Robustness but lacks Efficiency and Transferability categories | M | **High** |
| 3 | Enrich Python skills with quality anti-patterns reference | `toolchains/python/` (best fit: `testing/pytest` or new `toolchains/python/quality/`) | Changeability + Robustness / python (44 rules) | A `references/quality-antipatterns.md` doc covering: exception hierarchy rules, PEP-8 comparison idioms, magic number avoidance, wildcard import risk, unused-variable detection, backslash line continuation, and risky catches | `alt_illegalexception`, `alt_comparisontosingleton`, `alt_riskycatches`, `alt_magicnumbers`, `alt_unusedvar` | Additive — pytest skill covers testing mechanics; Django/FastAPI skills cover framework patterns; none covers code-quality anti-patterns | M | **High** |
| 4 | Enrich Spring Boot skill with Java robustness + changeability anti-patterns | `toolchains/java/frameworks/spring-boot` | Robustness (subset of 88 Java rules) + Changeability | A `references/quality-antipatterns.md` covering: nested try-catch, generic catch, catches-that-only-rethrow, missing final-else, collapsible-if, loop counter modification, and switch-statement hygiene | `alt_nestedtrycatches`, `alt_genericcatches`, `alt_onlyrethrowingcatches`, `alt_collapsibleif`, `alt_missingfinalelse` | Additive — Spring Boot skill covers framework DI/REST/Data patterns; quality anti-patterns section is absent | M | **High** |
| 5 | Enrich Open Source Safety section in dependency audit and security scanning skills | `toolchains/universal/dependency/audit` + `universal/security/security-scanning` | Security / methodology | Add CAST license-risk tier definitions (HIGH: GPL/AGPL, MEDIUM: EPL/MPL, LOW: MIT/Apache) and OSS Safety score components (CVE weighting, obsolescence scoring, license compliance) as a structured reference | `open-source-safety`, `open-source-license-risk-profiles`, `transitive-dependencies-much-can-trust-friends-friends` | Mostly additive — audit skill mentions CVE scanning but lacks license-risk taxonomy; security-scanning skill has no OSS component | S | **High** |
| 6 | Add multi-language robustness anti-patterns reference to code-review-standards | `universal/process/code-review-standards` | Robustness / _multi (42 rules) | A set of universal robustness items: generic catch, binary-operator-with-identical-members (always true/false), negative comparisons, avoid-public-finalize, exception-documentation consistency | `alt_genericcatches`, `alt_badvaluesoperator`, `alt_negativecomparison`, `alt_publicfinalizemethod`, `alt_commentedthrow` | Additive — code-review-standards has a "bare except" item but not the richer set | S | **Med** |
| 7 | Enrich PHP skills with robustness + security anti-patterns | `toolchains/php/frameworks/espocrm` + `toolchains/php/frameworks/wordpress/security-validation` | Security + Robustness / php (34 rules) | Add rules: empty-catch blocks, phpinfo() in production, goto usage, deprecated PHP4 constructor naming | `alt_emptycatches-avoid-empty-catch-blocks-php`, `alt_debug-phpinfo-not-used-production`, `alt_goto-never-use-goto` | Partially overlapping — WordPress security-validation skill covers XSS/CSRF/SQL-injection but not these code-quality issues; EspoCRM skill has no quality section | S | **Med** |
| 8 | Enrich TypeScript/JavaScript skills with JS-specific quality rules | `toolchains/typescript/core` or `toolchains/javascript/frameworks/nextjs` | Changeability / javascript (40 rules) | Rules: variables-should-be-declared-with-let-or-const, multiline-string-literals, logical-OR-in-switch-cases, modifications-of-builtin-objects, non-wrapped-IIFEs, variable-shadowing | `alt_variabledeclaration-variables-declared-let-const`, `alt_datashadowing`, `alt_behaviouralteration`, `alt_immediatefunccall` | Partial overlap — TypeScript Core skill covers tsconfig/type-safety; these are runtime/AST-level quality rules not currently covered | M | **Med** |
| 9 | Add SQL quality anti-patterns to database-migration or sqlalchemy skill | `toolchains/python/data/sqlalchemy` + `universal/data/database-migration` | Efficiency + Robustness / sql (35 rules) | Key SQL patterns: avoid SELECT DISTINCT for performance, avoid cursors-in-loops, avoid DDL/DML interleaving, avoid untrusted data in SQL, parameterize queries | `alt_badselect`, `alt_fetchinloop`, `alt_sqlinterleaving`, `alt_untrusteddata`, `alt_subqueries` | Additive — SQLAlchemy skill covers ORM patterns; database-migration skill covers migration mechanics; neither covers SQL code quality | M | **Med** |
| 10 | Enrich Go web/concurrency skills with Go-specific idioms from _multi rules (Go-tagged) | `toolchains/golang/web` + `toolchains/golang/concurrency` | Changeability / _multi (Go-tagged subset) | Go idioms: short variable declarations (:=), avoid naming unused receivers, avoid instantiation with new (use make/struct literal), avoid confusing closure placement | `alt_variabledeclaration-use-short-variable-declarations`, `alt_badreceiver`, `alt_badinstanciation`, `alt_closureaslastmethodparameter` | Additive — Go web skill covers HTTP frameworks and middleware; these idiomatic quality rules are absent | S | **Med** |
| 11 | Enrich software-patterns universal skill with Efficiency + Changeability architectural signals | `universal/architecture/software-patterns` | Efficiency + Changeability / _multi | Add a "code-smell signals that indicate architectural problems" appendix: large switch statements suggest missing polymorphism, nested loops suggest data-modelling issue, parameter updates inside routines suggest missing immutability | `alt_largeswitchcase`, `alt_nestedforloop`, `alt_parameterupdate` | Additive — software-patterns covers DI/SOA/Repository patterns; CAST rules provide code-smell signals that SHOULD trigger architectural review | S | **Med** |
| 12 | Add Kotlin/Scala quality rules to a new JVM quality reference | NEW or extend Spring Boot | Changeability + Transferability / kotlin (12), scala (13) | Expression-body preference, Elvis-operator idioms, labeled-return avoidance, unused-private-methods, boolean-check inversion | `alt_unexpectedbody`, `alt_couldbeelvis`, `alt_labeledreturnendinglambda`, `alt_unusedprivatemethods`, `alt_booleanpitfall` | Additive — we have no Kotlin or Scala skill; adding a compact JVM reference doc under Spring Boot is incremental | S | **Low** |
| 13 | Enrich webapp-testing / testing-anti-patterns with code-insight detection framing | `universal/testing/testing-anti-patterns` + `universal/testing/webapp-testing` | Transferability / _multi | Framing borrowed from CAST: "statistical tool" mindset, counting violations at scale, production-risk classification | `alt_genericcatches`, `alt_illegalexception` (as example CAST-style detection explanations) | Low overlap — testing skills cover test design; CAST's "how we detect" framing is a novel addition for test coverage guidelines | S | **Low** |

---

## 3. Methodology-Derived New Skill: `universal/quality/code-quality-scoring`

### Rationale

The 13 CAST methodology pages describe a complete, vendor-neutral framework for
quantifying and communicating software quality. We currently have no skill that helps
a developer or tech lead:

- Explain technical debt in business terms (USD per line of code by language)
- Score an application's cloud-readiness (Cloud Scan + Survey)
- Assess open-source component risk holistically (CVE + license + obsolescence)
- Understand the Resiliency / Agility / Elegance decomposition of "code health"

This is a genuine gap that affects architects, team leads, and anyone who needs to
present quality metrics to non-technical stakeholders.

### Proposed Skill Contents

**Entry point** (`SKILL.md`):
- When to use: when assessing a codebase for health, debt, or cloud readiness
- Quick reference: the 3 Software Health sub-scores + their thresholds
- Pointer to references

**Reference docs** (`references/`):

| File | Derived From | Content |
|------|-------------|---------|
| `software-health-framework.md` | `software-health.md`, `software-agility.md`, CAST methodology deck | Software Health = avg(Resiliency, Agility, Elegance); thresholds (red <53, orange 53-75, green >75); how each sub-score is composed |
| `technical-debt-estimation.md` | `technical-debt-estimates-stats-technology.md` | Tech debt density by language (min/quartile/median/max hours per LOC); how to produce a back-of-envelope estimate; caveats |
| `open-source-safety.md` | `open-source-safety.md`, `open-source-license-risk-profiles.md`, `transitive-dependencies-...md` | CVE weighting model; license risk tiers (HIGH/MEDIUM/LOW mapped to GPL/MPL/MIT); obsolescence scoring; transitive dependency trust model |
| `cloud-maturity.md` | `cloud-maturity.md` | Cloud Scan + Cloud Survey components; what blockers vs boosters look like in code |
| `quality-communication-guide.md` | Synthesis | How to present quality scores to stakeholders; mapping CAST scores to team actions |

### Effort and Caveats

**Effort:** L (one full day to write cleanly, ensure paraphrase fidelity, add worked examples)

**Important:** This skill should derive patterns and frameworks from CAST's methodology
rather than reproduce their exact scoring algorithms. The debt-per-LOC table values are
empirical from CAST's AppMarq dataset — these can be cited by reference/range rather
than copied verbatim. See Section 6 for the attribution approach.

**Is it worthwhile?** Yes. This is the only enrichment that creates net-new capability
rather than improving existing coverage. Every other item adds quality depth to existing
skills; this one opens a new category (quality strategy and communication) with no
current analogue.

---

## 4. Gaps — Languages / Topics Where CAST Is Rich but We Lack a Skill

### SQL (35 rules) — Significant Gap

CAST has 35 SQL rules covering: inefficient SELECT patterns, cursor-in-loop
anti-patterns, DDL/DML interleaving, parameterization, subquery complexity, and
documentation. We have no dedicated SQL skill. We have skills that touch SQL
adjacently (SQLAlchemy, database-migration, Neon, Supabase) but none that teaches SQL
code quality in its own right.

**Recommendation:** Do not create a standalone SQL skill (too specialized to be
broadly useful). Instead, route the most impactful SQL rules into `toolchains/python/
data/sqlalchemy` (performance and correctness rules) and `universal/data/database-
migration` (DDL hygiene and interleaving rules). Flag the rest as out of scope unless
the user base shows strong SQL demand.

### Kotlin and Scala (12 + 13 rules) — Partial Gap

CAST has 25 rules across Kotlin and Scala with good code examples. We have no Kotlin
or Scala skill. Given these are JVM-adjacent to Java/Spring Boot, the highest-effort
approach (new skills) is not justified yet. The lower-effort path: add a compact
"JVM family quality notes" appendix to the Spring Boot skill's reference docs.

### ABAP / COBOL / Swift / C++ (11 + 8 + 9 + 15 rules) — Out of Scope

We have no skills for these languages and no indication of user demand. CAST's content
here is genuine but unlikely to benefit our current audience. Flag for future if demand
emerges.

### .NET / C# (7 rules) — Partial Gap

Our VisualBasic skills cover VB.NET but not C#. CAST has 7 .NET rules (Efficiency-
focused: finalizer patterns, memory management). Low priority unless the user base
grows into .NET territory.

### Ruby (2 rules) — Too Sparse

CAST has only 2 Ruby rules. No basis for enrichment.

---

## 5. Licensing and Attribution Note

CAST Highlight's documentation is proprietary content belonging to CAST Software.
This knowledgebase was constructed from the public-facing documentation at
`https://doc.casthighlight.com/category/product/indicators-methodology/` for
internal research and skill development.

**Required practices for any enrichment work:**

1. **Paraphrase, do not copy.** Skill content must express the underlying principle in
   our own words with original examples. Do not reproduce CAST's exact prose or
   code snippets verbatim.
2. **Attribute sources.** Where a pattern, threshold value, or framework is derived
   from CAST's methodology, include a note such as: "Pattern derived from CAST
   Highlight code quality indicators (https://doc.casthighlight.com/)."
3. **Empirical data requires care.** The technical-debt-by-language table contains
   CAST-proprietary benchmark data from the AppMarq dataset. Use range descriptions
   (e.g., "Java median debt density is roughly 3-4x that of Python according to
   industry benchmarks") rather than exact values.
4. **Rules that mirror open standards** (PEP 8, Android code style, SonarSource
   rules, CodeNarc) can be written with reference to those primary sources instead of
   citing CAST, since CAST itself cites them.
5. **Do not embed CAST's scoring formulas or index thresholds** as normative without
   noting they are CAST's proprietary calibration. Present them as reference context,
   not as universal standards.

---

## 6. Recommended Phased Rollout

### Phase 1 — Maximum leverage, minimum new surface area (2–3 days total)

Focus on enriching existing skills with additive sections/references. No new skills
yet.

| Step | Action | Effort |
|------|--------|--------|
| 1a | Add Efficiency + Transferability checklist items to `universal/process/code-review-standards` (new criteria-efficiency.md + criteria-transferability.md reference docs) | M |
| 1b | Add Open Source Safety section to `toolchains/universal/dependency/audit` (license-risk tiers, CVE weighting framing, obsolescence signal) | S |
| 1c | Add Python quality anti-patterns reference to `toolchains/python/` — create `toolchains/python/quality/` or add `references/quality-antipatterns.md` to the pytest skill | M |

### Phase 2 — Highest-demand language enrichments (2–4 days)

| Step | Action | Effort |
|------|--------|--------|
| 2a | Add Java robustness + changeability reference doc to `toolchains/java/frameworks/spring-boot` | M |
| 2b | Add PHP quality/security rules to `toolchains/php/frameworks/espocrm` and WordPress security-validation skill | S |
| 2c | Add TypeScript/JS code-quality rules section to `toolchains/typescript/core` | M |

### Phase 3 — New skill and remaining enrichments (3–5 days)

| Step | Action | Effort |
|------|--------|--------|
| 3a | Create `universal/quality/code-quality-scoring` (new skill, methodology-derived) | L |
| 3b | SQL anti-patterns into SQLAlchemy and database-migration skills | M |
| 3c | Go idiomatic quality rules into golang/web + golang/concurrency | S |
| 3d | Software-patterns architectural signals appendix | S |

### What to skip (for now)

- Kotlin and Scala standalone skills: low user-base signal
- ABAP, COBOL, Swift, C++ enrichments: out of scope
- .NET enrichments: wait for demand signal
- CAST's exact scoring thresholds as normative values: licensing risk

---

## Appendix: Content Quality Assessment

Overall CAST KB quality is **high** for rules that have code examples (marked
`has_code_examples: true` in the catalog). Rules without code examples tend to be
thinner — often a paragraph of explanation without concrete before/after patterns. The
enrichment proposals above deliberately bias toward rules that have code examples, as
these provide the most usable content for our skills format.

The methodology pages are concise (typically 1–2 pages each) but well-structured.
They define quantitative thresholds that give our skills rare specificity on "what
constitutes healthy code" — a dimension most of our existing skills lack entirely.

The SQL rules vary in quality: some are rigorous (cursor-in-loop, DDL/DML
interleaving), others are underdeveloped (the fetchinloop file discusses primary key
selection, not actual cursor-in-loop behavior — the CAST KB has some title/content
mismatches in SQL rules). Recommend spot-checking individual SQL rules before
incorporating.
