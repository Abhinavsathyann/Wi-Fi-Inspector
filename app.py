import platform
import subprocess
import re
import socket
import psutil
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def run_cmd(cmd):
    """Run a shell command and return stdout (str)."""
    try:
        completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True, timeout=3)
        return completed.stdout.strip()
    except Exception:
        # Try shell=True fallback for some systems if needed
        try:
            completed = subprocess.run(" ".join(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, timeout=3)
            return completed.stdout.strip()
        except Exception:
            return ""

def get_windows_wifi():
    out = run_cmd(["netsh", "wlan", "show", "interfaces"])
    info = {}
    if not out:
        return info
    # parse lines like:    SSID                   : MyNetwork
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip().lower()
            v = v.strip()
            if k == "ssid":
                info["ssid"] = v
            elif k == "bssid":
                info["bssid"] = v
            elif k == "signal":
                info["signal"] = v
            elif k == "radio type":
                info["radio_type"] = v
            elif k == "authentication":
                info["authentication"] = v
            elif k == "cipher":
                info["cipher"] = v
            elif k == "channel":
                info["channel"] = v
    return info

def get_macos_wifi():
    # macOS airport utility path
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    out = run_cmd([airport, "-I"]) if psutil.os.name != 'nt' else ""
    info = {}
    if not out:
        return info
    # sample lines:     SSID: MyNetwork
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip().lower()
            v = v.strip()
            if k == "ssid":
                info["ssid"] = v
            elif k == "agrctlrssi" or k == "rssi":
                info["rssi"] = v
            elif k == "agrctlnoise" or k == "noise":
                info["noise"] = v
            elif k == "channel":
                info["channel"] = v
            elif k == "bssid":
                info["bssid"] = v
            elif k == "country":
                info["country"] = v
    return info

def get_linux_wifi():
    # Prefer nmcli if available
    info = {}
    nmcli_out = run_cmd(["nmcli", "-t", "-f", "ACTIVE,SSID,BSSID,CHAN,FREQ,SIGNAL,SECURITY", "dev", "wifi"])
    if nmcli_out:
        # find the ACTIVE:yes line
        for line in nmcli_out.splitlines():
            parts = line.split(":")
            if len(parts) >= 7 and parts[0] == "yes":
                info["ssid"] = parts[1]
                info["bssid"] = parts[2]
                info["channel"] = parts[3]
                info["freq"] = parts[4]
                info["signal"] = parts[5] + "%"
                info["security"] = parts[6]
                return info
    # fallback to iwgetid + iwconfig
    ssid = run_cmd(["iwgetid", "-r"])
    if ssid:
        info["ssid"] = ssid
    iwcfg = run_cmd(["iwconfig"])
    if iwcfg:
        # try to get wlan0 or first wireless interface block
        m = re.search(r'(\w+)\s+IEEE', iwcfg)
        if m:
            iface = m.group(1)
            # extract ESSID and Access Point and Signal level
            essid_m = re.search(r'ESSID:"([^"]+)"', iwcfg)
            if essid_m:
                info["ssid"] = essid_m.group(1)
            ap_m = re.search(r'Access Point: ([0-9A-Fa-f:]{17})', iwcfg)
            if ap_m:
                info["bssid"] = ap_m.group(1)
            sig_m = re.search(r'Signal level[=|:]\s*([-0-9]+)', iwcfg)
            if sig_m:
                info["signal"] = sig_m.group(1)
    return info

def get_basic_network_info():
    # IP addresses, gateway isn't trivial cross-platform without extra packages; do best-effort
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    # find likely active interface (non-loopback, up)
    chosen = None
    for IF, s in stats.items():
        if not s.isup: 
            continue
        if IF.lower().startswith("lo") or IF == "Loopback Pseudo-Interface 1":
            continue
        # pick first non-loopback up interface
        chosen = IF
        break
    data = {"interface": chosen}
    if chosen:
        iface_addrs = addrs.get(chosen, [])
        ipv4 = None
        mac = None
        for a in iface_addrs:
            if a.family == socket.AF_INET:
                ipv4 = a.address
            elif getattr(psutil, "AF_LINK", None) and a.family == psutil.AF_LINK:
                mac = a.address
            elif a.family == getattr(socket, 'AF_PACKET', None):
                mac = a.address
        data["ipv4"] = ipv4
        data["mac"] = mac
    # also include hostname
    try:
        data["hostname"] = socket.gethostname()
    except Exception:
        data["hostname"] = None
    return data

def gather_all():
    osname = platform.system().lower()
    wifi = {}
    if "windows" in osname:
        wifi = get_windows_wifi()
    elif "darwin" in osname or "mac" in osname:
        wifi = get_macos_wifi()
    elif "linux" in osname:
        wifi = get_linux_wifi()
    else:
        wifi = {}
    basic = get_basic_network_info()
    combined = {"os": osname, "wifi": wifi, "basic": basic}
    return combined

@app.route("/api/json")
def api_json():
    return jsonify(gather_all())

@app.route("/")
def index():
    data = gather_all()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
