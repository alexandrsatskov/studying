import select
import socket

queue = []
to_read = {}
to_write = {}


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5000))
    server_sock.listen()

    while True:
        yield 'read', server_sock
        client_sock, address = server_sock.accept()
        print('Connection', address)
        # Добавляем в очередь экземпляр объекта генератора
        queue.append(client(client_sock))


def client(client_sock):
    while True:
        yield 'read', client_sock
        request = client_sock.recv(4096).decode('utf-8')
        print(request)
        if request:
            response = b'Hello I server'
            yield 'write', client_sock
            client_sock.send(response)
        else:
            client_sock.close()
            break


def event_loop():
    while any([queue, to_read, to_write]):
        while not queue:
            read_rdy, write_rdy, *_ = select.select(to_read, to_write, [])

            for sock in read_rdy:
                queue.append(to_read.pop(sock))
            for sock in write_rdy:
                queue.append(to_write.pop(sock))

        try:
            task = queue.pop()

            condition, sock = next(task)

            if condition == 'read':
                to_read[sock] = task
            if condition == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Программа завершена')


if __name__ == '__main__':
    # Добавляем в очередь экземпляр объекта генератора
    queue.append(server())
    event_loop()
