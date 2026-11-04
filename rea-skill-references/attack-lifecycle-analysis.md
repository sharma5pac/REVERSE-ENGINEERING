# Attack Lifecycle Analysis Rule

## Purpose

This rule guides security teams in understanding the **complete technical lifecycle** an attacker takes when targeting an asset. The goal is defensive: map the full attack chain so defenses can be built at every stage.

## When to Apply

Apply this rule when:
- Analyzing a real or simulated attack against an asset
- Building detection rules, hardening guides, or incident response playbooks
- Reverse engineering malware, exploit kits, or attack infrastructure
- Reviewing a client's security posture from an attacker's perspective

## The 7-Stage Attack Lifecycle

### Stage 1: Reconnaissance
**What the attacker does:** Gathers information about the target before touching it.

- Passive recon: DNS records, WHOIS, certificate transparency logs, GitHub repos, job postings, employee LinkedIn, Shodan/Censys scans
- Active recon: port scanning, service fingerprinting, web crawling, technology stack detection
- **Defensive action:** Minimize public footprint; monitor certificate transparency; rate-limit scanning; deploy honeypots

### Stage 2: Initial Access
**What the attacker does:** Gains a foothold on the target environment.

- Phishing (spear-phishing, credential harvesting)
- Exploiting public-facing applications (web apps, VPNs, email servers)
- Supply chain compromise (third-party dependencies, vendor access)
- Valid account abuse (stolen credentials, brute force)
- **Defensive action:** MFA everywhere, patch management, WAF, email filtering, least-privilege access, vendor security reviews

### Stage 3: Execution
**What the attacker does:** Runs malicious code on the compromised system.

- PowerShell/cmd execution, script-based payloads
- Living-off-the-land binaries (LOLBins: certutil, mshta, regsvr32)
- In-memory execution to avoid disk-based detection
- **Defensive action:** Application control (AppLocker/WDAC), script block logging, AMSI, EDR behavioral detection

### Stage 4: Persistence
**What the attacker does:** Establishes mechanisms to maintain access across reboots.

- Registry Run keys, scheduled tasks, services
- WMI event subscriptions
- Bootkits/rootkits, DLL hijacking
- Account creation, credential manipulation
- **Defensive action:** Monitor persistence locations (Sysmon, Wazuh, Sigma rules), baseline startup items, regular integrity checks

### Stage 5: Privilege Escalation
**What the attacker does:** Elevates from user to admin/system/root.

- Kernel exploits, unpatched vulnerabilities
- Misconfigured services (weak permissions, unquoted paths)
- Token impersonation, UAC bypass
- Credential dumping (LSASS, SAM, Kerberoasting)
- **Defensive action:** Patch management, privilege separation, credential guard, LAPS, tiered admin model

### Stage 6: Lateral Movement
**What the attacker does:** Spreads to other systems in the network.

- Pass-the-Hash, Pass-the-Ticket
- Remote Desktop, PsExec, WMI, WinRM
- SMB shares, database connections
- **Defensive action:** Network segmentation, SMB signing, Kerberos hardening, EDR network containment, honeypots

### Stage 7: Impact / Exfiltration
**What the attacker does:** Achieves the objective — data theft, ransomware, destruction.

- Data staging and compression
- Exfiltration via DNS, HTTPS, cloud storage
- Ransomware encryption, wiper malware
- **Defensive action:** DLP, egress monitoring, backup strategy (3-2-1), immutable backups, incident response plan

## Analysis Methodology

When analyzing an attack lifecycle for a client:

1. **Map the kill chain** — document each stage with evidence (logs, artifacts, memory dumps, network captures)
2. **Identify the initial vector** — how did the attacker first get in? This is the most critical finding.
3. **Trace the movement** — follow the attacker's path through the environment
4. **Identify detection gaps** — where was the attacker *not* detected? These are your blind spots.
5. **Map to MITRE ATT&CK** — tag each technique with its ATT&CK ID for standardized reporting
6. **Prioritize remediation** — fix the highest-impact gaps first (usually initial access + persistence)

## MITRE ATT&CK Mapping Template

| Stage | Technique | ATT&CK ID | Evidence Source | Detection Gap |
|---|---|---|---|---|
| Recon | Active scanning | T1595 | Firewall logs | None |
| Initial Access | Phishing | T1566 | Email gateway | Credential theft undetected |
| Execution | PowerShell | T1059.001 | Sysmon EID 4688 | No script block logging |
| Persistence | Registry Run Key | T1547.001 | Autoruns | No baseline |
| Priv Esc | Token Impersonation | T1134 | EDR | Not monitored |
| Lateral | Pass-the-Hash | T1550.002 | 4624 Type 3 | No SMB signing |
| Exfiltration | DNS tunneling | T1048.001 | DNS logs | No DLP |

