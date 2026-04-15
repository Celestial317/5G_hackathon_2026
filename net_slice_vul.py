import socket

# The exposed 5G Virtual Machine subnet
target_ip = "172.16.0.22"

# The specific open ports found in the previous scan
# 22 (SSH), 80/8080 (HTTP), 5432 (Postgres), 8086 (InfluxDB)
ports_to_test = [22, 80, 8080, 5432, 8086]

print(f"Starting Application-Layer Banner Grab on {target_ip}\n")
print("Objective: Prove active services are exposed across the network slice.\n")
print("-" * 60)

for port in ports_to_test:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0) # 3-second timeout
        sock.connect((target_ip, port))
        if port in [80, 8080, 8081]:
            http_request = f"HEAD / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
            sock.sendall(http_request.encode())
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        
        if banner:
            print(f"[SUCCESS] Port {port} is actively running a service.")
            first_line = banner.split('\n')[0]
            print(f"          -> Service Banner: {first_line}\n")
        else:
            print(f"[!] Port {port} is open but returned no identification banner.\n")

    except socket.timeout:
        print(f"[-] Port {port} connection timed out.\n")
    except ConnectionRefusedError:
        print(f"[-] Port {port} actively refused the connection.\n")
    except Exception as e:
        print(f"[X] Error on port {port}: {e}\n")
    finally:
        sock.close()

print("-" * 60)
print("Banner Grabbing Complete.")