# pyscan : ver 0.02

import socket
import sys
from concurrent.futures import ThreadPoolExecutor


def scan_port(target_host, port, timeout=1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.settimeout(timeout)
            result = soc.connect_ex((target_host, port))
            
            if result == 0:
                print(f"Port {port} is open.")
                return port
            return None  # Explicit return for closed ports
            
    except socket.error:
        print("\n[-] Could not connect to server.")
        return None  # Explicit return on error


def run_scan(target_host="127.0.0.1", start_port=1, end_port=1024, max_workers=100):
    start_port, end_port = max(1, start_port), min(65535, end_port)
    if start_port > end_port:
        print("[x] Port range invalid!")
        return []
    
    ports_to_scan = range (start_port, end_port + 1)
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda p: scan_port(target_host, p), ports_to_scan)

    for result in results:
        if result is not None:
            open_ports.append(result)

    return open_ports

def main():
    target_host = input("Enter Host IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
    start_in = input("Enter starting port (default: 1): ").strip()
    end_in = input("Enter ending port (default: 1024): ").strip()

    start_port = int(start_in) if start_in else 1
    end_port = int(end_in) if end_in else 1024

    print(f"\n[*] Started TCP scan for host: {target_host}")
    print(f"[*] Scanning ports {start_port} to {end_port}...")

    try:
        open_ports = run_scan(target_host, start_port, end_port)
        print(f"[*] Scan Completed. Found {len(open_ports)} open ports: {open_ports}")
    except socket.gaierror:
        print("\n[-] Couldn't resolve hostname.")
    except KeyboardInterrupt:
        print("\n[-] Scan terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
