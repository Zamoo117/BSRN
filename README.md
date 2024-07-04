# BSRN
Werkstück 4, Client-Server-Anwendung

Ziel: Erstellen eines einfachen Netzwerk-Sniffers, welcher Netzwerkpakete erfasst und diese analysiert.

// Kurze Zusammenfassung der wichtigsten Punkte:

Zusammenfassung

0. Schritte falls Codespaces nicht Programme automatisch installiert:
   - sudo /home/codespace/.python/current/bin/pip install psutil
   - sudo /home/codespace/.python/current/bin/python -m pip install psutil
   - python -m pip show psutil


1. Projektstruktur und Dateien:
   - `netzwerkSniffer.py`: Hauptskript für das Sniffen und die Verarbeitung von Netzwerkpaketen.
   - `requirements.txt`: Listet die benötigten Python-Pakete (`scapy`, `psutil`) auf.
   - `README.md`: Dokumentation zur Installation und Nutzung des Projekts.

2. Wichtige Befehle:

   - Scapy installieren, da es irgendwie trotz Requirements Datei nicht installiert wird
   
      pip install scapy

   - Interfaces auflisten:
     
     python netzwerkSniffer.py --list
     
   - Pakete sniffen mit verkürzter Payload:
     
     sudo -E python netzwerkSniffer.py -i lo -c 100
    
   - Pakete sniffen mit detaillierter Payload:
     
     sudo -E python netzwerkSniffer.py -i lo -c 100 --detailed
     
   - Gespeicherte Daten anzeigen:
     
     sudo -E python netzwerkSniffer.py --read
     
   - Gespeicherte Daten exportieren
     
     sudo -E python netzwerkSniffer.py -i lo -c 10 > sniffidySniffSniff.txt
     

     Wichtigste TLS Befehle:

   - Mit NON anfangen:

     sudo -E python non_tls_server.py

   - dann Sniffer starten:

     sudo -E python netzwerkSniffer.py -i eth0 -c 100 -d > output_without_tls.json

   - Dann NON TLS Client starten

     python non_tls_client.py

   - Dasselbe dann mit TLS also "non" löschen

3. Projektsetup:

pip install -r requirements.txt
