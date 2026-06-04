import nmap
from datetime import datetime

scanner = nmap.PortScanner()
alvo = "portalweb.coxupe.com.br"
portas = "20-10000"

print(f"Iniciando a varredura no alvo {alvo}")
scanner.scan(alvo, portas, arguments="-sV")

# Formatação de data sem caracteres inválidos para nomes de arquivos
data_atual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
arquivo = f"relatorio_{data_atual}.txt"

with open(arquivo, "w") as relatorio:
    for host in scanner.all_hosts():
        relatorio.write(f"HOST: {host} {scanner[host].hostname()}\n")
        for proto in scanner[host].all_protocols():
            relatorio.write(f" PROTOCOLO: {proto}\n")
            # Corrigido: scanner[host][proto] é um dicionário, usamos .keys() para iterar as portas
            for porta in scanner[host][proto].keys():
                relatorio.write(f" PORTA: {porta}\n")
                relatorio.write(f" ESTADO: {scanner[host][proto][porta]['state']}\n")
                if 'name' in scanner[host][proto][porta]:
                    relatorio.write(f" NOME: {scanner[host][proto][porta]['name']}\n")
        relatorio.write("\n")