---
name: vercel-deployments-builds
description: Vercel deployment lifecycle for builds, deployments, previews, release phases, and rollback. Use when configuring build output, deployment workflows, or release controls on Vercel.
progressive_disclosure:
  entry_point:
    summary: "Vercel deployment lifecycle for builds, deployments, previews, release phases, and rollback. Use when configuring build output, deployment workflows, or release controls on Vercel."
    when_to_use: "When working with vercel-deployments-builds or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Vercel Deployments and Builds Skill

---
progressive_disclosure:
  entry_point:
    summary: "Deployments and builds on Vercel: build pipeline, deployment environments, deploy hooks, release phases, checks, and rollback."
    when_to_use:
      - "When configuring build and deployment workflows"
      - "When using preview and production deployments"
      - "When controlling releases and rollbacks"
    quick_start:
      - "Connect a Git repository"
      - "Review build and deployment settings"
      - "Use previews for every branch"
      - "Promote to production and monitor"
  token_estimate:
    entry: 90-110
    full: 3800-4800
---

## Overview

Vercel deployments and builds cover the full lifecycle from source changes to production releases with automated previews and rollback controls.

## Deployments

- Use preview deployments for every branch or pull request.
- Promote deployments to production when ready.
- Configure deployment retention where needed.

## Builds

- Define build settings per project.
- Use the Build Output API for custom build output.
- Review build logs for failures.

## Release Controls

- Use release phases for controlled rollouts.
- Use instant rollback when a deployment causes regressions.
- Add deployment checks for quality gates.

## Automation

- Trigger deployments with deploy hooks.
- Add a deploy button for fast deploys.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **vercel-functions-runtime**: Functions and runtime behavior for deployments.
- **vercel-networking-domains**: Domains, routing, and CDN behavior.
- **vercel-observability**: Logs and tracing for deployment issues.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**Vercel Docs**:
- Deployments: https://vercel.com/docs/deployments
- Builds: https://vercel.com/docs/builds
- Build Output API: https://vercel.com/docs/build-output-api
- Deploy hooks: https://vercel.com/docs/deploy-hooks
- Deploy button: https://vercel.com/docs/deploy-button
- Release phases: https://vercel.com/docs/release-phases
- Deployment checks: https://vercel.com/docs/deployment-checks
- Instant rollback: https://vercel.com/docs/instant-rollback
- Deployment retention: https://vercel.com/docs/deployment-retention
