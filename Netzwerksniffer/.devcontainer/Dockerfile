# Use a base image with Python 3.10
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends gcc python3-dev musl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /workspace

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /workspace/
RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Debugging outputs
RUN python --version
RUN pip --version
RUN pip list
