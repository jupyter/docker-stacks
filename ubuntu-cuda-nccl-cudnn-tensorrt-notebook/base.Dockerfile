# Copyright (c) fuzhuzheng Development Team.
# Distributed under the terms of the Modified BSD License.

# Ubuntu 20.04 (focal)
# https://hub.docker.com/_/ubuntu/?tab=tags&name=focal
# OS/ARCH: linux/amd64
ARG BASE_CONTAINER=nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
ARG TENSORRT_URL='https://nvidia-cuda-cudnn-tensortr-jupyter.oss-cn-hongkong.aliyuncs.com/nv-tensorrt-repo-ubuntu1804-cuda10.1-trt6.0.1.5-ga-20190913_1-1_amd64.deb?Expires=1607121449&OSSAccessKeyId=TMP.3KiaWC4Ld6PhYuJn48vsTggbx5WXGSk4z5CkcVM6EGqsUYWYPbPtmGsHLhD9giPxkuGgQ3dsvD2MzSrMJoSmqdBWcepx5i&Signature=BUgEJudm0xivKZyP9sS2pnvOSFU%3D'


FROM $BASE_CONTAINER

LABEL maintainer="fuzhuzheng Project <fuzhuzheng@163.com>"
ARG NB_USER="fuzhuzheng"

