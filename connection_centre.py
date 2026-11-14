#!/usr/bin/env python3
# XFCE Connection Centre
# Android / Termux / Proot - Tab device only

import json
import os
import re
import shutil
import subprocess
import threading
import queue
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


APP_TITLE = "XFCE Connection Centre"

BG = "#111827"
CARD = "#1f2937"
CARD2 = "#263449"
TEXT = "#f9fafb"
MUTED = "#aab6c5"
GREEN = "#22c55e"
YELLOW = "#facc15"
BLUE = "#60a5fa"
RED = "#f87171"

COMMAND_PATHS = {
    "am": ["/system/bin/am"],
    "settings": ["/system/bin/settings"],
    "ip": ["/usr/sbin/ip", "/sbin/ip"],
    "ifconfig": ["/usr/sbin/ifconfig", "/sbin/ifconfig"],
    "bluetoothctl": ["/usr/bin/bluetoothctl", "/usr/local/bin/bluetoothctl"],
    "termux-wifi-connectioninfo": [
        "/data/data/com.termux/files/usr/bin/termux-wifi-connectioninfo"
    ],
}


def find_command(name):
    found = shutil.which(name)
    if found:
        return found

    for path in COMMAND_PATHS.get(name, []):
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def run_command(command, timeout=4):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    except subprocess.TimeoutExpired:
        return 124, "", "Command timed out"

    except Exception as exc:
        return 1, "", str(exc)


def concise_error(error):
    if not error:
        return "Information unavailable"

    error = error.replace("\n", " ").strip()

    if "SecurityException" in error or "Permission Denial" in error:
        return "Android permission restricted"

    if "not found" in error.lower():
        return "Required command unavailable"

    if "timed out" in error.lower():
        return "System response timed out"

    return error[:100]


def read_android_setting(key):
    command = find_command("settings")

    if not command:
        return None, "Android settings command unavailable"

    rc, out, err = run_command(
        [command, "get", "global", key],
        timeout=3
    )

    if rc == 0 and out in ("0", "1"):
        return out == "1", None

    return None, concise_error(err or out)


def read_interfaces():
    interfaces = {}
    ip_cmd = find_command("ip")

    if ip_cmd:
        rc, out, _ = run_command([ip_cmd, "-o", "link", "show"])

        if rc == 0:
            for line in out.splitlines():
                match = re.match(r"\s*\d+:\s+([^:@]+)", line)

                if match:
                    name = match.group(1)
                    interfaces[name] = {
                        "name": name,
                        "up": "UP" in line,
                        "ip": ""
                    }

            rc, addr_out, _ = run_command(
                [ip_cmd, "-o", "-4", "addr", "show"]
            )

            if rc == 0:
                for line in addr_out.splitlines():
                    match = re.search(
                        r"^\s*\d+:\s+([^ ]+).*?\binet\s+([0-9.]+)",
                        line
                    )

                    if match:
                        name = match.group(1).split("@")[0]
                        if name in interfaces:
                            interfaces[name]["ip"] = match.group(2)

    if not interfaces:
        ifconfig = find_command("ifconfig")

        if ifconfig:
            rc, out, _ = run_command([ifconfig, "-a"])

            if rc == 0:
                current = None

                for line in out.splitlines():
                    if line and not line[0].isspace():
                        match = re.match(r"^([a-zA-Z0-9_.:-]+)", line)
                        if match:
                            current = match.group(1).rstrip(":")
                            interfaces[current] = {
                                "name": current,
                                "up": "UP" in line,
                                "ip": ""
                            }

                    if current and "inet " in line:
                        match = re.search(
                            r"\binet(?: addr:)?\s*([0-9.]+)",
                            line
                        )
                        if match:
                            interfaces[current]["ip"] = match.group(1)

    return interfaces


def is_wifi(name):
    name = name.lower()
    return (
        name.startswith(("wlan", "wifi", "wl", "wlp"))
        or os.path.exists(f"/sys/class/net/{name}/wireless")
    )


def is_ethernet(name):
    name = name.lower()
    return name.startswith(
        ("eth", "enp", "eno", "ens", "enx", "usb")
    )


