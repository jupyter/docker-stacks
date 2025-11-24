FROM mcr.microsoft.com/devcontainers/python:3.13

COPY requirements-dev.txt /tmp/
COPY docs/requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    rm -rf /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt
