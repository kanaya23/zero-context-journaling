---
name: zero-context-journaling
description: >-
  Universal zero-context state persistence and micro-step journaling for AI coding agents.
  Enforces deterministic cold-start state transfer across session wipes, immediate halt discipline
  on pause/exit, and a standardized 4-part state tracker (Completed Micro-Steps, Pending Objectives,
  Milestones, and Rolling Ground-Truth Summary).
---

# Universal Zero-Context State Persistence & Micro-Step Journaling

AI coding agents operate in volatile runtime environments where context windows truncate, tokens compact, and sessions terminate abruptly. When an agent restarts, it suffers from total ambient amnesia.

This skill equips the agent with **Zero-Context State Persistence**: a rigorous operational protocol and standardized journaling schema that ensures any subsequent cold-start agent or session can resume execution instantly with zero hallucination, zero speculative re-exploration, and zero wasted tokens.

---

## 1. Core Architectural Axioms

### Axiom 1: The Cold-Start Principle (Assume Total Amnesia)
* Treat every session boundary, context truncation, compact event, or restart as an **instantaneous memory wipe**.
* The next session or subagent will have **zero ambient memory** of previous chat messages, unspoken assumptions, or intermediate tool outputs.
* The persistent journal file (`JOURNAL.md` or workspace state tracker) is the **single source of ground truth**.
* Maintain a strictly **neutral, analytical, and professional** tone. Never adopt conversational personas, roleplay quirks, or conversational fluff that wastes token budget.

### Axiom 2: Immediate Halt Discipline (No "One More Thing")
* When the user issues an instruction to **pause, stop, log progress, dump findings, exit, or conclude**:
  1. **HALT IMMEDIATELY**.
  2. Do **NOT** invoke investigative tools (no speculative directory scans, no extra `read_file` calls, no git status exploration).
  3. Do **NOT** enter a "one more thing" loop to fix a newly discovered issue.
  4. Immediately write/update the journal file.
  5. Commit and push modified files to the active version control safety net.
  6. Clean up volatile resources (kill background processes, detach debuggers, free ports).
  7. Conclude the turn cleanly and concisely.

### Axiom 3: Project-Local Placement & Bootstrap Discovery
* **Location Invariant (Colocate with Changes)**:
  - The journal (`journal.md` / `JOURNAL.md`) **MUST** always be created and maintained directly inside the root directory where active changes are taking place (e.g., `project1/journal.md`), **regardless** of where the agent's current working directory (`CWD`) or shell happens to be (e.g., even if executing from `~/system1/`).
  - Never place project-specific journals in global user directories, home directories, or temporary scratch folders unless the project itself resides there.
* **Bootstrap Discovery (Read vs. Fresh)**:
  - Whenever entering, switching to, or starting work on a project directory:
    1. **Check for Existing Journal**: Inspect the project directory for `journal.md` (or `JOURNAL.md`).
    2. **If Found**: Read it immediately before invoking any other tools or speculative searches to bootstrap context and recover the rolling ground-truth state.
    3. **If NOT Found**: Start fresh by initializing a new `journal.md` adhering strictly to the standardized 4-part schema.

---

## 2. Standardized 4-Part State Tracker Schema

Every journal file (`JOURNAL.md`) **MUST** strictly adhere to the following four standardized sections:

```markdown
# Project State & Execution Journal

## 1. Completed Task List (Micro-Steps)
- [x] Step Name: Exact files touched, commands executed, offsets found, or bugs resolved.
- [x] Step Name: Exact verification output or test assertion confirmed.

## 2. Pending (Ongoing / Unfinished)
### [Progress %] Active Task Title
- Concrete sequential objective 1
- Concrete sequential objective 2

## 3. Milestone (User Remarks & Backlog)
- Future Goal Title: Description of user requests, planned features, and prerequisites.

## 4. Summary (Rolling Ground Truth)
- Chronological actions & proven findings
- Current ground-truth environment state
- PRECISE IMMEDIATE ACTION to take upon resume
```

### Deep Section Breakdown

#### Section 1: Completed Task List (Micro-Steps Down to Minute Detail)
Record every individual step executed so far. Avoid vague statements like "worked on auth". Every item must record tangible micro-steps:
- Format: `- [x] <Micro-Step Title>: <Exact details>`
- Must include: Specific file paths (`src/auth/jwt.ts`), line numbers or function names (`verifyToken()`), exact CLI commands run, memory addresses/offsets found, or specific error codes resolved.

