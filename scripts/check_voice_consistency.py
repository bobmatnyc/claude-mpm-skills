#!/usr/bin/env python3
"""
Voice Consistency and Example Format Checker for Claude Code Skills

Comprehensive automated checker for:
1. Voice Consistency: Second-person detection, passive voice, imperative mood
2. Example Format: ✅/❌ pattern validation, code block formatting
3. Anti-Pattern Documentation: Ensuring best practices are documented

Designed for CI/CD integration with detailed reporting and auto-fix capabilities.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json


class Severity(Enum):
    """Violation severity levels."""
    ERROR = "error"      # Critical violations, block CI
    WARNING = "warning"  # Should be fixed, but not blocking
    INFO = "info"        # Suggestions for improvement


@dataclass
class Violation:
    """Represents a single quality violation."""
    file_path: str
    line_num: int
    line_content: str
    violation_type: str
    severity: Severity
    message: str
    suggestion: Optional[str] = None
    matched_text: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export."""
        return {
            "file": self.file_path,
            "line": self.line_num,
            "content": self.line_content.strip(),
            "type": self.violation_type,
            "severity": self.severity.value,
            "message": self.message,
            "suggestion": self.suggestion,
            "matched_text": self.matched_text
        }


@dataclass
class FileReport:
    """Quality report for a single file."""
    file_path: Path
    violations: List[Violation] = field(default_factory=list)
    has_examples: bool = False
    has_anti_patterns: bool = False
    line_count: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.INFO)


# ============================================================================
# PATTERN DEFINITIONS
# ============================================================================

# Second-person voice patterns (violations of imperative voice)
SECOND_PERSON_PATTERNS = {
    r'\byou\s+should\b': "Replace with imperative: 'Use X' or 'Apply Y'",
    r'\byou\s+must\b': "Replace with imperative: 'Must X' or 'Always Y'",
    r'\byou\s+can\b': "Replace with capability statement: 'To X, do Y' or 'X enables Y'",
    r'\byou\s+need\s+to\b': "Replace with imperative: '[Verb] directly'",
    r'\byou\s+have\s+to\b': "Replace with imperative: 'Required: X' or 'Must Y'",
    r'\byou\s+want\s+to\b': "Replace with purpose: 'To accomplish X, do Y'",
    r'\byou\'ll\s+need\b': "Replace with requirement: 'Required: X' or 'Need: Y'",
    r'\byou\'ll\s+want\b': "Replace with purpose: 'To accomplish X, do Y'",
    r'\byou\'re\b': "Rewrite in imperative voice",
    r'\byourself\b': "Rewrite in imperative voice",
    r'\byour\s+\w+\s+should\b': "Replace with imperative statement",
    r'\byour\s+\w+\s+must\b': "Replace with imperative requirement",
    r'\byour\s+\w+\s+can\b': "Replace with capability description",
    r'\bif\s+you\b': "Replace with conditional: 'When X occurs, do Y'",
    r'\bwhen\s+you\b': "Replace with temporal: 'When X occurs' or 'During Y'",
}

# Passive voice patterns
PASSIVE_VOICE_PATTERNS = {
    r'\bis\s+\w+ed\b': "Consider active voice: 'X does Y' instead of 'Y is done by X'",
    r'\bare\s+\w+ed\b': "Consider active voice",
    r'\bwas\s+\w+ed\b': "Consider active voice",
    r'\bwere\s+\w+ed\b': "Consider active voice",
    r'\bbeen\s+\w+ed\b': "Consider active voice",
    r'\bbeing\s+\w+ed\b': "Consider active voice",
}

# Non-imperative mood patterns
NON_IMPERATIVE_PATTERNS = {
    r'\bshould\s+\w+\b': "Use imperative: '[Verb] X' instead of 'should [verb]'",
    r'\bwould\s+\w+\b': "Use imperative or conditional",
    r'\bcould\s+\w+\b': "Use imperative or possibility statement",
    r'\bmight\s+\w+\b': "Use imperative or conditional",
    r'\bmay\s+\w+\b': "Use imperative or permission statement",
    r'\bconsider\s+\w+ing\b': "Use imperative: '[Verb] X' instead of 'consider [verb]ing'",
}

