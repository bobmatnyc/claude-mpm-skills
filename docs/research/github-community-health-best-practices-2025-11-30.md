# GitHub Community Health Best Practices for Open Source Skill Repositories

**Research Date:** 2025-11-30
**Repository:** claude-mpm-skills
**Objective:** Identify essential GitHub community health files and configurations needed to accept public PRs and issues for open source skill repository.

## Executive Summary

This research identifies the critical GitHub community health files, issue template structures, PR workflows, and repository configurations required to transform `claude-mpm-skills` into a contributor-friendly open source project. The repository already has a strong foundation with CONTRIBUTING.md, PR template, CODEOWNERS, and validation workflow. Key gaps include: CODE_OF_CONDUCT.md, SECURITY.md, structured issue templates, and comprehensive label taxonomy.

**Key Findings:**
- ✅ **Strong Foundation**: CONTRIBUTING.md, PR template, CODEOWNERS, CI validation already in place
- ⚠️ **Missing Critical Files**: CODE_OF_CONDUCT.md, SECURITY.md, structured YAML issue templates
- 📋 **Recommended Additions**: 4 issue template types, label taxonomy, branch protection rules
- 🎯 **Priority Focus**: Skill proposal workflow, quality validation, community engagement

**Current State Assessment:**

| Component | Status | Priority |
|-----------|--------|----------|
| CONTRIBUTING.md | ✅ Exists (comprehensive) | Maintain |
| LICENSE | ✅ Exists (MIT) | Maintain |
| Pull Request Template | ✅ Exists | Enhance |
| CODEOWNERS | ✅ Exists | Maintain |
| CI Validation Workflow | ✅ Exists | Enhance |
| CODE_OF_CONDUCT.md | ❌ Missing | HIGH |
| SECURITY.md | ❌ Missing | MEDIUM |
| Issue Templates (YAML) | ❌ Missing | HIGH |
| Label Taxonomy | ⚠️ Basic | MEDIUM |
| Branch Protection Rules | ⚠️ Unknown | MEDIUM |

---

## 1. GitHub Community Health Files: Complete Inventory

### 1.1 Required Files (GitHub Standard)

Based on GitHub's official documentation, these files are recognized as community health standards:

#### **CODE_OF_CONDUCT.md** (HIGH PRIORITY - MISSING)
- **Purpose:** Defines standards for community engagement and behavior
- **Location:** Repository root, `.github/`, or `docs/`
- **Standard:** Contributor Covenant (v2.1 recommended)
- **Status:** ❌ **Not present in claude-mpm-skills**

**Why Required:**
- Sets clear expectations for respectful collaboration
- Required for GitHub Community Standards badge
- Signals professional, welcoming environment to contributors
- Reduces moderation burden through clear policies

