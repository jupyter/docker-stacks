# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"
USER root

ENV DEBIAN_FRONTEND noninteractive

ENV ORACLE_INSTANTCLIENT_MAJOR 11.2
ENV ORACLE_INSTANTCLIENT_VERSION 11.2.0.4.0
ENV ORACLE /usr/local/oracle
ENV ORACLE_HOME $ORACLE/lib/oracle/$ORACLE_INSTANTCLIENT_MAJOR/client64
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$ORACLE_HOME/lib
ENV C_INCLUDE_PATH $C_INCLUDE_PATH:$ORACLE/include/oracle/$ORACLE_INSTANTCLIENT_MAJOR/client64

RUN apt-get update && apt-get install -y libaio1 \
        curl rpm2cpio cpio \
    && mkdir $ORACLE && TMP_DIR="$(mktemp -d)" && cd "$TMP_DIR" \
    && curl -L https://github.com/sergeymakinen/docker-oracle-instant-client/raw/assets/oracle-instantclient$ORACLE_INSTANTCLIENT_MAJOR-basic-$ORACLE_INSTANTCLIENT_VERSION-1.x86_64.rpm -o basic.rpm \
    && rpm2cpio basic.rpm | cpio -i -d -v && cp -r usr/* $ORACLE && rm -rf ./* \
    && ln -s libclntsh.so.11.1 $ORACLE/lib/oracle/$ORACLE_INSTANTCLIENT_MAJOR/client64/lib/libclntsh.so.$ORACLE_INSTANTCLIENT_MAJOR \
    && ln -s libocci.so.11.1 $ORACLE/lib/oracle/$ORACLE_INSTANTCLIENT_MAJOR/client64/lib/libocci.so.$ORACLE_INSTANTCLIENT_MAJOR \
    && curl -L https://github.com/sergeymakinen/docker-oracle-instant-client/raw/assets/oracle-instantclient$ORACLE_INSTANTCLIENT_MAJOR-devel-$ORACLE_INSTANTCLIENT_VERSION-1.x86_64.rpm -o devel.rpm \
    && rpm2cpio devel.rpm | cpio -i -d -v && cp -r usr/* $ORACLE && rm -rf "$TMP_DIR" \
    && echo "$ORACLE_HOME/lib" > /etc/ld.so.conf.d/oracle.conf && chmod o+r /etc/ld.so.conf.d/oracle.conf && ldconfig \
    && rm -rf /var/lib/apt/lists/* && apt-get purge -y --auto-remove curl rpm2cpio cpio

RUN apt-get update && apt-get install -yq --no-install-recommends graphviz \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER $NB_USER

# Install Tensorflow
RUN pip install influxdb
RUN pip install pyreadline
RUN conda install --quiet --yes \
    'numpy' \
    'matplotlib' \
    'pandas' \
    'scipy' \
    'seaborn' \
    'scikit-learn' \
    'scikit-image' \
    'tensorflow' \
    'keras' \
    'plotly' \
    'quandl' \
    'tweepy' \
    'textblob' \
    'PyYAML' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR 
RUN pip install gym
RUN apt-get install python-opengl
