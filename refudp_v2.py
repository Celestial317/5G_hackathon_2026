import socket
import threading
import time

target_ip = "172.16.0.22"
target_port = 80 # The exposed web dashboard we found earlier
concurrent_connections = 150

print("="*60)
print(f"Initiating Final 5G Data-Plane Diagnostic")
print(f"Targeting: {target_ip}:{target_port} with {concurrent_connections} concurrent TCP connections")
print("="*60)

# Metrics trackers
results = {
    "successful": 0,
    "refused": 0,
    "firewall_dropped": 0,
    "errors": 0
}
sockets = []
lock = threading.Lock()

def connect_to_target():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        
        # Attempt connection
        result = sock.connect_ex((target_ip, target_port))
        
        with lock:
            if result == 0:
                results["successful"] += 1
                sockets.append(sock)
            elif result in [111, 10061]:
                results["refused"] += 1
            else:
                results["errors"] += 1
                
    except socket.timeout:
        with lock:
            results["firewall_dropped"] += 1
    except Exception:
        with lock:
            results["errors"] += 1

# Launch the concurrent connections
print("[*] Launching connection burst...")
threads = []
for _ in range(concurrent_connections):
    t = threading.Thread(target=connect_to_target)
    threads.append(t)
    t.start()

# Wait for all connections to resolve
for t in threads:
    t.join()

print("\n[*] Burst complete. Closing persistent sockets...")
for sock in sockets:
    try:
        sock.close()
    except:
        pass

# --- METRICS OUTPUT ---
print("\n" + "="*60)
print("              FINAL SECURITY DIAGNOSTIC RESULTS")
print("="*60)
print(f"Total Connections Attempted: {concurrent_connections}")
print(f"[+] Successfully Connected:  {results['successful']} (Server accepted connection)")
print(f"[-] Firewall Dropped:        {results['firewall_dropped']} (SDN stepped in to protect)")
print(f"[-] Connection Refused:      {results['refused']} (Server actively rejected)")
print(f"[x] Other Errors:            {results['errors']}")
print("="*60)