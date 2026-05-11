#Criaremos um cliente tipo C&C em que aceita conexões remotas de um servidor para que eu possa executar comandos remotos.

import socket

def start_client():
    #Cria o socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8080))
    
    #https://www.kea.nu/files/textbooks/humblepy/blackhatpython.pdf