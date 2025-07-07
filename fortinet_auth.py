"""
Fortinet Authentication Module
Handles Fortinet firewall session-based authentication
"""

import os
import json
import pickle
import requests


def save_session(session, hostname):
    """Save Fortinet session to pickle file."""
    with open(f"{os.path.dirname(__file__)}/fortigate/fortigate_session_{hostname}.pkl", 'wb') as f:
        pickle.dump(session.cookies, f)
    with open(f"{os.path.dirname(__file__)}/fortigate/fortigate_hostname.txt", 'w') as f:
        f.write(hostname)


def load_session(hostname):
    """Load Fortinet session from pickle file."""
    filename = f"{os.path.dirname(__file__)}/fortigate/fortigate_session_{hostname}.pkl"
    if not os.path.exists(filename):
        return None
    
    session = requests.Session()
    try:
        with open(filename, 'rb') as f:
            session.cookies.update(pickle.load(f))
        return session
    except:
        return None


def is_session_valid_fortinet(address, session):
    """Check if Fortinet session is valid."""
    try:
        url = f"https://{address}/api/v2/monitor/system/status"
        response = session.get(url, verify=False, timeout=10)
        return (response.status_code == 200 and 
                response.headers.get('Content-Type', '').startswith('application/json'))
    except:
        return False


def regenerate_session_fortinet(address, username, password, hostname):
    """Generate new Fortinet session."""
    url = f"https://{address}/api/v2/authentication"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": username,
        "secretkey": password,
        "ack_post_disclaimer": True
    }
    
    session = requests.Session()
    try:
        response = session.post(url, headers=headers, data=json.dumps(data), 
                              verify=False, timeout=10)
        if response.status_code == 200 and response.json().get("status_code") == 5:
            save_session(session, hostname)
            return session
    except:
        pass
    return None


def handle_fortinet_auth(address, username, password, site):
    """Handle Fortinet authentication and session management."""
    hostname = site
    session = load_session(hostname)
    
    if not session or not is_session_valid_fortinet(address, session):
        session = regenerate_session_fortinet(address, username, password, hostname)
        if not session:
            print(f"[{site}] Failed to re-login to Fortinet.")
            return None
    return session