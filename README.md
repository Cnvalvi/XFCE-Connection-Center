# XFCE Connection Centre

A lightweight Android and Linux connectivity dashboard built with Python and Tkinter.

Designed for Android tablets running Linux desktop environments through Termux and Proot.

## Features

- **Wi-Fi:** Displays wireless network status and available connection information.
- **Bluetooth:** Displays Bluetooth radio and device information when available.
- **Ethernet:** Detects wired network interfaces.
- **Airplane Mode:** Displays airplane mode status when Android settings access is available.
- **Open Settings:** Opens the corresponding Android settings screen.
- **Refresh Status:** Updates all connectivity information.
- **Last Update:** Displays the most recent status refresh time.
- **Background Refresh:** Collects status information in a background thread to keep the GUI responsive.

## Screenshots

Screenshots will be added in a future release.

## Requirements

- Python 3
- Tkinter
- Linux desktop environment with an active graphical display (X11)
- Android / Termux / Proot environment
- Android Activity Manager (`am`) for opening Android settings

Optional system utilities:

- `ip` or `ifconfig`
- `bluetoothctl`
- `termux-wifi-connectioninfo`
- Android `settings` command

No third-party Python packages are currently required.

## Installation

Clone the repository:

```bash
git clone git@github.com:Cnvalvi/XFCE-Connection-Center.git
```

Enter the project directory:

```bash
cd XFCE-Connection-Center
```

Install Tkinter if it is missing (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install python3 python3-tk
```

Run the application:

```bash
python3 connection_centre.py
```

Make sure your Linux graphical environment and DISPLAY are available before launching the application.

## How It Works

The application uses Python standard libraries, Linux network interfaces and available Android system commands to collect connectivity information.

Android system access depends on the permissions and capabilities available in the Termux/Proot environment.

The Open Settings buttons launch Android settings activities when the Android Activity Manager is accessible.

This application monitors connectivity status. It does not directly enable or disable Wi-Fi, Bluetooth or airplane mode.

## Project Structure

```text
XFCE-Connection-Center/
├── connection_centre.py
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt
```

## Platform

Developed and tested in an Android tablet Linux desktop environment.

Hardware and software compatibility may vary across devices and Android versions.

## Developer

**Cnvalvi**

GitHub: https://github.com/Cnvalvi

## License

This project is licensed under the MIT License.
See the LICENSE file for details.
