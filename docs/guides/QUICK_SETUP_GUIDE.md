# Quick Setup Guide for claude-mpm-skills

**Time Required:** 30-45 minutes
**Prerequisites:** Repository owner/admin access to https://github.com/bobmatnyc/claude-mpm-skills

---

## ✅ Step 1: Labels [COMPLETED]

- [x] Run `bash scripts/create-labels.sh`
- [x] 40 labels created successfully

---

## 🔧 Step 2: Configure Repository Settings

**Navigation:** Go to https://github.com/bobmatnyc/claude-mpm-skills/settings

### About Section (Repository Homepage)

1. Click ⚙️ **gear icon** next to "About" (top right of repository homepage)

2. **Description:**
   ```
   Production-ready Claude Code skills for intelligent project development
   ```

3. **Website:** (optional)
   ```
   https://github.com/bobmatnyc/claude-mpm-skills#readme
   ```

4. **Topics:** Add these tags (click in field, type, press Enter after each):
   - `claude-code`
   - `claude`
   - `anthropic`
   - `skills`
   - `ai-development`
   - `development-tools`
   - `project-management`
   - `automation`
   - `typescript`
   - `python`
   - `nextjs`
   - `ai-workflows`
   - `code-generation`
   - `developer-productivity`
   - `mcp-servers`

5. ✅ Click **Save changes**

### Features Configuration

**Navigation:** Settings → General → Features

1. **Issues:**
   - [x] Enable issues

2. **Discussions:**
   - [x] Enable Discussions
   - Click **Set up Discussions** button
   - GitHub will create initial categories automatically
   - Recommended categories:
     - 💡 **Ideas** - Skill proposals and feature requests
     - 🙏 **Q&A** - Questions about using skills
     - 📣 **Announcements** - New releases (maintainers only)
     - 🎉 **Show and Tell** - Share implementations
     - 💬 **General** - Everything else

3. **Projects:**
   - ⚠️ Optional - Enable if you want project boards for roadmap tracking

4. **Wiki:**
   - [ ] Keep disabled (use `/docs/` directory instead)

5. **Sponsorships:**
   - [ ] Leave disabled unless ready

6. **Preserve this repository:**
   - [x] Enable (Arctic Code Vault archival)

### Pull Requests Configuration

**Navigation:** Settings → General → Pull Requests

1. **Merge button options:**
   - [x] Allow merge commits
   - [x] Allow squash merging
   - [ ] Allow rebase merging (optional)

2. **Pull request options:**
   - [x] Always suggest updating pull request branches
   - [x] Allow auto-merge
   - [x] Automatically delete head branches

3. ✅ Click **Save** at bottom of page

---

## 🛡️ Step 3: Enable Branch Protection on `main`

**Navigation:** Settings → Branches → Add branch protection rule

**Direct link:** https://github.com/bobmatnyc/claude-mpm-skills/settings/branches

### Configuration

1. **Branch name pattern:** `main`

2. **Protect matching branches** (check these boxes):

   **✅ Require a pull request before merging**
   - [x] Require approvals: **1**
   - [x] Dismiss stale pull request approvals when new commits are pushed
   - [x] Require review from Code Owners

   **✅ Require status checks to pass before merging**
   - [x] Require branches to be up to date before merging
   - Search for and add status check:
     - Type `validate` in search box
     - Select: `validate / validate`
     - **Note:** If not visible, the workflow must run at least once first

   **✅ Require conversation resolution before merging**

   **⚠️ Require signed commits** (Optional - Recommended for security)
   - [x] Enable if security is paramount
   - [ ] Skip initially if it adds contributor friction

   **❌ Require linear history** (Leave unchecked - too strict for open source)

   **❌ Require deployments to succeed** (Leave unchecked - N/A for this repo)

3. **Rules applied to everyone including administrators:**

   **✅ Do not allow bypassing the above settings**
   - [x] Enable (prevents accidental direct commits)

   **⚠️ Restrict who can push to matching branches** (Recommended)
   - [x] Enable and add: `bobmatnyc`
   - This enforces PR workflow even for maintainers

   **❌ Allow force pushes** (Leave at "Do not allow" - protects history)

   **❌ Allow deletions** (Leave unchecked - prevents accidental deletion)

