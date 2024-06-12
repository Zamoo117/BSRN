import socket

def run_non_tls_client(host, port):
    with socket.create_connection((host, port)) as sock:
        # Receive the plain text message
        data = sock.recv(1024)
        print("Received:", data.decode('utf-8'))

if __name__ == "__main__":
    run_non_tls_client('localhost', 8080)
