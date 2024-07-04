# Verwenden eines Basis-Images mit Python 3.10
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Installieren von Systemabhängigkeiten
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends gcc python3-dev musl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /workspace

# Kopieren der requirements.txt in das Arbeitsverzeichnis
COPY requirements.txt /workspace/

# Sicherstellen, dass pip installiert und aktualisiert ist
RUN python -m ensurepip --upgrade

# Aktualisieren von pip, setuptools und wheel
RUN pip install --upgrade pip setuptools wheel

# Installieren der Abhängigkeiten aus der requirements.txt
RUN pip install -r requirements.txt

# Debugging-Ausgaben:
# Ausgabe der installierten Python-Version
RUN python --version

# Ausgabe der installierten pip-Version
RUN pip --version

# Ausgabe der installierten Python-Pakete
RUN pip list

# Standardmäßige Befehlsausführung, um den Container aktiv zu halten
CMD ["sleep", "infinity"]
