FROM mcr.microsoft.com/devcontainers/python:3.15@sha256:0ae003ea761a00b8f8809cfdd08a04edfb1c7f17e76c413b27882ce5939a65f4

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY docs/requirements.txt /tmp/requirements-docs.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt && \
    pip install --no-cache-dir -r /tmp/requirements-docs.txt
