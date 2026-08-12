# pyscan : ver 0.04 (async!)

import asyncio
import socket
import sys


async def scan_port(target_host, port, timeout=1.0):
    """Scan a single port asynchronously (IPv4 only)."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(target_host, port, family=socket.AF_INET),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        print(f"Port {port} is open.")
        return port
     
    except asyncio.TimeoutError:
        return None
    except OSError as e:
        if e.errno == 111:  # Connection refused = closed port
            return None
        print(f"\n[-] Network error on port {port}: {e}")
        return None


async def run_scan(target_host="127.0.0.1", start_port=1, end_port=1024, max_workers=100):
    """Run asynchronous port scan with concurrency limit."""
    start_port, end_port = max(1, start_port), min(65535, end_port)
    
    if start_port > end_port:
        print("[x] Port range invalid!")
        return []
    
    semaphore = asyncio.Semaphore(max_workers)
    
    async def scan_with_semaphore(port):
        async with semaphore:
            return await scan_port(target_host, port)
    
    tasks = [scan_with_semaphore(port) for port in range(start_port, end_port + 1)]
    results = await asyncio.gather(*tasks)
    
    return [port for port in results if port is not None]


async def main():
    target_host = input("Enter Host IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
    start_in = input("Enter starting port (default: 1): ").strip()
    end_in = input("Enter ending port (default: 1024): ").strip()

    start_port = int(start_in) if start_in else 1
    end_port = int(end_in) if end_in else 1024

    print(f"\n[*] Started TCP scan for host: {target_host}")
    print(f"[*] Scanning ports {start_port} to {end_port}...")


    try:
        open_ports = await run_scan(target_host, start_port, end_port)
        print(f"[*] Scan Completed. Found {len(open_ports)} open ports: {open_ports}")
    except OSError:
        print("\n[-] Couldn't resolve hostname.")
    except KeyboardInterrupt:
        print("\n[-] Scan terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())