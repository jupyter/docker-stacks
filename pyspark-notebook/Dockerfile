# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 2.3.0
ENV HADOOP_VERSION 2.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y openjdk-8-jre-headless ca-certificates-java && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
        wget -q http://apache.claz.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
        echo "258683885383480BA01485D6C6F7DC7CFD559C1584D6CEB7A3BBCF484287F7F57272278568F16227BE46B4F92591768BA3D164420D87014A136BF66280508B46 *spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | sha512sum -c - && \
        tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local --owner root --group root --no-same-owner && \
        rm spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

# Mesos dependencies
# Install from the Xenial Mesosphere repository since there does not (yet)
# exist a Bionic repository and the dependencies seem to be compatible for now.
COPY mesos.key /tmp/
RUN apt-get -y update && \
    apt-get install --no-install-recommends -y gnupg && \
    apt-key add /tmp/mesos.key && \
    echo "deb http://repos.mesosphere.io/ubuntu xenial main" > /etc/apt/sources.list.d/mesosphere.list && \
    apt-get -y update && \
    apt-get --no-install-recommends -y install mesos=1.2\* && \
    apt-get purge --auto-remove -y gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Spark and Mesos config
ENV SPARK_HOME /usr/local/spark
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.6-src.zip
ENV MESOS_NATIVE_LIBRARY /usr/local/lib/libmesos.so
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info



# Azure Storage provider for Spark 
ENV HADOOP_SEMVER $HADOOP_VERSION.0

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends software-properties-common && \
    apt-add-repository universe && \
    apt-get install -y --no-install-recommends  maven && \
    echo "<project>" \
                    "<modelVersion>4.0.0</modelVersion>" \
                    "<groupId>groupId</groupId>" \
                    "<artifactId>artifactId</artifactId>" \
                    "<version>1.0</version>" \
                "<dependencies>" \
                    "<dependency>" \
                        "<groupId>org.apache.hadoop</groupId>" \
                        "<artifactId>hadoop-azure</artifactId>" \
                        "<version>${HADOOP_SEMVER}</version>" \
                    "<exclusions>" \
                        "<exclusion>" \
                            "<groupId>org.apache.hadoop</groupId>" \
                            "<artifactId>hadoop-common</artifactId>" \
                        "</exclusion>" \
                        "<exclusion>" \
                            "<groupId>com.fasterxml.jackson.core</groupId>" \
                            "<artifactId>jackson-core</artifactId>" \
                        "</exclusion>" \
                    "</exclusions> " \
                    "</dependency>" \
                    "<dependency>" \
                        "<groupId>com.microsoft.sqlserver</groupId>" \
                        "<artifactId>mssql-jdbc</artifactId>" \
                        "<version>6.4.0.jre8</version>" \
                    "</dependency>" \
                    "<dependency>" \
                        "<groupId>com.microsoft.azure</groupId>" \
                        "<artifactId>azure-storage</artifactId>" \
                        "<version>2.2.0</version>" \
                        "<exclusions>" \
                            "<exclusion>" \
                                "<groupId>com.fasterxml.jackson.core</groupId>" \
                                "<artifactId>jackson-core</artifactId>" \
                            "</exclusion>" \
                            "<exclusion>" \
                                "<groupId>org.apache.commons</groupId>" \
                                "<artifactId>commons-lang3</artifactId>" \
                            "</exclusion>" \
                            "<exclusion>" \
                                "<groupId>org.slf4j</groupId>" \
                                "<artifactId>slf4j-api</artifactId>" \
                            "</exclusion>" \
                        "</exclusions>" \
                    "</dependency>" \
                    "<dependency>" \
                        "<groupId>com.microsoft.azure</groupId>" \
                        "<artifactId>azure-cosmosdb-spark_2.2.0_2.11</artifactId>" \
                        "<version>1.1.1</version>" \
                        "<exclusions>" \
                            "<exclusion>" \
                                "<groupId>org.apache.tinkerpop</groupId>" \
                                "<artifactId>tinkergraph-gremlin</artifactId>" \
                            "</exclusion>" \
                            "<exclusion>" \
                                "<groupId>org.apache.tinkerpop</groupId>" \
                                "<artifactId>spark-gremlin</artifactId>" \
                            "</exclusion>" \
                            "<exclusion>" \
                                "<groupId>io.netty</groupId>" \
                                "<artifactId>*</artifactId>" \
                            "</exclusion>" \
                            "<exclusion>" \
                                "<groupId>com.fasterxml.jackson.core</groupId>" \
                                "<artifactId>jackson-annotations</artifactId>" \
                            "</exclusion>" \
                        "</exclusions> " \
                    "</dependency>" \
                "</dependencies>" \
            "</project>" > /tmp/pom.xml \
    && cd /tmp \
    && mvn dependency:copy-dependencies -DoutputDirectory="${SPARK_HOME}/jars/" \
    && apt-get --purge autoremove -y maven \
    && rm -rf /tmp/*  

USER $NB_UID

# Install pyarrow
RUN conda install --quiet -y 'pyarrow' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
