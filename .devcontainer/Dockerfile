FROM mcr.microsoft.com/devcontainers/python:3.14@sha256:1c3a6304ca90d6843915738d1adfbc4db1a660a65fa96948b88048357cc3811a

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
