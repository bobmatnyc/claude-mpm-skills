---
name: digitalocean-agentic-cloud
description: DigitalOcean Gradient AI agentic cloud and AI platform for building, training, and deploying AI agents on GPU infrastructure with foundation models, knowledge bases, and agent routes. Use when planning or operating AI agents on DigitalOcean.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean Gradient AI agentic cloud and AI platform for building, training, and deploying AI agents on GPU infrastructure with foundation models, knowledge bases, and agent routes. Use when plan..."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Agentic Cloud Skill

---
progressive_disclosure:
  entry_point:
    summary: "Gradient AI agentic cloud and AI platform for building, training, and deploying AI agents with GPU infrastructure, knowledge bases, and agent routes."
    when_to_use:
      - "When building or deploying AI agents on DigitalOcean"
      - "When selecting Gradient AI for GPU-backed inference"
      - "When designing agent workflows with knowledge bases and routes"
    quick_start:
      - "Choose Gradient AI Agentic Cloud or Gradient AI Platform"
      - "Select foundation models and GPU resources"
      - "Attach knowledge bases and define agent routes"
      - "Deploy agents and monitor usage"
  token_estimate:
    entry: 90-110
    full: 3000-4200
---

## Overview

DigitalOcean Gradient AI provides managed infrastructure for building and deploying AI agents. Use Agentic Cloud for end-to-end agent workflows and the AI Platform for GPU-powered agent deployment.

## Gradient AI Agentic Cloud

- Build, train, and deploy AI agents on managed infrastructure.
- Use managed resources to run agent workloads without manual GPU orchestration.

## Gradient AI Platform

- Use GPU-powered infrastructure for AI agents and inference.
- Combine foundation models with knowledge bases.
- Configure agent routes to direct traffic and workflows.

## Agent Workflow

- Select the target model and compute profile.
- Prepare datasets and knowledge bases.
- Define agent routes and inference behavior.
- Deploy agents and observe runtime metrics.

## Integration Considerations

- Use object or block storage for datasets and artifacts.
- Align deployment with VPC and access controls.
- Track costs and usage in projects.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-storage**: Spaces, Volumes, and NFS for datasets.
- **digitalocean-compute**: GPU Droplets or Kubernetes for adjacent workloads.
- **digitalocean-management**: Monitoring and project organization.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Gradient AI Agentic Cloud: https://docs.digitalocean.com/products/gradient-ai-agentic-cloud/
- Gradient AI Platform: https://docs.digitalocean.com/products/gradient-ai-platform/
