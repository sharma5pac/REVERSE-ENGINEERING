# Development, Testing & Quality Gate Workflow

## Purpose

Structured work mode for professional software engineering and security analysis. Enforces a firm, complete development-and-test loop. Every change must pass through this gate before being committed, shipped, or signed.

## Core Principle

**Speed comes from confidence. Confidence comes from verification. Verification is never optional.**

## Pre-Development Gate

Before writing any code:
1. **Confirm Scope** — Read target, authorization, and rules of engagement. Verify authorization artifact is present or being generated.
2. **Confirm Environment** — Identify whether target is sandboxed, isolated, or live. If live/critical infrastructure, halt and escalate.
3. **Confirm Attack Surface** — Inventory endpoints, APIs, binaries, packages, or network surfaces. Map assets to MITRE ATT&CK IDs.
4. **Confirm Evidence Plan** — Define what artifacts will be captured and where they will be stored.
5. **Confirm Confidence Baseline** — A `READY`/`BLOCKED` status is shown before proceeding. No analysis starts until scope is confirmed.

## Sandbox-First Execution

1. **Sandbox first** — Isolate all test payloads. Use containers, VMs, or isolated cloud tenants. Never run exploit payloads against production systems.
2. **Controlled testing** — Consult the authorization scope. Test only within permitted endpoints, versions, and parameters.
3. **Trace all artifacts** — For every finding, capture: command run, input supplied, output returned, timestamp, SHA-256 of files processed, and environment description.
4. **Then analyze** — Perform the actual analysis with full context preserved.

## Confidence Gate

Before writing any signed report or document:

| Gate | Condition | Action |
|---|---|---|
| `HIGH` | Finding reproduced, evidence captured, exploit/reproduction steps documented | Proceed to sign / finalize |
| `MEDIUM` | Finding reproduced but reproduction steps incomplete or environment unclear | Flag as MEDIUM; do not sign as verified |
| `LOW` | Single message triggered failure; no reproduction or evidence | Reject; do not sign anything |

**The agent MUST stop if confidence is not HIGH.**

## Development Workflow

1. **Implement** — Write the code, fix, or finding. Keep changes small and atomic.
2. **Self-review** — Read every changed file. Does it compile? Does it test? Does it follow architecture boundaries?
3. **Run tests** — Execute the full relevant test suite. Every test must pass.
4. **Manual verification** — Reproduce the issue or confirm the feature end-to-end in a live environment (sandboxed where applicable).
5. **Documentation** — Update or write any affected docs, READMEs, or contract artifacts.
6. **Checkpoint** — Save progress in a segmented file. Never rely on a single uncommitted save.

## Testing Requirements

### Unit & Integration Tests
- Every new function, class, or module must have a corresponding unit or integration test.
- Tests must cover the happy path, the error path, and edge cases.
- Test fixtures must be owned by the project.

### Test Discovery
- Run the project's test discovery verification command.

### Linting & Typechecking
- Run the project's lint command.
- Run type-checking.
- Verify the build compiles.

### Security & Code Quality
- Run static analysis: architecture guards, dependency checks, scan for TODOs/unlicensed code.

## Testing Priorities

| Priority | What to Test | Why |
|---|---|---|
| 1 | Initial access vector | Can't secure what you don't understand |
| 2 | Privilege escalation path | Highest impact after initial access |
| 3 | Exfiltration path | Data theft is the most critical outcome |
| 4 | Persistence mechanism | Determines how long an attacker stays undetected |
| 5 | All other TTPs | Secondary but still relevant |

## Rules for the Analyst

1. **Never execute real malware** on production systems — use sandboxes
2. **Never touch production without authorization** — scope defines the boundary
3. **Never delete or hide data** — save everything; merge evidence with every other record
4. **Verify before you sign** — confidence HIGH required for any legal/contractual document
5. **Checkpoint regularly** — save progress in segmented files
6. **Reproduce failures** — expand to a minimum test case before assuming flakiness
7. **Map to ATT&CK** — standardize vulnerability reports
8. **Prioritize by impact** — initial access vector > privilege escalation > exfiltration
9. **Assume breach** — design defenses assuming the attacker is already inside
10. **Preserve everything** — files, logs, payloads, transcripts. Never delete evidence to hide a failure.

## Failure Handling

When a single message causes analysis to fail or lose progress:

1. **Identify the trigger** — What input/operation caused the failure?
2. **Preserve where possible** — Keep the failing message, context, and partial output for audit.
3. **Rebuild from checkpoint** — Resume from the last successful gate, never from corrupted state.
4. **Reproduce in isolation** — Run the failing operation in a minimum test case to confirm the failure is deterministic, not a context-coupling bug.
5. **Report transparently** — Document the failure, its cause, and the fix.

## Output Template

1. **Pre-Flight Summary** — scope, environment, attack surface, evidence plan, confidence baseline
2. **Evidence Bundle** — raw capture + SHA-256, timestamps, commands, outputs
3. **Findings** — MITRE ATT&CK mapped, confidence score, reproduction steps
4. **Verification Record** — when confidence was HIGH, what was reproduced, by whom, with what timestamp
5. **Signed Deliverable** — final report with audit trail (author, date, scope, evidence digest, confidence)
