# Contributed Recipes

Users sometimes share interesting ways of using the Jupyter Docker Stacks. We encourage users to
[contribute these recipes](../contributing/recipes.md) to the documentation in case they prove
useful to other members of the community by submitting a pull request to `docs/using/recipes.md`.
The sections below capture this knowledge.

## Using `sudo` within a container

Password authentication is disabled for the `NB_USER` (e.g., `jovyan`). This choice was made to
avoid distributing images with a weak default password that users ~might~ will forget to change
before running a container on a publicly accessible host.

You can grant the within-container `NB_USER` passwordless `sudo` access by adding
`-e GRANT_SUDO=yes` and `--user root` to your Docker command line or appropriate container
orchestrator config.

For example:

```bash
docker run -it -e GRANT_SUDO=yes --user root jupyter/minimal-notebook
```

**You should only enable `sudo` if you trust the user and/or if the container is running on an
isolated host.** See [Docker security documentation](https://docs.docker.com/engine/security/userns-remap/) for more information about running containers as `root`.

## Using `pip install` or `conda install` in a Child Docker image

Create a new Dockerfile like the one shown below.

```dockerfile
# Start from a core stack version
FROM jupyter/datascience-notebook:9f9e5ca8fe5a
# Install in the default python3 environment
RUN pip install 'ggplot==0.6.8'
```

Then build a new image.

```bash
docker build --rm -t jupyter/my-datascience-notebook .
```

To use a requirements.txt file, first create your `requirements.txt` file with the listing of
packages desired. Next, create a new Dockerfile like the one shown below.

```dockerfile
# Start from a core stack version
FROM jupyter/datascience-notebook:9f9e5ca8fe5a
# Install from requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
```

For conda, the Dockerfile is similar:

```dockerfile
# Start from a core stack version
FROM jupyter/datascience-notebook:9f9e5ca8fe5a
# Install from requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN conda install --yes --file /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
```

Ref:
[docker-stacks/commit/79169618d571506304934a7b29039085e77db78c](https://github.com/jupyter/docker-stacks/commit/79169618d571506304934a7b29039085e77db78c#commitcomment-15960081)

## Add a Python 2.x environment

Python 2.x was removed from all images on August 10th, 2017, starting in tag `cc9feab481f7`. You can
add a Python 2.x environment by defining your own Dockerfile inheriting from one of the images like
so:

```dockerfile
# Choose your desired base image
FROM jupyter/scipy-notebook:latest

# Create a Python 2.x environment using conda including at least the ipython kernel
# and the kernda utility. Add any additional packages you want available for use
# in a Python 2 notebook to the first line here (e.g., pandas, matplotlib, etc.)
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 ipython ipykernel kernda && \
    conda clean --all -f -y

USER root

# Create a global kernelspec in the image and modify it so that it properly activates
# the python2 conda environment.
RUN $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
$CONDA_DIR/envs/python2/bin/kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json

USER $NB_USER
```

Ref:
[https://github.com/jupyter/docker-stacks/issues/440](https://github.com/jupyter/docker-stacks/issues/440)

## Add a Python 3.x environment

The default version of Python that ships with conda/ubuntu may not be the version you want.
To add a conda environment with a different version and make it accessible to Jupyter, the instructions are very similar to Python 2.x but are slightly simpler (no need to switch to `root`):

```dockerfile
# Choose your desired base image
FROM jupyter/minimal-notebook:latest

# name your environment and choose python 3.x version
ARG conda_env=python36
ARG py_ver=3.6

# you can add additional libraries you want conda to install by listing them below the first line and ending with "&& \"
RUN conda create --quiet --yes -p $CONDA_DIR/envs/$conda_env python=$py_ver ipython ipykernel && \
    conda clean --all -f -y

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml /home/$NB_USER/tmp/
# RUN cd /home/$NB_USER/tmp/ && \
#     conda env create -p $CONDA_DIR/envs/$conda_env -f environment.yml && \
#     conda clean --all -f -y


# create Python 3.x environment and link it to jupyter
RUN $CONDA_DIR/envs/${conda_env}/bin/python -m ipykernel install --user --name=${conda_env} && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# any additional pip installs can be added by uncommenting the following line
# RUN $CONDA_DIR/envs/${conda_env}/bin/pip install

# prepend conda environment to path
ENV PATH $CONDA_DIR/envs/${conda_env}/bin:$PATH

# if you want this environment to be the default one, uncomment the following line:
# ENV CONDA_DEFAULT_ENV ${conda_env}
```

## Run JupyterLab

JupyterLab is preinstalled as a notebook extension starting in tag
[c33a7dc0eece](https://github.com/jupyter/docker-stacks/wiki/Docker-build-history).

Run jupyterlab using a command such as
`docker run -it --rm -p 8888:8888 jupyter/datascience-notebook start.sh jupyter lab`

## Dask JupyterLab Extension

[Dask JupyterLab Extension](https://github.com/dask/dask-labextension) provides a JupyterLab extension to manage Dask clusters, as well as embed Dask's dashboard plots directly into JupyterLab panes. Create the Dockerfile as:

```dockerfile
# Start from a core stack version
FROM jupyter/scipy-notebook:latest

# Install the Dask dashboard
RUN pip install dask-labextension

# Dask Scheduler & Bokeh ports
EXPOSE 8787
EXPOSE 8786

ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
```

And build the image as:
```bash
docker build -t jupyter/scipy-dasklabextension:latest .
```

Once built, run using the command:
```bash
docker run -it --rm -p 8888:8888 -p 8787:8787 jupyter/scipy-dasklabextension:latest
```

Ref:
[https://github.com/jupyter/docker-stacks/issues/999](https://github.com/jupyter/docker-stacks/issues/999)

## Let's Encrypt a Notebook server

See the README for the simple automation here
[https://github.com/jupyter/docker-stacks/tree/master/examples/make-deploy](https://github.com/jupyter/docker-stacks/tree/master/examples/make-deploy)
which includes steps for requesting and renewing a Let's Encrypt certificate.

Ref:
[https://github.com/jupyter/docker-stacks/issues/78](https://github.com/jupyter/docker-stacks/issues/78)

## Slideshows with Jupyter and RISE

[RISE](https://github.com/damianavila/RISE) allows via extension to create live slideshows of your
notebooks, with no conversion, adding javascript Reveal.js:

```bash
# Add Live slideshows with RISE
RUN conda install -c damianavila82 rise
```

Credit: [Paolo D.](https://github.com/pdonorio) based on
[docker-stacks/issues/43](https://github.com/jupyter/docker-stacks/issues/43)

## xgboost

You need to install conda's gcc for Python xgboost to work properly. Otherwise, you'll get an
exception about libgomp.so.1 missing GOMP_4.0.

```bash
%%bash
conda install -y gcc
pip install xgboost

import xgboost
```

## Running behind a nginx proxy

Sometimes it is useful to run the Jupyter instance behind a nginx proxy, for instance:

- you would prefer to access the notebook at a server URL with a path
  (`https://example.com/jupyter`) rather than a port (`https://example.com:8888`)
- you may have many different services in addition to Jupyter running on the same server, and want
  to nginx to help improve server performance in manage the connections

Here is a [quick example NGINX configuration](https://gist.github.com/cboettig/8643341bd3c93b62b5c2)
to get started. You'll need a server, a `.crt` and `.key` file for your server, and `docker` &
`docker-compose` installed. Then just download the files at that gist and run `docker-compose up -d`
to test it out. Customize the `nginx.conf` file to set the desired paths and add other services.

## Host volume mounts and notebook errors

If you are mounting a host directory as `/home/jovyan/work` in your container and you receive
permission errors or connection errors when you create a notebook, be sure that the `jovyan` user
(UID=1000 by default) has read/write access to the directory on the host. Alternatively, specify the
UID of the `jovyan` user on container startup using the `-e NB_UID` option described in the
[Common Features, Docker Options section](../using/common.html#Docker-Options)

Ref:
[https://github.com/jupyter/docker-stacks/issues/199](https://github.com/jupyter/docker-stacks/issues/199)

## Manpage installation

Most containers, including our Ubuntu base image, ship without manpages installed to save space. You
can use the following dockerfile to inherit from one of our images to enable manpages:

```dockerfile
# Choose your desired base image
ARG BASE_CONTAINER=jupyter/datascience-notebook:latest
FROM $BASE_CONTAINER

USER root

# Remove the manpage blacklist, install man, install docs
RUN rm /etc/dpkg/dpkg.cfg.d/excludes \
    && apt-get update \
    && dpkg -l | grep ^ii | cut -d' ' -f3 | xargs apt-get install -yq --no-install-recommends --reinstall man \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID
```

Adding the documentation on top of an existing singleuser image wastes a lot of space and requires
reinstalling every system package, which can take additional time and bandwidth; the
`datascience-notebook` image has been shown to grow by almost 3GB when adding manapages in this way.
Enabling manpages in the base Ubuntu layer prevents this container bloat.
Just use previous `Dockerfile` with original ubuntu image as your base container:

```dockerfile
# Ubuntu 20.04 (focal) from 2020-04-23
# https://github.com/docker-library/official-images/commit/4475094895093bcc29055409494cce1e11b52f94
ARG BASE_CONTAINER=ubuntu:focal-20200423@sha256:238e696992ba9913d24cfc3727034985abd136e08ee3067982401acdc30cbf3f
```

For Ubuntu 18.04 (bionic) and earlier, you may also require to workaround for a mandb bug, which was fixed in mandb >= 2.8.6.1:
```dockerfile
# https://git.savannah.gnu.org/cgit/man-db.git/commit/?id=8197d7824f814c5d4b992b4c8730b5b0f7ec589a
# http://launchpadlibrarian.net/435841763/man-db_2.8.5-2_2.8.6-1.diff.gz

RUN echo "MANPATH_MAP ${CONDA_DIR}/bin ${CONDA_DIR}/man" >> /etc/manpath.config \
    && echo "MANPATH_MAP ${CONDA_DIR}/bin ${CONDA_DIR}/share/man" >> /etc/manpath.config \
    && mandb

```

Be sure to check the current base image in `base-notebook` before building.

## JupyterHub

We also have contributed recipes for using JupyterHub.

### Use JupyterHub's dockerspawner

In most cases for use with DockerSpawner, given any image that already has a notebook stack set up,
you would only need to add:

1. install the jupyterhub-singleuser script (for the right Python)
2. change the command to launch the single-user server

Swapping out the `FROM` line in the `jupyterhub/singleuser` Dockerfile should be enough for most
cases.

Credit: [Justin Tyberg](https://github.com/jtyberg), [quanghoc](https://github.com/quanghoc), and
[Min RK](https://github.com/minrk) based on
[docker-stacks/issues/124](https://github.com/jupyter/docker-stacks/issues/124) and
[docker-stacks/pull/185](https://github.com/jupyter/docker-stacks/pull/185)

### Containers with a specific version of JupyterHub

To use a specific version of JupyterHub, the version of `jupyterhub` in your image should match the
version in the Hub itself.

```dockerfile
FROM jupyter/base-notebook:5ded1de07260
RUN pip install jupyterhub==0.8.0b1
```

Credit: [MinRK](https://github.com/jupyter/docker-stacks/issues/423#issuecomment-322767742)

Ref:
[https://github.com/jupyter/docker-stacks/issues/177](https://github.com/jupyter/docker-stacks/issues/177)

## Spark

A few suggestions have been made regarding using Docker Stacks with spark.

### Using PySpark with AWS S3

Using Spark session for hadoop 2.7.3

```py
import os
# !ls /usr/local/spark/jars/hadoop* # to figure out what version of hadoop
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages "org.apache.hadoop:hadoop-aws:2.7.3" pyspark-shell'

import pyspark
myAccessKey = input()
mySecretKey = input()

spark = pyspark.sql.SparkSession.builder \
        .master("local[*]") \
        .config("spark.hadoop.fs.s3a.access.key", myAccessKey) \
        .config("spark.hadoop.fs.s3a.secret.key", mySecretKey) \
        .getOrCreate()

df = spark.read.parquet("s3://myBucket/myKey")
```

Using Spark context for hadoop 2.6.0

```py
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.amazonaws:aws-java-sdk:1.10.34,org.apache.hadoop:hadoop-aws:2.6.0 pyspark-shell'

import pyspark
sc = pyspark.SparkContext("local[*]")

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

hadoopConf = sc._jsc.hadoopConfiguration()
myAccessKey = input()
mySecretKey = input()
hadoopConf.set("fs.s3.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
hadoopConf.set("fs.s3.awsAccessKeyId", myAccessKey)
hadoopConf.set("fs.s3.awsSecretAccessKey", mySecretKey)

df = sqlContext.read.parquet("s3://myBucket/myKey")
```

Ref:
[https://github.com/jupyter/docker-stacks/issues/127](https://github.com/jupyter/docker-stacks/issues/127)

### Using Local Spark JARs

```python
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /home/jovyan/spark-streaming-kafka-assembly_2.10-1.6.1.jar pyspark-shell'
import pyspark
from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext
sc = pyspark.SparkContext()
ssc = StreamingContext(sc,1)
broker = "<my_broker_ip>"
directKafkaStream = KafkaUtils.createDirectStream(ssc, ["test1"], {"metadata.broker.list": broker})
directKafkaStream.pprint()
ssc.start()
```

Ref:
[https://github.com/jupyter/docker-stacks/issues/154](https://github.com/jupyter/docker-stacks/issues/154)

### Using spark-packages.org

If you'd like to use packages from [spark-packages.org](https://spark-packages.org/), see
[https://gist.github.com/parente/c95fdaba5a9a066efaab](https://gist.github.com/parente/c95fdaba5a9a066efaab)
for an example of how to specify the package identifier in the environment before creating a
SparkContext.

Ref:
[https://github.com/jupyter/docker-stacks/issues/43](https://github.com/jupyter/docker-stacks/issues/43)

### Use jupyter/all-spark-notebooks with an existing Spark/YARN cluster

```dockerfile
FROM jupyter/all-spark-notebook

# Set env vars for pydoop
ENV HADOOP_HOME /usr/local/hadoop-2.7.3
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_CONF_HOME /usr/local/hadoop-2.7.3/etc/hadoop
ENV HADOOP_CONF_DIR  /usr/local/hadoop-2.7.3/etc/hadoop

USER root
# Add proper open-jdk-8 not just the jre, needed for pydoop
RUN echo 'deb http://cdn-fastly.deb.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get -y update && \
    apt-get install --no-install-recommends -t jessie-backports -y openjdk-8-jdk && \
    rm /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
# Add hadoop binaries
    wget http://mirrors.ukfast.co.uk/sites/ftp.apache.org/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz && \
    tar -xvf hadoop-2.7.3.tar.gz -C /usr/local && \
    chown -R $NB_USER:users /usr/local/hadoop-2.7.3 && \
    rm -f hadoop-2.7.3.tar.gz && \
# Install os dependencies required for pydoop, pyhive
    apt-get update && \
    apt-get install --no-install-recommends -y build-essential python-dev libsasl2-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
# Remove the example hadoop configs and replace
# with those for our cluster.
# Alternatively this could be mounted as a volume
    rm -f /usr/local/hadoop-2.7.3/etc/hadoop/*

# Download this from ambari / cloudera manager and copy here
COPY example-hadoop-conf/ /usr/local/hadoop-2.7.3/etc/hadoop/

# Spark-Submit doesn't work unless I set the following
RUN echo "spark.driver.extraJavaOptions -Dhdp.version=2.5.3.0-37" >> /usr/local/spark/conf/spark-defaults.conf  && \
    echo "spark.yarn.am.extraJavaOptions -Dhdp.version=2.5.3.0-37" >> /usr/local/spark/conf/spark-defaults.conf && \
    echo "spark.master=yarn" >>  /usr/local/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.yarn.timeline-service.enabled=false" >> /usr/local/spark/conf/spark-defaults.conf && \
    chown -R $NB_USER:users /usr/local/spark/conf/spark-defaults.conf && \
    # Create an alternative HADOOP_CONF_HOME so we can mount as a volume and repoint
    # using ENV var if needed
    mkdir -p /etc/hadoop/conf/ && \
    chown $NB_USER:users /etc/hadoop/conf/

USER $NB_USER

# Install useful jupyter extensions and python libraries like :
# - Dashboards
# - PyDoop
# - PyHive
RUN pip install jupyter_dashboards faker && \
    jupyter dashboards quick-setup --sys-prefix && \
    pip2 install pyhive pydoop thrift sasl thrift_sasl faker

USER root
# Ensure we overwrite the kernel config so that toree connects to cluster
RUN jupyter toree install --sys-prefix --spark_opts="--master yarn --deploy-mode client --driver-memory 512m  --executor-memory 512m  --executor-cores 1 --driver-java-options -Dhdp.version=2.5.3.0-37 --conf spark.hadoop.yarn.timeline-service.enabled=false"
USER $NB_USER
```

Credit: [britishbadger](https://github.com/britishbadger) from
[docker-stacks/issues/369](https://github.com/jupyter/docker-stacks/issues/369)

## Run Jupyter Notebook/Lab inside an already secured environment (i.e., with no token)

(Adapted from [issue 728](https://github.com/jupyter/docker-stacks/issues/728))

The default security is very good. There are use cases, encouraged by containers, where the jupyter
container and the system it runs within, lie inside the security boundary. In these use cases it is
convenient to launch the server without a password or token. In this case, you should use the
`start.sh` script to launch the server with no token:

For jupyterlab:

```bash
docker run jupyter/base-notebook:6d2a05346196 start.sh jupyter lab --LabApp.token=''
```

For jupyter classic:

```bash
docker run jupyter/base-notebook:6d2a05346196 start.sh jupyter notebook --NotebookApp.token=''
```

## Enable nbextension spellchecker for markdown (or any other nbextension)

NB: this works for classic notebooks only

```dockerfile
# Update with your base image of choice
FROM jupyter/minimal-notebook:latest

USER $NB_USER

RUN pip install jupyter_contrib_nbextensions && \
    jupyter contrib nbextension install --user && \
    # can modify or enable additional extensions here
    jupyter nbextension enable spellchecker/main --user
```

Ref:
[https://github.com/jupyter/docker-stacks/issues/675](https://github.com/jupyter/docker-stacks/issues/675)

## Enable auto-sklearn notebooks

Using `auto-sklearn` requires `swig`, which the other notebook images lack, so it cant be experimented with. Also, there is no Conda package for `auto-sklearn`.

```dockerfile
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM jupyter/scipy-notebook:latest

USER root

# autosklearn requires swig, which no other image has
RUN apt-get update && \
    apt-get install -y --no-install-recommends swig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


USER $NB_UID

RUN pip install --quiet --no-cache-dir auto-sklearn
```

## Enable SensiML notebooks

Using `sensiml` requires `tensorflow`, and installs `qgrid` and `bqplot`. There is no conda package for `sensiml` at this time.

```dockerfile
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/tensorflow-notebook
FROM $BASE_CONTAINER

# Install SensiML and enable notebook extensions.
RUN pip install --quiet --no-cache-dir \
    'sensiml' && \
    jupyter nbextension enable --py widgetsnbextension --sys-prefix  && \
    jupyter nbextension enable --py --sys-prefix bqplot  && \
    jupyter nbextension enable --py --sys-prefix qgrid  && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

```
