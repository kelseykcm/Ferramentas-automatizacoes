import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import json
from datetime import datetime
from scapy.all import *
from scapy.layers.l2 import Ether, ARP
from mac_vendor_lookup import MacLookup  # Nova biblioteca para buscar fabricantes

# Inicializa e baixa/atualiza a lista de fabricantes (pode demorar alguns segundos na primeira execução)
try:
    mac_lookup = MacLookup()
    mac_lookup.update_vendors()
except Exception:
    # Caso esteja sem internet, ele usa a base de dados padrão já embutida
    pass

devices_corporativos = {
    "192.168.0.1": "Roteador",
    "192.168.0.100": "Camera",
    "aa:bb:cc:0e:aa:90": "Mac"
}

def scan_rede(rede):
    arp = ARP(pdst=rede)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    pacote = ether / arp

    resultado, _ = srp(pacote, timeout=2, verbose=False)
    
    dispositivos = []
    for enviado, recebido in resultado:
        mac_atual = recebido.hwsrc
        
        # Tenta descobrir o fabricante pelo MAC
        try:
            fabricante = mac_lookup.lookup(mac_atual)
        except KeyError:
            fabricante = "Desconhecido (MAC Virtual/Privado)"
        except Exception:
            fabricante = "Erro ao consultar"

        dispositivos.append({
            "ip": recebido.psrc,
            "mac": mac_atual,
            "fabricante": fabricante  # Campo adicionado dinamicamente
        })
    return dispositivos

def detectar_dispositivos(dispositivos):
    desconhecidos = []
    for disp in dispositivos:
        ip = disp['ip']
        mac = disp['mac']
        if ip not in devices_corporativos and mac not in devices_corporativos:
            desconhecidos.append(disp)
    return desconhecidos

def salvar_relatorio(dispositivos):
    nome_arquivo = f"relatorio_dispositivos_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(nome_arquivo, "w") as f:
        json.dump(dispositivos, f, indent=4)
    print(f" * Relatório salvo com sucesso como: {nome_arquivo}")

print(" * Escaneando rede... ") 
dispositivos_encontrados = scan_rede("192.168.0.0/24")

print(" * Verificando dispositivos desconhecidos... ")
novos = detectar_dispositivos(dispositivos_encontrados)

if novos:
    print(" * Dispositivos não reconhecidos encontrados: ")
    for d in novos:
        # Agora o campo 'fabricante' funciona perfeitamente
        print(f"  - IP: {d['ip']} - MAC: {d['mac']} - Fabricante: {d['fabricante']}")
    
    salvar_relatorio(novos)
else:
    print(" * Nenhum dispositivo desconhecido encontrado.")