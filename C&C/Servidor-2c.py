import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.0.110', 8443))
    s.listen(1)
    print('Server listening on 192.168.0.110:8443')

    conn, addr = s.accept()
    print(f'Connected by {addr}')

    while True:
        command = input("Enter command (or 'exit' to quit): ")
        try:
            conn.send(command.encode('utf-8'))
            if command.strip() == 'exit':
                print('Exiting...')
                conn.close()
                s.close()
                sys.exit(0)
            data = conn.recv(4096)
            if not data:
                print('Client disconnected.')
                break
            print('Response:', data.decode('utf-8'))
        except Exception as e:
            print(f'Error during communication: {e}')
            break

except KeyboardInterrupt:
    print('\nServer interrupted by user.')
except Exception as e:
    print(f'Server setup error: {e}')

finally:
    try:
        if 's' in locals():
            s.close()
    except:
        pass
    print('Server stopped.')