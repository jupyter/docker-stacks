FROM mcr.microsoft.com/devcontainers/python:3.14@sha256:882b17d068262c7af4300180ead0ee14423d2c03393778c92435b0ca642dea07

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
