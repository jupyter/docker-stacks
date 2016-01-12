# Copyright (c) Jupyter Development Team.
FROM debian:jessie

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    wget \
    build-essential \
    python3-dev \
    python3-pip \
    libsm6 \
    python3-zmq \
    && apt-get clean

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.6.0/tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Install Kernel Gateway
RUN pip3 install jupyter_kernel_gateway==0.2.0

# Configure container startup
USER nobody
EXPOSE 8888
WORKDIR /tmp
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway"]
CMD ["--KernelGatewayApp.ip=0.0.0.0"]

#error Permission denied: '/nonexistent' when not running as root or as user nobody
USER root