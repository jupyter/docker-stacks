FROM jupyter/base-notebook

USER root

# Install java, javac and alien
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends software-properties-common && \
    add-apt-repository universe && \
    apt-get update --yes && \
    apt-get install --yes --no-install-recommends alien default-jre default-jdk openjdk-11-jdk libaio1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG instantclient_major_version=21
ARG instantclient_version=${instantclient_major_version}.11.0.0.0-1
ARG instantclient_url=https://download.oracle.com/otn_software/linux/instantclient/2111000

# Then install Oracle SQL Instant client, SQL+Plus, tools and JDBC.
# Note: You may need to change the URL to a newer version.
# See: https://www.oracle.com/es/database/technologies/instant-client/linux-x86-64-downloads.html
WORKDIR "/tmp"
RUN wget --progress=dot:giga ${instantclient_url}/oracle-instantclient-basiclite-${instantclient_version}.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-basiclite-${instantclient_version}.el8.x86_64.rpm && \
    wget --progress=dot:giga ${instantclient_url}/oracle-instantclient-sqlplus-${instantclient_version}.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-sqlplus-${instantclient_version}.el8.x86_64.rpm && \
    wget --progress=dot:giga ${instantclient_url}/oracle-instantclient-tools-${instantclient_version}.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-tools-${instantclient_version}.el8.x86_64.rpm && \
    wget --progress=dot:giga ${instantclient_url}/oracle-instantclient-jdbc-${instantclient_version}.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-jdbc-${instantclient_version}.el8.x86_64.rpm && \
    chown -R "${NB_UID}":"${NB_GID}" "${HOME}/.rpmdb" && \
    rm -f ./*.rpm

# Configure environment
ENV ORACLE_HOME=/usr/lib/oracle/${instantclient_major_version}/client64
ENV PATH="${ORACLE_HOME}/bin:${PATH}"
ENV LD_LIBRARY_PATH="${ORACLE_HOME}/lib:${LD_LIBRARY_PATH}"

# (Optional) Add credentials for the Oracle Database server; files must be present on your `docker build PATH` folder.
WORKDIR /usr/lib/oracle/${instantclient_major_version}/client64/lib/network/admin
# Adding a wildcard `[]` on the last letter of the filename to avoid throwing an error if the file does not exist.
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
