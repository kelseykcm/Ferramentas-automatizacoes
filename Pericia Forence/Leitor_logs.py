from collections import Counter

arquivo_log = "acessos.log"

tentativas_suspeitas = []

with open(arquivo_log, "r", encoding="utf-8") as f:
    for linha in f:
        partes = linha.strip().split("-")
        if len(partes) != 4:
            continue
        data, ip, recurso, codigo = partes
        codigo = int(codigo)
        
        if codigo == 401 in recurso:
            tentativas_suspeitas.append(ip)
            
contador_suspeitos = Counter(tentativas_suspeitas)

print("---resumo de IPs suspeitos---")
for ip, cont in contador_suspeitos.items():
    print(f"IP: {ip} -> {cont} eventos suspeitos\n")
    
with open("relatorio_analise.txt", "w", encoding="utf-8") as relatorio:
    relatorio.write("---resumo dos IPs suspeitos---\n")
    for ip, cont in contador_suspeitos.items():
        relatorio.write(f"IP: {ip} -> {cont} eventos suspeitos\n")