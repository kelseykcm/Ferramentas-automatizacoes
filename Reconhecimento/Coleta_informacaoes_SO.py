#identificar a plataforma em que o script rodará para coletar as informações de acordo com o sistema operacional
#se o sistema operacional for Linux, coletar as seguintes informações: nome do sistema operacional, versão do sistema operacional e arquitetura do sistema operacional
#Se o sistema for windows, coletar as seguintes informações: nome do sistema operacional, versão do sistema operacional e arquitetura do sistema operacional

import platform
import subprocess

def coletar_informacoes():
    sistema = platform.system()
    versao = platform.version()
    arquitetura = platform.architecture()[0]
    return {
        "sistema": sistema,
        "versao": versao,
        "arquitetura": arquitetura
    }

result = coletar_informacoes()

#funcoes dos comandos para serem chamados

def executar_comandos_linux():
    print("Executando comandos para Linux...")
    print("Informacoes de rede : \n", subprocess.run(["ip", "a"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["ip", "route"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["ss", "-tulpn"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["lsof", "-i"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["nslookup", "www.google.com.br"], capture_output=True, text=True).stdout)
    print("#######################################################################################################")
    print("Informacoes de processos : \n", subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout)
    print("Informacoes de processos : \n", subprocess.run(["top", "-b -n4"], capture_output=True, text=True).stdout)
    print("Informacoes de processos : \n", subprocess.run(["pstree", "-a"], capture_output=True, text=True).stdout)
    print("#######################################################################################################")
    print("Informacoes do sistema : \n", subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout)
    print("#######################################################################################################")
    
def executar_comandos_windows():
    print("Executando comandos para Windows...")
    print("Informacoes de rede : \n", subprocess.run(["ipconfig", "-a"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["route", "print"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout)
    print("Informacoes de rede : \n", subprocess.run(["nslookup", "www.google.com.br"], capture_output=True, text=True).stdout)
    print("#######################################################################################################")
    print("Informacoes de processos : \n", subprocess.run(["tasklist"], capture_output=True, text=True).stdout)
    print("Informacoes de processos : \n", subprocess.run(["tasklist", "/v"], capture_output=True, text=True).stdout)
    print("Informacoes de processos : \n", subprocess.run(["tasklist", "/m"], capture_output=True, text=True).stdout)
    print("#######################################################################################################")
    print("Informacoes do sistema : \n", subprocess.run(["systeminfo"], capture_output=True, text=True).stdout)


if result["sistema"] == "Linux" :
    print(f"Sistema operacional encontrado {result['sistema']}")
    executar_comandos_linux()
elif result["sistema"] == "Windows":
    print(f"Sistema operacional encontrado {result['sistema']}")
    executar_comandos_windows()

if __name__ == "__main__":
    result = coletar_informacoes()