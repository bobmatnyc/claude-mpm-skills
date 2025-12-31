#!/usr/bin/env python3
"""
Add missing progressive_disclosure sections to SKILL.md files.

Generates minimal progressive_disclosure based on existing frontmatter:
- summary: from description
- when_to_use: from name/description
- quick_start: generic steps
"""

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


def parse_frontmatter(content: str) -> tuple[dict, str, str]:
    """Parse YAML frontmatter from SKILL.md content.

    Returns:
        tuple: (frontmatter_dict, frontmatter_raw, body)
    """
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, '', content

    frontmatter_raw = match.group(1)
    body = content[match.end():]

    # Simple YAML parsing for key fields
    frontmatter = {}

    # Extract name
    name_match = re.search(r'^name:\s*["\']?([^"\'\n]+)["\']?\s*$', frontmatter_raw, re.MULTILINE)
    if name_match:
        frontmatter['name'] = name_match.group(1).strip()

    # Extract description (may be multi-line or quoted)
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', frontmatter_raw, re.MULTILINE)
    if desc_match:
        frontmatter['description'] = desc_match.group(1).strip().strip('"\'')

    # Extract when_to_use if present
    when_match = re.search(r'^when_to_use:\s*["\']?(.+?)["\']?\s*$', frontmatter_raw, re.MULTILINE)
    if when_match:
        frontmatter['when_to_use'] = when_match.group(1).strip().strip('"\'')

    # Check if progressive_disclosure already exists
    if 'progressive_disclosure:' in frontmatter_raw:
        frontmatter['has_progressive_disclosure'] = True

    return frontmatter, frontmatter_raw, body


def generate_progressive_disclosure(frontmatter: dict, skill_path: Path) -> str:
    """Generate progressive_disclosure section based on frontmatter."""
    name = frontmatter.get('name', skill_path.name)
    description = frontmatter.get('description', f'{name} skill')
    when_to_use = frontmatter.get('when_to_use', '')

    # Clean up description for summary
    summary = description
    if len(summary) > 200:
        summary = summary[:197] + '...'

    # Generate when_to_use if not present
    if not when_to_use:
        # Try to infer from name/description
        name_lower = name.lower()
        if 'test' in name_lower:
            when_to_use = f"When writing tests, implementing {name}, or ensuring code quality."
        elif 'debug' in name_lower:
            when_to_use = f"When debugging issues, tracing errors, or investigating problems."
        elif 'api' in name_lower:
            when_to_use = f"When designing, implementing, or documenting APIs."
        elif 'git' in name_lower or 'pr' in name_lower:
            when_to_use = f"When working with version control, branches, or pull requests."
        elif 'data' in name_lower or 'database' in name_lower:
            when_to_use = f"When working with data, databases, or data transformations."
        elif 'auth' in name_lower:
            when_to_use = f"When implementing authentication, authorization, or security."
        else:
            when_to_use = f"When working with {name} or related functionality."

    # Generate quick_start steps
    quick_start = "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."

    # Check for references directory
    references_dir = skill_path / "references"
    references = []
    if references_dir.exists():
        for ref in sorted(references_dir.glob("*.md")):
            references.append(ref.name)

    # Build the progressive_disclosure YAML
    pd_lines = [
        "progressive_disclosure:",
        "  entry_point:",
        f'    summary: "{summary}"',
        f'    when_to_use: "{when_to_use}"',
        f'    quick_start: "{quick_start}"',
    ]

    if references:
        pd_lines.append("  references:")
        for ref in references[:5]:  # Limit to 5 references
            pd_lines.append(f"    - {ref}")

    return '\n'.join(pd_lines)


def fix_skill_progressive_disclosure(skill_path: Path, dry_run: bool = False) -> list[str]:
    """Add progressive_disclosure to SKILL.md if missing."""
    fixes = []
    skill_md_path = skill_path / "SKILL.md"

    if not skill_md_path.exists():
        return fixes

    content = skill_md_path.read_text(encoding='utf-8')
    frontmatter, frontmatter_raw, body = parse_frontmatter(content)

    # Skip if already has progressive_disclosure
    if frontmatter.get('has_progressive_disclosure'):
        return fixes

    # Check if frontmatter exists
    if not frontmatter_raw:
        return [f"WARNING: No frontmatter found in {skill_md_path}"]

    # Generate progressive_disclosure
    pd_section = generate_progressive_disclosure(frontmatter, skill_path)

    # Insert progressive_disclosure before the closing ---
    # Find a good insertion point (after tags, before ---)
    lines = frontmatter_raw.split('\n')

    # Find insertion point - after the last top-level field
    insert_idx = len(lines)
    for i, line in enumerate(lines):
        # Skip if line is part of a list or nested
        if line.startswith('  ') or line.startswith('-'):
            continue
        if ':' in line and not line.strip().startswith('#'):
            insert_idx = i + 1
            # If this field has list values, skip them
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('  ') or lines[j].startswith('-'):
                    insert_idx = j + 1
                else:
                    break

    # Insert progressive_disclosure
    new_frontmatter_lines = lines[:insert_idx] + [pd_section] + lines[insert_idx:]
    new_frontmatter = '\n'.join(new_frontmatter_lines)

    # Rebuild content
    new_content = f"---\n{new_frontmatter}\n---\n{body}"

    if not dry_run:
        skill_md_path.write_text(new_content, encoding='utf-8')

    fixes.append("progressive_disclosure: added")
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

    print(f"{'[DRY RUN] ' if dry_run else ''}Fixing progressive_disclosure for {len(skills)} skills...\n")

    total_fixes = 0
    skills_fixed = 0

    for skill_path in skills:
        relative = skill_path.relative_to(repo_root)
        fixes = fix_skill_progressive_disclosure(skill_path, dry_run)

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
