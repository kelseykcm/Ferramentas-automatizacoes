import socket

def coletar_banner(ip,porta):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, porta))
        banner = s.recv(4096).decode(errors="ignore")
        s.close()
        return banner
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def scanear(ip,portas):
    resultado = []
    for porta in portas:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((ip, porta))
            banner = coletar_banner(ip, porta)
            resultado.append((porta, banner if banner else "sem banner"))
            sock.close()
        except:
            return resultado
        
if __name__ == "__main__":
    alvo = input("Digite o IP ou dominio para escanear: ")
    portas_comuns = [21,22,23,25,80,110,143,443,2289]
    resultados = scanear(alvo, portas_comuns)
    
    with open("relatorios.txt", "w", encoding="utf-8") as arquivo:
        for porta, banner in resultados:
            arquivo.write(f"porta {porta} : {banner}\n")
            
print("Varredura concluido : resultado salvo em ")