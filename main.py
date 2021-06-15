import socket

URLS = {
    '/': 'main page',
    '/about': 'about us page',
}


def generate_body(status_code, url):
    if status_code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if status_code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return f'<h1>{URLS[url]}</h1>'


def generate_headers(method, url):
    if method != 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    if url not in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


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
