import socket
from select import select

to_monitor = []

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Чтобы OS не забирала наш порт, после каждого нашего прерывания скрипта
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5000))
server_sock.listen()


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    print('Соединение:', address)
    to_monitor.append(client_socket)


def send_message(client_socket):
    print('Жду данные')
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        # Готовые для чтения, для записи; ошибки
        read_ready, _, _ = select(to_monitor, [], [])

        for sock in read_ready:
            if sock is server_sock:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_sock)
    event_loop()


