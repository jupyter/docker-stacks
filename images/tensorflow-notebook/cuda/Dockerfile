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

# Install TensorFlow, CUDA and cuDNN with pip
RUN pip install --no-cache-dir \
    "jupyter-server-proxy" \
    "tensorflow[and-cuda]" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

COPY --chown="${NB_UID}:${NB_GID}" 20tensorboard-proxy-env.sh /usr/local/bin/before-notebook.d/

# workaround for https://github.com/tensorflow/tensorflow/issues/63362
RUN mkdir -p "${CONDA_DIR}/etc/conda/activate.d/" && \
    fix-permissions "${CONDA_DIR}"

COPY --chown="${NB_UID}:${NB_GID}" nvidia-lib-dirs.sh "${CONDA_DIR}/etc/conda/activate.d/"

# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html#dockerfiles
ENV NVIDIA_VISIBLE_DEVICES="all" \
    NVIDIA_DRIVER_CAPABILITIES="compute,utility"

# Puts the nvidia-smi binary (system management interface) on path
# with associated library files to execute it
ENV PATH="${PATH}:/usr/local/nvidia/bin" \
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/nvidia/lib64"
