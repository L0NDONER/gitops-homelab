# FILE: /home/martin/ansible/commander/config.py
import os
import actions # Added import to reference handlers

# Base Paths
BASE_DIR = os.path.expanduser('~/ansible')
INVENTORY_PATH = os.path.join(BASE_DIR, 'inventory')
VAULT_PASS_FILE = os.path.join(BASE_DIR, '.vault_pass')

# --- COMMAND REGISTRIES MOVED FROM APP.PY ---
# Command Registry: maps keywords to handler functions
KEYWORD_COMMANDS = {
    'inspect': (actions.handle_inspect_command, ['inspect', 'motherboard', 'cpu', 'chip']),
    'weather': (actions.handle_weather_command, ['weather']),
    'disk': (actions.handle_disk_command, ['disk']),
    'pingall': (actions.handle_pingall_command, ['pingall']),
    'fleet': (actions.handle_fleet_command, ['fleet']),
    'seed': (actions.handle_seed_command, ['seed']),
}

# Prefix Commands: require arguments after the command
PREFIX_COMMANDS = {
    'addtv': actions.handle_addtv_command,
    'addmovies': actions.handle_addmovies_command,
}

# Secrets handling
try:
    import secrets
    WEATHER_API_KEY = secrets.WEATHER_API_KEY
    CITY_NAME = secrets.CITY_NAME
    ALLOWED_NUMBERS = secrets.ALLOWED_NUMBERS
except (ImportError, AttributeError):
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    CITY_NAME = os.getenv('CITY_NAME', 'Dereham,GB')
    ALLOWED_NUMBERS = os.getenv('ALLOWED_WHATSAPP_NUMBERS', '').split(',')

TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
