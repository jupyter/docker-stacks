# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_CONTAINER=$REGISTRY/$OWNER/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install CUDA libs and cuDNN with mamba
RUN mamba install --yes -c nvidia/label/cuda-12.3.2 \
    'cuda-cupti' \
    'cuda-libraries-dev' \
    'cuda-nvcc' \
    'cuda-nvtx' \
    'cudnn' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

ENV XLA_FLAGS="--xla_gpu_cuda_data_dir=${CONDA_DIR}" \
    LD_LIBRARY_PATH="${CONDA_DIR}/lib/${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" \
    # https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html#dockerfiles
    NVIDIA_VISIBLE_DEVICES="all" \
    NVIDIA_DRIVER_CAPABILITIES="compute,utility"

# Install Tensorflow with pip
RUN pip install --no-cache-dir tensorflow && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
