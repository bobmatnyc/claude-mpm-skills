---
name: emergency-release-workflow
description: Emergency release workflow for critical bug fixes and security patches. Use when production issues require fast-track deployment.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - urgency_assessment
  sections:
    - emergency_process
    - pr_template
    - deployment_steps
    - communication
    - post_incident
    - backport_strategy
---

# Emergency Release Workflow Skill

## Summary
Fast-track workflow for critical production issues requiring immediate deployment. Covers urgency assessment, expedited PR process, deployment verification, and post-incident analysis.

## When to Use
- Critical production bugs affecting users
- Security vulnerabilities (CVEs)
- Urgent business requirements
- Data integrity issues
- Service outages
- Payment processing failures

## Urgency Assessment

### Priority Levels
| Level | Type | Response Time | Deployment | Example |
|-------|------|---------------|------------|---------|
| **P0** | Security vulnerability | < 2 hours | Immediate to production | Auth bypass, data leak, active exploit |
| **P1** | Production down | < 4 hours | Same day | App crash, complete feature failure, payment down |
| **P2** | Major bug | < 24 hours | Next business day | Critical feature broken, significant user impact |
| **P3** | Business critical | < 48 hours | Scheduled release | Marketing campaign blocker, partner deadline |

### P0 Criteria (Immediate Action)
- Authentication/authorization bypass
- Data breach or exposure
- Remote code execution vulnerability
- Production service completely unavailable
- Data corruption affecting multiple users
- Payment processing completely broken

### P1 Criteria (Same Day)
- Critical feature completely broken
- Error affecting majority of users
- Revenue-impacting bug
- Database connectivity issues
- Third-party integration failure (critical service)

### P2 Criteria (Next Business Day)
- Major feature partially broken
- Affects specific user segment
- Workaround available but not ideal
- Performance degradation (not complete failure)

---

## Emergency Release Process

### 1. Create Hotfix Branch
```bash
# Branch from current production (main)
git checkout main
git pull origin main

# Create hotfix branch
git checkout -b hotfix/ENG-XXX-brief-description

# Example:
git checkout -b hotfix/ENG-1234-fix-auth-bypass
```

### 2. Implement Minimal Fix
```
⚠️ CRITICAL: Minimal change only

DO:
✅ Fix the immediate issue
✅ Add regression test
✅ Document root cause in comments

DON'T:
❌ Refactor surrounding code
❌ Fix unrelated issues
❌ Add new features
❌ Update dependencies (unless that's the fix)
```

### 3. Test Thoroughly
```bash
# Run full test suite
pnpm test

# Type check
pnpm tsc --noEmit

# Build verification
pnpm build

# Manual testing checklist:
# - [ ] Reproduce original issue
# - [ ] Verify fix resolves issue
# - [ ] Test happy path
# - [ ] Test edge cases
# - [ ] Verify no new issues introduced
```

### 4. Create PR with Labels
```bash
git add .
git commit -m "fix: [brief description of fix]

Fixes critical issue where [description].
Root cause: [explanation].

Ticket: ENG-XXX
Priority: P0"

git push origin hotfix/ENG-XXX-brief-description
```

**Use clear labels in PR title:**
- `[RELEASE]` - Direct to production
- `[HOTFIX]` - Critical fix, expedited review
- `[P0]` or `[P1]` - Priority indicator

---

## PR Template for Hotfixes

