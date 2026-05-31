FROM mcr.microsoft.com/devcontainers/python:3.13@sha256:e797f7e02a8adf1c6d375a4873591205cc867a2d68083506e7f3aa89822f2026

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
