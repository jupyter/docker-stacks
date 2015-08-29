# Copyright (c) Jupyter Development Team.
FROM debian:jessie

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    wget \
    build-essential \
    python-dev \
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    supervisor \
    sudo \
    && apt-get clean

# Configure docker environment
ENV CONDA_DIR /opt/conda
ENV NB_USER jovyan
ENV WORK /home/$NB_USER/work
ENV PATH $CONDA_DIR/bin:$PATH

# Install conda
RUN echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-3.9.1-Linux-x86_64.sh && \
    /bin/bash /Miniconda3-3.9.1-Linux-x86_64.sh -b -p $CONDA_DIR && \
    rm Miniconda3-3.9.1-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --yes conda==3.14.1

# Install Jupyter notebook
RUN conda install --yes \
    'notebook=4.0*' \
    terminado \
    && conda clean -yt

# Configure container startup
EXPOSE 8888
CMD [ "start-notebook.sh" ]

# Add local files as late as possible to avoid cache busting
COPY start-notebook.sh /usr/local/bin/
COPY notebook.conf /etc/supervisor/conf.d/
COPY jupyter_notebook_config.py /etc/skel/.jupyter/
