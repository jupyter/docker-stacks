ARG BASE_IMAGE=quay.io/jupyter/base-notebook
FROM $BASE_IMAGE

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

ENV MSSQL_DRIVER="ODBC Driver 18 for SQL Server"
ENV PATH="/opt/mssql-tools18/bin:${PATH}"

# `packages-microsoft-prod` sets up the repository together with its signing key for the current Ubuntu version
RUN . /etc/os-release && \
    wget --progress=dot:giga --no-hsts --output-document=/tmp/packages-microsoft-prod.deb \
        "https://packages.microsoft.com/config/ubuntu/${VERSION_ID}/packages-microsoft-prod.deb" && \
    dpkg --install /tmp/packages-microsoft-prod.deb && \
    rm /tmp/packages-microsoft-prod.deb

RUN apt-get update --yes && \
    ACCEPT_EULA=Y apt-get install --yes --no-install-recommends msodbcsql18 && \
    # optional: for bcp and sqlcmd
    ACCEPT_EULA=Y apt-get install --yes --no-install-recommends mssql-tools18 && \
    # optional: for unixODBC development headers
    apt-get install --yes --no-install-recommends unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

RUN mamba install --yes 'pyodbc' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
