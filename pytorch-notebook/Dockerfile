# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=dain/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Pekka Ahtonen <pekka.ahtonen@dainstudios.com>"

USER $NB_UID

# Install Pytorch 1.6 with CUDA 10.2 support
# Note that channel priority must be set flexible since cudatoolkit package is
# not available in conda-forge, to prevent a frozen dependency resolve
#
# Install OpenCV and switch to Intel MKL backend
#
RUN conda config --show channels && \
    conda config --add channels pytorch && \
    conda config --add channels conda-forge && \
    conda config --show channels && \
    conda config --system --set channel_priority flexible && \
    conda install -q -y \
    'conda-forge::blas=*=mkl' \
    'conda-forge::opencv=4.*' \
    'tensorboard=2.*' \
    'pytorch=1.6*' \
    'torchvision=0.7*' \
    'ignite=0.4*' \
    'pytorch-lightning=0.9*' \
    'cudatoolkit=10.2*' \
    && \
    conda config --system --set channel_priority strict && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Install MONAI milestone edition with some extras
RUN pip install -q --no-cache-dir 'monai[gdown,nibabel,pillow]'

# Install and build MONAI from master branch
#RUN pip install -q --no-cache-dir git+https://github.com/Project-MONAI/MONAI#egg=MONAI

WORKDIR $HOME