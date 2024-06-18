import socket
import sys

def main():
    # Eingabe der Serveradresse durch den Benutzer
    server_address = input("IP-Address: ")

    # Eingabe des Servicetyps durch den Benutzer
    service_type = input("Connect to (TCP-Server, UDP-Server): ").strip().upper()

    # Validierung des Servicetyps
    if service_type not in ["TCP-SERVER", "UDP-SERVER"]:
        print("Invalid service type. Please enter either 'TCP-Server' or 'UDP-Server'.")
        sys.exit(1)

    # Eingabe der Nachricht durch den Benutzer
    message = input("Message: ")

    # Eingabe der HTTP-Methode durch den Benutzer
    method = input("Method (GET, POST, DELETE): ").strip().upper()

    # Validierung der HTTP-Methode
    if method not in ["GET", "POST", "DELETE"]:
        print("Invalid HTTP method. Please enter one of the following methods: GET, POST, DELETE.")
        sys.exit(1)

    # Umwandlung des Server-Hostnamens in eine IP-Adresse
    try:
        ip_address = socket.gethostbyname(server_address)
    except socket.error:
        print("Hostname could not be found.")
        sys.exit(1)

    # Erstellung des Payloads basierend auf den Benutzereingaben
    if method == "POST":
        content_length = len(message)
        payload = (f"{method} / HTTP/1.1\r\n"
                   f"Host: {ip_address}\r\n"
                   f"Content-Length: {content_length}\r\n"
                   f"Content-Type: text/plain\r\n"
                   f"\r\n"
                   f"{message}")
    else:
        payload = (f"{method} / HTTP/1.1\r\n"
                   f"Host: {ip_address}\r\n"
                   f"\r\n"
                   f"{message}")

    # Entscheiden, ob TCP oder UDP basierend auf dem Service
    if service_type == "TCP-SERVER":
        send_to_loadbalancer_tcp(ip_address, 8001, payload)
    else:
        send_to_loadbalancer_udp(ip_address, 8002, payload)

def send_to_loadbalancer_tcp(ip_address, port, payload):
    try:
        # Erstellung eines TCP-Sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Attempting to connect to {ip_address} on port {port} via TCP")
        # Verbindung zum Loadbalancer herstellen
        sock.connect((ip_address, port))
        print(f"Connected to Loadbalancer: {ip_address}:{port}")

        # Senden des Payloads
        sock.sendall(payload.encode())

        # Empfang der Antwort vom Loadbalancer
        response = sock.recv(4096)
        print("Response from Loadbalancer:")
        print(response.decode())

    except socket.error as e:
        print(f"Socket-Error: {e}")
    finally:
        sock.close()

def send_to_loadbalancer_udp(ip_address, port, payload):
    try:
        # Erstellung eines UDP-Sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Attempting to connect to {ip_address} on port {port} via UDP")
        # Senden des Payloads
        sock.sendto(payload.encode(), (ip_address, port))
        print(f"Sent data to Loadbalancer: {ip_address}:{port}")

        # Empfang der Antwort vom Loadbalancer
        response, _ = sock.recvfrom(4096)
        print("Response from Loadbalancer:")
        print(response.decode())

    except socket.error as e:
        print(f"Socket-Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
