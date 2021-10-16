# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Temporary fix for https://github.com/jupyter/docker-stacks/issues/1480
USER root
WORKDIR /opt/conda/lib/python3.9/site-packages/
RUN wget -qO- https://patch-diff.githubusercontent.com/raw/tensorflow/tensorflow/pull/51450.diff | git apply
USER ${NB_UID}
WORKDIR "${HOME}"

# Install Tensorflow
RUN mamba install --quiet --yes \
    'tensorflow' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
