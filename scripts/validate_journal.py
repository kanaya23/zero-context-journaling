#!/usr/bin/env python3
"""
Zero-Context Journal Validator & Linter (validate_journal.py)
Validates that a JOURNAL.md or state tracker adheres to the Universal Zero-Context
State Persistence Schema.

Zero external dependencies - standard library only.
Supports CI/CD integration, automated linting, test suites, and scaffolding.
"""

import sys
import os
import re
import argparse
from typing import List, Tuple, Dict, Any

# Required top-level schema sections
SECTION_PATTERNS = {
    "completed": re.compile(r"^##\s+1\.\s+Completed\s+Task\s+List", re.IGNORECASE | re.MULTILINE),
    "pending": re.compile(r"^##\s+2\.\s+Pending", re.IGNORECASE | re.MULTILINE),
    "milestone": re.compile(r"^##\s+3\.\s+Milestone", re.IGNORECASE | re.MULTILINE),
    "summary": re.compile(r"^##\s+4\.\s+Summary", re.IGNORECASE | re.MULTILINE),
}

PROGRESS_REGEX = re.compile(r"\[Progress\s+(\d+)%\]", re.IGNORECASE)
CHECKBOX_REGEX = re.compile(r"^[\s\t]*-\s+\[([ xX])\]\s+(.+)$", re.MULTILINE)
NEXT_ACTION_REGEX = re.compile(r"(Immediate\s+Next\s+Action|Next\s+Action|Next\s+Step|Resumption\s+Action)", re.IGNORECASE)
ENV_STATE_REGEX = re.compile(r"(Environment\s+State|Active\s+Processes|Git\s+Branch|Current\s+State)", re.IGNORECASE)

SCAFFOLD_TEMPLATE = """# Project State & Execution Journal

## 1. Completed Task List (Micro-Steps)
<!-- Record completed items as: - [x] Title: details and verification outcome -->
- [x] Initial State: Verified repository structure and environment baseline.

## 2. Pending (Ongoing / Unfinished)
<!-- Active work with explicit completion percentage and concrete objectives -->
### [Progress 0%] Task Title
- [ ] Concrete actionable objective 1
- [ ] Concrete actionable objective 2

## 3. Milestone (User Remarks & Future Backlog)
<!-- Long-term milestones and user requests outside current sprint -->
- Future Roadmap Item: Description of user request and prerequisites.

## 4. Summary (Rolling Ground Truth)
### Proven Findings & Verifications
- Baseline environment initialized and verified.

### Current Ground-Truth Environment State
- Git Branch: main
- Active Processes: None
- Bound Ports: None

### Immediate Next Action Upon Resuming
- Define immediate next step here.
"""


class JournalValidator:
    def __init__(self, content: str):
        self.content = content
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        self.errors.clear()
        self.warnings.clear()

        # 1. Section Header Verification
        for sec_name, pattern in SECTION_PATTERNS.items():
            if not pattern.search(self.content):
                self.errors.append(f"Missing required section: '## {self._section_display_name(sec_name)}'")

        if self.errors:
            # If fundamental sections are missing, stop deep check
            return False

        # 2. Section 1 (Completed Tasks) Quality Checks
        self._check_completed_section()

        # 3. Section 2 (Pending) Progress Checks
        self._check_pending_section()

        # 4. Section 4 (Summary) Ground Truth Checks
        self._check_summary_section()

        return len(self.errors) == 0

    def _section_display_name(self, name: str) -> str:
        names = {
            "completed": "1. Completed Task List (Micro-Steps)",
            "pending": "2. Pending (Ongoing / Unfinished)",
            "milestone": "3. Milestone (User Remarks & Future Backlog)",
            "summary": "4. Summary (Rolling Ground Truth)",
        }
        return names.get(name, name)

    def _extract_section(self, sec_key: str, next_key: str = None) -> str:
        pattern = SECTION_PATTERNS[sec_key]
        match = pattern.search(self.content)
        if not match:
            return ""
        start = match.end()

        if next_key and next_key in SECTION_PATTERNS:
            next_match = SECTION_PATTERNS[next_key].search(self.content, start)
            end = next_match.start() if next_match else len(self.content)
        else:
            end = len(self.content)

        return self.content[start:end]

    def _check_completed_section(self):
        sec_text = self._extract_section("completed", "pending")
        checkboxes = CHECKBOX_REGEX.findall(sec_text)

        if not checkboxes:
            self.warnings.append("Section 1 has no completed micro-step checkbox items (`- [x]`).")
            return

        for state, desc in checkboxes:
            clean_desc = desc.strip()
            if len(clean_desc) < 15:
                self.warnings.append(f"Micro-step too short/vague: '- [{state}] {clean_desc}' (aim for file paths, commands, or verification outcomes).")

    def _check_pending_section(self):
        sec_text = self._extract_section("pending", "milestone")
        has_progress = PROGRESS_REGEX.search(sec_text)

        # If there are subheadings or text indicating active tasks, check for progress tag
        if "###" in sec_text and not has_progress:
            self.warnings.append("Section 2 active tasks should declare an explicit progress indicator (e.g. `### [Progress 50%] Task Name`).")

        # Check for bulleted/numbered objectives
        lines = [l.strip() for l in sec_text.splitlines() if l.strip() and not l.strip().startswith("<!--")]
        action_items = [l for l in lines if l.startswith("-") or l.startswith("*") or (len(l) > 2 and l[0].isdigit() and l[1] in ".")]
        if lines and not action_items and "none" not in sec_text.lower():
            self.warnings.append("Section 2 should list concrete sequential objectives for pending tasks.")

    def _check_summary_section(self):
        sec_text = self._extract_section("summary")

        if not NEXT_ACTION_REGEX.search(sec_text):
            self.errors.append("Section 4 MUST include an 'Immediate Next Action' anchor for cold-start resumption.")

        if not ENV_STATE_REGEX.search(sec_text):
            self.warnings.append("Section 4 should describe the current ground-truth environment state (active branch, processes, or ports).")


