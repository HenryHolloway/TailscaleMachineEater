#!/usr/bin/env python3

import requests
import json
import logging
import argparse
import getpass

# Setup logging
logging.basicConfig(level=logging.INFO)

def get_devices(base_url, headers):
    """
    Fetch all devices in the current TailScale network via the API.
    """
    url = f"{base_url}/devices"
    logging.info("Fetching devices from the TailScale network...")
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['devices']  # Return the list of devices

def delete_device(device_id, headers):
    """
    Delete a specific device by ID.
    """
    delete_url = f"https://api.tailscale.com/api/v2/device/{device_id}"
    logging.info(f"Deleting device {device_id}...")
    
    delete_response = requests.delete(delete_url, headers=headers)
    
    if delete_response.status_code == 200:
        logging.info(f"Successfully deleted device {device_id}")
    else:
        logging.error(f"Error deleting device {device_id}: {delete_response.status_code} - {delete_response.text}")

def main():
    parser = argparse.ArgumentParser(description="Delete TailScale devices based on matching parameters.")
    parser.add_argument('--name', type=str, help="Match devices by name.")
    parser.add_argument('--hostname', type=str, help="Match devices by hostname.")
    parser.add_argument('--authorized', type=bool, help="Match devices by authorization status (true/false).")
    parser.add_argument('--os', type=str, help="Match devices by operating system.")
    parser.add_argument('--user', type=str, help="Match devices by user.")
    parser.add_argument('--client_version', type=str, help="Match devices by client version.")
    parser.add_argument('--org', type=str, help="TailScale organization name.")
    parser.add_argument('--api_key', type=str, help="TailScale API key.")
    
    args = parser.parse_args()

    # Check if at least one filtering argument is provided
    if not any([args.name, args.hostname, args.authorized, args.os, args.user, args.client_version]):
        parser.print_help()
        print("ERROR: At least one filtering argument (--name, --hostname, --authorized, --os, --user, --client_version) must be provided.")
        return

    # Prompt for organization name and API key if not provided
    org_name = args.org if args.org else input("Enter your TailScale organization name: ")
    api_key = args.api_key if args.api_key else getpass.getpass("Enter your TailScale API key: ")

    # TailScale API URL
    base_url = f"https://api.tailscale.com/api/v2/tailnet/{org_name}/"

    # HTTP Headers for Authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Get all devices
    devices = get_devices(base_url, headers)

    # Filter devices based on provided arguments
    target_devices = devices
    if args.name:
        target_devices = [device for device in target_devices if args.name.lower() in device.get('name', '').lower()]
    if args.hostname:
        target_devices = [device for device in target_devices if args.hostname.lower() in device.get('hostname', '').lower()]
    if args.authorized is not None:
        target_devices = [device for device in target_devices if device.get('authorized') == args.authorized]
    if args.os:
        target_devices = [device for device in target_devices if args.os.lower() in device.get('os', '').lower()]
    if args.user:
        target_devices = [device for device in target_devices if args.user.lower() in device.get('user', '').lower()]
    if args.client_version:
        target_devices = [device for device in target_devices if args.client_version.lower() in device.get('clientVersion', '').lower()]

    if not target_devices:
        logging.info("No devices found matching the given parameters.")
        return

    logging.info(f"Found {len(target_devices)} device(s) matching the given parameters.")
    
    # Delete each target device
    for device in target_devices:
        device_id = device['id']
        delete_device(device_id, headers)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")