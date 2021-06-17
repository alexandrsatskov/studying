import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Чтобы OS не забирала наш порт, после каждого нашего прерывания скрипта
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5000))
server_sock.listen()


def accept_connection(server_socket):
    while True:
        client_socket, address = server_socket.accept()
        print('Соединение:', address)
        send_message(client_socket)


def send_message(client_socket):
    while True:
        print('Жду данные')
        request = client_socket.recv(4096)

        if request:
            response = 'Hello world\n'.encode()
            client_socket.send(response)
        else:
            break
        client_socket.close()

