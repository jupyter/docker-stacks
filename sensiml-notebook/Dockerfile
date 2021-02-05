# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/tensorflow-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install SensiML and enable notebook extensions.
RUN pip install --quiet --no-cache-dir \
    'sensiml' && \
    jupyter nbextension enable --py widgetsnbextension --sys-prefix  && \
    jupyter nbextension enable --py --sys-prefix bqplot  && \
    jupyter nbextension enable --py --sys-prefix qgrid  && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
