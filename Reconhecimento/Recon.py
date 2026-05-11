import requests
from bs4 import BeautifulSoup
import os

# Configuração do proxy TOR
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

def start_tor():
    os.system('sh -c \'/home/kelsey/Downloads/tor-browser/Browser/start-tor-browser --detach || ([ !  -x "/home/kelsey/Downloads/tor-browser/Browser/start-tor-browser" ] && "$(dirname "$*")"/Browser/start-tor-browser --detach)\' dummy %k')
    
})

def fetch_onion_site(url):
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Erro ao acessar {url}: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Exemplo de site na Deep Web
onion_url = "http://torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd.onion/"
html_content = fetch_onion_site(onion_url)

if html_content:
    soup = BeautifulSoup(html_content, 'html.parser')
    print(soup.title.string)  # Exibe o título da página


def search_for_keyword(html_content, keywords):
    results = []
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    for keyword in keywords:
        if keyword in text:
            results.append(keyword)
    return results

# Palavras-chave relacionadas ao domínio
keywords = ["cooxupe.com", "admin@cooxupe.com.br"]

if html_content:
    found_keywords = search_for_keyword(html_content, keywords)
    if found_keywords:
        print(f"Palavras-chave encontradas: {found_keywords}")
    else:
        print("Nenhuma palavra-chave encontrada.")




forum_urls = [
    "http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/post/ee8e8059205aa7baf425",
    "http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/post/f9028c83c314f4d851dc"
]

for forum in forum_urls:
    print(f"Visitando: {forum}")
    html_content = fetch_onion_site(forum)
    if html_content:
        found_keywords = search_for_keyword(html_content, keywords)
        if found_keywords:
            print(f"Informações relevantes encontradas em {forum}: {found_keywords}")
            

    