## Defensive Recommendations Template

For each stage, provide:
- **Detection**: What logs/alerts would catch this?
- **Prevention**: What controls stop it?
- **Response**: What's the IR playbook step?
- **Hardening**: What configuration change closes the gap?

## Rules for the Analyst

1. **Never execute real malware** on production systems — use sandboxes
2. **Document everything** — every finding needs a source (log entry, hash, timestamp)
3. **Think like the attacker** — but act like the defender
4. **Map to ATT&CK** — standardize findings for client reporting
5. **Prioritize by impact** — initial access vector > lateral movement > persistence
6. **Test your detections** — atomic red team or purple team exercises
7. **Assume breach** — design defenses assuming the attacker is already inside

## Output Format

When delivering an attack lifecycle analysis to a client, produce:
1. **Executive Summary** — 1-page, non-technical, business impact focus
2. **Attack Timeline** — chronological kill chain with evidence
3. **MITRE ATT&CK Mapping** — technique-to-evidence table
4. **Detection Gaps** — prioritized list of blind spots
5. **Remediation Roadmap** — phased fixes (immediate, 30-day, 90-day)
6. **Detection Rules** — Sigma/YARA/Suricata rules for the observed TTPs

## Rule 8: Evidence Preservation (Merge with Rule 2)

\> "Save everything it analyses. Never delete or hide data — merge this with the documentation rule."

### Purpose

Complete technical analysis is worthless if evidence is lost, truncated, or sanitized after collection. Every finding, artifact, log entry, memory dump, network capture, hash, and timestamp must be preserved in full for the entire lifecycle of the investigation — from initial detection through remediation and any future re-analysis.

### When to Apply

Apply this rule alongside Rule 2 (Document Everything) for every phase of an attack lifecycle analysis:
- During initial reconnaissance and mapping
- While capturing external telemetry (network captures, DNS logs, firewall logs, auth logs)
- While collecting forensic artifacts (memory, disk, process trees, open sockets, loaded modules)
- While extracting and analyzing code, binaries, payloads, and configurations
- While writing reports and delivering findings to clients

### Preservation Standards

1. **Full fidelity capture**
   - Record raw source, not sanitized excerpts. Never strip context that could change the meaning of a finding.
   - For network captures (pcap, DNS, HTTP, TLS): retain original binary format. Do not re-extract to text-only summaries without keeping the original alongside the analysis.
   - For memory/disk evidence: capture forensic images (not just text representations) with checksums.

2. **No truncation of findings**
   - Do not abbreviate or elide technical detail in your working notes, intermediate reports, or final outputs. If a finding is long, append it rather than replacing it.
   - Keep the full endpoint, attack chain, and tool chain visible at all times.

3. **No data hiding**
   - Do not redact, anonymize, or suppress evidence in the primary analysis. If a client receives a cleaned-up/abridged version, the full original must also be delivered.
   - Never omit a step in the kill chain because it is uncomfortable or embarrassing — document it.

4. **Immutable, backed-up storage**
   - Store all evidence in write-once-read-many (WORM) or append-only storage where available.
   - Maintain at least 3 copies across at least 2 media types (local + cloud backup).
   - Compute and record SHA-256 hashes for every primary artifact (files, pcap, memory dump, disk image, script output, interaction transcript).

5. **Indexing, not deleting**
   - Use metadata tags, indexing, and file naming conventions to organize findings — never by deleting or moving them out of analysis scope.
   - Archive older findings separately, but preserve them with their original identifiers and cross-references.

6. **Versioning and provenance**
   - Record the analysis tool version, the exact command/operation used, the date/time, and the analyst who performed it for every finding.
   - Preserve intermediate files and scratch artifacts even if they were superseded — they may be needed for audit or re-analysis.

## Rules for the Analyst

1. **Never execute real malware** on production systems — use sandboxes
2. **Document everything** — every finding needs a source (log entry, hash, timestamp)
3. **Think like the attacker** — but act like the defender
4. **Map to ATT&CK** — standardize findings for client reporting
5. **Prioritize by impact** — initial access vector > lateral movement > persistence
6. **Test your detections** — atomic red team or purple team exercises
7. **Assume breach** — design defenses assuming the attacker is already inside
8. **Save everything it analyses** — never delete or hide data; merge evidence with every other record
