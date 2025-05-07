ARG BASE_IMAGE=quay.io/jupyter/base-notebook
FROM $BASE_IMAGE

RUN mamba install --yes 'py-xgboost' && \
    mamba clean --all -f -y && \
    (rm -r /home/${NB_USER}/.cache/rosetta || true) && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
