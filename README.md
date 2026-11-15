# XFCE Connection Centre

A lightweight connectivity dashboard for Android-based Linux desktop environments.

XFCE Connection Centre displays connectivity-related information inside XFCE running through Termux and Proot. It provides a simple graphical interface for checking network status and launching selected Android settings shortcuts.

---

# What This Project Does

XFCE Connection Centre can:

- Display Wi‑Fi status
- Display Bluetooth status (if available)
- Detect network interfaces
- Show connectivity information
- Refresh status manually
- Refresh status automatically
- Integrate into the XFCE Applications Menu

---

# What This Project Does NOT Do

XFCE Connection Centre does NOT:

- Install Termux
- Install Debian or Ubuntu
- Install Proot
- Install XFCE Desktop
- Install VNC Server
- Install Termux:X11
- Enable or disable Android Wi‑Fi
- Enable or disable Android Bluetooth
- Modify Android system settings automatically

It is a dashboard application, not a complete Android desktop setup solution.

---

# Who Is This For?

This project is intended for users who already run Linux desktop environments on Android using:

- Termux
- Proot-Distro
- Debian or Ubuntu
- XFCE Desktop

If you do not have XFCE running yet, complete that setup first.

---

# Recommended Environment

```text
Android Device
│
├── Termux
│
├── Proot-Distro
│
├── Debian or Ubuntu
│
├── XFCE Desktop
│
├── Termux:X11 or VNC
│
└── XFCE Connection Centre
```

---

# Fresh Android Setup Guide

If you are starting from a completely fresh Android device, follow these steps first.

---

## Step 1 - Install Termux

Install Termux from F-Droid:

https://f-droid.org/packages/com.termux/

Update Termux:

```bash
pkg update && pkg upgrade -y
```

Install basic tools:

```bash
pkg install git wget curl proot-distro -y
```

Grant storage access:

```bash
termux-setup-storage
```

---

## Step 2 - Install Debian

Install Debian:

```bash
proot-distro install debian
```

Login to Debian:

```bash
proot-distro login debian
```

Update packages:

```bash
apt update && apt upgrade -y
```

---

## Step 3 - Install XFCE Desktop

Install XFCE:

```bash
apt install xfce4 xfce4-goodies -y
```

Install required packages:

```bash
apt install \
python3 \
python3-tk \
iproute2 \
net-tools \
bluetooth \
git \
-y
```

---

## Step 4 - Configure Graphical Environment

You must have a working graphical session.

Common methods:

- Termux:X11
- VNC Server

Verify that XFCE starts correctly before continuing.

---

## Step 5 - Verify Required Components

Check Python:

```bash
python3 --version
```

Check networking tools:

```bash
which ip
```

Check Tkinter:

```bash
python3 -c "import tkinter"
```

If any command fails, fix it before installing XFCE Connection Centre.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Cnvalvi/XFCE-Connection-Center.git
```

Enter the project directory:

```bash
cd XFCE-Connection-Center
```

Make installer executable:

```bash
chmod +x install.sh
```

Run installer:

```bash
./install.sh
```

After installation, launch:

```text
XFCE Connection Centre
```

from the XFCE Applications Menu.

---

# Test Before Installing

You can test the application without installing it.

Run:

```bash
python3 connection_centre.py
```

If the application window opens successfully, installation should work normally.

---

# Running Without Installation

Direct execution:

```bash
python3 connection_centre.py
```

---

# Required Dependencies

The application requires:

```text
python3
python3-tk
iproute2
```

Recommended:

```text
net-tools
bluetooth
```

---

# Dependency Verification

The installer checks:

```text
python3
tkinter
ip command
required project files
```

If something is missing, installation stops and displays an error message.

---

# Troubleshooting

## tkinter Module Not Found

Install:

```bash
apt install python3-tk -y
```

---

## ip Command Not Found

Install:

```bash
apt install iproute2 -y
```

---

## ifconfig Command Not Found

Install:

```bash
apt install net-tools -y
```

---

## Bluetooth Information Not Available

Install:

```bash
apt install bluetooth -y
```

Note that some Android devices do not expose Bluetooth information inside Proot environments.

---

## Application Opens But Information Is Missing

Check:

```bash
which ip
which ifconfig
which bluetoothctl
```

Some devices restrict access to connectivity information.

---

## No Graphical Display

Make sure:

- XFCE is running
- Termux:X11 is running, or
- VNC is running

This application requires a graphical desktop environment.

---

## Android Features Behave Differently

Android integration depends on:

- Android version
- Device manufacturer
- Available commands
- Application permissions

Different devices may provide different results.

---

# Uninstallation

Make uninstaller executable:

```bash
chmod +x uninstall.sh
```

Run:

```bash
./uninstall.sh
```

This removes:

- Application files
- Desktop launcher

This does NOT remove:

- Termux
- Debian
- Ubuntu
- Proot
- XFCE
- VNC
- The cloned repository directory

---

# Project Structure

```text
XFCE-Connection-Center
├── connection_centre.py
├── install.sh
├── uninstall.sh
├── launch.sh
├── xfce-connection-centre.desktop
├── icon.svg
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

# Known Limitations

- Designed primarily for Android + Linux desktop environments.
- Some functionality depends on available system commands.
- Bluetooth detection may not work on all devices.
- Android manufacturers may restrict access to certain information.
- Results can vary between devices and Android versions.

---

# Roadmap

- [ ] Dark Mode
- [ ] Battery Status
- [ ] VPN Detection
- [ ] Mobile Data Detection
- [ ] Network Usage Statistics
- [ ] Improved Error Reporting
- [ ] Better Android Integration
- [ ] Theme Support

---

# Contributing

Contributions, bug reports and suggestions are welcome.

Steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push your branch
6. Open a Pull Request

---

# License

MIT License

See the LICENSE file for full details.

---

# Author

**Cnvalvi**

GitHub:
https://github.com/Cnvalvi
