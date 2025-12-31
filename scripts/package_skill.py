#!/usr/bin/env python3
"""
Package a skill for deployment to the Claude skills directory.

This script validates and packages individual skills:
1. Validates SKILL.md exists and has proper frontmatter
2. Validates metadata.json exists and has required fields
3. Calculates token counts using tiktoken
4. Copies skill to .claude/skills with flattened name
5. Optionally copies reference files

Usage:
    # Package a single skill
    python scripts/package_skill.py toolchains/python/frameworks/django

    # Package with validation only (no copy)
    python scripts/package_skill.py --validate toolchains/python/frameworks/django

    # Package to custom target
    python scripts/package_skill.py --target ~/.claude/skills toolchains/python/frameworks/django

    # Package all skills matching pattern
    python scripts/package_skill.py --pattern "toolchains/python/*"

    # Force overwrite
    python scripts/package_skill.py --force toolchains/python/frameworks/django

Examples:
    # Validate skill structure
    python scripts/package_skill.py --validate toolchains/rust/frameworks/tauri

    # Package with verbose output
    python scripts/package_skill.py --verbose toolchains/typescript/testing/vitest

    # Dry run to see what would happen
    python scripts/package_skill.py --dry-run toolchains/javascript/frameworks/react
"""

import argparse
import fnmatch
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Optional

try:
    import tiktoken

    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