# Conversational tone patterns
CONVERSATIONAL_PATTERNS = {
    r'\blet\'s\b': "Use imperative: 'Create X' instead of 'Let's create X'",
    r'\bwe\s+can\b': "Rewrite with focus on action, not actor",
    r'\bwe\s+should\b': "Use imperative directive",
    r'\bwe\s+need\s+to\b': "Use imperative requirement",
    r'\bI\s+recommend\b': "State recommendation directly: 'Use X for Y'",
    r'\bI\s+suggest\b': "State suggestion directly",
    r'\bIn\s+my\s+experience\b': "State fact directly or remove",
}

# Example format patterns
EXAMPLE_CHECKMARK_PATTERN = r'^\s*✅\s+'
EXAMPLE_CROSSMARK_PATTERN = r'^\s*❌\s+'
CODE_BLOCK_START = r'^```(\w+)?'
CODE_BLOCK_END = r'^```\s*$'

# Allowed exceptions (context where second-person is acceptable)
EXCEPTION_CONTEXTS = [
    r'^\s*[>#]\s+',           # Inside markdown quotes or comments
    r'^\s*-\s+\*\*.*\*\*:',   # Inside definition lists
    r'^\s*\|\s*.*\s*\|',      # Inside tables
    r'`[^`]+`',               # Inline code
]


# ============================================================================
# CONTEXT DETECTION
# ============================================================================

class ContextDetector:
    """Detects various contexts in markdown files."""

    def __init__(self, lines: List[str]):
        self.lines = lines
        self._build_context_map()

    def _build_context_map(self):
        """Build map of line contexts for fast lookup."""
        self.in_code_block = [False] * len(self.lines)
        self.in_frontmatter = [False] * len(self.lines)
        self.in_quote = [False] * len(self.lines)
        self.in_table = [False] * len(self.lines)

        code_block_active = False
        frontmatter_active = False

        for i, line in enumerate(self.lines):
            # Track code blocks
            if re.match(CODE_BLOCK_START, line):
                code_block_active = not code_block_active
            self.in_code_block[i] = code_block_active

            # Track frontmatter (YAML between --- markers)
            if line.strip() == '---':
                if i == 0:
                    frontmatter_active = True
                elif frontmatter_active:
                    frontmatter_active = False
            self.in_frontmatter[i] = frontmatter_active

            # Track quotes
            self.in_quote[i] = bool(re.match(r'^\s*>', line))

            # Track tables
            self.in_table[i] = bool(re.match(r'^\s*\|', line))

    def is_exception_context(self, line_idx: int, line: str) -> bool:
        """Check if line is in an exception context."""
        # Check precomputed contexts
        if (self.in_code_block[line_idx] or
            self.in_frontmatter[line_idx] or
            self.in_quote[line_idx] or
            self.in_table[line_idx]):
            return True

        # Check inline exceptions
        for pattern in EXCEPTION_CONTEXTS:
            if re.search(pattern, line):
                return True

        return False


# ============================================================================
# CHECKERS
# ============================================================================