#### Section 2: Pending (Ongoing / Unfinished Work)
Record all currently active, interrupted, or incomplete work.
- Must include: Explicit progress percentage (`[Progress 40%]`).
- Must include: Concrete, numbered or bulleted list of sequential objectives required to bring the task to 100% completion.
- No ambiguous TODOs without actionable next steps.

#### Section 3: Milestone (Optional — User Remarks & Future Backlog)
Captures external user feedback, long-term roadmap items, or future enhancements requested by the user that are out of scope for the current sprint.
- Include only when the user has remarked upon, requested, or planned future work.
- Document prerequisites and architectural dependencies.

#### Section 4: Summary (MUST — Non-Optional Rolling Ground Truth)
The anchor of cold-start recovery. A vivid, condensed, technical summary that answers three questions with zero ambiguity:
1. **Proven Findings**: What facts have been physically verified (e.g. "Endpoint returns 200 with JWT payload; memory offset 0x7FF... contains target vtable")?
2. **Current Environment State**: What is active right now (active process IDs, open ports, checked-out git branch, modified uncommitted files, active environment variables)?
3. **Immediate Next Action**: The exact first tool call or file modification the cold-start agent must perform the moment work resumes.

---

## 3. Execution Lifecycle: When to Update the Journal

```
[Enter Project Directory]
          │
          ├──> journal.md exists? ─── YES ──> Read journal.md ──> Resume "Immediate Next Action"
          │                                                               │
          └──> NO ──> Start fresh journal.md                      (After major micro-step)
                            │                                             │
                            ▼                                             ▼
                   Execute Micro-Step                            Update Section 1 & 2
                            │                                             │
                            └──────────────────────┬──────────────────────┘
                                                   │
                                     (User triggers Pause / Exit / Stop)
                                                   │
                                                   ▼
                                      Immediate Halt Discipline
                                                   │
                                                   ▼
                                    Write Sections 1-4 + Commit VCS
```

1. **On Session Bootstrap / Entering a Project**:
   - Locate the target project directory where changes will occur.
   - Check if `journal.md` (or `JOURNAL.md`) exists in that specific project root directory.
   - **If found**: Read Section 4 ("Summary: Immediate Next Action") and Section 2 ("Pending") to recover context instantly with zero exploratory tool overhead.
   - **If not found**: Create a fresh `journal.md` in that project directory following the standardized 4-part schema before proceeding with work.

2. **During Active Development**:
   - As tasks complete, append them directly to Section 1 as checked micro-steps (`- [x]`).
   - Keep Section 2 updated with accurate completion percentages.

3. **On Session Suspension (Halt / Exit Trigger)**:
   - Stop tool invocations instantly.
   - Refresh Section 4 with current environment state and the exact resumption command.
   - Commit changes to Git safety net.

---

## 4. Anti-Patterns vs. Best Practices

| Anti-Pattern (Fails Cold-Start) | Best Practice (Zero-Context Compliant) |
| :--- | :--- |
| "Refactored user authentication." | `- [x] Refactor Auth Middleware: Updated JWT verification in `src/middleware/auth.ts` lines 42-68 to use RS256; validated with `npm test auth.test.ts` (14 passing).` |
| "Investigate database performance." | `### [Progress 25%] Optimize SQL Queries`<br>`1. Add index on `users.tenant_id``<br>`2. Replace N+1 query in `fetchOrders()` at `src/services/order.ts:88`` |
| Running 5 more bash commands after user says "stop for today". | Halting immediately, writing `JOURNAL.md`, committing to git, and printing state summary. |
| Missing Section 4 or vague "Next: continue coding". | `Next Action: Run 'npm run db:migrate' to apply migration 004_add_tenant_index.sql, then check 'curl localhost:3000/api/health'.` |

---

## 5. Supplementary Resources

* **Drop-in Template**: [journal_template.md](./resources/journal_template.md)
* **Micro-Step Formatting Rules**: [microstep_cheat_sheet.md](./resources/microstep_cheat_sheet.md)
* **Cold-Start Architecture Reference**: [cold_start_architecture.md](./references/cold_start_architecture.md)
* **Halt Discipline Deep-Dive**: [halt_discipline.md](./references/halt_discipline.md)
* **Linter & Validator Script**: [validate_journal.py](./scripts/validate_journal.py)
