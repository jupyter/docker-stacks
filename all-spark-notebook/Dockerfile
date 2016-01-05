# Copyright (c) Jupyter Development Team.
FROM jupyter/minimal-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 1.6.0
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends openjdk-7-jre-headless && \
    apt-get clean
RUN curl -s https://transfer.sh/ipPxf/spark-1.6.0-bin-2.6.0.tgz | tar -xz -C /usr/local/
RUN cd /usr/local && ln -s spark-1.6.0-bin-hadoop2.6 spark

ENV SPARK_HOME /usr/local/spark


# Mesos dependencies
ENV VERSION 0.25.0
ENV PKG_RELEASE 0.2.70

RUN apt-get -y install curl

RUN \
  curl -s -O https://downloads.mesosphere.io/master/debian/8/mesos_${VERSION}-${PKG_RELEASE}.debian81_amd64.deb && \
  dpkg --unpack mesos_${VERSION}-${PKG_RELEASE}.debian81_amd64.deb && \
  apt-get install -f -y && \
  rm mesos_${VERSION}-${PKG_RELEASE}.debian81_amd64.deb && \
  apt-get clean

# Scala Spark kernel (build and cleanup)
RUN cd /tmp && \
    echo deb http://dl.bintray.com/sbt/debian / > /etc/apt/sources.list.d/sbt.list && \
    apt-get update && \
    git clone https://github.com/ibm-et/spark-kernel.git && \
    apt-get install -yq --force-yes --no-install-recommends sbt && \
    cd spark-kernel && \
    git checkout 3905e47815 && \
    make dist SHELL=/bin/bash && \
    mv dist/spark-kernel /opt/spark-kernel && \
    chmod +x /opt/spark-kernel && \
    rm -rf ~/.ivy2 && \
    rm -rf ~/.sbt && \
    rm -rf /tmp/spark-kernel && \
    apt-get remove -y sbt && \
    apt-get clean

# Spark and Mesos pointers
ENV SPARK_HOME /usr/local/spark
ENV R_LIBS_USER $SPARK_HOME/R/lib
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.9-src.zip
ENV MESOS_NATIVE_LIBRARY /usr/local/lib/libmesos.so
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    gfortran \
    gcc && apt-get clean

USER jovyan

# Install Python 3 packages
RUN conda install --yes \
    'ipywidgets=4.0*' \
    'pandas=0.17*' \
    'matplotlib=1.4*' \
    'scipy=0.16*' \
    'seaborn=0.6*' \
    'bokeh=0.10*' \
    'scikit-learn=0.16*' \
    && conda clean -yt

# Install Python 2 packages
RUN conda create -p $CONDA_DIR/envs/python2 python=2.7 \
    'ipython=4.0*' \
    'ipywidgets=4.0*' \
    'pandas=0.17*' \
    'matplotlib=1.4*' \
    'scipy=0.16*' \
    'seaborn=0.6*' \
    'bokeh=0.10*' \
    'scikit-learn=0.16*' \
    pyzmq \
    && conda clean -yt

# R packages
RUN conda config --add channels r
RUN conda install --yes \
    'r-base=3.2*' \
    'r-irkernel=0.5*' \
    'r-ggplot2=1.0*' \
    'r-rcurl=1.95*' && conda clean -yt


# WORKAROUND: symlink version of zmq required by latest rzmq back into conda lib
# https://github.com/jupyter/docker-stacks/issues/55
RUN ln -s /opt/conda/pkgs/zeromq-4.0.*/lib/libzmq.so.4.* /opt/conda/lib/libzmq.so.4
RUN ln -s /opt/conda/pkgs/libsodium-0.4.*/lib/libsodium.so.4.* /opt/conda/lib/libsodium.so.4



# Scala Spark kernel spec
RUN mkdir -p /opt/conda/share/jupyter/kernels/scala
COPY kernel.json /opt/conda/share/jupyter/kernels/scala/

USER root

# Install Python 2 kernel spec globally to avoid permission problems when NB_UID
# switching at runtime.
RUN $CONDA_DIR/envs/python2/bin/python \
    $CONDA_DIR/envs/python2/bin/ipython \
    kernelspec install-self



USER jovyan