class VoiceConsistencyChecker:
    """Checks for voice consistency violations."""

    def __init__(self, context: ContextDetector):
        self.context = context

    def check_file(self, file_path: Path, lines: List[str]) -> List[Violation]:
        """Check file for voice consistency violations."""
        violations = []

        for idx, line in enumerate(lines):
            if self.context.is_exception_context(idx, line):
                continue

            line_lower = line.lower()

            # Check second-person patterns
            for pattern, suggestion in SECOND_PERSON_PATTERNS.items():
                matches = list(re.finditer(pattern, line_lower, re.IGNORECASE))
                for match in matches:
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_num=idx + 1,
                        line_content=line,
                        violation_type="second_person_voice",
                        severity=Severity.ERROR,
                        message="Second-person voice detected (use imperative)",
                        suggestion=suggestion,
                        matched_text=match.group(0)
                    ))

            # Check passive voice patterns
            for pattern, suggestion in PASSIVE_VOICE_PATTERNS.items():
                matches = list(re.finditer(pattern, line_lower, re.IGNORECASE))
                for match in matches:
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_num=idx + 1,
                        line_content=line,
                        violation_type="passive_voice",
                        severity=Severity.WARNING,
                        message="Passive voice detected",
                        suggestion=suggestion,
                        matched_text=match.group(0)
                    ))

            # Check non-imperative mood
            for pattern, suggestion in NON_IMPERATIVE_PATTERNS.items():
                matches = list(re.finditer(pattern, line_lower, re.IGNORECASE))
                for match in matches:
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_num=idx + 1,
                        line_content=line,
                        violation_type="non_imperative_mood",
                        severity=Severity.WARNING,
                        message="Non-imperative mood detected",
                        suggestion=suggestion,
                        matched_text=match.group(0)
                    ))

            # Check conversational tone
            for pattern, suggestion in CONVERSATIONAL_PATTERNS.items():
                matches = list(re.finditer(pattern, line_lower, re.IGNORECASE))
                for match in matches:
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_num=idx + 1,
                        line_content=line,
                        violation_type="conversational_tone",
                        severity=Severity.INFO,
                        message="Conversational tone detected",
                        suggestion=suggestion,
                        matched_text=match.group(0)
                    ))

        return violations


class ExampleFormatChecker:
    """Checks for ✅/❌ example format consistency."""

    def __init__(self, context: ContextDetector):
        self.context = context

    def check_file(self, file_path: Path, lines: List[str]) -> Tuple[List[Violation], bool]:
        """Check file for example format violations. Returns (violations, has_examples)."""
        violations = []
        has_examples = False

        # Track example pairs
        good_examples = []
        bad_examples = []
        orphaned_code_blocks = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # Detect ✅ example
            if re.match(EXAMPLE_CHECKMARK_PATTERN, line):
                has_examples = True
                good_examples.append(i + 1)

                # Check if followed by code block
                if i + 1 < len(lines) and not re.match(CODE_BLOCK_START, lines[i + 1]):
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_num=i + 1,
                        line_content=line,
                        violation_type="missing_code_block",
                        severity=Severity.WARNING,
                        message="✅ example not followed by code block",
                        suggestion="Add code block after ✅ example"
                    ))

            # Detect ❌ example
            if re.match(EXAMPLE_CROSSMARK_PATTERN, line):
                has_examples = True
                bad_examples.append(i + 1)

                # Check if followed by code block
                if i + 1 < len(lines) and not re.match(CODE_BLOCK_START, lines[i + 1]):
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_num=i + 1,
                        line_content=line,
                        violation_type="missing_code_block",
                        severity=Severity.WARNING,
                        message="❌ example not followed by code block",
                        suggestion="Add code block after ❌ example"
                    ))

            # Detect orphaned code blocks (not preceded by ✅/❌)
            if re.match(CODE_BLOCK_START, line):
                # Check if previous non-empty line has example marker
                prev_line_idx = i - 1
                while prev_line_idx >= 0 and lines[prev_line_idx].strip() == '':
                    prev_line_idx -= 1

                if prev_line_idx >= 0:
                    prev_line = lines[prev_line_idx]
                    if not (re.match(EXAMPLE_CHECKMARK_PATTERN, prev_line) or
                           re.match(EXAMPLE_CROSSMARK_PATTERN, prev_line)):
                        # Check if it's in a section that should have examples
                        if self._is_example_section(lines, i):
                            orphaned_code_blocks.append(i + 1)

            i += 1

        # Check for imbalanced examples (should have both ✅ and ❌)
        if good_examples and not bad_examples:
            violations.append(Violation(
                file_path=str(file_path),
                line_num=good_examples[0],
                line_content="",
                violation_type="imbalanced_examples",
                severity=Severity.INFO,
                message="Only ✅ examples found, consider adding ❌ anti-patterns",
                suggestion="Add ❌ examples to show what NOT to do"
            ))

        if bad_examples and not good_examples:
            violations.append(Violation(
                file_path=str(file_path),
                line_num=bad_examples[0],
                line_content="",
                violation_type="imbalanced_examples",
                severity=Severity.INFO,
                message="Only ❌ examples found, consider adding ✅ correct patterns",
                suggestion="Add ✅ examples to show correct usage"
            ))

        return violations, has_examples

    def _is_example_section(self, lines: List[str], line_idx: int) -> bool:
        """Check if line is in a section that should have examples."""
        # Look backwards for section headers
        for i in range(line_idx - 1, max(0, line_idx - 20), -1):
            line = lines[i].lower()
            if re.match(r'^#+\s+(examples?|patterns?|usage|anti-patterns?)', line):
                return True
        return False


