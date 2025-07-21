# extrahop_backup.py

import json
import requests
from urllib.parse import urlunparse
import os

def download_extrahop_config(host, api_key, backup_name, site, today, root_dir):
    try:
        headers = {
            "Authorization": f"ExtraHop apikey={api_key}",
            "Content-Type": "application/json"
        }

        # Step 1: Create Backup
        create_url = urlunparse(("https", host, "/api/v1/customizations", "", "", ""))
        resp = requests.post(create_url, headers=headers, data=json.dumps({"name": f"{site}_{today}"}), verify=False)
        resp.raise_for_status()
        backup_id = resp.headers["Location"].split("/")[-1]

        # Step 2: Get Backup Name
        name_url = urlunparse(("https", host, f"/api/v1/customizations/{backup_id}", "", "", ""))
        resp = requests.get(name_url, headers=headers, verify=False)
        resp.raise_for_status()
        backup_name = resp.json()[".meta"]["name"]

        # Step 3: Download Backup
        download_url = urlunparse(("https", host, f"/api/v1/customizations/{backup_id}/download", "", "", ""))
        download_headers = {
            "Authorization": f"ExtraHop apikey={api_key}",
            "accept": "application/exbk"
        }
        resp = requests.post(download_url, headers=download_headers, verify=False)
        resp.raise_for_status()

        # Step 4: Save Backup File
        os.makedirs(f"{root_dir}/backup-file", exist_ok=True)
        backup_filename = f"{site}_{today}.exbk"
        output_path = os.path.join(root_dir, "backup-file", backup_filename)
        with open(output_path, "wb") as f:
            f.write(resp.content)

        # print(f"[{site}] Backup saved: {output_path}")
        return output_path, backup_filename

    except Exception as e:
        print(f"[{site}] ExtraHop backup error: {type(e).__name__}: {e}")
        return None, None
