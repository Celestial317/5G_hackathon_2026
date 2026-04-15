from scapy.all import Ether, IP, ICMP, sendp
import sys

# 1. Hardware Targeting
# Scapy prefers colons for MAC addresses, so we format it standardly
router_mac = "48:21:0b:46:28:25"

spoofed_source_ip = "172.16.0.21"  # (decoy)

# 3. The Target - The firewall, router, or MEC server
target_destination_ip = "192.168.1.1"

print("="*50)
print("Initiating Layer-2 Directed uRPF Diagnostic")
print("="*50)
print(f"[*] Constructing forged Ethernet and IP headers...")
print(f"    -> Destination MAC:     {router_mac}")
print(f"    -> Spoofed Source IP:   {spoofed_source_ip}")
print(f"    -> Destination Target:  {target_destination_ip}\n")


# Layer 2 (Ether) -> Layer 3 (IP) -> Protocol (ICMP) -> Payload
packet = Ether(dst=router_mac) / IP(src=spoofed_source_ip, dst=target_destination_ip) / ICMP() / b"URPF_AUDIT_PACKET"

try:
    print("[*] Transmitting directed packet into the 5G core...")
    sendp(packet, count=1, verbose=False)
    
    print("\n[+] Transmission Complete.")
    print("\nNext Step: Verify arrival on the Operator PC Wireshark.")

except PermissionError:
    print("\n[X] PERMISSION DENIED: Crafting Layer-2 packets requires Administrator privileges.")
    print("    Right-click your terminal, select 'Run as Administrator', and try again.")
except Exception as e:
    print(f"\n[X] Execution Error: {e}")