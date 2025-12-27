"""
Checkpoint format validator for coihuin-compress.

This module provides validation for checkpoint files and INDEX.md files,
including structural validation and advisory heuristics.
"""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

import yaml


class ValidationResult(NamedTuple):
    """Result of validating a checkpoint or INDEX file."""

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
CHECKPOINT_FRONTMATTER_OPTIONAL = ["anchor", "last_delta", "parent"]


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
            if not any(sub.lower() in s.lower() for s in subsections):
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


def is_index(file_path: Path, content: str) -> bool:
    """Check if file is an INDEX.md file."""
    # Check filename
    if file_path.name == "INDEX.md":
        return True

    # Check for INDEX-specific structure
    if "# Active Checkpoints" in content:
        # Also verify it has the table headers
        if "| Checkpoint | Description | Last Updated |" in content:
            return True

    return False


def extract_table_rows(content: str) -> list[dict[str, str]]:
    """Extract rows from the quick reference table."""
    rows = []
    lines = content.split("\n")
    in_table = False
    header_found = False

    for line in lines:
        stripped = line.strip()
        # Detect table start
        if "| Checkpoint | Description | Last Updated |" in stripped:
            in_table = True
            header_found = True
            continue
        # Skip separator row
        if in_table and stripped.startswith("|") and "---" in stripped:
            continue
        # Parse data rows
        if in_table and stripped.startswith("|") and stripped.endswith("|"):
            parts = [p.strip() for p in stripped.split("|")]
            # parts[0] and parts[-1] are empty due to leading/trailing |
            if len(parts) >= 4:
                checkpoint = parts[1]
                description = parts[2]
                last_updated = parts[3]
                if checkpoint and checkpoint != "Checkpoint":  # Skip header if matched again
                    rows.append({
                        "checkpoint": checkpoint,
                        "description": description,
                        "last_updated": last_updated,
                    })
        # End of table (non-table line after table started)
        elif in_table and header_found and stripped and not stripped.startswith("|"):
            break

    return rows


def extract_summary_sections(content: str) -> dict[str, dict[str, str]]:
    """Extract summary sections (## checkpoint-name) with their fields."""
    summaries = {}
    lines = content.split("\n")
    current_section = None
    current_fields = {}

    for line in lines:
        # Detect section header (## chk-xxx style)
        if line.startswith("## "):
            # Save previous section if exists
            if current_section:
                summaries[current_section] = current_fields
            section_name = line[3:].strip()
            # Only track sections that look like checkpoint names (usually start with chk-)
            if section_name.startswith("chk-") or section_name.lower().startswith("checkpoint"):
                current_section = section_name
                current_fields = {}
            else:
                current_section = None
        # Parse fields within a summary section
        elif current_section:
            if line.startswith("**Problem**:"):
                current_fields["Problem"] = line.replace("**Problem**:", "").strip()
            elif line.startswith("**Scope**:"):
                current_fields["Scope"] = line.replace("**Scope**:", "").strip()
            elif line.startswith("**Status**:"):
                current_fields["Status"] = line.replace("**Status**:", "").strip()

    # Don't forget the last section
    if current_section:
        summaries[current_section] = current_fields

    return summaries


def validate_iso_date(date_str: str) -> bool:
    """Validate ISO-8601 date format (YYYY-MM-DD)."""
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_index(content: str) -> ValidationResult:
    """Validate INDEX.md format."""
    errors = []
    structural_warnings = []
    advisory_warnings = []

    # Check for title
    if "# Active Checkpoints" not in content:
        errors.append("Missing title: # Active Checkpoints")

    # Check for quick reference table headers
    expected_headers = "| Checkpoint | Description | Last Updated |"
    if expected_headers not in content:
        errors.append(f"Missing or incorrect table headers. Expected: {expected_headers}")

    # Extract table rows and summary sections
    table_rows = extract_table_rows(content)
    summary_sections = extract_summary_sections(content)

    # Check if table is empty (not an error, just a note)
    if not table_rows:
        # Check for empty state message
        if "*No active checkpoints" not in content:
            structural_warnings.append("Table is empty but missing empty state message")

    # Validate each table entry
    for row in table_rows:
        checkpoint_name = row["checkpoint"]
        last_updated = row["last_updated"]

        # Check for matching summary section
        if checkpoint_name not in summary_sections:
            errors.append(f"Table entry '{checkpoint_name}' has no matching ## {checkpoint_name} section")

        # Validate date format
        if not validate_iso_date(last_updated):
            errors.append(f"Invalid date format for '{checkpoint_name}': '{last_updated}' (expected YYYY-MM-DD)")

    # Validate each summary section has required fields
    for section_name, fields in summary_sections.items():
        for required_field in ["Problem", "Scope", "Status"]:
            if required_field not in fields or not fields[required_field]:
                errors.append(f"Section '{section_name}' missing required field: **{required_field}**:")

    # Check for orphaned summary sections (sections without table entries)
    table_checkpoints = {row["checkpoint"] for row in table_rows}
    for section_name in summary_sections:
        if section_name not in table_checkpoints:
            structural_warnings.append(f"Summary section '{section_name}' has no matching table entry")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        structural_warnings=structural_warnings,
        advisory_warnings=advisory_warnings,
    )


def validate_file(path: Path) -> ValidationResult:
    """Validate a checkpoint or INDEX file.

    Args:
        path: Path to the file to validate

    Returns:
        ValidationResult with validation status

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file type cannot be determined
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    content = path.read_text()

    # Detect file type and validate accordingly
    if is_index(path, content):
        return validate_index(content)
    elif is_checkpoint(content):
        return validate_checkpoint(content)
    else:
        raise ValueError(
            "File does not appear to be a checkpoint or INDEX.md.\n"
            "Expected:\n"
            "  - Checkpoint: YAML frontmatter with 'checkpoint' field, or ## Problem / ## Essential Information sections\n"
            "  - INDEX: # Active Checkpoints title with quick reference table"
        )


def print_result(result: ValidationResult, file_type: str, path: str) -> None:
    """Print validation result in formatted output.

    Args:
        result: The validation result
        file_type: "checkpoint" or "INDEX"
        path: Path string for display
    """
    # Output results in two-layer format
    print(f"\nFormat check ({file_type}): {path}")
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
