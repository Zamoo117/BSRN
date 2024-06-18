import socket
import argparse
import logging

def start_udp_server(host, port, logfile):
    # Set up logging
    logging.basicConfig(filename=logfile, level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Erstellen des UDP Sockets 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    logger.info(f"UDP server listening on {host}:{port}")
    
    while True:
        # Datenempfang des Clients
        data, client_address = server_socket.recvfrom(1024)
        logger.info(f"Received message: {data.decode()} from {client_address}")
        
        # Senden einer Antwort an den Client
        response = f"Echo: {data.decode()}"
        server_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start the UDP server.')
    parser.add_argument('--host', default='localhost', help='Hostname to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--logfile', default='udp_server.log', help='Log file path')
    args = parser.parse_args()

    start_udp_server(args.host, args.port, args.logfile)
