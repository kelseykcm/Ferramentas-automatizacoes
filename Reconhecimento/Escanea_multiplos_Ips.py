import socket
import threading
from queue import Queue
from datetime import datetime
import csv
 
# Cores para terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
 
# Coleta de banner
def coletar_banner(ip, porta):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, porta))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "sem banner"
    except:
        return "sem resposta"
 
# Identificação simples de serviço
def identificar_servico(banner):
    b = banner.lower()
    if "http" in b: return "HTTP"
    elif "ftp" in b: return "FTP"
    elif "ssh" in b: return "SSH"
    elif "smtp" in b: return "SMTP"
    elif "imap" in b: return "IMAP"
    elif "pop3" in b: return "POP3"
    else: return "Desconhecido"
 
# Detecção de vulnerabilidades simples
def detectar_vulnerabilidades(porta, banner):
    vulns = []
    if porta == 21 and "ftp" in banner.lower():
        vulns.append("FTP anônimo possível")
    if porta == 80 and "http" in banner.lower():
        vulns.append("Checar métodos HTTP inseguros (TRACE/OPTIONS)")
    if porta == 3306:
        vulns.append("MySQL aberto - verificar acesso remoto")
    return ", ".join(vulns) if vulns else "Nenhuma detectada"
 
# Função da thread
def escanear_porta(ip, porta, resultados):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, porta))
        banner = coletar_banner(ip, porta)
        servico = identificar_servico(banner)
        vulns = detectar_vulnerabilidades(porta, banner)
        resultados.append((porta, servico, banner, vulns))
        print(f"{GREEN}[ABERTA]{RESET} Porta {porta:5} | Serviço: {servico:10} | Vulnerabilidades: {vulns}")
        sock.close()
    except:
        resultados.append((porta, "fechada", "", ""))
        print(f"{RED}[FECHADA]{RESET} Porta {porta:5}")
 
# Escaneamento multithread
def escanear_multithread(ip, portas):
    resultados = []
    queue = Queue()
    for porta in portas:
        queue.put(porta)
 
    def worker():
        while not queue.empty():
            porta = queue.get()
            escanear_porta(ip, porta, resultados)
            queue.task_done()
 
    threads = []
    for _ in range(min(20, len(portas))):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
 
    queue.join()
    return resultados
 
# Função para varrer múltiplos alvos
def varrer_alvos(alvos, portas):
    for alvo in alvos:
        print(f"\n{YELLOW}=== Varredura no alvo: {alvo} ==={RESET}")
        resultados = escanear_multithread(alvo, portas)
        salvar_relatorio(alvo, resultados)
 
# Salvar relatório
def salvar_relatorio(ip, resultados):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    txt_file = f"relatorio_{ip.replace('.', '_')}_{timestamp}.txt"
    csv_file = f"relatorio_{ip.replace('.', '_')}_{timestamp}.csv"
 
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"Relatório de Varredura - Alvo: {ip}\n")
        f.write(f"Data: {datetime.now()}\n\n")
        for porta, serv, banner, vulns in resultados:
            f.write(f"Porta {porta:5} | Serviço: {serv:10} | Banner: {banner} | Vulnerabilidades: {vulns}\n")
 
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Porta", "Serviço", "Banner", "Vulnerabilidades"])
        for porta, serv, banner, vulns in resultados:
            writer.writerow([porta, serv, banner, vulns])
 
    print(f"\n{YELLOW}Relatórios salvos: {txt_file} e {csv_file}{RESET}")
 
# Função principal
def main():
    print(f"{YELLOW}=== Ferramenta de Varredura Avançada com Fingerprinting e Vulnerabilidade ==={RESET}")
    alvos_input = input("Digite IPs ou domínios separados por vírgula: ")
    alvos = [a.strip() for a in alvos_input.split(",")]
    portas_comuns = [21,22,23,25,53,80,110,143,443,3389,3306,8080,27017] # inclui MongoDB
 
    varrer_alvos(alvos, portas_comuns)
    print(f"\n{GREEN}Varredura concluída para todos os alvos!{RESET}")
 
if __name__ == "__main__":
    main()