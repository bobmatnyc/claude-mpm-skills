#!/usr/bin/env python3
"""
Fix metadata issues in skills:
1. Update full_tokens with actual token counts
2. Add missing entry_point_tokens
3. Add missing toolchain field
4. Fix unrecognized categories (platform -> toolchain)
"""

import json
import re
import sys
from pathlib import Path

try:
    import tiktoken
    encoding = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(encoding.encode(text))
except ImportError:
    def count_tokens(text: str) -> int:
        return len(text) // 4

def extract_entry_point_tokens(skill_md_content: str) -> int:
    """Extract tokens from progressive_disclosure entry_point section."""
    # Find the progressive_disclosure section
    match = re.search(
        r'progressive_disclosure:\s*\n\s*entry_point:\s*\n(.*?)(?=\n\s*(?:references:|token_estimate:|---|\n\n[A-Z#]))',
        skill_md_content,
        re.DOTALL
    )
    if match:
        entry_point = match.group(1)
        return count_tokens(entry_point)

    # Fallback: use frontmatter only
    match = re.match(r'^---\s*\n(.*?)\n---', skill_md_content, re.DOTALL)
    if match:
        return count_tokens(match.group(1))

    return 85  # Default

def get_toolchain_from_path(skill_path: Path) -> tuple[str | None, bool]:
    """Extract toolchain from skill path.

    Returns:
        tuple: (toolchain_value, should_set_explicit_null)
        - For language toolchains: ("python", False)
        - For platforms/universal: (None, True) - explicitly set null
    """
    parts = str(skill_path).split('/')

    # universal/* skills - cross-language, set explicit null
    if 'universal' in parts:
        return (None, True)

    # toolchains/{toolchain}/...
    if 'toolchains' in parts:
        idx = parts.index('toolchains')
        if idx + 1 < len(parts):
            toolchain = parts[idx + 1]
            # Platforms are cross-language - set explicit null
            if toolchain == 'platforms':
                return (None, True)
            return (toolchain, False)

    return (None, False)

def fix_skill_metadata(skill_path: Path, dry_run: bool = False) -> list[str]:
    """Fix metadata issues for a single skill."""
    fixes = []

    metadata_path = skill_path / "metadata.json"
    skill_md_path = skill_path / "SKILL.md"

    if not metadata_path.exists():
        return fixes

    try:
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return [f"ERROR: Invalid JSON in {metadata_path}"]

    original = json.dumps(metadata, sort_keys=True)

    # Fix 1: Calculate actual full_tokens
    if skill_md_path.exists():
        skill_content = skill_md_path.read_text(encoding='utf-8')
        actual_tokens = count_tokens(skill_content)

        # Add reference files
        references_dir = skill_path / "references"
        if references_dir.exists():
            for ref in references_dir.glob("*.md"):
                actual_tokens += count_tokens(ref.read_text(encoding='utf-8'))

        # Update if different by more than 10%
        declared = metadata.get('full_tokens', 0)
        if declared == 0 or abs(declared - actual_tokens) > declared * 0.1:
            metadata['full_tokens'] = actual_tokens
            fixes.append(f"full_tokens: {declared} -> {actual_tokens}")

    # Fix 2: Add entry_point_tokens if missing
    if 'entry_point_tokens' not in metadata and skill_md_path.exists():
        skill_content = skill_md_path.read_text(encoding='utf-8')
        entry_tokens = extract_entry_point_tokens(skill_content)
        metadata['entry_point_tokens'] = entry_tokens
        fixes.append(f"entry_point_tokens: added ({entry_tokens})")

    # Fix 3: Add toolchain if missing
    if 'toolchain' not in metadata:
        toolchain, explicit_null = get_toolchain_from_path(skill_path)
        if toolchain:
            metadata['toolchain'] = toolchain
            fixes.append(f"toolchain: added ({toolchain})")
        elif explicit_null:
            metadata['toolchain'] = None
            fixes.append("toolchain: set to null (cross-language skill)")

    # Fix 4: Fix unrecognized categories
    if metadata.get('category') == 'platform':
        metadata['category'] = 'toolchain'
        fixes.append("category: platform -> toolchain")

    # Write if changed
    if fixes and not dry_run:
        # Reorder keys for consistency
        ordered_keys = ['name', 'version', 'category', 'toolchain', 'framework',
                       'tags', 'entry_point_tokens', 'full_tokens', 'related_skills',
                       'author', 'license']

        ordered_metadata = {}
        for key in ordered_keys:
            if key in metadata:
                ordered_metadata[key] = metadata[key]

        # Add remaining keys
        for key, value in metadata.items():
            if key not in ordered_metadata:
                ordered_metadata[key] = value

        metadata_path.write_text(
            json.dumps(ordered_metadata, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8'
        )

    return fixes


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Find all skills
    skills = []
    for search_dir in ['toolchains', 'universal', 'examples']:
        base = repo_root / search_dir
        if base.exists():
            for skill_md in base.rglob("SKILL.md"):
                skills.append(skill_md.parent)

    skills = sorted(set(skills))

    print(f"{'[DRY RUN] ' if dry_run else ''}Fixing metadata for {len(skills)} skills...\n")

    total_fixes = 0
    skills_fixed = 0

    for skill_path in skills:
        relative = skill_path.relative_to(repo_root)
        fixes = fix_skill_metadata(skill_path, dry_run)

        if fixes:
            skills_fixed += 1
            total_fixes += len(fixes)
            print(f"📦 {relative}")
            for fix in fixes:
                print(f"   ✓ {fix}")
        elif verbose:
            print(f"📦 {relative} - OK")

    print(f"\n{'='*50}")
    print(f"Summary: {skills_fixed} skills fixed, {total_fixes} total fixes")

    if dry_run:
        print("\n[DRY RUN] No files were modified. Run without --dry-run to apply fixes.")


if __name__ == '__main__':
    main()
