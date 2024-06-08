FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt /workspace
RUN pip install --upgrade pip
RUN pip install -r requirements.txt