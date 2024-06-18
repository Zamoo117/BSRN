from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

def run_https_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.pem', server_side=True)
    print(f'Starting HTTPS server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run_https_server()
