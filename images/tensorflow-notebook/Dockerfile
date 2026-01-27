# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/scipy-notebook
FROM $BASE_IMAGE

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Pin protobuf version for tensorflow 2.20 to avoid user warning.
# The fix can be removed once tensorflow is built with newer version of protobuf:
# https://github.com/tensorflow/tensorflow/issues/98980
RUN mamba install --yes \
    'jupyter-server-proxy' \
    'protobuf>=5.28.3,<6' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Install tensorflow with pip, on x86_64 tensorflow-cpu
RUN [[ $(uname -m) = x86_64 ]] && TF_POSTFIX="-cpu" || TF_POSTFIX="" && \
    pip install --no-cache-dir \
    "tensorflow${TF_POSTFIX}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

COPY --chown="${NB_UID}:${NB_GID}" cuda/20tensorboard-proxy-env.sh /usr/local/bin/before-notebook.d/
