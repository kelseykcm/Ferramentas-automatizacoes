#faça um programa que envie pacotes de rede usando a biblioteca scapy.
#O programa poderá escolher um aalvo especifico ou poderá enviar pacotes para todos os dispotivos na

from scapy.all import *

pkt = sniff(filter="ether dst cc:32:e5:0d:9f:d5", count=1)
print("Frame capturado : ", pkt[0])
print("Frame capturado com detalhes : ", pkt[0].show())
print("Camada Ethernet : ", pkt[0][0].show())
print("Camada 1 'Logical Link Control' : ",pkt[0][1].show())
print("Camada 2 'Network Enlace' : ",pkt[0][2].show())                                                                                                                                                                                                                                                                                                                                                                                                                                                  

