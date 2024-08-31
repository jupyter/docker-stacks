FROM quay.io/jupyter/base-notebook:ubuntu-22.04

USER root

# Install Java & Oracle SQL Instant Client
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends software-properties-common && \
    add-apt-repository universe && \
    apt-get update --yes && \
    apt-get install --yes --no-install-recommends alien default-jre default-jdk openjdk-11-jdk libaio1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Oracle
ARG INSTANTCLIENT_MAJOR_VERSION=23
ARG INSTANTCLIENT_BIN_SUFFIX=${INSTANTCLIENT_MAJOR_VERSION}.4.0.24.05-1.el9.x86_64.rpm
ARG INSTANTCLIENT_URL=https://download.oracle.com/otn_software/linux/instantclient/2340000

# Then install Oracle SQL Instant client, SQL+Plus, tools, and JDBC.
# Note: You may need to change the URL to a newer version.
# See: https://www.oracle.com/es/database/technologies/instant-client/linux-x86-64-downloads.html
RUN mkdir "/opt/oracle"
WORKDIR "/opt/oracle"
# alien doesn't work well with sqlplus, so skipping it for now
RUN wget --progress=dot:giga "${INSTANTCLIENT_URL}/oracle-instantclient-basiclite-${INSTANTCLIENT_BIN_SUFFIX}" && \
    alien --install --scripts "oracle-instantclient-basiclite-${INSTANTCLIENT_BIN_SUFFIX}" && \
    wget --progress=dot:giga "${INSTANTCLIENT_URL}/oracle-instantclient-sqlplus-${INSTANTCLIENT_BIN_SUFFIX}" && \
    # alien --install --scripts "oracle-instantclient-sqlplus-${INSTANTCLIENT_BIN_SUFFIX}" && \
    wget --progress=dot:giga "${INSTANTCLIENT_URL}/oracle-instantclient-tools-${INSTANTCLIENT_BIN_SUFFIX}" && \
    alien --install --scripts "oracle-instantclient-tools-${INSTANTCLIENT_BIN_SUFFIX}" && \
    wget --progress=dot:giga "${INSTANTCLIENT_URL}/oracle-instantclient-jdbc-${INSTANTCLIENT_BIN_SUFFIX}" && \
    alien --install --scripts "oracle-instantclient-jdbc-${INSTANTCLIENT_BIN_SUFFIX}" && \
    chown -R "${NB_UID}":"${NB_GID}" "${HOME}/.rpmdb" && \
    rm -f ./*.rpm

# And configure variables
RUN echo "ORACLE_HOME=/usr/lib/oracle/${INSTANTCLIENT_MAJOR_VERSION}/client64" >> "${HOME}/.bashrc" && \
    echo "PATH=\"${ORACLE_HOME}/bin:${PATH}\"" >> "${HOME}/.bashrc" && \
    echo "LD_LIBRARY_PATH=\"${ORACLE_HOME}/lib:${LD_LIBRARY_PATH}\"" >> "${HOME}/.bashrc" && \
    echo "export ORACLE_HOME" >> "${HOME}/.bashrc" && \
    echo "export PATH" >> "${HOME}/.bashrc" && \
    echo "export LD_LIBRARY_PATH" >> "${HOME}/.bashrc"

# Add credentials for /redacted/ using Oracle DB.
WORKDIR /usr/lib/oracle/${INSTANTCLIENT_MAJOR_VERSION}/client64/lib/network/admin/
# Add a wildcard `[]` on the last letter of the filename to avoid throwing an error if the file does not exist.
# See: https://stackoverflow.com/questions/31528384/conditional-copy-add-in-dockerfile
COPY cwallet.ss[o] ./
COPY sqlnet.or[a] ./
COPY tnsnames.or[a] ./

# Switch back to jovyan to avoid accidental container runs as root
USER "${NB_UID}"

WORKDIR "${HOME}"

# Install `oracledb` Python library to use Oracle SQL Instant Client
RUN mamba install --yes 'oracledb' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
