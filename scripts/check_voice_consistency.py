#!/usr/bin/env python3
"""
Voice Consistency Checker for Claude Code Skills

Checks skills for second-person voice violations ("you should", "you must", "you can")
per BUILD_INSTRUCTIONS.md requirement to use imperative voice throughout.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Patterns that indicate second-person voice (violations)
SECOND_PERSON_PATTERNS = [
    r'\byou\s+should\b',
    r'\byou\s+must\b',
    r'\byou\s+can\b',
    r'\byou\s+need\s+to\b',
    r'\byou\s+have\s+to\b',
    r'\byou\s+want\s+to\b',
    r'\byou\'ll\s+need\b',
    r'\byou\'ll\s+want\b',
    r'\byour\s+\w+\s+should\b',
    r'\byour\s+\w+\s+must\b',
]

# Exceptions where second-person is acceptable
EXCEPTION_PATTERNS = [
    r'^\s*[>#-]\s+',  # Inside code comments or markdown quotes
    r'```[\s\S]*?```',  # Inside code blocks
    r'`[^`]+`',  # Inline code
]

def is_exception(line: str, context_lines: List[str], line_idx: int) -> bool:
    """Check if line is within an exception context (code block, comment)."""
    # Check if we're inside a code block
    code_block_count = 0
    for i in range(line_idx):
        if '```' in context_lines[i]:
            code_block_count += 1
    if code_block_count % 2 == 1:  # Odd number means we're inside a code block
        return True
    
    # Check inline exceptions
    for pattern in EXCEPTION_PATTERNS:
        if re.search(pattern, line):
            return True
    
    return False

def check_file(file_path: Path) -> List[Dict]:
    """Check a single file for voice violations."""
    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for idx, line in enumerate(lines):
            if is_exception(line, lines, idx):
                continue
            
            line_lower = line.lower()
            for pattern in SECOND_PERSON_PATTERNS:
                matches = list(re.finditer(pattern, line_lower, re.IGNORECASE))
                for match in matches:
                    violations.append({
                        'file': str(file_path),
                        'line_num': idx + 1,
                        'line': line.strip(),
                        'violation': match.group(0),
                        'pattern': pattern
                    })
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return violations

def suggest_fix(violation: str, line: str) -> str:
    """Suggest an imperative voice alternative."""
    fixes = {
        r'you should': 'Use / Apply / Implement',
        r'you must': 'Must / Always / Required:',
        r'you can': 'To accomplish X, [verb]',
        r'you need to': '[Verb directly]',
        r'you have to': 'Required: / Must',
        r'you want to': 'To accomplish X, [verb]',
        r"you'll need": 'Required: / Need:',
        r"you'll want": 'To accomplish X, [verb]',
    }
    
    for pattern, fix in fixes.items():
        if re.search(pattern, violation.lower()):
            return fix
    
    return '[Rewrite in imperative voice]'

def main():
    """Run voice consistency check on all skills."""
    if len(sys.argv) > 1:
        skills_dir = Path(sys.argv[1])
    else:
        skills_dir = Path(__file__).parent.parent
    
    # Find all SKILL.md files
    skill_files = []
    for pattern in ['universal/**/SKILL.md', 'toolchains/**/SKILL.md', 'examples/**/SKILL.md']:
        skill_files.extend(skills_dir.glob(pattern))
    
    print(f"Checking {len(skill_files)} skills for voice violations...\n")
    
    all_violations = []
    files_with_violations = []
    
    for skill_file in sorted(skill_files):
        violations = check_file(skill_file)
        if violations:
            all_violations.extend(violations)
            files_with_violations.append((skill_file, violations))
    
    # Report results
    if not all_violations:
        print("✅ No voice violations found! All skills use imperative voice correctly.")
        return 0
    
    print(f"❌ Found {len(all_violations)} voice violations in {len(files_with_violations)} files\n")
    print("=" * 80)
    
    # Group by file
    for skill_file, violations in files_with_violations:
        rel_path = skill_file.relative_to(skills_dir)
        print(f"\n📄 {rel_path} ({len(violations)} violations)")
        print("-" * 80)
        
        for v in violations[:10]:  # Show first 10 per file
            print(f"  Line {v['line_num']}: {v['line']}")
            print(f"  Violation: \"{v['violation']}\"")
            print(f"  Suggestion: {suggest_fix(v['violation'], v['line'])}")
            print()
        
        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more violations")
            print()
    
    # Summary by violation type
    print("\n" + "=" * 80)
    print("SUMMARY BY VIOLATION TYPE")
    print("=" * 80)
    
    violation_counts = {}
    for v in all_violations:
        key = v['violation'].lower()
        violation_counts[key] = violation_counts.get(key, 0) + 1
    
    for violation, count in sorted(violation_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {count:3d}x: \"{violation}\"")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(all_violations)} violations in {len(files_with_violations)} files")
    print("=" * 80)
    
    return 1 if all_violations else 0

if __name__ == '__main__':
    sys.exit(main())
