import socket
import sys

def get_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, int(port)))
            
            # Hybrid approach: Try to receive data first (passive banner grabbing)
            try:
                banner = s.recv(1024)
                if banner:
                    return f"[+] Banner recebido: {banner.decode().strip()}"
            except Exception:
                pass

            # If no banner received, send a probe (active banner grabbing)
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024)
            if banner:
                return f"[+] Banner via probe: {banner.decode().strip()}"
            
            return "[-] Nenhuma resposta de banner obtida."
            
    except socket.timeout:
        return "[-] Erro: Tempo limite excedido."
    except ConnectionRefusedError:
        return "[-] Erro: Conexão recusada."
    except Exception as e:
        return f"[-] Erro inesperado: {e}"

def main():
    print("--- Coletor de Banner Profissional ---")
    target = input("Digite o IP ou endereço do alvo: ").strip()
    port = input("Digite a porta: ").strip()

    if not target or not port.isdigit():
        print("Entrada inválida.")
        sys.exit(1)

    print(f"\nConectando em {target}:{port}...")
    result = get_banner(target, port)
    print(result)

if __name__ == "__main__":
    main()