def read_wifi(interfaces):
    api = find_command("termux-wifi-connectioninfo")
    info = {}

    if api:
        rc, out, err = run_command([api], timeout=5)

        if rc == 0 and out:
            try:
                info = json.loads(out)
            except (json.JSONDecodeError, TypeError):
                info = {}

    wifi_interfaces = [
        item for name, item in interfaces.items()
        if is_wifi(name)
    ]

    connected = any(
        item["up"] or item["ip"]
        for item in wifi_interfaces
    )

    ssid = info.get("ssid")
    if ssid and str(ssid).lower() not in ("<unknown ssid>", "unknown", "null"):
        ssid_text = str(ssid).strip('"')
    elif connected:
        ssid_text = "Connected - SSID hidden by Android"
    else:
        ssid_text = "Not connected / information unavailable"

    ip_address = info.get("ip", "")

    if not ip_address:
        for item in wifi_interfaces:
            if item["ip"]:
                ip_address = item["ip"]
                break

    rssi = info.get("rssi")
    signal = f"{rssi} dBm" if isinstance(rssi, (int, float)) else "Unavailable"

    if connected:
        status = "Connected"
        color = GREEN
    else:
        status = "Not connected or restricted"
        color = YELLOW

    details = (
        f"Network: {ssid_text}\n"
        f"IP address: {ip_address or 'Unavailable'}\n"
        f"Signal: {signal}"
    )

    return status, details, color


def read_ethernet(interfaces):
    wired = [
        item for name, item in interfaces.items()
        if is_ethernet(name)
    ]

    if not wired:
        if not find_command("ip") and not find_command("ifconfig"):
            return (
                "Information unavailable",
                "Install iproute2 or net-tools to inspect interfaces.",
                YELLOW
            )

        return (
            "No Ethernet interface detected",
            "No wired Ethernet interface is visible to Linux.",
            MUTED
        )

    lines = []

    for item in wired:
        state = "UP" if item["up"] else "DOWN"
        address = item["ip"] or "No IPv4 address"
        lines.append(f"{item['name']}: {state}\nIP: {address}")

    connected = any(item["up"] and item["ip"] for item in wired)

    return (
        "Connected" if connected else "Interface detected",
        "\n".join(lines),
        GREEN if connected else YELLOW
    )


def read_bluetooth():
    setting, error = read_android_setting("bluetooth_on")

    if setting is True:
        radio = "ON"
        color = GREEN
    elif setting is False:
        radio = "OFF"
        color = MUTED
    else:
        radio = "State unavailable"
        color = YELLOW

    # BlueZ support is optional. Android Proot normally
    # does not expose its Bluetooth stack to bluetoothctl.
    btctl = find_command("bluetoothctl")
    device_names = []

    if btctl:
        rc, out, _ = run_command(
            [btctl, "devices", "Connected"],
            timeout=3
        )

        if rc == 0:
            for line in out.splitlines():
                match = re.match(
                    r"Device\s+[0-9A-Fa-f:]+\s+(.+)",
                    line.strip()
                )
                if match:
                    device_names.append(match.group(1))

    if device_names:
        devices = "\n".join(device_names)
    else:
        devices = (
            "Connected device names are not exposed to this Linux session.\n"
            "Open Bluetooth Settings to view paired/connected devices."
        )

    details = f"Bluetooth: {radio}\n\n{devices}"

    if error and setting is None:
        details += f"\n\nReason: {error}"

    return radio, details, color


def read_airplane():
    setting, error = read_android_setting("airplane_mode_on")

    if setting is True:
        return "ON", "Airplane Mode is enabled.", YELLOW

    if setting is False:
        return "OFF", "Airplane Mode is disabled.", GREEN

    return (
        "State unavailable",
        f"Android did not expose the state.\nReason: {error}",
        YELLOW
    )


def collect_status():
    interfaces = read_interfaces()

    wifi = read_wifi(interfaces)
    ethernet = read_ethernet(interfaces)
    bluetooth = read_bluetooth()
    airplane = read_airplane()

    return {
        "wifi": wifi,
        "ethernet": ethernet,
        "bluetooth": bluetooth,
        "airplane": airplane,
        "time": datetime.now().strftime("%d-%m-%Y  %I:%M:%S %p")
    }


