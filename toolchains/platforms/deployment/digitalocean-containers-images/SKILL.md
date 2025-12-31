---
name: digitalocean-containers-images
description: DigitalOcean containers and images including Container Registry, preconfigured images, and custom images. Use when building, storing, or deploying container images or Droplet images on DigitalOcean.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean containers and images including Container Registry, preconfigured images, and custom images. Use when building, storing, or deploying container images or Droplet images on DigitalOcean."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Containers and Images Skill

---
progressive_disclosure:
  entry_point:
    summary: "Containers and images on DigitalOcean: Container Registry, preconfigured images, custom images, and image lifecycle management."
    when_to_use:
      - "When storing or deploying container images"
      - "When using custom Droplet images"
      - "When managing image lifecycle with snapshots"
    quick_start:
      - "Create a Container Registry"
      - "Push images and configure pulls"
      - "Select base images or upload custom images"
      - "Use snapshots for versioned images"
  token_estimate:
    entry: 90-110
    full: 3500-4600
---

## Overview

DigitalOcean provides a private Container Registry plus tools for managing Droplet images and snapshots.

## Container Registry

Use Container Registry to store private container images.

- Create a registry in the target region.
- Authenticate build systems to push images.
- Configure App Platform or Kubernetes to pull from the registry.

## Containers and Images

Use preconfigured images to create Droplets quickly.

- Select official or marketplace images when creating Droplets.
- Use snapshots to capture a configured Droplet as a reusable image.

## Custom Images

Use custom images to boot Droplets with preinstalled stacks.

- Upload a custom image that meets DigitalOcean requirements.
- Use the custom image as the base for new Droplets.

## Image Lifecycle Practices

- Standardize base images for consistency.
- Use snapshots to version and roll back Droplet states.
- Store container images in the registry alongside source commits.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-compute**: Droplets, App Platform, and Kubernetes compute selection.
- **digitalocean-storage**: Snapshots and backups.
- **docker**: Container build and runtime patterns.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Containers and Images: https://docs.digitalocean.com/products/images/
- Container Registry: https://docs.digitalocean.com/products/container-registry/
- Custom Images: https://docs.digitalocean.com/products/custom-images/
- Snapshots: https://docs.digitalocean.com/products/snapshots/
- Backups: https://docs.digitalocean.com/products/backups/
