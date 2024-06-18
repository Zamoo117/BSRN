# http_client.py
import requests

def make_request(url='http://localhost:8081'):
    response = requests.get(url)
    print(f'Response: {response.text}')

if __name__ == "__main__":
    make_request()
