import hashlib

texto = "/bin/nash"
resultado = hashlib.sha256("texto".encode('utf-8')).digest()
print(resultado)