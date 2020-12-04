# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
LABEL maintainer="fuzhuzheng <fuzhuzheng@163.com>"

USER root

RUN tensorrt_file_name=$(echo $TENSORRT_URL|awk -F '?' '{print $1}'|awk -F '/' '{print $4}') && \
    ubuntu_os=$(echo $tensorrt_file_name|awk -F '-' '{print $4}') && \
    cuda_v=$(echo $tensorrt_file_name|awk -F '-' '{print $5}') && \
    tensorrt_v=$(echo $tensorrt_file_name|awk -F '-' '{print $6}') && \
    tensorrt_n=$(echo $tensorrt_v|awk -F 'trt' '{print $2}'|awk -F '.' '{print $1}') && \
    app_v=$(echo $tensorrt_v|awk -F 'trt' '{print $2}'|awk -F '.' '{print $1"."$2"."$3}')-1+${cuda_v} && \
    wget -nv ${TENSORRT_URL} -O ${tensorrt_file_name} && \
    dpkg -i ${tensorrt_file_name} && \
    apt-key add $(echo $tensorrt_file_name|awk -F '-' '{print "/var/"$1"-"$2"-"$3"-"$5"-"$6"-"$7"-"$8}'|awk -F '_' '{print $1"/7fa2af80.pub"}') && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    graphsurgeon-tf=${app_v} \
    libnvinfer-bin=${app_v} \
    libnvinfer-dev=${app_v} \
    libnvinfer-doc=${app_v} \
    libnvinfer-plugin-dev=${app_v} \
    libnvinfer-plugin${tensorrt_n}=${app_v} \
    libnvinfer-samples=${app_v} \
    libnvinfer${tensorrt_n}=${app_v} \
    libnvonnxparsers-dev=${app_v} \
    libnvonnxparsers${tensorrt_n}=${app_v} \
    libnvparsers-dev=${app_v} \
    libnvparsers${tensorrt_n}=${app_v} \
    python-libnvinfer=${app_v} \
    python-libnvinfer-dev=${app_v} \
    python3-libnvinfer=${app_v} \
    python3-libnvinfer-dev=${app_v} \
    tensorrt=$(echo $tensorrt_v|awk -F 'trt' '{print $2}')-1+${cuda_v} \
    uff-converter-tf=${app_v} && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -fr ${tensorrt_file_name}

USER $NB_UID
