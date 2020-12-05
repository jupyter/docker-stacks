# Copyright (c) fuzhuzheng Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=fuzhuzheng/ubuntu-cuda-nccl-cudnn-tensorrt-notebook:ubuntu18.04-cuda10.2-nccl2.7-cudnn7-tensorrt7-notebook
FROM $BASE_CONTAINER

LABEL maintainer="fuzhuzheng <fuzhuzheng@163.com>"

# Install paddle
RUN pip install --quiet --no-cache-dir \
    paddlepaddle-gpu==2.0.0rc0 \
    paddlehub==2.0.0b1 \
    -i https://mirror.baidu.com/pypi/simple && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