4. ✅ Click **Create** at bottom of page

**Visual confirmation:** You should see a green checkmark next to `main` in the Branches list.

---

## 🔐 Step 4: Enable Security Features

**Navigation:** Settings → Security & analysis

**Direct link:** https://github.com/bobmatnyc/claude-mpm-skills/settings/security_analysis

### Enable These Features (click Enable for each):

1. **✅ Private vulnerability reporting**
   - Click **Enable**
   - Allows security researchers to privately report issues
   - Notifications sent to repository admins

2. **✅ Dependency graph**
   - Should be enabled by default for public repos
   - If not, click **Enable**

3. **✅ Dependabot alerts**
   - Click **Enable**
   - Get alerts for known vulnerabilities in dependencies

4. **✅ Dependabot security updates**
   - Click **Enable**
   - Automatically creates PRs to fix vulnerable dependencies

5. **⚠️ Dependabot version updates** (Optional)
   - Creates PRs for all dependency updates (can be noisy)
   - Skip initially, enable later if desired

6. **✅ Secret scanning** (Enabled by default for public repos)
   - Verify status shows "Enabled"
   - Detects exposed secrets in code

7. **✅ Secret scanning push protection**
   - Click **Enable**
   - Blocks commits containing secrets before they're pushed

8. **⚠️ Code scanning (CodeQL)** (If available - requires GitHub Advanced Security)
   - Click **Set up** if available
   - Only available on Pro/Enterprise plans
   - Skip if not available

### Verify Security Tab

- Navigate to: https://github.com/bobmatnyc/claude-mpm-skills/security
- You should see sections for:
  - Dependabot alerts
  - Secret scanning
  - Security advisories

---

## ⚙️ Step 5: Configure GitHub Actions

**Navigation:** Settings → Actions → General

**Direct link:** https://github.com/bobmatnyc/claude-mpm-skills/settings/actions

### Actions Permissions

1. **Actions permissions:**
   - Select: **[x] Allow all actions and reusable workflows**
   - Rationale: Open source projects benefit from community actions

### Workflow Permissions

2. **Workflow permissions:**
   - Select: **[x] Read repository contents and packages permissions**
   - [x] Allow GitHub Actions to create and approve pull requests
   - **Do NOT enable write access** (prevents accidental auto-commits)

### Fork Pull Request Workflows

3. **Fork pull request workflows from outside collaborators:**
   - Select: **[x] Require approval for first-time contributors**

4. **Fork pull request workflows in private repositories:**
   - Select: **[x] Require approval for all outside collaborators**

5. ✅ Click **Save** at bottom of page

---

## ✅ Verification Checklist

After completing steps 2-5, verify:

### Repository Settings
- [ ] 15 topics added to repository (visible on homepage)
- [ ] Issues enabled
- [ ] Discussions enabled
- [ ] Auto-delete head branches enabled
- [ ] Create a test issue to verify templates work

### Branch Protection
- [ ] Branch protection rule exists for `main`
  - Check: https://github.com/bobmatnyc/claude-mpm-skills/settings/branches
- [ ] Rule requires 1 approval
- [ ] Rule dismisses stale reviews
- [ ] Force pushes blocked
- [ ] Branch deletions blocked
- [ ] Only maintainers can push directly (if restricted)

### Security Features
- [ ] Dependabot alerts enabled
  - Check: https://github.com/bobmatnyc/claude-mpm-skills/security/dependabot
- [ ] Dependabot security updates enabled
- [ ] Private vulnerability reporting enabled
- [ ] Secret scanning enabled
- [ ] Secret scanning push protection enabled

### GitHub Actions
- [ ] Workflow permissions configured (read-only)
- [ ] Fork PR approval required for outside collaborators
- [ ] Actions can create/approve PRs

---

## 🎯 Next Steps

After completing this setup:

### 1. Test the Configuration

**Create a test issue:**
- Go to: https://github.com/bobmatnyc/claude-mpm-skills/issues/new/choose
- Select one of the issue templates
- Verify labels auto-populate
- Close the test issue

