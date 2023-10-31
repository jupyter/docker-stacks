FROM quay.io/jupyter/base-notebook

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

ENV MSSQL_DRIVER "ODBC Driver 18 for SQL Server"
ENV PATH="/opt/mssql-tools18/bin:${PATH}"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends curl gnupg2 lsb-release && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update --yes && \
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
