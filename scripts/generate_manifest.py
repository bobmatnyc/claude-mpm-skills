#!/usr/bin/env python3
"""
Generate correct manifest.json for all skills in the repository.

This script:
1. Discovers all SKILL.md files
2. Extracts metadata from metadata.json and SKILL.md frontmatter
3. Calculates token counts using tiktoken
4. Extracts git history for last modification dates
5. Validates all paths and metadata
6. Generates a complete, correct manifest.json

Usage:
    python scripts/generate_manifest.py --output manifest.json
    python scripts/generate_manifest.py --validate
    python scripts/generate_manifest.py --dry-run
    python scripts/generate_manifest.py --verbose
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False
    print("Warning: tiktoken not available. Token counts will be estimated.", file=sys.stderr)


class SkillDiscovery:
    """Discover all SKILL.md files in the repository."""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.encoding = None

        if HAS_TIKTOKEN:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
            except Exception as e:
                print(f"Warning: Failed to load tiktoken encoding: {e}", file=sys.stderr)

    def find_all_skills(self) -> List[Path]:
        """Find all SKILL.md files in universal/ and toolchains/ directories."""
        skill_files = []

        # Search universal/ directory
        universal_dir = self.repo_root / "universal"
        if universal_dir.exists():
            skill_files.extend(universal_dir.rglob("SKILL.md"))

        # Search toolchains/ directory
        toolchains_dir = self.repo_root / "toolchains"
        if toolchains_dir.exists():
            skill_files.extend(toolchains_dir.rglob("SKILL.md"))

        # Search examples/ directory
        examples_dir = self.repo_root / "examples"
        if examples_dir.exists():
            skill_files.extend(examples_dir.rglob("SKILL.md"))

        # Exclude .claude/skills deployment directory
        skill_files = [
            f for f in skill_files
            if ".claude/skills" not in str(f)
        ]

        if self.verbose:
            print(f"Found {len(skill_files)} SKILL.md files")

        return sorted(skill_files)

    def extract_frontmatter(self, skill_path: Path) -> Dict[str, Any]:
        """Extract YAML frontmatter from SKILL.md file."""
        try:
            content = skill_path.read_text(encoding="utf-8")

            # Match YAML frontmatter: ---\n...\n---
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            frontmatter = {}

            # Simple YAML parser (handles basic key: value pairs)
            for line in frontmatter_text.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    frontmatter[key] = value

            return frontmatter
        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to extract frontmatter from {skill_path}: {e}", file=sys.stderr)
            return {}

    def load_metadata_json(self, skill_dir: Path) -> Dict[str, Any]:
        """Load metadata.json if it exists in skill directory."""
        metadata_path = skill_dir / "metadata.json"
        if metadata_path.exists():
            try:
                return json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Failed to parse {metadata_path}: {e}", file=sys.stderr)
        return {}

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken or estimate."""
        if self.encoding:
            try:
                return len(self.encoding.encode(text))
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Token counting failed: {e}", file=sys.stderr)

        # Fallback: estimate ~4 characters per token
        return len(text) // 4

    def calculate_token_counts(self, skill_path: Path) -> Tuple[int, int]:
        """Calculate entry point and full token counts."""
        try:
            # Entry point: just SKILL.md
            entry_content = skill_path.read_text(encoding="utf-8")
            entry_tokens = self.count_tokens(entry_content)

            # Full: SKILL.md + all reference files
            full_tokens = entry_tokens
            skill_dir = skill_path.parent

            # Add reference files
            references_dir = skill_dir / "references"
            if references_dir.exists():
                for ref_file in references_dir.rglob("*.md"):
                    try:
                        ref_content = ref_file.read_text(encoding="utf-8")
                        full_tokens += self.count_tokens(ref_content)
                    except Exception:
                        pass

            # Add examples
            examples_dir = skill_dir / "examples"
            if examples_dir.exists():
                for ex_file in examples_dir.rglob("*.md"):
                    try:
                        ex_content = ex_file.read_text(encoding="utf-8")
                        full_tokens += self.count_tokens(ex_content)
                    except Exception:
                        pass

            return entry_tokens, full_tokens
        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to calculate tokens for {skill_path}: {e}", file=sys.stderr)
            return 0, 0

    def get_git_last_modified(self, skill_path: Path) -> str:
        """Get last git commit date for file, fallback to mtime."""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ad", "--date=short", "--", str(skill_path)],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception as e:
            if self.verbose:
                print(f"Warning: Git command failed for {skill_path}: {e}", file=sys.stderr)

        # Fallback to file modification time
        try:
            mtime = skill_path.stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except Exception:
            return datetime.now().strftime("%Y-%m-%d")

    def get_relative_path(self, skill_path: Path) -> str:
        """Get path relative to repo root."""
        try:
            return str(skill_path.relative_to(self.repo_root))
        except ValueError:
            return str(skill_path)

    def classify_skill(self, relative_path: str) -> Dict[str, Optional[str]]:
        """Classify skill by category, toolchain, and framework."""
        parts = relative_path.split('/')

        if parts[0] == 'universal':
            return {
                'category': 'universal',
                'toolchain': None,
                'framework': None
            }
        elif parts[0] == 'toolchains':
            toolchain = parts[1] if len(parts) > 1 else None
            framework = None

            # Try to extract framework from path
            if len(parts) > 3 and parts[2] == 'frameworks':
                framework = parts[3]
            elif len(parts) > 2:
                # Framework might be in skill directory name
                skill_dir = parts[-2]
                # Common framework patterns
                framework_patterns = [
                    'django', 'flask', 'fastapi', 'tauri', 'react',
                    'nextjs', 'express', 'vue', 'angular', 'svelte'
                ]
                for pattern in framework_patterns:
                    if pattern in skill_dir.lower():
                        framework = pattern
                        break

            return {
                'category': 'toolchain',
                'toolchain': toolchain,
                'framework': framework
            }
        elif parts[0] == 'examples':
            return {
                'category': 'example',
                'toolchain': None,
                'framework': None
            }

        return {
            'category': 'unknown',
            'toolchain': None,
            'framework': None
        }

    def check_references(self, skill_dir: Path) -> Tuple[bool, List[str]]:
        """Check if skill has reference files."""
        references = []

        # Check references/ directory
        references_dir = skill_dir / "references"
        if references_dir.exists():
            for ref_file in sorted(references_dir.rglob("*.md")):
                references.append(ref_file.name)

        # Check examples/ directory
        examples_dir = skill_dir / "examples"
        if examples_dir.exists():
            for ex_file in sorted(examples_dir.rglob("*.md")):
                references.append(f"examples/{ex_file.name}")

        has_references = len(references) > 0
        return has_references, references

    def extract_skill_metadata(self, skill_path: Path) -> Dict[str, Any]:
        """Extract complete metadata for a skill."""
        skill_dir = skill_path.parent
        relative_path = self.get_relative_path(skill_path)

        # Load metadata from various sources
        metadata_json = self.load_metadata_json(skill_dir)
        frontmatter = self.extract_frontmatter(skill_path)
        classification = self.classify_skill(relative_path)

        # Extract skill name from directory
        skill_name = skill_dir.name

        # Get token counts
        entry_tokens, full_tokens = self.calculate_token_counts(skill_path)

        # Get last modified date
        updated = self.get_git_last_modified(skill_path)

        # Check for references
        has_references, reference_files = self.check_references(skill_dir)

        # Build skill entry
        skill = {
            'name': metadata_json.get('name', skill_name),
            'version': metadata_json.get('version', '1.0.0'),
            'category': classification['category'],
            'toolchain': classification['toolchain'],
            'framework': classification['framework'],
            'tags': metadata_json.get('tags', []),
            'entry_point_tokens': metadata_json.get('entry_point_tokens', entry_tokens),
            'full_tokens': metadata_json.get('full_tokens', full_tokens),
            'requires': metadata_json.get('requires', []),
            'author': metadata_json.get('author', 'Claude MPM Team'),
            'updated': updated,
            'source_path': relative_path
        }

        # Add optional fields
        if has_references:
            skill['has_references'] = True
            skill['reference_files'] = reference_files

        return skill


