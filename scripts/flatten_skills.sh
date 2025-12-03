#!/usr/bin/env bash

# flatten_skills.sh - Deploy hierarchical skills to flat directory structure
#
# This script auto-discovers all skills from toolchains/, universal/, and examples/
# directories, transforms their paths to flat names, and copies required files to
# the target deployment directory.
#
# Usage:
#   ./flatten_skills.sh                           # Deploy to .claude/skills
#   ./flatten_skills.sh --target ~/.claude/skills # Custom target
#   ./flatten_skills.sh --dry-run                 # Show what would be deployed
#   ./flatten_skills.sh --force                   # Overwrite existing files
#   ./flatten_skills.sh --verbose                 # Detailed output
#   ./flatten_skills.sh --help                    # Show usage information

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_TARGET="$PROJECT_ROOT/.claude/skills"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Default options
TARGET_DIR="$DEFAULT_TARGET"
DRY_RUN=false
FORCE=false
VERBOSE=false

# Global arrays
DISCOVERED_SKILLS=()

# Statistics
SKILLS_DEPLOYED=0
FILES_COPIED=0
REFERENCES_PRESERVED=0
ERRORS=0
WARNINGS=0

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_color() {
    local color="$1"
    shift
    echo -e "${color}$*${RESET}"
}

print_error() {
    print_color "$RED" "❌ ERROR: $*" >&2
    ((ERRORS++))
}

print_warning() {
    print_color "$YELLOW" "⚠️  WARNING: $*" >&2
    ((WARNINGS++))
}

print_success() {
    print_color "$GREEN" "$*"
}

print_info() {
    print_color "$CYAN" "$*"
}

print_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        print_color "$BLUE" "   ℹ️  $*"
    fi
}

show_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Deploy hierarchical skills to flat directory structure for Claude.

OPTIONS:
    --target DIR        Target directory for deployment (default: .claude/skills)
    --dry-run           Show what would be deployed without making changes
    --force             Overwrite existing files in target directory
    --verbose           Show detailed output during deployment
    --help              Show this help message

EXAMPLES:
    # Deploy to default location
    $(basename "$0")

    # Deploy to custom location
    $(basename "$0") --target ~/.claude/skills

    # Preview deployment without making changes
    $(basename "$0") --dry-run

    # Force overwrite existing deployment
    $(basename "$0") --force --verbose

EXIT CODES:
    0   Success
    1   Error occurred during deployment

DESCRIPTION:
    This script discovers all skills from toolchains/, universal/, and examples/
    directories, transforms hierarchical paths to flat names (e.g.,
    'toolchains/python/frameworks/django' becomes 'toolchains-python-frameworks-django'),
    and copies SKILL.md, metadata.json, and references/ (if present) to the target.

    Files excluded: .etag_cache.json, .DS_Store, hidden files (.*), README.md
EOF
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

