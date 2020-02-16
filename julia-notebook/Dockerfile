# Copyright (c) Salzburg Research
FROM jupyter/all-spark-notebook:6c3390a9292e
LABEL maintainer="Christoph Schranz <iotlab@salzburgresarch.at>"

USER root

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  git apt-utils wget python-pip unzip && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

#ENV PYSPARK_PYTHON /opt/conda/bin/python
# Install elasticsearch libs
RUN apt-get update \
 && curl -sL http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/6.8.1/elasticsearch-hadoop-6.8.1.jar

RUN set -ex \
 && buildDeps=' \
    elasticsearch==6.3.1 \
#    rpy2==2.9.4 \
 ' \
 && apt-get update \
 && apt-get -y upgrade \
 && apt-get -y install r-base \
 && pip install --no-cache-dir $buildDeps \
 && rm -rf /home/$NB_USER/.local \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

# Install Graphviz
RUN apt-get update \
  && apt-get install -y graphviz libgraphviz-dev \
  && pip install --no-cache-dir graphviz==0.11

# Install Julia
# install Julia packages in /opt/julia-${JULIA_VERSION} instead of $HOME
ENV JULIA_VERSION=1.1.1
ENV JULIA_PKGDIR=/opt/julia-${JULIA_VERSION}
RUN mkdir /opt/julia-${JULIA_VERSION} && \
    cd /tmp && \
    wget -q https://julialang-s3.julialang.org/bin/linux/x64/1.1/julia-${JULIA_VERSION}-linux-x86_64.tar.gz && \
    tar xzf julia-${JULIA_VERSION}-linux-x86_64.tar.gz -C /opt/julia-${JULIA_VERSION} --strip-components=1 && \
    rm /tmp/julia-${JULIA_VERSION}-linux-x86_64.tar.gz
RUN ln -fs /opt/julia-${JULIA_VERSION}/bin/julia /usr/local/bin/julia

# Show Julia where conda libraries are \
RUN mkdir /etc/julia && \
    echo "push!(Libdl.DL_LOAD_PATH, \"$CONDA_DIR/lib\")" >> /etc/julia/juliarc.jl && \
    chown -R $NB_USER $JULIA_PKGDIR && \
    fix-permissions $JULIA_PKGDIR

# Add Julia packages:
#RUN rm -r /home/jovyan/.julia/registries/General
RUN julia -e 'import Pkg; using Pkg; Pkg.update();Pkg.add("IJulia")'
RUN julia -e 'using Pkg;Pkg.add("DataFrames");Pkg.add("Gadfly");Pkg.add("RDatasets")'
RUN julia -e 'using IJulia'

RUN mv $HOME/.local/share/jupyter/kernels/julia* $CONDA_DIR/share/jupyter/kernels/ && \
    chmod -R go+rx $CONDA_DIR/share/jupyter && \
    fix-permissions $JULIA_PKGDIR $CONDA_DIR/share/jupyter && \
    chown -R  $NB_USER /home/$NB_USER/.julia && \
    chmod -R 755 /home/$NB_USER/.julia

# Install rpy2 to share data between Python and R
RUN conda install rpy2=2.9.4 plotly=4.0.0
RUN conda install -c conda-forge ipyleaflet

# Install various extensions
RUN jupyter labextension install @jupyterlab/github
RUN jupyter labextension install jupyterlab-drawio
RUN jupyter labextension install jupyter-leaflet
RUN jupyter labextension install @jupyterlab/plotly-extension
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter nbextension enable spellchecker/main
RUN jupyter nbextension enable codefolding/main


RUN chown -R $NB_USER /home/$NB_USER/.local && \
    chmod -R 755 /home/$NB_USER/.local

# Change jupyter_notebook_config.py
COPY jupyter_notebook_config.json /home/jovyan/.jupyter/jupyter_notebook_config.json

USER $NB_USER
