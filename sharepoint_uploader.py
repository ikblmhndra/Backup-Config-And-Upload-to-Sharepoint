# sharepoint_uploader.py
import os
from dotenv import load_dotenv
from O365 import Account

load_dotenv()

# Ambil env
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# SharePoint info
sharepoint_hostname = "privygate.sharepoint.com"
sharepoint_site_name = "BlueTeamLibrary"
base_folder = "BACKUP FILE CONFIG NETWORK SECURITY"

# Auth
credentials = (client_id, client_secret)
account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)

if not account.is_authenticated:
    account.authenticate()

def upload_to_sharepoint(output, filename, site):
    try:
        sharepoint = account.sharepoint()
        sp_site = sharepoint.get_site(sharepoint_hostname, f"sites/{sharepoint_site_name}")
        drive = sp_site.get_default_document_library()

        # path tujuan: "Shared Documents/BACKUP FILE CONFIG NETWORK SECURITY/<site>"
        target_path = f"{base_folder}/{site}"

        try:
            folder_item = drive.get_item_by_path(target_path)
        except Exception:
            # kalau folder belum ada, bikin dulu
            parent_folder = drive.get_item_by_path(base_folder)
            folder_item = parent_folder.create_child_folder(site)

        # Upload file → yang dipakai output (path lokal)
        uploaded_item = folder_item.upload_file(output)

        print(f"[{site}] Upload success: {uploaded_item.web_url}")
        return uploaded_item.web_url

    except Exception as e:
        print(f"[{site}] SharePoint upload failed: {e}")
        return None

