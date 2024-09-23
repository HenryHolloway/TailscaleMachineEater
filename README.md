# TailScale Device Deletion Tool

Hey there! This is a handy Python script to help you delete devices from your TailScale network based on different criteria.

## What It Does

- Fetches all devices from your TailScale network.
- Lets you filter devices by name, hostname, authorization status, OS, user, and client version.
- Deletes the devices that match your filters.

## How to Use It

Run the script with the necessary arguments to filter and delete devices:

```sh
python deleteMachines.py --org <organization_name> --api_key <api_key> [--name <device_name>] [--hostname <hostname>] [--authorized <true/false>] [--os <operating_system>] [--user <user>] [--client_version <client_version>]
```

### Arguments

- `--org`: Your TailScale organization name (you'll be prompted if you don't provide it).
- `--api_key`: Your TailScale API key (you'll be prompted if you don't provide it).
- `--name`: Filter devices by name.
- `--hostname`: Filter devices by hostname.
- `--authorized`: Filter devices by authorization status (true/false).
- `--os`: Filter devices by operating system.
- `--user`: Filter devices by user.
- `--client_version`: Filter devices by client version.

### Example

```sh
python3 deleteMachines.py --org myOrg --api_key myApiKey --name myDevice --authorized true
```

This will delete all authorized devices with names *containing* "myDevice" in the "myOrg" TailScale organization.
