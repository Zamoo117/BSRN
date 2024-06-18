#  Dieses Thema wurde von Matin auf Amines Laptop bearbeitet, da es zu Problemen kam auf dem Github von Matin


import socket
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TCP Handler
def handle_tcp(client_socket, address, backend_host, backend_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_socket:
            backend_socket.connect((backend_host, backend_port))
            threading.Thread(target=forward, args=(client_socket, backend_socket)).start()
            threading.Thread(target=forward, args=(backend_socket, client_socket)).start()
    except Exception as e:
        logger.error(f"Error handling TCP connection: {e}")
    finally:
        client_socket.close()

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except Exception as e:
        logger.error(f"Error forwarding data: {e}")
    finally:
        source.close()
        destination.close()      
# UDP Handler
def handle_udp(server_socket, backend_host, backend_port):
    while True:
        try:
            data, client_address = server_socket.recvfrom(4096)
            backend_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            backend_socket.sendto(data, (backend_host, backend_port))
            response, _ = backend_socket.recvfrom(4096)
            server_socket.sendto(response, client_address)
            backend_socket.close()
        except Exception as e:
            logger.error(f"Error handling UDP connection: {e}")

# Start Loadbalancer
def start_load_balancer(tcp_port, udp_port, tcp_backend_host, tcp_backend_port, udp_backend_host, udp_backend_port):
    # TCP Server
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('0.0.0.0', tcp_port))
    tcp_server_socket.listen(5)
    logger.info(f"TCP Load Balancer listening on port {tcp_port}")

    # UDP Server
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(('0.0.0.0', udp_port))
    logger.info(f"UDP Load Balancer listening on port {udp_port}")

    threading.Thread(target=handle_udp, args=(udp_server_socket, udp_backend_host, udp_backend_port)).start()
    while True:
        client_socket, address = tcp_server_socket.accept()
        logger.info(f"Accepted connection from {address}")
        threading.Thread(target=handle_tcp, args=(client_socket, address, tcp_backend_host, tcp_backend_port)).start()

if __name__ == "__start_load_loadbalancer__":
    tcp_port = 8001
    udp_port = 8000
    tcp_backend_host = '127.0.0.1'
    tcp_backend_port = 9000
    udp_backend_host = '127.0.0.1'
    udp_backend_port = 9001

    start_load_balancer(tcp_port, udp_port, tcp_backend_host, tcp_backend_port, udp_backend_host, udp_backend_port)