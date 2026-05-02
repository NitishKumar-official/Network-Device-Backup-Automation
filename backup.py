"""
Network Config Backup System
Author: Nitish Kumar
GitHub: github.com/ernitish123

Automatically connects to multiple routers/switches via SSH,
fetches running configuration, and saves versioned backups.
"""

import os
import yaml
import json
import logging
from datetime import datetime
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/backup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ── Load device inventory from YAML ───────────────────────────────────────────
def load_inventory(path: str = "inventory.yaml") -> list:
    """Load device list from YAML inventory file."""
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("devices", [])


# ── Connect and fetch config ───────────────────────────────────────────────────
def fetch_config(device: dict) -> str | None:
    """
    SSH into a network device using Netmiko and fetch running config.
    Returns config string or None on failure.
    """
    connection_params = {
        "device_type": device["device_type"],   # e.g. cisco_ios, cisco_xe
        "host":        device["host"],
        "username":    device["username"],
        "password":    device["password"],
        "secret":      device.get("secret", ""),  # enable password (optional)
        "timeout":     device.get("timeout", 10),
    }

    try:
        logger.info(f"Connecting to {device['name']} ({device['host']})...")
        with ConnectHandler(**connection_params) as conn:
            conn.enable()                              # enter enable mode
            config = conn.send_command("show running-config")
            logger.info(f"✅ Config fetched from {device['name']}")
            return config

    except NetmikoAuthenticationException:
        logger.error(f"❌ Auth failed for {device['name']} ({device['host']})")
    except NetmikoTimeoutException:
        logger.error(f"❌ Timeout — {device['name']} ({device['host']}) unreachable")
    except Exception as e:
        logger.error(f"❌ Unexpected error for {device['name']}: {e}")

    return None


# ── Save config to file ────────────────────────────────────────────────────────
def save_config(device_name: str, config: str, backup_dir: str = "backups") -> str:
    """
    Save config string to a timestamped file.
    Directory structure: backups/<device_name>/<timestamp>.cfg
    """
    device_dir = os.path.join(backup_dir, device_name)
    os.makedirs(device_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.cfg"
    filepath = os.path.join(device_dir, filename)

    with open(filepath, "w") as f:
        f.write(config)

    logger.info(f"💾 Saved: {filepath}")
    return filepath


# ── Generate backup report ─────────────────────────────────────────────────────
def save_report(results: list, report_dir: str = "reports") -> None:
    """Save a JSON summary report of the backup run."""
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.json")

    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"📊 Report saved: {report_path}")


# ── Main orchestrator ──────────────────────────────────────────────────────────
def run_backup(inventory_path: str = "inventory.yaml") -> None:
    """
    Main function:
    1. Load device inventory
    2. Connect to each device
    3. Fetch running config
    4. Save to file
    5. Generate report
    """
    os.makedirs("logs", exist_ok=True)

    logger.info("=" * 50)
    logger.info("🚀 Network Config Backup Started")
    logger.info("=" * 50)

    devices  = load_inventory(inventory_path)
    results  = []
    success  = 0
    failed   = 0

    for device in devices:
        config = fetch_config(device)

        if config:
            filepath = save_config(device["name"], config)
            results.append({
                "device":    device["name"],
                "host":      device["host"],
                "status":    "success",
                "file":      filepath,
                "timestamp": datetime.now().isoformat()
            })
            success += 1
        else:
            results.append({
                "device":    device["name"],
                "host":      device["host"],
                "status":    "failed",
                "file":      None,
                "timestamp": datetime.now().isoformat()
            })
            failed += 1

    # Summary
    logger.info("=" * 50)
    logger.info(f"✅ Success: {success} | ❌ Failed: {failed} | Total: {len(devices)}")
    logger.info("=" * 50)

    save_report(results)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_backup()
