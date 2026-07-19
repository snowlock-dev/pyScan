# pyscan : ver 0.01

import socket

target_host = "127.0.0.1"
target_port = 80

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.settimeout(2)

result = soc.connect_ex((target_host, target_port))

if result == 0:
    print(f"Port is open.")
else:
    print(f"Port is closed.")