class AntiPatternChecker:
    """Checks for documented anti-patterns and best practices."""

    def check_file(self, file_path: Path, lines: List[str]) -> Tuple[List[Violation], bool]:
        """Check if file documents anti-patterns. Returns (violations, has_anti_patterns)."""
        violations = []
        content = '\n'.join(lines).lower()

        # Check for anti-pattern documentation
        has_anti_patterns = bool(
            re.search(r'anti[-\s]pattern', content) or
            re.search(r'❌.*wrong', content) or
            re.search(r'don\'?t', content) or
            re.search(r'avoid', content)
        )

        # Check for best practices section
        has_best_practices = bool(
            re.search(r'best\s+practice', content) or
            re.search(r'✅.*correct', content) or
            re.search(r'recommended', content)
        )

        # Skills should document what NOT to do
        if not has_anti_patterns and len(lines) > 100:
            violations.append(Violation(
                file_path=str(file_path),
                line_num=1,
                line_content="",
                violation_type="missing_anti_patterns",
                severity=Severity.INFO,
                message="No anti-patterns documented",
                suggestion="Consider adding section on common mistakes/anti-patterns"
            ))

        return violations, has_anti_patterns


# ============================================================================
# REPORT GENERATION
# ============================================================================

class ReportGenerator:
    """Generates quality reports in various formats."""

    def __init__(self, reports: List[FileReport], verbose: bool = False):
        self.reports = reports
        self.verbose = verbose

    def generate_summary(self) -> str:
        """Generate summary statistics."""
        total_files = len(self.reports)
        files_with_violations = sum(1 for r in self.reports if r.violations)

        total_errors = sum(r.error_count for r in self.reports)
        total_warnings = sum(r.warning_count for r in self.reports)
        total_info = sum(r.info_count for r in self.reports)
        total_violations = total_errors + total_warnings + total_info

        files_with_examples = sum(1 for r in self.reports if r.has_examples)
        files_with_anti_patterns = sum(1 for r in self.reports if r.has_anti_patterns)

        lines = [
            "=" * 80,
            "VOICE CONSISTENCY & EXAMPLE FORMAT REPORT",
            "=" * 80,
            f"Files checked: {total_files}",
            f"Files with violations: {files_with_violations}",
            f"",
            f"Violations by severity:",
            f"  Errors:   {total_errors:4d}  (critical, blocks CI)",
            f"  Warnings: {total_warnings:4d}  (should fix)",
            f"  Info:     {total_info:4d}  (suggestions)",
            f"  Total:    {total_violations:4d}",
            f"",
            f"Quality metrics:",
            f"  Files with ✅/❌ examples: {files_with_examples}/{total_files}",
            f"  Files with anti-patterns:  {files_with_anti_patterns}/{total_files}",
            "=" * 80,
        ]

        return '\n'.join(lines)

    def generate_detail(self, max_violations_per_file: int = 10) -> str:
        """Generate detailed violation report."""
        lines = []

        for report in self.reports:
            if not report.violations:
                continue

            rel_path = report.file_path
            lines.append(f"\n📄 {rel_path}")
            lines.append(f"   {report.error_count} errors, {report.warning_count} warnings, {report.info_count} info")
            lines.append("-" * 80)

            # Group violations by type
            by_type: Dict[str, List[Violation]] = {}
            for v in report.violations:
                by_type.setdefault(v.violation_type, []).append(v)

            for vtype, violations in sorted(by_type.items()):
                lines.append(f"\n  {vtype.replace('_', ' ').title()} ({len(violations)}):")

                for v in violations[:max_violations_per_file]:
                    severity_icon = "🔴" if v.severity == Severity.ERROR else "🟡" if v.severity == Severity.WARNING else "🔵"
                    lines.append(f"    {severity_icon} Line {v.line_num}: {v.message}")
                    if v.matched_text:
                        lines.append(f"       Matched: \"{v.matched_text}\"")
                    if v.suggestion:
                        lines.append(f"       Fix: {v.suggestion}")
                    if self.verbose and v.line_content.strip():
                        lines.append(f"       Context: {v.line_content.strip()}")
                    lines.append("")

                if len(violations) > max_violations_per_file:
                    lines.append(f"    ... and {len(violations) - max_violations_per_file} more")
                    lines.append("")

        return '\n'.join(lines)

    def generate_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            "# Voice Consistency & Example Format Report",
            "",
            "## Summary",
            "",
        ]

        # Add summary table
        total_files = len(self.reports)
        files_with_violations = sum(1 for r in self.reports if r.violations)
        total_errors = sum(r.error_count for r in self.reports)
        total_warnings = sum(r.warning_count for r in self.reports)
        total_info = sum(r.info_count for r in self.reports)

        lines.extend([
            f"- **Files checked:** {total_files}",
            f"- **Files with violations:** {files_with_violations}",
            f"- **Errors:** {total_errors} (critical)",
            f"- **Warnings:** {total_warnings}",
            f"- **Info:** {total_info}",
            "",
            "## Violations by File",
            "",
        ])

        for report in self.reports:
            if not report.violations:
                continue

            lines.append(f"### {report.file_path}")
            lines.append("")
            lines.append(f"**{report.error_count}** errors, **{report.warning_count}** warnings, **{report.info_count}** info")
            lines.append("")

            # Group by type
            by_type: Dict[str, List[Violation]] = {}
            for v in report.violations:
                by_type.setdefault(v.violation_type, []).append(v)

            for vtype, violations in sorted(by_type.items()):
                lines.append(f"#### {vtype.replace('_', ' ').title()}")
                lines.append("")

                for v in violations[:10]:
                    severity = "🔴" if v.severity == Severity.ERROR else "🟡" if v.severity == Severity.WARNING else "🔵"
                    lines.append(f"- {severity} **Line {v.line_num}:** {v.message}")
                    if v.suggestion:
                        lines.append(f"  - *Fix:* {v.suggestion}")
                    lines.append("")

        return '\n'.join(lines)

    def generate_json(self) -> str:
        """Generate JSON report."""
        data = {
            "summary": {
                "total_files": len(self.reports),
                "files_with_violations": sum(1 for r in self.reports if r.violations),
                "total_errors": sum(r.error_count for r in self.reports),
                "total_warnings": sum(r.warning_count for r in self.reports),
                "total_info": sum(r.info_count for r in self.reports),
            },
            "files": [
                {
                    "path": str(r.file_path),
                    "violations": [v.to_dict() for v in r.violations],
                    "error_count": r.error_count,
                    "warning_count": r.warning_count,
                    "info_count": r.info_count,
                }
                for r in self.reports if r.violations
            ]
        }
        return json.dumps(data, indent=2)


