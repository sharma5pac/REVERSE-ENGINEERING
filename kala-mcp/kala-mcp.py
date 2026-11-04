#!/usr/bin/env python3
"""
Kala MCP Server — Unified Gateway for Kali Linux Penetration Testing Tools
Connects your local Kali toolchain to OpenCode / Cline AI agents.
MIT License — for authorized defense/testing only.
"""

import json
import os
import subprocess
import hashlib
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server.lowlevel import Server
from mcp.types import (
    Tool,
    TextContent,
    ListToolsRequest,
    CallToolRequestParams,
    ListToolsResult,
    CallToolResult,
)

app = Server("kala")

# ─── Authorization Config ───────────────────────────────────────────────────
HIGH_RISK_TOOLS = {
    "hashcat", "john", "medusa", "hydra", "mimikatz",
    "msfvenom", "metasploit-framework", "set", "beef-xss",
    "sqlmap", "sqlninja", "oscanner", "jsql-injection",
    "bbqsql", "aircrack-ng", "wifite", "responder",
    "bettercap", "fern-wifi-cracker", "kismet", "volatility",
    "autopsy", "bloodhound", "crackmapexec",
    "ghidra", "recon-ng", "autorecon", "legion",
}

BLOCKED_TOOLS = set()
EVIDENCE_DIR = Path.home() / ".kala_evidence"


def ensure_evidence_dir():
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    return EVIDENCE_DIR


def hash_file(file_path, blocksize=65536):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            h.update(chunk)
    return h.hexdigest()


def log_authorization(user, tool, target, authorized, reason=""):
    log = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "tool": tool,
        "target": target,
        "authorized": authorized,
        "reason": reason,
        "action": "ALLOWED" if authorized else "DENIED"
    }
    log_path = EVIDENCE_DIR / f"auth_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
    return log_path


def check_authorization(tool, target, user="default"):
    if tool in BLOCKED_TOOLS:
        return False, f"Tool {tool} is blocked"
    if tool in HIGH_RISK_TOOLS:
        reason = f"High-risk tool {tool} requires explicit authorization"
        authorized = os.environ.get("KALA_HIGH_RISK_ALLOW", "0") == "1"
        if not authorized:
            log_authorization(user, tool, target, False, reason)
        else:
            log_authorization(user, tool, target, True, "Allowed via KALA_HIGH_RISK_ALLOW=1")
        return authorized, reason
    return True, f"{tool} is authorized"


KALA_TOOLS = {
    "reconnaissance": {
        "nmap": "Port scanner & network mapper (industry standard)",
        "subfinder": "Passive subdomain discovery",
        "assetfinder": "Lightweight subdomain discovery",
        "theHarvester": "Email, subdomain, employee directory OSINT",
        "dnsrecon": "Advanced DNS checking engine",
        "dnsenum": "DNS enumeration (zone transfers, reverse lookups)",
        "massdns": "High-performance DNS stub resolver",
        "dnstracer": "Follows DNS queries to authoritative source servers",
        "dnswalk": "Debugging tool that performs zone transfers",
        "dnsmap": "Domain name sub-brute-forcing utility",
        "unicornscan": "High-speed stateless TCP/UDP packet scanner",
        "lbd": "Load Balancing Detector",
        "amass": "In-depth subdomain enumeration and network mapping",
        "autorecon": "Automated network reconnaissance tool",
        "dmitry": "Deepmagic Information Gathering tool",
        "legion": "Graphical network auditing tool",
        "zenmap": "Graphical user interface for Nmap",
    },
    "web_app": {
        "dirsearch": "Directory and file brute-forcing tool",
        "feroxbuster": "Fast, recursive content discovery tool written in Rust",
        "ffuf": "High-speed web fuzzing framework",
        "gobuster": "Directory, file, and DNS brute-forcer written in Go",
        "gospider": "Fast web spidering framework built in Go",
        "lbd": "Load Balancing Detector",
        "parsero": "Robots.txt audit tool",
        "recon-ng": "Modular web reconnaissance framework",
        "subfinder": "Modular subdomain discovery tool",
        "sublist3r": "Subdomain enumerator utilizing search engine OSINT variables",
        "uniscan-gui": "Web vulnerability scanner optimized for RFI and LFI audits",
        "urlcrazy": "Typo-squatting domain generator",
        "uro": "URL cleaner that filters duplicate parameters",
        "wfuzz": "Flexible web application fuzzer",
        "dirb": "Directory brute-forcing tool",
        "dirbuster": "Multi-threaded Java application to map directories and files",
        "finalrecon": "All-in-one web reconnaissance engine",
        "findomain": "Cross-platform asset monitoring and fast domain discovery",
    },
    "exploitation": {
        "msfvenom": "Combined framework payload generator and encoder",
        "searchsploit": "Local command-line repository for exploring Exploit-DB files",
        "set": "Social Engineer Toolkit (custom human-vector and phishing simulator)",
        "beef-xss": "Browser Exploitation Framework focusing on client-side vectors",
        "metasploit-framework": "Modular framework to develop, test, and execute exploit payloads",
    },
    "database": {
        "sqlmap": "Automated tool designed to detect and exploit SQL injection vulnerabilities",
        "jsql-injection": "Lightweight Java application used to test database injection",
        "bbqsql": "Blind SQL injection framework optimized for complex network behavior",
        "oscanner": "Oracle database vulnerability assessment tool",
        "sqlninja": "SQL Server injection exploitation engine",
    },
    "password_cracking": {
        "hashcat": "Advanced GPU-accelerated password recovery engine",
        "john": "John the Ripper: High-speed CPU password cracker",
        "medusa": "Modular, parallel network login cracking engine",
        "hydra": "Parallelized network login cracker supporting over 50 protocols",
        "mimikatz": "Windows post-exploitation tool used to dump credentials and kerberos tickets",
    },
    "wireless": {
        "aircrack-ng": "Suite of tools designed for Wi-Fi traffic capturing, packet injection, and key cracking",
        "kismet": "Wireless packet sniffer and device discovery system for 802.11 layers, Bluetooth, and SDR frequencies",
        "wifite": "Automated Python tool engineered to audit WEP, WPA, and WPA2 wireless setups",
        "bettercap": "Complete environment framework for auditing Wi-Fi, BLE, and Ethernet environments",
        "fern-wifi-cracker": "Graphical Python application engineered to audit wireless security configurations",
    },
    "network_intercept": {
        "wireshark": "Deep packet analysis utility that breaks down live stream headers",
        "tcpdump": "Lightweight command-line terminal network package capture utility",
        "macchanger": "System tool used to alter a hardware MAC address profile",
        "responder": "LLMNR, NBT-NS, and MDNS rogue validation authentication poisoner",
    },
    "forensics_reverse": {
        "autopsy": "Graphical interface engine running on top of The Sleuth Kit for disk image investigations",
        "volatility": "Advanced framework designed to dissect active system memory (RAM) dumps",
        "binwalk": "Automated analysis tool used to extract embedded binary firmware files",
        "ghidra": "Software reverse engineering suite used to decompile compiled binaries",
    },
    "active_directory": {
        "bloodhound": "Sharp graphical interface mapping tool that computes Active Directory access relationships to identify attack vectors",
        "crackmapexec": "Swiss army knife utility designed to brute force and map environments across Active Directory configurations",
    },
}


