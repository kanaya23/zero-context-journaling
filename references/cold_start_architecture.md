# Cold-Start State Transfer Architecture

## 1. The Core Dilemma: LLM Context Volatility

Large Language Model (LLM) agents do not have persistent memory across independent sessions. Even within a long-running single session, contemporary agentic harnesses apply strategies such as:
1. **Context Compaction / Summarization**: Squeezing earlier turns into lossy semantic summaries.
2. **Context Window Truncation**: Dropping older conversation turns once token limits are reached.
3. **Subagent Delegation**: Launching specialized worker agents that start with completely isolated, clean context windows.
4. **Session Restarts / Crashes**: Tool crashes, IDE restarts, or user disconnects that wipe all in-memory conversational history.

In every one of these scenarios, the agent experiences **Total Ambient Amnesia**.

---

## 2. The High Cost of Speculative Re-Exploration

When an agent restarts without a structured persistent journal, it predictably exhibits the following degenerate behaviors:
* **Directory Wandering**: Calling `list_directory`, `find_files`, or `grep` across hundreds of files trying to figure out what was being worked on.
* **Redundant Tests & Builds**: Re-running builds, re-installing dependencies, or re-verifying code that was already proven working.
* **Scope Drift & Hallucination**: Assuming certain modules were not completed and re-writing working code from scratch, causing regression bugs.
* **Token Budget Exhaustion**: Burning 20,000 to 50,000 prompt tokens simply re-reading source code that was previously analyzed.
* **Deferred Journaling Failure**: Waiting until the end of the session to write notes—which are lost entirely if the session aborts or truncates early.

---

## 3. The Architecture: Externalized Ground Truth & Continuous Persistence

Instead of relying on volatile LLM context or memory embeddings, Zero-Context State Persistence externalizes ground-truth state directly onto the file system in a human- and machine-readable journal (`journal.md`).

```
┌────────────────────────────────────────────────────────┐
│               ENTER PROJECT / COLD-START               │
│  - Inspect project root for journal.md                 │
│  - Mandatory Journal Summary Reading (Section 4 & 2)   │
│  - Take "Immediate Next Action" on first tool call     │
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
└────────────────────────────────────────────────────────┘
```

---

## 4. Cold-Start Ingestion Algorithm

When an agent wakes up or boots in an existing repository, it must execute the following deterministic boot sequence:

1. **Project-Local Discovery**:
   - Inspect the local directory where active changes occur for `journal.md` (or `JOURNAL.md`).
   - If not found, initialize a fresh `journal.md` adhering strictly to the standardized 4-part schema.

2. **Mandatory Journal Summary Reading**:
   - On every session start, cold start, or entry into a project directory, read `journal.md` (specifically the **Summary** section) before taking action.
   - Parse Section 4 (`Summary: MUST — Non-Optional, Always Updated Rolling Ground Truth`).
   - Parse Section 2 (`Pending (Ongoing / Unfinished)`).
   - Identify:
     - Verified baseline facts (ports, processes, verified tests, memory offsets).
     - The active task and its sequential sub-objectives.
     - The `Immediate Next Action`.

3. **Resumption without Re-Exploration**:
   - Do NOT run broad directory searches or re-read irrelevant files.
   - Take the specified `Immediate Next Action` as the very first tool call of the session.

4. **Continuous Persistence Invariant (Axiom 0)**:
   - As each micro-step completes, immediately record it in Section 1 of `journal.md`.
   - Never defer journaling to the end of the session.

This reduces cold-start bootstrap latency from minutes down to seconds, eliminating token waste and preventing regressions.
