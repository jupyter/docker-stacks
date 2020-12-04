# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
LABEL maintainer="fuzhuzheng <fuzhuzheng@163.com>"
ARG TENSORRT_URL='https://nvidia-cuda-cudnn-tensortr-jupyter.oss-cn-hongkong.aliyuncs.com/nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.2.1.6-ga-20201006_1-1_amd64.deb?Expires=1606932105&OSSAccessKeyId=TMP.3Kg43SoAHNv5CuQnAirTQCGsWLnwoN6TsvcHLB7RanYyeP5KY8r4Wd6WzckXAQJHbcsmkB33nU3wemcMpiSyCRaK6626wt&Signature=LqwuUIgLeuJsm1ID%2F69PQWBcfEA%3D'

USER root

RUN tensorrt_file_name=$(echo $TENSORRT_URL|awk -F '?' '{print $1}'|awk -F '/' '{print $4}') && \
    ubuntu_os=$(echo $tensorrt_file_name|awk -F '-' '{print $4}') && \
    cuda_v=$(echo $tensorrt_file_name|awk -F '-' '{print $5}') && \
    tensorrt_v=$(echo $tensorrt_file_name|awk -F '-' '{print $6}') && \
    app_v=$(echo $tensorrt_v|awk -F 'trt' '{print $2}'|awk -F '.' '{print $1"."$2"."$3}')-1+${cuda_v} && \
    RUN wget $TENSORRT_URL -O $tensorrt_file_name && \
    dpkg -i $tensorrt_file_name && \
    apt-key add $(echo $tensorrt_file_name|awk -F '-' '{print "/var/"$1"-"$2"-"$3"-"$5"-"$6"-"$7"-"$8"/7fa2af80.pub"}'|awk -F '_' '{print $1}') && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    graphsurgeon-tf=$app_v \
    libnvinfer-bin=$app_v \
    libnvinfer-dev=$app_v \
    libnvinfer-doc=$app_v \
    libnvinfer-plugin-dev=$app_v \
    libnvinfer-plugin7=$app_v \
    libnvinfer-samples=$app_v \
    libnvinfer7=$app_v \
    libnvonnxparsers-dev=$app_v \
    libnvonnxparsers7=$app_v \
    libnvparsers-dev=$app_v \
    libnvparsers7=$app_v \
    python-libnvinfer=$app_v \
    python-libnvinfer-dev=$app_v \
    python3-libnvinfer=$app_v \
    python3-libnvinfer-dev=$app_v \
    tensorrt=$(echo $tensorrt_v|awk -F 'trt' '{print $2}')-1+$cuda_v \
    uff-converter-tf=$app_v && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -fr $tensorrt_file_name

USER $NB_UID
