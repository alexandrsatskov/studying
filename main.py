import socket


def parse_request(request):
    method, url, *_ = request.split()
    return method, url


def generate_response(request):
    method, url = parse_request(request)
    headers, status_code = generate_headers(method, url)
    body = generate_body(status_code, url)
    return (headers + body).encode()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')

        response = generate_response(request)

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    main()
