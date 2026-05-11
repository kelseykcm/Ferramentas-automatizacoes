#!/bin/bash

# --- CONFIGURAÇÃO ---
# Altere estas variáveis conforme sua necessidade.
URL_ALVO="http://businesscorp.com.br"
WORDLIST="common.txt"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# Modo Verbose:
# true  -> Mostra TODAS as tentativas, incluindo as que falham (404).
# false -> Mostra APENAS os diretórios/arquivos encontrados (status diferente de 404).
VERBOSE=true
# --------------------

# Verifica se o comando curl está instalado
if ! command -v curl &> /dev/null; then
    echo "Erro: O comando 'curl' não foi encontrado. Por favor, instale-o."
    exit 1
fi

# Verifica se a wordlist existe
if [ ! -f "$WORDLIST" ]; then
    echo "Erro: Wordlist não encontrada em '$WORDLIST'"
    exit 1
fi

echo "Iniciando varredura em: $URL_ALVO..."
echo "Usando User-Agent: Chrome"
[ "$VERBOSE" = true ] && echo "Modo Verbose: ATIVADO" || echo "Modo Verbose: DESATIVADO"
echo "-----------------------------------"

# Lê o arquivo da wordlist linha por linha
while read -r entrada; do

    # Monta a URL completa
    URL_COMPLETA="${URL_ALVO}/${entrada}"

    # Usa o curl para obter apenas o código de status HTTP
    STATUS=$(curl -s -A "$USER_AGENT" -o /dev/null -w "%{http_code}" "$URL_COMPLETA")

    # Lógica de exibição:
    # 1. Se o status NÃO for 404, sempre mostra como "Encontrado".
    # 2. Se o status for 404 E o modo verbose estiver ativo, mostra como "Testando".
    if [ "$STATUS" != "404" ]; then
        echo "[+] Encontrado: ${URL_COMPLETA}  (Status: ${STATUS})"
    elif [ "$VERBOSE" = true ]; then
        echo "[-] Testando:   ${URL_COMPLETA} (Status: 404)"
    fi

done < "$WORDLIST"

echo "-----------------------------------"
echo "Varredura concluída."