def run_tests() -> int:
    """Built-in test suite for self-validation."""
    print("Running Zero-Context Journal Validator Test Suite...")

    # Test 1: Valid schema
    valid_sample = """# Project State & Execution Journal

## 1. Completed Task List (Micro-Steps)
- [x] Initial Scaffolding: Authored config files in src/config.ts; verified with npm test.
- [x] Database Migration: Generated migration 001_auth.sql; executed migrate up.

## 2. Pending (Ongoing / Unfinished)
### [Progress 50%] JWT Auth Flow
- [x] Generate RS256 keys
- [ ] Add middleware in src/auth.ts

## 3. Milestone (User Remarks & Future Backlog)
- Future Scale: Redis cluster migration.

## 4. Summary (Rolling Ground Truth)
### Current Ground-Truth Environment State
- Git Branch: feature/auth (commit 4b2c1d pushed).
- Active Processes: Node.js on port 3000.

### Immediate Next Action Upon Resuming
- Implement verifyToken in src/auth.ts line 42 and test with curl.
"""
    validator = JournalValidator(valid_sample)
    assert validator.validate(), f"Valid sample failed: {validator.errors}"
    assert len(validator.warnings) == 0, f"Unexpected warnings: {validator.warnings}"
    print("  [PASS] Test 1: Full compliant journal passes validation.")

    # Test 2: Missing Next Action
    missing_action_sample = valid_sample.replace("Immediate Next Action Upon Resuming", "Other Notes")
    validator2 = JournalValidator(missing_action_sample)
    assert not validator2.validate(), "Should fail when Immediate Next Action is missing."
    assert any("Immediate Next Action" in err for err in validator2.errors)
    print("  [PASS] Test 2: Missing Immediate Next Action rejected.")

    # Test 3: Missing Required Section
    missing_sec_sample = """# State
## 1. Completed Task List (Micro-Steps)
- [x] Step 1
## 4. Summary (Rolling Ground Truth)
Immediate Next Action: Do something.
"""
    validator3 = JournalValidator(missing_sec_sample)
    assert not validator3.validate()
    assert len(validator3.errors) >= 2
    print("  [PASS] Test 3: Missing sections detected and rejected.")

    # Test 4: Scaffolding test
    validator4 = JournalValidator(SCAFFOLD_TEMPLATE)
    assert validator4.validate(), f"Scaffold template failed: {validator4.errors}"
    print("  [PASS] Test 4: Default scaffold template is 100% compliant.")

    print("\nAll 4 unit tests passed successfully!")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Linter and validator for Universal Zero-Context State Persistence Journals."
    )
    parser.add_argument("file", nargs="?", default="JOURNAL.md", help="Path to journal file (default: JOURNAL.md)")
    parser.add_argument("--test", action="store_true", help="Run the internal self-test suite")
    parser.add_argument("--scaffold", action="store_true", help="Scaffold a new compliant JOURNAL.md at target path")
    parser.add_argument("--quiet", "-q", action="store_true", help="Output errors only")

    args = parser.parse_args()

    if args.test:
        sys.exit(run_tests())

    if args.scaffold:
        target_path = args.file
        if os.path.exists(target_path):
            print(f"Error: File '{target_path}' already exists. Refusing to overwrite.", file=sys.stderr)
            sys.exit(1)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(SCAFFOLD_TEMPLATE)
        print(f"Successfully scaffolded compliant journal template at: {target_path}")
        sys.exit(0)

    # Read from file or stdin
    target_path = args.file
    if not os.path.exists(target_path):
        if not sys.stdin.isatty():
            content = sys.stdin.read()
            target_path = "<stdin>"
        else:
            print(f"Error: Target journal file '{target_path}' not found.", file=sys.stderr)
            print("Tip: Run 'python validate_journal.py --scaffold' to create one.", file=sys.stderr)
            sys.exit(1)
    else:
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

    validator = JournalValidator(content)
    is_valid = validator.validate()

    if not args.quiet:
        print(f"Checking '{target_path}' against Zero-Context Persistence Schema...\n")

    if validator.errors:
        print(f"FAILED: {len(validator.errors)} schema error(s) found in {target_path}:", file=sys.stderr)
        for err in validator.errors:
            print(f"  [ERROR] {err}", file=sys.stderr)

    if validator.warnings and not args.quiet:
        print(f"WARNINGS: {len(validator.warnings)} suggestion(s):")
        for warn in validator.warnings:
            print(f"  [WARN]  {warn}")

    if is_valid:
        if not args.quiet:
            print("\nSUCCESS: Journal adheres to Zero-Context Persistence Schema!")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
