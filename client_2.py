import socket
import time

if __name__ == '__main__':
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', 5000))
    while True:
        try:
            client_sock.send('Hello I client №2'.encode('utf-8'))
            print(client_sock.recv(4096).decode())
            time.sleep(3)
        except KeyboardInterrupt:
            client_sock.close()
            break
