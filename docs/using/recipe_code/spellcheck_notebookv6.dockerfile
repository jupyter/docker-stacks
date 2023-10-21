# Using Docker Hub here, because this image is old and not pushed to Quay.io
FROM docker.io/jupyter/base-notebook:notebook-6.5.4

RUN pip install --no-cache-dir 'jupyter_contrib_nbextensions' && \
    jupyter contrib nbextension install --user && \
    # can modify or enable additional extensions here
    jupyter nbclassic-extension enable spellchecker/main --user && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
