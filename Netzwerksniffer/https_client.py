import requests

def make_request(url='https://localhost:8443', verify=False):
    response = requests.get(url, verify=verify)
    print(f'Response: {response.text}')

if __name__ == "__main__":
    make_request()
