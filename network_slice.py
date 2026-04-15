import socket

# The IP of the secure slice (Virtual Machines)
target_ip = "172.16.0.22"

# Standard ports to test
# 22 (SSH), 80 (HTTP), 443 (HTTPS), 554 (RTSP for Cameras), 8080 (Alt HTTP), 54532 (PostgreSQL), 7070 (Alt RTSP), 8081(HTTP), 8086(InfluxDB), 8081(Appache Tom Cat)
ports_to_check = [22, 80, 443, 554, 8080, 5432, 7070, 8081, 8086, 8081]

print(f"Starting Cross-Slice Visibility Test against target: {target_ip}\n")
print("Evaluating Network Function (NF) Isolation...\n")

for port in ports_to_check:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0) 
    
    try:
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"[!] VULNERABILITY FOUND: Port {port} is OPEN.")
            print("    -> Traffic successfully routed across 5G slices.\n")
        elif result in [111, 10061]: # Common codes for 'Connection Refused'
            print(f"[!] VISIBILITY CONFIRMED: Port {port} is CLOSED, but the host responded.")
            print("    -> The VM is reachable. Slice isolation is fundamentally broken.\n")
        else:
            print(f"[-] Port {port} is filtered/dropped (Code: {result}).")
            
    except socket.timeout:
        print(f"[-] Port {port} timed out. The SDN firewall successfully blocked the route.")
    except socket.error as e:
        print(f"[X] Network error on port {port}: {e}")
    finally:
        sock.close()

print("\nReconnaissance Complete.")