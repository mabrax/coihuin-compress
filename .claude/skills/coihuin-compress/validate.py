#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
Checkpoint and Delta format validator for coihuin-compress.

Usage:
    uv run validate.py checkpoint <file>
    uv run validate.py delta <file>
    uv run validate.py <file>  # auto-detect type
"""

import re
import sys
from pathlib import Path
from typing import NamedTuple

import yaml


class ValidationResult(NamedTuple):
    valid: bool
    errors: list[str]
    warnings: list[str]


# Required sections for checkpoint format
CHECKPOINT_REQUIRED_SECTIONS = [
    "Problem",
    "Essential Information",
]

CHECKPOINT_REQUIRED_SUBSECTIONS = [
    "Decisions",
    "Current State",
    "Next Actions",
]

CHECKPOINT_RECOMMENDED_SUBSECTIONS = [
    "Technical Context",
    "Play-By-Play",
    "Artifact Trail",
]

CHECKPOINT_FRONTMATTER_REQUIRED = ["checkpoint", "created"]
CHECKPOINT_FRONTMATTER_OPTIONAL = ["anchor"]

# Required sections for delta format
DELTA_REQUIRED_SECTIONS = [
    "Summary",
    "Changes",
]

DELTA_FRONTMATTER_REQUIRED = ["delta", "from", "to", "created"]


def extract_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter, body
    except yaml.YAMLError:
        return None, content


def extract_sections(content: str) -> dict[str, list[str]]:
    """Extract markdown sections (## headers) and subsections (### headers)."""
    sections: dict[str, list[str]] = {}
    current_section = None

    for line in content.split("\n"):
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections[current_section] = []
        elif line.startswith("### ") and current_section:
            subsection = line[4:].strip()
            sections[current_section].append(subsection)

    return sections


def validate_checkpoint(content: str) -> ValidationResult:
    """Validate checkpoint format."""
    errors = []
    warnings = []

    frontmatter, body = extract_frontmatter(content)

    # Check frontmatter
    if frontmatter is None:
        warnings.append("Missing YAML frontmatter (recommended: checkpoint, created, anchor)")
    else:
        for field in CHECKPOINT_FRONTMATTER_REQUIRED:
            if field not in frontmatter:
                errors.append(f"Missing required frontmatter field: {field}")
        for field in CHECKPOINT_FRONTMATTER_OPTIONAL:
            if field not in frontmatter:
                warnings.append(f"Missing optional frontmatter field: {field}")

    # Extract sections
    sections = extract_sections(body if frontmatter else content)

    # Check required sections
    for section in CHECKPOINT_REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"Missing required section: ## {section}")

    # Check subsections under Essential Information
    if "Essential Information" in sections:
        subsections = sections["Essential Information"]
        for sub in CHECKPOINT_REQUIRED_SUBSECTIONS:
            # Flexible matching (e.g., "Decisions" matches "Decisiones del Usuario")
            if not any(sub.lower() in s.lower() or s.lower() in sub.lower() for s in subsections):
                # Check if it exists as a direct match or partial match
                found = False
                for s in subsections:
                    if sub.lower() in s.lower():
                        found = True
                        break
                if not found:
                    errors.append(f"Missing required subsection: ### {sub}")

        for sub in CHECKPOINT_RECOMMENDED_SUBSECTIONS:
            if not any(sub.lower() in s.lower() for s in subsections):
                warnings.append(f"Missing recommended subsection: ### {sub}")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def validate_delta(content: str) -> ValidationResult:
    """Validate delta format."""
    errors = []
    warnings = []

    frontmatter, body = extract_frontmatter(content)

    # Check frontmatter
    if frontmatter is None:
        warnings.append("Missing YAML frontmatter (recommended: delta, from, to, created)")
    else:
        for field in DELTA_FRONTMATTER_REQUIRED:
            if field not in frontmatter:
                errors.append(f"Missing required frontmatter field: {field}")

    # Extract sections
    sections = extract_sections(body if frontmatter else content)

    # Check required sections (flexible - look for key terms)
    has_summary = any("summary" in s.lower() or "resumen" in s.lower() for s in sections.keys())
    has_changes = any("change" in s.lower() or "delta" in s.lower() for s in sections.keys())

    if not has_summary:
        # Check if there's a summary line at the start
        if "**Resumen:**" not in content and "## Summary" not in content:
            warnings.append("Missing summary section or inline summary")

    # Check for change categories (can be ## or ### level)
    change_keywords = ["added", "modified", "removed", "status", "new", "update"]
    content_lower = content.lower()
    has_change_detail = any(kw in content_lower for kw in change_keywords)

    if not has_change_detail:
        warnings.append("Consider adding explicit change categories (Added/Modified/Removed)")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def detect_type(content: str) -> str:
    """Auto-detect if content is checkpoint or delta."""
    frontmatter, _ = extract_frontmatter(content)

    if frontmatter:
        if "delta" in frontmatter:
            return "delta"
        if "checkpoint" in frontmatter:
            return "checkpoint"

    # Heuristics
    content_lower = content.lower()
    if "delta:" in content_lower or "vs" in content_lower or "changes" in content_lower:
        return "delta"
    if "## problem" in content_lower or "## essential information" in content_lower:
        return "checkpoint"

    return "unknown"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) == 2:
        doc_type = None
        file_path = sys.argv[1]
    else:
        doc_type = sys.argv[1]
        file_path = sys.argv[2]

    # Read file
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()

    # Auto-detect type if not specified
    if doc_type is None or doc_type not in ("checkpoint", "delta"):
        doc_type = detect_type(content)
        if doc_type == "unknown":
            print("Error: Could not detect document type. Specify 'checkpoint' or 'delta'.")
            sys.exit(1)
        print(f"Auto-detected type: {doc_type}")

    # Validate
    if doc_type == "checkpoint":
        result = validate_checkpoint(content)
    else:
        result = validate_delta(content)

    # Output results
    print(f"\nValidating {doc_type}: {file_path}")
    print("=" * 50)

    if result.errors:
        print("\nERRORS:")
        for error in result.errors:
            print(f"  ✗ {error}")

    if result.warnings:
        print("\nWARNINGS:")
        for warning in result.warnings:
            print(f"  ⚠ {warning}")

    if result.valid:
        print(f"\n✓ Valid {doc_type}")
        if result.warnings:
            print(f"  ({len(result.warnings)} warnings)")
        sys.exit(0)
    else:
        print(f"\n✗ Invalid {doc_type}")
        print(f"  ({len(result.errors)} errors, {len(result.warnings)} warnings)")
        sys.exit(1)


if __name__ == "__main__":
    main()
