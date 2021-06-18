import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Чтобы OS не забирала наш порт, после каждого нашего прерывания скрипта
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

while True:
    print('Жду соединения')
    client_socket, address = server_socket.accept()
    print('Соединение:', address)

    while True:
        print('Жду данные')
        request = client_socket.recv(4096)

        if request:
            response = 'Hello world\n'.encode()
            client_socket.send(response)
        else:
            client_socket.close()
            break

