import requests

def make_request(url='https://localhost:8443', cert='ca_bundle.pem'):
    print(f'Verifying with cert: {cert}')
    try:
        response = requests.get(url, verify=cert)
        print(f'Response: {response.text}')
    except requests.exceptions.SSLError as e:
        print(f'SSL Error: {e}')

if __name__ == "__main__":
    make_request()
