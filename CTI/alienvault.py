import requests
from elasticsearch import Elasticsearch
from datetime import datetime

###Configuracao Elasticsearch
OTX_API="af9277801ab5f57df02c94dbd81957d71766dea01069808509a04fcbcb32287f"
HOST="https://localhost:9200"
USER="elastic"
SENHA="MlDkXDvViD3QQg8d5M4C"
INDEX_NAME="threatintel"

###Busca dados no alient Vault
headers = {"X-OTX-API-KEY":OTX_API}
url = "https://otx.alienvault.com/api/v1/pulses/subscribed"

response = requests.get(url, headers=headers)
data = response.json()

###Monta conexao com o elasticsearch
es = Elasticsearch(
    HOST,
    basic_auth=(USER, SENHA),
    verify_certs=False  # cuidado em produção!
)

for pulse in data.get("results", []):
    for indicator in pulse.get("indicators", []):
        doc = {
            "indicator": indicator.get("indicator"),
            "type": indicator.get("type"),
            "description": pulse.get("name"),
            "source": "AlienVault OTX",
            "created": indicator.get("created"),
            "pulse_id": pulse.get("id"),
            "tags": pulse.get("tags"),
            "@timestamp": datetime.utcnow().isoformat()
        }

        es.index(index=INDEX_NAME, document=doc)

print("Dados enviados com sucesso para o Elasticsearch.")