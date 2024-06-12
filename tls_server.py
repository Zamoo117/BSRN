import socket
import ssl
import os

def run_tls_server(host, port):
    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir(os.getcwd()))

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((host, port))
        sock.listen(5)
        print("TLS Server listening on port", port)
        
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            print("Connection from", addr)
            
            # Send an encrypted message
            payload = "This is a secret message".encode('utf-8')
            conn.send(payload)
            conn.close()

if __name__ == "__main__":
    run_tls_server('0.0.0.0', 8443)
