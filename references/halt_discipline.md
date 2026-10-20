# Immediate Halt Discipline: Halting Runaway Agent Loops

## 1. The "One More Thing" Syndrome in AI Agents

A well-documented failure mode in autonomous AI agents is the inability to cleanly stop when commanded. When a user sends prompts such as:
- *"Pause here, let's continue tomorrow."*
- *"Dump your findings and exit."*
- *"Stop and log your progress."*
- *"That's all for now."*

Untrained agents frequently succumb to the **"One More Thing" Loop**:
1. The agent notices an unresolved linter warning or curiosity in a file.
2. It decides to call `run_command("npm test")` or `view_file` "just to be sure".
3. The test reveals another minor warning.
4. The agent attempts to fix that warning, triggering another cascade of tool calls.
5. Five minutes and \$1.50 in API tokens later, the agent is still running tool calls instead of stopping.

---

## 2. The Strict Halt Protocol

When the user gives any termination or pause directive, the agent must immediately switch to **Execution Discipline: Immediate Halt on Exit / Stop**.

Because the agent follows **Axiom 0 (The Continuous Journaling Invariant)**, all completed micro-steps are already persisted in Section 1. The halt routine executes cleanly and atomically without speculative exploration.

```
User says "Pause / Stop / Dump findings / Exit"
                 │
                 ▼
       [STOP ALL TOOL CALLS]
                 │
                 ├── 1. Disallow any new file reads, directory scans, or shell searches
                 ├── 2. Disallow speculative fixes or refactoring
                 │
                 ▼
       [EXECUTE ATOMIC SAVE]
                 │
                 ├── Step A: Freeze Section 4 (Rolling Ground Truth + Next Resumption Action)
                 ├── Step B: Stage and commit all active work to Git safety net
                 ├── Step C: Free volatile resources (detach debuggers, kill child procs)
                 │
                 ▼
       [CLEAN TURN CONCLUSION]
                 │
                 └── Output crisp summary and state resume instructions
```

---

## 3. Concrete Checklist for Immediate Halt

Before yielding the turn to the user upon a halt command, the agent must execute these actions and **nothing else**:

- [ ] **Zero Speculative Tools**: Ensure no search, linter, or exploratory commands are queued.
- [ ] **Update & Freeze `journal.md`**:
  - Verify recently finished actions are recorded as `- [x]` or `1. [x]` micro-steps in Section 1.
  - Set accurate progress percentages and sequential objectives in Section 2.
  - Refresh Section 4 with:
    - Active branch / commit hash.
    - Active background tasks or bound ports.
    - Exact resumption command.
- [ ] **Git Safety Net Commit**:
  - Run `git status`.
  - Stage changes (`git add -A`).
  - Commit with descriptive message (`git commit -m "checkpoint: save progress before pause"`).
  - Push to remote if configured (`git push`).
- [ ] **Volatile Resource Teardown**:
  - Kill daemon processes started during the session that shouldn't persist indefinitely.
  - Release hardware/serial locks, virtual screen instances, or debug attachments.
- [ ] **Concise Output**: Report state concisely without generating multi-page prose.
