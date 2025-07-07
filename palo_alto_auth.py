"""
Palo Alto Authentication Module
Handles Palo Alto firewall authentication and token management
"""

import os
import requests
import xml.etree.ElementTree as ET
from config_manager import update_env_token


def check_token_valid_pa(address, api_key, cek_token):
    """Check if Palo Alto API token is valid."""
    try:
        url = f"https://{address}/{cek_token}{api_key}"
        response = requests.get(url, verify=False, timeout=10)
        root = ET.fromstring(response.text)
        return root.attrib.get("status") == "success"
    except Exception as e:
        print(f"[PA] Token check error: {e}")
        return False


def regenerate_token_pa(address, username, password, gen_token):
    """Generate new Palo Alto API token."""
    try:
        url = f"https://{address}/{gen_token}&user={username}&password={password}"
        response = requests.get(url, verify=False, timeout=10)
        root = ET.fromstring(response.text)
        key = root.find(".//key")
        return key.text if key is not None else None
    except Exception as e:
        print(f"[PA] Token generation error: {e}")
        return None


def handle_palo_alto_auth(address, api_key, username, password, site, i):
    """Handle Palo Alto authentication and token management."""
    cek_token = os.getenv(f"EXPIRY{i}")
    gen_token = os.getenv(f"GENERATE_TOKEN{i}")
    
    if not check_token_valid_pa(address, api_key, cek_token):
        print(f"[{site}] Token invalid. Regenerating...")
        new_token = regenerate_token_pa(address, username, password, gen_token)
        if new_token:
            update_env_token(i, new_token)
            return new_token
        else:
            return None
    return api_key