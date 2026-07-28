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

USER root

# Spark dependencies
# Default values can be overridden at build time
# (ARGS are in lowercase to distinguish them from ENV)
ARG openjdk_version="21"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jre-headless" \
    ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# If spark_version is not set, latest Spark will be installed
ARG spark_version
ARG hadoop_version="3"
# If scala_version is not set, Spark without Scala will be installed
ARG scala_version
# URL to use for Spark downloads
# You need to use https://archive.apache.org/dist/spark/ website if you want to download old Spark versions
# But it seems to be slower, that's why we use the recommended site for download
ARG spark_download_url="https://dlcdn.apache.org/spark/"
ARG derby_version="10.17.1.0"
# The sha256 checksum of the derby jar from Maven Central
# It must be updated together with derby_version
ARG derby_sha256="764e4c133f860a8876e835ef2306efecad27a742d27f05bc4bce669432c6b397"

ENV SPARK_HOME=/usr/local/spark
ENV PATH="${PATH}:${SPARK_HOME}/bin"
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info"

COPY setup_spark.py /opt/setup-scripts/

# Setup Spark
RUN /opt/setup-scripts/setup_spark.py \
    --spark-version="${spark_version}" \
    --hadoop-version="${hadoop_version}" \
    --scala-version="${scala_version}" \
    --spark-download-url="${spark_download_url}"

# Spark bundles Derby 10.16.1.1 by default; replace it with a fixed release.
# The exact filename makes the build fail loudly once Spark bumps the bundled version.
RUN set -eux; \
    rm "${SPARK_HOME}/jars/derby-10.16.1.1.jar"; \
    curl -fsSL -o "/tmp/derby-${derby_version}.jar" \
      "https://repo1.maven.org/maven2/org/apache/derby/derby/${derby_version}/derby-${derby_version}.jar"; \
    echo "${derby_sha256} */tmp/derby-${derby_version}.jar" | sha256sum -c -; \
    mv "/tmp/derby-${derby_version}.jar" "${SPARK_HOME}/jars/"

# Configure IPython system-wide
COPY ipython_kernel_config.py "/etc/ipython/"
RUN fix-permissions "/etc/ipython/"

# hadolint ignore=DL3059
RUN rm -rf "/home/${NB_USER}/.cache/rosetta"

USER ${NB_UID}

# Install pyarrow
# The pandas version must match the version on which the Pandas API for Spark is built,
# setup_spark.py resolves it from https://github.com/apache/spark/blob/<SPARK_VERSION>/dev/infra/Dockerfile
RUN mamba install --yes \
    'grpcio-status' \
    'grpcio' \
    "pandas=$(cat /opt/setup-scripts/pandas-version.txt)" \
    'pyarrow' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

RUN rm -rf "/home/${NB_USER}/.cache/rosetta"

WORKDIR "${HOME}"
EXPOSE 4040
