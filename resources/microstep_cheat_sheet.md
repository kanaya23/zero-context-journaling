# Micro-Step Precision Cheat Sheet

## The Philosophy of a Micro-Step

A **micro-step** is the smallest indivisible unit of engineering progress that yields a verified state transition.

In traditional human changelogs, entries like "fixed login bug" or "updated CSS" are common. For AI coding agents, such entries are **information black holes**. When a subsequent agent boots up with zero ambient memory, it must know:
1. Exactly which file and line/function was altered.
2. What input or command triggered the verification.
3. What concrete outcome or artifact was produced.

---

## The 4 Micro-Step Anatomy Rules

Every completed micro-step item (`- [x]`) must follow this formula:

$$\text{Micro-Step} = \text{[Action Verb]} + \text{[Concrete Target / File]} + \text{[Technical Change]} + \text{[Verified Outcome]}$$

### Examples by Domain

#### 1. Software Engineering & Web Development
* **Bad**: `- [x] Fixed user registration validation.`
* **Good**: `- [x] Fix Registration Schema Validation: In 'src/schemas/user.ts' (lines 28-35), added email regex enforcement; ran 'npm test tests/unit/user.test.ts' and verified 12/12 passing assertions.`

#### 2. Systems Programming & Reverse Engineering
* **Bad**: `- [x] Found the health check function.`
* **Good**: `- [x] Locate Entity Health VTable: Scanned .text section of 'GameAssembly.dll' for signature '48 8B 05 ?? ?? ?? ?? 48 85 C0 74 08'; identified 'PlayerEntity::TakeDamage' at offset '0x1404A8120'; verified RIP breakpoint hit in x64dbg with RCX holding valid entity pointer.`

#### 3. DevOps & Infrastructure
* **Bad**: `- [x] Setup Docker containers.`
* **Good**: `- [x] Provision Container Topology: Authored 'docker-compose.yml' configuring PostgreSQL 16 on port 5432 and Redis 7 on port 6379; executed 'docker compose up -d' and confirmed health status via 'docker compose ps' showing (healthy).`

#### 4. Bug Fixing & Regression Resolution
* **Bad**: `- [x] Solved null pointer exception.`
* **Good**: `- [x] Guard Against Null Session Token: In 'src/api/auth.go:114', wrapped 'claims.UserID' retrieval in 'if session == nil' guard returning HTTP 401; confirmed fix with 'curl -i http://localhost:8080/protected' returning '401 Unauthorized' instead of panicking.`

---

## Common Sins to Eliminate

1. **The Ghost Edit**: Mentioning that a feature was added without providing the relative file path.
2. **The Unverified Claim**: Marking a task complete without mentioning the test command, curl output, or compiler check that verified it.
3. **The Multi-Task Bundle**: Packing 4 separate file refactors into 1 bullet point. Split them into individual `- [x]` micro-steps.
4. **Vague Quantifiers**: Writing "made performance faster" instead of "reduced query latency from 320ms to 18ms by indexing 'tenant_id'".
