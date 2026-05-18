import time
import os
import pathlib
import logging
import platform
from datetime import datetime

# Configuração de Logging Profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitoramento_forense.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def monitorar_arquivos(diretorio_path):
    logging.info(f"Iniciando monitoramento em: {diretorio_path} (SO: {platform.system()})")
    arquivos_monitorados = {}

    try:
        while True:
            # rglob('*') percorre recursivamente todos os arquivos
            for item in diretorio_path.rglob('*'):
                if item.is_file():
                    try:
                        caminho_str = str(item.absolute())
                        mtime = item.stat().st_mtime
                        
                        if caminho_str not in arquivos_monitorados:
                            # Primeira leitura: armazena o estado atual
                            arquivos_monitorados[caminho_str] = mtime
                        else:
                            # Comparação de modificação
                            if mtime != arquivos_monitorados[caminho_str]:
                                logging.warning(f"ALTERAÇÃO DETECTADA: {caminho_str}")
                                arquivos_monitorados[caminho_str] = mtime
                    except (PermissionError, FileNotFoundError):
                        # Pula arquivos que o SO bloqueia a leitura (comum em arquivos de sistema)
                        continue
            
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Monitoramento encerrado pelo usuário.")

if __name__ == "__main__":
    entrada = input("Digite ou cole o caminho da pasta: ").strip()
    
    # Remove aspas extras que podem vir ao copiar o caminho
    entrada = entrada.replace('"', '').replace("'", "")
    
    # Converte para objeto de caminho absoluto (resolve barras / e \ automaticamente)
    diretorio_monitorado = pathlib.Path(entrada).resolve()

    if diretorio_monitorado.exists() and diretorio_monitorado.is_dir():
        monitorar_arquivos(diretorio_monitorado)
    else:
        print(f"\n[ERRO] Diretório inválido ou inacessível: {diretorio_monitorado}")
        print("Dica: Certifique-se de que o caminho existe e você tem permissão de leitura.")