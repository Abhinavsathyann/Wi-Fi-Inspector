import platform, psutil, socket, subprocess, json, os, time, requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------- Utility functions ----------

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, timeout=5)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_wifi_details():
    sysname = platform.system().lower()
    data = {}
    if "windows" in sysname:
        out = run_cmd("netsh wlan show interfaces")
        for line in out.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    elif "linux" in sysname:
        out = run_cmd("nmcli -t -f active,ssid,bssid,chan,rate,signal,security dev wifi")
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 7 and parts[0] == "yes":
                data = {
                    "SSID": parts[1],
                    "BSSID": parts[2],
                    "Channel": parts[3],
                    "Rate": parts[4],
                    "Signal": parts[5],
                    "Security": parts[6],
                }
    elif "darwin" in sysname:
        out = run_cmd("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
        for line in out.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data

def get_interfaces():
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    interfaces = []
    for name, stat in stats.items():
        interfaces.append({
            "name": name,
            "isup": stat.isup,
            "speed": stat.speed,
            "mtu": stat.mtu,
            "addresses": [a.address for a in addrs.get(name, []) if a.family == socket.AF_INET],
        })
    return interfaces

def get_system_info():
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Python": platform.python_version(),
        "Hostname": socket.gethostname(),
    }

def get_connected_devices():
    out = run_cmd("arp -a")
    return out.splitlines() if out else ["No devices found"]

def run_speedtest():
    try:
        out = run_cmd("speedtest-cli --json")
        return json.loads(out)
    except:
        return {"error": "speedtest-cli not found or failed"}

def ping_host(host):
    return run_cmd(f"ping -n 4 {host}" if platform.system() == "Windows" else f"ping -c 4 {host}")

def traceroute_host(host):
    cmd = "tracert" if platform.system() == "Windows" else "traceroute"
    return run_cmd(f"{cmd} {host}")

# ---------- Routes ----------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wifi")
def wifi():
    return render_template("wifi.html", data=get_wifi_details())

@app.route("/interfaces")
def interfaces():
    return render_template("interfaces.html", data=get_interfaces())

@app.route("/system")
def system():
    return render_template("system.html", data=get_system_info())

@app.route("/devices")
def devices():
    return render_template("devices.html", data=get_connected_devices())

@app.route("/speedtest")
def speedtest():
    return render_template("speedtest.html")

@app.route("/speedtest/run")
def speedtest_run():
    return jsonify(run_speedtest())

@app.route("/ping", methods=["GET", "POST"])
def ping():
    result = None
    if request.method == "POST":
        host = request.form.get("host")
        result = ping_host(host)
    return render_template("ping.html", result=result)

@app.route("/traceroute", methods=["GET", "POST"])
def traceroute():
    result = None
    if request.method == "POST":
        host = request.form.get("host")
        result = traceroute_host(host)
    return render_template("traceroute.html", result=result)

@app.route("/api")
def api():
    return render_template("api.html")

@app.route("/api/all")
def api_all():
    data = {
        "wifi": get_wifi_details(),
        "interfaces": get_interfaces(),
        "system": get_system_info(),
    }
    return jsonify(data)

@app.route("/about")
def about():
    return render_template("about.html")

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
