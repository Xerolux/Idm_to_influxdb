# Xerolux 2026
import requests
import argparse
import os
import time
from datetime import datetime

# Can be run inside the container or locally if ports are forwarded
API_URL = "http://localhost:8000/api/v1"
# For CLI, we assume we are admin and can read the token from env or arg
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "change-me-to-something-secure")


def get_headers():
    return {"Authorization": f"Bearer {AUTH_TOKEN}"}


def format_number(num):
    """Format number with thousands separator."""
    try:
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return str(num)


def show_pool_status():
    """Fetch and display data pool statistics."""
    try:
        # Public endpoint
        response = requests.get(f"{API_URL}/pool/status")
        if response.status_code == 200:
            data = response.json()
            print("\n=== Data Pool Statistics ===")
            print(
                f"Total Installations:     {format_number(data.get('total_installations', 0))}"
            )
            print(
                f"Total Data Points:       {format_number(data.get('total_data_points', 0))}"
            )
            print(
                f"Data Sufficient:         {'Yes' if data.get('data_sufficient') else 'No'}"
            )
            print(f"Status Message:          {data.get('message', '')}")
        else:
            print(f"\n[!] Error fetching pool status: {response.status_code}")
    except Exception as e:
        print(f"\n[!] Connection Error (Pool Status): {e}")


def show_models():
    """Fetch and display available models."""
    try:
        response = requests.get(f"{API_URL}/models", headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"\n=== Available Models ({len(models)}) ===")
            if not models:
                print("No models generated yet.")
            for model in models:
                size_mb = model.get("size_bytes", 0) / (1024 * 1024)
                mod_time = datetime.fromtimestamp(model.get("modified", 0)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                print(f"- {model.get('name')}")
                print(f"  Filename: {model.get('filename')}")
                print(f"  Size:     {size_mb:.2f} MB")
                print(f"  Created:  {mod_time}")
                print(f"  Hash:     {model.get('hash')[:8]}...")
        elif response.status_code == 401:
            print("\n[!] Unauthorized to list models. Check AUTH_TOKEN.")
        else:
            print(f"\n[!] Error fetching models: {response.status_code}")
    except Exception as e:
        print(f"\n[!] Connection Error (Models): {e}")


def show_server_status():
    """Show server status and stats."""
    try:
        response = requests.get(f"{API_URL}/status", headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            print("\n=== Telemetry Server Status ===")
            print(f"Service Status:          {data.get('status')}")
            # This metric might overlap with pool status but is good for verification
            print(f"Active Installs (30d):   {data.get('active_installations_30d')}")
            srv_time = datetime.fromtimestamp(
                data.get("timestamp", time.time())
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(f"Server Time:             {srv_time}")
        elif response.status_code == 401:
            print("\n[!] Unauthorized to check status. Check AUTH_TOKEN.")
        else:
            print(
                f"\n[!] Error fetching status: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"\n[!] Connection Error (Status): {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telemetry Server Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Status command
    subparsers.add_parser("status", help="Show full server statistics and model info")

    args = parser.parse_args()

    if args.command == "status":
        print(f"Connecting to {API_URL}...")
        show_server_status()
        show_pool_status()
        show_models()
        print("\n")
    else:
        # Default to status if no command provided, or print help
        if not args.command:
            parser.print_help()
