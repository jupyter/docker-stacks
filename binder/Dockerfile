# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# https://hub.docker.com/r/jupyter/base-notebook/tags
ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/base-notebook:6b49f3337709
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV TAG="6b49f3337709"

WORKDIR "${HOME}"
COPY binder/README.ipynb .

# Fix permissions on README.ipynb as root
USER root

RUN fix-permissions README.ipynb

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"
