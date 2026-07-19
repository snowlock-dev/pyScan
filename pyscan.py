# pyscan : ver 0.01

import socket
import sys

target_host = input("Enter Host IP (default: 127.0.0.1):").strip()

if not target_host:
    target_host = "127.0.0.1"

start_in = input("Enter starting port (default: 1):").strip()
end_in = input("Enter starting port (default: 1024):").strip()

start_port = int(start_in) if start_in else 1
end_port   = int(end_in) if end_in else 1024


print(f"[*] Started TCP scan for host: {target_host}")
print(f"[*] Scanning ports {start_port} to {end_port}...")


try:
    for port in range(start_port, end_port + 1):
        
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(1)
        result = soc.connect_ex((target_host, port))
        
        if result == 0:
            print(f"Port {port} is open.")
        
        soc.close()

except socket.gaierror:
    print("\n[-] Couldn't resolve hostname.")
        
except KeyboardInterrupt:
    print("\n[-] Scan terminated by user.")
    sys.exit()

except socket.error:
    print("\n[-] Could not connect to server.")
    sys.exit()
