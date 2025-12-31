#!/usr/bin/env python3
"""
Initialize a new skill with proper directory structure and templates.

This script creates a new skill following the claude-mpm-skills conventions:
1. Creates directory structure: {category}/{toolchain}/{subcategory}/{framework}/
2. Generates SKILL.md with proper frontmatter and progressive_disclosure
3. Generates metadata.json with proper structure
4. Validates the skill name and path

Usage:
    # Interactive mode
    python scripts/init_skill.py

    # With arguments
    python scripts/init_skill.py --category toolchains --toolchain python --framework fastapi
    python scripts/init_skill.py --category universal --subcategory testing --name tdd-patterns

    # Quick mode with full path
    python scripts/init_skill.py --path toolchains/python/frameworks/fastapi

Examples:
    # Create a new framework skill
    python scripts/init_skill.py --category toolchains --toolchain python --subcategory frameworks --framework django

    # Create a universal skill
    python scripts/init_skill.py --category universal --subcategory debugging --name systematic-debugging

    # Create with description
    python scripts/init_skill.py --path toolchains/rust/testing/integration --description "Rust integration testing patterns"
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


# Template for SKILL.md
SKILL_MD_TEMPLATE = """---
name: {name}
description: "{description}"
---

# {title}

---
progressive_disclosure:
  entry_point:
    summary: "{summary}"
    when_to_use:
      - "{use_case_1}"
      - "{use_case_2}"
      - "{use_case_3}"
    quick_start:
      - "{quick_start_1}"
      - "{quick_start_2}"
      - "{quick_start_3}"
  token_estimate:
    entry: 75-100
    full: 3000-5000
---

## Overview

{overview_placeholder}

## Core Concepts

### Concept 1

[Describe the first core concept]

### Concept 2

[Describe the second core concept]

## Implementation Patterns

### Pattern 1: Basic Usage

```{code_lang}
# Example code here
```

### Pattern 2: Advanced Usage

```{code_lang}
# Advanced example code here
```

## Best Practices

1. **Practice 1**: [Description]
2. **Practice 2**: [Description]
3. **Practice 3**: [Description]

## Anti-Patterns

- **Anti-pattern 1**: [What to avoid and why]
- **Anti-pattern 2**: [What to avoid and why]

## Decision Trees

### When to Use This Skill

```
Is your use case X?
├── Yes → Use Pattern A
└── No
    ├── Is it Y? → Use Pattern B
    └── Otherwise → Consider Alternative Z
```

## Examples

### Example 1: [Title]

```{code_lang}
# Complete working example
```

### Example 2: [Title]

```{code_lang}
# Another complete example
```

## Troubleshooting

### Common Issue 1

**Problem**: [Description]
**Solution**: [How to fix]

### Common Issue 2

**Problem**: [Description]
**Solution**: [How to fix]

## Resources

