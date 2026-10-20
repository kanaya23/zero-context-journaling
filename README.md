# Universal Zero-Context State Persistence & Micro-Step Journaling

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-Zero-success.svg)]()
[![Schema: v1.0 Compliant](https://img.shields.io/badge/Schema-v1.0%20Compliant-orange.svg)]()

A production-grade, reusable **AI Agent Skill Package** designed to eliminate AI agent amnesia, context truncation decay, and multi-session hallucinations through deterministic cold-start state transfer and continuous micro-step journaling.

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
4. **Deferred Journaling Amnesia**: Waiting until the end of a session to write logs—losing all context if a crash or abrupt termination occurs midway.

---

## Core Architectural Axioms

### Axiom 0: The Unconditional Invariant: ALWAYS JOURNAL
* **Continuous Persistence**: Journaling is **continuous**, not just a post-session cleanup. **Every feature completed, every action done, every micro-step executed, every offset proven, and every critical command run MUST be immediately recorded in `journal.md`**.
* **Mandatory Journal Summary Reading**: On **every session start, cold start, or entry into a project directory**, read `journal.md` (specifically the **Summary** section) before taking action to recover ground truth without redundant scans.

### Axiom 1: Operational Principle: Cold-Start State Transfer
* Treat every session boundary, context truncation, or restart as an **instantaneous memory wipe**.
* The next session or subagent will have **zero ambient memory** of preceding interactions.
* The project journal (`journal.md`) is the **sole persistent record** that brings any subsequent cold-start agent up to speed immediately with zero hallucination, guesswork, or re-exploration.
* Keep personality neutral, analytical, and professional—never adopt persona or roleplay quirks.

### Axiom 2: Execution Discipline: Immediate Halt on Exit / Stop
* When the user directs the agent to dump findings, log progress, pause, or exit: **HALT IMMEDIATELY**.
* Do **NOT** invoke investigative tools, do **NOT** trigger speculative scans, and do **NOT** enter a "one more thing" loop.
* Immediately write/update the journal file, commit changes to the active version control safety net, clean up volatile resources, and conclude the turn cleanly.

### Axiom 3: Project-Local Placement & Bootstrap Discovery
* **Location Invariant**: Always create and maintain `journal.md` directly in the folder/directory where active changes are occurring (e.g., `project1/journal.md`), **regardless** of where the active shell or working directory is located.
* **Bootstrap Discovery on Entry**:
  - Whenever starting or resuming work on any project directory, immediately inspect it for an existing `journal.md`.
  - **If found**: Read it first (specifically the **Summary** section) to recover ground truth without exploratory scans.
  - **If not found**: Start fresh by initializing a new `journal.md` adhering strictly to the standardized 4-part schema.

---

## The Architecture: Externalized Ground Truth & Continuous Persistence

```
┌────────────────────────────────────────────────────────┐
│               ENTER PROJECT / COLD-START               │
│  - Inspect project root for journal.md                 │
│  - Mandatory Journal Summary Reading (Section 4 & 2)   │
│  - Resume "Immediate Next Action" on first tool call   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│             CONTINUOUS EXECUTION LIFECYCLE             │
│  - Executes verified micro-step                        │
│  - IMMEDIATELY records micro-step in Section 1 (- [x]) │
│  - Updates completion % in Section 2                   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ (Pause / Stop / Exit Trigger)
┌────────────────────────────────────────────────────────┐
│          EXECUTION DISCIPLINE: IMMEDIATE HALT          │
│  - HALT IMMEDIATELY: zero speculative tool calls       │
│  - Freeze Section 4 (Rolling Ground Truth)             │
│  - Commit & push to Git safety net                     │
│  - Clean up volatile resources                         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │        journal.md         │
              │  1. Completed Micro-steps │
              │  2. Pending Tasks & %     │
              │  3. Milestones & Remarks  │
              │  4. Rolling Ground Truth  │
              └───────────────────────────┘
```

---

## The Standardized 4-Part Schema

Every journal file (`journal.md` / `JOURNAL.md`) strictly adheres to a battle-tested four-part contract:

### 1. Completed Task List (Micro-Steps Down to Minute Detail)
Records every individual step executed so far. Avoids generic claims like "worked on backend".
- **Format**: `- [x] <Title>: <Exact details>` or `1. [x] <Title>: <Exact details>`
- **Requirements**: Must cite relative file paths (`src/auth/jwt.ts`), modified line ranges/functions, specific CLI commands run, memory addresses/offsets, or exact error codes resolved.

### 2. Pending (Ongoing / Unfinished)
Declares all currently active, interrupted, or incomplete work.
- **Requirements**:
  - Must declare an explicit progress indicator (e.g. `### Title: Short description ([Progress 65%], specific remaining work left unfinished)`).
  - Must provide a sequential checklist of concrete objectives required to reach 100%.

### 3. Milestone (Optional — User Remarks & Future Backlog)
Include ONLY if the user has requested, remarked upon, or planned an unimplemented future feature or milestone:
- **Format**: `1. Title: Description of the milestone, rationale, and prerequisites.`

### 4. Summary (MUST — Non-Optional, Always Updated Rolling Ground Truth)
The anchor of cold-start recovery. A high-density technical rolling summary answering three questions:
1. **Proven Findings**: The exact chronological actions completed and findings proven with tests/tools.
2. **Current Ground-Truth Environment State**: Git branch, commit hash, active background tasks, bound ports, uncommitted files, verified anchors.
3. **Immediate Next Action**: The precise immediate action or tool call to take the moment work resumes.

---

## Directory Structure

```text
zero-context-journaling/
├── SKILL.md                          # Antigravity skill manifest & agent procedures
├── resources/
│   ├── journal_template.md           # Drop-in boilerplate template for journal.md
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

1. Copy `resources/journal_template.md` into your project root as `journal.md`.
2. Add the following directive to your agent instructions (e.g., `CLAUDE.md`, `.cursorrules`, `SYSTEM_PROMPT.md`):

```markdown
Adhere to the Zero-Context State Persistence Protocol:
1. Axiom 0 (ALWAYS JOURNAL): Record every completed micro-step, action, offset, or critical command immediately into 'journal.md'. On every session start or entry into a project, execute Mandatory Journal Summary Reading on Section 4 before taking action.
2. Maintain 'journal.md' using the 4-part schema (Completed Micro-Steps, Pending Objectives, Milestones, Rolling Summary).
3. Colocate 'journal.md' directly inside the project root where active changes are occurring.
4. When directed to pause, stop, or exit: HALT IMMEDIATELY. Do not run speculative scans. Refresh Section 4 and commit to Git.
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
python scripts/validate_journal.py path/to/journal.md
```

### Scaffold a New Compliant Journal
```bash
python scripts/validate_journal.py --scaffold journal.md
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
        run: python scripts/validate_journal.py journal.md
```

---

## License

This project is licensed under the [MIT License](LICENSE).
