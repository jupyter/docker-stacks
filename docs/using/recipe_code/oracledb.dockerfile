FROM jupyter/base-notebook

## Install java, javac and alien
USER root
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends software-properties-common && \
    add-apt-repository universe && \
    apt-get update --yes && \
    apt-get install --yes --no-install-recommends alien default-jre default-jdk openjdk-11-jdk libaio1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

## Then install Oracle SQL Instant client, SQL+Plus, tools and JDBC.
## Note: You may need to change the URL to a newer version.
## See: https://www.oracle.com/es/database/technologies/instant-client/linux-x86-64-downloads.html
RUN mkdir "/opt/oracle"
WORKDIR "/opt/oracle"
RUN wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-basiclite-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-basiclite-21.11.0.0.0-1.el8.x86_64.rpm && \
    wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-sqlplus-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-sqlplus-21.11.0.0.0-1.el8.x86_64.rpm && \
    wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-tools-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-tools-21.11.0.0.0-1.el8.x86_64.rpm && \
    wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-jdbc-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien --install --scripts oracle-instantclient-jdbc-21.11.0.0.0-1.el8.x86_64.rpm && \
    chown -R "${NB_UID}":"${NB_GID}" "${HOME}/.rpmdb" && \
    rm -f ./*.rpm

## Configure environment
## Note: You may need to change the ORACLE_HOME path to a different version `.../oracle/21/...`.
ENV ORACLE_HOME=/usr/lib/oracle/21/client64
ENV PATH="${ORACLE_HOME}/bin:${PATH}"
ENV LD_LIBRARY_PATH="${ORACLE_HOME}/lib:${LD_LIBRARY_PATH}"

## (Optional) Add credentials for the Oracle Database server; files must be present on your root folder.
WORKDIR /usr/lib/oracle/21/client64/lib/network/admin
## Adding a wildcard `[]` on the last letter of the filename to avoid throwing an error if the file does not exist.
## See: https://stackoverflow.com/questions/31528384/conditional-copy-add-in-dockerfile
COPY cwallet.ss[o] ./
COPY sqlnet.or[a] ./
COPY tnsnames.or[a] ./

## Switch back to jovyan.
USER "${NB_UID}"

## Change workdir back to jovyan.
WORKDIR "${HOME}"

## Install `oracledb` Python library to use Oracle SQL Instant Client

RUN mamba install --yes 'oracledb' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
