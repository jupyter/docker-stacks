# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# https://quay.io/repository/jupyter/base-notebook?tab=tags
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/base-notebook:2025-12-31@sha256:4ed6681f1bfe736ac7dff06a9d558acb69b5b1fdbf4fc9904bbf89e4853626cc
FROM $BASE_IMAGE

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV TAG="2025-12-31"

COPY --chown=${NB_UID}:${NB_GID} binder/README.ipynb "${HOME}"/README.ipynb

RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
