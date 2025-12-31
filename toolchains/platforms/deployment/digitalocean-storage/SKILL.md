---
name: digitalocean-storage
description: DigitalOcean storage services including Spaces object storage, Volumes block storage, NFS, Snapshots, and Backups. Use when selecting or managing storage for DigitalOcean workloads.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean storage services including Spaces object storage, Volumes block storage, NFS, Snapshots, and Backups. Use when selecting or managing storage for DigitalOcean workloads."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Storage Skill

---
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean storage: Spaces object storage, Volumes block storage, NFS file storage, Snapshots, and Backups."
    when_to_use:
      - "When selecting object, block, or file storage"
      - "When designing backup and snapshot strategies"
      - "When attaching persistent storage to Droplets"
    quick_start:
      - "Choose Spaces, Volumes, or NFS"
      - "Provision storage in the target region"
      - "Attach or mount storage to compute"
      - "Enable snapshots or backups"
  token_estimate:
    entry: 90-110
    full: 3800-5000
---

## Overview

DigitalOcean storage includes S3-compatible object storage, network-attached block storage, managed NFS, plus snapshots and backups for recovery workflows.

## Spaces Object Storage

Use Spaces for large datasets, static assets, and logs.

- Create a Space in the required region.
- Generate access keys for S3-compatible tooling.
- Configure access controls for public or private objects.

## Volumes Block Storage

Use Volumes to add persistent block storage to Droplets.

- Create a Volume in the same region as the Droplet.
- Attach the Volume to a Droplet.
- Mount the Volume on the Droplet OS.

## NFS File Storage

Use managed NFS for shared file access across services.

- Provision an NFS file system.
- Mount from compute resources that require shared storage.

## Snapshots

Use snapshots for on-demand backups of Droplets or Volumes.

- Create snapshots before major changes.
- Use snapshots to create new Droplets or Volumes.

## Backups

Use scheduled backups for routine recovery points.

- Enable backups on Droplets.
- Restore from backups during recovery.

## Storage Selection Guide

- Use **Spaces** for object storage and static assets.
- Use **Volumes** for persistent block storage on Droplets.
- Use **NFS** for shared POSIX file storage.
- Use **Snapshots** for point-in-time recovery.
- Use **Backups** for scheduled system-level protection.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-compute**: Droplets and App Platform storage attachment.
- **digitalocean-containers-images**: Image and registry workflows.
- **digitalocean-managed-databases**: Data backups and migration planning.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Storage: https://docs.digitalocean.com/products/storage/
- Spaces: https://docs.digitalocean.com/products/spaces/
- Volumes: https://docs.digitalocean.com/products/volumes/
- NFS: https://docs.digitalocean.com/products/nfs/
- Snapshots: https://docs.digitalocean.com/products/snapshots/
- Backups: https://docs.digitalocean.com/products/backups/
