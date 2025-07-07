"""
Notification Service Module
Handles Telegram notifications and message formatting
"""

from datetime import datetime
from telebot import simpleChat


def send_telegram_notification(tele_group_id, message, message_thread_id):
    """Send notification via Telegram."""
    try:
        simpleChat(tele_group_id, message, message_thread_id)
        return True
    except Exception as e:
        print(f"Telegram notification error: {e}")
        return False


def create_failure_message(site, reason, today):
    """Create failure notification message."""
    return (
        f"=== *Periodical System Backup Fail* ===\n"
        f"Site : PID-FW-{site}\n"
        f"Status : Failed\n"
        f"Timestamp : {today}\n"
        f"Reason : {reason}"
    )


def create_success_message(site, target_file):
    """Create success notification message."""
    timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    return (
        "=== *Periodical System Backup Success* ===\n"
        f"Site : PID-FW-{site}\n"
        "Status : Success\n"
        f"Timestamp : {timestamp}\n"
        f"Link : [File Backup PID-FW-{site}](https://privygate.sharepoint.com{target_file.serverRelativeUrl})"
    )


def create_custom_message(site, status, timestamp, reason=None, link=None):
    """Create custom notification message."""
    message = (
        f"=== *Periodical System Backup {status}* ===\n"
        f"Site : PID-FW-{site}\n"
        f"Status : {status}\n"
        f"Timestamp : {timestamp}\n"
    )
    
    if reason:
        message += f"Reason : {reason}\n"
    
    if link:
        message += f"Link : {link}\n"
    
    return message.strip()


def send_failure_notification(tele_group_id, message_thread_id, site, reason, today):
    """Send failure notification."""
    message = create_failure_message(site, reason, today)
    return send_telegram_notification(tele_group_id, message, message_thread_id)


def send_success_notification(tele_group_id, message_thread_id, site, target_file):
    """Send success notification."""
    message = create_success_message(site, target_file)
    return send_telegram_notification(tele_group_id, message, message_thread_id)