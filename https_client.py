import requests
import os

# Funktion, um eine HTTPS-Anfrage zu erstellen
def make_request(url='https://localhost:8443'):
    cert_path = os.path.abspath('ca_bundle.pem')  # Vollständiger Pfad zur Zertifikatsdatei
    print(f'Verifying with cert: {cert_path}')
    
    try:
        response = requests.get(url, verify=cert_path)  # Verwendet das Zertifikatsbundle zur Überprüfung
        print(f'Response status code: {response.status_code}')
        print(f'Response: {response.text}')
    except requests.exceptions.SSLError as e:
        print(f'SSL Error: {e}')
    except requests.exceptions.RequestException as e:
        print(f'Request Error: {e}')

# Überprüft, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    make_request()