# ============================================================================
# MAIN CHECKER
# ============================================================================

class SkillQualityChecker:
    """Main checker coordinating all quality checks."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.reports: List[FileReport] = []

    def check_file(self, file_path: Path) -> FileReport:
        """Check a single skill file."""
        report = FileReport(file_path=file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            report.line_count = len(lines)

            # Build context detector
            context = ContextDetector(lines)

            # Run checkers
            voice_checker = VoiceConsistencyChecker(context)
            example_checker = ExampleFormatChecker(context)
            anti_pattern_checker = AntiPatternChecker()

            # Collect violations
            report.violations.extend(voice_checker.check_file(file_path, lines))

            example_violations, has_examples = example_checker.check_file(file_path, lines)
            report.violations.extend(example_violations)
            report.has_examples = has_examples

            anti_pattern_violations, has_anti_patterns = anti_pattern_checker.check_file(file_path, lines)
            report.violations.extend(anti_pattern_violations)
            report.has_anti_patterns = has_anti_patterns

        except Exception as e:
            print(f"Error checking {file_path}: {e}", file=sys.stderr)

        return report

    def check_directory(self, directory: Path, pattern: str = "**/SKILL.md") -> List[FileReport]:
        """Check all skill files in directory."""
        skill_files = sorted(directory.glob(pattern))

        if self.verbose:
            print(f"Found {len(skill_files)} skill files to check...")

        for skill_file in skill_files:
            if self.verbose:
                print(f"Checking {skill_file.relative_to(directory)}...")
            report = self.check_file(skill_file)
            self.reports.append(report)

        return self.reports

    def get_exit_code(self) -> int:
        """Get exit code based on violations (0 = pass, 1 = fail)."""
        total_errors = sum(r.error_count for r in self.reports)
        return 1 if total_errors > 0 else 0


# ============================================================================
# CLI
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check voice consistency and example format in Claude Code skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Check all skills
  %(prog)s --path universal/            # Check specific directory
  %(prog)s --verbose                    # Detailed output
  %(prog)s --report report.md           # Generate markdown report
  %(prog)s --ci                         # CI mode (strict, exit 1 on warnings or errors)
  %(prog)s --format json > report.json  # JSON output
        """
    )

    parser.add_argument(
        '--path',
        type=Path,
        default=None,
        help='Specific directory or file to check (default: all skills)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with line context'
    )

    parser.add_argument(
        '--report',
        type=Path,
        help='Generate report file (markdown)'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--ci',
        action='store_true',
        help='CI mode: strict checking, exit 1 on warnings or errors'
    )

    parser.add_argument(
        '--max-violations',
        type=int,
        default=10,
        help='Max violations to show per file (default: 10)'
    )

    args = parser.parse_args()

    # Determine root directory
    if args.path:
        check_path = args.path
    else:
        repo_root = Path(__file__).parent.parent
        default_roots = [
            repo_root / "toolchains",
            repo_root / "universal",
            repo_root / "examples",
        ]
        check_paths = [p for p in default_roots if p.exists()]
        check_path = None

    # Run checks
    checker = SkillQualityChecker(verbose=args.verbose)

    if check_path is not None:
        if check_path.is_file():
            checker.reports.append(checker.check_file(check_path))
        else:
            checker.check_directory(check_path)
    else:
        for root in check_paths:
            checker.check_directory(root)

    # Generate report
    generator = ReportGenerator(checker.reports, verbose=args.verbose)

    # Output results
    if args.format == 'json':
        output = generator.generate_json()
        print(output)
        # Don't print status messages in JSON mode
    elif args.format == 'markdown':
        output = generator.generate_markdown()
        print(output)
        # Don't print status messages in markdown mode
    else:
        output = generator.generate_summary()
        if checker.reports and any(r.violations for r in checker.reports):
            output += "\n" + generator.generate_detail(max_violations_per_file=args.max_violations)
        print(output)

        # Success/failure message (text mode only)
        total_errors = sum(r.error_count for r in checker.reports)
        total_warnings = sum(r.warning_count for r in checker.reports)

        if total_errors == 0 and total_warnings == 0:
            print("\n✅ All checks passed! Skills maintain high quality standards.")
        elif total_errors == 0:
            print(f"\n⚠️  {total_warnings} warnings found. Consider fixing for better quality.")
        else:
            print(f"\n❌ {total_errors} errors found. Fix before merging.")

    # Save report file
    if args.report:
        report_content = generator.generate_markdown()
        args.report.write_text(report_content)
        if args.format != 'json':  # Don't print in JSON mode
            print(f"\nReport saved to {args.report}")

    # Return exit code
    total_errors = sum(r.error_count for r in checker.reports)
    if total_errors > 0:
        return 1
    elif args.ci and sum(r.warning_count for r in checker.reports) > 0:
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
