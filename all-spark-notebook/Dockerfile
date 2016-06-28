# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/pyspark-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# RSpark config
ENV R_LIBS_USER $SPARK_HOME/R/lib

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    gfortran \
    gcc && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_USER

# R packages
RUN conda config --add channels r && \
    conda install --quiet --yes \
    'r-base=3.2*' \
    'r-irkernel=0.5*' \
    'r-ggplot2=1.0*' \
    'r-rcurl=1.95*' && conda clean -tipsy

# Apache Toree kernel
RUN pip --no-cache-dir install toree==0.1.0.dev7
RUN jupyter toree install --user