- [Official Documentation](https://example.com)
- [Tutorial](https://example.com/tutorial)
- [Best Practices Guide](https://example.com/best-practices)

## Related Skills

- **related-skill-1**: [Brief description of relationship]
- **related-skill-2**: [Brief description of relationship]
"""


def get_code_language(toolchain: str) -> str:
    """Map toolchain to code language for syntax highlighting."""
    language_map = {
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "rust": "rust",
        "golang": "go",
        "go": "go",
        "java": "java",
        "ruby": "ruby",
        "php": "php",
        "elixir": "elixir",
        "swift": "swift",
        "kotlin": "kotlin",
        "csharp": "csharp",
        "cpp": "cpp",
        "c": "c",
    }
    return language_map.get(toolchain.lower(), "text")


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text


def title_case(text: str) -> str:
    """Convert slug or text to title case."""
    return " ".join(
        word.capitalize() for word in text.replace("-", " ").replace("_", " ").split()
    )


def create_metadata_json(
    name: str,
    category: str,
    toolchain: Optional[str],
    framework: Optional[str],
    tags: list[str],
    author: str = "Claude MPM",
) -> dict:
    """Create metadata.json content."""
    metadata = {
        "name": name,
        "version": "1.0.0",
        "category": category,
        "toolchain": toolchain,
        "framework": framework,
        "tags": tags,
        "entry_point_tokens": 85,
        "full_tokens": 4000,
        "related_skills": [],
        "author": author,
        "license": "MIT",
    }

    # Remove None values
    return {k: v for k, v in metadata.items() if v is not None}


def create_skill_md(
    name: str,
    title: str,
    description: str,
    toolchain: Optional[str] = None,
    framework: Optional[str] = None,
) -> str:
    """Create SKILL.md content from template."""
    code_lang = get_code_language(toolchain) if toolchain else "text"

    # Generate placeholder content
    summary = description if description else f"{title} patterns and best practices"
    use_case_1 = f"When working with {framework or toolchain or 'this technology'}"
    use_case_2 = "When implementing common patterns"
    use_case_3 = "When troubleshooting issues"

    quick_start_1 = "Step 1: [Installation or setup]"
    quick_start_2 = "Step 2: [Basic configuration]"
    quick_start_3 = "Step 3: [First implementation]"

    overview = f"[Provide an overview of {title}. Explain what it is, why it's useful, and key concepts.]"

    return SKILL_MD_TEMPLATE.format(
        name=name,
        description=description or f"{title} skill",
        title=title,
        summary=summary,
        use_case_1=use_case_1,
        use_case_2=use_case_2,
        use_case_3=use_case_3,
        quick_start_1=quick_start_1,
        quick_start_2=quick_start_2,
        quick_start_3=quick_start_3,
        overview_placeholder=overview,
        code_lang=code_lang,
    )


def parse_path(path: str) -> dict:
    """Parse a skill path into components."""
    parts = path.strip("/").split("/")

    result = {
        "category": None,
        "toolchain": None,
        "subcategory": None,
        "framework": None,
        "name": None,
    }

    if not parts:
        return result

    # First part is category (toolchains, universal, examples)
    result["category"] = parts[0]

    if result["category"] == "toolchains" and len(parts) > 1:
        result["toolchain"] = parts[1]
        if len(parts) > 2:
            result["subcategory"] = parts[2]
        if len(parts) > 3:
            result["framework"] = parts[3]
            result["name"] = parts[3]
    elif result["category"] == "universal" and len(parts) > 1:
        result["subcategory"] = parts[1]
        if len(parts) > 2:
            result["name"] = parts[2]
    elif result["category"] == "examples" and len(parts) > 1:
        result["name"] = parts[1]

    return result


def build_skill_path(
    category: str,
    toolchain: Optional[str] = None,
    subcategory: Optional[str] = None,
    framework: Optional[str] = None,
    name: Optional[str] = None,
) -> Path:
    """Build the skill directory path from components."""
    parts = [category]

    if category == "toolchains":
        if toolchain:
            parts.append(toolchain)
        if subcategory:
            parts.append(subcategory)
        if framework:
            parts.append(framework)
    elif category == "universal":
        if subcategory:
            parts.append(subcategory)
        if name:
            parts.append(name)
    elif category == "examples":
        if name:
            parts.append(name)

    return Path("/".join(parts))


def interactive_mode(repo_root: Path) -> dict:
    """Run interactive mode to gather skill parameters."""
    print("\n🔧 Claude MPM Skill Initializer\n")
    print("This wizard will help you create a new skill.\n")

    # Category
    print("Categories:")
    print("  1. toolchains - Language/framework specific skills")
    print("  2. universal  - Cross-language patterns and practices")
    print("  3. examples   - Example skills for reference")
    category_choice = input("\nSelect category [1/2/3] (default: 1): ").strip() or "1"
    category_map = {"1": "toolchains", "2": "universal", "3": "examples"}
    category = category_map.get(category_choice, "toolchains")

    toolchain = None
    subcategory = None
    framework = None
    name = None

    if category == "toolchains":
        # Toolchain
        print(
            "\nCommon toolchains: python, javascript, typescript, rust, golang, java, php, ruby, elixir"
        )
        toolchain = input("Enter toolchain: ").strip().lower()

        # Subcategory
        print(
            "\nCommon subcategories: frameworks, testing, tooling, data, async, validation, state, api, build"
        )
        subcategory = input("Enter subcategory: ").strip().lower()

        # Framework/name
        framework = input("Enter framework/skill name: ").strip().lower()
        framework = slugify(framework)
        name = framework

    elif category == "universal":
        # Subcategory
        print(
            "\nCommon subcategories: testing, debugging, architecture, collaboration, infrastructure, main"
        )
        subcategory = input("Enter subcategory: ").strip().lower()

        # Name
        name = input("Enter skill name: ").strip().lower()
        name = slugify(name)

    elif category == "examples":
        name = input("Enter example name: ").strip().lower()
        name = slugify(name)

    # Description
    print("\n")
    description = input("Enter skill description (one line): ").strip()

    # Tags
    tags_input = input("Enter tags (comma-separated): ").strip()
    tags = [t.strip().lower() for t in tags_input.split(",") if t.strip()]

    return {
        "category": category,
        "toolchain": toolchain,
        "subcategory": subcategory,
        "framework": framework,
        "name": name or framework,
        "description": description,
        "tags": tags,
    }


def create_skill(
    repo_root: Path,
    category: str,
    toolchain: Optional[str] = None,
    subcategory: Optional[str] = None,
    framework: Optional[str] = None,
    name: Optional[str] = None,
    description: str = "",
    tags: Optional[list[str]] = None,
    force: bool = False,
    dry_run: bool = False,
) -> bool:
    """Create a new skill with all required files."""

    # Determine skill name
    skill_name = name or framework
    if not skill_name:
        print("Error: Skill name is required", file=sys.stderr)
        return False

    # Build path
    skill_path = build_skill_path(category, toolchain, subcategory, framework, name)
    full_path = repo_root / skill_path

    # Check if already exists
    if full_path.exists() and not force:
        print(f"Error: Skill already exists at {skill_path}", file=sys.stderr)
        print("Use --force to overwrite", file=sys.stderr)
        return False

    # Generate title
    title = title_case(skill_name)
    if framework and toolchain:
        title = f"{title_case(framework)} ({title_case(toolchain)})"

    # Generate tags if not provided
    if not tags:
        tags = []
        if toolchain:
            tags.append(toolchain)
        if framework:
            tags.append(framework)
        if subcategory:
            tags.append(subcategory)

    # Create content
    skill_md_content = create_skill_md(
        name=skill_name,
        title=title,
        description=description,
        toolchain=toolchain,
        framework=framework,
    )

    metadata_content = create_metadata_json(
        name=skill_name,
        category="toolchain" if category == "toolchains" else category,
        toolchain=toolchain,
        framework=framework,
        tags=tags,
    )

    if dry_run:
        print(f"\n[DRY RUN] Would create skill at: {skill_path}")
        print("\nDirectory structure:")
        print(f"  {skill_path}/")
        print(f"    SKILL.md ({len(skill_md_content)} chars)")
        print("    metadata.json")
        print("\nmetadata.json content:")
        print(json.dumps(metadata_content, indent=2))
        return True

    # Create directory
    full_path.mkdir(parents=True, exist_ok=True)

    # Write SKILL.md
    skill_md_path = full_path / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding="utf-8")

    # Write metadata.json
    metadata_path = full_path / "metadata.json"
    metadata_path.write_text(
        json.dumps(metadata_content, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("\n✅ Skill created successfully!")
    print(f"\n📁 Location: {skill_path}/")
    print("   - SKILL.md")
    print("   - metadata.json")
    print("\n📝 Next steps:")
    print(f"   1. Edit {skill_path}/SKILL.md with actual content")
    print("   2. Update metadata.json with accurate token counts")
    print("   3. Add related_skills references")
    print("   4. Run: python scripts/generate_manifest.py --validate")
    print("   5. Deploy: ./scripts/flatten_skills.sh")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new skill with proper structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--path",
        "-p",
        type=str,
        help="Full skill path (e.g., toolchains/python/frameworks/django)",
    )

    parser.add_argument(
        "--category",
        "-c",
        choices=["toolchains", "universal", "examples"],
        help="Skill category",
    )

    parser.add_argument(
        "--toolchain", "-t", type=str, help="Toolchain (e.g., python, javascript, rust)"
    )

    parser.add_argument(
        "--subcategory",
        "-s",
        type=str,
        help="Subcategory (e.g., frameworks, testing, tooling)",
    )

    parser.add_argument("--framework", "-f", type=str, help="Framework or skill name")

    parser.add_argument(
        "--name", "-n", type=str, help="Skill name (for universal/examples)"
    )

    parser.add_argument(
        "--description", "-d", type=str, default="", help="Skill description"
    )

    parser.add_argument("--tags", type=str, help="Comma-separated tags")

    parser.add_argument("--force", action="store_true", help="Overwrite existing skill")

    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without creating files"
    )

    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )

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

    # Determine mode
    if args.interactive or (not args.path and not args.category):
        # Interactive mode
        params = interactive_mode(repo_root)
        success = create_skill(
            repo_root=repo_root,
            category=params["category"],
            toolchain=params["toolchain"],
            subcategory=params["subcategory"],
            framework=params["framework"],
            name=params["name"],
            description=params["description"],
            tags=params["tags"],
            force=args.force,
            dry_run=args.dry_run,
        )
    elif args.path:
        # Path mode
        parsed = parse_path(args.path)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        success = create_skill(
            repo_root=repo_root,
            category=parsed["category"] or "toolchains",
            toolchain=parsed["toolchain"],
            subcategory=parsed["subcategory"],
            framework=parsed["framework"],
            name=parsed["name"] or args.name,
            description=args.description,
            tags=tags,
            force=args.force,
            dry_run=args.dry_run,
        )
    else:
        # Argument mode
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        success = create_skill(
            repo_root=repo_root,
            category=args.category,
            toolchain=args.toolchain,
            subcategory=args.subcategory,
            framework=args.framework,
            name=args.name,
            description=args.description,
            tags=tags,
            force=args.force,
            dry_run=args.dry_run,
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
