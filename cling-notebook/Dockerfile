FROM jupyter/base-notebook

USER root

ENV PATH=/opt/cling_2017-11-13_ubuntu16/bin:$PATH \
    CLING_VERSION=cling_2017-11-13_ubuntu16

RUN apt-get -y update && \
    apt-get install -y --upgrade python3-pip     

RUN cd /tmp && \
    wget --quiet https://root.cern.ch/download/cling/${CLING_VERSION}.tar.bz2 && \
    tar -C /opt -xjf ${CLING_VERSION}.tar.bz2 && \
    cd /opt/${CLING_VERSION}/share/cling/Jupyter/kernel && \
    pip3 install -e . && \
    jupyter-kernelspec install cling-cpp17 && \
    jupyter-kernelspec install cling-cpp1z && \
    jupyter-kernelspec install cling-cpp14 && \
    jupyter-kernelspec install cling-cpp11

RUN fix-permissions /opt/${CLING_VERSION}
RUN fix-permissions $HOME

USER $NB_USER
