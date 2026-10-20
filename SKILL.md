---
name: zero-context-journaling
description: >-
  Universal zero-context state persistence and micro-step journaling for AI coding agents.
  Enforces continuous journaling invariant (Axiom 0), deterministic cold-start state transfer
  across session wipes, immediate halt discipline on pause/exit, project-local placement, and a
  standardized 4-part state tracker (Completed Micro-Steps, Pending Objectives, Milestones, and
  Rolling Ground-Truth Summary).
---

# Universal Zero-Context State Persistence & Micro-Step Journaling

AI coding agents operate in volatile runtime environments where context windows truncate, tokens compact, and sessions terminate abruptly. When an agent restarts, it suffers from total ambient amnesia.

This skill equips the agent with **Zero-Context State Persistence**: a rigorous operational protocol and standardized journaling schema that ensures any subsequent cold-start agent or session can resume execution instantly with zero hallucination, zero speculative re-exploration, and zero wasted tokens.

---

## 1. Core Architectural Axioms

### Axiom 0: The Unconditional Invariant: ALWAYS JOURNAL
* **Continuous Persistence (Not Just Post-Session Cleanup)**:
  - Journaling is **continuous**, not an afterthought or batch cleanup performed only at exit.
  - **Every feature completed, every action done, every micro-step executed, every offset proven, and every critical command run MUST be immediately recorded in `journal.md`**.
* **Mandatory Journal Summary Reading**:
  - On **every session start, cold start, or entry into a project directory**, read `journal.md` (specifically the **Summary** section) before taking action to recover ground truth without redundant scans.

### Axiom 1: Operational Principle: Cold-Start State Transfer (Assume Total Amnesia)
* Treat every session boundary, context truncation, compact event, or restart as an **instantaneous memory wipe**.
* The next session or subagent will have **zero ambient memory** of previous chat messages, unspoken assumptions, or intermediate tool outputs.
* The persistent project journal / state tracker is the **sole persistent record** that brings any subsequent cold-start agent up to speed immediately with zero hallucination, guesswork, or re-exploration.
* Maintain a strictly **neutral, analytical, and professional** tone. Never adopt conversational personas, roleplay quirks, or conversational fluff that wastes token budget.

### Axiom 2: Execution Discipline: Immediate Halt on Exit / Stop (No "One More Thing")
* When the user issues an instruction to **dump findings, log progress, pause, or exit**:
  1. **HALT IMMEDIATELY**.
  2. Do **NOT** invoke investigative tools (no speculative directory scans, no extra `read_file` calls, no git status exploration).
  3. Do **NOT** enter a "one more thing" loop to fix a newly discovered issue.
  4. Immediately write/update the journal file.
  5. Commit and push modified files to the active version control safety net.
  6. Clean up volatile resources (kill background processes, detach debuggers, free ports).
  7. Conclude the turn cleanly and concisely.

### Axiom 3: Project-Local Placement & Bootstrap Discovery
* **Location Invariant (Colocate with Changes)**:
  - Always create and maintain `journal.md` directly in the folder/directory where active changes are occurring (e.g., `project1/journal.md`), **regardless** of where the active shell or current working directory (`CWD`) is located (e.g., even if executing from `~/system1/`).
  - Never place project-specific journals in global user directories, home directories, or temporary scratch folders unless the project itself resides there.
* **Bootstrap Discovery on Entry (Read vs. Fresh)**:
  - Whenever starting or resuming work on any project directory, immediately inspect it for an existing `journal.md`:
    1. **If it exists**: Read it first (specifically the **Summary** section) to recover ground truth without exploratory scans.
    2. **If it does not exist**: Start fresh by initializing a new `journal.md` following the standardized 4-part schema.

---

## 2. Standardized 4-Part State Tracker Schema

Whenever creating or updating a progress journal, state file, or task tracker across ANY project, adhere strictly to the following 4-part structure:

```markdown
# Project State & Execution Journal

## 1. Completed Task List (Micro-Steps Down to Minute Detail)
1. [x] Title: Short description detailing the exact micro-step and outcome.
2. [x] Title: Short description detailing the exact micro-step and outcome.

## 2. Pending (Ongoing / Unfinished)
### Title: Short description ([Progress %], specific remaining work left unfinished)
- Concrete sequential objective 1
- Concrete sequential objective 2

## 3. Milestone (Optional — User Remarks & Future Backlog)
1. Title: Description of the milestone, rationale, and prerequisites.

## 4. Summary (MUST — Non-Optional, Always Updated Rolling Ground Truth)
- Chronological actions & proven findings
- Current ground-truth environment state
- PRECISE IMMEDIATE ACTION to take upon resume
```

### Deep Section Breakdown

#### Section 1: Completed Task List (Micro-Steps Down to Minute Detail)
Record every individual step executed so far, down to the exact files modified, commands executed, offsets found, or bugs resolved:
- Format: `1. [x] <Title>: <Exact details>` or `- [x] <Title>: <Exact details>`
- Must include: Specific relative file paths (`src/auth/jwt.ts`), line numbers or function names (`verifyToken()`), exact CLI commands run, memory addresses/offsets found, or specific error codes resolved.

