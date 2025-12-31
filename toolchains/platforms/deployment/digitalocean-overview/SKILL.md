---
name: digitalocean-overview
description: DigitalOcean platform overview for account setup, projects, tooling (Control Panel, doctl, API, Terraform), and service selection across compute, storage, databases, networking, management, and teams. Use when onboarding or planning DigitalOcean usage.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean platform overview for account setup, projects, tooling (Control Panel, doctl, API, Terraform), and service selection across compute, storage, databases, networking, management, and tea..."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Platform Overview Skill

---
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean overview: accounts, projects, tooling (Control Panel, doctl, API, Terraform), and service map for compute, storage, databases, networking, management, teams."
    when_to_use:
      - "When onboarding to DigitalOcean or planning architecture"
      - "When selecting DigitalOcean services for a workload"
      - "When setting up teams, projects, and automation"
    quick_start:
      - "Create a project in the Control Panel"
      - "Generate API tokens and add SSH keys"
      - "Install doctl and authenticate"
      - "Choose compute, storage, and database services"
  token_estimate:
    entry: 90-110
    full: 3000-4000
---

## Overview

DigitalOcean provides cloud services for compute, storage, networking, and managed databases, plus monitoring and team management. Use the Control Panel, doctl CLI, REST API, or Terraform for provisioning and operations.

## Platform Entry Points

- **Control Panel**: Use the web UI for interactive provisioning and monitoring.
- **doctl CLI**: Automate resource creation and lifecycle management.
- **REST API**: Integrate provisioning into internal tooling.
- **Terraform**: Manage infrastructure as code.

## Account and Access Setup

- Create a team and configure billing and access.
- Enable account security settings (2FA and secure sign-in).
- Add SSH keys for Droplet access.
- Create API tokens for automation and CI/CD.

## Project Organization

- Use Projects to group resources by application, environment, or team.
- Standardize naming to simplify search and ownership.

## DigitalOcean Skill Map

Use these skills for deeper coverage (if deployed):

- **digitalocean-compute**: Droplets, App Platform, Functions, Kubernetes, GPU.
- **digitalocean-agentic-cloud**: Gradient AI agentic cloud and AI platform.
- **digitalocean-storage**: Spaces, Volumes, NFS, Snapshots, Backups.
- **digitalocean-containers-images**: Container Registry, custom images, image lifecycle.
- **digitalocean-managed-databases**: Managed Postgres, MySQL, Redis, MongoDB, Kafka, OpenSearch, Valkey.
- **digitalocean-networking**: VPC, firewalls, load balancers, DNS, reserved IPs.
- **digitalocean-management**: Monitoring, uptime checks, projects.
- **digitalocean-teams**: Teams, organizations, roles, access controls.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **kubernetes**: Cluster operations and troubleshooting patterns.
- **docker**: Container build and runtime fundamentals.
- **terraform**: Infrastructure as code workflows.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Product overview: https://docs.digitalocean.com/products/
- Projects: https://docs.digitalocean.com/products/projects/
- Teams: https://docs.digitalocean.com/platform/teams/
- Organizations: https://docs.digitalocean.com/platform/organizations/

**Automation**:
- doctl CLI: https://docs.digitalocean.com/reference/doctl/
- REST API: https://docs.digitalocean.com/reference/api/
- Terraform: https://docs.digitalocean.com/reference/terraform/
