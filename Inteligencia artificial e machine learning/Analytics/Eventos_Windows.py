import pandas as pd
import re

# Carrega o CSV com eventos do Windows exportados via PowerShell
df = pd.read_csv("eventos_analiticos.csv")

# Se quiser trabalhar com eventos específicos:
eventos_importantes = [
    4624, 4625, 4648, 4672, 4688, 4697,
    4720, 4723, 4724, 4728, 4732, 4740,
    4776, 5140
]

df = df[df['Id'].isin(eventos_importantes)].copy()

# =============================
# Funções para extrair campos
# =============================

def extrair_ip(msg):
    match = re.search(r'Source Network Address:\s+([^\s\r\n]+)', str(msg))
    if match:
        ip = match.group(1)
        if re.match(r'\d{1,3}(\.\d{1,3}){3}', ip):
            return ip
    return None

def extrair_usuario(msg):
    match = re.search(r'Account Name:\s+([^\s\r\n$]+)', str(msg))
    if match:
        return match.group(1)
    return None

def extrair_dominio(msg):
    match = re.search(r'Account Domain:\s+([^\s\r\n]+)', str(msg))
    if match:
        return match.group(1)
    return None

def extrair_logon_type(msg):
    match = re.search(r'Logon Type:\s+(\d+)', str(msg))
    return int(match.group(1)) if match else None

def extrair_processo(msg):
    match = re.search(r'Process Name:\s+([^\s\r\n]+)', str(msg))
    return match.group(1) if match else None

def extrair_logon_id(msg):
    match = re.search(r'Logon ID:\s+([^\s\r\n]+)', str(msg))
    return match.group(1) if match else None

# =============================
# Aplica as extrações ao DataFrame
# =============================

df['IP_Origem'] = df['Message'].apply(extrair_ip)
df['Usuario'] = df['Message'].apply(extrair_usuario)
df['Dominio'] = df['Message'].apply(extrair_dominio)
df['Logon_Type'] = df['Message'].apply(extrair_logon_type)
df['Processo'] = df['Message'].apply(extrair_processo)
df['Logon_ID'] = df['Message'].apply(extrair_logon_id)

# =============================
# Análise e visualização básica
# =============================

print("\nTop 10 usuários:")
print(df['Usuario'].value_counts().head(10))

print("\nTop 10 IPs:")
print(df['IP_Origem'].value_counts().head(10))

print("\nTipos de logon mais comuns:")
print(df['Logon_Type'].value_counts())

print("\nProcessos mais executados:")
print(df['Processo'].value_counts().head(10))
