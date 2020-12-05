# Copyright (c) fuzhuzheng Development Team.
# Distributed under the terms of the Modified BSD License.

# Ubuntu 20.04 (focal)
# https://hub.docker.com/_/ubuntu/?tab=tags&name=focal
# OS/ARCH: linux/amd64
ARG BASE_CONTAINER=nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
FROM $BASE_CONTAINER

LABEL maintainer="fuzhuzheng Project <fuzhuzheng@163.com>"
ARG NB_USER="fuzhuzheng"
ARG TENSORRT_URL='https://nvidia-cuda-cudnn-tensortr-jupyter.oss-cn-hongkong.aliyuncs.com/nv-tensorrt-repo-ubuntu1804-cuda10.1-trt6.0.1.5-ga-20190913_1-1_amd64.deb?Expires=1607181704&OSSAccessKeyId=TMP.3KdjCbaMXxgD79Nfb3rXFTEJVibsQ6Aq2NeZd29uvqgmXTAz6dC8fXm1m8zxSQkmUmTKb26GJTq2WFx4xyz3QE5SgmRkvU&Signature=%2Bw68hqUzDlthYeVxmSa49%2BUICDA%3D'



