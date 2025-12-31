---
name: vercel-overview
description: Vercel platform overview for onboarding, projects, CLI, Git integration, environment variables, project configuration, REST API, and webhooks. Use when planning or operating workloads on Vercel.
progressive_disclosure:
  entry_point:
    summary: "Vercel platform overview for onboarding, projects, CLI, Git integration, environment variables, project configuration, REST API, and webhooks. Use when planning or operating workloads on Vercel."
    when_to_use: "When working with vercel-overview or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Vercel Platform Overview Skill

---
progressive_disclosure:
  entry_point:
    summary: "Vercel overview: projects, CLI, Git integration, env vars, project config, REST API, webhooks, and service map for deployments, functions, data, networking, observability, security, and AI."
    when_to_use:
      - "When onboarding to Vercel or planning architecture"
      - "When setting up projects, environments, and automation"
      - "When selecting Vercel services for a workload"
    quick_start:
      - "Create a Vercel project"
      - "Connect a Git repository"
      - "Configure environment variables"
      - "Deploy via Dashboard or CLI"
  token_estimate:
    entry: 90-110
    full: 3000-4000
---

## Overview

Vercel provides a platform for building, deploying, and scaling web applications and AI workloads with integrated deployments, edge runtime, data services, and observability.

## Platform Entry Points

- **Vercel Dashboard**: Use the web UI for projects, deployments, and settings.
- **Vercel CLI**: Automate deployments and configuration.
- **REST API**: Integrate provisioning and management into tooling.
- **Webhooks**: Trigger workflows on deployment events.

## Project Setup Workflow

- Create a project and connect a Git repository.
- Configure environment variables for each environment.
- Review project configuration defaults and overrides.
- Deploy and verify build output.

## Vercel Skill Map

Use these skills for deeper coverage (if deployed):

- **vercel-deployments-builds**: Deployments, builds, and release workflows.
- **vercel-functions-runtime**: Serverless and Edge Functions, cron jobs, and runtime behavior.
- **vercel-storage-data**: Postgres, Redis, Blob, Edge Config, and data cache.
- **vercel-networking-domains**: Domains, routing, headers, and edge caching.
- **vercel-observability**: Analytics, Speed Insights, logs, and tracing.
- **vercel-security-access**: RBAC, SSO, deployment protection, firewall, and bot defense.
- **vercel-teams-billing**: Accounts, plans, spend management, and team controls.
- **vercel-ai**: AI SDK, AI Gateway, Agent, and MCP.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **nextjs**: Next.js deployment patterns.
- **react**: Frontend integration patterns.
- **typescript**: Type-safe runtime patterns.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**Vercel Docs**:
- Getting started: https://vercel.com/docs/getting-started-with-vercel
- Projects: https://vercel.com/docs/projects
- CLI: https://vercel.com/docs/cli
- Git integration: https://vercel.com/docs/git
- Environment variables: https://vercel.com/docs/environment-variables
- Project configuration: https://vercel.com/docs/project-configuration
- REST API: https://vercel.com/docs/rest-api
- Webhooks: https://vercel.com/docs/webhooks
- Integrations: https://vercel.com/docs/integrations
