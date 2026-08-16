# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# This build arg allows building the image based on a different root image
ARG ROOT_IMAGE=default_root_image

# Ubuntu 24.04 (noble)
# https://hub.docker.com/_/ubuntu/tags?page=1&name=noble
# Referenced as a build stage, so dependabot is able to keep the version and digest up to date
FROM ubuntu:24.04@sha256:561618e2c15bf2397621dd04f96926663a3b5616c189cf7e38db7e82f5c538ea AS default_root_image

# Micromamba is taken from the official image, pinned by digest for integrity
# Dependabot keeps this version and digest up to date (`docker` ecosystem covers this directory)
# The binary is bind-mounted into the install RUN below, so it is not added to any image layer
FROM mambaorg/micromamba:2.9.0@sha256:b62ed0c54940e3c801642d72ba7d2462f06356c378eba92d603d39f2ce5e4a0d AS micromamba

FROM $ROOT_IMAGE

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for the Server that starts
# but lacks all features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update --yes && \
    # - `apt-get upgrade` is run to patch known vulnerabilities in system packages
    #   as the Ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    ca-certificates \
    locales \
    # - `netbase` provides /etc/{protocols,rpc,services}, part of POSIX
    #   and required by various C functions like getservbyname and getprotobyname
    #   https://github.com/jupyter/docker-stacks/pull/2129
    netbase \
    sudo \
    # - `tini` is installed as a helpful container entrypoint,
    #   that reaps zombie processes and such of the actual executable we want to start
    #   See https://github.com/krallin/tini#why-tini for details
    tini \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "C.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
    # More information in: https://github.com/jupyter/docker-stacks/pull/2047
    # and docs: https://docs.conda.io/projects/conda/en/latest/dev-guide/deep-dives/activation.html
    echo 'eval "$(conda shell.bash hook)"' >> /etc/skel/.bashrc

# Delete existing user with UID="${NB_UID}" if it exists
RUN if id -un "${NB_UID}" >/dev/null 2>&1; then \
        userdel --remove "$(id -un "${NB_UID}")"; \
    fi

# Create "${NB_USER}" user (`jovyan` by default) with UID="${NB_UID}" (`1000` by default) and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Pre-create the cache dir owned by the user, macOS Rosetta junk can then only appear inside it
RUN rm -rf "/home/${NB_USER}/.cache/" && \
    mkdir -p "/home/${NB_USER}/.cache" && \
    chown "${NB_USER}:${NB_GID}" "/home/${NB_USER}/.cache"

RUN rm -rf "/home/${NB_USER}/.cache/rosetta"

USER ${NB_UID}

# Pin the Python version here, or set it to "default"
ARG PYTHON_VERSION=3.13

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}"

# Install the Conda prefix using Micromamba from the digest-pinned official image (see top of this file).
#   <https://github.com/mamba-org/mamba#micromamba>
#   Similar projects using Micromamba:
#     - Micromamba-Docker: <https://github.com/mamba-org/micromamba-docker>
#     - repo2docker: <https://github.com/jupyterhub/repo2docker>
# Install Python, Mamba, and jupyter_core
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
COPY --chown="${NB_UID}:${NB_GID}" initial-condarc "${CONDA_DIR}/.condarc"
WORKDIR /tmp
RUN --mount=type=bind,from=micromamba,source=/bin/micromamba,target=/usr/local/bin/micromamba \
    set -x && \
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" && \
    if [ "${PYTHON_VERSION}" = "default" ]; then PYTHON_SPECIFIER="python"; fi && \
    # Install the packages
    micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        'jupyter_core' \
        'conda' \
        # Install mamba with the same version as the micromamba image pinned above
        # (they are released together), so dependabot keeps the version up to date
        "mamba==$(micromamba --version)" \
        "${PYTHON_SPECIFIER}" && \
    # Pin major.minor version of python
    # https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html#preventing-packages-from-updating-pinning
    mamba list --full-name 'python' | awk 'END{sub("[^.]*$", "*", $2); print $1 " " $2}' >> "${CONDA_DIR}/conda-meta/pinned" && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Copy local files as late as possible to avoid cache busting
COPY _docker_stacks_log.sh run-hooks.sh start.sh /usr/local/bin/

# Configure container entrypoint
ENTRYPOINT ["tini", "-g", "--", "start.sh"]

USER root

# Create dirs for startup hooks
RUN mkdir /usr/local/bin/start-notebook.d && \
    mkdir /usr/local/bin/before-notebook.d

COPY 10activate-conda-env.sh /usr/local/bin/before-notebook.d/

RUN rm -rf "/home/${NB_USER}/.cache/rosetta"

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"
