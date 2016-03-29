# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/jupyterhub:master

# Install dockerspawner and its dependencies
RUN /opt/conda/bin/pip install \
    -e git+https://github.com/jupyter/jupyterhub#egg=jupyterhub \
    -e git+https://github.com/jupyter/oauthenticator#egg=oauthenticator \
    -e git+https://github.com/jupyter/dockerspawner#egg=dockerspawner

COPY ./userlist /srv/jupyterhub/userlist
