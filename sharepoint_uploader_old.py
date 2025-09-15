"""
SharePoint Uploader Module
Handles file uploads to SharePoint
"""

import os
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext


def get_sharepoint_credentials():
    """Get SharePoint credentials from environment variables."""
    return {
        'username': os.getenv("SHAREPOINT_USERNAME"),
        'password': os.getenv("SHAREPOINT_PASSWORD"),
        'site_url': os.getenv("SITE_URL")
    }


def create_target_folder_url(site):
    """Create target folder URL for SharePoint upload."""
    return f"{os.getenv('SITE_URL_PATH')}/{site}"



def authenticate_sharepoint(site_url, username, password):
    """Authenticate with SharePoint."""
    auth_context = AuthenticationContext(site_url)
    if auth_context.acquire_token_for_user(username, password):
        return auth_context
    return None


def upload_file_to_sharepoint(ctx, file_path, filename, target_folder_url):
    """Upload file to SharePoint folder."""
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
            target_file = target_folder.upload_file(filename, file_content)
            ctx.execute_query()
        return target_file
    except Exception as e:
        print(f"SharePoint upload error: {e}")
        return None


def upload_to_sharepoint(output, filename, site):
    """Main function to upload backup file to SharePoint."""
    credentials = get_sharepoint_credentials()
    target_folder_url = create_target_folder_url(site)
    
    auth_context = authenticate_sharepoint(
        credentials['site_url'], 
        credentials['username'], 
        credentials['password']
    )
    
    if auth_context:
        try:
            ctx = ClientContext(credentials['site_url'], auth_context)
            target_file = upload_file_to_sharepoint(ctx, output, filename, target_folder_url)
            return target_file
        except Exception as e:
            print(f"[{site}] SharePoint upload failed: {e}")
            return None
    else:
        print(f"[{site}] SharePoint authentication failed.")
        return None