### Hotfix PR Template
```markdown
## 🚨 [RELEASE] ENG-XXX: Brief description of fix

### Urgency
- [x] P0 - Security vulnerability
- [ ] P1 - Production down
- [ ] P2 - Major bug
- [ ] P3 - Business critical

### Impact
**Users affected**: [All users / Premium tier / Specific region / etc.]

**Severity**: [Choose one]
- [ ] Service completely unavailable
- [ ] Critical feature broken
- [ ] Security vulnerability
- [ ] Data integrity issue
- [ ] Degraded performance

**User impact**:
Describe how this affects end users.

### Root Cause
[Brief explanation of what caused the issue]

**How it happened:**
1. [Step 1]
2. [Step 2]
3. [Result: issue manifested]

**Why it wasn't caught:**
- [ ] Missing test coverage
- [ ] Race condition in production
- [ ] External service behavior changed
- [ ] Recent deployment introduced regression
- [ ] Other: [explain]

### The Fix
[What this PR changes to resolve the issue]

**Changes made:**
- Modified `file.ts` to [specific change]
- Added validation for [specific case]
- Fixed logic in [specific function]

**Why this fixes it:**
[Explanation of how the change resolves the root cause]

### Testing
- [ ] ✅ Reproduced issue locally
- [ ] ✅ Verified fix resolves issue
- [ ] ✅ Regression test added
- [ ] ✅ No other functionality affected
- [ ] ✅ Tested edge cases
- [ ] ✅ Deployed to staging and verified

### Regression Test
```typescript
// Test added to prevent recurrence
describe('ENG-XXX: Auth bypass fix', () => {
  it('should reject expired tokens', async () => {
    const expiredToken = generateExpiredToken();
    const response = await fetch('/api/protected', {
      headers: { Authorization: `Bearer ${expiredToken}` }
    });
    expect(response.status).toBe(401);
  });
});
```

### Rollback Plan
**If this causes issues:**

```bash
# Option 1: Revert commit
git revert <commit-hash>
git push origin main

# Option 2: Deploy previous version
vercel rollback  # or your platform's rollback command

# Option 3: Feature flag
Set FEATURE_FIX_XXX=false in environment
```

**Monitoring:**
- [ ] Error rate in Sentry
- [ ] API response times in monitoring dashboard
- [ ] User reports in support channels

### Deploy Checklist
- [ ] PR approved by at least one reviewer (waive for P0 if necessary)
- [ ] All CI checks pass
- [ ] Deployed to staging and verified
- [ ] Monitoring alerts configured
- [ ] On-call engineer notified
- [ ] Ready for production deployment

### Post-Deploy Verification
**Immediately after deploy:**
- [ ] Verify fix in production (test endpoint directly)
- [ ] Check error tracking (Sentry, etc.)
- [ ] Monitor for new errors
- [ ] Confirm user reports stop coming in

**Metrics to watch:**
- Error rate (should drop)
- API latency (should remain stable)
- User activity (should normalize)

### Follow-Up
- [ ] Update Linear ticket with resolution
- [ ] Schedule post-incident review (if P0/P1)
- [ ] Create tickets for proper fix (if this was a band-aid)
- [ ] Update runbook/documentation
```

---

## Deployment Steps

### Pre-Deployment
```bash
# 1. Merge PR to main
# (After approval or P0 emergency waiver)

# 2. Pull latest
git checkout main
git pull origin main

# 3. Verify commit
git log -1
# Confirm this is your hotfix commit

# 4. Tag release (if using semantic versioning)
git tag -a v2.3.5 -m "Hotfix: Fix auth bypass vulnerability"
git push origin v2.3.5
```

### Deployment (Platform-Specific)

#### Vercel
```bash
# Trigger production deployment
vercel --prod

# Or use Vercel dashboard:
# Deployments → Select commit → Deploy to Production

# Monitor deployment
vercel logs --follow
```

#### Netlify
```bash
# Deploy via CLI
netlify deploy --prod

# Or trigger from dashboard:
# Deploys → Select commit → Publish deploy
```

#### Railway
```bash
# Push to main triggers deployment automatically
# Monitor in dashboard: railway.app/project/logs
```

#### AWS/GCP/Azure
```bash
# Follow platform-specific deployment process
# Example for AWS Elastic Beanstalk:
eb deploy production --staged

# Monitor:
eb logs --follow
```

### Post-Deployment Verification

