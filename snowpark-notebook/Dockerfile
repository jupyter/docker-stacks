ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook:python-3.8.8
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

RUN apt-get update --yes && \
apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

WORKDIR /tmp

RUN pip install \
    'snowflake-snowpark-python'

WORKDIR "${HOME}"