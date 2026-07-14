import os
import shutil
import sqlite3
import time
import winreg
import subprocess
import pandas as pd
import platform
import socket

def get_chrome_history():
    data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    if os.path.exists(data_path):
        try:
            temp_history = "temp_chrome_history"
            shutil.copyfile(data_path, temp_history)
            conn = sqlite3.connect(temp_history)
            cursor = conn.cursor()
            query = """
            SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime'), url, title, visit_count 
            FROM urls 
            ORDER BY last_visit_time DESC 
            LIMIT 50;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            if os.path.exists(temp_history):
                os.remove(temp_history)
            df = pd.DataFrame(rows, columns=['Timestamp', 'URL', 'Title', 'Visit Count'])
            return df
        except Exception as e:
            return pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
    return pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])

def get_recent_files():
    recent_path = os.path.expanduser('~') + r"\AppData\Roaming\Microsoft\Windows\Recent"
    if os.path.exists(recent_path):
        try:
            files_list = []
            for file in os.listdir(recent_path):
                if file.endswith(".lnk"):
                    full_path = os.path.join(recent_path, file)
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(full_path)))
                    clean_name = file.replace(".lnk", "")
                    files_list.append([timestamp, "Recent File Logs", clean_name, "-"])
            df = pd.DataFrame(files_list, columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
            df = df.sort_values(by='Timestamp', ascending=False).head(30)
            return df
        except Exception as e:
            return pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
    return pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])

def get_usb_logs():
    try:
        usb_list = []
        registry_path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            device_name = winreg.EnumKey(key, i)
            timestamp = "Artifact Logged" 
            clean_device = device_name.replace("Disk&Ven_", "").split("&")[0]
            usb_list.append([timestamp, "USB Registry Logs", f"Connected Device: {clean_device}", "-"])
        winreg.CloseKey(key)
        df = pd.DataFrame(usb_list, columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
        return df.head(15)
    except Exception as e:
        return pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])

def get_wifi_logs():
    try:
        wifi_list = []
        cmd = subprocess.run(
            ["netsh", "wlan", "show", "profiles"], 
            capture_output=True, 
            text=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if cmd.returncode == 0:
            for line in cmd.stdout.split('\n'):
                if "All User Profile" in line:
                    wifi_name = line.split(":")[1].strip()
                    wifi_list.append(["Artifact Logged", "Wi-Fi Network Logs", f"Saved SSID: {wifi_name}", "-"])
        df = pd.DataFrame(wifi_list, columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])
        return df.head(15)
    except Exception as e:
        return pd.DataFrame(columns=['Timestamp', 'Artifact Source', 'Details / Value', 'Visit Count'])

def get_system_metadata():
    try:
        # Operating system basic specifications
        os_name = platform.system() or "Windows"
        os_release = platform.release() or "N/A"
        os_version = platform.version() or "N/A"
        if len(os_version) > 30:
            os_version = os_version[:30] + "..."
            
        hostname = socket.gethostname() or "Local Machine"
        
        raw_processor = platform.processor() or "Intel/AMD Processor"
        if len(raw_processor) > 40:
            processor = raw_processor[:40] + "..."
        else:
            processor = raw_processor
            
        try:
            ip_addr = socket.gethostbyname(hostname)
        except:
            ip_addr = "127.0.0.1"
            
        return {
            "OS": os_name,
            "OS Release": os_release,
            "OS Version": os_version,
            "Hostname": hostname,
            "Processor": processor,
            "Local IP Address": ip_addr
        }
    except Exception:
        return {
            "OS": "Windows", 
            "OS Release": "10/11", 
            "OS Version": "Build N/A", 
            "Hostname": "Client-PC", 
            "Processor": "Multi-Core CPU", 
            "Local IP Address": "127.0.0.1"
        }