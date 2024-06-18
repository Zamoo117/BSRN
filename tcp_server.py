import http.server  # Importieren des HTTP-Server-Moduls
import socketserver  # Importieren des Socketserver-Moduls für die Netzwerkanbindung
import argparse  # Importieren des Argumentparser-Moduls für Kommandozeilenargumente
import logging  # Importieren des Logging-Moduls für Protokollierung

# Definition einer benutzerdefinierten HTTP-Anfrage-Handler-Klasse
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")  # Protokollierung der GET-Anfrage
        self.send_response(200)  # Senden einer HTTP-200-OK-Antwort
        self.end_headers()  # Beenden der Header-Sektion der Antwort
        self.wfile.write(b'Hello, GET request received!')  # Senden des Antwortinhalts

    def do_POST(self):
        content_length = self.headers.get('Content-Length')  # Abrufen des Content-Length-Headers
        if content_length is not None:
            content_length = int(content_length)  # Konvertieren des Content-Length-Werts in einen Integer
            post_data = self.rfile.read(content_length)  # Lesen der POST-Daten basierend auf Content-Length
            logging.info(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data.decode('utf-8')}\n")  # Protokollierung der POST-Anfrage
            self.send_response(200)  # Senden einer HTTP-200-OK-Antwort
            self.end_headers()  # Beenden der Header-Sektion der Antwort
            self.wfile.write(b'Hello, POST request received!')  # Senden des Antwortinhalts
        else:
            logging.error("POST request missing Content-Length header")  # Protokollierung des Fehlers bei fehlendem Content-Length-Header
            self.send_response(411)  # Senden einer HTTP-411-Length-Required-Antwort
            self.end_headers()  # Beenden der Header-Sektion der Antwort
            self.wfile.write(b'Missing Content-Length header')  # Senden des Fehlerinhalts

    def do_DELETE(self):
        logging.info(f"DELETE request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")  # Protokollierung der DELETE-Anfrage
        self.send_response(200)  # Senden einer HTTP-200-OK-Antwort
        self.end_headers()  # Beenden der Header-Sektion der Antwort
        self.wfile.write(b'Hello, DELETE request received!')  # Senden des Antwortinhalts

# Funktion zum Starten des HTTP-Servers
def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler):
    parser = argparse.ArgumentParser(description='Start the TCP server.')  # Initialisierung des Argumentparsers
    parser.add_argument('--host', default='localhost', help='Hostname to bind to')  # Hinzufügen des Host-Arguments
    parser.add_argument('--port', type=int, default=9000, help='Port to bind to')  # Hinzufügen des Port-Arguments
    parser.add_argument('--logfile', default='server.log', help='Log file path')  # Hinzufügen des Logfile-Arguments
    args = parser.parse_args()  # Parsen der Kommandozeilenargumente

    logging.basicConfig(filename=args.logfile, level=logging.INFO)  # Einrichten der Protokollierung
    server_address = (args.host, args.port)  # Festlegen der Serveradresse und des Ports
    httpd = server_class(server_address, handler_class)  # Erstellen des HTTP-Servers
    logging.info(f'Starting httpd server on {args.host}:{args.port}')  # Protokollierung des Serverstarts
    httpd.serve_forever()  # Starten des Servers

if __name__ == "__main__":
    run()  # Aufruf der run-Funktion, um den Server zu starten
