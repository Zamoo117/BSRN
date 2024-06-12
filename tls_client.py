import socket
import ssl

def run_tls_client(host, port):
    context = ssl.create_default_context()
    context.load_verify_locations(cafile="server.crt")
    
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            print("TLS connection established with", host)
            # Receive the encrypted message
            data = ssock.recv(1024)
            print("Received:", data.decode('utf-8'))

if __name__ == "__main__":
    run_tls_client('localhost', 8443)
