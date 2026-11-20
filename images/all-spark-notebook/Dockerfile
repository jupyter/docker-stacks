# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/pyspark-notebook
FROM $BASE_IMAGE

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# RSpark config
ENV R_LIBS_USER="${SPARK_HOME}/R/lib"
RUN fix-permissions "${R_LIBS_USER}"

# sparklyr fails with ClassNotFoundException on Spark 4.3, which does not ship unshaded protobuf-java
# Remove this once sparklyr or Spark fixes it
ARG protobuf_version="4.33.5"
# The sha256 checksum of the protobuf-java jar from Maven Central
# It must be updated together with protobuf_version
ARG protobuf_sha256="cb9e00d6e3d4b1305f3fdc147490ce347bfe8c05dc821a433b23b2ff28749bb1"

RUN set -eux; \
    curl -fsSL -o "/tmp/protobuf-java-${protobuf_version}.jar" \
      "https://repo1.maven.org/maven2/com/google/protobuf/protobuf-java/${protobuf_version}/protobuf-java-${protobuf_version}.jar"; \
    echo "${protobuf_sha256} */tmp/protobuf-java-${protobuf_version}.jar" | sha256sum -c -; \
    mv "/tmp/protobuf-java-${protobuf_version}.jar" "${SPARK_HOME}/jars/"

# R pre-requisites
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    fonts-dejavu \
    gfortran \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN rm -rf "/home/${NB_USER}/.cache/rosetta"

USER ${NB_UID}

# R packages including IRKernel which gets installed globally.
RUN mamba install --yes \
    'r-base' \
    'r-ggplot2' \
    'r-irkernel' \
    'r-rcurl' \
    'r-sparklyr' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

RUN rm -rf "/home/${NB_USER}/.cache/rosetta"
