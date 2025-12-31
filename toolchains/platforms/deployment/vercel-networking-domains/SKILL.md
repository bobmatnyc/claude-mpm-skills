---
name: vercel-networking-domains
description: Vercel networking and routing for domains, DNS, redirects, rewrites, headers, CDN, edge cache, and regions. Use when configuring routing or traffic behavior on Vercel.
progressive_disclosure:
  entry_point:
    summary: "Vercel networking and routing for domains, DNS, redirects, rewrites, headers, CDN, edge cache, and regions. Use when configuring routing or traffic behavior on Vercel."
    when_to_use: "When working with vercel-networking-domains or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Vercel Networking and Domains Skill

---
progressive_disclosure:
  entry_point:
    summary: "Vercel networking: domains, routing rules, headers, CDN, edge cache, and region configuration."
    when_to_use:
      - "When configuring domains and DNS"
      - "When managing redirects, rewrites, or headers"
      - "When tuning CDN and edge cache behavior"
    quick_start:
      - "Add and verify domains"
      - "Configure redirects and rewrites"
      - "Set headers and caching"
      - "Select deployment regions"
  token_estimate:
    entry: 90-110
    full: 3800-4800
---

## Overview

Vercel networking covers domain configuration, routing rules, and edge delivery behavior through the CDN and edge cache.

## Domains and DNS

- Add domains and verify ownership.
- Configure DNS records for routing.

## Routing Rules

- Define redirects and rewrites for URL behavior.
- Apply custom headers and compression.

## CDN and Edge Cache

- Use CDN distribution for global delivery.
- Purge or invalidate edge cache when needed.

## Regions

- Select regions for deployment and execution.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **vercel-functions-runtime**: Function routing and edge execution.
- **vercel-deployments-builds**: Deployment workflow and releases.
- **vercel-observability**: Traffic analytics and performance metrics.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**Vercel Docs**:
- Domains: https://vercel.com/docs/domains
- Headers: https://vercel.com/docs/headers
- Redirects: https://vercel.com/docs/redirects
- Rewrites: https://vercel.com/docs/rewrites
- CDN: https://vercel.com/docs/cdn
- Edge Cache: https://vercel.com/docs/edge-cache
- Regions: https://vercel.com/docs/regions
- Compression: https://vercel.com/docs/compression
