# Importiert das requests-Modul, um HTTP-Anfragen zu senden
import requests

# Funktion, um eine HTTP-Anfrage zu erstellen
def make_request(url='http://localhost:8081'):
    response = requests.get(url)  # Sendet eine GET-Anfrage an die angegebene URL
    print(f'Response: {response.text}')  # Gibt den Antworttext der Anfrage aus

# Überprüft, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    make_request()  # Führt die Funktion make_request aus
