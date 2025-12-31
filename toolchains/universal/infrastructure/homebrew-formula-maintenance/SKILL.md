---
name: homebrew-formula-maintenance
description: Homebrew formula maintenance workflows for Python CLIs and taps, including version bumps, SHA/resource updates, testing, audits, and releases.
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Maintain Homebrew Python formulas: bump version/sha, refresh resources, test install, audit/style, and push tap updates."
    when_to_use: "Updating Homebrew tap formulas for Python CLIs, syncing PyPI releases, or automating tap updates in CI."
    quick_start: "1. Verify PyPI release exists 2. Update url+sha in Formula 3. Regenerate resources if needed 4. brew install --build-from-source + brew test + brew audit"
tags:
  - homebrew
  - formula
  - tap
  - python
  - pypi
  - release
  - ci
---

# Homebrew Formula Maintenance

## Overview

Use this workflow to keep Homebrew formulas in sync with PyPI releases for Python CLIs. The pattern in your taps is: update version + sha, refresh resource blocks when needed, run brew install/test/audit, then push the tap update (manually or via CI).

## Quick Start (manual bump)

1. Verify the PyPI release exists and grab the sdist URL + SHA256.
2. Update the `url` and `sha256` in the formula.
3. Refresh `resource` stanzas if the formula uses `virtualenv_install_with_resources`.
4. Test: `brew install --build-from-source` + `brew test` + `brew audit --strict`.
5. Update changelog/tag and push the tap repo.

## Local Scripts You Already Use

- `homebrew-claude-mpm/scripts/update_formula.sh <version>`
  - Verifies PyPI, updates url/sha, regenerates resources, optional brew test/audit.
- `homebrew-claude-mpm/scripts/generate_resources.py`
  - Emits Python dependency `resource` blocks from PyPI.
- `homebrew-claude-mpm/scripts/test_formula.sh`
  - End-to-end brew install/test/audit/style.
- `mcp-vector-search/scripts/update_homebrew_formula.py`
  - End-to-end tap update with `--dry-run`, `--version`, `--tap-repo-path` and `HOMEBREW_TAP_TOKEN`.

## Standard Workflow

### 1. Confirm PyPI Release

- Check the sdist is available and capture URL/SHA.
- Typical command: `curl -s https://pypi.org/pypi/<package>/<version>/json`.

### 2. Update Formula URL + SHA

- Replace `url` and `sha256` in `Formula/<name>.rb`.
- Keep the formula version implicit via the sdist URL (your taps do this).

### 3. Refresh Resources (Python Virtualenv Formula)

If the formula uses `Language::Python::Virtualenv` and `virtualenv_install_with_resources`:

- Regenerate `resource` stanzas after dependency changes.
- Use `generate_resources.py` or equivalent; review output before pasting.

### 4. Test and Audit

Run these in the tap repo:

```bash
brew install --build-from-source ./Formula/<name>.rb
brew test <name>
brew audit --strict ./Formula/<name>.rb
brew style ./Formula/<name>.rb
```

### 5. Commit and Push

- Update `CHANGELOG.md` if the tap repo tracks releases.
- Commit, tag, and push as required by the tap workflow.

## Formula Patterns (From Your Taps)

### Full Virtualenv Formula (claude-mpm)

- `include Language::Python::Virtualenv`
- `virtualenv_install_with_resources`
- Large `resource` blocks to pin dependencies
- `test do` uses CLI commands like `--version` and subcommands

### Minimal Venv Formula (mcp-vector-search)

- Create venv explicitly and `pip install -v buildpath`
- `bin.install_symlink` for CLI entrypoint
- Minimal `test do` uses `--version` and `--help`

## CI Automation Pattern

Your GitHub Actions workflow for Homebrew updates follows this flow:

- Trigger on tag or `workflow_run` after CI succeeds.
- Run `scripts/update_homebrew_formula.py`.
- Require `HOMEBREW_TAP_TOKEN` (and optional `HOMEBREW_TAP_REPO`).
- On failure, open an issue with manual update steps.

## Troubleshooting

- **PyPI release missing**: verify tag push and publish step completed.
- **SHA mismatch**: re-fetch sdist SHA from PyPI JSON.
- **brew audit failures**: confirm dependency resource blocks match the sdist and `python@x.y` dependency is present.
- **Install failures**: verify `python@x.y` dependency and `virtualenv_install_with_resources` usage.

## Related Skills

- `toolchains/universal/infrastructure/github-actions`
- `toolchains/universal/infrastructure/docker`
