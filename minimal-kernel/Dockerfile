# Copyright (c) Jupyter Development Team.
FROM debian:jessie

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    python3-pip \
    python3-zmq \
    && apt-get clean

# Install Tini
RUN apt-get update && \
    apt-get install -yq --no-install-recommends wget && \
    wget --quiet https://github.com/krallin/tini/releases/download/v0.6.0/tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini && \
    apt-get remove --purge -y wget && \
    apt-get autoremove -y && \
    apt-get clean

# Configure environment
ENV KG_USER jovyan
ENV KG_UID 1000

# Create jovyan user with UID=1000
RUN useradd -m -s /bin/bash -N -u $KG_UID $KG_USER

# Install Kernel Gateway
RUN apt-get update && \
    apt-get install -yq --no-install-recommends build-essential python3-dev && \
    pip3 install jupyter_kernel_gateway==0.2.0 && \
    apt-get remove --purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    apt-get clean

# Configure container startup
EXPOSE 8888
WORKDIR /tmp
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway"]
CMD ["--KernelGatewayApp.ip=0.0.0.0"]

# Run container as jovyan
USER jovyan
