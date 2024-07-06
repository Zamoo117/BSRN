import sys  # Ermöglicht die Interaktion mit dem Python-Interpreter
import base64  # Kodiert und dekodiert Daten in Base64-Format
import json  # Arbeitet mit JSON-Daten, um sie zu lesen und zu schreiben
import argparse  # Parst Kommandozeilenargumente, um die Benutzung des Skripts flexibel zu gestalten
import psutil  # Erhält System- und Netzwerkinformationen, ähnlich wie ein Systemmonitor
import socket  # Arbeitet mit Netzwerksockets, um Verbindungen zu verwalten
from scapy.all import sniff, Raw, IP, UDP, TCP  # Importiert Scapy-Funktionen zum Sniffen und Verarbeiten von Paketen

def packet_handler(packet, detailed):
    """
    Diese Funktion wird für jedes gesniffte Paket aufgerufen und verarbeitet das Paket.
    """
    # Bestimmt die Quell-IP-Adresse des Pakets
    src_ip = packet[IP].src if IP in packet else "Unknown"
    # Bestimmt die Ziel-IP-Adresse des Pakets
    dst_ip = packet[IP].dst if IP in packet else "Unknown"
    # Bestimmt den Quellport des Pakets (entweder UDP oder TCP)
    src_port = packet[UDP].sport if UDP in packet else packet[TCP].sport if TCP in packet else "Unknown"
    # Bestimmt den Zielport des Pakets (entweder UDP oder TCP)
    dst_port = packet[UDP].dport if UDP in packet else packet[TCP].dport if TCP in packet else "Unknown"
    # Bestimmt das Protokoll des Pakets (entweder UDP oder TCP)
    protocol = "UDP" if UDP in packet else "TCP" if TCP in packet else "Unknown"
    # Kodiert die Nutzlast des Pakets in Base64, falls vorhanden
    payload = base64.b64encode(packet[Raw].load).decode('ascii') if Raw in packet else None

    # Ausgabe der Paketinformationen
    print(f"Source IP: {src_ip}")
    print(f"Source Port: {src_port}")
    print(f"Destination IP: {dst_ip}")
    print(f"Destination Port: {dst_port}")
    print(f"Protocol: {protocol}")

    # Detaillierte Ausgabe der Nutzlast
    if detailed:
        if payload:
            print("Payload:", payload)
    else:
        if payload:
            print("Payload (truncated):", payload[:50] + '...')

    print('-' * 40)

    # Erstellen eines Wörterbuchs mit den Paketdaten
    packet_data = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol,
        "payload": payload
    }

    # Speichern der Paketdaten in einer JSON-Datei
    with open("output.json", "a") as f:
        json.dump(packet_data, f)
        f.write("\n")

def read_saved_data(filename):
    """
    Diese Funktion liest gespeicherte JSON-Daten aus einer Datei und gibt sie aus.
    """
    try:
        # Öffnen der Datei im Lesemodus
        with open(filename, "r") as file:
            # Lesen und Ausgeben jeder Zeile der Datei
            for line in file:
                data = json.loads(line)  # JSON-Daten aus der Datei dekodieren
                print(data)  # JSON-Daten ausgeben
    except FileNotFoundError:
        print("Die angegebene Datei wurde nicht gefunden.")
    except json.JSONDecodeError:
        print("Fehler beim Decodieren der JSON-Daten.")

def list_interfaces():
    """
    Diese Funktion listet alle verfügbaren Netzwerkinterfaces und ihre IP- und MAC-Adressen auf.
    """
    print("Verfügbare Interfaces:")
    # Durch alle verfügbaren Interfaces iterieren und ihre Adressen abrufen
    for iface, addrs in psutil.net_if_addrs().items():
        ip = None
        mac = None
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac = addr.address  # MAC-Adresse abrufen
            elif addr.family == socket.AF_INET:
                ip = addr.address  # IP-Adresse abrufen
        print(f"{iface} - IP: {ip}, MAC: {mac}")  # Interface-Informationen ausgeben

def parse_arguments():
    """
    Diese Funktion parst die Kommandozeilenargumente.
    """
    parser = argparse.ArgumentParser(description="Network Sniffer")
    # Argumente für das Skript definieren
    parser.add_argument("-i", "--interface", help="Interface to sniff packets on", required=False)
    parser.add_argument("-c", "--count", help="Number of packets to sniff", type=int, default=10)
    parser.add_argument("-r", "--read", help="Read and display the saved data", action="store_true")
    parser.add_argument("-l", "--list", help="List available interfaces", action="store_true")
    parser.add_argument("-d", "--detailed", help="Show detailed output including full payloads", action="store_true")
    return parser.parse_args()  # Geparste Argumente zurückgeben

if __name__ == "__main__":
    # Parsing der Kommandozeilenargumente
    args = parse_arguments()

    # Wenn das Argument "--list" übergeben wurde, verfügbare Netzwerkinterfaces anzeigen
    if args.list:
        list_interfaces()
    # Wenn das Argument "--read" übergeben wurde, gespeicherte Daten lesen und anzeigen
    elif args.read:
        read_saved_data("output.json")
    else:
        # Wenn kein Interface angegeben wurde, Fehlermeldung ausgeben und Programm beenden
        if not args.interface:
            print("Bitte geben Sie ein Interface zum Sniffen an.")
            sys.exit(1)
        # Öffne eine Datei im Schreibmodus (falls vorhanden, wird sie überschrieben)
        with open("output.json", "w") as f:
            # Pakete auf dem angegebenen Interface sniffern und verarbeiten
            try:
                sniff(iface=args.interface, prn=lambda x: packet_handler(x, args.detailed), count=args.count)
            # Falls keine ausreichenden Berechtigungen vorliegen, Fehlermeldung ausgeben
            except PermissionError:
                print("Erlaubnis verweigert. Bitte führen Sie das Skript mit root-Rechten aus.")
