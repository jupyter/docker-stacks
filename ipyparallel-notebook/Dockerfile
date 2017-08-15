# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyterhub/systemuser

USER root

WORKDIR /opt

ENV CONDA_DIR /opt/conda

# update apt-get source with 163
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://mirrors.163.com/debian/ jessie main non-free contrib" >/etc/apt/sources.list && \
    echo "deb http://mirrors.163.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.163.com/debian/ jessie main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.163.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list

RUN apt-get update --fix-missing && apt-get install git gcc g++ build-essential -y

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
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ --system && \
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ --system && \
conda config --set show_channel_urls yes --system && \
conda config --set allow_softlinks False --system

# Install Python 3 packages
RUN conda install --quiet --yes \
    'ipyparallel=6.0.*' \
    'nb_conda'

# Create Python 2 and Install Python 2 packages
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 && \
$CONDA_DIR/envs/python2/bin/conda install --quiet --yes \
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

RUN pip install --no-cache -q -r /opt/requirements.txt && \
${CONDA_DIR}/envs/python2/bin/pip install --no-cache -q -r /opt/requirements.txt && \
pip install --no-cache -q TA-lib && \
${CONDA_DIR}/envs/python2/bin/pip install --no-cache -q TA-lib

COPY ./submodule /opt/submodule

RUN cd /opt/submodule && \
ls -F1 | sed 's/\///g' | xargs -I {} bash -c "echo {} && cd {} && pip install --no-cache -q --force-reinstall ." && \
cd ..

RUN conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy && \
    ${CONDAIR}/env/python2/bin/conda remove --quiet --yes --force qt pyqt && \
    ${CONDAIR}/env/python2/bin/conda clean -tipsy