**Recommendation:** Adopt Contributor Covenant v2.1 ([template](https://www.contributor-covenant.org/))

---

#### **CONTRIBUTING.md** (✅ EXISTS - EXCELLENT)
- **Purpose:** Communicates how people should contribute to the project
- **Location:** Repository root (current location)
- **Status:** ✅ **Present and comprehensive**

**Current Strengths:**
- Clear skill structure requirements
- Self-containment standard enforcement
- Progressive disclosure format guidelines
- Step-by-step submission process
- Testing requirements with checklist
- Manifest update instructions

**Recommendations:**
- ✅ Already excellent - no major changes needed
- Consider adding "New Contributor Guide" section
- Link to issue templates when created

---

#### **SECURITY.md** (MEDIUM PRIORITY - MISSING)
- **Purpose:** Provides instructions for reporting security vulnerabilities
- **Location:** Repository root, `.github/`, or `docs/`
- **Status:** ❌ **Not present in claude-mpm-skills**

**Why Needed:**
- Populates GitHub's "Security Policy" field
- Provides secure channel for vulnerability reporting
- Industry best practice for open source projects
- Low-risk project but still recommended

**Template Structure (based on OSSF guidelines):**
```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

**DO NOT** create a public issue for security vulnerabilities.

Instead, please report vulnerabilities by:
1. Using GitHub's private vulnerability reporting (if enabled)
2. Emailing: [security contact email]
3. Including: affected skill, description, reproduction steps

**Response Timeline:**
- Acknowledgment: Within 48 hours
- Initial assessment: Within 7 days
- Remediation: Based on severity

## Disclosure Policy

We practice coordinated disclosure and will work with reporters to:
- Validate and fix vulnerabilities
- Credit reporters (if desired)
- Coordinate public disclosure timing
```

**Specific Considerations for Skill Repository:**
- Lower risk than code libraries (skills are instructions, not executable packages)
- Focus on: malicious skill content, credential leakage in examples, social engineering risks
- Template should address: skill validation, content review process, example safety

---

#### **FUNDING.yml** (OPTIONAL)
- **Purpose:** Displays sponsor button in repository
- **Location:** `.github/FUNDING.yml`
- **Status:** ❌ Not present
- **Priority:** LOW (optional for this project type)

---

#### **SUPPORT.md** (OPTIONAL)
- **Purpose:** Explains where to get help with the project
- **Location:** Repository root, `.github/`, or `docs/`
- **Status:** ❌ Not present
- **Priority:** LOW (can redirect to GitHub Discussions or Issues)

**Minimal Template:**
```markdown
# Support

## Getting Help

- **Questions**: Open a [GitHub Discussion](link)
- **Bug Reports**: Use the [Bug Report template](link)
- **Feature Requests**: Use the [Feature Request template](link)
- **Skill Proposals**: Use the [New Skill Proposal template](link)

## Community

- Maintainer: @bobmatnyc
- Response time: Best effort, typically within 7 days
```

---

### 1.2 Issue and Pull Request Templates

#### **Issue Templates (YAML Format) - HIGH PRIORITY**

GitHub recommends YAML-based issue forms over markdown templates for structured data collection.

**Location:** `.github/ISSUE_TEMPLATE/`

**Required Files:**
1. `bug_report.yml` - Bug reports for broken skills
2. `feature_request.yml` - Enhancement requests
3. `new_skill_proposal.yml` - Structured skill submissions
4. `config.yml` - Template configuration

---

##### **Template 1: Bug Report (`bug_report.yml`)**

```yaml
name: 🐛 Bug Report
description: Report a broken skill or deployment issue
title: "[Bug]: "
labels: ["bug", "triage"]
assignees:
  - bobmatnyc
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report this bug! Please provide details below.

  - type: dropdown
    id: bug-type
    attributes:
      label: Bug Type
      description: What kind of issue are you experiencing?
      options:
        - Skill fails to load in Claude Code
        - Broken reference or link
        - Validation error
        - Manifest inconsistency
        - Documentation error
        - Other
      default: 0
    validations:
      required: true

  - type: input
    id: skill-name
    attributes:
      label: Skill Name
      description: Which skill is affected?
      placeholder: "e.g., fastapi-local-dev, nextjs-routing"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Clear description of the bug
      placeholder: What went wrong?
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this issue?
      placeholder: |
        1. Deploy skill to Claude Code
        2. Trigger condition X
        3. See error Y
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen instead?
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Technical details
      value: |
        - Claude Code version:
        - OS:
        - Project type:
    validations:
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: Pre-submission Checklist
      options:
        - label: I searched existing issues for duplicates
          required: true
        - label: I verified the skill was recently updated
          required: false
        - label: I tested with latest Claude Code version
          required: false
```

---

##### **Template 2: Feature Request (`feature_request.yml`)**

```yaml
name: ✨ Feature Request
description: Suggest an enhancement to existing skill or repository
title: "[Feature]: "
labels: ["enhancement", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting an improvement!

  - type: dropdown
    id: feature-type
    attributes:
      label: Feature Type
      options:
        - Enhancement to existing skill
        - New documentation
        - Tooling improvement
        - CI/CD enhancement
        - Repository organization
        - Other
      default: 0
    validations:
      required: true

  - type: input
    id: skill-or-area
    attributes:
      label: Skill or Area
      description: Which skill or area would this enhance?
      placeholder: "e.g., pytest, CONTRIBUTING.md, CI workflow"
    validations:
      required: true

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this solve?
      placeholder: Describe the pain point or limitation
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How would you solve this?
      placeholder: Describe your proposed enhancement
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Any alternative approaches?
    validations:
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: Pre-submission Checklist
      options:
        - label: I searched existing issues and PRs
          required: true
        - label: This aligns with repository goals
          required: true
```

---

##### **Template 3: New Skill Proposal (`new_skill_proposal.yml`) - CRITICAL**

This is the most important template for skill repositories - it guides contributors through proper skill submission.

```yaml
name: 🚀 New Skill Proposal
description: Propose a new skill for the repository
title: "[Skill]: "
labels: ["new-skill", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        ## Skill Proposal Guidelines

        Before proposing a new skill, please:
        - Review [CONTRIBUTING.md](../CONTRIBUTING.md)
        - Check [Skill Self-Containment Standard](../docs/SKILL_SELF_CONTAINMENT_STANDARD.md)
        - Verify no similar skill exists

        **Note:** For complex skills, consider opening a proposal issue BEFORE implementing.

  - type: input
    id: skill-name
    attributes:
      label: Skill Name
      description: Proposed skill name (kebab-case)
      placeholder: "e.g., redis-caching, graphql-federation"
    validations:
      required: true

  - type: dropdown
    id: category
    attributes:
      label: Category
      description: Where does this skill belong?
      options:
        - Python Framework
        - Python Testing
        - Python Data/ORM
        - Python Async
        - Python Tooling
        - TypeScript Framework
        - TypeScript Testing
        - TypeScript Data
        - TypeScript State Management
        - JavaScript Framework
        - JavaScript Testing
        - Next.js
        - UI Components
        - UI Styling
        - AI SDK
        - AI Framework
        - AI Services
        - Platform Deployment
        - Platform Database
        - Universal Infrastructure
        - Universal Testing
        - Universal Architecture
        - Other (specify in description)
      default: 0
    validations:
      required: true

  - type: dropdown
    id: toolchain
    attributes:
      label: Toolchain
      description: Which toolchain does this target?
      options:
        - python
        - typescript
        - javascript
        - nextjs
        - ui
        - ai
        - platforms
        - universal
      default: 0
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Skill Description
      description: What does this skill do? (30-50 word summary)
      placeholder: "Example: Guides FastAPI development with async patterns, dependency injection, OpenAPI docs, and testing strategies."
    validations:
      required: true

  - type: textarea
    id: when-to-use
    attributes:
      label: When to Use
      description: What triggers should activate this skill?
      placeholder: |
        - Project has pyproject.toml with fastapi dependency
        - User mentions "FastAPI" or "API development"
        - Detected FastAPI imports in codebase
    validations:
      required: true

  - type: textarea
    id: key-topics
    attributes:
      label: Key Topics Covered
      description: What will this skill teach Claude?
      placeholder: |
        - Path operations and routing
        - Dependency injection
        - Request/response models (Pydantic)
        - Authentication patterns
        - Testing with TestClient
    validations:
      required: true

  - type: textarea
    id: examples
    attributes:
      label: Example Use Cases
      description: Real-world scenarios where this skill is valuable
      placeholder: |
        1. Building REST API with automatic OpenAPI docs
        2. Implementing OAuth2 authentication
        3. Writing async background tasks
    validations:
      required: true

  - type: dropdown
    id: complexity
    attributes:
      label: Skill Complexity
      description: How complex is this skill to implement?
      options:
        - Simple (< 500 tokens, minimal examples)
        - Moderate (500-2000 tokens, multiple examples)
        - Complex (2000-5000 tokens, comprehensive examples)
        - Very Complex (5000+ tokens, extensive documentation)
      default: 1
    validations:
      required: true

  - type: dropdown
    id: implementation-status
    attributes:
      label: Implementation Status
      description: Have you already implemented this skill?
      options:
        - Proposal only (seeking feedback before implementing)
        - Draft implementation (will submit PR soon)
        - Ready to submit PR (already implemented and tested)
      default: 0
    validations:
      required: true

  - type: textarea
    id: self-containment
    attributes:
      label: Self-Containment Verification
      description: How will this skill meet self-containment requirements?
      placeholder: |
        - No dependencies on other skills
        - All examples inlined
        - Works in flat directory structure
        - No relative path references
    validations:
      required: true

  - type: textarea
    id: related-skills
    attributes:
      label: Related Skills
      description: Any existing skills this complements or overlaps with?
      placeholder: "e.g., Complements pytest skill, overlaps with django (different framework)"
    validations:
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: Proposal Checklist
      options:
        - label: I searched for similar existing skills
          required: true
        - label: I read the Skill Self-Containment Standard
          required: true
        - label: I reviewed CONTRIBUTING.md guidelines
          required: true
        - label: This skill serves a distinct purpose (not duplicate)
          required: true
        - label: I can provide real-world examples
          required: true

  - type: markdown
    attributes:
      value: |
        ---

        **Next Steps:**
        1. Maintainer will review proposal and provide feedback
        2. If approved, you can implement the skill following CONTRIBUTING.md
        3. Submit PR using the PR template when ready
        4. PR will undergo validation and review

        Thank you for contributing! 🙏
```

---

##### **Template 4: config.yml**

Controls template chooser behavior and adds custom links.

```yaml
blank_issues_enabled: false
contact_links:
  - name: 💬 GitHub Discussions
    url: https://github.com/bobmatnyc/claude-mpm-skills/discussions
    about: Ask questions, share ideas, and discuss skills
  - name: 📚 Documentation
    url: https://github.com/bobmatnyc/claude-mpm-skills/blob/main/CONTRIBUTING.md
    about: Read contributing guidelines and skill standards
  - name: 🔍 Skill Self-Containment Standard
    url: https://github.com/bobmatnyc/claude-mpm-skills/blob/main/docs/SKILL_SELF_CONTAINMENT_STANDARD.md
    about: Review self-containment requirements before submitting skills
```

**Configuration Notes:**
- `blank_issues_enabled: false` - Forces use of templates (recommended for structured intake)
- Contact links appear above template chooser
- Provides alternative support channels

---

#### **Pull Request Template Enhancement**

**Current Template:** Good foundation, needs enrichment for comprehensive validation.

**Location:** `.github/pull_request_template.md`

**Enhanced Version:**

```markdown
## Pull Request Type

- [ ] New skill
- [ ] Enhancement to existing skill
- [ ] Bug fix
- [ ] Documentation update
- [ ] Repository infrastructure (CI, templates, etc.)

## Skill Information

**Skill Name:** <!-- e.g., fastapi-local-dev -->
**Toolchain:** <!-- Python, TypeScript, JavaScript, Next.js, UI, AI, Platforms, Universal -->
**Category:** <!-- Framework, Testing, Data, etc. -->

## Description

<!-- Clear description of what this PR does and why it's needed -->

## Related Issues

Closes #<!-- issue number -->

## Self-Containment Compliance

All skills MUST follow the [Skill Self-Containment Standard](../docs/SKILL_SELF_CONTAINMENT_STANDARD.md).

**Verification (required for skill PRs):**

- [ ] **Zero relative paths**: Ran `grep -r "\\.\\.\\/\\|\\.\\/.*SKILL\\.md" <skill-directory>/` → returns empty
- [ ] **No skill dependencies**: `metadata.json` has empty `dependencies` array
- [ ] **Flat directory test**: Deployed skill to `/tmp/skill-test/` and verified it loads correctly
- [ ] **Essential content inlined**: All critical examples and guidance included in SKILL.md
- [ ] **Works standalone**: Skill functions without requiring other skills

## Testing

<!-- How did you test this? -->

- [ ] Tested with Claude Code in real project
- [ ] Verified progressive loading works (entry point loads first)
- [ ] Checked token efficiency (entry point < 50 tokens)
- [ ] Tested trigger conditions (skill activates appropriately)
- [ ] Verified examples are practical and tested

## Documentation Checklist

- [ ] **SKILL.md follows progressive disclosure format**
  - [ ] Tier 1: Entry Point (30-50 tokens max)
  - [ ] Tier 2: Full documentation with examples
- [ ] **metadata.json is complete and valid**
  - [ ] All required fields present (name, version, category, toolchain, description, tags, author, updated)
  - [ ] Version follows semver (X.Y.Z)
  - [ ] Tags are descriptive and relevant
  - [ ] Date is current (YYYY-MM-DD format)
- [ ] **No sensitive data** (API keys, credentials, tokens, emails)
- [ ] **Examples are provided** and tested in real scenarios
- [ ] **Skill category is appropriate** for toolchain and functionality

## Manifest Update (for new skills)

- [ ] Updated `manifest.json` with new skill entry
- [ ] Entry includes: name, path, version
- [ ] Placed in correct toolchain/category section
- [ ] JSON is valid (no syntax errors)

## Code Quality

- [ ] **Self-contained**: Meets all requirements in checklist above
- [ ] **No broken links**: All URLs and references work
- [ ] **Clear and concise**: Documentation is easy to understand
- [ ] **Real-world focused**: Examples reflect actual use cases
- [ ] **Best practices**: Follows current 2025 patterns

## Additional Notes

<!-- Any extra context, implementation decisions, or areas needing review -->

## Pre-submission Final Check

- [ ] I have read and followed [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] I have reviewed the [Skill Self-Containment Standard](../docs/SKILL_SELF_CONTAINMENT_STANDARD.md)
- [ ] I have used the [PR Checklist](../docs/SKILL_CREATION_PR_CHECKLIST.md)
- [ ] All checkboxes above are completed
- [ ] This PR is ready for review

---

/cc @bobmatnyc
```

**Key Enhancements:**
1. **Self-containment verification** - Explicit commands to verify compliance
2. **Flat directory test** - Ensures skills work in any location
3. **Manifest update** - Reminds contributors to update registry
4. **Progressive disclosure check** - Validates token efficiency
5. **Pre-submission final check** - Ensures thorough review

---

## 2. Label Taxonomy for Issue Triage

Based on research from Creative Commons and GitHub best practices, here's a recommended label system for claude-mpm-skills:

### 2.1 Label Organization Principles

**Format:** `<prefix>: <name>` or `<emoji> <category>: <name>`
**Colors:** Consistent within categories
**Goal:** Enable efficient filtering and visual scanning

### 2.2 Recommended Label Categories

#### **Priority Labels** (Mandatory for issues)

Controls sprint planning and urgency.

| Label | Color | Description |
|-------|-------|-------------|
| `🟥 priority: critical` | `#b60205` (red) | Must be fixed ASAP - broken core functionality |
| `🟧 priority: high` | `#d93f0b` (orange) | Blocks dependent work or affects many users |
| `🟨 priority: medium` | `#fbca04` (yellow) | Important but non-blocking |
| `🟩 priority: low` | `#cfda2c` (green) | Nice to have, no rush |

**Usage:**
- Every issue gets exactly ONE priority label
- Re-evaluate priority as context changes
- Critical: security issues, broken deployments, blocking bugs
- High: feature gaps affecting major workflows
- Medium: enhancements, minor bugs, documentation
- Low: polish, refactoring, future considerations

---

#### **Status Labels** (Workflow state)

Indicates readiness for work.

| Label | Color | Description |
|-------|-------|-------------|
| `🚦 status: triage` | `#eeeeee` (light gray) | Needs initial review and labeling |
| `🔍 status: needs-info` | `#d4c5f9` (purple) | Awaiting information from reporter |
| `🚧 status: blocked` | `#333333` (dark gray) | Cannot proceed due to dependency |
| `🏁 status: ready` | `#0e8a16` (green) | Ready for implementation |
| `👀 status: in-review` | `#fbca04` (yellow) | Under active review |
| `⛔ status: wontfix` | `#ffffff` (white) | Rejected/out of scope |
| `✅ status: done` | `#1d76db` (blue) | Completed (before closing) |

**Usage:**
- Issues start with `status: triage`
- Move to `status: ready` after validation
- `status: blocked` requires explanation in comments
- `status: wontfix` requires justification before closing

---

#### **Type Labels** (Issue classification)

Describes the nature of the issue.

| Label | Color | Description |
|-------|-------|-------------|
| `🐛 type: bug` | `#d73a4a` (red) | Something isn't working correctly |
| `✨ type: enhancement` | `#a2eeef` (cyan) | Improvement to existing feature |
| `🚀 type: new-skill` | `#0075ca` (blue) | Proposal for new skill |
| `📖 type: documentation` | `#0075ca` (blue) | Documentation improvements |
| `🔧 type: tooling` | `#d4c5f9` (purple) | CI/CD, scripts, automation |
| `💬 type: question` | `#d876e3` (pink) | User question or clarification |
| `🎨 type: design` | `#e99695` (salmon) | UI/UX, repository structure |

**Usage:**
- Issues typically have ONE type label
- `type: new-skill` triggers special review process
- Questions should be redirected to Discussions if possible

---

#### **Skill Category Labels** (Skill-specific)

Links issues to skill domains.

| Label | Color | Description |
|-------|-------|-------------|
| `skill: python` | `#3572A5` (python blue) | Python skills |
| `skill: typescript` | `#2b7489` (TS blue) | TypeScript skills |
| `skill: javascript` | `#f1e05a` (JS yellow) | JavaScript skills |
| `skill: nextjs` | `#000000` (black) | Next.js skills |
| `skill: ui` | `#563d7c` (purple) | UI/styling skills |
| `skill: ai` | `#ff6f00` (orange) | AI/ML skills |
| `skill: platform` | `#89e051` (green) | Platform/deployment skills |
| `skill: universal` | `#ededed` (gray) | Universal skills |

**Usage:**
- Tag issues with relevant skill area(s)
- Helps maintainers route to domain experts
- Can apply multiple skill labels if cross-cutting

---

#### **Effort Labels** (Contributor guidance)

Indicates implementation complexity.

| Label | Color | Description |
|-------|-------|-------------|
| `effort: small` | `#c2e0c6` (light green) | < 2 hours of work |
| `effort: medium` | `#fef2c0` (light yellow) | 2-8 hours of work |
| `effort: large` | `#f9d0c4` (light orange) | 1-3 days of work |
| `effort: epic` | `#d93f0b` (dark orange) | Multi-day or requires research |

**Usage:**
- Helps contributors choose appropriately scoped work
- Combines with `good first issue` for onboarding

---

#### **Community Labels** (Contributor friendliness)

Signals opportunities for external contributors.

| Label | Color | Description |
|-------|-------|-------------|
| `good first issue` | `#7057ff` (purple) | Good for newcomers (GitHub recognized) |
| `help wanted` | `#008672` (teal) | Maintainer requests community help (GitHub recognized) |
| `🔒 staff only` | `#d73a4a` (red) | Requires maintainer privileges |
| `duplicate` | `#cfd3d7` (gray) | Duplicate of another issue |
| `invalid` | `#e4e669` (pale yellow) | Invalid issue (spam, off-topic) |

**Usage:**
- `good first issue`: Well-defined, small effort, clear acceptance criteria
- `help wanted`: Maintainer is not planning to work on this immediately
- `staff only`: Security issues, governance, critical infrastructure

---

#### **Automated Labels** (Applied by CI)

| Label | Color | Description |
|-------|-------|-------------|
| `🤖 auto: validation-failed` | `#b60205` (red) | CI validation checks failed |
| `🤖 auto: sensitive-data` | `#d73a4a` (red) | Potential credentials detected |
| `🤖 auto: manifest-error` | `#d93f0b` (orange) | manifest.json validation failed |

**Usage:**
- Applied automatically by GitHub Actions
- Require manual intervention to clear
- Block PR merging until resolved

---

### 2.3 Label Application Rules

**Every Issue Must Have:**
1. One `priority` label
2. One `type` label
3. One `status` label (starts with `status: triage`)

**Optional Labels:**
- One or more `skill` labels
- One `effort` label (recommended for tasks)
- Community labels as appropriate

**Label Workflow:**
```
New Issue Created
   ↓
Auto-labeled: status: triage
   ↓
Maintainer Reviews
   ↓
Applies: priority, type, skill, effort
   ↓
Changes status → ready | needs-info | blocked | wontfix
   ↓
Contributor assigned
   ↓
status → in-review (during PR review)
   ↓
status → done (PR merged)
   ↓
Issue Closed
```

---

## 3. Repository Settings and Configuration

### 3.1 Branch Protection Rules

**Branch:** `main`

**Recommended Settings:**

#### **Require Pull Request Reviews Before Merging**
- ✅ **Required approvals:** 1
- ✅ **Dismiss stale reviews:** Yes (when new commits pushed)
- ✅ **Require review from Code Owners:** Yes (CODEOWNERS file exists)
- ⚠️ **Restrict who can dismiss reviews:** Optional (small team)

**Rationale:**
- Single maintainer (@bobmatnyc) makes 1 approval appropriate
- CODEOWNERS ensures @bobmatnyc reviews all changes
- Stale dismissal prevents outdated approvals

---

#### **Require Status Checks to Pass**
- ✅ **Require branches to be up to date:** Yes
- ✅ **Required checks:**
  - `validate / validate` (from `.github/workflows/validate-skills.yml`)

**Rationale:**
- Prevents merging of malformed skills
- Validates manifest.json consistency
- Detects sensitive data before merge
- Ensures skill structure compliance

---

#### **Require Conversation Resolution**
- ✅ **Enabled:** Yes

**Rationale:**
- All review comments must be addressed before merge
- Ensures thorough discussion of issues

---

#### **Require Linear History**
- ⚠️ **Optional:** Consider enabling

**Rationale:**
- Pros: Cleaner git history, easier to track changes
- Cons: Requires rebase workflow (may confuse new contributors)
- Recommendation: **Disabled** initially for contributor friendliness

---

#### **Other Settings**
- ✅ **Allow force pushes:** Disabled
- ✅ **Allow deletions:** Disabled
- ⚠️ **Restrict who can push:** Optional (only @bobmatnyc if strict control desired)

---

### 3.2 Repository Settings

**General Settings:**

| Setting | Recommendation | Rationale |
|---------|----------------|-----------|
| **Issues** | ✅ Enabled | Primary contribution channel |
| **Projects** | Optional | May be useful for roadmap tracking |
| **Discussions** | ✅ Enabled | Q&A, community feedback |
| **Sponsorships** | Optional | If FUNDING.yml added |
| **Preserve this repository** | ✅ Yes | Arctic Code Vault archival |
| **Require signed commits** | ⚠️ Optional | Increases security but adds friction |

**Pull Request Settings:**

| Setting | Recommendation | Rationale |
|---------|----------------|-----------|
| **Allow merge commits** | ✅ Yes | Standard workflow |
| **Allow squash merging** | ✅ Yes | Cleaner history for small PRs |
| **Allow rebase merging** | ⚠️ Optional | Advanced users |
| **Automatically delete head branches** | ✅ Yes | Keeps repo clean |
| **Limit to collaborators** | ❌ No | Open source - accept external PRs |

**Merge Button:**
- Default to: **Squash and merge** (recommended for skill PRs)
- Allows: Merge commit, Squash, Rebase

**Rationale:**
- Squash encourages atomic skill additions
- Merge commits for multi-commit PRs with logical progression
- Rebase for advanced contributors maintaining clean history

---

### 3.3 GitHub Actions Permissions

**Workflow Permissions:**
- **Default:** Read repository contents
- **Custom:**
  - ✅ Read: Issues, Pull Requests, Contents
  - ✅ Write: Comments (for bot feedback)
  - ❌ Write: Contents (prevent accidental auto-commits)

**Token Permissions for External Actions:**
- Use `secrets.GITHUB_TOKEN` with minimal scope
- No third-party actions currently in use (good security posture)

---

### 3.4 Security Settings

**Vulnerability Alerts:**
- ✅ **Dependabot alerts:** Enabled (monitors dependencies if added)
- ✅ **Dependabot security updates:** Enabled
- ⚠️ **Private vulnerability reporting:** Enable when SECURITY.md added

**Code Scanning:**
- ⚠️ **CodeQL:** Not critical (no executable code, only markdown/json)
- ✅ **Secret scanning:** **HIGHLY RECOMMENDED** (detects leaked credentials in skills)

**Recommendation:** Enable secret scanning alerts via repository settings.

---

## 4. Skill Contribution Workflow

### 4.1 Contributor Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTRIBUTOR JOURNEY                       │
└─────────────────────────────────────────────────────────────┘

1. DISCOVER
   ├─ Browse README.md (skill catalog)
   ├─ Check existing skills for gaps
   └─ Read CONTRIBUTING.md

2. PROPOSE (Optional but Recommended)
   ├─ Open "New Skill Proposal" issue
   ├─ Describe skill purpose, category, examples
   ├─ Get feedback from maintainer
   └─ Issue labeled: type: new-skill, priority: X, status: ready

3. IMPLEMENT
   ├─ Fork repository
   ├─ Create feature branch: add-skill-<name>
   ├─ Create skill directory in correct category
   │   ├─ toolchains/<toolchain>/<category>/<skill-name>/
   │   │   ├─ SKILL.md (progressive disclosure format)
   │   │   └─ metadata.json (complete fields)
   │   └─ OR universal/<category>/<skill-name>/
   ├─ Verify self-containment:
   │   ├─ grep -r "\\.\\.\\/\\|\\.\\/.*SKILL\\.md" <skill-dir>/ → empty
   │   ├─ Test in /tmp/skill-test/ (flat directory)
   │   └─ Check metadata.json dependencies: []
   ├─ Update manifest.json (add skill entry)
   └─ Test in real Claude Code session

4. VALIDATE (Local)
   ├─ Run self-containment checklist
   ├─ Verify progressive disclosure (entry < 50 tokens)
   ├─ Test skill loading and trigger conditions
   ├─ Ensure examples are practical and tested
   └─ Check no sensitive data in examples

5. SUBMIT
   ├─ Push to fork: git push origin add-skill-<name>
   ├─ Create Pull Request using PR template
   ├─ Complete ALL checklist items in PR template
   ├─ Link to proposal issue (if exists): "Closes #X"
   └─ Tag @bobmatnyc for review

6. REVIEW
   ├─ Automated checks run (CI validation)
   │   ├─ Skill structure validation
   │   ├─ manifest.json syntax check
   │   └─ Sensitive data detection
   ├─ Maintainer review:
   │   ├─ Self-containment compliance
   │   ├─ Progressive disclosure format
   │   ├─ Content quality and accuracy
   │   ├─ Example practicality
   │   └─ Category/toolchain appropriateness
   ├─ Feedback provided via PR comments
   └─ Contributor addresses feedback

7. MERGE
   ├─ All checks pass (CI + manual review)
   ├─ Maintainer approval (@bobmatnyc)
   ├─ PR merged (squash recommended)
   ├─ Branch auto-deleted
   └─ Issue closed (if linked)

8. DEPLOY
   ├─ Skill available in main branch
   ├─ Contributors can deploy via Claude Code
   └─ Added to skill catalog in README.md
```

---

### 4.2 Quality Gates

Every skill PR must pass these gates:

#### **Gate 1: Automated Validation (CI)**
- ✅ SKILL.md exists
- ✅ metadata.json exists and is valid JSON
- ✅ manifest.json syntax valid
- ✅ No sensitive data detected (secrets, API keys)

**Implementation:** `.github/workflows/validate-skills.yml` (already exists)

**Enhancement Recommendations:**
```yaml
# Add to existing validate-skills.yml

- name: Validate progressive disclosure format
  run: |
    # Check entry point token count (approx < 300 characters = 50 tokens)
    for skill in $(find toolchains/ universal/ -name "SKILL.md"); do
      entry=$(sed -n '/^#/,/^##/p' "$skill" | head -n -1)
      char_count=$(echo "$entry" | wc -c)
      if [ $char_count -gt 300 ]; then
        echo "⚠️  $skill entry point may exceed 50 tokens ($char_count chars)"
      fi
    done

- name: Check self-containment
  run: |
    # Detect relative path references to other skills
    if grep -r "\\.\\.\\/.*SKILL\\.md\\|\\.\\/.*SKILL\\.md" toolchains/ universal/ --include="*.md"; then
      echo "❌ Found relative path references to other skills"
      exit 1
    fi
    echo "✅ No cross-skill references detected"

- name: Validate metadata schema
  run: |
    # Check required fields in metadata.json
    python3 << 'EOF'
    import json, sys
    from pathlib import Path

    required_fields = ["name", "version", "category", "toolchain", "description", "tags", "author", "updated"]

    for meta_file in Path(".").rglob("metadata.json"):
        with open(meta_file) as f:
            data = json.load(f)

        missing = [f for f in required_fields if f not in data]
        if missing:
            print(f"❌ {meta_file} missing: {missing}")
            sys.exit(1)

        # Validate version format
        if not data["version"].count(".") == 2:
            print(f"❌ {meta_file} invalid version format (must be X.Y.Z)")
            sys.exit(1)

        # Validate dependencies is array
        if "dependencies" in data and not isinstance(data["dependencies"], list):
            print(f"❌ {meta_file} dependencies must be array")
            sys.exit(1)

    print("✅ All metadata.json files valid")
    EOF
```

---

#### **Gate 2: Self-Containment Review (Manual)**

Maintainer verifies:
- [ ] Zero relative paths to other skills
- [ ] Works in flat directory (no parent directory assumptions)
- [ ] Essential content inlined (not just referenced)
- [ ] No skill dependencies in metadata.json
- [ ] Examples are complete and self-explanatory

**Tool:** [SKILL_CREATION_PR_CHECKLIST.md](docs/SKILL_CREATION_PR_CHECKLIST.md) (already exists)

---

#### **Gate 3: Content Quality Review (Manual)**

Maintainer evaluates:
- [ ] Progressive disclosure format followed (Tier 1 + Tier 2)
- [ ] Entry point is concise (30-50 tokens)
- [ ] Full documentation is comprehensive
- [ ] Examples are practical and tested
- [ ] Best practices reflect 2025 patterns
- [ ] No misleading or outdated information
- [ ] Category and toolchain are appropriate

---

#### **Gate 4: Integration Review (Manual)**

Maintainer checks:
- [ ] manifest.json updated correctly
- [ ] No duplicate skills exist
- [ ] Complements (not competes with) existing skills
- [ ] Tags are descriptive and consistent with taxonomy

---

### 4.3 Rejection Criteria

PRs may be rejected if:

❌ **Self-containment violations**
- Relies on other skills via relative paths
- Assumes specific directory structure
- References external skills without inlining

❌ **Quality issues**
- Entry point exceeds 50 tokens
- Missing examples or incomplete documentation
- Outdated patterns or anti-patterns
- Inaccurate technical information

❌ **Policy violations**
- Contains sensitive data (API keys, credentials)
- Violates Code of Conduct
- Duplicate of existing skill without justification
- Out of scope for repository

❌ **Format violations**
- Missing SKILL.md or metadata.json
- Invalid JSON in metadata or manifest
- Doesn't follow progressive disclosure structure

**Feedback Process:**
1. Maintainer comments on specific violations
2. Labels PR: `status: needs-info`
3. Contributor addresses feedback
4. Re-review cycle begins

---

## 5. Issue Template Categories (Summary)

### 5.1 Primary Templates

| Template | Purpose | Auto-Labels | Priority |
|----------|---------|-------------|----------|
| **Bug Report** | Broken skills, deployment issues | `bug`, `triage` | HIGH |
| **Feature Request** | Enhancements to existing skills/repo | `enhancement`, `triage` | MEDIUM |
| **New Skill Proposal** | Structured skill submissions | `new-skill`, `triage` | HIGH |

### 5.2 Contact Links (config.yml)

- **Discussions:** General questions, community feedback
- **Documentation:** Link to CONTRIBUTING.md
- **Self-Containment Standard:** Pre-submission reading

### 5.3 Template Usage Guidelines

**When to Use Each Template:**

**Bug Report:**
- Skill fails to load in Claude Code
- Broken links or references
- Validation errors in CI
- Manifest inconsistencies
- Documentation errors

**Feature Request:**
- Enhancement to existing skill
- New documentation section
- Repository tooling improvement
- CI/CD enhancement
- Better organization

**New Skill Proposal:**
- Proposing completely new skill
- Major addition to existing skill area
- Unsure if skill is needed (seeking feedback)
- Want maintainer input before implementing

**Discussions:**
- "How do I...?" questions
- Brainstorming new features
- General community feedback
- Showcase projects using skills

---

## 6. Comparison with Current State

### 6.1 What Exists (Strong Foundation)

✅ **CONTRIBUTING.md**
- Comprehensive guidelines
- Self-containment standard reference
- Clear submission process
- Testing requirements
- Progressive disclosure format

✅ **Pull Request Template**
- Checklist-based validation
- Skill metadata capture
- Self-containment verification
- Testing confirmation

✅ **CODEOWNERS**
- Ensures @bobmatnyc reviews all changes
- Protects critical files (manifest.json, .github/)

✅ **CI Validation Workflow**
- Validates skill structure
- Checks manifest.json syntax
- Detects sensitive data

✅ **LICENSE (MIT)**
- Clear, permissive open source license

---

### 6.2 What's Missing (Gaps)

❌ **CODE_OF_CONDUCT.md** (HIGH PRIORITY)
- Required for GitHub Community Standards
- Sets behavior expectations
- Signals professional environment

❌ **SECURITY.md** (MEDIUM PRIORITY)
- Provides vulnerability reporting channel
- Industry best practice
- Populates Security tab

❌ **Structured Issue Templates** (HIGH PRIORITY)
- YAML-based forms for consistent data collection
- New Skill Proposal template (critical for workflow)
- Bug Report and Feature Request templates
- config.yml for template chooser

❌ **Comprehensive Label Taxonomy** (MEDIUM PRIORITY)
- Priority, status, type, skill category labels
- Effort estimation labels
- Community-friendly labels (good first issue, help wanted)

❌ **Branch Protection Rules** (MEDIUM PRIORITY)
- Require PR reviews before merging
- Require status checks to pass
- Prevent force pushes and deletions

❌ **GitHub Discussions** (LOW PRIORITY)
- Optional but useful for Q&A
- Reduces noise in Issues

---

## 7. Implementation Roadmap

### Phase 1: Critical Files (Week 1)

**Priority: HIGH**

1. **Add CODE_OF_CONDUCT.md**
   - Adopt Contributor Covenant v2.1
   - Place in repository root
   - Link from README.md

2. **Create Issue Templates**
   - `.github/ISSUE_TEMPLATE/bug_report.yml`
   - `.github/ISSUE_TEMPLATE/feature_request.yml`
   - `.github/ISSUE_TEMPLATE/new_skill_proposal.yml`
   - `.github/ISSUE_TEMPLATE/config.yml`

3. **Add SECURITY.md**
   - Customize template for skill repository
   - Define vulnerability reporting process
   - Place in repository root

4. **Enhance PR Template**
   - Add self-containment verification commands
   - Add flat directory test requirement
   - Strengthen manifest update reminder

**Deliverables:**
- 4 new files
- 1 updated file
- GitHub Community Standards badge

---

### Phase 2: Repository Configuration (Week 2)

**Priority: MEDIUM**

1. **Set Up Branch Protection**
   - Enable for `main` branch
   - Require 1 approval
   - Require status checks (validate workflow)
   - Require conversation resolution

2. **Create Label Taxonomy**
   - Import labels via GitHub API or manual creation
   - Document label usage in CONTRIBUTING.md
   - Apply initial labels to existing issues

3. **Enable Repository Features**
   - Enable GitHub Discussions
   - Enable secret scanning alerts
   - Enable private vulnerability reporting
   - Configure auto-delete head branches

**Deliverables:**
- Branch protection rules configured
- 40+ labels created and documented
- Enhanced security features enabled

---

### Phase 3: Enhanced Validation (Week 3)

**Priority: MEDIUM**

1. **Enhance CI Validation**
   - Add progressive disclosure token check
   - Add self-containment path scanning
   - Add metadata.json schema validation
   - Add manifest.json consistency check

2. **Create Contribution Guide Improvements**
   - Add "New Contributor Quick Start" section
   - Create visual workflow diagram
   - Add troubleshooting section
   - Link to issue templates

**Deliverables:**
- Enhanced CI workflow
- Improved contributor documentation
- Faster PR review cycle

---

### Phase 4: Community Building (Ongoing)

**Priority: LOW**

1. **Promote Contribution**
   - Tag issues with `good first issue`
   - Tag issues with `help wanted`
   - Create GitHub Discussions for Q&A
   - Write contributor spotlight in README

2. **Governance Documentation**
   - Add GOVERNANCE.md (decision-making process)
   - Document maintainer responsibilities
   - Define escalation paths

**Deliverables:**
- Active community engagement
- Transparent governance
- Growing contributor base

---

## 8. Evidence and Best Practices

### 8.1 Similar Successful Repositories

**Analyzed Projects:**

1. **Anthropic skills repository** (`anthropics/skills`)
   - Status: Educational/reference repository
   - Community files: Minimal (README, LICENSE, .gitignore)
   - Observation: Positioned as example collection, not active collaboration platform
   - Lesson: claude-mpm-skills aims for MORE community engagement

2. **Creative Commons Open Source**
   - Label taxonomy: Comprehensive emoji-prefixed system
   - Mandatory categories: Priority, Status, Goal, Aspect
   - Lesson: Structured labeling enables efficient triage

3. **Contributor Covenant**
   - CODE_OF_CONDUCT.md: Industry-standard template
   - Adopted by 100,000+ open source projects
   - Lesson: Use proven, tested templates

4. **OSSF oss-vulnerability-guide**
   - SECURITY.md: Comprehensive vulnerability disclosure templates
   - Coordinated disclosure process
   - Lesson: Even low-risk projects benefit from security policy

---

### 8.2 GitHub Official Documentation

**Key Findings:**

1. **Community Health Files** (GitHub Docs)
   - Supported files: CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, SUPPORT, FUNDING, GOVERNANCE
   - Default locations: Root, `.github/`, `docs/`
   - License limitation: Cannot be created as defaults (must be per-repo)

2. **Issue Forms Syntax** (GitHub Docs)
   - YAML-based templates > Markdown templates
   - Form elements: markdown, input, textarea, dropdown, checkboxes
   - Validation: Required fields, type enforcement
   - Benefits: Structured data, better UX, easier triage

3. **Branch Protection** (GitHub Docs)
   - Required for production repositories
   - Prevents force pushes, accidental deletions
   - Enforces review process
   - Requires passing CI checks

---

### 8.3 Industry Best Practices (2025)

**From Research:**

1. **Label Taxonomy**
   - Use prefixes for filtering (`priority:`, `type:`, `status:`)
   - Consistent colors within categories
   - Avoid over-labeling (reduces signal-to-noise)

2. **Issue Templates**
   - Mandatory fields for critical information
   - Markdown instructions for guidance
   - Dropdowns for controlled vocabulary
   - Checkboxes for acknowledgments (Code of Conduct)

3. **Contribution Workflow**
   - Proposal-first for large contributions
   - Lightweight for small fixes
   - Automated validation reduces review burden
   - Clear acceptance criteria in issues

4. **Security**
   - Secret scanning alerts (detects leaked credentials)
   - Private vulnerability reporting
   - Coordinated disclosure process
   - Safe harbor for researchers

---

## 9. Recommended File Templates

### 9.1 CODE_OF_CONDUCT.md

**Source:** Contributor Covenant v2.1
**Location:** `/CODE_OF_CONDUCT.md`

```markdown
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, caste, color, religion, or sexual
identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the overall
  community

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or advances of
  any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email address,
  without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at
[INSERT CONTACT EMAIL].
All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Enforcement Guidelines

Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:

### 1. Correction

**Community Impact**: Use of inappropriate language or other behavior deemed
unprofessional or unwelcome in the community.

**Consequence**: A private, written warning from community leaders, providing
clarity around the nature of the violation and an explanation of why the
behavior was inappropriate. A public apology may be requested.

### 2. Warning

**Community Impact**: A violation through a single incident or series of
actions.

**Consequence**: A warning with consequences for continued behavior. No
interaction with the people involved, including unsolicited interaction with
those enforcing the Code of Conduct, for a specified period of time. This
includes avoiding interactions in community spaces as well as external channels
like social media. Violating these terms may lead to a temporary or permanent
ban.

### 3. Temporary Ban

**Community Impact**: A serious violation of community standards, including
sustained inappropriate behavior.

**Consequence**: A temporary ban from any sort of interaction or public
communication with the community for a specified period of time. No public or
private interaction with the people involved, including unsolicited interaction
with those enforcing the Code of Conduct, is allowed during this period.
Violating these terms may lead to a permanent ban.

### 4. Permanent Ban

**Community Impact**: Demonstrating a pattern of violation of community
standards, including sustained inappropriate behavior, harassment of an
individual, or aggression toward or disparagement of classes of individuals.

**Consequence**: A permanent ban from any sort of public interaction within the
community.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.1, available at
[https://www.contributor-covenant.org/version/2/1/code_of_conduct.html][v2.1].

Community Impact Guidelines were inspired by
[Mozilla's code of conduct enforcement ladder][Mozilla CoC].

For answers to common questions about this code of conduct, see the FAQ at
[https://www.contributor-covenant.org/faq][FAQ]. Translations are available at
[https://www.contributor-covenant.org/translations][translations].

[homepage]: https://www.contributor-covenant.org
[v2.1]: https://www.contributor-covenant.org/version/2/1/code_of_conduct.html
[Mozilla CoC]: https://github.com/mozilla/diversity
[FAQ]: https://www.contributor-covenant.org/faq
[translations]: https://www.contributor-covenant.org/translations
```

**Customization Required:**
- Replace `[INSERT CONTACT EMAIL]` with maintainer contact (e.g., GitHub username or email)

---

### 9.2 SECURITY.md

**Location:** `/SECURITY.md`

```markdown
# Security Policy

## Supported Versions

We actively maintain the following versions of the claude-mpm-skills repository:

| Version | Supported          |
| ------- | ------------------ |
| Latest (main branch) | ✅ |
| Older releases | ❌ |

We recommend always using skills from the `main` branch for the latest updates and security improvements.

## What Qualifies as a Security Vulnerability?

Given that this repository contains **skill instructions** (not executable code), security concerns are different from traditional software projects. We consider the following as security issues:

### High Severity
- **Credential Leakage**: API keys, tokens, passwords, or other secrets in skill examples
- **Malicious Content**: Skills designed to extract user data or perform harmful operations
- **Social Engineering**: Skills that trick users into revealing sensitive information
- **Command Injection**: Examples that demonstrate unsafe command execution patterns

### Medium Severity
- **Insecure Patterns**: Skills promoting deprecated or vulnerable practices
- **Misleading Examples**: Code samples with known security flaws presented without warnings
- **Dependency Vulnerabilities**: Skills referencing libraries with known CVEs without mitigation guidance

### Low Severity
- **Outdated Security Practices**: Skills using older but not critically insecure patterns
- **Missing Security Warnings**: Skills involving sensitive operations without proper cautions

## Reporting a Vulnerability

**DO NOT** create a public issue for security vulnerabilities.

### Preferred Reporting Methods

1. **GitHub Private Vulnerability Reporting** (Recommended)
   - Navigate to the Security tab
   - Click "Report a vulnerability"
   - Provide details using the form

2. **Direct Email** (Alternative)
   - Send to: [INSERT MAINTAINER EMAIL]
   - Subject: "[SECURITY] claude-mpm-skills vulnerability"
   - Include:
     - Affected skill name and path
     - Description of the vulnerability
     - Potential impact
     - Steps to reproduce (if applicable)
     - Suggested remediation (optional)

### What to Include in Your Report

Please provide as much information as possible:

- **Affected Skill**: Name and file path (e.g., `toolchains/python/frameworks/fastapi-local-dev`)
- **Vulnerability Type**: Credential leak, malicious pattern, insecure practice, etc.
- **Description**: Clear explanation of the security concern
- **Impact**: Who is affected and how severe is the risk?
- **Evidence**: Code snippets, screenshots, or examples demonstrating the issue
- **Suggested Fix**: How to remediate (if you have ideas)

### Response Timeline

We are committed to addressing security issues promptly:

| Stage | Timeline |
|-------|----------|
| **Initial Response** | Within 48 hours |
| **Vulnerability Assessment** | Within 7 days |
| **Remediation Plan** | Within 14 days (for confirmed issues) |
| **Fix Implementation** | Depends on severity (critical: 24-48 hours; high: 7 days; medium: 30 days) |
| **Public Disclosure** | After fix is deployed (coordinated with reporter) |

## Disclosure Policy

We practice **coordinated disclosure**:

1. **Private Reporting**: Reporter submits vulnerability privately
2. **Validation**: We assess and confirm the issue
3. **Fix Development**: We develop and test a remediation
4. **Private Notification**: We notify the reporter before public disclosure
5. **Public Release**: We publish the fix and advisory simultaneously
6. **Credit**: We acknowledge the reporter (if desired) in commit messages and release notes

### Safe Harbor

We support security research conducted in good faith:

- We will not pursue legal action against reporters who:
  - Follow this disclosure policy
  - Avoid privacy violations and data destruction
  - Do not exploit vulnerabilities beyond demonstration

- We welcome responsible disclosure and will:
  - Acknowledge your contribution
  - Work with you on remediation
  - Credit you in our security acknowledgments (if desired)

## Security Best Practices for Contributors

When contributing skills, please:

- ✅ **Never include real credentials**: Use placeholders like `YOUR_API_KEY`, `{API_TOKEN}`, or `<INSERT_SECRET>`
- ✅ **Review examples for security flaws**: Ensure code samples follow current security best practices
- ✅ **Add security warnings**: Note potential risks in skills involving authentication, data access, or system commands
- ✅ **Use environment variables**: Demonstrate proper secret management (`.env` files, environment variables)
- ✅ **Validate inputs**: Show examples of input sanitization and validation
- ✅ **Follow least privilege**: Examples should demonstrate minimal necessary permissions

### Automated Protections

Our CI/CD pipeline includes:

- **Secret Scanning**: Detects common credential patterns (API keys, tokens, passwords)
- **Content Validation**: Checks for dangerous patterns or malicious content
- **Manifest Verification**: Ensures consistency and prevents injection attacks

## Security Acknowledgments

We thank the following individuals for responsibly disclosing security issues:

<!-- This section will be updated as vulnerabilities are reported and fixed -->

*No security issues have been reported to date.*

---

**Last Updated:** 2025-11-30
**Contact:** @bobmatnyc (GitHub) | [INSERT EMAIL]
```

**Customization Required:**
- Replace `[INSERT MAINTAINER EMAIL]` with actual contact
- Update "Last Updated" date
- Enable GitHub Private Vulnerability Reporting in repository settings

---

## 10. Actionable Recommendations

### 10.1 Immediate Actions (This Week)

**Priority: CRITICAL**

1. **Create CODE_OF_CONDUCT.md**
   - Adopt Contributor Covenant v2.1 template
   - Customize enforcement contact
   - Commit to repository root
   - Link from README.md

2. **Create Issue Templates**
   - Create `.github/ISSUE_TEMPLATE/` directory
   - Add `bug_report.yml`, `feature_request.yml`, `new_skill_proposal.yml`, `config.yml`
   - Test template chooser

3. **Create SECURITY.md**
   - Use template from section 9.2
   - Customize for skill repository context
   - Enable private vulnerability reporting in GitHub settings

4. **Enhance Pull Request Template**
   - Add self-containment verification commands
   - Add flat directory test requirement
   - Strengthen checklist items

**Expected Outcome:**
- GitHub Community Standards badge
- Professional appearance to external contributors
- Structured contribution intake

---

### 10.2 Short-Term Actions (Next 2 Weeks)

**Priority: HIGH**

1. **Configure Branch Protection**
   - Enable for `main` branch
   - Require 1 approval from @bobmatnyc
   - Require `validate` status check to pass
   - Require conversation resolution before merge

2. **Create Label Taxonomy**
   - Create priority, status, type, skill, effort, community labels
   - Document label usage in CONTRIBUTING.md
   - Apply labels to existing issues

3. **Enhance CI Validation**
   - Add progressive disclosure token check
   - Add self-containment path scanning
   - Add metadata.json schema validation

4. **Enable GitHub Discussions**
   - Create Q&A category
   - Create Ideas category
   - Create Show and Tell category
   - Link from README and issue templates

**Expected Outcome:**
- Protected main branch
- Consistent issue labeling
- Stronger quality gates
- Reduced noise in Issues

---

### 10.3 Long-Term Actions (Next Month)

**Priority: MEDIUM**

1. **Community Building**
   - Tag good first issues
   - Create contributor spotlight in README
   - Write "New Contributor Guide"
   - Promote repository in Claude Code communities

2. **Governance Documentation**
   - Add GOVERNANCE.md (decision-making process)
   - Document maintainer responsibilities
   - Define skill deprecation process

3. **Advanced Automation**
   - Auto-label issues based on keywords
   - Auto-assign reviewers based on skill category
   - Auto-close stale issues/PRs
   - Monthly contributor digest

**Expected Outcome:**
- Growing contributor base
- Transparent governance
- Reduced manual triage burden
- Active, engaged community

---

## 11. Success Metrics

Track these KPIs to measure community health improvements:

### 11.1 Contribution Metrics

| Metric | Current | 3 Months | 6 Months |
|--------|---------|----------|----------|
| External contributors | TBD | 5+ | 15+ |
| Skills from community | TBD | 3+ | 10+ |
| Average PR review time | TBD | < 3 days | < 2 days |
| Closed issues per month | TBD | 10+ | 20+ |

### 11.2 Quality Metrics

| Metric | Current | 3 Months | 6 Months |
|--------|---------|----------|----------|
| CI failure rate | TBD | < 10% | < 5% |
| Self-containment violations | TBD | 0% | 0% |
| Security issues detected | 0 | 0 | 0 |
| Stale PRs (>30 days) | TBD | < 5% | < 2% |

### 11.3 Community Health Metrics

| Metric | Current | 3 Months | 6 Months |
|--------|---------|----------|----------|
| GitHub Community Standards | 60% | 100% | 100% |
| Response time to issues | TBD | < 48h | < 24h |
| First-time contributor PRs | TBD | 2+ | 5+ |
| Active discussions threads | 0 | 5+ | 15+ |

---

## 12. Conclusion

The `claude-mpm-skills` repository has a **strong foundation** with excellent documentation (CONTRIBUTING.md), validation workflow, and PR template. To become a fully contributor-friendly open source project, it requires:

### Critical Additions:
1. ✅ CODE_OF_CONDUCT.md (GitHub Community Standard)
2. ✅ SECURITY.md (Security best practice)
3. ✅ YAML-based issue templates (Structured intake)
4. ✅ New Skill Proposal template (Critical workflow)

### Important Enhancements:
1. ⚠️ Branch protection rules (Quality gate)
2. ⚠️ Comprehensive label taxonomy (Efficient triage)
3. ⚠️ Enhanced CI validation (Self-containment checks)
4. ⚠️ GitHub Discussions (Community Q&A)

### Long-Term Investments:
1. 📋 Community building initiatives
2. 📋 Governance documentation
3. 📋 Advanced automation
4. 📋 Contributor recognition

**Estimated Effort:**
- Phase 1 (Critical Files): 4-6 hours
- Phase 2 (Configuration): 3-4 hours
- Phase 3 (Enhanced Validation): 4-6 hours
- Phase 4 (Community Building): Ongoing

**Expected Impact:**
- **Increased contributions** from external developers
- **Higher quality** skills through structured intake
- **Reduced maintenance burden** via automation
- **Professional reputation** as well-governed open source project

By implementing these recommendations, `claude-mpm-skills` will be positioned as a **model open source skill repository** with industry-standard community health practices, clear contribution workflows, and strong quality gates.

---

## Appendix A: File Checklist

### Files to Create

- [ ] `/CODE_OF_CONDUCT.md`
- [ ] `/SECURITY.md`
- [ ] `/.github/ISSUE_TEMPLATE/bug_report.yml`
- [ ] `/.github/ISSUE_TEMPLATE/feature_request.yml`
- [ ] `/.github/ISSUE_TEMPLATE/new_skill_proposal.yml`
- [ ] `/.github/ISSUE_TEMPLATE/config.yml`

### Files to Enhance

- [ ] `/.github/pull_request_template.md` (add self-containment commands)
- [ ] `/CONTRIBUTING.md` (link to issue templates, add new contributor guide)
- [ ] `/.github/workflows/validate-skills.yml` (add advanced checks)
- [ ] `/README.md` (link to CODE_OF_CONDUCT.md, update badges)

### Repository Settings to Configure

- [ ] Branch protection rules for `main`
- [ ] Enable GitHub Discussions
- [ ] Enable secret scanning alerts
- [ ] Enable private vulnerability reporting
- [ ] Auto-delete head branches
- [ ] Create label taxonomy (40+ labels)

---

## Appendix B: Label Creation Script

```bash
#!/bin/bash
# GitHub label creation script for claude-mpm-skills
# Run from repository root: bash create_labels.sh

# Priority Labels
gh label create "🟥 priority: critical" --color b60205 --description "Must be fixed ASAP"
gh label create "🟧 priority: high" --color d93f0b --description "Blocks dependent work"
gh label create "🟨 priority: medium" --color fbca04 --description "Important but non-blocking"
gh label create "🟩 priority: low" --color cfda2c --description "Nice to have, no rush"

# Status Labels
gh label create "🚦 status: triage" --color eeeeee --description "Needs initial review"
gh label create "🔍 status: needs-info" --color d4c5f9 --description "Awaiting information"
gh label create "🚧 status: blocked" --color 333333 --description "Cannot proceed"
gh label create "🏁 status: ready" --color 0e8a16 --description "Ready for implementation"
gh label create "👀 status: in-review" --color fbca04 --description "Under active review"
gh label create "⛔ status: wontfix" --color ffffff --description "Rejected/out of scope"
gh label create "✅ status: done" --color 1d76db --description "Completed"

# Type Labels
gh label create "🐛 type: bug" --color d73a4a --description "Something isn't working"
gh label create "✨ type: enhancement" --color a2eeef --description "Improvement to existing feature"
gh label create "🚀 type: new-skill" --color 0075ca --description "Proposal for new skill"
gh label create "📖 type: documentation" --color 0075ca --description "Documentation improvements"
gh label create "🔧 type: tooling" --color d4c5f9 --description "CI/CD, scripts, automation"
gh label create "💬 type: question" --color d876e3 --description "User question"
gh label create "🎨 type: design" --color e99695 --description "UI/UX, repository structure"

# Skill Category Labels
gh label create "skill: python" --color 3572A5 --description "Python skills"
gh label create "skill: typescript" --color 2b7489 --description "TypeScript skills"
gh label create "skill: javascript" --color f1e05a --description "JavaScript skills"
gh label create "skill: nextjs" --color 000000 --description "Next.js skills"
gh label create "skill: ui" --color 563d7c --description "UI/styling skills"
gh label create "skill: ai" --color ff6f00 --description "AI/ML skills"
gh label create "skill: platform" --color 89e051 --description "Platform/deployment"
gh label create "skill: universal" --color ededed --description "Universal skills"

# Effort Labels
gh label create "effort: small" --color c2e0c6 --description "< 2 hours of work"
gh label create "effort: medium" --color fef2c0 --description "2-8 hours of work"
gh label create "effort: large" --color f9d0c4 --description "1-3 days of work"
gh label create "effort: epic" --color d93f0b --description "Multi-day or requires research"

# Community Labels
gh label create "good first issue" --color 7057ff --description "Good for newcomers"
gh label create "help wanted" --color 008672 --description "Maintainer requests community help"
gh label create "🔒 staff only" --color d73a4a --description "Requires maintainer privileges"
gh label create "duplicate" --color cfd3d7 --description "Duplicate of another issue"
gh label create "invalid" --color e4e669 --description "Invalid issue"

# Automated Labels
gh label create "🤖 auto: validation-failed" --color b60205 --description "CI validation checks failed"
gh label create "🤖 auto: sensitive-data" --color d73a4a --description "Potential credentials detected"
gh label create "🤖 auto: manifest-error" --color d93f0b --description "manifest.json validation failed"

echo "✅ All labels created successfully!"
```

**Usage:**
```bash
# Install GitHub CLI: https://cli.github.com/
# Authenticate: gh auth login
# Run script: bash create_labels.sh
```

---

## Appendix C: Resources

### GitHub Documentation
- [Community Health Files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [Issue Forms Syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Managing Labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)

### Templates and Examples
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [OSSF Vulnerability Guide](https://github.com/ossf/oss-vulnerability-guide)
- [GitHub Issue Templates Collection](https://github.com/stevemao/github-issue-templates)
- [Creative Commons Label Taxonomy](https://opensource.creativecommons.org/contributing-code/repo-labels/)

### Best Practices Articles
- [10up Open Source Best Practices](https://10up.github.io/Open-Source-Best-Practices/community/)
- [GitHub Security Best Practices](https://www.legitsecurity.com/blog/github-security-best-practices-your-team-should-be-following)
- [Mastering GitHub Issues](https://gitprotect.io/blog/mastering-github-issues-best-practices-and-pro-tips/)

---

**Research Completed:** 2025-11-30
**Next Steps:** Review findings → Implement Phase 1 (Critical Files) → Configure repository settings → Enable community features
