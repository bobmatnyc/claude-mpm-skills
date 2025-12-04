# GitHub Repository Setup for Public Contributions

**Last Updated:** 2025-11-30
**Repository:** claude-mpm-skills
**Maintainer:** @bobmatnyc

## Table of Contents

- [1. Overview](#1-overview)
- [2. General Settings](#2-general-settings)
- [3. Branch Protection Rules](#3-branch-protection-rules)
- [4. Security Settings](#4-security-settings)
- [5. GitHub Actions Settings](#5-github-actions-settings)
- [6. Issue and PR Settings](#6-issue-and-pr-settings)
- [7. Discussions Settings](#7-discussions-settings)
- [8. Labels Setup](#8-labels-setup)
- [9. Collaborators and Teams](#9-collaborators-and-teams)
- [10. Repository Insights](#10-repository-insights)
- [11. Pre-Launch Checklist](#11-pre-launch-checklist)
- [12. Post-Launch Monitoring](#12-post-launch-monitoring)
- [13. Automated CI Workflows](#13-automated-ci-workflows)
- [Appendix A: Label Creation Script](#appendix-a-label-creation-script)
- [Appendix B: Troubleshooting](#appendix-b-troubleshooting)

---

## 1. Overview

### Purpose of This Document

This guide provides step-by-step instructions to configure the `claude-mpm-skills` repository for safe, high-quality public contributions. These settings enable:

- **Quality Control**: Branch protection and required reviews prevent broken code from merging
- **Automated Validation**: CI workflows enforce skill self-containment standards
- **Community Safety**: Security policies and code of conduct protect contributors
- **Efficient Triage**: Label taxonomy and issue templates streamline issue management
- **Contributor Experience**: Clear templates and guidelines reduce friction

### When to Apply These Settings

**Before making the repository public** or accepting external contributions. This prevents:
- Direct commits to `main` branch
- Merging of malformed skills or sensitive data
- Unclear contribution expectations
- Security vulnerabilities being publicly disclosed

### How to Access Repository Settings

1. Navigate to `https://github.com/OWNER/claude-mpm-skills`
2. Click **Settings** tab (requires admin/owner permissions)
3. Follow section-specific instructions below

**Note:** Some settings require repository admin or owner permissions.

---

## 2. General Settings

Navigate to: **Settings → General**

### Repository Details

**Description:**
```
Production-ready Claude Code skills for intelligent project development
```

**Website:**
```
https://github.com/OWNER/claude-mpm-skills#readme
```
(Update with documentation site URL if available)

**Topics/Tags:**

Add the following topics for discoverability:
```
claude-code
claude
anthropic
skills
ai-development
development-tools
project-management
automation
typescript
python
nextjs
ai-workflows
code-generation
developer-productivity
mcp-servers
```

**How to add:**
1. Click "⚙️" next to "About" section on repository homepage
2. Add topics in "Topics" field (comma-separated)
3. Click "Save changes"

### Features to Enable

| Feature | Enable? | Rationale |
|---------|---------|-----------|
| **Issues** | ✅ Yes | Primary contribution and bug tracking channel |
| **Discussions** | ✅ Yes | Q&A, skill proposals, community feedback |
| **Projects** | ⚠️ Optional | Useful for roadmap tracking (recommend enabling) |
| **Wiki** | ❌ No | Use `/docs/` directory instead for version control |
| **Sponsorships** | ⚠️ Optional | Enable if `FUNDING.yml` is created |
| **Preserve this repository** | ✅ Yes | Arctic Code Vault archival |

**Configuration Steps:**
1. Go to **Settings → General → Features**
2. Check/uncheck boxes according to table above
3. Scroll down and click **Save**

---

## 3. Branch Protection Rules for `main`

Navigate to: **Settings → Branches → Add branch protection rule**

### Required Configuration

**Branch name pattern:**
```
main
```

### Pull Request Requirements

#### ✅ Require a pull request before merging
- **✅ Require approvals:** `1`
  - **Rationale:** Single maintainer workflow, ensures code review
- **✅ Dismiss stale pull request approvals when new commits are pushed**
  - **Rationale:** Prevents outdated approvals after significant changes
- **✅ Require review from Code Owners**
  - **Rationale:** `.github/CODEOWNERS` exists and routes to @bobmatnyc
- **❌ Require approval of the most recent reviewable push**
  - **Rationale:** Optional - adds extra review burden for small changes

#### ✅ Require status checks to pass before merging
- **✅ Require branches to be up to date before merging**
  - **Rationale:** Prevents merge conflicts and ensures latest code tested
- **Status checks that are required:**
  - ✅ `validate / validate` (from `.github/workflows/validate-skills.yml`)

**How to add required checks:**
1. After enabling "Require status checks", a search box appears
2. Type `validate` and select `validate / validate`
3. If not visible, ensure the workflow has run at least once on a PR

#### ✅ Require conversation resolution before merging
- **Rationale:** All review comments must be addressed before merge

#### ⚠️ Require signed commits (Optional - Recommended)
- **Rationale:** Increases security, verifies commit authorship
- **Trade-off:** Adds setup burden for new contributors
- **Recommendation:** Enable if security is paramount, otherwise skip initially

#### ❌ Require linear history
- **Rationale:** Too strict for open source - requires rebasing knowledge
- **Recommendation:** **Disabled** for contributor friendliness

#### ❌ Require deployments to succeed before merging
- **Rationale:** N/A for skill library (no deployment process)

### Enforcement Settings

#### ✅ Do not allow bypassing the above settings
- **Rationale:** Applies rules to administrators (prevents accidental direct commits)

#### ⚠️ Restrict who can push to matching branches
- **Options:**
  - Enable and add only `@bobmatnyc` (strict control)
  - Disable (allow trusted collaborators to push)
- **Recommendation:** Enable for single-maintainer workflow

#### ❌ Allow force pushes
- **Rationale:** Never enable - protects commit history

#### ❌ Allow deletions
- **Rationale:** Never enable - prevents accidental branch deletion

### Summary Configuration

```yaml
Branch name pattern: main

Pull Request Settings:
  ✅ Require pull request reviews (1 approval)
  ✅ Dismiss stale reviews
  ✅ Require Code Owners review

Status Checks:
  ✅ Require status checks to pass
  ✅ Require branches to be up to date
  Required checks:
    - validate / validate

Other Requirements:
  ✅ Require conversation resolution
  ⚠️ Require signed commits (optional)
  ❌ Require linear history

Enforcement:
  ✅ Do not allow bypassing
  ⚠️ Restrict who can push (recommended)
  ❌ Allow force pushes
  ❌ Allow deletions
```

**Save the rule:** Click **Create** or **Save changes** at bottom of page.

---

## 4. Security Settings

Navigate to: **Settings → Security & analysis**

### Recommended Security Features

| Feature | Enable? | Description |
|---------|---------|-------------|
| **Private vulnerability reporting** | ✅ Yes | Allows researchers to privately report security issues |
| **Dependency graph** | ✅ Yes | Automatically track dependencies |
| **Dependabot alerts** | ✅ Yes | Get alerts for vulnerabilities in dependencies |
| **Dependabot security updates** | ✅ Yes | Auto-create PRs to update vulnerable dependencies |
| **Dependabot version updates** | ⚠️ Optional | Auto-create PRs for all dependency updates (can be noisy) |
| **Code scanning (CodeQL)** | ⚠️ If available | GitHub Advanced Security - only on Pro/Enterprise plans |
| **Secret scanning** | ✅ Yes | Detect secrets in code (available for public repos) |
| **Secret scanning push protection** | ✅ Yes | Block commits containing secrets |

### Configuration Steps

1. **Private vulnerability reporting:**
   - Click **Enable** next to "Private vulnerability reporting"
   - Ensure `SECURITY.md` exists (see [Pre-Launch Checklist](#11-pre-launch-checklist))

2. **Dependency graph:**
   - Should be enabled by default for public repos
   - If not, click **Enable**

3. **Dependabot alerts:**
   - Click **Enable** if not already active
   - Alerts appear in Security → Dependabot tab

4. **Dependabot security updates:**
   - Click **Enable**
   - Creates PRs automatically when security vulnerabilities found

5. **Secret scanning:**
   - Available by default for public repositories
   - Verify status shows "Enabled"

6. **Secret scanning push protection:**
   - Click **Enable** to block pushes with secrets

### Security Policy

Ensure `SECURITY.md` exists in repository root with vulnerability reporting instructions. See template in [Pre-Launch Checklist](#11-pre-launch-checklist).

---

## 5. GitHub Actions Settings

Navigate to: **Settings → Actions → General**

### Actions Permissions

**Actions permissions:**
```
✅ Allow all actions and reusable workflows
```

**Rationale:** Open source project benefits from community actions. Monitor for malicious actions in PRs.

**Alternative (more restrictive):**
```
⚠️ Allow OWNER, and select non-OWNER, actions and reusable workflows
```
Use if security is paramount.

### Workflow Permissions

**Default workflow permissions:**
```
✅ Read repository contents and packages permissions
```

**Rationale:** Minimal permissions for CI validation workflows.

**Additional permissions:**
```
✅ Allow GitHub Actions to create and approve pull requests
```

**Rationale:** Enables automation like Dependabot PRs.

**Warning:** Do NOT enable write access to repository contents unless absolutely necessary (prevents accidental auto-commits).

### Fork Pull Request Workflows

**Fork pull request workflows from outside collaborators:**
```
✅ Require approval for first-time contributors
```

**Rationale:** Prevents malicious workflows from external contributors.

**Fork pull request workflows from contributors:**
```
✅ Require approval for all outside collaborators
```

**Rationale:** All external PRs reviewed before running workflows.

### Configuration Summary

```yaml
Actions Permissions:
  ✅ Allow all actions and reusable workflows

Workflow Permissions:
  ✅ Read repository contents and packages
  ✅ Allow GitHub Actions to create and approve pull requests
  ❌ Read and write permissions (contents)

Fork Pull Request Workflows:
  ✅ Require approval for first-time contributors
  ✅ Require approval for all outside collaborators
```

**Save:** Scroll down and click **Save**.

---

## 6. Issue and PR Settings

Navigate to: **Settings → General → Features**

### Issue Settings

**Issues:**
```
✅ Enable issues
```

**Issue Templates:**
- ✅ Already created in `.github/ISSUE_TEMPLATE/`:
  - `bug_report.yml` (structured bug reports)
  - `feature_request.yml` (feature suggestions)
  - `new_skill_proposal.yml` (skill contribution workflow)
  - `config.yml` (template chooser configuration)

**No additional configuration needed** - templates auto-detected by GitHub.

### Pull Request Settings

Navigate to: **Settings → General → Pull Requests**

**Merge Button Options:**

| Option | Enable? | Rationale |
|--------|---------|-----------|
| **Allow merge commits** | ✅ Yes | Standard workflow for multi-commit PRs with logical progression |
| **Allow squash merging** | ✅ Yes | Recommended for atomic skill additions - creates clean history |
| **Allow rebase merging** | ⚠️ Optional | Advanced users only - can confuse new contributors |

**Recommendation:** Enable all three, default to **squash merging**.

**How to set default:**
1. Go to **Settings → General → Pull Requests**
2. Under "Allow merge commits", check the box
3. Under "Allow squash merging", check the box (select as default)
4. Under "Allow rebase merging", check if desired

**Additional PR Settings:**

| Setting | Enable? | Rationale |
|---------|---------|-----------|
| **Always suggest updating pull request branches** | ✅ Yes | Prompts contributors to sync with main |
| **Allow auto-merge** | ✅ Yes | Enables PR auto-merge when checks pass |
| **Automatically delete head branches** | ✅ Yes | Keeps repository clean after merge |

**Configuration:**
1. Check **Always suggest updating pull request branches**
2. Check **Allow auto-merge**
3. Check **Automatically delete head branches**
4. Scroll down and click **Save**

---

## 7. Discussions Settings

Navigate to: **Settings → General → Features → Discussions**

### Enable Discussions

1. Check **✅ Discussions** checkbox
2. Click **Set up discussions**

### Create Discussion Categories

GitHub creates default categories. Customize as follows:

| Category | Emoji | Description | Format | Who Can Post |
|----------|-------|-------------|--------|--------------|
| **Announcements** | 📣 | New skill releases, bundle updates | Announcement | Maintainers only |
| **Ideas** | 💡 | Skill proposals and feature requests | Open discussion | Anyone |
| **Q&A** | 🙏 | Questions about using skills | Q&A | Anyone |
| **Show and Tell** | 🎉 | Share your skill implementations | Open discussion | Anyone |
| **General** | 💬 | Everything else | Open discussion | Anyone |

**How to configure:**
1. Go to repository **Discussions** tab
2. Click ⚙️ (settings icon) or "Edit" next to category
3. Modify name, emoji, description per table
4. For **Announcements**: Check "Only maintainers can post"
5. Save each category

### Discussion Templates (Optional)

Create discussion templates in `.github/DISCUSSION_TEMPLATE/`:
```
.github/
└── DISCUSSION_TEMPLATE/
    ├── skill-idea.md
    └── implementation-help.md
```

**Example: `skill-idea.md`**
```markdown
---
title: "[Skill Idea] "
labels: ["type: new-skill"]
---

## Skill Name
<!-- e.g., "PostgreSQL Query Optimization" -->

## Category
<!-- toolchains/python, universal/, etc. -->

## Use Case
<!-- What problem does this skill solve? -->

## Key Features
<!-- What would this skill include? -->
```

---

## 8. Labels Setup

### Label Taxonomy Overview

A comprehensive label system enables efficient issue triage and filtering. Labels are organized into categories:

1. **Priority** (🟥🟧🟨🟩) - Urgency and importance
2. **Status** (🚦🔍🚧🏁👀⛔✅) - Workflow state
3. **Type** (🐛✨🚀📖🔧💬🎨) - Issue classification
4. **Skill Category** (skill:*) - Domain-specific
5. **Effort** (effort:*) - Implementation complexity
6. **Community** (good first issue, help wanted, etc.)
7. **Automated** (🤖 auto:*) - CI/bot-applied

### Label Application Rules

**Every issue must have:**
1. One `priority` label (🟥🟧🟨🟩)
2. One `type` label (🐛✨🚀📖🔧💬🎨)
3. One `status` label (starts with `status: triage`)

**Optional labels:**
- One or more `skill:*` labels
- One `effort:*` label (recommended for tasks)
- Community labels as appropriate

### Creating Labels

**Option 1: Automated Script (Recommended)**

See [Appendix A: Label Creation Script](#appendix-a-label-creation-script) for complete bash script using GitHub CLI.

**Option 2: Manual Creation**

Navigate to: **Issues → Labels → New label**

Create each label with specifications below:

#### Priority Labels (Mandatory)

| Label Name | Color | Description |
|------------|-------|-------------|
| `🟥 priority: critical` | `#b60205` | Must be fixed ASAP - broken core functionality |
| `🟧 priority: high` | `#d93f0b` | Blocks dependent work or affects many users |
| `🟨 priority: medium` | `#fbca04` | Important but non-blocking |
| `🟩 priority: low` | `#cfda2c` | Nice to have, no rush |

#### Status Labels (Workflow)

| Label Name | Color | Description |
|------------|-------|-------------|
| `🚦 status: triage` | `#eeeeee` | Needs initial review and labeling |
| `🔍 status: needs-info` | `#d4c5f9` | Awaiting information from reporter |
| `🚧 status: blocked` | `#333333` | Cannot proceed due to dependency |
| `🏁 status: ready` | `#0e8a16` | Ready for implementation |
| `👀 status: in-review` | `#fbca04` | Under active review |
| `⛔ status: wontfix` | `#ffffff` | Rejected/out of scope |
| `✅ status: done` | `#1d76db` | Completed (before closing) |

#### Type Labels (Classification)

| Label Name | Color | Description |
|------------|-------|-------------|
| `🐛 type: bug` | `#d73a4a` | Something isn't working correctly |
| `✨ type: enhancement` | `#a2eeef` | Improvement to existing feature |
| `🚀 type: new-skill` | `#0075ca` | Proposal for new skill |
| `📖 type: documentation` | `#0075ca` | Documentation improvements |
| `🔧 type: tooling` | `#d4c5f9` | CI/CD, scripts, automation |
| `💬 type: question` | `#d876e3` | User question or clarification |
| `🎨 type: design` | `#e99695` | UI/UX, repository structure |

#### Skill Category Labels

| Label Name | Color | Description |
|------------|-------|-------------|
| `skill: python` | `#3572A5` | Python skills |
| `skill: typescript` | `#2b7489` | TypeScript skills |
| `skill: javascript` | `#f1e05a` | JavaScript skills |
| `skill: nextjs` | `#000000` | Next.js skills |
| `skill: ui` | `#563d7c` | UI/styling skills |
| `skill: ai` | `#ff6f00` | AI/ML skills |
| `skill: platform` | `#89e051` | Platform/deployment skills |
| `skill: universal` | `#ededed` | Universal skills |

#### Effort Labels (Contributor Guidance)

| Label Name | Color | Description |
|------------|-------|-------------|
| `effort: small` | `#c2e0c6` | < 2 hours of work |
| `effort: medium` | `#fef2c0` | 2-8 hours of work |
| `effort: large` | `#f9d0c4` | 1-3 days of work |
| `effort: epic` | `#d93f0b` | Multi-day or requires research |

#### Community Labels

| Label Name | Color | Description |
|------------|-------|-------------|
| `good first issue` | `#7057ff` | Good for newcomers (GitHub recognized) |
| `help wanted` | `#008672` | Maintainer requests community help (GitHub recognized) |
| `🔒 staff only` | `#d73a4a` | Requires maintainer privileges |
| `duplicate` | `#cfd3d7` | Duplicate of another issue |
| `invalid` | `#e4e669` | Invalid issue (spam, off-topic) |

#### Automated Labels (Applied by CI)

| Label Name | Color | Description |
|------------|-------|-------------|
| `🤖 auto: validation-failed` | `#b60205` | CI validation checks failed |
| `🤖 auto: sensitive-data` | `#d73a4a` | Potential credentials detected |
| `🤖 auto: manifest-error` | `#d93f0b` | manifest.json validation failed |

**Total Labels:** 40

---

## 9. Collaborators and Teams

Navigate to: **Settings → Access → Collaborators and teams**

### Recommended Team Structure

| Role | Access Level | Members | Permissions |
|------|--------------|---------|-------------|
| **Maintainers** | Admin | @bobmatnyc | Full repository access, settings, merge |
| **Contributors** | Write | Trusted contributors | Can merge PRs, manage issues |
| **Triage** | Triage | Community moderators | Manage issues/PRs without merging |
| **External** | Read | Public | Fork and submit PRs |

### Adding Collaborators

1. Click **Add people** or **Add teams**
2. Search for GitHub username
3. Select role from dropdown
4. Click **Add**

### Creating Teams (Organization Repos Only)

If repository is under GitHub organization:

1. Go to organization **Teams** page
2. Click **New team**
3. Name: `claude-mpm-maintainers`, `claude-mpm-contributors`, etc.
4. Add team members
5. In repository settings, add team with appropriate role

### Single Maintainer Setup

For @bobmatnyc as sole maintainer:
- No additional collaborators needed initially
- Branch protection ensures all PRs reviewed before merge
- Add trusted contributors over time as community grows

---

## 10. Repository Insights

Navigate to: **Insights → Community**

### Community Health Checklist

Verify all items are checked (✅):

| Item | Status | Location |
|------|--------|----------|
| **Description** | ✅ | Repository settings |
| **README** | ✅ | `README.md` |
| **Code of conduct** | ⚠️ Required | `CODE_OF_CONDUCT.md` |
| **Contributing guidelines** | ✅ | `CONTRIBUTING.md` |
| **License** | ✅ | `LICENSE` |
| **Issue templates** | ✅ | `.github/ISSUE_TEMPLATE/` |
| **Pull request template** | ✅ | `.github/pull_request_template.md` |
| **Security policy** | ⚠️ Required | `SECURITY.md` |

**Missing items must be created before going public.** See [Pre-Launch Checklist](#11-pre-launch-checklist).

### Community Standards Badge

Once all files exist, repository displays **"Community standards: Complete"** badge.

**To verify:**
1. Go to **Insights → Community**
2. Check percentage (target: 100%)
3. Create missing files from checklist

---

## 11. Pre-Launch Checklist

Complete these tasks **before** making repository public or announcing to community:

### Required Files

- [ ] **`CODE_OF_CONDUCT.md`** - Download from [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md)
  - Save to repository root
  - Update contact email to maintainer email

- [ ] **`SECURITY.md`** - Create in repository root:

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

**DO NOT** create a public issue for security vulnerabilities.

Instead, please report security vulnerabilities via GitHub's private vulnerability reporting:

1. Go to the **Security** tab
2. Click **Report a vulnerability**
3. Fill out the form with details

Alternatively, email security concerns to: [MAINTAINER_EMAIL]

We aim to respond within 48 hours and provide a fix within 7 days for critical vulnerabilities.

## Scope

This repository contains Claude Code skills (documentation and configuration). Security concerns include:

- Exposure of API keys or secrets in skill examples
- Malicious code in skill instructions
- Dependency vulnerabilities (if any)
- Social engineering via skill content

## Out of Scope

- Issues with Claude Code itself (report to Anthropic)
- General skill usage questions (use Discussions)
```

### Repository Configuration

- [ ] **Branch protection enabled on `main`** (see [Section 3](#3-branch-protection-rules))
- [ ] **Security features enabled** (see [Section 4](#4-security-settings))
- [ ] **GitHub Actions permissions configured** (see [Section 5](#5-github-actions-settings))
- [ ] **Issue and PR templates tested** (create test issue/PR)
- [ ] **Labels created** (run script from [Appendix A](#appendix-a-label-creation-script))
- [ ] **Repository description and topics set** (see [Section 2](#2-general-settings))
- [ ] **Discussions enabled with categories** (see [Section 7](#7-discussions-settings))

### Documentation Review

- [ ] **`CONTRIBUTING.md` updated** with self-containment standard reference
- [ ] **`README.md` includes badges:**
  ```markdown
  ![GitHub](https://img.shields.io/github/license/OWNER/claude-mpm-skills)
  ![GitHub issues](https://img.shields.io/github/issues/OWNER/claude-mpm-skills)
  ![GitHub stars](https://img.shields.io/github/stars/OWNER/claude-mpm-skills)
  ```
- [ ] **`README.md` includes contribution section** linking to `CONTRIBUTING.md`
- [ ] **All documentation links tested** (no broken links)

### CI/CD Validation

- [ ] **`.github/workflows/validate-skills.yml` tested** (create test PR)
- [ ] **Self-containment validation working** (check for relative paths)
- [ ] **Manifest validation working** (test with invalid JSON)
- [ ] **Sensitive data detection working** (test with fake API key)

### Testing

- [ ] **Create test issue using each template** (verify fields work)
- [ ] **Create test PR using template** (verify checklist appears)
- [ ] **Trigger CI workflow and verify it runs**
- [ ] **Test branch protection** (attempt direct push to main - should fail)
- [ ] **Test required reviews** (verify PR cannot merge without approval)

### Final Verification

- [ ] **Community health at 100%** (check Insights → Community)
- [ ] **All required status checks configured**
- [ ] **CODEOWNERS file present and correct**
- [ ] **Repository visibility set appropriately** (public vs private)

---

## 12. Post-Launch Monitoring

### Week 1 (High Attention Period)

**Daily tasks:**
- [ ] Monitor new issues (are templates being used correctly?)
- [ ] Respond to first-time contributors within 24 hours
- [ ] Watch for CI failures on PRs
- [ ] Check Discussions for questions

**Metrics to track:**
- Number of issues opened
- Issue template compliance rate
- Average time to first response
- PR submission rate
- CI pass/fail rate

### Month 1 (Adjustment Period)

**Weekly tasks:**
- [ ] Review label usage (are labels being applied correctly?)
- [ ] Identify common questions → add to FAQ or documentation
- [ ] Evaluate issue template effectiveness (missing fields?)
- [ ] Monitor community engagement in Discussions
- [ ] Review and merge Dependabot PRs

**Adjust as needed:**
- Refine issue templates if missing critical information
- Add new labels based on emerging patterns
- Update CONTRIBUTING.md with lessons learned
- Create discussion templates for common topics

### Ongoing Maintenance

**Monthly:**
- [ ] Review community health score
- [ ] Audit open issues (close stale issues, update priorities)
- [ ] Update documentation based on contributor feedback
- [ ] Evaluate contributor growth (new vs repeat)
- [ ] Review CI workflow efficiency (reduce run time if possible)

**Quarterly:**
- [ ] Analyze contribution trends (which skills most requested?)
- [ ] Update roadmap based on community input
- [ ] Recognize top contributors (shoutouts in Discussions)
- [ ] Review and update security policy if needed
- [ ] Evaluate label taxonomy (add/remove/rename labels)

**Annually:**
- [ ] Complete documentation audit
- [ ] Update Code of Conduct if needed
- [ ] Review contributor guidelines for clarity
- [ ] Assess repository structure (reorganize if needed)

---

## 13. Automated CI Workflows

### Current Workflow: `validate-skills.yml`

Located at: `.github/workflows/validate-skills.yml`

**Current checks:**
- ✅ Skill structure validation (SKILL.md, metadata.json presence)
- ✅ Manifest validation (JSON syntax)
- ✅ Sensitive data detection (API keys, secrets)

### Recommended Enhancements

#### Enhanced Self-Containment Check

Create: `.github/workflows/self-containment-check.yml`

```yaml
name: Self-Containment Validation

on:
  pull_request:
    paths:
      - 'toolchains/**'
      - 'universal/**'
      - 'frameworks/**'
      - 'bundled/**'

jobs:
  validate-self-containment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for relative path dependencies
        run: |
          echo "🔍 Checking for relative path violations..."

          # Check for relative path imports in SKILL.md files
          VIOLATIONS=$(grep -r "\.\./\|\.\./" --include="SKILL.md" toolchains/ universal/ frameworks/ bundled/ 2>/dev/null || true)

          if [ -n "$VIOLATIONS" ]; then
            echo "❌ Found relative path dependencies:"
            echo "$VIOLATIONS"
            echo ""
            echo "Skills must be self-contained. See docs/SKILL_SELF_CONTAINMENT_STANDARD.md"
            exit 1
          fi

          echo "✅ No relative path dependencies found"

      - name: Check for skill dependencies
        run: |
          echo "🔍 Checking for hard skill dependencies..."

          # Look for phrases indicating dependencies
          DEPS=$(grep -r "requires.*skill\|depends on.*skill\|see.*skill" --include="SKILL.md" toolchains/ universal/ frameworks/ bundled/ 2>/dev/null || true)

          if [ -n "$DEPS" ]; then
            echo "⚠️ Potential skill dependencies found:"
            echo "$DEPS"
            echo ""
            echo "Review these references - skills should be self-contained."
            echo "Use soft references if complementary skills mentioned."
            # Warning only - don't fail build
          fi

      - name: Validate metadata.json
        run: |
          echo "🔍 Validating all metadata.json files..."

          FAILED=0
          for file in $(find toolchains/ universal/ frameworks/ bundled/ -name "metadata.json" 2>/dev/null); do
            echo "Checking $file..."
            if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
              echo "❌ Invalid JSON in $file"
              FAILED=1
            fi
          done

          if [ $FAILED -eq 1 ]; then
            exit 1
          fi

          echo "✅ All metadata.json files valid"

      - name: Check for complete examples
        run: |
          echo "🔍 Checking for code example completeness..."

          # Check for common indicators of incomplete examples
          INCOMPLETE=$(grep -r "# \.\.\.\|// \.\.\.\|truncated\|abbreviated" --include="SKILL.md" toolchains/ universal/ frameworks/ bundled/ 2>/dev/null || true)

          if [ -n "$INCOMPLETE" ]; then
            echo "⚠️ Potential incomplete examples found:"
            echo "$INCOMPLETE"
            echo ""
            echo "Examples should be complete and runnable."
            # Warning only
          fi
```

#### Label Auto-Assignment

Create: `.github/workflows/auto-label.yml`

```yaml
name: Auto-Label Issues and PRs

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  auto-label:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Label new issues
        if: github.event_name == 'issues'
        uses: actions/github-script@v7
        with:
          script: |
            // Auto-apply triage status to new issues
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['🚦 status: triage']
            });

      - name: Label skill-related PRs
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const { data: files } = await github.rest.pulls.listFiles({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });

            const labels = [];

            // Detect skill categories based on changed files
            const pathPatterns = {
              'skill: python': /toolchains\/python/,
              'skill: typescript': /toolchains\/typescript/,
              'skill: javascript': /toolchains\/javascript/,
              'skill: nextjs': /frameworks\/nextjs/,
              'skill: ai': /toolchains\/.*\/ai/,
              'skill: universal': /universal\//
            };

            for (const [label, pattern] of Object.entries(pathPatterns)) {
              if (files.some(file => pattern.test(file.filename))) {
                labels.push(label);
              }
            }

            // Check for new skills
            const hasNewSkill = files.some(file =>
              file.filename.includes('SKILL.md') && file.status === 'added'
            );

            if (hasNewSkill) {
              labels.push('🚀 type: new-skill');
            }

            // Apply labels
            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                labels: labels
              });
            }
```

#### PR Size Labeling

Create: `.github/workflows/pr-size.yml`

```yaml
name: PR Size Labeling

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  size-label:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_label: 'effort: small'
          xs_max_size: '50'
          s_label: 'effort: small'
          s_max_size: '150'
          m_label: 'effort: medium'
          m_max_size: '400'
          l_label: 'effort: large'
          l_max_size: '800'
          xl_label: 'effort: epic'
          fail_if_xl: 'false'
```

### Workflow Best Practices

**Do:**
- ✅ Keep workflows focused (one responsibility per workflow)
- ✅ Use descriptive job and step names
- ✅ Add comments explaining complex logic
- ✅ Test workflows on fork before deploying
- ✅ Use official GitHub actions when possible
- ✅ Set appropriate permissions (minimal required)

**Don't:**
- ❌ Store secrets in workflow files (use repository secrets)
- ❌ Run workflows on every commit (filter by path/files)
- ❌ Auto-merge PRs without review
- ❌ Grant write access to forks
- ❌ Ignore workflow security warnings

---

## Appendix A: Label Creation Script

Save as `scripts/create-labels.sh`:

```bash
#!/bin/bash
# GitHub label creation script for claude-mpm-skills
# Requires: GitHub CLI (gh) - Install: https://cli.github.com/
# Usage: bash scripts/create-labels.sh

set -e

echo "🏷️  Creating labels for claude-mpm-skills..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

echo "Creating Priority Labels..."
gh label create "🟥 priority: critical" --color b60205 --description "Must be fixed ASAP" --force
gh label create "🟧 priority: high" --color d93f0b --description "Blocks dependent work" --force
gh label create "🟨 priority: medium" --color fbca04 --description "Important but non-blocking" --force
gh label create "🟩 priority: low" --color cfda2c --description "Nice to have, no rush" --force

echo "Creating Status Labels..."
gh label create "🚦 status: triage" --color eeeeee --description "Needs initial review" --force
gh label create "🔍 status: needs-info" --color d4c5f9 --description "Awaiting information" --force
gh label create "🚧 status: blocked" --color 333333 --description "Cannot proceed" --force
gh label create "🏁 status: ready" --color 0e8a16 --description "Ready for implementation" --force
gh label create "👀 status: in-review" --color fbca04 --description "Under active review" --force
gh label create "⛔ status: wontfix" --color ffffff --description "Rejected/out of scope" --force
gh label create "✅ status: done" --color 1d76db --description "Completed" --force

echo "Creating Type Labels..."
gh label create "🐛 type: bug" --color d73a4a --description "Something isn't working" --force
gh label create "✨ type: enhancement" --color a2eeef --description "Improvement to existing feature" --force
gh label create "🚀 type: new-skill" --color 0075ca --description "Proposal for new skill" --force
gh label create "📖 type: documentation" --color 0075ca --description "Documentation improvements" --force
gh label create "🔧 type: tooling" --color d4c5f9 --description "CI/CD, scripts, automation" --force
gh label create "💬 type: question" --color d876e3 --description "User question" --force
gh label create "🎨 type: design" --color e99695 --description "UI/UX, repository structure" --force

echo "Creating Skill Category Labels..."
gh label create "skill: python" --color 3572A5 --description "Python skills" --force
gh label create "skill: typescript" --color 2b7489 --description "TypeScript skills" --force
gh label create "skill: javascript" --color f1e05a --description "JavaScript skills" --force
gh label create "skill: nextjs" --color 000000 --description "Next.js skills" --force
gh label create "skill: ui" --color 563d7c --description "UI/styling skills" --force
gh label create "skill: ai" --color ff6f00 --description "AI/ML skills" --force
gh label create "skill: platform" --color 89e051 --description "Platform/deployment" --force
gh label create "skill: universal" --color ededed --description "Universal skills" --force

echo "Creating Effort Labels..."
gh label create "effort: small" --color c2e0c6 --description "< 2 hours of work" --force
gh label create "effort: medium" --color fef2c0 --description "2-8 hours of work" --force
gh label create "effort: large" --color f9d0c4 --description "1-3 days of work" --force
gh label create "effort: epic" --color d93f0b --description "Multi-day or requires research" --force

echo "Creating Community Labels..."
gh label create "good first issue" --color 7057ff --description "Good for newcomers" --force
gh label create "help wanted" --color 008672 --description "Maintainer requests community help" --force
gh label create "🔒 staff only" --color d73a4a --description "Requires maintainer privileges" --force
gh label create "duplicate" --color cfd3d7 --description "Duplicate of another issue" --force
gh label create "invalid" --color e4e669 --description "Invalid issue" --force

echo "Creating Automated Labels..."
gh label create "🤖 auto: validation-failed" --color b60205 --description "CI validation checks failed" --force
gh label create "🤖 auto: sensitive-data" --color d73a4a --description "Potential credentials detected" --force
gh label create "🤖 auto: manifest-error" --color d93f0b --description "manifest.json validation failed" --force

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "Total: 40 labels across 7 categories"
```

**To use:**

```bash
# Make executable
chmod +x scripts/create-labels.sh

# Run script
bash scripts/create-labels.sh
```

**Prerequisites:**
1. Install GitHub CLI: `brew install gh` (macOS) or see https://cli.github.com/
2. Authenticate: `gh auth login`
3. Run script from repository root

---

## Appendix B: Troubleshooting

### Common Issues

#### Issue: Branch protection not enforcing

**Symptoms:** PRs merge without reviews or status checks

**Solutions:**
1. Verify protection rule applies to `main` (not `master` or typo)
2. Check "Do not allow bypassing" is enabled
3. Confirm you're not an admin bypassing rules
4. Verify status check name matches exactly (case-sensitive)

#### Issue: Status checks not appearing in branch protection

**Symptoms:** Cannot select CI workflow in required checks

**Solutions:**
1. Workflow must run at least once on a PR to be selectable
2. Check workflow name matches: `validate / validate`
3. Verify workflow triggers on `pull_request` events
4. Look for workflow errors in Actions tab

#### Issue: Labels not applying automatically

**Symptoms:** Auto-label workflow not triggering

**Solutions:**
1. Verify workflow file in `.github/workflows/` directory
2. Check workflow permissions (needs `issues: write`)
3. Ensure workflow triggers on correct events
4. Check Actions tab for errors
5. Verify repository allows Actions to run

#### Issue: Secret scanning blocking legitimate code

**Symptoms:** Push blocked for fake/example API keys

**Solutions:**
1. Use placeholders: `YOUR_API_KEY`, `<API_KEY>`, `{API_KEY}`
2. Mark as example in comments: `# Example only - not real`
3. Bypass protection if absolutely needed (not recommended)

#### Issue: Dependabot PRs not creating

**Symptoms:** No automatic dependency update PRs

**Solutions:**
1. Verify Dependabot is enabled in Settings → Security
2. Check for `dependabot.yml` configuration errors
3. Ensure repository has dependencies to update
4. Check Dependabot logs in Insights → Dependency graph

#### Issue: Community health checklist incomplete

**Symptoms:** Missing checkmarks in Insights → Community

**Solutions:**
1. Verify file names are exact (case-sensitive)
2. Ensure files in correct locations (root, `.github/`, or `docs/`)
3. Files must be on default branch (`main`)
4. Wait 5-10 minutes for GitHub to detect new files
5. Hard refresh browser cache

---

## Additional Resources

### Official GitHub Documentation

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [Securing your repository](https://docs.github.com/en/code-security/getting-started/securing-your-repository)
- [GitHub Actions permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)

### Community Standards

- [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/)
- [OSSF Vulnerability Disclosure Guide](https://github.com/ossf/oss-vulnerability-guide)
- [Creative Commons Label Taxonomy](https://opensource.creativecommons.org/contributing-code/repo-labels/)

### Related Documentation

- [CONTRIBUTING.md](/CONTRIBUTING.md) - Contribution guidelines
- [SKILL_SELF_CONTAINMENT_STANDARD.md](/docs/SKILL_SELF_CONTAINMENT_STANDARD.md) - Self-containment requirements
- [SKILL_CREATION_PR_CHECKLIST.md](/docs/SKILL_CREATION_PR_CHECKLIST.md) - PR submission checklist

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-30
**Maintainer:** @bobmatnyc

For questions or suggestions about this setup guide, open an issue with the `📖 type: documentation` label.
