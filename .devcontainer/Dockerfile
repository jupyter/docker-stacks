FROM mcr.microsoft.com/devcontainers/python:3.14@sha256:66af9ee0a89e76f83b5c54a0cfdc19966ec8e443e294707f8f9b45f465b42cf1

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