class ConnectionCentre:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("760x650")
        self.root.minsize(600, 550)
        self.root.configure(bg=BG)

        self.result_queue = queue.Queue()
        self.refreshing = False

        self.build_ui()
        self.refresh()
        self.root.after(200, self.process_queue)

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=20, pady=(18, 8))

        tk.Label(
            header,
            text="Connection Centre",
            font=("Arial", 22, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Tab A11 • Linux connectivity dashboard",
            font=("Arial", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 0))

        self.grid_frame = tk.Frame(self.root, bg=BG)
        self.grid_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.cards = {}

        self.create_card(
            "wifi",
            "Wi-Fi",
            "Wireless network"
        )

        self.create_card(
            "bluetooth",
            "Bluetooth",
            "Bluetooth radio and devices"
        )

        self.create_card(
            "ethernet",
            "Ethernet",
            "Wired network interfaces"
        )

        self.create_card(
            "airplane",
            "Airplane Mode",
            "Wireless radio mode"
        )

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=20, pady=(0, 15))

        self.refresh_button = tk.Button(
            footer,
            text="Refresh Status",
            command=self.refresh,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=9,
            font=("Arial", 10, "bold")
        )
        self.refresh_button.pack(side="left")

        self.last_update = tk.Label(
            footer,
            text="Last update: Waiting...",
            bg=BG,
            fg=MUTED,
            font=("Arial", 9)
        )
        self.last_update.pack(side="right")

    def create_card(self, key, title, subtitle):
        row = 0 if key in ("wifi", "ethernet") else 1
        column = 0 if key in ("wifi", "bluetooth") else 1

        frame = tk.Frame(
            self.grid_frame,
            bg=CARD,
            highlightthickness=1,
            highlightbackground="#374151"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=7,
            pady=7
        )

        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(1, weight=1)
        self.grid_frame.grid_rowconfigure(0, weight=1)
        self.grid_frame.grid_rowconfigure(1, weight=1)

        tk.Label(
            frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", padx=15, pady=(14, 2))

        tk.Label(
            frame,
            text=subtitle,
            font=("Arial", 9),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", padx=15)

        status = tk.Label(
            frame,
            text="Checking...",
            font=("Arial", 12, "bold"),
            bg=CARD,
            fg=YELLOW
        )
        status.pack(anchor="w", padx=15, pady=(12, 5))

        details = tk.Label(
            frame,
            text="Reading device information...",
            font=("Arial", 9),
            bg=CARD,
            fg=MUTED,
            justify="left",
            anchor="w",
            wraplength=300
        )
        details.pack(
            fill="both",
            expand=True,
            anchor="w",
            padx=15,
            pady=(0, 8)
        )

        button = tk.Button(
            frame,
            text="Open Settings",
            command=lambda k=key: self.open_settings(k),
            bg=CARD2,
            fg=TEXT,
            activebackground="#334155",
            activeforeground=TEXT,
            relief="flat",
            padx=12,
            pady=7
        )
        button.pack(anchor="w", padx=15, pady=(0, 14))

        self.cards[key] = {
            "status": status,
            "details": details
        }

    def open_settings(self, key):
        actions = {
            "wifi": [
                "android.settings.WIFI_SETTINGS",
                "android.settings.WIRELESS_SETTINGS"
            ],
            "bluetooth": [
                "android.settings.BLUETOOTH_SETTINGS",
                "android.settings.SETTINGS"
            ],
            "ethernet": [
                "android.settings.ETHERNET_SETTINGS",
                "android.settings.WIRELESS_SETTINGS",
                "android.settings.SETTINGS"
            ],
            "airplane": [
                "android.settings.AIRPLANE_MODE_SETTINGS",
                "android.settings.WIRELESS_SETTINGS",
                "android.settings.SETTINGS"
            ]
        }

        am = find_command("am")

        if not am:
            messagebox.showerror(
                "Settings",
                "Android Activity Manager (am) command is unavailable."
            )
            return

        for action in actions.get(key, []):
            rc, out, err = run_command(
                [am, "start", "-a", action],
                timeout=5
            )

            output = (out + " " + err).lower()

            if rc == 0 and "error:" not in output:
                return

        messagebox.showwarning(
            "Settings",
            "Android Settings could not be opened."
        )

    def refresh(self):
        if self.refreshing:
            return

        self.refreshing = True
        self.refresh_button.config(state="disabled")
        self.last_update.config(text="Refreshing...")

        worker = threading.Thread(
            target=self.refresh_worker,
            daemon=True
        )
        worker.start()

    def refresh_worker(self):
        try:
            result = collect_status()
            self.result_queue.put(("success", result))
        except Exception as exc:
            self.result_queue.put(("error", str(exc)))

    def process_queue(self):
        try:
            while True:
                kind, result = self.result_queue.get_nowait()

                self.refreshing = False
                self.refresh_button.config(state="normal")

                if kind == "success":
                    self.update_cards(result)
                else:
                    self.last_update.config(
                        text="Refresh error: " + concise_error(result)
                    )

        except queue.Empty:
            pass

        self.root.after(200, self.process_queue)

    def update_cards(self, result):
        for key in ("wifi", "bluetooth", "ethernet", "airplane"):
            status, details, color = result[key]

            self.cards[key]["status"].config(
                text=status,
                fg=color
            )

            self.cards[key]["details"].config(
                text=details
            )

        self.last_update.config(
            text="Last update: " + result["time"]
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectionCentre(root)
    root.mainloop()
