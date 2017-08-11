# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

# Install Tensorflow
RUN conda install --quiet --yes 'tensorflow=1.0*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR
