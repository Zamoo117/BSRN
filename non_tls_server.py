import socket

def run_non_tls_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        print("Non-TLS Server listening on port", port)
        
        conn, addr = sock.accept()
        with conn:
            print("Connection from", addr)
            
            # Send a plain text message
            payload = "This is a readable message".encode('utf-8')
            conn.send(payload)

if __name__ == "__main__":
    run_non_tls_server('0.0.0.0', 8080)