class SkillValidator:
    """Validate skill structure and content."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.encoding = None

        if HAS_TIKTOKEN:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
            except Exception:
                pass

    def reset(self):
        """Reset errors and warnings for new validation."""
        self.errors = []
        self.warnings = []

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            try:
                return len(self.encoding.encode(text))
            except Exception:
                pass
        # Fallback: estimate ~4 characters per token
        return len(text) // 4

    def validate_skill_md(self, skill_path: Path) -> bool:
        """Validate SKILL.md file."""
        skill_md = skill_path / "SKILL.md"

        if not skill_md.exists():
            self.errors.append(f"SKILL.md not found in {skill_path}")
            return False

        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(f"Cannot read SKILL.md: {e}")
            return False

        # Check frontmatter
        if not content.startswith("---"):
            self.errors.append("SKILL.md missing frontmatter (should start with ---)")
            return False

        # Extract frontmatter
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            self.errors.append("SKILL.md has malformed frontmatter")
            return False

        frontmatter = match.group(1)

        # Check required frontmatter fields
        if "name:" not in frontmatter:
            self.warnings.append("SKILL.md frontmatter missing 'name' field")

        if "description:" not in frontmatter:
            self.warnings.append("SKILL.md frontmatter missing 'description' field")

        # Check for progressive_disclosure section
        if "progressive_disclosure:" not in content:
            self.warnings.append("SKILL.md missing progressive_disclosure section")

        # Check content length
        tokens = self.count_tokens(content)
        if tokens < 100:
            self.warnings.append(f"SKILL.md seems too short ({tokens} tokens)")
        elif tokens > 20000:
            self.warnings.append(
                f"SKILL.md is very large ({tokens} tokens) - consider splitting"
            )

        if self.verbose:
            print(f"  SKILL.md: {tokens} tokens")

        return True

    def validate_metadata_json(self, skill_path: Path) -> Optional[dict]:
        """Validate metadata.json file."""
        metadata_path = skill_path / "metadata.json"

        if not metadata_path.exists():
            self.warnings.append(f"metadata.json not found in {skill_path}")
            return None

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            self.errors.append(f"metadata.json is not valid JSON: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Cannot read metadata.json: {e}")
            return None

        # Check required fields
        required_fields = ["name", "version", "category"]
        for field in required_fields:
            if field not in metadata:
                self.errors.append(f"metadata.json missing required field: {field}")

        # Check recommended fields
        recommended_fields = ["toolchain", "tags", "entry_point_tokens", "full_tokens"]
        for field in recommended_fields:
            if field not in metadata:
                self.warnings.append(
                    f"metadata.json missing recommended field: {field}"
                )

        # Validate version format
        version = metadata.get("version", "")
        if version and not re.match(r"^\d+\.\d+\.\d+$", version):
            self.warnings.append(
                f"metadata.json version '{version}' not in semver format"
            )

        # Validate category
        valid_categories = ["toolchain", "universal", "example"]
        category = metadata.get("category", "")
        if category and category not in valid_categories:
            self.warnings.append(f"metadata.json category '{category}' not recognized")

        if self.verbose:
            print(f"  metadata.json: {json.dumps(metadata, indent=2)[:200]}...")

        return metadata

    def validate_references(self, skill_path: Path) -> list[Path]:
        """Check for reference files."""
        references_dir = skill_path / "references"
        references = []

        if references_dir.exists():
            for ref in references_dir.glob("*.md"):
                references.append(ref)
                if self.verbose:
                    tokens = self.count_tokens(ref.read_text(encoding="utf-8"))
                    print(f"  references/{ref.name}: {tokens} tokens")

        return references

    def validate_skill(self, skill_path: Path) -> bool:
        """Validate a complete skill."""
        self.reset()

        if not skill_path.exists():
            self.errors.append(f"Skill path does not exist: {skill_path}")
            return False

        if not skill_path.is_dir():
            self.errors.append(f"Skill path is not a directory: {skill_path}")
            return False

        if self.verbose:
            print(f"\nValidating: {skill_path}")

        # Validate components
        skill_md_valid = self.validate_skill_md(skill_path)
        metadata = self.validate_metadata_json(skill_path)
        references = self.validate_references(skill_path)

        # Calculate total tokens
        if skill_md_valid:
            skill_content = (skill_path / "SKILL.md").read_text(encoding="utf-8")
            total_tokens = self.count_tokens(skill_content)

            for ref in references:
                total_tokens += self.count_tokens(ref.read_text(encoding="utf-8"))

            if self.verbose:
                print(f"  Total tokens: {total_tokens}")

            # Check if metadata token count is accurate
            if metadata and "full_tokens" in metadata:
                declared = metadata["full_tokens"]
                if abs(declared - total_tokens) > total_tokens * 0.2:
                    self.warnings.append(
                        f"Token count mismatch: declared {declared}, actual {total_tokens}"
                    )

        return len(self.errors) == 0


class SkillPackager:
    """Package skills for deployment."""

    def __init__(self, repo_root: Path, target: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.target = target
        self.verbose = verbose
        self.validator = SkillValidator(verbose)

    def get_flat_name(self, skill_path: Path) -> str:
        """Convert hierarchical path to flat name."""
        try:
            relative = skill_path.relative_to(self.repo_root)
        except ValueError:
            relative = skill_path

        # Convert path separators to dashes
        flat_name = str(relative).replace("/", "-").replace("\\", "-")

        # Remove trailing SKILL.md if present
        flat_name = flat_name.replace("-SKILL.md", "")

        return flat_name

    def package_skill(
        self, skill_path: Path, force: bool = False, dry_run: bool = False
    ) -> bool:
        """Package a single skill."""
        # Validate first
        if not self.validator.validate_skill(skill_path):
            print(f"\n❌ Validation failed for {skill_path}")
            for error in self.validator.errors:
                print(f"   ERROR: {error}")
            return False

        # Show warnings
        if self.validator.warnings:
            for warning in self.validator.warnings:
                print(f"   ⚠️  {warning}")

        # Get flat name
        flat_name = self.get_flat_name(skill_path)
        target_dir = self.target / flat_name

        if self.verbose:
            print(f"\n  Packaging as: {flat_name}")
            print(f"  Target: {target_dir}")

        # Check if exists
        if target_dir.exists() and not force:
            print(f"   Target exists: {target_dir}")
            print("   Use --force to overwrite")
            return False

        if dry_run:
            print(f"   [DRY RUN] Would package to: {target_dir}")
            return True

        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy SKILL.md
        shutil.copy2(skill_path / "SKILL.md", target_dir / "SKILL.md")

        # Copy metadata.json if exists
        metadata_path = skill_path / "metadata.json"
        if metadata_path.exists():
            shutil.copy2(metadata_path, target_dir / "metadata.json")

        # Copy references directory if exists
        references_src = skill_path / "references"
        if references_src.exists():
            references_dst = target_dir / "references"
            if references_dst.exists():
                shutil.rmtree(references_dst)
            shutil.copytree(references_src, references_dst)

        print(f"   ✅ Packaged: {flat_name}")
        return True

    def find_skills(self, pattern: str) -> list[Path]:
        """Find skills matching a pattern."""
        skills = []

        # Search in toolchains, universal, examples
        search_dirs = ["toolchains", "universal", "examples"]

        for search_dir in search_dirs:
            base = self.repo_root / search_dir
            if not base.exists():
                continue

            for skill_md in base.rglob("SKILL.md"):
                skill_path = skill_md.parent
                relative = str(skill_path.relative_to(self.repo_root))

                if fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(
                    relative, f"{pattern}*"
                ):
                    skills.append(skill_path)

        return sorted(set(skills))


def main():
    parser = argparse.ArgumentParser(
        description="Package a skill for deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "skill_path", nargs="?", help="Path to skill directory (relative to repo root)"
    )

    parser.add_argument(
        "--pattern",
        "-p",
        type=str,
        help='Pattern to match multiple skills (e.g., "toolchains/python/*")',
    )

    parser.add_argument(
        "--target",
        "-t",
        type=Path,
        help="Target directory for packaged skills (default: .claude/skills)",
    )

    parser.add_argument(
        "--validate", "-V", action="store_true", help="Validate only, do not package"
    )

    parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing packaged skills"
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without packaging"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    parser.add_argument("--all", "-a", action="store_true", help="Package all skills")

    args = parser.parse_args()

    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Validate repository
    if (
        not (repo_root / "toolchains").exists()
        and not (repo_root / "universal").exists()
    ):
        print(
            f"Error: Not a valid claude-mpm-skills repository: {repo_root}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Determine target
    target = args.target or (repo_root / ".claude" / "skills")

    # Create packager
    packager = SkillPackager(repo_root, target, args.verbose)

    # Determine skills to process
    skills_to_process: list[Path] = []

    if args.all:
        skills_to_process = packager.find_skills("*")
    elif args.pattern:
        skills_to_process = packager.find_skills(args.pattern)
    elif args.skill_path:
        skill_path = repo_root / args.skill_path
        if not skill_path.exists():
            # Try without leading slash
            skill_path = repo_root / args.skill_path.lstrip("/")
        if skill_path.exists():
            skills_to_process = [skill_path]
        else:
            print(f"Error: Skill path not found: {args.skill_path}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    if not skills_to_process:
        print("No skills found to process")
        sys.exit(1)

    print(f"\n🔧 Processing {len(skills_to_process)} skill(s)...")

    if args.validate:
        print("   Mode: Validation only\n")
    elif args.dry_run:
        print("   Mode: Dry run\n")
    else:
        print(f"   Target: {target}\n")

    success_count = 0
    error_count = 0

    for skill_path in skills_to_process:
        relative = skill_path.relative_to(repo_root)
        print(f"\n📦 {relative}")

        if args.validate:
            # Validation only
            if packager.validator.validate_skill(skill_path):
                print("   ✅ Valid")
                success_count += 1
            else:
                for error in packager.validator.errors:
                    print(f"   ❌ {error}")
                error_count += 1

            for warning in packager.validator.warnings:
                print(f"   ⚠️  {warning}")
        else:
            # Package
            if packager.package_skill(skill_path, args.force, args.dry_run):
                success_count += 1
            else:
                error_count += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Summary: {success_count} successful, {error_count} failed")

    if error_count > 0:
        sys.exit(1)

    if not args.validate and not args.dry_run:
        print(f"\n✅ Skills packaged to: {target}")
        print("\nNext steps:")
        print("  - Verify deployment with: ls -la .claude/skills/")
        print("  - Run manifest generator: python scripts/generate_manifest.py")


if __name__ == "__main__":
    main()
