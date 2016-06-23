# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    gfortran \
    unixodbc-dev \
    libtool-bin \
    autoconf \
    automake \
    gcc && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Julia dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    julia \
    libnettle4 && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jovyan

# R packages including IRKernel which gets installed globally.
# Note that there is a bug with rpy2 where the %R and %%R don't work.
# We need an newer version not yet available on conda to fix this so uninstall and install new version at end.
RUN conda config --add channels r && \
    conda install --quiet --yes \
    'rpy2=2.7*' \
    'r-base=3.2*' \
    'r-irkernel=0.5*' \
    'r-plyr=1.8*' \
    'r-devtools=1.9*' \
    'r-dplyr=0.4*' \
    'r-ggplot2=1.0*' \
    'r-tidyr=0.3*' \
    'r-shiny=0.12*' \
    'r-rmarkdown=0.8*' \
    'r-forecast=5.8*' \
    'r-stringr=0.6*' \
    'r-rsqlite=1.0*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=0.1*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-dbi=*' \
    'r-scales=*' \
    'r-randomforest=4.6*' && conda clean -tipsy

# Install additional non-conda R packages
RUN R -e 'install.packages(c("ggthemes", "RODBC", "sendmailR", "tis"), repos="http://cran.utstat.utoronto.ca/")'

# Install IJulia packages as jovyan and then move the kernelspec out
# to the system share location. Avoids problems with runtime UID change not
# taking effect properly on the .local folder in the jovyan home dir.
RUN julia -e 'Pkg.add("IJulia")' && \
    mv /home/$NB_USER/.local/share/jupyter/kernels/* $CONDA_DIR/share/jupyter/kernels/ && \
    chmod -R go+rx $CONDA_DIR/share/jupyter && \
    rm -rf /home/$NB_USER/.local/share

# Show Julia where conda libraries are
# Add essential packages
RUN echo 'push!(Sys.DL_LOAD_PATH, "/opt/conda/lib")' > /home/$NB_USER/.juliarc.jl && \
julia -e 'Pkg.add("Gadfly")' && julia -e 'Pkg.add("RDatasets")' && julia -F -e 'Pkg.add("HDF5")'

# Fix the graphing issue with ggplot2
# from: https://github.com/jupyter/docker-stacks/issues/210
RUN echo "jpeg 8*" >> /opt/conda/conda-meta/pinned
RUN conda update --all -y

# Add odbc drivers to the install
RUN cd /home/jovyan && \
    wget ftp://ftp.freetds.org/pub/freetds/stable/freetds-patched.tar.gz && \
    tar xvzf freetds-patched.tar.gz && \
    cd /home/jovyan/freetds-1.00.6 && \
    ./configure --prefix=/home/jovyan/odbcdriver && \
    make && \
    make install

# Add ODBC configuration file
RUN echo "[ODBC Data Sources]" >> ~/.odbc.ini && \
    echo "SQL_DB = Sample Database Configuration" >> ~/.odbc.ini && \
    echo "" >> ~/.odbc.ini && \
    echo "[Default]" >> ~/.odbc.ini && \
    echo "" >> ~/.odbc.ini && \
    echo "[SQL_DB]" >> ~/.odbc.ini && \
    echo "Description      = Sample Database Configuration" >> ~/.odbc.ini && \
    echo "Driver           = /home/jovyan/odbcdriver/lib/libtdsodbc.so" >> ~/.odbc.ini && \
    echo "Trace            = No" >> ~/.odbc.ini && \
    echo "TraceFile        = /home/jovyan/prodms.log" >> ~/.odbc.ini && \
    echo "Server           = MachineIPAddress >> ~/.odbc.ini && \
    echo "Host             = MachineHostName >> ~/.odbc.ini && \
    echo "Port             = MachineDBPort" >> ~/.odbc.ini && \
    echo "Database         = DatabaseInstanceName" >> ~/.odbc.ini && \
    echo "UID              = DatabaseUserName" >> ~/.odbc.ini && \
    echo "PWD              = DatabasePassword >> ~/.odbc.ini && \
    echo "Protocol         =" >> ~/.odbc.ini && \
    echo "ReadOnly         = No" >> ~/.odbc.ini && \
    echo "RowVersioning    = No" >> ~/.odbc.ini && \
    echo "ShowSystemTables = No" >> ~/.odbc.ini && \
    echo "ShowOidColumn    = No" >> ~/.odbc.ini && \
    echo "FakeOidIndex     = No" >> ~/.odbc.ini && \
    echo "ConnSettings     =" >> ~/.odbc.ini && \
    echo "TDS_Version      = 7.0" >> ~/.odbc.ini 

# Fix the version of rpy2 since the 2.7 is broken.  See note above
RUN conda uninstall rpy2 && \
    conda install -c bioconda rpy2=2.7.8

# Fix the ipywidgets since the base image has an older version of ipywidgets.
# This older version works with the Python2 instance but not the Python3 instance.
# Installing a newer version allows the widgets to work with both Python versions.
RUN conda uninstall ipywidgets && \
    conda install -c conda-forge ipywidgets=5.1.5

