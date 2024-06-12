import re
import base64
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Sample log data
log_data = """
Source IP: 172.16.5.4
Source Port: 58352
Destination IP: 20.103.221.187
Destination Port: 443
Protocol: TCP
Payload: FwMDAG/i2xpsZ6Ki5s6jjO5dM3E6dJOSJZBNYMxhGqif23yBNwZVE3EgYqUftmScb9YOz+Whn/ed3sh6JaZae50vryr49RgSS5Qm/wYjWfzJUQcfOxxaKJqggJBlGCyjBMJAMFtTtSBvU1zdjGZz8fOPROQ=
----------------------------------------
Source IP: 20.103.221.187
Source Port: 443
Destination IP: 172.16.5.4
Destination Port: 58352
Protocol: TCP
----------------------------------------
Source IP: 20.103.221.187
Source Port: 443
Destination IP: 172.16.5.4
Destination Port: 58352
Protocol: TCP
Payload: FwMDAV1He/rCqJbaGWlUJ/jzCy9Ga+7GHDbpbsVclEcyDurr0kjCS4DS4tuKS6KGaC6CLWAdHT6s37n64bh37tjsg1Q9X7QzBMlj07g06XlTkLIqtbkfGXORVNTcHm4RorQtd/VH9vkKYd0+mbudblhX1Dkt4Pi3l5O4ONSKDIdmcyLchHYR0Mq76SrMcqkUf0ZM/67aTpXGd0WRrkrqc1xoHD51Zcr7fh7CcaJQGRRuGVMMJ9SIvxrM3o0jx3e5REv8eteMabFyFufma2n0P44VFU3fOg3/iyjP8ZjnrNVGmabY/yYhq+e7clErdbZsKmAkTYr9YBJMmBkLorP6W455Q2GIgFjHKJmxlhY9oOrqcxfl11Px8v5alkaR0a10Cfrtk8L/15LZjRCkU8JCiC1rHkjShD4MA+3k/dUyMA1qTKlYkE3c2uIqi7n1rgy0XI6qMAck2gRN+SNysYnr9S9I
----------------------------------------
Source IP: 172.16.5.4
Source Port: 58352
Destination IP: 20.103.221.187
Destination Port: 443
Protocol: TCP
Payload: FwMDAG+bC95xXY1Cd4gQPCfg2EE55f6mCLQM9Ps+gTihAfaUBkJ+cD5yYZsDdeqxVzzK0KsG/HlWDNGvj+9wlQIpaC3vxane2v67XUnnkPSjxkBBkCUiEJji0O56uLR/ir4EyfjiMVR/9zq4kOD7SqUIvKc=
----------------------------------------
Source IP: 172.16.5.4
Source Port: 58352
Destination IP: 20.103.221.187
Destination Port: 443
Protocol: TCP
Payload: FwMDAG8Lz16zhXG1d5X+MewL95gJalHHrpCCYzwgYlJy0tzciZwPMraDPuatwvGIYrDQtXGM9zFAMcwo7a+8E/VrTKugpIHLnyqBQA2G6+Cuk0NkU7Q1dzCUScNG7QXgTH/4K9XDaoAaA8IBwKIiwe5fFJg=
----------------------------------------
"""

# Define regex patterns for extracting log entries
entry_pattern = re.compile(
    r"Source IP: (?P<source_ip>[0-9.]+)\n"
    r"Source Port: (?P<source_port>\d+)\n"
    r"Destination IP: (?P<destination_ip>[0-9.]+)\n"
    r"Destination Port: (?P<destination_port>\d+)\n"
    r"Protocol: (?P<protocol>[A-Z]+)(?:\nPayload: (?P<payload>[A-Za-z0-9+/=\s]+))?\n----------------------------------------"
)

# Function to determine if the payload indicates TLS
def tlsChecker(payload):
    """
    Check if the payload is a TLS payload.
    This function checks for the TLS record layer, which is indicated by:
    - Content Type for Handshake: 0x16
    - Content Type for Application Data: 0x17
    - Version TLS 1.0: 0x0301
    - Version TLS 1.1: 0x0302
    - Version TLS 1.2: 0x0303
    """
    logging.debug(f"Checking payload: {payload}")  # Debug statement
    if len(payload) > 5:
        content_type = payload[0]
        version = payload[1:3]
        record_length = int.from_bytes(payload[3:5], 'big')
        logging.debug(f"Content Type: {content_type}, Version: {version}, Record Length: {record_length}")

        # Check for valid content type and version
        if content_type in {0x16, 0x17} and version in {b'\x03\x01', b'\x03\x02', b'\x03\x03'}:
            # Ensure payload length matches record length
            if record_length <= len(payload[5:]):
                # Further check the handshake type if content_type is handshake
                if content_type == 0x16:
                    handshake_type = payload[5]
                    logging.debug(f"Handshake Type: {handshake_type}")
                    if handshake_type in {0x01, 0x02, 0x0b, 0x0e}:  # Ensure valid handshake types
                        logging.debug("TLS Handshake Detected")
                        return True
                    else:
                        logging.debug("Invalid Handshake Type, Not TLS")
                        return False
                elif content_type == 0x17:
                    logging.debug("TLS Application Data Detected")
                    return True
            else:
                logging.debug("Length Mismatch, Not TLS")
        else:
            logging.debug("Not TLS based on Content Type or Version")
    return False

def is_tls(payload):
    if payload:
        try:
            # Decode the base64 payload
            decoded_payload = base64.b64decode(payload.replace('\n', ''))
            logging.debug(f"Decoded payload: {decoded_payload}")  # Debug statement
            # Use the tlsChecker function to determine if it's a TLS payload
            return tlsChecker(decoded_payload)
        except Exception as e:
            logging.debug(f"Exception during payload check: {e}")  # Debug statement
            pass
    return False

# Parse log entries
entries = [match.groupdict() for match in entry_pattern.finditer(log_data)]

# Analyze entries to determine if they are TLS or non-TLS
for entry in entries:
    logging.debug(f"Checking entry: {entry}")  # Debug statement
    tls = is_tls(entry.get("payload", None))
    logging.info(f"Source IP: {entry['source_ip']} | Source Port: {entry['source_port']} | "
                 f"Destination IP: {entry['destination_ip']} | Destination Port: {entry['destination_port']} | "
                 f"Protocol: {entry['protocol']} | TLS: {'Yes' if tls else 'No'}")

# Check if we can reach an external URL as an additional test
try:
    response = requests.get("https://www.example.com")
    if response.status_code == 200:
        logging.info("Successfully reached https://www.example.com")
    else:
        logging.warning("Failed to reach https://www.example.com")
except requests.RequestException as e:
    logging.error(f"Error reaching https://www.example.com: {e}")
