import os
import sys
import argparse
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Erro: A variável de ambiente GEMINI_API_KEY não está definida.", file=sys.stderr)
    print("Por favor, crie um arquivo .env com GEMINI_API_KEY=\"SUA_CHAVE_API_AQUI\"", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = 'gemini-2.0-flash' # Modelo rápido e eficiente para esta tarefa
MAX_LOG_LINES_PER_CHUNK = 100 # Número de linhas de log a enviar por requisição ao Gemini.
                              # Ajuste conforme a verbosidade dos seus logs e limites do modelo.
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5

# --- Funções ---

def call_gemini_api_with_retry(prompt_content):
    """Chama a API do Gemini com lógica de reintento para maior robustez."""
    for attempt in range(RETRY_ATTEMPTS):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt_content)
            # Verifica se a resposta tem conteúdo
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                raise ValueError("Resposta vazia ou sem conteúdo da API Gemini.")
        except Exception as e:
            print(f"Erro ao chamar a API Gemini (Tentativa {attempt + 1}/{RETRY_ATTEMPTS}): {e}", file=sys.stderr)
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                raise # Re-lança o erro após todas as tentativas falharem
    return None

def parse_gemini_response(response_text):
    """Analisa a resposta JSON do Gemini, tratando possíveis blocos de markdown."""
    try:
        # A API Gemini às vezes envolve o JSON em blocos de markdown
        if "```json" in response_text:
            # Extrai o conteúdo entre o primeiro ```json e o último ```
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        data = json.loads(json_str)
        if not isinstance(data, list):
            print(f"Atenção: Resposta JSON não é uma lista. Conteúdo: {json_str}", file=sys.stderr)
            return []
        return data
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Erro ao decodificar JSON da resposta Gemini: {e}", file=sys.stderr)
        print(f"Resposta bruta recebida: {response_text}", file=sys.stderr)
        return []

def analyze_log_chunk(log_lines):
    """Envia um chunk de linhas de log para o Gemini e processa a resposta."""
    if not log_lines:
        return []

    log_content = "\n".join(log_lines)
    
    # Prompt de engenharia avançada para o Gemini
    prompt = f"""
    Você é um sistema especialista em análise de logs de servidor (SRE - Site Reliability Engineer). Sua tarefa é revisar os logs fornecidos e identificar quaisquer anomalias, erros, avisos críticos, problemas de segurança, ou padrões incomuns que um engenheiro de software deveria investigar.

    Para cada anomalia encontrada, extraia as seguintes informações e apresente-as em um formato de lista JSON.

    - "log_line_number": O número da linha original no chunk de log (a primeira linha é 0, a segunda é 1, etc.).
    - "log_line_content": A linha de log original completa que contém a anomalia.
    - "description": Uma descrição clara e concisa do porquê esta entrada é considerada uma anomalia ou problema. Explique o impacto potencial.
    - "severity": A severidade da anomalia. Use um dos seguintes valores: "Low", "Medium", "High", "Critical".
    - "suggested_action": Uma ação prática e recomendada para um engenheiro investigar ou resolver o problema.

    Se nenhuma anomalia for encontrada no chunk fornecido, retorne um array JSON vazio: `[]`.

    Exemplo de formato de saída esperado:
    ```json
    [
      {{
        "log_line_number": 15,
        "log_line_content": "2024-10-27 10:30:15 ERROR Database connection failed for user 'admin'",
        "description": "Falha crítica na conexão com o banco de dados. Isso pode causar a indisponibilidade de funcionalidades essenciais da aplicação.",
        "severity": "Critical",
        "suggested_action": "Verificar o status do servidor de banco de dados, as credenciais de acesso no arquivo de configuração e as regras de firewall entre a aplicação e o banco."
      }},
      {{
        "log_line_number": 25,
        "log_line_content": "WARNING: Disk space on /var/log is 95% full.",
        "description": "O espaço em disco para logs está quase esgotado. Se atingir 100%, a aplicação pode parar de funcionar ou perder logs importantes.",
        "severity": "High",
        "suggested_action": "Implementar ou executar a rotação de logs (log rotation) e arquivar ou apagar logs antigos."
      }}
    ]
    ```

    Aqui estão as entradas de log para sua análise:
    ```
    {log_content}
    ```
    """
    
    print("Enviando chunk para análise do Gemini...", end=" ", flush=True)
    try:
        gemini_response_text = call_gemini_api_with_retry(prompt)
        print("OK.")
        anomalies = parse_gemini_response(gemini_response_text)
        return anomalies
    except Exception as e:
        print(f"Falha na análise do chunk pelo Gemini: {e}", file=sys.stderr)
        return []

