import socket
import sys

def main():
    # 1. Validação da entrada do usuário
    if len(sys.argv) < 2:
        print(f"Uso: python {sys.argv[0]} <dominio_ou_ip>")
        sys.exit(1)
    
    target = sys.argv[1]

    # 2. Conexão inicial com o servidor da IANA para descobrir o servidor WHOIS correto
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("whois.iana.org", 43))
            
            # Codifica a string para bytes (UTF-8 é o padrão mais seguro)
            s.send((target + "\r\n").encode('ISO-8859-1'))
            
            # Recebe a resposta e decodifica de bytes para string
            response = s.recv(2048).decode('ISO-8859-1')

    except socket.error as e:
        print(f"Erro na conexão com a IANA: {e}")
        sys.exit(1)

    # 3. Procura pelo servidor WHOIS de referência na resposta
    refer_server = None
    for line in response.splitlines():
        if "whois:" in line.lower():
            # Extrai o nome do servidor da linha
            refer_server = line.split(":")[1].strip()
            break
    
    if not refer_server:
        print(f"Não foi possível encontrar um servidor WHOIS de referência para '{target}'.")
        print("\n--- Resposta da IANA ---")
        print(response)
        sys.exit(1)

    print(f"[*] Servidor WHOIS de referência encontrado: {refer_server}")
    print(f"[*] Consultando {target} em {refer_server}...")

    # 4. Conexão com o servidor WHOIS de referência para obter os detalhes
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
            s1.connect((refer_server, 43))
            s1.send((target + "\r\n").encode('utf-8'))
            
            # Um loop para receber todos os dados, já que a resposta pode ser grande
            full_response = b""
            while True:
                data = s1.recv(2048)
                if not data:
                    break
                full_response += data
            
            # Decodifica a resposta final e imprime
            print("\n--- Resultado do WHOIS ---")
            print(full_response.decode('utf-8', errors='ignore'))

    except socket.error as e:
        print(f"Erro na conexão com {refer_server}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()