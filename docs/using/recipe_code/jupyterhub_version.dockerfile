ARG BASE_IMAGE=quay.io/jupyter/base-notebook
FROM $BASE_IMAGE

RUN mamba install --yes 'jupyterhub-singleuser==5.2.1' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
