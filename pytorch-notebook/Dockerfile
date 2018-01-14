# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install PyTorch
RUN conda install --quiet --yes -c pytorch \
        'pytorch=0.3.0' \
        'torchvision=0.2.0' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR