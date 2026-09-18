FROM mcr.microsoft.com/devcontainers/python:3.14@sha256:3b3c45535947751e9dfcd513ef5bee858d221844f55e278e92d1cd8f5b1f2972

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
