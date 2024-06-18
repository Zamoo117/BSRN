import socket  # Importieren des Socket-Moduls für die Netzwerkkommunikation
import argparse  # Importieren des Argumentparser-Moduls für Kommandozeilenargumente
import logging  # Importieren des Logging-Moduls für Protokollierung

# Funktion zum Starten des UDP-Servers
def start_udp_server(host, port, logfile):
    # Einrichten der Protokollierung
    logging.basicConfig(filename=logfile, level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Erstellen des UDP-Sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))  # Binden des Sockets an die angegebene Adresse und den Port
    
    logger.info(f"UDP server listening on {host}:{port}")
    
    while True:
        # Datenempfang vom Client
        data, client_address = server_socket.recvfrom(1024)  # Empfangen von Daten vom Client
        logger.info(f"Received message: {data.decode()} from {client_address}")
        
        # Senden einer Antwort an den Client
        response = f"Echo: {data.decode()}"  # Erstellen der Antwortnachricht
        server_socket.sendto(response.encode(), client_address)  # Senden der Antwort an den Client

if __name__ == "__main__":
    # Initialisierung des Argumentparsers
    parser = argparse.ArgumentParser(description='Start the UDP server.')
    parser.add_argument('--host', default='localhost', help='Hostname to bind to')  # Hinzufügen des Host-Arguments
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')  # Hinzufügen des Port-Arguments
    parser.add_argument('--logfile', default='udp_server.log', help='Log file path')  # Hinzufügen des Logfile-Arguments
    args = parser.parse_args()  # Parsen der Kommandozeilenargumente

    # Starten des UDP-Servers mit den angegebenen Parametern
    start_udp_server(args.host, args.port, args.logfile)
