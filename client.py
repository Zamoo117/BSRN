import socket
import sys

def main():
    #Eingabe der Serveradresse durch den Benutzer
    server_address = input("Connect to (hostname or IP): ")

    #Eingabe der Nachricht durch den Benutzer
    message = input("Message: ")

    #Eingabe der HTTP-Methode durch den Benutzer
    method = input("Method (GET, POST, DELETE): ").strip().upper()

    #Validierung der HTTP-Methode
    if method not in ["GET", "POST", "DELETE"]:
        print("Invalid HTTP-method. Please enter one of the following methods: GET, POST, DELETE.")
        sys.exit(1)

    #Eingabe des Servicenamens durch den Benutzer
    service_name = input("Servicename (http, https): ").strip().lower()

    #Umwandlung des Servicenamens in einen Port
    try:
        port = socket.getservbyname(service_name, 'tcp')
    except socket.error:
        print("Service could not be found.")
        sys.exit(1)

    #Umwandlung des Server-Hostnamens in eine IP-Adresse
    try:
        ip_address = socket.gethostbyname(server_address)
    except socket.gaierror:
        print("Hostname could not be found.")
        sys.exit(1)

    #Erstellung des Payloads basierend auf den Benutzereingaben
    payload = f"{method} / HTTP/1.1\r\nHost: {ip_address}:{port}\r\n\r\n{message}"

    #Senden des Payloads an den Loadbalancer
    send_to_loadbalancer(ip_address, port, payload)

def send_to_loadbalancer(ip_address, port, payload):
    try:
        #Erstellung eines TCP-Sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Verbindung zum Loadbalancer herstellen
        sock.connect((ip_address, port))
        print(f"Connected to Loadbalancer: {ip_address}:{port}")

        #Senden des Payloads
        sock.sendall(payload.encode())

        #Empfang der Antwort vom Loadbalancer
        response = sock.recv(4096)
        print("Response from Loadbalancer:")
        print(response.decode())

    except socket.error as e:
        print(f"Socket-Error: {e}")

if __name__ == "__main__":
    main()
