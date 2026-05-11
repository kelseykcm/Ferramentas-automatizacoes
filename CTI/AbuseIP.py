import requests

KEY ="a9f1c46466814af7678b3bcdf9cb9a353a0645b938a484c5ebc48290d438d69bc99f9a82cae7c1b1"
url = "https://api.abuseipdb.com/api/v2/blacklist"

headers = {
    "Key": KEY,
    "Accept": "application/json"
}

response = requests.get(url,headers=headers)

if response.status_code == 200:
    threats = response.json()
    for threat in threats["data"]:
        print(f"IP: {threat['ipAddress']}, Score: {threat['abuseConfidenceScore']}")
