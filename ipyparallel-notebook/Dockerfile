# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook

USER root

# update apt-get source with 163
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://mirrors.163.com/debian/ jessie main non-free contrib" >/etc/apt/sources.list && \
    echo "deb http://mirrors.163.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.163.com/debian/ jessie main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.163.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list

USER $NB_USER

# update pip source
RUN mkdir -p ~/.pip && \
echo "[global]" > ~/.pip/pip.conf && \
echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf && \
echo "" >> ~/.pip/pip.conf && \
echo "[install]" >> ~/.pip/pip.conf && \
echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf

# update conda source
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda config --set show_channel_urls yes

# Install Python 3 packages
RUN conda install --quiet --yes \
    'ipyparallel=6.0.*'

# Install Python 2 packages
RUN $CONDA_DIR/envs/python2/bin/conda install --quiet --yes \
    'ipyparallel=6.0.*'

# activate ipyparallel-mesos
RUN pip install git+git://github.com/xingetouzi/ipyparallel-mesos.git

RUN jupyter nbextension install --sys-prefix --py ipyparallel  &&\
    jupyter nbextension enable --sys-prefix --py ipyparallel  &&\
    jupyter serverextension enable --sys-prefix --py ipyparallel

COPY profile /tmp/profile

RUN /tmp/profile/create_profile.sh -f /tmp/profile/profiles

ENTRYPOINT ["tini", "--"]

CMD ["start-singleuser.sh"]