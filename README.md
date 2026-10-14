# Universal Zero-Context State Persistence & Micro-Step Journaling

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-Zero-success.svg)]()
[![Schema: v1.0 Compliant](https://img.shields.io/badge/Schema-v1.0%20Compliant-orange.svg)]()

A production-grade, reusable **AI Agent Skill Package** designed to eliminate AI agent amnesia, context truncation decay, and multi-session hallucinations through deterministic cold-start state transfer.

Compatible with **Google Antigravity**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and any autonomous coding agent framework.

---

## The Problem: Total Ambient Amnesia in AI Coding Agents

When working on complex projects, autonomous AI coding agents inevitably face:
- **Context Compaction & Truncation**: Older turns are compressed or dropped once token thresholds are reached.
- **Session Restarts & Tool Crashes**: Network disconnects, IDE reloads, or process timeouts wipe active conversational memory.
- **Subagent Delegations**: Worker subagents spawn into clean, isolated contexts with zero memory of previous chats.

### The Failure Cascade
Without an externalized, standardized persistence layer, restarting agents succumb to predictable anti-patterns:
1. **Speculative Re-Exploration**: Scanning directories, re-reading dozens of files, and re-running exploratory search tools.
2. **Regression Overwriting**: Re-authoring working components from scratch because they cannot verify what was already implemented.
3. **The "One More Thing" Loop**: Failing to halt when commanded to stop or pause, burning tokens on unauthorized diagnostic loops.

---

## The Architecture: Externalized Ground Truth

```
┌────────────────────────────────────────────────────────┐
│                      SESSION N                         │
│  - Executes verified micro-steps                       │
│  - Hits pause, exit, or context boundary               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ (Immediate Halt Discipline)
              ┌───────────────────────────┐
              │        JOURNAL.md         │
              │  1. Completed Micro-steps │
              │  2. Pending Tasks & %     │
              │  3. Milestones & Remarks  │
              │  4. Rolling Ground Truth  │
              └─────────────┬─────────────┘
                            │
                            ▼ (Zero-Context Cold Start)
┌────────────────────────────────────────────────────────┐
│                     SESSION N+1                        │
│  - Bypasses exploratory file scans                     │
│  - Reads Section 4: "Immediate Next Action"            │
│  - Resumes execution on the very first tool call       │
└────────────────────────────────────────────────────────┘
```

---

## The Standardized 4-Part Schema

Every journal file (`JOURNAL.md`) strictly adheres to a battle-tested four-part contract:

### 1. Completed Task List (Micro-Steps Down to Minute Detail)
Records every individual step executed so far. Avoids generic claims like "worked on backend".
- **Format**: `- [x] <Title>: <Exact details>`
- **Requirements**: Must cite relative file paths (`src/auth/jwt.ts`), modified line ranges/functions, specific CLI commands run, memory addresses/offsets, or exact error codes resolved.

### 2. Pending (Ongoing / Unfinished)
Declares all currently active, interrupted, or incomplete work.
- **Requirements**:
  - Must declare an explicit progress indicator (e.g. `### [Progress 65%] Task Title`).
  - Must provide a sequential checklist of concrete objectives required to reach 100%.

### 3. Milestone (User Remarks & Future Backlog)
Captures external user feedback, long-term roadmap aspirations, and non-blocking backlog ideas.
- Documented with architectural prerequisites.

### 4. Summary (MUST — Rolling Ground Truth)
The anchor of cold-start recovery. A high-density technical summary answering three questions:
1. **Proven Findings**: What facts were physically verified with tests/tools?
2. **Current Environment State**: Git branch, commit hash, active background tasks, bound ports, uncommitted files.
3. **Immediate Next Action**: The exact first tool call or file modification the cold-start agent must execute upon resuming.

---

## Directory Structure

```text
zero-context-journaling/
├── SKILL.md                          # Antigravity skill manifest & agent procedures
├── resources/
│   ├── journal_template.md           # Drop-in boilerplate template for JOURNAL.md
│   └── microstep_cheat_sheet.md      # Rules and examples for micro-step precision
├── references/
│   ├── cold_start_architecture.md    # Theoretical foundations on agent memory & compaction
│   └── halt_discipline.md            # Deep dive on halting runaway tool loops on exit
├── examples/
│   ├── reverse_engineering_session.md # Real-world systems/binary reversing journal
│   └── fullstack_refactor_session.md  # Real-world web/database refactoring journal
├── scripts/
│   └── validate_journal.py           # Dependency-free Python linter, validator & scaffolder
├── install.ps1                       # Automated Windows PowerShell installer
├── install.sh                        # Automated Unix/macOS installer
├── LICENSE                           # MIT License
└── README.md                         # Documentation & integration guide
```

---

## Installation & Setup

### For Google Antigravity

#### Option A: Global Installation (Machine-Wide)
Installs the skill into your global Antigravity configuration (`~/.gemini/config/skills/`):

```powershell
# Windows PowerShell
.\install.ps1
```

```bash
# macOS / Linux
chmod +x install.sh
./install.sh
```

#### Option B: Workspace Installation (Project-Specific)
Installs the skill directly into your current repository's `.agents/skills/` folder so your entire team shares it via Git:

```powershell
# Windows PowerShell
.\install.ps1 -Workspace
```

```bash
# macOS / Linux
./install.sh --workspace
```

---

### For Other AI Agents (Claude Code, Cursor, Windsurf, Cline, Aider)

You can use this protocol across any AI coding harness:

1. Copy `resources/journal_template.md` into your project root as `JOURNAL.md`.
2. Add the following directive to your agent instructions (e.g., `CLAUDE.md`, `.cursorrules`, `SYSTEM_PROMPT.md`):

```markdown
Adhere to the Zero-Context State Persistence Protocol:
1. Maintain 'JOURNAL.md' using the 4-part schema (Completed Micro-Steps, Pending Objectives, Milestones, Rolling Summary).
2. On session bootstrap, read Section 4 and immediately execute 'Immediate Next Action' without speculative re-scanning.
3. When directed to pause, stop, or exit, halt immediately, write state to 'JOURNAL.md', and commit changes to git.
```

---

## Automated Linter & Validator: `validate_journal.py`

The package includes a zero-dependency Python script to validate journals, lint micro-steps, and scaffold new templates:

### Run Self-Tests
Verify that the validator's test suite passes:
```bash
python scripts/validate_journal.py --test
```

### Validate an Existing Journal
```bash
python scripts/validate_journal.py path/to/JOURNAL.md
```

### Scaffold a New Compliant Journal
```bash
python scripts/validate_journal.py --scaffold JOURNAL.md
```

### GitHub Actions CI/CD Integration
Add automated validation to pull requests to ensure agents or team members keep the journal up to date:

```yaml
name: Validate State Journal
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Validate Journal Schema
        run: python scripts/validate_journal.py JOURNAL.md
```

---

## License

This project is licensed under the [MIT License](LICENSE).