#### 1. Smoke Test
```bash
# Test the specific fix
curl -X POST https://api.production.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"token": "expired_token"}'

# Expected: 401 Unauthorized
```

#### 2. Monitor Error Tracking
```
✅ Check Sentry/Rollbar/etc.:
- Error rate should drop
- No new errors introduced

⏱️ Monitor for 15-30 minutes after deployment
```

#### 3. Verify Metrics
```
Check monitoring dashboard:
- API response times (should be normal)
- Error rates (should drop)
- Database performance (should be stable)
- Third-party service health
```

#### 4. Check User Reports
```
Monitor support channels:
- Support tickets
- In-app chat
- Social media
- Status page comments
```

---

## Communication

### Internal Communication

#### Slack/Teams Message Template
```
🚨 **Production Hotfix Deployed**

**Issue**: [Brief description]
**Ticket**: ENG-XXX
**Priority**: P0
**Status**: ✅ Resolved

**Timeline:**
- Issue discovered: 14:23 UTC
- Fix deployed: 15:47 UTC
- Duration: 1h 24m

**Impact**:
[Who was affected and how]

**Root Cause**:
[Brief explanation]

**Fix**:
[What was changed]

**Verification**:
✅ Error rate dropped from 450/min to 0/min
✅ All systems operating normally

**PR**: https://github.com/org/repo/pull/XXX

**Follow-up**:
- [ ] Post-incident review scheduled for [date]
- [ ] Documentation updated
```

### External Communication (if needed)

#### Status Page Update
```
🟢 Resolved - [Issue Title]

We've resolved an issue that was affecting [feature/service].

**What happened:**
Between 14:23 and 15:47 UTC, users experienced [specific issue].

**Current status:**
The issue has been fully resolved. All systems are operating normally.

**Next steps:**
We're conducting a thorough review to prevent similar issues in the future.

We apologize for any inconvenience.
```

#### Email to Affected Users (for serious issues)
```
Subject: Update on [Service] Issue - Resolved

Hi [User],

We're writing to update you on an issue that affected [feature/service] earlier today.

**What happened:**
Between [time] and [time], you may have experienced [specific issue].

**Resolution:**
Our team quickly identified and resolved the root cause. The service is now operating normally.

**What we're doing:**
We take these issues seriously and are:
- Conducting a full review of the incident
- Implementing additional safeguards
- Improving our monitoring

We apologize for any inconvenience this may have caused.

If you have any questions or concerns, please reach out to support@company.com.

Thank you for your patience.

The [Company] Team
```

---

## Post-Incident

### Immediate Actions (Within 24 hours)
- [ ] Update Linear ticket with full resolution details
- [ ] Add incident to incident log/spreadsheet
- [ ] Document timeline of events
- [ ] Identify metrics that should have alerted earlier
- [ ] Create follow-up tickets for proper fix (if hotfix was temporary)

### Post-Incident Review (PIR) - For P0/P1

**Schedule within 72 hours**

