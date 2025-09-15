# debug_sharepoint.py

import os
from dotenv import load_dotenv
from O365 import Account

load_dotenv()

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

credentials = (client_id, client_secret)
account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)

if not account.is_authenticated:
    account.authenticate()

SHAREPOINT_HOSTNAME = "privygate.sharepoint.com"
SHAREPOINT_SITE_NAME = "BlueTeamLibrary"

sharepoint = account.sharepoint()
site = sharepoint.get_site(SHAREPOINT_HOSTNAME, f"sites/{SHAREPOINT_SITE_NAME}")
drive = site.get_default_document_library()

print("=== Root items in default document library ===")
for item in drive.get_root_folder().get_items(limit=50):
    if item.is_folder:
        print(f"[Folder] {item.name}")
    else:
        print(f"[File]   {item.name}")
