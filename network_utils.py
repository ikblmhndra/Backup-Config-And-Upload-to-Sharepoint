"""
Network Utilities Module
Handles network connectivity checks and related utilities
"""

from icmplib import ping


def check_device_connectivity(address, site=None):
    """Check if device is reachable via ping."""
    try:
        result = ping(address, count=1)
        is_reachable = result.packets_received > 0
        
        if site:
            status = "reachable" if is_reachable else "unreachable"
            print(f"[{site}] Device {address} is {status}")
        
        return is_reachable
    except Exception as e:
        if site:
            print(f"[{site}] Ping error for {address}: {e}")
        return False


def check_multiple_devices(addresses):
    """Check connectivity for multiple devices."""
    results = {}
    for address in addresses:
        results[address] = check_device_connectivity(address)
    return results


def is_device_online(address, timeout=5, count=3):
    """Check if device is online with custom timeout and count."""
    try:
        result = ping(address, count=count, timeout=timeout)
        return result.packets_received > 0
    except Exception as e:
        print(f"Connectivity check error for {address}: {e}")
        return False


def get_device_response_time(address, count=1):
    """Get device response time via ping."""
    try:
        result = ping(address, count=count)
        if result.packets_received > 0:
            return result.avg_rtt
        return None
    except Exception as e:
        print(f"Response time check error for {address}: {e}")
        return None


def validate_ip_address(ip):
    """Basic IP address validation."""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except ValueError:
        return False