class ManifestValidator:
    """Validate manifest structure and contents."""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_path(self, source_path: str) -> bool:
        """Validate that source_path exists and has correct format."""
        # Check format
        if not (source_path.startswith('universal/') or
                source_path.startswith('toolchains/') or
                source_path.startswith('examples/')):
            self.errors.append(f"Invalid path prefix: {source_path}")
            return False

        if not source_path.endswith('/SKILL.md'):
            self.errors.append(f"Path doesn't end with /SKILL.md: {source_path}")
            return False

        # Check existence
        full_path = self.repo_root / source_path
        if not full_path.exists():
            self.errors.append(f"Path doesn't exist: {source_path}")
            return False

        return True

    def validate_skill(self, skill: Dict[str, Any]) -> bool:
        """Validate a single skill entry."""
        valid = True

        # Required fields
        required_fields = ['name', 'version', 'category', 'source_path',
                          'entry_point_tokens', 'full_tokens', 'updated']
        for field in required_fields:
            if field not in skill:
                self.errors.append(f"Missing required field '{field}' in skill: {skill.get('name', 'unknown')}")
                valid = False

        # Validate path
        if 'source_path' in skill:
            if not self.validate_path(skill['source_path']):
                valid = False

        # Validate category
        if skill.get('category') not in ['universal', 'toolchain', 'example']:
            self.errors.append(f"Invalid category '{skill.get('category')}' for skill: {skill.get('name')}")
            valid = False

        # Validate token counts
        entry_tokens = skill.get('entry_point_tokens', 0)
        full_tokens = skill.get('full_tokens', 0)

        if entry_tokens < 10 or entry_tokens > 200:
            self.warnings.append(f"Unusual entry_point_tokens ({entry_tokens}) for skill: {skill.get('name')}")

        if full_tokens < 100 or full_tokens > 50000:
            self.warnings.append(f"Unusual full_tokens ({full_tokens}) for skill: {skill.get('name')}")

        if entry_tokens > full_tokens:
            self.errors.append(f"entry_point_tokens > full_tokens for skill: {skill.get('name')}")
            valid = False

        # Validate version format
        version = skill.get('version', '')
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            self.warnings.append(f"Invalid version format '{version}' for skill: {skill.get('name')}")

        # Validate date format
        updated = skill.get('updated', '')
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', updated):
            self.errors.append(f"Invalid date format '{updated}' for skill: {skill.get('name')}")
            valid = False

        return valid

    def check_duplicates(self, skills: List[Dict[str, Any]]) -> bool:
        """Check for duplicate skill names."""
        names = [skill['name'] for skill in skills]
        duplicates = [name for name in names if names.count(name) > 1]

        if duplicates:
            unique_duplicates = sorted(set(duplicates))
            self.errors.append(f"Duplicate skill names found: {', '.join(unique_duplicates)}")
            return False

        return True

    def validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        """Validate complete manifest structure."""
        valid = True

        # Check top-level structure
        required_top_level = ['version', 'repository', 'updated', 'skills', 'metadata', 'provenance']
        for field in required_top_level:
            if field not in manifest:
                self.errors.append(f"Missing top-level field: {field}")
                valid = False

        # Validate skills section
        if 'skills' in manifest:
            skills_section = manifest['skills']

            if 'universal' not in skills_section:
                self.errors.append("Missing 'skills.universal' section")
                valid = False
            else:
                universal_skills = skills_section['universal']
                for skill in universal_skills:
                    if not self.validate_skill(skill):
                        valid = False
                if not self.check_duplicates(universal_skills):
                    valid = False

            if 'toolchains' not in skills_section:
                self.errors.append("Missing 'skills.toolchains' section")
                valid = False
            else:
                toolchains = skills_section['toolchains']
                for toolchain_name, toolchain_skills in toolchains.items():
                    for skill in toolchain_skills:
                        if not self.validate_skill(skill):
                            valid = False
                    if not self.check_duplicates(toolchain_skills):
                        valid = False

        return valid

    def print_report(self):
        """Print validation report."""
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ Validation passed with no errors or warnings!")
        elif not self.errors:
            print(f"\n✅ Validation passed with {len(self.warnings)} warning(s)")
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} error(s) and {len(self.warnings)} warning(s)")


