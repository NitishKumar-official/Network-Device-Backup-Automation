#  Network Device Backup Automation (Python + Netmiko)

##  Project Overview

This project is a simple network automation tool built using Python and Netmiko. It connects to multiple network devices (routers/switches) over SSH and automatically takes their running configuration backup.

The main goal of this project is to reduce manual effort and ensure regular backup of network device configurations.

---

## Features

* Connects to multiple devices using SSH
* Takes running configuration backup
* Saves backup in local files
* Handles connection errors
* Easy to scale for large networks

---

##  Technologies Used

* Python
* Netmiko (for SSH connection)
* Basic Networking (Cisco devices)

---

##  Project Structure

```
project-folder/
│
├── backup_script.py
├── devices.py (optional)
├── backups/
│   ├── 192.168.1.1_backup.txt
│   ├── 192.168.1.2_backup.txt
│
└── README.md
```

---

##  Installation

1. Clone the repository:

```
git clone [https://github.com/your-username/network-backup.git](https://github.com/NitishKumar-official/Network-Device-Backup-Automation)
cd network-backup
```

2. Install dependencies:

```
pip install netmiko
```

---

##  Usage

1. Update device details in the script:

```python
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'admin123',
    }
]
```

2. Run the script:

```
python backup_script.py
```

3. Backups will be saved in the project folder.

---

## 📸 Sample Output

```
Backup saved for 192.168.1.1
Backup saved for 192.168.1.2
```

---

## ⚠️ Error Handling

* If a device is unreachable, the script will show an error message.
* The script continues running for other devices.

---

## 🔥 Future Improvements

* Add timestamp to backup files
* Read device list from CSV/Excel
* Send email notifications
* Create web dashboard using Flask
* Schedule automatic backups

---

##  Use Case

This project can be used in real-world networking environments to:

* Maintain regular backups
* Reduce manual configuration effort
* Improve network reliability

---

##  Author

Nitish Kumar

---

##  Conclusion

This project demonstrates basic network automation using Python and Netmiko, which is highly useful in modern IT infrastructure management.
