# 🔧 Network Config Backup System

Automated network device configuration backup tool using **Python + Netmiko**.

## 🎯 Problem Solved
In real companies, network device configs are backed up manually.  
If a device crashes → config is **lost**.  
This tool **automatically** connects to multiple routers/switches, fetches their running config, and saves versioned backups.

---

## 🚀 Features
- ✅ SSH into **multiple routers/switches** simultaneously
- ✅ Fetches `show running-config` from each device
- ✅ Saves **timestamped, versioned backups** per device
- ✅ **YAML-driven** device inventory — easy to add/remove devices
- ✅ **JSON report** generated after every backup run
- ✅ Handles failures gracefully (auth errors, timeouts, unreachable hosts)
- ✅ Full **PyTest** unit test suite with mocked SSH connections

---

## 📁 Project Structure
```
network-config-backup/
├── backup.py            # Main backup engine
├── inventory.yaml       # Device inventory (hosts, credentials)
├── requirements.txt     # Dependencies
├── tests/
│   └── test_backup.py   # PyTest unit tests
├── backups/             # Auto-created — stores .cfg files
│   └── Router-01/
│       └── 2025-05-01_10-30-00.cfg
├── reports/             # Auto-created — JSON run reports
│   └── report_2025-05-01_10-30-00.json
└── logs/
    └── backup.log       # Run logs
```

---

## ⚙️ Setup & Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure your devices in `inventory.yaml`
```yaml
devices:
  - name: "Router-01"
    host: "192.168.1.1"
    device_type: "cisco_ios"
    username: "admin"
    password: "your_password"
    secret: "enable_password"
```

### 3. Run backup
```bash
python backup.py
```

### 4. Run tests
```bash
pytest tests/ -v
```

---

## 📊 Sample Output
```
2025-05-01 10:30:00 [INFO] 🚀 Network Config Backup Started
2025-05-01 10:30:02 [INFO] ✅ Config fetched from Router-01
2025-05-01 10:30:02 [INFO] 💾 Saved: backups/Router-01/2025-05-01_10-30-02.cfg
2025-05-01 10:30:05 [INFO] ❌ Timeout — Switch-02 (192.168.1.11) unreachable
2025-05-01 10:30:05 [INFO] ✅ Success: 3 | ❌ Failed: 1 | Total: 4
```

---

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Netmiko | SSH connection to network devices |
| PyYAML | Device inventory management |
| PyTest | Unit testing with mocked SSH |
| JSON | Backup run reporting |
| Logging | Run logs & audit trail |

---

## 📌 Supported Devices
- Cisco IOS / IOS-XE / NX-OS
- Juniper JunOS
- Arista EOS
- Any Netmiko-supported platform

---

## 👤 Author
**Nitish Kumar** — [github.com/ernitish123](https://github.com/ernitish123)
