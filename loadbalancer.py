import socket  # Importieren des Socket-Moduls für die Netzwerkkommunikation
import threading  # Importieren des Threading-Moduls für parallele Verarbeitung
import logging  # Importieren des Logging-Moduls für Protokollierung

# Einrichten der Basisprotokollierung
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Erstellen eines Loggers

# TCP Handler
def handle_tcp(client_socket, backend_host, backend_port):
    backend_socket = None  # Initialisieren der Backend-Socket-Variable
    try:
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Erstellen eines TCP-Sockets für das Backend
        logger.info(f"Connecting to backend TCP server at {backend_host}:{backend_port}")
        backend_socket.connect((backend_host, backend_port))  # Verbindung zum Backend-Server herstellen
        
        # Erstellen und Starten der Threads für das Weiterleiten der Daten
        client_to_backend = threading.Thread(target=forward, args=(client_socket, backend_socket, "client_to_backend"))
        backend_to_client = threading.Thread(target=forward, args=(backend_socket, client_socket, "backend_to_client"))
        
        client_to_backend.start()
        backend_to_client.start()
        
        client_to_backend.join()
        backend_to_client.join()
    except Exception as e:
        logger.error(f"Error handling TCP connection: {e}")
    finally:
        try:
            # Sicheres Schließen der Sockets
            if client_socket:
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
            if backend_socket:
                backend_socket.shutdown(socket.SHUT_RDWR)
                backend_socket.close()
        except Exception as e:
            logger.error(f"Error closing sockets: {e}")

# Funktion zum Weiterleiten von Daten zwischen Sockets
def forward(source, destination, direction):
    try:
        while True:
            data = source.recv(4096)  # Empfangen von Daten vom Quell-Socket
            if not data:
                break
            destination.sendall(data)  # Senden der Daten an den Ziel-Socket
            logger.info(f"Forwarding data {direction}: {data}")
    except Exception as e:
        logger.error(f"Error forwarding data {direction}: {e}")
    finally:
        try:
            # Sicheres Schließen der Sockets
            if source:
                source.shutdown(socket.SHUT_RDWR)
                source.close()
            if destination:
                destination.shutdown(socket.SHUT_RDWR)
                destination.close()
        except Exception as e:
            logger.error(f"Error closing sockets {direction}: {e}")

# UDP Handler
def handle_udp(server_socket, backend_host, backend_port):
    while True:
        try:
            data, client_address = server_socket.recvfrom(4096)  # Empfangen von UDP-Daten vom Client
            logger.info(f"Received UDP data from {client_address}: {data}")
            backend_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Erstellen eines UDP-Sockets für das Backend
            backend_socket.sendto(data, (backend_host, backend_port))  # Senden der Daten an das Backend
            response, _ = backend_socket.recvfrom(4096)  # Empfang der Antwort vom Backend
            server_socket.sendto(response, client_address)  # Senden der Antwort an den Client
            backend_socket.close()  # Schließen des Backend-Sockets
            logger.info(f"Forwarded UDP response to {client_address}")
        except Exception as e:
            logger.error(f"Error handling UDP connection: {e}")

# Starten des Loadbalancers
def start_load_balancer(tcp_port, udp_port, tcp_backend_host, tcp_backend_port, udp_backend_host, udp_backend_port):
    # Einrichten des TCP-Servers
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('0.0.0.0', tcp_port))
    tcp_server_socket.listen(5)
    logger.info(f"TCP Load Balancer listening on port {tcp_port}")

    # Einrichten des UDP-Servers
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(('0.0.0.0', udp_port))
    logger.info(f"UDP Load Balancer listening on port {udp_port}")

    # Starten des UDP-Handlers in einem separaten Thread
    threading.Thread(target=handle_udp, args=(udp_server_socket, udp_backend_host, udp_backend_port)).start()

    while True:
        client_socket, address = tcp_server_socket.accept()  # Akzeptieren eingehender TCP-Verbindungen
        logger.info(f"Accepted connection from {address}")
        # Starten des TCP-Handlers in einem separaten Thread
        threading.Thread(target=handle_tcp, args=(client_socket, tcp_backend_host, tcp_backend_port)).start()

if __name__ == "__main__":
    tcp_port = 8001  # Port für eingehende TCP-Verbindungen
    udp_port = 8002  # Port für eingehende UDP-Verbindungen
    tcp_backend_host = '127.0.0.1'  # Adresse des Backend-TCP-Servers
    tcp_backend_port = 9000  # Port des Backend-TCP-Servers
    udp_backend_host = '127.0.0.1'  # Adresse des Backend-UDP-Servers
    udp_backend_port = 8000  # Port des Backend-UDP-Servers

    # Starten des Loadbalancers mit den angegebenen Parametern
    start_load_balancer(tcp_port, udp_port, tcp_backend_host, tcp_backend_port, udp_backend_host, udp_backend_port)
