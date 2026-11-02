FROM mcr.microsoft.com/devcontainers/python:3.15@sha256:eb39f07323784af4c7558396808ceb01dacbe6dd7c63614f34d0235d0344a0ff

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
