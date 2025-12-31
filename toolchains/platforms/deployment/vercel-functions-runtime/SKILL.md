---
name: vercel-functions-runtime
description: Vercel Functions and Edge Runtime, including cron jobs and routing middleware. Use when building APIs, serverless workloads, or scheduled tasks on Vercel.
progressive_disclosure:
  entry_point:
    summary: "Vercel Functions and Edge Runtime, including cron jobs and routing middleware. Use when building APIs, serverless workloads, or scheduled tasks on Vercel."
    when_to_use: "When working with vercel-functions-runtime or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Vercel Functions and Runtime Skill

---
progressive_disclosure:
  entry_point:
    summary: "Vercel Functions and Edge Runtime: serverless APIs, edge execution, cron jobs, and routing middleware."
    when_to_use:
      - "When building API routes or serverless logic"
      - "When targeting the Edge Runtime"
      - "When scheduling tasks with cron jobs"
    quick_start:
      - "Create a function entry point"
      - "Choose the runtime (Node or Edge)"
      - "Configure cron schedules"
      - "Deploy and monitor"
  token_estimate:
    entry: 90-110
    full: 3600-4700
---

## Overview

Vercel Functions provide serverless execution for APIs and background tasks. The Edge Runtime enables low-latency execution closer to users.

## Vercel Functions

- Define serverless functions in the project structure.
- Use environment variables for configuration.
- Review logs for errors and performance.

## Edge Runtime

- Use the Edge Runtime for low-latency execution.
- Validate compatibility with the Edge runtime constraints.

## Cron Jobs

- Schedule jobs with cron definitions.
- Use cron for periodic maintenance tasks or sync jobs.

## Routing and Middleware

- Apply routing middleware for request handling.
- Use headers, rewrites, and redirects to control traffic.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **vercel-deployments-builds**: Deployment workflow and release controls.
- **vercel-networking-domains**: Routing, headers, and edge caching.
- **vercel-observability**: Logs and tracing for function debugging.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**Vercel Docs**:
- Functions: https://vercel.com/docs/functions
- Edge Runtime: https://vercel.com/docs/functions/runtimes/edge
- Cron Jobs: https://vercel.com/docs/cron-jobs
- Routing Middleware: https://vercel.com/docs/routing-middleware
