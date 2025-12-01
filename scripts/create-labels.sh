#!/bin/bash
# GitHub label creation script for claude-mpm-skills
# Requires: GitHub CLI (gh) - Install: https://cli.github.com/
# Usage: bash scripts/create-labels.sh

set -e

echo "🏷️  Creating labels for claude-mpm-skills..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

echo "Creating Priority Labels..."
gh label create "🟥 priority: critical" --color b60205 --description "Must be fixed ASAP - broken core functionality" --force
gh label create "🟧 priority: high" --color d93f0b --description "Blocks dependent work or affects many users" --force
gh label create "🟨 priority: medium" --color fbca04 --description "Important but non-blocking" --force
gh label create "🟩 priority: low" --color cfda2c --description "Nice to have, no rush" --force

echo "Creating Status Labels..."
gh label create "🚦 status: triage" --color eeeeee --description "Needs initial review and labeling" --force
gh label create "🔍 status: needs-info" --color d4c5f9 --description "Awaiting information from reporter" --force
gh label create "🚧 status: blocked" --color 333333 --description "Cannot proceed due to dependency" --force
gh label create "🏁 status: ready" --color 0e8a16 --description "Ready for implementation" --force
gh label create "👀 status: in-review" --color fbca04 --description "Under active review" --force
gh label create "⛔ status: wontfix" --color ffffff --description "Rejected/out of scope" --force
gh label create "✅ status: done" --color 1d76db --description "Completed (before closing)" --force

echo "Creating Type Labels..."
gh label create "🐛 type: bug" --color d73a4a --description "Something isn't working correctly" --force
gh label create "✨ type: enhancement" --color a2eeef --description "Improvement to existing feature" --force
gh label create "🚀 type: new-skill" --color 0075ca --description "Proposal for new skill" --force
gh label create "📖 type: documentation" --color 0075ca --description "Documentation improvements" --force
gh label create "🔧 type: tooling" --color d4c5f9 --description "CI/CD, scripts, automation" --force
gh label create "💬 type: question" --color d876e3 --description "User question or clarification" --force
gh label create "🎨 type: design" --color e99695 --description "UI/UX, repository structure" --force

echo "Creating Skill Category Labels..."
gh label create "skill: python" --color 3572A5 --description "Python skills" --force
gh label create "skill: typescript" --color 2b7489 --description "TypeScript skills" --force
gh label create "skill: javascript" --color f1e05a --description "JavaScript skills" --force
gh label create "skill: nextjs" --color 000000 --description "Next.js skills" --force
gh label create "skill: ui" --color 563d7c --description "UI/styling skills" --force
gh label create "skill: ai" --color ff6f00 --description "AI/ML skills" --force
gh label create "skill: platform" --color 89e051 --description "Platform/deployment skills" --force
gh label create "skill: universal" --color ededed --description "Universal skills" --force

echo "Creating Effort Labels..."
gh label create "effort: small" --color c2e0c6 --description "< 2 hours of work" --force
gh label create "effort: medium" --color fef2c0 --description "2-8 hours of work" --force
gh label create "effort: large" --color f9d0c4 --description "1-3 days of work" --force
gh label create "effort: epic" --color d93f0b --description "Multi-day or requires research" --force

echo "Creating Community Labels..."
gh label create "good first issue" --color 7057ff --description "Good for newcomers (GitHub recognized)" --force
gh label create "help wanted" --color 008672 --description "Maintainer requests community help (GitHub recognized)" --force
gh label create "🔒 staff only" --color d73a4a --description "Requires maintainer privileges" --force
gh label create "duplicate" --color cfd3d7 --description "Duplicate of another issue" --force
gh label create "invalid" --color e4e669 --description "Invalid issue (spam, off-topic)" --force

echo "Creating Automated Labels..."
gh label create "🤖 auto: validation-failed" --color b60205 --description "CI validation checks failed" --force
gh label create "🤖 auto: sensitive-data" --color d73a4a --description "Potential credentials detected" --force
gh label create "🤖 auto: manifest-error" --color d93f0b --description "manifest.json validation failed" --force

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "📊 Summary:"
echo "  - Priority labels: 4"
echo "  - Status labels: 7"
echo "  - Type labels: 7"
echo "  - Skill category labels: 8"
echo "  - Effort labels: 4"
echo "  - Community labels: 5"
echo "  - Automated labels: 3"
echo "  ────────────────────"
echo "  Total: 40 labels"
echo ""
echo "🎯 Next steps:"
echo "  1. Review labels in GitHub: Issues → Labels"
echo "  2. Configure auto-labeling workflow (see docs/GITHUB_REPOSITORY_SETUP.md)"
echo "  3. Train team on label usage guidelines"
