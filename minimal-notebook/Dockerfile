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

ENV CONDA_DIR /opt/conda
ENV NB_USER jovyan

# Install conda
RUN echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-3.9.1-Linux-x86_64.sh && \
    /bin/bash /Miniconda3-3.9.1-Linux-x86_64.sh -b -p $CONDA_DIR && \
    rm Miniconda3-3.9.1-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --yes conda==3.14.1

# Create non-root user
RUN useradd -m -s /bin/bash $NB_USER
RUN chown -R $NB_USER:$NB_USER $CONDA_DIR
RUN chown $NB_USER:$NB_USER /home/$NB_USER -R

# Configure user environment
USER $NB_USER
ENV HOME /home/$NB_USER
ENV SHELL /bin/bash
ENV USER $NB_USER
ENV PATH $CONDA_DIR/bin:$PATH

# Setup a work directory rooted in home for ease of volume mounting
ENV WORK $HOME/work
RUN mkdir -p $WORK
WORKDIR $WORK

# Install Jupyter notebook
RUN conda install --yes \
    'notebook=4.0*' \
    terminado \
    && conda clean -yt

# Configure Jupyter
RUN jupyter notebook --generate-config

# Configure container startup
EXPOSE 8888
USER root
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]

# Add local files as late as possible to avoid cache busting
COPY jupyter_notebook_config.py $HOME/.jupyter/
COPY notebook.conf /etc/supervisor/conf.d/
COPY enable_sudo.sh /usr/local/bin/
RUN chown $NB_USER:$NB_USER $HOME/.jupyter/jupyter_notebook_config.py