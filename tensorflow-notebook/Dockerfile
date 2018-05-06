# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"


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
#RUN pip install gym
#RUN apt-get install python-opengl
