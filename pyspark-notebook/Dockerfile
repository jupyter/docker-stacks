# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Saagie"

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 2.3.4
ENV HADOOP_VERSION 2.7
# On debian slim needs mkdir man directory to avoid installation errors
RUN mkdir -p /usr/share/man/man1 && \
    apt-get -y update && \
    apt-get install --no-install-recommends -y \
      openjdk-8-jre-headless ca-certificates-java && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
        wget -q https://archive.apache.org/dist/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
        tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local --owner root --group root --no-same-owner && \
        rm spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

# Mesos dependencies
COPY mesos.key /tmp/
# PATCH for issue MARATHON-7694 (https://jira.mesosphere.com/browse/MARATHON-7694)
RUN touch /usr/local/bin/systemctl && chmod +x /usr/local/bin/systemctl

RUN apt-get update -qq && apt-get install -yqq --no-install-recommends \
      libcurl3 libevent-dev libsvn1 libsasl2-modules libcurl4-nss-dev && \
    rm -rf /var/lib/apt/lists/*;

RUN cd /tmp && \
    wget -q repos.mesosphere.com/debian/pool/main/m/mesos/mesos_1.3.1-2.0.1.debian9_amd64.deb && \
    dpkg -i mesos_1.3.1-2.0.1.debian9_amd64.deb && \
    rm mesos_1.3.1-2.0.1.debian9_amd64.deb

# Spark and Mesos config
ENV SPARK_HOME /usr/local/spark
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip
ENV MESOS_NATIVE_LIBRARY /usr/local/lib/libmesos.so
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info

USER $NB_UID

# Install pyarrow
RUN conda install --quiet -y 'pyarrow' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER root
# Install Kerberos & ACL for Saagie
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq && apt-get install -yqq --no-install-recommends \
      krb5-user acl && \
    rm -rf /var/lib/apt/lists/*;

# Install tools
RUN apt-get update -qq && apt-get install -yqq --no-install-recommends \
      vim nano gnupg2 && \
    rm -rf /var/lib/apt/lists/*;

# Instll freeip client
RUN wget -qO - http://apt.numeezy.fr/numeezy.asc | apt-key add - && \
    echo 'deb http://apt.numeezy.fr stretch main' >> /etc/apt/sources.list && \
    apt-get update -qq && apt-get install -yqq --no-install-recommends \
      freeipa-client && \
    rm -rf /var/lib/apt/lists/*;

RUN mkdir -p /usr/lib/impala/lib/ && chown $NB_UID /usr/lib/impala/lib

RUN sed -i '2iln -s /etc/hadoop/conf/sentry-libs/hive-hcatalog-core.jar /usr/lib/impala/lib/hive-hcatalog-core.jar' /usr/local/bin/start-notebook.sh && cat /usr/local/bin/start-notebook.sh

WORKDIR /home/jovyan/work

USER $NB_UID
