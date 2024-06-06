import socket
def start_udp_server(host='localhost', port=8000):
    # Erstellen des UDP Sockets 
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    
    print(f"UDP server listening on {host}:{port}")
    
    while True:
        # Datenempfang des Clients
        data, client_address = server_socket.recvfrom(1024)
        print(f"Received message: {data.decode()} from {client_address}")
        
        # Senden einer Antwort an den Client
        response = f"Echo: {data.decode()}"
        server_socket.sendto(response.encode(), client_address)
if __name__=="__main__":
    start_udp_server()
        
