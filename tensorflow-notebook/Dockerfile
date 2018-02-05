# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG TAG_POSTFIX=
FROM jupyter/scipy-notebook:latest${TAG_POSTFIX}

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install Tensorflow
RUN conda install --quiet --yes \
    tensorflow${TAG_POSTFIX}=1.3* \
    'keras=2.0*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR
