# Security Bug Bounty & Red Teaming Workflow

## Purpose

Structured work mode for professional bug bounty researchers, red teamers, and cybersecurity analysts who produce **pay-verified findings, signed contracts, and high-accuracy reports** while working in sandboxed and live environments. Speed and accuracy are both mandatory.

---

## Pre-Flight Gate

Before any analysis begins, the agent MUST complete these five steps and present a short status summary:

1. **Confirm Scope** — Read target, authorization, and rules of engagement. Verify authorization artifact (contract, scope doc, bug bounty letter, signed IP assignment) is present or being generated.
2. **Confirm Environment** — Identify whether the target is sandboxed, isolated, or live. If live/critical infrastructure, halt and escalate before analysis begins. The agent MUST NOT analyze or test live payment/mfa/credential systems without a signed authorization scope.
3. **Confirm Attack Surface** — Inventory endpoints, APIs, binaries, packages, or network surfaces per the scope. Map assets to MITRE ATT&CK IDs for the report.
4. **Confirm Evidence Plan** — Define what artifacts will be captured (logs, pcap, memory images, hashes, timestamps) and where they will be stored. Refer to the Evidence Preservation rule.
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
| `LOW` | Analysis failed or no reproduction; insufficient evidence | Reject; do not sign anything |

**The agent MUST stop if confidence is not HIGH.** It must expand context, gather more evidence, or ask the user for clarification before signing or finalizing any legal/contractual document.

---

## Speed vs. Accuracy Trade-off

| Mode | When to Use | Rules |
|---|---|---|
| **FAST** | Voluminous but low-risk recon, vulnerability taxonomy, doc drafting | No live exploitation; no signature generation |
| **ACCURATE** | Vulnerability reproduction, exploit verification, contract prep, sandbox validation | Required: evidence capture, sandbox isolation, confidence HIGH gate |

**Default to ACCURATE** for any task involving paid contracts, vulnerability claims, or signing artifacts. Use FAST only for low-risk recon.

---

## Failure Handling

When a single message causes analysis to fail or lose progress:

1. **Identify the trigger** — What input/operation caused the failure?
2. **Preserve where possible** — Keep the failing message, context, and partial output for audit.
3. **Rebuild from checkpoint** — Resume from the last successful gate, never from corrupted state.
4. **Reproduce in isolation** — Run the failing operation in a minimum test case to confirm the failure is deterministic, not a context-coupling bug.
5. **Report transparently** — Document the failure, its cause, and the fix.

---

## Rules for the Analyst

1. **Never touch production without authorization** — scope defines the boundary
2. **Verify before you sign** — confidence HIGH required for any legal/contractual document
3. **Preserve everything** — files, logs, payloads, transcripts
4. **Checkpoint regularly** — save progress in segmented files
5. **Reproduce failures** — expand to minimum test case before assuming flakiness
6. **Map to ATT&CK** — standardize vulnerability reports
7. **Prioritize by impact** — initial access vector > privilege escalation > exfiltration
8. **Save everything it analyses** — never delete or hide data

---

## Output Template

For every high-stakes engagement, produce:
1. **Pre-Flight Summary** — scope, environment, attack surface, evidence plan, confidence baseline
2. **Evidence Bundle** — raw capture + SHA-256, timestamps, commands, outputs
3. **Findings** — MITRE ATT&CK mapped, confidence score, reproduction steps
4. **Verification Record** — when confidence was HIGH, what was reproduced, by whom, with what timestamp
5. **Signed Deliverable** — final report with audit trail (author, date, scope, evidence digest, confidence)
