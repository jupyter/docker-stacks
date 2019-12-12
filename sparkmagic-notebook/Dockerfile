# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/base-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root
# This is needed because requests-kerberos fails to install on debian due to missing linux headers
RUN conda install --quiet --yes 'requests-kerberos==0.12.*' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

# Install sparkmagic
RUN conda install --quiet --yes 'sparkmagic==0.14.*' && \
    conda clean --all -f -y && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^1.0.1 --no-build && \
    jupyter-kernelspec install --user $(pip show sparkmagic | grep Location | cut -d" " -f2)/sparkmagic/kernels/sparkkernel && \
    jupyter-kernelspec install --user $(pip show sparkmagic | grep Location | cut -d" " -f2)/sparkmagic/kernels/pysparkkernel && \
    jupyter-kernelspec install --user $(pip show sparkmagic | grep Location | cut -d" " -f2)/sparkmagic/kernels/sparkrkernel && \
    jupyter serverextension enable --sys-prefix --py sparkmagic && \
    mkdir /home/$NB_USER/.sparkmagic && \
    npm cache clean --force --silent && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER root
# Install startup script to customize sparkmagic config
COPY configure-sparkmagic.sh /usr/local/bin/start-notebook.d/configure-sparkmagic.sh
RUN chmod +x /usr/local/bin/start-notebook.d/configure-sparkmagic.sh && \
    fix-permissions /usr/local/bin/start-notebook.d/
# Switch back to jovyan
USER $NB_UID
