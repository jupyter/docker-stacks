FROM jupyter/base-notebook

## Install java, javac and alien
USER root
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends software-properties-common && \
    apt-get clean && rm -rf /var/lib/apt/lists/*  && \
    apt-get update --yes && \
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
    alien -d --scripts oracle-instantclient-basiclite-21.11.0.0.0-1.el8.x86_64.rpm && \
    dpkg -i oracle-instantclient-basiclite_21.11.0.0.0-2_amd64.deb && \
    wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-sqlplus-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien -d  --scripts oracle-instantclient-sqlplus-21.11.0.0.0-1.el8.x86_64.rpm && \
    dpkg -i oracle-instantclient-sqlplus_21.11.0.0.0-2_amd64.deb && \
    wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-tools-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien -d --scripts oracle-instantclient-tools-21.11.0.0.0-1.el8.x86_64.rpm && \
    dpkg -i oracle-instantclient-tools_21.11.0.0.0-2_amd64.deb && \
    wget --progress=dot:giga https://download.oracle.com/otn_software/linux/instantclient/2111000/oracle-instantclient-jdbc-21.11.0.0.0-1.el8.x86_64.rpm && \
    alien -d --scripts oracle-instantclient-jdbc-21.11.0.0.0-1.el8.x86_64.rpm && \
    dpkg -i oracle-instantclient-jdbc_21.11.0.0.0-2_amd64.deb
## Remove temporary files to avoid issues with `fix-permissions` commands
RUN rm "*.deb" && rm "*.rpm" & chown -R "${NB_UID}":"${NB_GID}" "${HOME}/.rpmdb"

## Configure environment
## Note: You may need to change the ORACLE_HOME path to a different version `.../oracle/21/...`.
RUN echo "ORACLE_HOME=/usr/lib/oracle/21/client64" >> "${HOME}/.bashrc"
RUN echo "PATH=$ORACLE_HOME/bin:$PATH" >> "${HOME}/.bashrc" && \
    echo "LD_LIBRARY_PATH=$ORACLE_HOME/lib" >> "${HOME}/.bashrc" && \
    echo "export ORACLE_HOME" >> "${HOME}/.bashrc" && \
    echo "export LD_LIBRARY_PATH" >> "${HOME}/.bashrc" && \
    echo "export PATH" >> "${HOME}/.bashrc"

## (Optional) Add credentials for the Oracle Database server; files must be present on your root folder.
WORKDIR /usr/lib/oracle/21/client64/lib
## Adding a wildcard `[]` on the last letter of the filename to avoid throwing an error if the file does not exist.
## See: https://stackoverflow.com/questions/31528384/conditional-copy-add-in-dockerfile
COPY cwallet.ss[o] /usr/lib/oracle/21/client64/lib/network/admin
COPY sqlnet.or[a] /usr/lib/oracle/21/client64/lib/network/admin
COPY tnsnames.or[a] /usr/lib/oracle/21/client64/lib/network/admin

## Switch back to jovyan.
USER "${NB_UID}"

## Install `oracledb` Python library to use Oracle SQL Instant Client with `--upgrade --user` options enabled
RUN "${CONDA_DIR}/envs/${CONDA_ENV}/bin/pip" install --no-cache-dir oracledb --upgrade --user && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "${HOME}"
