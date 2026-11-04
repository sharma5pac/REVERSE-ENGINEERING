# REVERSE-ENGINEERING

Professional reverse engineering, bug bounty, red teaming, and cybersecurity analysis toolkit.

## 📁 Repository Structure

| Directory | Contents |
|-----------|----------|
| `kala-mcp/` | MCP Server for Kali Linux tools integration with OpenCode/Cline |
| `cline-rules/` | Cline agent rules for security workflows |
| `opencode-config/` | OpenCode MCP server configuration |
| `darkgpt-analysis/` | WormGPT reverse engineering analysis (dark web AI platform) |
| `rea-skill-references/` | REA skill reference documentation |

## 🛠️ Kala MCP Server (`kala-mcp/`)

A unified MCP (Model Context Protocol) server that connects your local Kali Linux penetration testing tools to OpenCode and Cline AI agents.

### Features
- **50+ Kali tools** across 9 kill-chain categories
- **Authorization gates** — high-risk tools require explicit `KALA_HIGH_RISK_ALLOW=1`
- **Evidence preservation** — SHA-256 hashed logs saved to `~/.kala_evidence/`
- **Stdout/stdout MCP transport** — works with OpenCode, Cline, and any MCP client

### Tool Categories
- reconnaissance (nmap, subfinder, amass, theHarvester, dnsrecon, etc.)
- web_app (ffuf, gobuster, dirsearch, dirbuster, etc.)
- exploitation (msfvenom, metasploit-framework, sqlmap, set, beef-xss)
- database (sqlmap, sqlninja, oscanner, bbqsql)
- password_cracking (hashcat, john, hydra, medusa, mimikatz)
- wireless (aircrack-ng, kismet, wifite, bettercap)
- network_intercept (wireshark, tcpdump, macchanger, responder)
- forensics_reverse (volatility, ghidra, binwalk, autopsy)
- active_directory (bloodhound, crackmapexec)

### Usage
```bash
# Add to your OpenCode MCP config (~/.opencode/mcp.json):
{
  "mcpServers": {
    "kala-mcp": {
      "command": "python3",
      "args": ["/path/to/kala-mcp/kala-mcp.py"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "KALA_HIGH_RISK_ALLOW": "0"
      }
    }
  }
}

# Run the MCP server standalone:
python3 kala-mcp/kala-mcp.py
```

### Example Tool Calls
- `kala_reconnaissance_nmap` — Port scan & network mapping
- `kala_web_app_ffuf` — Web fuzzing
- `kala_password_cracking_hashcat` — GPU password cracking
- `kala_database_sqlmap` — SQL injection testing
- `kala_wireless_aircrack-ng` — WiFi security auditing
- `kala_forensics_reverse_ghidra` — Binary decompilation

## 📋 Cline Rules (`cline-rules/`)

Agent rules for professional security analysis workflows:

| Rule | Purpose |
|------|---------|
| `kali-workflow.md` | Guard-rail override for authorized Kali tool work |
| `attack-lifecycle-analysis.md` | 7-stage attack lifecycle + evidence preservation |
| `security-bug-bounty-workflow.md` | Pre-flight gate + confidence gate for bug bounty |
| `development-testing-driveway.md` | Dev/test/QA gate for software changes |

## 🔧 OpenCode Config (`opencode-config/`)

MCP server configuration for OpenCode integration. Copy `mcp.json` to `~/.opencode/mcp.json` to enable the Kali MCP server in OpenCode.

## 🕵️ DarkGPT Analysis (`darkgpt-analysis/`)

Complete reverse engineering analysis of wormgpt.co — an uncensored AI platform for cybersecurity research. Includes:

- Full rendered DOM capture
- Extracted API endpoints (`/v1/chat/completions`, `/api/web-proxy`, `/api/admin`, etc.)
- 8 AI models with per-token pricing
- Pricing tiers ($50/mo to $260 lifetime)
- Security observations (admin query param leakage, crypto payments, etc.)
- JS bundle (1.89 MB) for further analysis

## 📚 REA Skill References (`rea-skill-references/`)

Reference documentation for the REA (Reverse Engineer Anything) skill system, including skill references for Android apps, JavaScript applications, native artifacts, runtime observation, and more.

## ⚠️ Legal & Ethical Use

**Authorized use only.** These tools are for:
- Authorized penetration testing and bug bounty programs
- Defensive security research and malware analysis
- Security education and training

**Never** use against systems you do not own or have explicit written authorization to test.

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/sharma5pac/REVERSE-ENGINEERING.git
cd REVERSE-ENGINEERING

# Set up OpenCode MCP config
cp opencode-config/mcp.json ~/.opencode/mcp.json

# Run the MCP server
python3 kala-mcp/kala-mcp.py

# Start OpenCode
opencode
```

---

**Repository:** https://github.com/sharma5pac/REVERSE-ENGINEERING
