import sys  # Importiert das sys-Modul, um mit dem Python-Interpreter zu interagieren
import base64  # Importiert das base64-Modul, um Daten in Base64 zu kodieren und dekodieren
import json  # Importiert das json-Modul, um mit JSON-Daten zu arbeiten
import argparse  # Importiert das argparse-Modul, um Kommandozeilenargumente zu parsen
import psutil  # Importiert das psutil-Modul, um System- und Netzwerkinformationen zu erhalten
import socket  # Importiert das socket-Modul, um mit Netzwerksockets zu arbeiten
from scapy.all import sniff, Raw, IP, UDP, TCP  # Importiert Funktionen und Klassen aus Scapy, einem Netzwerkpaketmodul

def packet_handler(packet, detailed):
    """
    Diese Funktion wird für jedes gesniffte Paket aufgerufen und verarbeitet das Paket.
    """
    # Extrahieren relevanter Informationen aus dem Paket
    src_ip = packet[IP].src if IP in packet else "Unknown"  # Quell-IP-Adresse des Pakets, wenn vorhanden
    dst_ip = packet[IP].dst if IP in packet else "Unknown"  # Ziel-IP-Adresse des Pakets, wenn vorhanden
    src_port = packet[UDP].sport if UDP in packet else packet[TCP].sport if TCP in packet else "Unknown"  # Quellport, falls UDP oder TCP
    dst_port = packet[UDP].dport if UDP in packet else packet[TCP].dport if TCP in packet else "Unknown"  # Zielport, falls UDP oder TCP
    protocol = "UDP" if UDP in packet else "TCP" if TCP in packet else "Unknown"  # Protokolltyp (UDP/TCP), falls vorhanden
    payload = base64.b64encode(packet[Raw].load).decode('ascii') if Raw in packet else None  # Nutzlast (Payload) des Pakets in Base64 kodieren, falls vorhanden

    # Ausgabe der extrahierten Informationen
    print(f"Source IP: {src_ip}")  # Ausgabe der Quell-IP-Adresse
    print(f"Source Port: {src_port}")  # Ausgabe des Quellports
    print(f"Destination IP: {dst_ip}")  # Ausgabe der Ziel-IP-Adresse
    print(f"Destination Port: {dst_port}")  # Ausgabe des Zielports
    print(f"Protocol: {protocol}")  # Ausgabe des Protokolltyps

    if detailed:  # Wenn detaillierte Ausgabe aktiviert ist
        if payload:
            print("Payload:", payload)  # Ausgabe der vollständigen Payload, wenn vorhanden
    else:
        if payload:
            print("Payload (truncated):", payload[:50] + '...')  # Ausgabe der gekürzten Payload, wenn vorhanden

    print('-' * 40)  # Trenner zwischen Paketen

    # JSON-Objekt mit den extrahierten Informationen erstellen
    packet_data = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol,
        "payload": payload
    }

    # JSON-Objekt als Zeichenkette formatieren und in eine Datei schreiben
    with open("output.json", "a") as f:
        json.dump(packet_data, f)  # JSON-Objekt in die Datei schreiben
        f.write("\n")  # Neue Zeile nach jedem JSON-Objekt hinzufügen

def read_saved_data(filename):
    """
    Diese Funktion liest gespeicherte JSON-Daten aus einer Datei und gibt sie aus.
    """
    try:
        with open(filename, "r") as file:
            # Lese jede Zeile und dekodiere das JSON-Objekt
            for line in file:
                data = json.loads(line)  # JSON-Daten aus der Zeile laden
                print(data)  # Ausgabe der JSON-Daten
    except FileNotFoundError:
        print("Die angegebene Datei wurde nicht gefunden.")  # Fehler, wenn die Datei nicht gefunden wurde
    except json.JSONDecodeError:
        print("Fehler beim Decodieren der JSON-Daten.")  # Fehler beim Decodieren der JSON-Daten

def list_interfaces():
    """
    Diese Funktion listet alle verfügbaren Netzwerkinterfaces und ihre IP- und MAC-Adressen auf.
    """
    print("Verfügbare Interfaces:")
    for iface, addrs in psutil.net_if_addrs().items():  # Iteriert über alle Netzwerkinterfaces
        ip = None
        mac = None
        for addr in addrs:  # Iteriert über alle Adressen eines Interfaces
            if addr.family == psutil.AF_LINK:  # Wenn die Adresse eine MAC-Adresse ist
                mac = addr.address
            elif addr.family == socket.AF_INET:  # Wenn die Adresse eine IP-Adresse ist
                ip = addr.address
        print(f"{iface} - IP: {ip}, MAC: {mac}")  # Ausgabe des Interfaces mit IP- und MAC-Adresse

def parse_arguments():
    """
    Diese Funktion parst die Kommandozeilenargumente.
    """
    parser = argparse.ArgumentParser(description="Network Sniffer")  # Erstellen eines Argumentparsers mit Beschreibung
    parser.add_argument("-i", "--interface", help="Interface to sniff packets on", required=False)  # Argument für das zu sniffende Interface
    parser.add_argument("-c", "--count", help="Number of packets to sniff", type=int, default=10)  # Argument für die Anzahl der zu sniffenden Pakete
    parser.add_argument("-r", "--read", help="Read and display the saved data", action="store_true")  # Argument zum Lesen und Anzeigen der gespeicherten Daten
    parser.add_argument("-l", "--list", help="List available interfaces", action="store_true")  # Argument zum Auflisten der verfügbaren Interfaces
    parser.add_argument("-d", "--detailed", help="Show detailed output including full payloads", action="store_true")  # Argument für detaillierte Ausgabe
    return parser.parse_args()  # Parsen der übergebenen Argumente

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
            sniff(iface=args.interface, prn=lambda x: packet_handler(x, args.detailed), count=args.count)
