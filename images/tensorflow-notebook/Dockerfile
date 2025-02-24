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

RUN mamba install --yes \
    'jupyter-server-proxy' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Can't use `conda-forge` for aarch64 tensorflow:
# https://github.com/conda-forge/tensorflow-feedstock/issues/136
RUN if [ "$(uname -m)" = "x86_64" ]; then \
        # https://github.com/conda-forge/tensorflow-feedstock/issues/174
        CONDA_OVERRIDE_CUDA=12.6 mamba install --yes \
            'tensorflow-cpu' && \
            mamba clean --all -f -y ; \
    else \
        pip install --no-cache-dir \
            'tensorflow'; \
    fi && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

COPY --chown="${NB_UID}:${NB_GID}" cuda/20tensorboard-proxy-env.sh /usr/local/bin/before-notebook.d/
