# BSRN
Werkstück 4, Client-Server-Anwendung

Ziel: Erstellen eines einfachen Netzwerk-Sniffers, welcher Netzwerkpakete erfasst und diese analysiert.

// Kurze Zusammenfassung der wichtigsten Punkte:

### Zusammenfassung

1. Projektstruktur und Dateien:
   - `netzwerkSniffer.py`: Hauptskript für das Sniffen und die Verarbeitung von Netzwerkpaketen.
   - `requirements.txt`: Listet die benötigten Python-Pakete (`scapy`, `psutil`) auf.
   - `README.md`: Dokumentation zur Installation und Nutzung des Projekts.

2. Wichtige Befehle:
   - Interfaces auflisten:
     ```bash
     python netzwerkSniffer.py --list
     ```
   - Pakete sniffen mit verkürzter Payload:
     ```bash
     sudo /workspaces/BSRN/.venv/bin/python /workspaces/BSRN/netzwerkSniffer.py -i "interfacehiereingeben" -c 100
     ```
   - Pakete sniffen mit detaillierter Payload:
     ```bash
     sudo /workspaces/BSRN/.venv/bin/python /workspaces/BSRN/netzwerkSniffer.py -i "interfacehiereingeben" -c 100 --detailed
     ```
   - Gespeicherte Daten anzeigen:
     ```bash
     python netzwerkSniffer.py --read
     ```

3. Projektsetup:

```bash
pip install -r requirements.txt