#### Section 2: Pending (Ongoing / Unfinished)
Record all currently active, interrupted, or incomplete work:
- Format: `<Title>: <Short description> ([Progress %], <specific remaining work left unfinished>)`
- Must include: Explicit progress percentage (`[Progress 40%]`).
- Must include: Concrete sequential list of objectives required to finish this specific work.
- No ambiguous TODOs without actionable next steps.

#### Section 3: Milestone (Optional — User Remarks & Future Backlog)
Include ONLY if the user has requested, remarked upon, or planned an unimplemented future feature or milestone:
- Format: `<Title>: <Description of the milestone, rationale, and prerequisites>`
- Document architectural prerequisites and external dependencies.

#### Section 4: Summary (MUST — Non-Optional, Always Updated Rolling Ground Truth)
A vivid rolling description summarizing:
1. **Proven Findings**: The exact chronological actions completed and findings proven (e.g., "Endpoint returns 200 with JWT payload; memory offset 0x7FF... contains target vtable").
2. **Current Ground-Truth Environment State**: Active processes, open ports, checked-out git branch, modified uncommitted files, active environment variables, verified anchors.
3. **Immediate Next Action**: The precise immediate action or tool call to take the moment work resumes.

---

## 3. Execution Lifecycle: When to Update the Journal

```
[Enter Project Directory / Session Cold-Start]
          │
          ├──> journal.md exists? ─── YES ──> Mandatory Journal Summary Reading
          │                                   (Read Section 4: Summary & Section 2: Pending)
          │                                                 │
          └──> NO ──> Start fresh journal.md                ▼
                            │                   Resume "Immediate Next Action"
                            │                               │
                            ▼                               ▼
                 ┌─────────────────────────────────────────────────────┐
                 │          CONTINUOUS JOURNALING INVARIANT            │
                 │  Immediately record EVERY completed micro-step,     │
                 │  proven offset, action, or critical command into   │
                 │  Section 1 & 2 of journal.md as it happens          │
                 └──────────────────────────┬──────────────────────────┘
                                            │
                             (User triggers Pause / Exit / Stop)
                                            │
                                            ▼
                               Execution Discipline: Immediate Halt
                                            │
                                            ▼
                           Freeze Section 4 + Commit to VCS
```

1. **On Session Bootstrap / Entering a Project**:
   - Locate the target project directory where changes will occur.
   - Inspect the directory for an existing `journal.md` (or `JOURNAL.md`).
   - **If found**: **Mandatory Journal Summary Reading** — read Section 4 ("Summary: Immediate Next Action") and Section 2 ("Pending") to recover context instantly with zero exploratory tool overhead.
   - **If not found**: Create a fresh `journal.md` in that project directory adhering strictly to the standardized 4-part schema before proceeding with work.

2. **During Active Development (The Continuous Journaling Invariant)**:
   - Journaling is continuous, not just a post-session cleanup.
   - Immediately append every completed micro-step to Section 1 (`- [x]` or `1. [x]`).
   - Keep Section 2 updated with accurate completion percentages and pending sequential objectives.

3. **On Session Suspension (Immediate Halt on Exit / Stop)**:
   - Stop tool invocations instantly. No speculative scans, no "one more thing".
   - Refresh Section 4 with current environment state and the exact resumption command.
   - Commit and push changes to the active version control safety net.
   - Conclude the turn cleanly and concisely.

---

## 4. Anti-Patterns vs. Best Practices

| Anti-Pattern (Fails Cold-Start) | Best Practice (Zero-Context Compliant) |
| :--- | :--- |
| Deferring journaling to session end or post-session cleanup. | **Continuous Journaling**: Recording every micro-step, command, and offset immediately into `journal.md` as soon as executed. |
| Starting session with broad directory scans and re-reading files. | **Mandatory Journal Summary Reading**: Reading Section 4 of `journal.md` first to recover ground truth with zero wasted tokens. |
| Placing `journal.md` in root home or global directory. | **Project-Local Colocation**: Always colocating `journal.md` directly inside the folder where active changes take place. |
| "Refactored user authentication." | `- [x] Refactor Auth Middleware: Updated JWT verification in `src/middleware/auth.ts` lines 42-68 to use RS256; validated with `npm test auth.test.ts` (14 passing).` |
| "Investigate database performance." | `### [Progress 25%] Optimize SQL Queries`<br>`1. Add index on `users.tenant_id``<br>`2. Replace N+1 query in `fetchOrders()` at `src/services/order.ts:88`` |
| Running 5 more bash commands after user says "stop for today". | **Immediate Halt Discipline**: Halting immediately, writing `JOURNAL.md`, committing to git, and printing state summary. |
| Missing Section 4 or vague "Next: continue coding". | `Next Action: Run 'npm run db:migrate' to apply migration 004_add_tenant_index.sql, then check 'curl localhost:3000/api/health'.` |

---

## 5. Supplementary Resources

* **Drop-in Template**: [journal_template.md](./resources/journal_template.md)
* **Micro-Step Formatting Rules**: [microstep_cheat_sheet.md](./resources/microstep_cheat_sheet.md)
* **Cold-Start Architecture Reference**: [cold_start_architecture.md](./references/cold_start_architecture.md)
* **Halt Discipline Deep-Dive**: [halt_discipline.md](./references/halt_discipline.md)
* **Linter & Validator Script**: [validate_journal.py](./scripts/validate_journal.py)
