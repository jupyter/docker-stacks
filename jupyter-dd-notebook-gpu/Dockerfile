# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jolibrain/scipy-notebook-gpu
FROM $BASE_CONTAINER

LABEL maintainer="Emmanuel Benazera <emmanuel.benazera@jolibrain.com>"

# Install Tensorflow, uses cuda 9.2
RUN conda install --quiet --yes \
    'tensorflow-gpu=1.12*' \
    'keras=2.2*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Install Pytorch, uses cuda 9.0, or 10.0
RUN conda install pytorch torchvision cudatoolkit=9.0 -c pytorch
    