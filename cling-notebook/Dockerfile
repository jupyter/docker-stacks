FROM jupyter/base-notebook

USER root

ENV PATH /opt/cling_2017-11-13_ubuntu16/bin:$PATH

RUN apt-get -y update && \
    apt-get install -y --upgrade python3-pip     

RUN cd /tmp && \
    wget --quiet https://root.cern.ch/download/cling/cling_2017-11-13_ubuntu16.tar.bz2 && \
    tar -C /opt -xjf cling_2017-11-13_ubuntu16.tar.bz2 && \
    cd /opt/cling_2017-11-13_ubuntu16/share/cling/Jupyter/kernel && \
    pip3 install -e . && \
    jupyter-kernelspec install cling-cpp17 && \
    jupyter-kernelspec install cling-cpp1z && \
    jupyter-kernelspec install cling-cpp14 && \
    jupyter-kernelspec install cling-cpp11

RUN fix-permissions /opt/cling_2017-11-13_ubuntu16
RUN fix-permissions $HOME

USER $NB_USER
