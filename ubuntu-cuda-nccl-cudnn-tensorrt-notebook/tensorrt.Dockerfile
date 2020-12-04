LABEL maintainer="fuzhuzheng <fuzhuzheng@163.com>"

USER root

RUN wget 'https://nvidia-cuda-cudnn-tensortr-jupyter.oss-cn-hongkong.aliyuncs.com/nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.2.1.6-ga-20201006_1-1_amd64.deb?Expires=1606932105&OSSAccessKeyId=TMP.3Kg43SoAHNv5CuQnAirTQCGsWLnwoN6TsvcHLB7RanYyeP5KY8r4Wd6WzckXAQJHbcsmkB33nU3wemcMpiSyCRaK6626wt&Signature=LqwuUIgLeuJsm1ID%2F69PQWBcfEA%3D' -O nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.2.1.6-ga-20201006_1-1_amd64.deb && \
    dpkg -i nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.2.1.6-ga-20201006_1-1_amd64.deb && \
    apt-key add /var/nv-tensorrt-repo-cuda10.2-trt7.2.1.6-ga-20201006/7fa2af80.pub && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    graphsurgeon-tf=7.2.1-1+cuda10.2 \
    libnvinfer-bin=7.2.1-1+cuda10.2 \
    libnvinfer-dev=7.2.1-1+cuda10.2 \
    libnvinfer-doc=7.2.1-1+cuda10.2 \
    libnvinfer-plugin-dev=7.2.1-1+cuda10.2 \
    libnvinfer-plugin7=7.2.1-1+cuda10.2 \
    libnvinfer-samples=7.2.1-1+cuda10.2 \
    libnvinfer7=7.2.1-1+cuda10.2 \
    libnvonnxparsers-dev=7.2.1-1+cuda10.2 \
    libnvonnxparsers7=7.2.1-1+cuda10.2 \
    libnvparsers-dev=7.2.1-1+cuda10.2 \
    libnvparsers7=7.2.1-1+cuda10.2 \
    python-libnvinfer=7.2.1-1+cuda10.2 \
    python-libnvinfer-dev=7.2.1-1+cuda10.2 \
    python3-libnvinfer=7.2.1-1+cuda10.2 \
    python3-libnvinfer-dev=7.2.1-1+cuda10.2 \
    tensorrt=7.2.1.6-1+cuda10.2 \
    uff-converter-tf=7.2.1-1+cuda10.2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -fr ./nv-tensorrt-repo-ubuntu1804-cuda10.2-trt7.2.1.6-ga-20201006_1-1_amd64.deb


USER $NB_UID
