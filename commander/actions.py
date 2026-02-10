# actions_net.py
import subprocess
import os
import json
import time
import socket
import requests

# -------------------------------
# Helpers
# -------------------------------

def run(cmd, timeout=5):
    return subprocess.check_output(
        cmd,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        text=True
    ).strip()


# -------------------------------
# Hint / Guidance Handlers
# -------------------------------

def handle_ssh_hint():
    return "🔐 Use: `ssh <host>` to test SSH connectivity"

def handle_ping_hint():
    return "🏓 Use: `ping <host>` to test reachability"

def handle_tailping_hint():
    return "🌀 Use: `tailping <node>` to test Tailscale connectivity"


# -------------------------------
# Prefix Command Handlers
# -------------------------------

def handle_ping_command(target):
    try:
        out = run(["ping", "-c", "2", "-W", "2", target], timeout=5)
        return f"🏓 Ping OK\n{out.splitlines()[-1]}"
    except Exception as e:
        return f"❌ Ping failed: {target}"

def handle_ssh_command(host):
    try:
        run([
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=3",
            host,
            "echo ok"
        ], timeout=5)
        return f"🔐 SSH OK: {host}"
    except Exception:
        return f"❌ SSH failed: {host}"

def handle_tailping_command(node):
    try:
        out = run(["tailscale", "ping", "--c=3", node], timeout=6)
        return f"🌀 Tailscale ping OK\n{out.splitlines()[-1]}"
    except Exception:
        return f"❌ Tailscale ping failed: {node}"

def handle_trace_command(target):
    try:
        out = run(["traceroute", "-m", "8", target], timeout=10)
        lines = out.splitlines()[:6]
        return "🧭 Trace:\n" + "\n".join(lines)
    except Exception:
        return f"❌ Trace failed: {target}"


# -------------------------------
# Status / Info Handlers
# -------------------------------

def handle_tailscale_status():
    try:
        out = run(["tailscale", "status"], timeout=5)
        lines = out.splitlines()
        online = [l for l in lines if "idle" in l or "active" in l]
        return f"🌀 Tailnet OK\nNodes online: {len(online)}"
    except Exception:
        return "❌ Tailscale not running"

def handle_exitip_command():
    try:
        ip = requests.get("https://api.ipify.org", timeout=4).text.strip()
        return f"🌍 Exit IP: {ip}"
    except Exception:
        return "❌ Unable to fetch public IP"