def process_log_file(filepath):
    """Lê um arquivo de log, divide em chunks e envia para análise da IA."""
    print(f"\nAnalisando arquivo: {filepath}")
    anomalies_found = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        if total_lines == 0:
            print("Arquivo de log vazio. Nenhum conteúdo para analisar.")
            return []

        print(f"Total de {total_lines} linhas no arquivo. Dividindo em chunks de {MAX_LOG_LINES_PER_CHUNK} linhas.")

        for i in range(0, total_lines, MAX_LOG_LINES_PER_CHUNK):
            chunk_lines = lines[i:i + MAX_LOG_LINES_PER_CHUNK]
            line_offset = i # Guarda o número da linha inicial deste chunk
            
            chunk_anomalies = analyze_log_chunk([line.strip() for line in chunk_lines])
            
            for anomaly in chunk_anomalies:
                # Mapeia a linha do chunk de volta para a linha original no arquivo
                original_line_num_in_file = line_offset + anomaly.get('log_line_number', 0)
                anomaly['original_file_line'] = original_line_num_in_file + 1 # +1 para ser legível por humanos
                anomaly['filepath'] = filepath
                anomalies_found.append(anomaly)
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.", file=sys.stderr)
    except IOError as e:
        print(f"Erro ao ler arquivo '{filepath}': {e}", file=sys.stderr)
    
    return anomalies_found

def generate_report(all_anomalies, processed_files_count):
    """Gera um relatório formatado e detalhado das anomalias encontradas."""
    print("\n" + "="*80)
    print(" " * 25 + "RELATÓRIO DE ANÁLISE DE LOGS COM IA")
    print("="*80)
    print(f"Arquivos processados: {processed_files_count}")
    print(f"Total de anomalias encontradas: {len(all_anomalies)}\n")

    if not all_anomalies:
        print("Nenhuma anomalia significativa encontrada nos logs analisados. ✅")
        print("="*80)
        return

    # Agrupa por severidade para um resumo rápido
    severity_counts = defaultdict(int)
    for anomaly in all_anomalies:
        severity = anomaly.get('severity', 'Unknown')
        severity_counts[severity] += 1
    
    print("Resumo por Severidade:")
    for severity, count in sorted(severity_counts.items(), key=lambda item: ["Low", "Medium", "High", "Critical"].index(item[0])):
        print(f"  - {severity:<10}: {count} ocorrência(s)")
    print("\n" + "-"*80)

    # Detalhes das Anomalias
    print("Detalhes das Anomalias Encontradas:\n")
    for i, anomaly in enumerate(all_anomalies, 1):
        print(f"--- Anomalia #{i} ---")
        print(f"| Arquivo:     {anomaly.get('filepath', 'N/A')}")
        print(f"| Linha:       {anomaly.get('original_file_line', 'N/A')}")
        print(f"| Severidade:  {anomaly.get('severity', 'N/A')}")
        print(f"| Descrição:   {anomaly.get('description', 'N/A')}")
        print(f"| Ação Sugerida: {anomaly.get('suggested_action', 'N/A')}")
        print(f"| Log Original:  '{anomaly.get('log_line_content', 'N/A')}'")
        print("-" * 20 + "\n")
    
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description="Analisa arquivos de log usando a API do Google Gemini para identificar anomalias.")
    parser.add_argument('log_files', metavar='ARQUIVO_LOG', type=str, nargs='+',
                        help='Caminho para um ou mais arquivos de log para analisar.')
    
    args = parser.parse_args()

    all_anomalies = []
    processed_files_count = len(args.log_files)

    for log_file in args.log_files:
        anomalies = process_log_file(log_file)
        all_anomalies.extend(anomalies)
    
    generate_report(all_anomalies, processed_files_count)

if __name__ == "__main__":
    main()