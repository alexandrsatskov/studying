import socket
import selectors

selector = selectors.DefaultSelector()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Чтобы OS не забирала наш порт, после каждого нашего прерывания скрипта
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5000))
    server_sock.listen()

    selector.register(fileobj=server_sock,
                      events=selectors.EVENT_READ,
                      data=accept_connection)


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    print('Соединение:', address)
    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ,
                      data=send_message)


def send_message(client_socket):
    print('Жду данные')
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        events = selector.select()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
