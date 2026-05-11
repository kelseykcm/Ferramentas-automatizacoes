SEARCH="firefox"
ALVO="$1"

echo "Pesquisando informacoes:"
$SEARCH "https://www.google.com.br/search?q=site:pastebin.com+$ALVO" 2> /dev/null
echo "Pesquisando por informacoes : "
$SEARCH "https://www.google.com.br/search?q=site:$ALVO+ext:pdf+OR+ext:doc" 2> /dev/null
