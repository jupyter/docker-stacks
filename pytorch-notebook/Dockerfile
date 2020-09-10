# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=dain/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER $NB_UID

# Install Pytorch 1.6 with CUDA 10.2 support
# Note that channel priority must be set flexible since cudatoolkit package is
# not available in conda-forge, to prevent a frozen dependency resolve
RUN conda config --show channels && \
    conda config --add channels conda-forge && \
    conda config --add channels pytorch && \
    conda config --show channels && \
    conda config --system --set channel_priority flexible && \
    conda install -q -y \
    'pytorch=1.6*' \
    'torchvision=0.7*' \
    'cudatoolkit=10.2*' && \
    conda config --system --set channel_priority strict && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

WORKDIR $HOME