class ManifestGenerator:
    """Generate complete manifest.json."""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.discovery = SkillDiscovery(repo_root, verbose)
        self.validator = ManifestValidator(repo_root, verbose)

    def generate_manifest(self) -> Dict[str, Any]:
        """Generate complete manifest structure."""
        if self.verbose:
            print("Discovering skills...")

        skill_files = self.discovery.find_all_skills()

        if not skill_files:
            print("Error: No SKILL.md files found!", file=sys.stderr)
            sys.exit(1)

        # Extract metadata for all skills
        all_skills = []
        for i, skill_path in enumerate(skill_files, 1):
            if self.verbose:
                print(f"Processing {i}/{len(skill_files)}: {skill_path.relative_to(self.repo_root)}")

            skill_metadata = self.discovery.extract_skill_metadata(skill_path)
            all_skills.append(skill_metadata)

        # Organize skills by category and toolchain
        universal_skills = []
        toolchain_skills: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        example_skills = []

        for skill in all_skills:
            if skill['category'] == 'universal':
                universal_skills.append(skill)
            elif skill['category'] == 'toolchain':
                toolchain = skill['toolchain']
                if toolchain:
                    toolchain_skills[toolchain].append(skill)
            elif skill['category'] == 'example':
                example_skills.append(skill)

        # Calculate statistics
        toolchain_counts = {
            toolchain: len(skills)
            for toolchain, skills in toolchain_skills.items()
        }

        # Build manifest
        manifest = {
            'version': '1.0.0',
            'repository': 'https://github.com/bobmatnyc/claude-mpm-skills',
            'updated': datetime.now().strftime('%Y-%m-%d'),
            'description': 'Curated collection of Claude Code skills for intelligent project development',
            'skills': {
                'universal': sorted(universal_skills, key=lambda s: s['name']),
                'toolchains': {
                    toolchain: sorted(skills, key=lambda s: s['name'])
                    for toolchain, skills in sorted(toolchain_skills.items())
                }
            },
            'metadata': {
                'total_skills': len(all_skills),
                'categories': {
                    'universal': len(universal_skills),
                    'toolchains': sum(toolchain_counts.values()),
                    'examples': len(example_skills)
                },
                'toolchains': toolchain_counts,
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'schema_version': '2.0.0'
            },
            'provenance': {
                'source_repository': 'https://github.com/bobmatnyc/claude-mpm',
                'skills_repository': 'https://github.com/bobmatnyc/claude-mpm-skills',
                'author': 'Claude MPM Team',
                'license': 'MIT',
                'attribution_required': True
            }
        }

        # Add examples if present
        if example_skills:
            manifest['skills']['examples'] = sorted(example_skills, key=lambda s: s['name'])

        return manifest

    def print_summary(self, manifest: Dict[str, Any]):
        """Print generation summary."""
        print("\n" + "="*60)
        print("MANIFEST GENERATION SUMMARY")
        print("="*60)

        metadata = manifest['metadata']
        print(f"\nTotal Skills: {metadata['total_skills']}")
        print(f"  - Universal: {metadata['categories']['universal']}")
        print(f"  - Toolchains: {metadata['categories']['toolchains']}")
        if metadata['categories'].get('examples', 0) > 0:
            print(f"  - Examples: {metadata['categories']['examples']}")

        print("\nToolchain Breakdown:")
        for toolchain, count in sorted(metadata['toolchains'].items()):
            print(f"  - {toolchain}: {count}")

        print(f"\nGeneration Date: {metadata['last_updated']}")
        print(f"Schema Version: {metadata['schema_version']}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Generate correct manifest.json for all skills',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('manifest.json'),
        help='Output file path (default: manifest.json)'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate existing manifest.json instead of generating'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing file'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    if not (repo_root / 'universal').exists() or not (repo_root / 'toolchains').exists():
        print(f"Error: Not a valid repository root: {repo_root}", file=sys.stderr)
        sys.exit(1)

    generator = ManifestGenerator(repo_root, args.verbose)

    if args.validate:
        # Validate existing manifest
        manifest_path = repo_root / 'manifest.json'
        if not manifest_path.exists():
            print(f"Error: {manifest_path} does not exist", file=sys.stderr)
            sys.exit(1)

        print(f"Validating {manifest_path}...")
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

        valid = generator.validator.validate_manifest(manifest)
        generator.validator.print_report()

        sys.exit(0 if valid else 1)

    # Generate new manifest
    print("Generating manifest.json...")
    manifest = generator.generate_manifest()

    # Validate generated manifest
    print("\nValidating generated manifest...")
    valid = generator.validator.validate_manifest(manifest)
    generator.validator.print_report()

    if not valid:
        print("\n❌ Generated manifest has validation errors!", file=sys.stderr)
        sys.exit(1)

    # Print summary
    generator.print_summary(manifest)

    # Write or preview
    if args.dry_run:
        print("\n[DRY RUN] Would write to:", args.output)
        print("\nFirst 3 universal skills:")
        for skill in manifest['skills']['universal'][:3]:
            print(f"  - {skill['name']}: {skill['source_path']}")
    else:
        output_path = repo_root / args.output
        output_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8'
        )
        print(f"\n✅ Manifest written to: {output_path}")


if __name__ == '__main__':
    main()
