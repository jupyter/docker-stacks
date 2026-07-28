# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# https://quay.io/repository/jupyter/base-notebook?tab=tags
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/base-notebook:2026-07-28@sha256:a8b2611c4c380dde6159f9963ee4f294373a0b214958987b7b469d312287c4ef
FROM $BASE_IMAGE

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV TAG="2026-07-28"

COPY --chown=${NB_UID}:${NB_GID} binder/README.ipynb "${HOME}"/README.ipynb

RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
