#!/usr/bin/env python3
"""
Generate token-count summaries from manifest.json for dashboards or CI checks.

Usage:
  python scripts/token_report.py --manifest manifest.json
  python scripts/token_report.py --manifest manifest.json --out stats/token-summary.json
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any


def summarize(manifest: Dict[str, Any]) -> Dict[str, Any]:
    skills = []
    for section in manifest.get("skills", {}).values():
        if isinstance(section, list):
            skills.extend(section)
        elif isinstance(section, dict):
            for arr in section.values():
                skills.extend(arr)

    entry_total = sum(s.get("entry_point_tokens", 0) for s in skills)
    full_total = sum(s.get("full_tokens", 0) for s in skills)

    return {
        "total_skills": len(skills),
        "entry_point_tokens_total": entry_total,
        "full_tokens_total": full_total,
        "categories": manifest.get("metadata", {}).get("categories"),
        "toolchains": manifest.get("metadata", {}).get("toolchains"),
        "last_updated": manifest.get("metadata", {}).get("last_updated") or manifest.get("updated"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Token summary for skills manifest.")
    parser.add_argument("--manifest", default="manifest.json", help="Path to manifest.json")
    parser.add_argument("--out", help="Optional path to write JSON summary")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text())
    summary = summarize(data)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, indent=2) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
