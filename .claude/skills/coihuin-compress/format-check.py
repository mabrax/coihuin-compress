#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
Checkpoint format validator for coihuin-compress.

Usage:
    uv run format-check.py <file>
"""

import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

import yaml


class ValidationResult(NamedTuple):
    valid: bool
    errors: list[str]
    structural_warnings: list[str]
    advisory_warnings: list[str]


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
CHECKPOINT_FRONTMATTER_OPTIONAL = ["anchor", "last_delta"]


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


def extract_section_content(body: str, section_name: str) -> str:
    """Extract the content of a ## section until the next ## or end of file."""
    lines = body.split("\n")
    in_section = False
    content_lines = []

    for line in lines:
        if line.startswith("## "):
            if in_section:
                break  # Found next section, stop
            if section_name.lower() in line.lower():
                in_section = True
                continue
        elif in_section:
            content_lines.append(line)

    return "\n".join(content_lines).strip()


def extract_subsection_content(body: str, section_name: str, subsection_name: str) -> str:
    """Extract the content of a ### subsection within a ## section."""
    section_content = extract_section_content(body, section_name)
    if not section_content:
        return ""

    lines = section_content.split("\n")
    in_subsection = False
    content_lines = []

    for line in lines:
        if line.startswith("### "):
            if in_subsection:
                break  # Found next subsection, stop
            if subsection_name.lower() in line.lower():
                in_subsection = True
                continue
        elif in_subsection:
            content_lines.append(line)

    return "\n".join(content_lines).strip()


def count_list_items(text: str) -> int:
    """Count list items (lines starting with - or numbered lists)."""
    count = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            count += 1
        elif re.match(r"^\d+\.\s", stripped):
            count += 1
    return count


def parse_iso_datetime(date_str: str) -> datetime | None:
    """Parse ISO 8601 datetime string (e.g., 2025-12-17T10:30:00Z)."""
    if not date_str:
        return None
    try:
        # Handle both 'Z' and '+00:00' timezone formats
        if isinstance(date_str, str):
            date_str = date_str.replace("Z", "+00:00")
            return datetime.fromisoformat(date_str)
        elif isinstance(date_str, datetime):
            return date_str
    except (ValueError, TypeError):
        return None
    return None


def check_advisory_heuristics(frontmatter: dict | None, body: str) -> list[str]:
    """Check advisory heuristics and return warnings."""
    warnings = []
    now = datetime.now(timezone.utc)

    # 1. Problem length < 20 words
    problem_text = extract_section_content(body, "Problem")
    word_count = len(problem_text.split())
    if word_count < 20:
        warnings.append(f"Problem section is brief ({word_count} words, recommend >= 20)")

    # 2. Decisions count < 2
    decisions_text = extract_subsection_content(body, "Essential Information", "Decisions")
    decisions_count = count_list_items(decisions_text)
    if decisions_count < 2:
        warnings.append(f"Few decisions recorded ({decisions_count}, recommend >= 2)")

    # 3. Play-By-Play < 2 entries
    playbyplay_text = extract_subsection_content(body, "Essential Information", "Play-By-Play")
    playbyplay_count = count_list_items(playbyplay_text)
    if playbyplay_count < 2:
        warnings.append(f"Play-By-Play has few entries ({playbyplay_count}, recommend >= 2)")

    # 4. Artifact Trail empty
    artifact_text = extract_subsection_content(body, "Essential Information", "Artifact Trail")
    if not artifact_text.strip():
        warnings.append("Artifact Trail is empty")

    # 5. Next Actions empty
    next_actions_text = extract_subsection_content(body, "Essential Information", "Next Actions")
    if not next_actions_text.strip():
        warnings.append("Next Actions is empty")

    # 6. Current State < 30 words
    current_state_text = extract_subsection_content(body, "Essential Information", "Current State")
    state_word_count = len(current_state_text.split())
    if state_word_count < 30:
        warnings.append(f"Current State is brief ({state_word_count} words, recommend >= 30)")

    # 7. Checkpoint age > 7 days (using created field)
    if frontmatter and "created" in frontmatter:
        created = parse_iso_datetime(str(frontmatter["created"]))
        if created:
            age = now - created
            if age > timedelta(days=7):
                warnings.append(f"Checkpoint is {age.days} days old (consider refreshing if still active)")

    # 8. Last delta > 3 days (using last_delta field, skip if missing)
    if frontmatter and "last_delta" in frontmatter:
        last_delta = parse_iso_datetime(str(frontmatter["last_delta"]))
        if last_delta:
            delta_age = now - last_delta
            if delta_age > timedelta(days=3):
                warnings.append(f"Last delta was {delta_age.days} days ago (consider updating)")

    return warnings


