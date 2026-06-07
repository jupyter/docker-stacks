# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Pick your favorite docker-stacks image
FROM quay.io/jupyter/minimal-notebook:2025-12-31@sha256:5bb65b1758fca6915271353932d8fcd577a17cc73299a557197747555e6f142a

USER root

# Add permanent apt-get installs and other root commands here
# e.g., RUN apt-get install --yes --no-install-recommends npm nodejs

USER ${NB_UID}

# Switch back to jovyan to avoid accidental container runs as root
# Add permanent mamba/pip/conda installs, data files, other user libs here
# e.g., RUN pip install --no-cache-dir flake8
