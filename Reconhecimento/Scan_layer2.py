#Faça Um script que faça um scan de layer2 para descobrir os hosts na rede

import scapy.all as scapy

def scan_layer2(ip):
     arp_request = scapy.ARP(pdst=ip)
     broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
     arp_request_broadcast = broadcast / arp_request
     answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
     clients = []
     for element in answered_list:
         clients.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
     return clients

if __name__ == "__main__":
    ip_range = "192.168.0.0/24"
    clients = scan_layer2(ip_range)
    print("Dispositivos encontrados na rede:")
    for client in clients:
        print(f"IP: {client['ip']}, MAC: {client['mac']}")