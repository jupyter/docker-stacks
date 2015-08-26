# Copyright (c) Jupyter Development Team.
FROM jupyter/minimal-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 1.4.1
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends openjdk-7-jre-headless && \
    apt-get clean
RUN wget -qO - http://d3kbcqa49mib13.cloudfront.net/spark-${APACHE_SPARK_VERSION}-bin-hadoop2.6.tgz | tar -xz -C /usr/local/
RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop2.6 spark

# Mesos dependencies
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF && \
    DISTRO=debian && \
    CODENAME=wheezy && \
    echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" > /etc/apt/sources.list.d/mesosphere.list && \
    apt-get -y update && \
    apt-get --no-install-recommends -y --force-yes install mesos=0.22.1-1.0.debian78 && \
    apt-get clean

# Scala Spark kernel (build and cleanup)
RUN cd /tmp && \
    echo deb http://dl.bintray.com/sbt/debian / > /etc/apt/sources.list.d/sbt.list && \
    apt-get update && \
    git clone https://github.com/ibm-et/spark-kernel.git && \
    apt-get install -yq --force-yes --no-install-recommends sbt && \
    cd spark-kernel && \
    sbt compile -Xms1024M \
        -Xmx2048M \
        -Xss1M \
        -XX:+CMSClassUnloadingEnabled \
        -XX:MaxPermSize=1024M && \
    sbt pack && \
    mv kernel/target/pack /opt/sparkkernel && \
    chmod +x /opt/sparkkernel && \
    rm -rf ~/.ivy2 && \
    rm -rf ~/.sbt && \
    rm -rf /tmp/spark-kernel && \
    apt-get remove -y sbt && \
    apt-get clean

USER jovyan

# Spark and Mesos pointers
ENV SPARK_HOME /usr/local/spark
ENV R_LIBS_USER $SPARK_HOME/R/lib
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip
ENV MESOS_NATIVE_LIBRARY /usr/local/lib/libmesos.so

# Install Python 3 packages
RUN conda install --yes \
    'ipywidgets=4.0*' \
    'pandas=0.16*' \
    'matplotlib=1.4*' \
    'scipy=0.15*' \
    'seaborn=0.6*' \
    'scikit-learn=0.16*' \
    && conda clean -yt

# Install Python 2 packages and kernel spec
RUN conda create -p $CONDA_DIR/envs/python2 python=2.7 \
    'ipython=4.0*' \
    'ipywidgets=4.0*' \
    'pandas=0.16*' \
    'matplotlib=1.4*' \
    'scipy=0.15*' \
    'seaborn=0.6*' \
    'scikit-learn=0.16*' \
    pyzmq \
    && conda clean -yt
RUN $CONDA_DIR/envs/python2/bin/python \
    $CONDA_DIR/envs/python2/bin/ipython \
    kernelspec install-self --user

# R packages
RUN conda config --add channels r
RUN conda install --yes \
    'r-base=3.1*' \
    'r-irkernel=0.4*' \
    'r-ggplot2=1.0*' \
    'r-rcurl=1.95*' && conda clean -yt

# Scala Spark kernel spec
RUN mkdir -p $HOME/.ipython/kernels/scala
COPY kernel.json $HOME/.ipython/kernels/scala/

# Switch back to root so that supervisord runs under that user
USER root
RUN chown -R $NB_USER:$NB_USER $HOME/.ipython/kernels/scala/