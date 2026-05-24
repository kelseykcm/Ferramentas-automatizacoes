import socket
import ssl

def test_connectivity(host, port, use_ssl):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        sock.connect((host, port))
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())
        response = sock.recv(4096)
        print(f"Response: {response.decode(errors='ignore')}")
    except ConnectionResetError:
        print("Connection was reset by the remote server.")
    except socket.timeout:
        print("Connection timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    host = input("Enter host: ")
    port = int(input("Enter port: "))
    ssl_choice = input("Use SSL? (S/N): ").strip().upper()
    use_ssl = ssl_choice == 'S'
    test_connectivity(host, port, use_ssl)