import os
import subprocess
import sys
import platform
from datetime import datetime


def coletar_informacoes():
    info = {}
    if platform.system() == 'Windows':
        info['hostname'] = os.environ.get('COMPUTERNAME', 'N/A')
        info['user'] = os.environ.get('USERNAME', 'N/A')
        info['os'] = platform.platform()
    else:
        info['hostname'] = subprocess.getoutput('hostname')
        info['user'] = subprocess.getoutput('whoami')
        info['os'] = subprocess.getoutput('uname -a')
    return info

def criar_estrutura():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    root_dir = f"relatorio_forense_{timestamp}"
    os.makedirs(os.path.join(root_dir, 'Rede'), exist_ok=True)
    os.makedirs(os.path.join(root_dir, 'Processos'), exist_ok=True)
    os.makedirs(os.path.join(root_dir, 'Sistema'), exist_ok=True)
    return root_dir

def salvar_comando(root_dir, subpasta, nome_arquivo, comando, info_header):
    caminho_pasta = os.path.join(root_dir, subpasta)
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_arquivo = os.path.join(caminho_pasta, f"{nome_arquivo}.txt")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=30)
        saida = resultado.stdout + resultado.stderr
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"=== RELATÓRIO FORENSE - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ===\n\n")
            f.write("=== INFORMAÇÕES DO SISTEMA ===\n")
            for chave, valor in info_header.items():
                f.write(f"{chave}: {valor}\n")
            f.write("\n=== SAÍDA DO COMANDO ===\n")
            f.write(saida)
        print(f"Comando '{comando}' salvo em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao executar comando '{comando}': {e}")

def coletar():
    info = coletar_informacoes()
    root_dir = criar_estrutura()
    
    if platform.system() == 'Windows':
        comandos_rede = [
            ('ipconfig', 'ipconfig'),
            ('arp -a', 'arp'),
            ('netstat -an', 'netstat'),
            ('nslookup localhost', 'dns'),
        ]
        comandos_processos = [
            ('tasklist', 'tasklist'),
            ('tasklist /svc', 'servicos'),
        ]
        comandos_sistema = [
            ('systeminfo', 'systeminfo'),
            ('wmic os get caption,version', 'os_info'),
            ('dir C:\\Users', 'usuarios'),
        ]
    else:
        comandos_rede = [
            ('ip addr', 'ip_addr'),
            ('arp -a', 'arp'),
            ('netstat -tuln', 'netstat'),
            ('dig localhost', 'dns'),
            ('ss -tuln', 'ss'),
            ('mount', 'mount'),
            ('crontab -l', 'crontab'),
            ('nslookup www.google.com', 'dns_google'),
        ]
        comandos_processos = [
            ('ps aux', 'ps_aux'),
            ('top -b -n1', 'top'),
            ('pstree -a',  'pstree'),
            ('lsof -T',  'lsof'),
        ]
        comandos_sistema = [
            ('uname -a', 'uname'),
            ('cat /etc/os-release', 'os_release'),
            ('ls /home', 'usuarios'),
        ]
    
    for comando, nome in comandos_rede:
        salvar_comando(root_dir, 'Rede', nome, comando, info)
    for comando, nome in comandos_processos:
        salvar_comando(root_dir, 'Processos', nome, comando, info)
    for comando, nome in comandos_sistema:
        salvar_comando(root_dir, 'Sistema', nome, comando, info)
    
    print(f"Relatório salvo em: {root_dir}")

if __name__ == '__main__':
    coletar()