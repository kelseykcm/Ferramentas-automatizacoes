#Faça um programa que leia pacotes de rede e que mostram seus conteúdos, como scapy
from scapy.all import *

def mostrar_conteudo_pacote(pacote):
    # Exibe informações básicas do pacote
    print("Conteudo do pacote : ")
    print(pacote.show())
    print("Resumo do pacote : ")
    print(pacote.summary())

if __name__ == "__main__":
    sniff(prn=mostrar_conteudo_pacote)
