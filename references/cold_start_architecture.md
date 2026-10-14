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

---

## 3. The Solution: Externalized Ground Truth

Instead of relying on volatile LLM context or memory embeddings, Zero-Context State Persistence externalizes ground-truth state directly onto the file system in a human- and machine-readable journal (`JOURNAL.md`).

```
┌────────────────────────────────────────┐
│             Session N                  │
│  - Completes micro-steps               │
│  - Verifies assertions                 │
│  - Encounters Pause/Exit trigger       │
└───────────────────┬────────────────────┘
                    │
                    ▼ (Writes Atomic Ground Truth)
      ┌───────────────────────────┐
      │        JOURNAL.md         │
      │  1. Completed Micro-steps │
      │  2. Pending Objectives    │
      │  3. Milestones            │
      │  4. Rolling Summary       │
      └─────────────┬─────────────┘
                    │
                    ▼ (Cold-Start Bootstrap)
┌────────────────────────────────────────┐
│            Session N+1                 │
│  - Reads Section 4 & Section 2         │
│  - Bypasses all exploratory scanning   │
│  - Executes "Immediate Next Action"    │
└────────────────────────────────────────┘
```

---

## 4. Cold-Start Ingestion Algorithm

When an agent wakes up or boots in an existing repository, it must execute the following deterministic boot sequence:

1. **Existence Check**:
   - Check if `JOURNAL.md` or `.agents/state.md` exists.
   - If not found, check version control status and initialize Section 1.

2. **Ground-Truth Reading**:
   - Parse Section 4 (`Summary: Rolling Ground Truth`).
   - Parse Section 2 (`Pending (Ongoing / Unfinished)`).
   - Identify:
     - Verified baseline facts (ports, processes, verified tests).
     - The active task and its sub-objectives.
     - The `Immediate Next Action`.

3. **Resumption without Re-Exploration**:
   - Do NOT run broad directory searches or re-read irrelevant files.
   - Take the specified `Immediate Next Action` as the very first tool call of the session.

This reduces cold-start bootstrap latency from minutes down to seconds, saving up to 90% of initialization tokens.
