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
     sudo python netzwerkSniffer.py -i eth0 -c 100
     ```
   - Pakete sniffen mit detaillierter Payload:
     ```bash
     sudo python netzwerkSniffer.py -i eth0 -c 100 --detailed
     ```
   - Gespeicherte Daten anzeigen:
     ```bash
     sudo python netzwerkSniffer.py --read
     ```
   - Gespeicherte Daten exportieren
     ```bash
     sudo python netzwerkSniffer.py -i eth0 -c 100 > sniffing_output.txt
     ```

     Wichtigste TLS Befehle:

   - Mit NON anfangen:

     sudo python non_tls_server.py

   - dann Sniffer starten:

     sudo python netzwerkSniffer.py -i eth0 -c 100 -d > output_without_tls.json

   - Dann NON TLS Client starten

     python non_tls_client.py

   - Dasselbe dann mit TLS also "non" löschen

3. Projektsetup:

```bash
pip install -r requirements.txt
