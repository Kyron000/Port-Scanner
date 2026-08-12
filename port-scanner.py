# WHEN ABUSING SYSTEM. OWNER IS NOT RESPONSIBLE FOR ANY ILLEGAL ACTIONS

import socket
import json
import urllib.request
import concurrent.futures
import threading
import sys
import os
import time

WATERMARK = "PORT-SCANNER | BY KYRON"

class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 1433: "MSSQL", 1521: "Oracle", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}

def print_banner():
    # Stel de titel van het Windows Terminal tabblad in
    sys.stdout.write("\x1b]0;PORT-SCANNER | BY KYRON\x07")
    sys.stdout.flush()

    os.system('cls' if os.name == 'nt' else 'clear')
    
    ascii_lines = [
        "██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ",
        "██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗",
        "██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝",
        "██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗",
        "██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║",
        "╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
    ]
    
    banner_width = len(ascii_lines[0])
    
    def render_ascii():
        print("\n")
        for line in ascii_lines:
            colored_line = ""
            for i, char in enumerate(line):
                r = int(17 + (0 - 17) * (i / banner_width))
                g = int(85 + (255 - 85) * (i / banner_width))
                b = int(204 + (255 - 204) * (i / banner_width))
                colored_line += f"\033[38;2;{r};{g};{b}m{char}"
            print(colored_line + Color.RESET)
            
        print(f"\n{Color.CYAN}{Color.BOLD}{'Made by Kyron':^{banner_width}}{Color.RESET}\n")

    render_ascii()

    # --- DISCLAIMER & WARNING ---
    print("=" * banner_width)
    print(f"{Color.RED}{Color.BOLD} WARNING & LEGAL DISCLAIMER:{Color.RESET}")
    print(" This tool is strictly intended for educational purposes and authorized network")
    print(" audits. Scanning target infrastructure without explicit, prior written permission")
    print(" from the system owner is illegal and unethical.")
    print(" Abuse of network scanning tools may lead to severe legal penalties.")
    print("=" * banner_width)
    
    confirm = input(f"\n{Color.BOLD}Do you agree to these terms? (y/n): {Color.RESET}").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print(f"\n{Color.RED}[!] Usage declined. Exiting program.{Color.RESET}")
        sys.exit(0)
        
    print(f"\n{Color.BLUE}[*] Terms accepted. Loading scanner...{Color.RESET}", end="", flush=True)
    time.sleep(1.0)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    render_ascii()

def probe_port(ip, port, open_ports, lock):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            if s.connect_ex((ip, port)) == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                with lock:
                    open_ports.append((port, service))
                    print(f" {Color.GREEN}[+] OPEN:{Color.RESET} Port {Color.BOLD}{port:<5}{Color.RESET} ({service})")
    except Exception:
        pass

def send_webhook(url, target, open_ports):
    print(f"\n{Color.BLUE}[*] Sending webhook report...{Color.RESET}")
    
    sorted_ports = sorted(open_ports, key=lambda x: x[0])
    formatted_ports = [f"• **Port {port}**: {service}" for port, service in sorted_ports]
    
    payload = {
        "embeds": [{
            "title": "Port Scan Results",
            "color": 3066993,
            "fields": [
                {"name": "Target Host/IP", "value": f"`{target}`", "inline": True},
                {"name": "Open Ports Found", "value": f"`{len(open_ports)}`", "inline": True},
                {"name": "Details", "value": "\n".join(formatted_ports) if formatted_ports else "None", "inline": False}
            ],
            "footer": {
                "text": WATERMARK
            }
        }]
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "PortScanner/3.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status in (200, 204):
                print(f"{Color.GREEN}[+] Webhook delivered successfully.{Color.RESET}")
            else:
                print(f"{Color.RED}[!] Webhook failed (HTTP {resp.status}).{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[!] Error sending webhook: {e}{Color.RESET}")

def main():
    print_banner()

    target = input(f"{Color.BOLD}[?] Target Host / IP: {Color.RESET}").strip()
    if not target:
        print(f"{Color.RED}[!] Target cannot be empty.{Color.RESET}")
        sys.exit(1)

    print(f"\n{Color.BOLD}Select Scan Mode:{Color.RESET}")
    print(" [1] Quick Scan (Top common ports)")
    print(" [2] Custom Range (Custom port range)")
    
    mode = input("\nSelect option [1 Recommended]: ").strip()
    
    ports_to_scan = []
    if mode == "2":
        try:
            start_p = int(input("Start port (1-65535): ").strip())
            end_p = int(input("End port (1-65535): ").strip())
            if not (0 < start_p <= end_p <= 65535):
                raise ValueError
            ports_to_scan = list(range(start_p, end_p + 1))
        except ValueError:
            print(f"{Color.RED}[!] Invalid port range specified.{Color.RESET}")
            sys.exit(1)
    else:
        ports_to_scan = list(COMMON_PORTS.keys())

    webhook = input(f"\n{Color.BOLD}Webhook URL (Optional, press Enter to skip): {Color.RESET}").strip()

    print(f"\n{Color.BLUE}[*] Resolving target IP...{Color.RESET}")
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{Color.BLUE}[*] Target IP: {target_ip}{Color.RESET}")
        print(f"{Color.BLUE}[*] Total ports to scan: {len(ports_to_scan)}{Color.RESET}")
        print("─" * 55)
    except socket.gaierror:
        print(f"{Color.RED}[!] Error: Could not resolve hostname '{target}'.{Color.RESET}")
        sys.exit(1)

    open_ports = []
    lock = threading.Lock()

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(probe_port, target_ip, port, open_ports, lock) for port in ports_to_scan]
            concurrent.futures.wait(futures)
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[!] Scan aborted by user.{Color.RESET}")
        sys.exit(0)

    print("─" * 55)
    if open_ports:
        print(f"{Color.BOLD}{Color.GREEN}[*] Scan finished! {len(open_ports)} open port(s) found.{Color.RESET}")
        if webhook:
            send_webhook(webhook, target, open_ports)
    else:
        print(f"{Color.BOLD}{Color.YELLOW}[*] Scan finished. No open ports detected.{Color.RESET}")

if __name__ == "__main__":
    main()

# WHEN ABUSING SYSTEM. OWNER IS NOT RESPONSIBLE FOR ANY ILLEGAL ACTIONS
