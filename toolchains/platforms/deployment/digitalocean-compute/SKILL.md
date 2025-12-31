---
name: digitalocean-compute
description: DigitalOcean compute services covering Droplets, App Platform, Functions, Kubernetes (DOKS), GPU Droplets, and Bare Metal GPUs. Use when selecting or provisioning compute for applications, containers, or serverless workloads.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean compute services covering Droplets, App Platform, Functions, Kubernetes (DOKS), GPU Droplets, and Bare Metal GPUs. Use when selecting or provisioning compute for applications, containe..."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Compute Skill

---
progressive_disclosure:
  entry_point:
    summary: "Compute on DigitalOcean: Droplets, App Platform, Functions, Kubernetes, GPU Droplets, Bare Metal GPUs."
    when_to_use:
      - "When choosing a compute model for an application"
      - "When provisioning VMs, PaaS, serverless, or Kubernetes"
      - "When planning GPU-backed workloads"
    quick_start:
      - "Pick Droplets, App Platform, Functions, or Kubernetes"
      - "Select region, size, and image"
      - "Configure networking and access"
      - "Deploy and monitor workloads"
  token_estimate:
    entry: 90-110
    full: 4000-5200
---

## Overview

DigitalOcean compute includes VMs, managed PaaS, serverless functions, and managed Kubernetes, plus GPU offerings for AI workloads.

## Droplets (VMs)

Use Droplets for full OS control and custom networking.

- Choose region and Droplet plan.
- Select an OS image or snapshot.
- Add SSH keys for secure access.
- Attach Volumes for persistent block storage.
- Apply firewalls and VPC configuration.

## App Platform (PaaS)

Use App Platform to deploy from Git or container images with managed build and runtime.

- Connect a Git repository or container registry.
- Define build and run commands or app spec.
- Set environment variables and secrets.
- Configure custom domains and HTTPS.

## Functions (FaaS)

Use Functions for event-driven or lightweight API workloads.

- Create a Functions namespace.
- Deploy functions with doctl or the Control Panel.
- Configure environment variables and triggers.
- Monitor execution and logs.

## Kubernetes (DOKS)

Use managed Kubernetes for multi-service container orchestration.

- Create a cluster and node pools.
- Save kubeconfig for cluster access.
- Deploy workloads with Kubernetes manifests.
- Pull images from Container Registry.

## GPU Compute

Use GPU Droplets or Bare Metal GPUs for AI and ML workloads.

- GPU Droplets: VM-based GPU workloads with flexible sizing.
- Bare Metal GPUs: Dedicated GPU hardware for high performance.

## Compute Selection Guide

- Use **Droplets** for full control and custom configurations.
- Use **App Platform** for managed app deployments from Git or containers.
- Use **Functions** for event-driven workflows and micro APIs.
- Use **Kubernetes** for multi-service container orchestration.
- Use **GPU Droplets** or **Bare Metal GPUs** for AI or GPU-heavy workloads.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-containers-images**: Registry and image workflows.
- **digitalocean-storage**: Spaces, Volumes, and backups.
- **kubernetes**: Cluster operations and troubleshooting.
- **docker**: Container build and runtime patterns.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Compute: https://docs.digitalocean.com/products/compute/
- Droplets: https://docs.digitalocean.com/products/droplets/
- App Platform: https://docs.digitalocean.com/products/app-platform/
- Functions: https://docs.digitalocean.com/products/functions/
- Kubernetes: https://docs.digitalocean.com/products/kubernetes/
- GPU Droplets: https://docs.digitalocean.com/products/gpu-droplets/
- Bare Metal GPUs: https://docs.digitalocean.com/products/bare-metal-gpus/
