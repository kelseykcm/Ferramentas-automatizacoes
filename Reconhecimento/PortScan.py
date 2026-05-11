from scapy.all import IP, TCP, sr, sr1, send
import logging

# Desativa mensagens de log verbosas da Scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def stealth_scan(target_host, port_range, scan_type="SYN"):
    """
    Realiza diferentes tipos de scans furtivos em um host e range de portas.

    :param target_host: O endereço IP do alvo.
    :param port_range: Um objeto range ou lista de portas para escanear.
    :param scan_type: Tipo de scan: "SYN", "FIN", "XMAS", "NULL".
    :return: Duas listas: (portas abertas, portas fechadas).
    """
    open_ports = []
    closed_ports = []
    
    scan_flags = {
        "SYN": "S",
        "FIN": "F",
        "XMAS": "FPU",
        "NULL": ""
    }

    if scan_type not in scan_flags:
        print(f"Erro: Tipo de scan '{scan_type}' desconhecido.")
        return [], []

    flag = scan_flags[scan_type]
    print(f"[*] Iniciando Scan do tipo '{scan_type}' em {target_host}...")
    
    packets = IP(dst=target_host) / TCP(dport=list(port_range), flags=flag)
    answered, unanswered = sr(packets, timeout=5, verbose=0)

    if scan_type == "SYN":
        # Para SYN Scan, a resposta indica o estado
        for sent, received in answered:
            if received.getlayer(TCP).flags == 0x12: # SYN/ACK
                port = received.sport
                open_ports.append(port)
                # Envia RST para ser "stealth"
                send(IP(dst=target_host)/TCP(dport=port, flags="R"), verbose=0)
            elif received.getlayer(TCP).flags == 0x14: # RST/ACK
                closed_ports.append(received.sport)
        # Portas não respondidas podem estar filtradas
    
    else: # Lógica para FIN, XMAS, NULL
        # Portas que NÃO respondem estão ABERTAS ou FILTRADAS
        for packet in unanswered:
            open_ports.append(packet.dport)
        
        # Portas que RESPONDEM (com RST) estão FECHADAS
        for sent, received in answered:
            if received.getlayer(TCP).flags == 0x14: # RST/ACK
                closed_ports.append(received.sport)

    open_ports.sort()
    closed_ports.sort()
    
    return open_ports, closed_ports


if __name__ == "__main__":
    target = "37.59.174.227" # Use um alvo que você tenha permissão para escanear!
    ports_to_scan = range(1, 65355)

    # --- Exemplo de uso ---
    
    # 1. SYN Scan (mais confiável)
    open_p, closed_p = stealth_scan(target, ports_to_scan, "SYN")
    print("\n--- Resultados do SYN Scan ---")
    print(f"Portas Abertas: {open_p}")
    # print(f"Portas Fechadas: {closed_p}") # Descomente se quiser ver

    # 2. FIN Scan (pode não funcionar em todos os alvos)
    open_p, closed_p = stealth_scan(target, ports_to_scan, "FIN")
    print("\n--- Resultados do FIN Scan ---")
    print(f"Portas Abertas ou Filtradas: {open_p}")
    
    # 3. Xmas Scan
    open_p, closed_p = stealth_scan(target, ports_to_scan, "XMAS")
    print("\n--- Resultados do Xmas Scan ---")
    print(f"Portas Abertas ou Filtradas: {open_p}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 