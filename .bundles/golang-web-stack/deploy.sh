#!/usr/bin/env bash
# Bundle Deployment Script Template
# Version: 1.0.0
# Usage: ./deploy.sh [--flat|--hierarchical|--validate] [target_dir]

set -euo pipefail

# Configuration
BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUNDLE_NAME="$(basename "$BUNDLE_DIR")"
SKILLS_LIST="$BUNDLE_DIR/skills.list"
REPO_ROOT="$(cd "$BUNDLE_DIR/../.." && pwd)"

# Default values
MODE="${1:---flat}"
TARGET_DIR="${2:-$HOME/.claude}"
VALIDATE_ONLY=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# Parse arguments
case "$MODE" in
    --validate)
        VALIDATE_ONLY=true
        ;;
    --flat|--hierarchical)
        # Valid modes
        ;;
    *)
        log_error "Invalid mode: $MODE"
        echo "Usage: $0 [--flat|--hierarchical|--validate] [target_dir]"
        exit 1
        ;;
esac

log_info "Bundle: $BUNDLE_NAME"
log_info "Mode: $MODE"
log_info "Target: $TARGET_DIR"
echo

# Validate skills.list exists
if [[ ! -f "$SKILLS_LIST" ]]; then
    log_error "skills.list not found: $SKILLS_LIST"
    exit 1
fi

# Parse skills.list (skip comments and empty lines)
declare -a SKILLS=()
declare -a MISSING_SKILLS=()
declare -a FOUND_SKILLS=()

while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue

    # Parse skill path (format: path/to/skill:version or path/to/skill)
    skill_path="${line%%:*}"
    skill_version="${line#*:}"
    [[ "$skill_version" == "$skill_path" ]] && skill_version="latest"

    SKILLS+=("$skill_path|$skill_version")

    # Validate skill exists in repo
    skill_full_path="$REPO_ROOT/$skill_path"
    if [[ -d "$skill_full_path" ]]; then
        FOUND_SKILLS+=("$skill_path")
        log_success "Found: $skill_path"
    else
        MISSING_SKILLS+=("$skill_path")
        log_error "Missing: $skill_path"
    fi
done < "$SKILLS_LIST"

echo
log_info "Summary: ${#FOUND_SKILLS[@]} found, ${#MISSING_SKILLS[@]} missing"
echo

# Exit if validation only
if [[ "$VALIDATE_ONLY" == "true" ]]; then
    if [[ ${#MISSING_SKILLS[@]} -gt 0 ]]; then
        log_error "Validation failed: ${#MISSING_SKILLS[@]} missing skills"
        exit 1
    fi
    log_success "Validation passed: all skills found"
    exit 0
fi

# Exit if skills are missing
if [[ ${#MISSING_SKILLS[@]} -gt 0 ]]; then
    log_error "Cannot deploy: ${#MISSING_SKILLS[@]} skills missing"
    exit 1
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Deploy skills
log_info "Deploying ${#SKILLS[@]} skills to $TARGET_DIR"
echo

deployed_count=0
skipped_count=0

for skill_entry in "${SKILLS[@]}"; do
    skill_path="${skill_entry%%|*}"
    skill_version="${skill_entry#*|}"

    source_path="$REPO_ROOT/$skill_path"
    skill_name="$(basename "$skill_path")"

    if [[ "$MODE" == "--flat" ]]; then
        # Flat deployment: copy directly to target
        target_path="$TARGET_DIR/$skill_name"
    else
        # Hierarchical deployment: preserve directory structure
        target_path="$TARGET_DIR/$skill_path"
    fi

    # Check if already deployed
    if [[ -d "$target_path" ]]; then
        log_warning "Skipped: $skill_name (already exists)"
        ((skipped_count++))
        continue
    fi

    # Create parent directory if needed
    mkdir -p "$(dirname "$target_path")"

    # Copy skill
    cp -r "$source_path" "$target_path"
    log_success "Deployed: $skill_name → $target_path"
    ((deployed_count++))
done

echo
log_info "Deployment complete"
log_success "Deployed: $deployed_count skills"
[[ $skipped_count -gt 0 ]] && log_warning "Skipped: $skipped_count skills (already exist)"

# Create deployment manifest
manifest_file="$TARGET_DIR/.bundle-manifest-$BUNDLE_NAME.json"
cat > "$manifest_file" << EOF
{
  "bundle": "$BUNDLE_NAME",
  "mode": "$MODE",
  "deployed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "skills_count": ${#SKILLS[@]},
  "deployed_count": $deployed_count,
  "skipped_count": $skipped_count,
  "target_dir": "$TARGET_DIR"
}
EOF

log_success "Manifest created: $manifest_file"
echo
log_success "Bundle '$BUNDLE_NAME' deployed successfully!"

