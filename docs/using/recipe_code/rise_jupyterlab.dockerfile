FROM quay.io/jupyter/base-notebook

RUN mamba install --yes 'jupyterlab_rise' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
