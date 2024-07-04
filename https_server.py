# Importiert HTTPServer und SimpleHTTPRequestHandler aus dem http.server-Modul
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl  # Importiert das ssl-Modul zur Unterstützung von SSL/TLS

# Funktion zum Starten des HTTPS-Servers
def run_https_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8443):
    server_address = ('', port)  # Definiert die Serveradresse, '' bedeutet, dass der Server auf allen verfügbaren Interfaces lauscht
    httpd = server_class(server_address, handler_class)  # Erstellt eine Instanz des HTTP-Servers
    # Verpackt den Server-Socket mit SSL, verwendet das Zertifikat 'server.pem'
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server.pem', server_side=True)
    print(f'Starting HTTPS server on port {port}')  # Gibt eine Meldung aus, dass der Server gestartet wird
    httpd.serve_forever()  # Startet den Server und lässt ihn Anfragen unbegrenzt verarbeiten

# Überprüft, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    run_https_server()  # Führt die Funktion run_https_server aus und startet den Server auf Port 8443
