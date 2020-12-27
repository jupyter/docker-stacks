# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Octave pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gnuplot \
    ghostscript \
    texinfo \
    octave \
    octave-io \
    octave-struct \
    octave-symbolic \
    octave-miscellaneous \
    octave-parallel \
    octave-statistics && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN export OCTAVE_EXECUTABLE=$(which octave)

USER $NB_UID

# Install octave kernel
RUN conda config --add channels conda-forge && \
    conda install --quiet --yes \
    'octave_kernel=0.32.0' \
    'texinfo=6.7' \
    && \
    python3 -m octave_kernel install --user && \
    python3 -m octave_kernel.check && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}"
