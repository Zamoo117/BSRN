import socket

#Nutzer auffordern Serveradresse, Nachricht und HTTP-Methode einzugeben
def user_input():
  server_address = input("Connect to (hostname or IP): ")
  message = input("Message: ")
  method = input("Method (GET, POST, DELETE): ").upper()

#Falls der Nutzer nicht TCP oder UDP als Server eingeben sollte dann wird er darauf aufgefordert es zu tun
if server_adress not in ["TCP-Server", "UDP-Server"]:
  print("Invalid Server address. Please enter either TCP-Server or UDP-Server.")
  return None, None, None

#Falls der Nutzer keine von den drei Methoden eingeben sollte dann wird er darauf hingewiesen es doch zutun 
if method not in ["GET", "POST", "DELETE"]:
  print("Invalid HTTP-method. Please enter one of the following methods: GET, POST, DELETE.")
  return None, None, None

return server_address, message, method

#Auflisten der verfügbaren Services und der zugehörigen UDP/TCP Ports
def list_services():
  services = ["http", "https"]
  print("Available services:")
  for service in services:
    try:
      tcp_port = socket.getservbyname(service, 'tcp')
      udp_port = socket.getservbyname(service, 'udp')
      print(f"{service}: TCP port {tcp_port}, UDP port {udp_port}")
    except socket.error:
      print(f"{service}: Service not found")

def main():
    print("Client")

if __name__ == "__main__":
    main()