async def handle_list_tools(request: ListToolsRequest) -> ListToolsResult:
    """List all available Kali tools grouped by category."""
    mcp_tools = []
    for group, tools_dict in KALA_TOOLS.items():
        for name, desc in tools_dict.items():
            mcp_tools.append(Tool(
                name=f"kala_{group}_{name}",
                description=f"{desc} [Group: {group}]",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target": {"type": "string", "description": "Target IP, domain, URL, or file path"},
                        "options": {"type": "string", "description": "Optional command-line options/arguments", "default": ""},
                        "output_file": {"type": "string", "description": "Optional output file path", "default": ""},
                    },
                    "required": ["target"]
                }
            ))
    return ListToolsResult(tools=mcp_tools)


async def handle_call_tool(request: CallToolRequestParams) -> CallToolResult:
    """Execute a Kali tool."""
    name = request.name
    arguments = request.arguments or {}

    parts = name.split("_", 2)
    if len(parts) < 3:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Invalid tool name: {name}. Use: kala_<group>_<tool>")],
            is_error=True
        )

    group, tool = parts[1], parts[2]

    if group not in KALA_TOOLS:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Unknown group: {group}. Available: {list(KALA_TOOLS.keys())}")],
            is_error=True
        )
    if tool not in KALA_TOOLS[group]:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {tool} in group {group}. Available: {list(KALA_TOOLS[group].keys())}")],
            is_error=True
        )

    target = arguments.get("target", "")
    options = arguments.get("options", "")
    output_file = arguments.get("output_file", "")

    if not target:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Missing required 'target' argument for {tool}")],
            is_error=True
        )

    # ─── Authorization Check ────────────────────────────────────────────────
    authorized, reason = check_authorization(tool, target, user="opencode")
    if not authorized:
        return CallToolResult(
            content=[TextContent(type="text", text=f"DENIED: {reason}")],
            is_error=True
        )

    # ─── Build Command ──────────────────────────────────────────────────────
    cmd = [tool, target]
    if options:
        cmd.extend(options.split())
    if output_file:
        cmd.extend(["-o", output_file])

    evidence_path = None
    if output_file:
        evidence_dir = Path.home() / ".kala_evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        evidence_path = evidence_dir / output_file

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            env={**os.environ, "LANG": "C.UTF-8"}
        )

        output = result.stdout or result.stderr or "(no output)"
        if len(output) > 20000:
            output = output[:20000] + "\n[truncated — tool output too large]"

        if output_file:
            with open(evidence_path, "w") as f:
                f.write(output)
            if os.path.exists(evidence_path):
                sha256 = hash_file(str(evidence_path))
                log_authorization("opencode", tool, target, True, f"Output saved to {evidence_path} (sha256: {sha256})")

        return CallToolResult(
            content=[TextContent(type="text", text=f"=== {tool} on {target} ===\n{output}")]
        )

    except subprocess.TimeoutExpired:
        return CallToolResult(
            content=[TextContent(type="text", text=f"[{tool}] Timed out after 300s on target {target}")],
            is_error=True
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"[{tool}] Error: {str(e)}")],
            is_error=True
        )


# Register request handlers
app.add_request_handler("tools/list", ListToolsRequest, handle_list_tools)
app.add_request_handler("tools/call", CallToolRequestParams, handle_call_tool)


if __name__ == "__main__":
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    asyncio.run(main())
