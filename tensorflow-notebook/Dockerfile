# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER $NB_USER

# Install Python 3 Tensorflow
RUN conda install --quiet --yes -c conda-forge 'tensorflow=0.9.0'

# Install Python 2 Tensorflow
RUN conda install --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 'tensorflow=0.9.0'
