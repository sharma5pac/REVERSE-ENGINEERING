# Development, Testing & Quality Gate Rule

## Purpose

A structured work mode for professional software engineering and security analysis that enforces a firm, complete development-and-test loop. Every change — whether a new feature, a vulnerability finding, a bug fix, or a signed deliverable — must pass through this gate before being committed, shipped, or signed.

## Core Principle

**Speed comes from confidence. Confidence comes from verification. Verification is never optional.**

A single message that causes failure mid-contract is a failure, not a speed gain. The agent MUST stop and report rather than guess or proceed from partial context.

---

## Pre-Development Gate

Before writing any code, the agent MUST complete these steps:

1. **Confirm Scope** — Read the target, authorization, and rules of engagement. Verify the authorization artifact (contract, scope doc, bug bounty letter, signed IP assignment) is present or being generated.
2. **Confirm Environment** — Identify whether the target is sandboxed, isolated, or live. If live/critical infrastructure, halt and escalate before analysis begins.
3. **Confirm Attack Surface** — Inventory endpoints, APIs, binaries, packages, or network surfaces per the scope. Map assets to MITRE ATT&CK IDs for the report.
4. **Confirm Evidence Plan** — Define what artifacts will be captured (logs, pcap, memory images, hashes, timestamps) and where they will be stored.
5. **Confirm Confidence Baseline** — A `READY`/`BLOCKED` status is shown before the agent proceeds. No analysis starts until scope is confirmed.

---

## Sandbox-First Execution

When performing vulnerability analysis or testing, the agent MUST follow this priority:

1. **Sandbox first** — Isolate all test payloads and systems. Use containers, VMs, or isolated cloud tenants. Never run exploit payloads against production systems or third-party infrastructure.
2. **Controlled testing** — If the domain is a live/public service, consult the authorization scope. Test only within permitted endpoints, versions, and parameters.
3. **Trace all artifacts** — For every finding, capture: command run, input supplied, output returned, timestamp, SHA-256 of files processed, and environment description.
4. **Then analyze** — Perform the actual vulnerability/metamorphic analysis with full context preserved.

## Confidence Gate

Once analysis is complete, the agent MUST apply a confidence gate before writing any signed report or document:

| Gate | Condition | Action |
|---|---|---|
| `HIGH` | Finding reproduced, evidence captured, exploit/reproduction steps documented | Proceed to sign / finalize |
| `MEDIUM` | Finding reproduced but reproduction steps incomplete or environment unclear | Flag as MEDIUM in report; do not sign as verified |
| `LOW` | Single message triggered failure; no reproduction or evidence | Reject; do not sign anything |

**The agent MUST stop if confidence is not HIGH.** It must expand context, gather more evidence, or ask the user for clarification before signing or finalizing any legal/contractual document.

---

## Development Workflow

1. **Implement** — Write the code, fix, or finding. Keep changes small and atomic.
2. **Self-review** — Read every changed file. Does it compile? Does it test? Does it follow the project's architecture boundaries?
3. **Run tests** — Execute the full relevant test suite. Every test must pass.
4. **Manual verification** — Reproduce the issue or confirm the feature end-to-end in a live environment (sandboxed where applicable).
5. **Documentation** — Update or write any affected docs, READMEs, or contract artifacts.
6. **Checkpoint** — Save progress in a segmented file. Never rely on a single uncommitted save.

---

## Testing Requirements

### Unit & Integration Tests
- Every new function, class, or module must have a corresponding unit or integration test.
- Tests must cover the happy path, the error path, and edge cases.
- Test fixtures must be owned by the project (owned-cache principle).

### Test Discovery
- Run `npm run verify:test-discovery` (or the equivalent in the project) to confirm the test runner can discover all tests.

### Linting & Typechecking
- Run the project's lint command (`npm run lint` / equivalent).
- Run type-checking (`npm run typecheck` / equivalent).
- Verify the build compiles (`npm run build` / equivalent).

### Security & Code Quality
- Run the project's static analysis: `npm run verify:architecture-guards` (or equivalent).
- Run dependency checks: `npm run deps:check` (or equivalent).
- Scan for TODOs and unlicensed code: `npm run scan:todos` (or equivalent).

---

## Testing Priorities

| Priority | What to Test | Why |
|---|---|---|---|
| 1 | Initial access vector | Can't secure what you don't understand |
| 2 | Privilege escalation path | Highest impact after initial access |
| 3 | Exfiltration path | Data theft is the most critical outcome |
| 4 | Persistence mechanism | Determines how long an attacker stays undetected |
| 5 | All other TTPs | Secondary but still relevant |

---

## Rules for the Analyst

1. **Never execute real malware** on production systems — use sandboxes (containers, VMs, isolated cloud tenants)
2. **Never touch production without authorization** — scope defines the boundary
3. **Never delete or hide data** — save everything; merge evidence with every other record (Rule 8)
4. **Verify before you sign** — confidence HIGH required for any legal/contractual document
5. **Checkpoint regularly** — save progress in segmented files; never from corrupted state
6. **Reproduce failures** — expand to a minimum test case before assuming flakiness
7. **Map to ATT&CK** — standardize vulnerability reports
8. **Prioritize by impact** — initial access vector > privilege escalation > exfiltration
9. **Assume breach** — design defenses assuming the attacker is already inside
10. **Preserve everything** — files, logs, payloads, transcripts. Never delete evidence to hide a failure.

---

## Failure Handling

When a single message causes analysis to fail or lose progress:

1. **Identify the trigger** — What input/operation caused the failure?
2. **Preserve where possible** — Keep the failing message, context, and partial output for audit.
3. **Rebuild from checkpoint** — Resume from the last successful gate, never from corrupted state.
4. **Reproduce in isolation** — Run the failing operation in a minimum test case to confirm the failure is deterministic, not a context-coupling bug.
5. **Report transparently** — Document the failure, its cause, and the fix. Never silently drop evidence to hide the issue.

---

## Output Template

For every high-stakes engagement, produce:

1. **Pre-Flight Summary** — scope, environment, attack surface, evidence plan, confidence baseline
2. **Evidence Bundle** — raw capture + SHA-256, timestamps, commands, outputs
3. **Findings** — MITRE ATT&CK mapped, confidence score, reproduction steps
4. **Verification Record** — when confidence was HIGH, what was reproduced, by whom, with what timestamp
5. **Signed Deliverable** — final report with audit trail (author, date, scope, evidence digest, confidence)
