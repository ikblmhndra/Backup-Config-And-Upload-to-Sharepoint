"""
Main Backup Script
Orchestrates the firewall backup process using modular components
"""

# Import all required modules
from config_manager import load_environment, get_constants, get_device_config
from palo_alto_auth import handle_palo_alto_auth
from fortinet_auth import handle_fortinet_auth
from backup_operations import download_config
from sharepoint_uploader import upload_to_sharepoint
from notification_service import (
    send_failure_notification, 
    send_success_notification,
    create_failure_message,
    send_telegram_notification
)
from network_utils import check_device_connectivity


def process_single_firewall(i, constants):
    """Process backup for a single firewall device."""
    config = get_device_config(i)
    site = config['site']
    address = config['address']
    
    print(f"[{site}] Starting backup...")

    # Check connectivity
    if not check_device_connectivity(address, site):
        send_failure_notification(
            constants['tele_group_id'], 
            constants['message_thread_id'], 
            site, 
            "Device Unreachable", 
            constants['today']
        )
        print(f"[{site}] Unreachable")
        return False

    # Handle authentication based on device type
    session = None
    if config['device_type'] == "PA":
        api_key = handle_palo_alto_auth(
            address, config['api_key'], config['username'], 
            config['password'], site, i
        )
        if not api_key:
            send_failure_notification(
                constants['tele_group_id'], 
                constants['message_thread_id'], 
                site, 
                "Authentication Failed", 
                constants['today']
            )
            return False
        config['api_key'] = api_key
        
    elif config['device_type'] == "FORTI":
        session = handle_fortinet_auth(
            address, config['username'], config['password'], site
        )
        if not session:
            send_failure_notification(
                constants['tele_group_id'], 
                constants['message_thread_id'], 
                site, 
                "Authentication Failed", 
                constants['today']
            )
            return False

    # Download configuration
    output, filename = download_config(
        config['device_type'], address, config['endpoint'], 
        config['api_key'], session, site, constants['today'], 
        config['root_dir']
    )
    
    if not output:
        send_failure_notification(
            constants['tele_group_id'], 
            constants['message_thread_id'], 
            site, 
            "Config Download Failed", 
            constants['today']
        )
        return False

    # Upload to SharePoint
    target_file = upload_to_sharepoint(output, filename, site)
    if target_file:
        send_success_notification(
            constants['tele_group_id'], 
            constants['message_thread_id'], 
            site, 
            target_file
        )
        print(f"[{site}] Backup completed successfully")
        return True
    else:
        send_failure_notification(
            constants['tele_group_id'], 
            constants['message_thread_id'], 
            site, 
            "SharePoint Upload Failed", 
            constants['today']
        )
        return False


def run_backup_process():
    """Run the complete backup process for all firewalls."""
    print("Starting firewall backup process...")
    
    load_environment()
    constants = get_constants()
    
    successful_backups = 0
    failed_backups = 0
    
    for i in constants['firewalls_iteration']:
        try:
            if process_single_firewall(i, constants):
                successful_backups += 1
            else:
                failed_backups += 1
        except Exception as e:
            print(f"Error processing firewall {i}: {e}")
            failed_backups += 1
            continue
    
    print(f"\nBackup process completed:")
    print(f"Successful backups: {successful_backups}")
    print(f"Failed backups: {failed_backups}")
    print(f"Total devices processed: {successful_backups + failed_backups}")


def main():
    """Main function to orchestrate the backup process."""
    try:
        run_backup_process()
    except KeyboardInterrupt:
        print("\nBackup process interrupted by user.")
    except Exception as e:
        print(f"Critical error in backup process: {e}")
    finally:
        print("Backup process terminated.")


if __name__ == "__main__":
    main()