# Importiert das requests-Modul, um HTTP- und HTTPS-Anfragen zu senden
import requests

# Funktion, um eine HTTPS-Anfrage zu erstellen
def make_request(url='https://localhost:8443', cert='path/to/cert.pem'):
    response = requests.get(url, verify=verify)  # Sendet eine GET-Anfrage an die angegebene URL, wobei die SSL-Zertifikatsprüfung deaktiviert ist
    print(f'Response: {response.text}')  # Gibt den Antworttext der Anfrage aus

# Überprüft, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    make_request()  # Führt die Funktion make_request aus