**Create a test branch and PR:**
```bash
git checkout -b test-branch-protection
echo "# Test" >> test.md
git add test.md
git commit -m "test: verify branch protection"
git push origin test-branch-protection
```
- Create PR via GitHub UI
- Verify you cannot merge without approval
- Verify status checks are required
- Close and delete the test PR

### 2. Review Community Health

- Navigate to: https://github.com/bobmatnyc/claude-mpm-skills/community
- Verify all items show green checkmarks:
  - [x] Description
  - [x] README
  - [x] Code of conduct
  - [x] Contributing guidelines
  - [x] License
  - [x] Security policy
  - [x] Issue templates
  - [x] Pull request template

### 3. Optional: Add CI Workflow

If `.github/workflows/validate-skills.yml` doesn't exist yet:
- See Section 13 in `docs/GITHUB_REPOSITORY_SETUP.md`
- Create workflow to validate skill self-containment
- This enables the `validate / validate` status check

### 4. Optional: Create CODEOWNERS File

Create `.github/CODEOWNERS`:
```
# Repository owner auto-assigned to all PRs
* @bobmatnyc

# Skills require review from maintainer
/skills/ @bobmatnyc

# Documentation can be reviewed by anyone
/docs/ @bobmatnyc
```

### 5. Make Repository Public (when ready)

**Final steps before going public:**
1. Review all documentation for accuracy
2. Ensure no sensitive data in commit history
3. Test all issue/PR templates
4. Verify CI workflows pass

**To make public:**
1. Go to: Settings → General → Danger Zone
2. Click **Change visibility**
3. Select **Public**
4. Type repository name to confirm
5. Click **I understand, make this repository public**

---

## 📚 Additional Resources

- **Full setup guide:** [docs/GITHUB_REPOSITORY_SETUP.md](./GITHUB_REPOSITORY_SETUP.md)
- **Community health best practices:** [docs/research/github-community-health-best-practices-2025-11-30.md](./research/github-community-health-best-practices-2025-11-30.md)
- **Self-containment standard:** [docs/SKILL_SELF_CONTAINMENT_STANDARD.md](./SKILL_SELF_CONTAINMENT_STANDARD.md)
- **Contributing guide:** [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Code of conduct:** [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)

---

## 🆘 Troubleshooting

### Can't find branch protection settings?

- Ensure you have admin access to the repository
- Direct link: https://github.com/bobmatnyc/claude-mpm-skills/settings/branches
- If you still don't see it, you may not have owner/admin permissions

### Status checks not appearing in branch protection?

- The workflow must run at least once before it appears
- Create a test PR first, let the workflow run, then configure branch protection
- Check workflow status: https://github.com/bobmatnyc/claude-mpm-skills/actions

### Dependabot/Security features not available?

- Some features require specific GitHub plans
- Public repositories get most security features for free
- Code scanning (CodeQL) requires GitHub Advanced Security
- Check your organization/account plan if features are missing

### Can't enable Discussions?

- Discussions must be enabled in repository settings first
- Go to: Settings → General → Features
- Check the "Discussions" checkbox
- Click "Set up Discussions" to configure categories

### Branch protection preventing your own merges?

- This is correct behavior! Branch protection applies to everyone
- Create a PR even for your own changes
- Use a different GitHub account or add yourself as a collaborator to approve
- Alternatively, temporarily disable "Do not allow bypassing" (not recommended)

### Need more help?

- See **Appendix B: Troubleshooting** in [docs/GITHUB_REPOSITORY_SETUP.md](./GITHUB_REPOSITORY_SETUP.md)
- Create an issue with the 💬 **question** label
- Check GitHub's official documentation: https://docs.github.com

---

## 📊 Completion Status

**Setup Progress:**
- [x] Step 1: Labels created (40 labels)
- [ ] Step 2: Repository settings configured
- [ ] Step 3: Branch protection enabled
- [ ] Step 4: Security features enabled
- [ ] Step 5: GitHub Actions configured

**Estimated time per step:**
- Step 2: 10-15 minutes
- Step 3: 5-10 minutes
- Step 4: 5-10 minutes
- Step 5: 5 minutes
- Verification: 5-10 minutes

**Total:** 30-45 minutes

---

**Last Updated:** 2025-11-30
**Repository:** claude-mpm-skills
**Maintainer:** @bobmatnyc
