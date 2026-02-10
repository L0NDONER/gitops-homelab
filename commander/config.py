# config.py (NETOPS edition)
import os

# Import your network/tunnel handlers.
# Create actions_net.py with the matching functions, or rename your existing actions file.
import actions

# Base Paths
BASE_DIR = os.path.expanduser('~/ansible')
INVENTORY_PATH = os.path.join(BASE_DIR, 'inventory')
VAULT_PASS_FILE = os.path.join(BASE_DIR, '.vault_pass')

# --- COMMAND REGISTRIES ---
# Keyword Commands: maps a command "concept" to (handler, trigger words)
# Keep triggers broad so natural messages still hit the right handler.
KEYWORD_COMMANDS = {
    # Tailscale / tunnels
    'tailscale': (actions.handle_tailscale_status, ['tailscale', 'tailnet', 'tunnel', 'vpn', 'ts']),
    'tailping': (actions.handle_tailping_hint, ['tailping', 'ts ping', 'tailscale ping']),

    # Connectivity basics
    'ping': (actions.handle_ping_hint, ['ping', 'reachable', 'can you reach', 'connectivity']),
    'ssh': (actions.handle_ssh_hint, ['ssh', 'login', 'connect to', 'port 22']),

    # Exit/public IP sanity
    'exitip': (actions.handle_exitip_command, ['exit', 'exit node', 'public ip', 'egress', 'what ip']),
}

# Prefix Commands: require arguments after the command
# Example: "ssh host1", "ping 1.2.3.4", "tailping mynode", "trace host"
PREFIX_COMMANDS = {
    'ssh': actions.handle_ssh_command,
    'ping': actions.handle_ping_command,
    'tailping': actions.handle_tailping_command,
    'trace': actions.handle_trace_command,   # optional; can be a no-op if you don’t want traceroute
}

# Secrets handling
try:
    import secrets
    ALLOWED_NUMBERS = secrets.ALLOWED_NUMBERS
    GROQ_API_KEY = getattr(secrets, "GROQ_API_KEY", None)
except (ImportError, AttributeError):
    ALLOWED_NUMBERS = os.getenv('ALLOWED_WHATSAPP_NUMBERS', '').split(',')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Twilio
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')

# Optional debug toggle
DEBUG_MODE = os.getenv('DEBUG_MODE', '0') in ('1', 'true', 'True', 'yes', 'YES')