validate_environment() {
    print_verbose "Validating environment..."

    # Check source directories exist
    local source_dirs=("$PROJECT_ROOT/toolchains" "$PROJECT_ROOT/universal" "$PROJECT_ROOT/examples")
    for dir in "${source_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            print_error "Source directory not found: $dir"
            return 1
        fi
        print_verbose "Found source directory: $dir"
    done

    # Check if target directory exists (when not dry-run and not force)
    if [[ "$DRY_RUN" == "false" && "$FORCE" == "false" && -d "$TARGET_DIR" ]]; then
        local existing_count
        existing_count=$(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
        if [[ "$existing_count" -gt 0 ]]; then
            print_error "Target directory already exists with $existing_count skills: $TARGET_DIR"
            print_info "Use --force to overwrite or choose a different --target"
            return 1
        fi
    fi

    # Check target parent directory is writable
    local target_parent
    target_parent="$(dirname "$TARGET_DIR")"
    if [[ ! -d "$target_parent" ]]; then
        print_error "Target parent directory does not exist: $target_parent"
        return 1
    fi
    if [[ ! -w "$target_parent" ]]; then
        print_error "Target parent directory is not writable: $target_parent"
        return 1
    fi

    print_verbose "Environment validation passed"
    return 0
}

# ============================================================================
# DISCOVERY FUNCTIONS
# ============================================================================

discover_skills() {
    print_verbose "Discovering skills..."

    # Find all SKILL.md files in toolchains/, universal/, and examples/
    # Output to global DISCOVERED_SKILLS array
    DISCOVERED_SKILLS=()
    while IFS= read -r -d '' skill_file; do
        DISCOVERED_SKILLS+=("$skill_file")
    done < <(find "$PROJECT_ROOT/toolchains" "$PROJECT_ROOT/universal" "$PROJECT_ROOT/examples" \
        -type f -name "SKILL.md" -print0 2>/dev/null)

    print_verbose "Discovered ${#DISCOVERED_SKILLS[@]} skills"
}

# ============================================================================
# PATH TRANSFORMATION
# ============================================================================

transform_path_to_flat_name() {
    local skill_path="$1"
    local skill_dir
    skill_dir="$(dirname "$skill_path")"

    # Get relative path from project root
    local rel_path="${skill_dir#$PROJECT_ROOT/}"

    # Replace / with - to create flat name
    local flat_name="${rel_path//\//-}"

    echo "$flat_name"
}

# ============================================================================
# DEPLOYMENT FUNCTIONS
# ============================================================================

copy_file_if_exists() {
    local source="$1"
    local dest="$2"
    local file_type="$3"

    if [[ -f "$source" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            print_verbose "Would copy $file_type: $(basename "$source")"
        else
            cp "$source" "$dest"
            print_verbose "Copied $file_type: $(basename "$source")"
        fi
        ((FILES_COPIED++))
        return 0
    else
        return 1
    fi
}

copy_references_if_exists() {
    local source_dir="$1"
    local dest_dir="$2"
    local ref_dir="$source_dir/references"

    if [[ -d "$ref_dir" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            local ref_count
            ref_count=$(find "$ref_dir" -type f ! -name ".*" ! -name ".DS_Store" | wc -l | tr -d ' ')
            print_verbose "Would copy references/ directory ($ref_count files)"
        else
            # Copy references directory, excluding hidden files and .DS_Store
            mkdir -p "$dest_dir/references"
            find "$ref_dir" -type f ! -name ".*" ! -name ".DS_Store" -exec cp {} "$dest_dir/references/" \;
            local copied_count
            copied_count=$(find "$dest_dir/references" -type f | wc -l | tr -d ' ')
            print_verbose "Copied references/ directory ($copied_count files)"
            FILES_COPIED=$((FILES_COPIED + copied_count))
        fi
        ((REFERENCES_PRESERVED++))
        return 0
    fi
    return 1
}

deploy_skill() {
    local skill_path="$1"
    local index="$2"
    local total="$3"

    local skill_dir
    skill_dir="$(dirname "$skill_path")"

    local flat_name
    flat_name="$(transform_path_to_flat_name "$skill_path")"

    local target_skill_dir="$TARGET_DIR/$flat_name"

    # Progress indicator
    printf "[%d/%d] %s " "$index" "$total" "$flat_name"

    # Validate required file exists
    if [[ ! -f "$skill_path" ]]; then
        print_error "SKILL.md not found: $skill_path"
        echo "✗"
        return 1
    fi

    # Create target directory
    if [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$target_skill_dir"
    fi

    # Copy SKILL.md (required)
    if ! copy_file_if_exists "$skill_path" "$target_skill_dir/SKILL.md" "SKILL.md"; then
        print_error "Failed to find SKILL.md in: $skill_dir"
        echo "✗"
        return 1
    fi

    # Copy metadata.json (optional, warning if missing)
    if ! copy_file_if_exists "$skill_dir/metadata.json" "$target_skill_dir/metadata.json" "metadata.json"; then
        print_warning "metadata.json not found in: $flat_name"
    fi

    # Copy references/ directory if exists
    copy_references_if_exists "$skill_dir" "$target_skill_dir" || true

    ((SKILLS_DEPLOYED++))
    print_success "✓"
    return 0
}

# ============================================================================
# MAIN DEPLOYMENT LOGIC
# ============================================================================

deploy_all_skills() {
    discover_skills

    local total="${#DISCOVERED_SKILLS[@]}"

    if [[ "$total" -eq 0 ]]; then
        print_error "No skills found to deploy"
        return 1
    fi

    # Create target directory if needed
    if [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$TARGET_DIR"
    fi

    # Deploy each skill
    local index=1
    for skill_path in "${DISCOVERED_SKILLS[@]}"; do
        deploy_skill "$skill_path" "$index" "$total"
        ((index++))
    done

    return 0
}

generate_manifest() {
    if [[ "$DRY_RUN" == "true" ]]; then
        return 0
    fi

    local manifest_file="$TARGET_DIR/.deployment_manifest"

    cat > "$manifest_file" << EOF
# Skill Deployment Manifest
# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
# Source: $PROJECT_ROOT
# Target: $TARGET_DIR
# Skills Deployed: $SKILLS_DEPLOYED
# Files Copied: $FILES_COPIED
# References Preserved: $REFERENCES_PRESERVED
# Script Version: 1.0.0
EOF

    print_verbose "Generated deployment manifest: $manifest_file"
}

# ============================================================================
# SUMMARY OUTPUT
# ============================================================================

print_summary() {
    echo ""
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "🔍 Dry-Run Summary:"
    else
        print_success "✅ Deployment Summary:"
    fi

    echo "   - Skills deployed: $SKILLS_DEPLOYED"
    echo "   - Files copied: $FILES_COPIED"
    echo "   - References preserved: $REFERENCES_PRESERVED"
    echo "   - Target: $TARGET_DIR"

    if [[ "$WARNINGS" -gt 0 ]]; then
        print_warning "Warnings: $WARNINGS"
    fi

    if [[ "$ERRORS" -gt 0 ]]; then
        print_error "Errors: $ERRORS"
    fi

    echo ""
}

# ============================================================================
# COMMAND LINE PARSING
# ============================================================================

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --target)
                TARGET_DIR="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Make target directory absolute
    TARGET_DIR="$(cd "$(dirname "$TARGET_DIR")" 2>/dev/null && pwd)/$(basename "$TARGET_DIR")" || true
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    parse_arguments "$@"

    # Print header
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "🔍 Dry-run: Flattening skills for deployment..."
    else
        print_info "🔄 Flattening skills for deployment..."
    fi
    echo "Source: $PROJECT_ROOT"
    echo "Target: $TARGET_DIR"
    echo ""

    # Validate environment
    if ! validate_environment; then
        print_error "Environment validation failed"
        exit 1
    fi

    # Deploy skills
    if ! deploy_all_skills; then
        print_error "Deployment failed"
        print_summary
        exit 1
    fi

    # Generate manifest
    generate_manifest

    # Print summary
    print_summary

    if [[ "$ERRORS" -gt 0 ]]; then
        exit 1
    fi

    exit 0
}

# Run main function
main "$@"