#### PIR Template
```markdown
# Post-Incident Review: [ENG-XXX]
Date: YYYY-MM-DD
Severity: P0/P1
Duration: Xh Xm

## Summary
Brief description of the incident.

## Timeline (UTC)
- 14:23 - Issue first detected
- 14:25 - On-call engineer alerted
- 14:30 - Root cause identified
- 14:45 - Fix PR opened
- 15:20 - PR approved and merged
- 15:47 - Fix deployed to production
- 16:00 - Verified resolved

## Impact
- **Users affected**: ~5,000 users
- **Duration**: 1h 24m
- **User experience**: Unable to log in
- **Revenue impact**: Estimated $X in lost transactions
- **Reputation impact**: 23 support tickets, 5 social media mentions

## Root Cause
Detailed technical explanation of what caused the issue.

[Include code snippets, sequence diagrams if helpful]

## Resolution
What was changed to fix the issue.

## What Went Well
- ✅ Fast detection (2 minutes after deploy)
- ✅ Clear reproduction steps identified quickly
- ✅ Team collaborated effectively
- ✅ Fix deployed in under 90 minutes

## What Went Wrong
- ❌ Missing test coverage for expired token edge case
- ❌ Staging didn't catch the issue (different token expiry settings)
- ❌ No automatic rollback triggered
- ❌ Monitoring alert threshold too high

## Action Items
- [ ] ENG-XXX-1: Add test for expired token validation (@engineer, by YYYY-MM-DD)
- [ ] ENG-XXX-2: Align staging token expiry with production (@devops, by YYYY-MM-DD)
- [ ] ENG-XXX-3: Implement automatic rollback on error spike (@platform, by YYYY-MM-DD)
- [ ] ENG-XXX-4: Lower monitoring alert threshold (@observability, by YYYY-MM-DD)
- [ ] ENG-XXX-5: Add runbook for similar issues (@oncall, by YYYY-MM-DD)

## Prevention
How we'll prevent this from happening again:

1. **Testing**: Add test coverage for edge cases
2. **Monitoring**: Improve alerting thresholds
3. **Process**: Update deployment checklist
4. **Documentation**: Create runbook for on-call

## Lessons Learned
Key takeaways for the team.
```

---

## Backport Strategy

When fix needs to go to multiple branches/environments:

### Multiple Environment Deployment
```bash
# 1. Fix applied to main (production)
git checkout main
git cherry-pick <hotfix-commit-hash>

# 2. Backport to release candidate
git checkout release-candidate
git cherry-pick <hotfix-commit-hash>
git push origin release-candidate

# 3. Backport to develop
git checkout develop
git cherry-pick <hotfix-commit-hash>
git push origin develop

# Create PRs for each backport:
gh pr create --base release-candidate --head backport/rc/hotfix-ENG-XXX
gh pr create --base develop --head backport/dev/hotfix-ENG-XXX
```

### Handling Merge Conflicts
```bash
# If cherry-pick fails due to conflicts
git cherry-pick <hotfix-commit-hash>
# CONFLICT in file.ts

# Resolve conflicts manually
# Then:
git add file.ts
git cherry-pick --continue
```

### Alternative: Patch File
```bash
# Create patch from hotfix
git format-patch -1 <hotfix-commit-hash>
# Creates: 0001-fix-auth-bypass.patch

# Apply to other branch
git checkout release-candidate
git apply 0001-fix-auth-bypass.patch
```

---

## Summary

### Emergency Release Quick Reference

#### Decision Tree
```
Is production broken?
├─ Yes → Severity level?
│  ├─ P0 (security/down) → Deploy immediately, inform after
│  ├─ P1 (critical bug) → Fast-track PR, deploy same day
│  └─ P2 (major bug) → Standard expedited process
└─ No → Use normal deployment process
```

#### Time Targets
- **P0**: Issue → Deploy in < 2 hours
- **P1**: Issue → Deploy in < 4 hours
- **P2**: Issue → Deploy in < 24 hours

#### Key Principles
1. **Minimal Change**: Fix only the immediate issue
2. **Add Regression Test**: Prevent recurrence
3. **Fast Feedback**: Deploy to staging first (except P0)
4. **Clear Communication**: Keep stakeholders informed
5. **Learn & Improve**: Conduct PIR for P0/P1

#### Checklist
- [ ] Assess urgency correctly
- [ ] Create hotfix branch from production
- [ ] Implement minimal fix with regression test
- [ ] Use appropriate PR labels
- [ ] Test thoroughly (staging for P1/P2)
- [ ] Get approval (or waive for P0)
- [ ] Deploy with monitoring
- [ ] Verify fix in production
- [ ] Communicate status
- [ ] Schedule PIR (P0/P1)
- [ ] Create follow-up tickets

Use this skill when production issues require immediate attention and fast-track deployment outside normal release processes.
