ARG BASE_IMAGE=quay.io/jupyter/base-notebook
FROM $BASE_IMAGE

RUN mamba install --yes 'jupyterlab_rise' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
