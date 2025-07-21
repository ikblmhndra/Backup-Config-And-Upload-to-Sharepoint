"""
Backup Operations Module
Handles configuration download and file operations
"""

import os
import requests
from extrahop_backup import download_extrahop_config


def download_config(device_type, address, endpoint, api_key, session, site, today, root_dir):
    """Download configuration from firewall device."""
    try:
        os.makedirs(f"{root_dir}/backup-file", exist_ok=True)
        filename = f"{site}_{today}.xml"
        output = f"{root_dir}/backup-file/{filename}"

        if device_type == "FORTI":  # Fortigate
            response = session.get(
                f"https://{address}/api/v2/monitor/system/config/backup", 
                params={"scope": "global"}, 
                verify=False, 
                stream=True
            )
            response.raise_for_status()
            with open(output, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        elif device_type == "EXTRAHOP":  # ExtraHop
            output, filename = download_extrahop_config(
                host=address,
                api_key=api_key,
                backup_name=f"{site}_{today}",
                site=site,
                today=today,
                root_dir=root_dir
            )

        else:  # Palo Alto
            response = requests.get(f"https://{address}/{endpoint}{api_key}", verify=False)
            response.raise_for_status()
            with open(output, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"[{site}] Backup saved: {output}")
        return output, filename
    except Exception as e:
        print(f"[{site}] Download error: {e}")
        return None, None

def create_backup_directory(root_dir):
    """Create backup directory if it doesn't exist."""
    backup_dir = f"{root_dir}/backup-file"
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def generate_filename(site, today, extension="xml"):
    """Generate backup filename based on site and date."""
    return f"{site}_{today}.{extension}"


def save_config_to_file(response, output_path):
    """Save configuration response to file."""
    try:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False