def validate_checkpoint(content: str) -> ValidationResult:
    """Validate checkpoint format (structural) and check advisory heuristics."""
    errors = []
    structural_warnings = []

    frontmatter, body = extract_frontmatter(content)

    # Check frontmatter
    if frontmatter is None:
        structural_warnings.append("Missing YAML frontmatter (recommended: checkpoint, created, anchor)")
    else:
        for field in CHECKPOINT_FRONTMATTER_REQUIRED:
            if field not in frontmatter:
                errors.append(f"Missing required frontmatter field: {field}")
        for field in CHECKPOINT_FRONTMATTER_OPTIONAL:
            if field not in frontmatter:
                structural_warnings.append(f"Missing optional frontmatter field: {field}")

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
                structural_warnings.append(f"Missing recommended subsection: ### {sub}")

    # Run advisory heuristics (only if structural validation passes)
    advisory_warnings = []
    if len(errors) == 0:
        advisory_warnings = check_advisory_heuristics(frontmatter, body if frontmatter else content)

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        structural_warnings=structural_warnings,
        advisory_warnings=advisory_warnings,
    )


def is_checkpoint(content: str) -> bool:
    """Check if content appears to be a checkpoint."""
    frontmatter, _ = extract_frontmatter(content)

    if frontmatter and "checkpoint" in frontmatter:
        return True

    # Heuristics
    content_lower = content.lower()
    if "## problem" in content_lower or "## essential information" in content_lower:
        return True

    return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    file_path = sys.argv[1]

    # Read file
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()

    # Verify it looks like a checkpoint
    if not is_checkpoint(content):
        print("Error: File does not appear to be a checkpoint.")
        print("Expected: YAML frontmatter with 'checkpoint' field, or ## Problem / ## Essential Information sections.")
        sys.exit(1)

    # Validate checkpoint
    result = validate_checkpoint(content)

    # Output results in two-layer format
    print(f"\nFormat check: {file_path}")
    print("=" * 60)

    # Layer 1: Structural Validation
    if result.valid:
        print("\nSTRUCTURAL VALIDATION: Pass")
        print("  All required sections and fields present")
        if result.structural_warnings:
            print(f"  ({len(result.structural_warnings)} structural warnings)")
            for warning in result.structural_warnings:
                print(f"    - {warning}")
    else:
        print("\nSTRUCTURAL VALIDATION: Fail")
        print(f"  {len(result.errors)} errors found:")
        for error in result.errors:
            print(f"    - {error}")
        if result.structural_warnings:
            print(f"  {len(result.structural_warnings)} warnings:")
            for warning in result.structural_warnings:
                print(f"    - {warning}")

    # Layer 2: Advisory Heuristics (only shown if structural validation passes)
    if result.valid:
        if result.advisory_warnings:
            print(f"\nADVISORY HEURISTICS: {len(result.advisory_warnings)} warnings")
            for warning in result.advisory_warnings:
                print(f"  - {warning}")
        else:
            print("\nADVISORY HEURISTICS: No warnings")

    # Disclaimer footer
    print("\n" + "-" * 60)
    print("Note: This tool checks format, not content quality.")
    print("A valid checkpoint may still be insufficient for work resumption.")

    # Exit codes: 0 on structural pass (even with heuristic warnings), 1 on structural errors
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
