FROM mcr.microsoft.com/devcontainers/python:3.15@sha256:6e261c4a01a94ab86485a6b9d08083c3e968ea51440c0c24b6efaa771c33312d

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
