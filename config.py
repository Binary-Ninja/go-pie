"""Load in configuration file and set defaults."""

# Standard library imports.
import json
from pathlib import Path

# Export the configuration variables.
__all__ = [
    "DEFAULT_SCREEN_SIZE",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "PUBLIC_SERVER",
]

# Try to load in the config file.
try:
    # Decode json configuration file.
    with open(Path() / "config.json") as file:
        config_data = json.load(file)
except FileNotFoundError:
    # The file doesn't exist, so create an empty configuration.
    config_data = {}

# Extract configuration data with default values.
# The starting screen resolution.
DEFAULT_SCREEN_SIZE = config_data.get("screen_resolution", (800, 600))
# The default host for servers and clients.
DEFAULT_HOST = config_data.get("default_host", "127.0.0.1")
# The default port for servers and clients.
DEFAULT_PORT = config_data.get("default_port", 5071)
# Whether the server is public with ngrok or not.
PUBLIC_SERVER = config_data.get("public_server", False)
