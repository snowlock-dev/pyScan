# pyscan : ver 0.01

import socket
import sys

target_host = "127.0.0.1"

start_port = 1
end_port = 1024

print(f"[*] Started TCP scan for host: {target_host}")
print(f"[*] Scannign ports {start_port} to {end_port}...")


try:
    for port in range(start_port, end_port + 1):
        
        soc = socket.socket(socket.AF_INET,         socket.SOCK_STREAM)
        
        soc.settimeout(2)
        
        result = soc.connect_ex((target_host,       port))
        
        if result == 0:
            print(f"Port {port} is open.")
        else:
            print(f"Port {port} is closed.")
        
        soc.close()
        
except KeyboardInterrupt:
    print("\n[-] Scan terminated by user.")
    sys.exit()

except socket.error:
    print("\n[-] Could not connect to server.")
    sys.exit()