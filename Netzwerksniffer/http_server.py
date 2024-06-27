# Importiert SimpleHTTPRequestHandler und HTTPServer aus dem http.server-Modul
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Funktion zum Starten des HTTP-Servers
def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)  # Definiert die Serveradresse, '' bedeutet, dass der Server auf allen verfügbaren Interfaces lauscht
    httpd = server_class(server_address, handler_class)  # Erstellt eine Instanz des HTTP-Servers
    print(f'Starting HTTP server on port {port}')  # Gibt eine Meldung aus, dass der Server gestartet wird
    httpd.serve_forever()  # Startet den Server und lässt ihn Anfragen unbegrenzt verarbeiten

# Überprüft, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    run_server(port=8081)  # Startet den Server auf Port 8081
