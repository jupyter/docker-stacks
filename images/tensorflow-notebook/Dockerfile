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

# Install tensorflow with pip, on x86_64 tensorflow-cpu
RUN [[ $(uname -m) = x86_64 ]] && TF_POSTFIX="-cpu" || TF_POSTFIX="" && \
    pip install --no-cache-dir \
    "jupyter-server-proxy" \
    "tensorflow${TF_POSTFIX}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

COPY --chown="${NB_UID}:${NB_GID}" cuda/20tensorboard-proxy-env.sh /usr/local/bin/before-notebook.d/
