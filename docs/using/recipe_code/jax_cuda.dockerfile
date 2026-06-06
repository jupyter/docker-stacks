ARG BASE_IMAGE=quay.io/jupyter/base-notebook
FROM $BASE_IMAGE

RUN pip install -v --no-cache-dir 'jax[cuda13]' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
