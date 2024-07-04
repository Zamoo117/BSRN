import sys  # Interagiert mit dem Python-Interpreter
import base64  # Kodiert und dekodiert Daten in Base64
import json  # Arbeitet mit JSON-Daten
import argparse  # Parst Kommandozeilenargumente
import psutil  # Erhält System- und Netzwerkinformationen
import socket  # Arbeitet mit Netzwerksockets
from scapy.all import sniff, Raw, IP, UDP, TCP  # Importiert Scapy-Funktionen und Klassen

def packet_handler(packet, detailed):
    """
    Diese Funktion wird für jedes gesniffte Paket aufgerufen und verarbeitet das Paket.
    """
    src_ip = packet[IP].src if IP in packet else "Unknown"
    dst_ip = packet[IP].dst if IP in packet else "Unknown"
    src_port = packet[UDP].sport if UDP in packet else packet[TCP].sport if TCP in packet else "Unknown"
    dst_port = packet[UDP].dport if UDP in packet else packet[TCP].dport if TCP in packet else "Unknown"
    protocol = "UDP" if UDP in packet else "TCP" if TCP in packet else "Unknown"
    payload = base64.b64encode(packet[Raw].load).decode('ascii') if Raw in packet else None

    print(f"Source IP: {src_ip}")
    print(f"Source Port: {src_port}")
    print(f"Destination IP: {dst_ip}")
    print(f"Destination Port: {dst_port}")
    print(f"Protocol: {protocol}")

    if detailed:
        if payload:
            print("Payload:", payload)
    else:
        if payload:
            print("Payload (truncated):", payload[:50] + '...')

    print('-' * 40)

    packet_data = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol,
        "payload": payload
    }

    with open("output.json", "a") as f:
        json.dump(packet_data, f)
        f.write("\n")

def read_saved_data(filename):
    """
    Diese Funktion liest gespeicherte JSON-Daten aus einer Datei und gibt sie aus.
    """
    try:
        with open(filename, "r") as file:
            for line in file:
                data = json.loads(line)
                print(data)
    except FileNotFoundError:
        print("Die angegebene Datei wurde nicht gefunden.")
    except json.JSONDecodeError:
        print("Fehler beim Decodieren der JSON-Daten.")

def list_interfaces():
    """
    Diese Funktion listet alle verfügbaren Netzwerkinterfaces und ihre IP- und MAC-Adressen auf.
    """
    print("Verfügbare Interfaces:")
    for iface, addrs in psutil.net_if_addrs().items():
        ip = None
        mac = None
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac = addr.address
            elif addr.family == socket.AF_INET:
                ip = addr.address
        print(f"{iface} - IP: {ip}, MAC: {mac}")

def parse_arguments():
    """
    Diese Funktion parst die Kommandozeilenargumente.
    """
    parser = argparse.ArgumentParser(description="Network Sniffer")
    parser.add_argument("-i", "--interface", help="Interface to sniff packets on", required=False)
    parser.add_argument("-c", "--count", help="Number of packets to sniff", type=int, default=10)
    parser.add_argument("-r", "--read", help="Read and display the saved data", action="store_true")
    parser.add_argument("-l", "--list", help="List available interfaces", action="store_true")
    parser.add_argument("-d", "--detailed", help="Show detailed output including full payloads", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    # Parsing der Kommandozeilenargumente
    args = parse_arguments()

    if args.list:
        # Liste der verfügbaren Netzwerkinterfaces anzeigen
        list_interfaces()
    elif args.read:
        # Lese und zeige die gespeicherten Daten an
        read_saved_data("output.json")
    else:
        if not args.interface:
            print("Bitte geben Sie ein Interface zum Sniffen an.")
            sys.exit(1)
        # Öffne eine Datei im Schreibmodus (falls vorhanden, wird sie überschrieben)
        with open("output.json", "w") as f:
            # Führe den Code aus, dessen Ausgabe du speichern möchtest
            try:
                sniff(iface=args.interface, prn=lambda x: packet_handler(x, args.detailed), count=args.count)
            except PermissionError:
                print("Erlaubnis verweigert. Bitte führen Sie das Skript mit root-Rechten aus.")
