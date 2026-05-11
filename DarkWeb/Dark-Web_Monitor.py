import requests
from bs4 import BeautifulSoup
import time

# Configuração do proxy Tor SOCKS5
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Palavras-chave para busca (adicione as suas)
keywords = [
    "empresa.com",
    "email@empresa.com",
    "vpn empresa",
    "acesso rdp",
    "senha empresa"
]

# Fóruns públicos (páginas visíveis sem login)
forums = {
    "Dread": "http://dreadditevelidot.onion",
    "TheHub": "http://thehub7gqe43miyc.onion",
    "BreachForums": "http://bfnnkhvpsknai4rg.onion"
}

def fetch_page(url):
    try:
        response = requests.get(url, proxies=proxies, timeout=25)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[!] Erro {response.status_code} ao acessar {url}")
            return None
    except Exception as e:
        print(f"[!] Falha ao acessar {url} -> {e}")
        return None

def search_keywords(html, forum_name, forum_url):
    found = []
    soup = BeautifulSoup(html, 'html.parser')
    for keyword in keywords:
        if keyword.lower() in html.lower():
            found.append((forum_name, forum_url, keyword))
    return found

def main():
    print("=== MONITORAMENTO DE FÓRUNS DA DARK WEB ===\n")
    results = []

    for forum_name, url in forums.items():
        print(f"[+] Acessando {forum_name}...")
        html = fetch_page(url)
        if html:
            found = search_keywords(html, forum_name, url)
            if found:
                for item in found:
                    print(f"   └─ Encontrado: {item[2]} em {item[0]}")
                results.extend(found)
            else:
                print("   └─ Nenhuma palavra-chave encontrada.")
        time.sleep(5)

    if results:
        with open("monitoramento_resultados.txt", "a") as f:
            for res in results:
                f.write(f"{res[0]} | {res[1]} | {res[2]}\n")
        print("\n[✓] Resultados salvos em monitoramento_resultados.txt")
    else:
        print("\n[✓] Nenhuma correspondência encontrada.")

if __name__ == "__main__":
    main()
