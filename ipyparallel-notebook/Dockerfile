# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM jupyter/scipy-notebook

USER root

RUN userdel $NB_USER && rm -rf /home/$NB_USER

WORKDIR /opt

ENV CONDA_DIR /opt/conda

# RUN apt-get update --fix-missing && apt-get install git gcc g++ build-essential -y

# TA-lib dependencies
RUN wget -O ta-lib.tar.gz http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
tar -xzf ta-lib.tar.gz &&\
cd ta-lib && ./configure --prefix=/usr && make && make install && cd ..

# update pip source
RUN mkdir -p ~/.pip && \
echo "[global]" > ~/.pip/pip.conf && \
echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf && \
echo "" >> ~/.pip/pip.conf && \
echo "[install]" >> ~/.pip/pip.conf && \
echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf

# activate ipyparallel-mesos
RUN pip install jupyter_contrib_nbextensions && \
pip install jupyter_nbextensions_configurator

# update conda settings
RUN rm /opt/conda/.condarc && \
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ --system && \
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ --system && \
conda config --set show_channel_urls yes --system && \
conda config --set allow_softlinks False --system

# Install Python 3 packages
RUN conda install --quiet --yes \
    'ipyparallel=6.0.*'

# Create Python 2 and Install Python 2 packages
# Install Python 2 packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 \
    'nomkl' \
    'ipython=5.3*' \
    'ipywidgets=6.0*' \
    'pandas=0.19*' \
    'numexpr=2.6*' \
    'matplotlib=2.0*' \
    'scipy=0.19*' \
    'seaborn=0.7*' \
    'scikit-learn=0.18*' \
    'scikit-image=0.12*' \
    'sympy=1.0*' \
    'cython=0.25*' \
    'patsy=0.4*' \
    'statsmodels=0.8*' \
    'cloudpickle=0.2*' \
    'dill=0.2*' \
    'numba=0.31*' \
    'bokeh=0.12*' \
    'hdf5=1.8.17' \
    'h5py=2.6*' \
    'sqlalchemy=1.1*' \
    'pyzmq' \
    'vincent=0.4.*' \
    'beautifulsoup4=4.5.*' \
    'xlrd' \
    'ipyparallel=6.0.*'

# Add shortcuts to distinguish pip for python2 and python3 envs
RUN ln -s $CONDA_DIR/envs/python2/bin/pip $CONDA_DIR/bin/pip2 && \
    ln -s $CONDA_DIR/bin/pip $CONDA_DIR/bin/pip3

RUN jupyter nbextension install --sys-prefix --py ipyparallel  &&\
    jupyter nbextension enable --sys-prefix --py ipyparallel  &&\
    jupyter serverextension enable --sys-prefix --py ipyparallel &&\
    jupyter contrib nbextension install --sys-prefix && \
    jupyter nbextensions_configurator enable --sys-prefix &&\
    jupyter nbextensions_configurator enable --system

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/usr/local/bin/start-systemuser.sh"]

COPY systemuser.sh /usr/local/bin/start-systemuser.sh

# install all extra packages at last to ensure cache works well
COPY ./requirements.txt /opt/requirements.txt

ARG PIP_EXTRA

RUN pip install --no-cache ${PIP_EXTRA} TA-lib && \
${CONDA_DIR}/envs/python2/bin/pip install --no-cache ${PIP_EXTRA} TA-lib

RUN pip install --no-cache ${PIP_EXTRA} -r /opt/requirements.txt

RUN ${CONDA_DIR}/envs/python2/bin/pip install --no-cache ${PIP_EXTRA} -r /opt/requirements.txt

COPY ./submodule /opt/submodule

RUN cd /opt/submodule && \
ls -F1 | sed 's/\///g' | xargs -I {} bash -c "echo {} && cd {} && pip --no-cache install -q --force-reinstall ." && \
cd ..

RUN conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy && \
    ${CONDA_DIR}/env/python2/bin/conda remove --quiet --yes --force qt pyqt && \
    ${CONDA_DIR}/env/python2/bin/conda clean -tipsy