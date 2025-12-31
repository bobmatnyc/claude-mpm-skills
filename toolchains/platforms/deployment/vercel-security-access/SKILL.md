---
name: vercel-security-access
description: Vercel security and access controls including RBAC, SSO, deployment protection, firewall, bot defense, audit logs, and 2FA. Use when securing Vercel projects or managing access.
progressive_disclosure:
  entry_point:
    summary: "Vercel security and access controls including RBAC, SSO, deployment protection, firewall, bot defense, audit logs, and 2FA. Use when securing Vercel projects or managing access."
    when_to_use: "When working with vercel-security-access or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Vercel Security and Access Skill

---
progressive_disclosure:
  entry_point:
    summary: "Vercel security and access: RBAC, SSO (SAML/OIDC), deployment protection, firewall, BotID, audit logs, and 2FA."
    when_to_use:
      - "When managing access control and roles"
      - "When securing deployments and endpoints"
      - "When auditing activity and enforcing MFA"
    quick_start:
      - "Enable RBAC and role assignments"
      - "Configure SSO and authentication policies"
      - "Apply deployment protection and firewall"
      - "Review audit and activity logs"
  token_estimate:
    entry: 90-110
    full: 4000-5200
---

## Overview

Vercel security features cover identity, access control, deployment protection, and threat mitigation.

## Access Control

- Use RBAC to define project permissions.
- Configure SAML or OIDC for SSO.
- Require 2FA for sensitive access.

## Deployment Protection

- Apply deployment protection for previews and production.
- Limit access to protected deployments.

## Firewall and Bot Defense

- Use Vercel Firewall to manage traffic rules.
- Use BotID to mitigate automated abuse.

## Audit and Activity Logs

- Review audit logs for compliance.
- Track activity history for user actions.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **vercel-teams-billing**: Team settings and account policy.
- **vercel-observability**: Operational visibility for security events.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**Vercel Docs**:
- RBAC: https://vercel.com/docs/rbac
- SAML: https://vercel.com/docs/saml
- OIDC: https://vercel.com/docs/oidc
- Deployment protection: https://vercel.com/docs/deployment-protection
- Vercel Firewall: https://vercel.com/docs/vercel-firewall
- BotID: https://vercel.com/docs/botid
- Audit log: https://vercel.com/docs/audit-log
- Activity log: https://vercel.com/docs/activity-log
- Two-factor authentication: https://vercel.com/docs/two-factor-authentication
- Code owners: https://vercel.com/docs/code-owners
