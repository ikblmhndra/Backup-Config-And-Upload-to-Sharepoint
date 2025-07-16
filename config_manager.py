"""
Configuration Management Module
Handles environment variables, constants, and device configuration
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import requests


def load_environment():
    """Load environment variables and disable SSL warnings."""
    load_dotenv()
    requests.packages.urllib3.disable_warnings()


def get_constants():
    """Return application constants."""
    return {
        'today': datetime.strftime(datetime.today(), "%Y-%m-%d"),
        'firewalls_iteration': [1, 2, 3, 4, 5, 6],
        'tele_group_id': os.getenv("TELEBOT_GROUP_ID"),
        'message_thread_id': 631,
        'hostname_file': f"{os.path.dirname(__file__)}/fortigate/fortigate_hostname.txt"
    }


def get_device_config(i):
    """Get device configuration from environment variables."""
    return {
        'device_type': os.getenv(f"DEVICE_TYPE{i}"),
        'address': os.getenv(f"ADDRESS{i}"),
        'endpoint': os.getenv(f"ENDPOINT{i}"),
        'site': os.getenv(f"SITE{i}"),
        'root_dir': os.path.dirname(__file__),
        'api_key': os.getenv(f"API_KEY{i}"),
        'username': os.getenv("FW_USERNAME"),
        'password': os.getenv("FW_PASSWORD")
    }


def update_env_token(index, new_token):
    """Update API token in .env file."""
    file_path = ".env"
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    key = f"API_KEY{index}="
    for i, line in enumerate(lines):
        if line.startswith(key):
            lines[i] = f"{key}{new_token}\n"
            break
    else:
        lines.append(f"{key}{new_token}\n")
    
    with open(file_path, "w") as file:
        file.writelines(lines)