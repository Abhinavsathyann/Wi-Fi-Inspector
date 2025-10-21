# 🌐 WiFi Details Web App (Python + Flask)

A modern, multi-page Flask web application that displays **your connected WiFi network details**, system information, and advanced diagnostics.  
Includes 10 stylish pages with responsive design and real-time data display.

---

## 🚀 Features

✅ Display **connected WiFi details** (SSID, BSSID, Signal Strength, Speed, Security, etc.)  
✅ Show **system & network info** (IP, MAC, OS, and uptime)  
✅ Live **bandwidth usage monitor**  
✅ **WiFi history logs** (stored locally)  
✅ **Ping test** & latency checker  
✅ **IP & Geolocation lookup**  
✅ **Network speed test** (via API)  
✅ **Modern UI/UX** with CSS animations  
✅ Built using **Flask**, **HTML5**, **Tailwind CSS**, and **JavaScript**

---

## 📁 Project Structure
wifi-details/

│

├── app.py # Main Flask server

├── templates/ # HTML files (10 pages)

│ ├── index.html

│ ├── wifi_details.html

│ ├── system_info.html

│ ├── bandwidth.html

│ ├── ping_test.html

│ ├── speed_test.html

│ ├── location.html

│ ├── history.html

│ ├── about.html

│ └── contact.html

│

├── static/ # Static assets (CSS, JS, images)

│ ├── css/

│ │ └── style.css

│ ├── js/

│ │ └── main.js

│ └── images/

│ └── background.svg
│
└── requirements.txt # All dependencies

---

## Requirements File Example (requirements.txt)
flask

psutil

requests

---

## 🖥️ Pages Overview
| Page                  | Description                                    |
| --------------------- | ---------------------------------------------- |
| **Home**              | Dashboard showing current WiFi status          |
| **WiFi Details**      | SSID, BSSID, signal, and security info         |
| **System Info**       | OS, CPU, memory, uptime, and network card info |
| **Bandwidth Monitor** | Real-time upload/download graph                |
| **Ping Test**         | Test latency for a given domain                |
| **Speed Test**        | Run download/upload speed test                 |
| **IP Location**       | Find your public IP and geolocation            |
| **History**           | View saved WiFi connection logs                |
| **About**             | App details and version info                   |
| **Contact**           | Contact form / feedback page                   |

---

## 🧩 Technologies Used

Backend: Flask (Python)

Frontend: HTML5, Tailwind CSS, JavaScript

Libraries: psutil, requests, socket, subprocess

Icons: Lucide / Font Awesome

---

## 🧠 Requirements

- Python 3.8 or above  
- pip (Python package manager)  
- Flask & other modules (see below)

---

## ⚡ License
This project is licensed under the MIT License — free to use, modify, and share.

---

## 💡 Tip
If you face ModuleNotFoundError like:

ModuleNotFoundError: No module named 'requests'
 
Just run:

pip install requests

---

## ⚙️ Installation

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/Abhinavsathyann/Wi-Fi-Inspector.git
   cd wifi-details

2. Create a virtual environment (optional but recommended):
 ```bash
python -m venv venv
venv\Scripts\activate        # Windows
# OR
source venv/bin/activate     # macOS/Linu

3. Install dependencies:
pip install -r requirements.txt

4.Run the app:
python app.py

5. Open your browser and go to:
http://127.0.0.1:5000

---
