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
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    python3-zmq \
    sudo \
    && apt-get clean

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.6.0/tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV SHELL /bin/bash
ENV NB_USER nobody
ENV NB_UID 1000

# Install Kernel Gateway
RUN pip3 install jupyter_kernel_gateway==0.2.0

# Configure container startup
USER $NB_USER
EXPOSE 8888
WORKDIR /home/$NB_USER/work
ENTRYPOINT ["tini", "--"]
CMD ["/usr/local/bin/start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
USER root
COPY start-notebook.sh /usr/local/bin/
COPY jupyter_kernel_gateway_config.py /home/$NB_USER/.jupyter/
RUN chown -R $NB_USER:users /home/$NB_USER/.jupyter
