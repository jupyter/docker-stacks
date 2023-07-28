# Contributed Recipes

Users sometimes share interesting ways of using the Jupyter Docker Stacks.
We encourage users to [contribute these recipes](../contributing/recipes.md) to the documentation in case they prove helpful to other community members by submitting a pull request to `docs/using/recipes.md`.
The sections below capture this knowledge.

## Using `sudo` within a container

Password authentication is disabled for the `NB_USER` (e.g., `jovyan`).
We made this choice to avoid distributing images with a weak default password that users ~might~ will forget to change before running a container on a publicly accessible host.

You can grant the within-container `NB_USER` passwordless `sudo` access by adding `--user root` and `-e GRANT_SUDO=yes` to your Docker command line or appropriate container orchestrator config.

For example:

```bash
docker run -it --rm \
    --user root \
    -e GRANT_SUDO=yes \
    jupyter/base-notebook
```

**You should only enable `sudo` if you trust the user and/or if the container is running on an isolated host.**
See [Docker security documentation](https://docs.docker.com/engine/security/userns-remap/) for more information about running containers as `root`.

## Using `mamba install` (recommended) or `pip install` in a Child Docker image

Create a new Dockerfile like the one shown below.
To use a requirements.txt file, first, create your `requirements.txt` file with the listing of packages desired.

```dockerfile
FROM jupyter/base-notebook

RUN mamba install --yes 'flake8' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Install from the requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN mamba install --yes --file /tmp/requirements.txt && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

`pip` usage is similar:

```dockerfile
FROM jupyter/base-notebook

# Install in the default python3 environment
RUN pip install --no-cache-dir 'flake8' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Install from the requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

Then build a new image.

```bash
docker build --rm -t my-custom-image .
```

## Add a custom conda environment and Jupyter kernel

The default version of Python that ships with the image may not be the version you want.
The instructions below permit adding a conda environment with a different Python version and making it accessible to Jupyter.

```dockerfile
FROM jupyter/minimal-notebook

# name your environment and choose the python version
ARG conda_env=python37
ARG py_ver=3.7

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
RUN mamba create --yes -p "${CONDA_DIR}/envs/${conda_env}" python=${py_ver} ipython ipykernel && \
    mamba clean --all -f -y

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml "/home/${NB_USER}/tmp/"
# RUN cd "/home/${NB_USER}/tmp/" && \
#     mamba env create -p "${CONDA_DIR}/envs/${conda_env}" -f environment.yml && \
#     mamba clean --all -f -y

# create Python kernel and link it to jupyter
RUN "${CONDA_DIR}/envs/${conda_env}/bin/python" -m ipykernel install --user --name="${conda_env}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# any additional pip installs can be added by uncommenting the following line
# RUN "${CONDA_DIR}/envs/${conda_env}/bin/pip" install --no-cache-dir

# if you want this environment to be the default one, uncomment the following line:
# RUN echo "conda activate ${conda_env}" >> "${HOME}/.bashrc"
```

## Dask JupyterLab Extension

[Dask JupyterLab Extension](https://github.com/dask/dask-labextension) provides a JupyterLab extension to manage Dask clusters, as well as embed Dask's dashboard plots directly into JupyterLab panes.
Create the Dockerfile as:

```dockerfile
FROM jupyter/base-notebook

# Install the Dask dashboard
RUN mamba install --yes 'dask-labextension' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Dask Scheduler port
EXPOSE 8787
```

And build the image as:

```bash
docker build --tag my-custom-image .
```

Once built, run using the command:

```bash
docker run -it --rm \
    -p 8888:8888 \
    -p 8787:8787 \
    my-custom-image
```

## Let's Encrypt a Server

See the README for a basic automation here
<https://github.com/jupyter/docker-stacks/tree/main/examples/make-deploy>
which includes steps for requesting and renewing a Let's Encrypt certificate.

Ref: <https://github.com/jupyter/docker-stacks/issues/78>

## Slideshows with JupyterLab and RISE

[RISE](https://github.com/jupyterlab-contrib/rise): "Live" Reveal.js JupyterLab Slideshow Extension.

```{note}
We're providing the recipe to install JupyterLab extension.
You can find the original Jupyter Notebook extenstion [here](https://github.com/damianavila/RISE)
```

```dockerfile
FROM jupyter/base-notebook

RUN mamba install --yes 'jupyterlab_rise' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

## xgboost

```dockerfile
FROM jupyter/base-notebook

RUN mamba install --yes 'py-xgboost' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# run "import xgboost" in python
```

## Running behind an nginx proxy

Sometimes it is helpful to run the Jupyter instance behind an nginx proxy, for example:

- you would prefer to access the notebook at a server URL with a path
  (`https://example.com/jupyter`) rather than a port (`https://example.com:8888`)
- you may have many services in addition to Jupyter running on the same server
  and want nginx to help improve server performance in managing the connections

Here is a [quick example of NGINX configuration](https://gist.github.com/cboettig/8643341bd3c93b62b5c2) to get started.
You'll need a server, a `.crt` and `.key` file for your server, and `docker` & `docker-compose` installed.
Then download the files at that gist and run `docker-compose up -d` to test it out.
Customize the `nginx.conf` file to set the desired paths and add other services.

## Host volume mounts and notebook errors

If you are mounting a host directory as `/home/jovyan/work` in your container,
and you receive permission errors or connection errors when you create a notebook,
be sure that the `jovyan` user (`UID=1000` by default) has read/write access to the directory on the host.
Alternatively, specify the UID of the `jovyan` user on container startup using the `-e NB_UID` option
described in the [Common Features, Docker Options section](common.md#docker-options)

Ref: <https://github.com/jupyter/docker-stacks/issues/199>

## Manpage installation

Most containers, including our Ubuntu base image, ship without manpages installed to save space.
You can use the following Dockerfile to inherit from one of our images to enable manpages:

```dockerfile
FROM jupyter/base-notebook

USER root

# `/etc/dpkg/dpkg.cfg.d/excludes` contains several `path-exclude`s, including man pages
# Remove it, then install man, install docs
RUN rm /etc/dpkg/dpkg.cfg.d/excludes && \
    apt-get update --yes && \
    dpkg -l | grep ^ii | cut -d' ' -f3 | xargs apt-get install --yes --no-install-recommends --reinstall man && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}
```

Adding the documentation on top of the existing image wastes a lot of space
and requires reinstalling every system package,
which can take additional time and bandwidth.
Enabling manpages in the base Ubuntu layer prevents this container bloat.
To achieve this, use the previous `Dockerfile`'s commands with the original `ubuntu` image as your base container:

```dockerfile
FROM ubuntu:22.04
```

Be sure to check the current base image in `jupyter/docker-stacks-foundation` before building.

## JupyterHub

We also have contributed recipes for using JupyterHub.

### Use JupyterHub's dockerspawner

In most cases for use with DockerSpawner, given an image that already has a notebook stack set up,
you would only need to add:

1. install the jupyterhub-singleuser script (for the correct Python version)
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
FROM jupyter/base-notebook

RUN pip install --no-cache-dir 'jupyterhub==1.4.1' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

Credit: [MinRK](https://github.com/jupyter/docker-stacks/issues/423#issuecomment-322767742)

Ref: <https://github.com/jupyter/docker-stacks/issues/177>

## Spark

A few suggestions have been made regarding using Docker Stacks with spark.

### Using PySpark with AWS S3

Using Spark session for Hadoop 2.7.3

```python
import os

# !ls /usr/local/spark/jars/hadoop* # to figure out what version of Hadoop
os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = '--packages "org.apache.hadoop:hadoop-aws:2.7.3" pyspark-shell'

import pyspark

myAccessKey = input()
mySecretKey = input()

spark = (
    pyspark.sql.SparkSession.builder.master("local[*]")
    .config("spark.hadoop.fs.s3a.access.key", myAccessKey)
    .config("spark.hadoop.fs.s3a.secret.key", mySecretKey)
    .getOrCreate()
)

df = spark.read.parquet("s3://myBucket/myKey")
```

Using Spark context for Hadoop 2.6.0

```python
import os

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages com.amazonaws:aws-java-sdk:1.10.34,org.apache.hadoop:hadoop-aws:2.6.0 pyspark-shell"

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

Ref: <https://github.com/jupyter/docker-stacks/issues/127>

### Using Local Spark JARs

```python
import os

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--jars /home/jovyan/spark-streaming-kafka-assembly_2.10-1.6.1.jar pyspark-shell"
import pyspark
from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext

sc = pyspark.SparkContext()
ssc = StreamingContext(sc, 1)
broker = "<my_broker_ip>"
directKafkaStream = KafkaUtils.createDirectStream(
    ssc, ["test1"], {"metadata.broker.list": broker}
)
directKafkaStream.pprint()
ssc.start()
```

Ref: <https://github.com/jupyter/docker-stacks/issues/154>

### Using spark-packages.org

If you'd like to use packages from [spark-packages.org](https://spark-packages.org/), see
[https://gist.github.com/parente/c95fdaba5a9a066efaab](https://gist.github.com/parente/c95fdaba5a9a066efaab)
for an example of how to specify the package identifier in the environment before creating a
SparkContext.

Ref: <https://github.com/jupyter/docker-stacks/issues/43>

### Use jupyter/all-spark-notebooks with an existing Spark/YARN cluster

```dockerfile
FROM jupyter/all-spark-notebook

# Set env vars for pydoop
ENV HADOOP_HOME /usr/local/hadoop-2.7.3
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_CONF_HOME /usr/local/hadoop-2.7.3/etc/hadoop
ENV HADOOP_CONF_DIR  /usr/local/hadoop-2.7.3/etc/hadoop

USER root
# Add proper open-jdk-8 not the jre only, needed for pydoop
RUN echo 'deb https://cdn-fastly.deb.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get update --yes && \
    apt-get install --yes --no-install-recommends -t jessie-backports openjdk-8-jdk && \
    rm /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
# Add Hadoop binaries
    wget --progress=dot:giga https://mirrors.ukfast.co.uk/sites/ftp.apache.org/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz && \
    tar -xvf hadoop-2.7.3.tar.gz -C /usr/local && \
    chown -R "${NB_USER}:users" /usr/local/hadoop-2.7.3 && \
    rm -f hadoop-2.7.3.tar.gz && \
# Install os dependencies required for pydoop, pyhive
    apt-get update --yes && \
    apt-get install --yes --no-install-recommends build-essential python-dev libsasl2-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
# Remove the example hadoop configs and replace
# with those for our cluster.
# Alternatively, this could be mounted as a volume
    rm -f /usr/local/hadoop-2.7.3/etc/hadoop/*

# Download this from ambari/cloudera manager and copy it here
COPY example-hadoop-conf/ /usr/local/hadoop-2.7.3/etc/hadoop/

# Spark-Submit doesn't work unless I set the following
RUN echo "spark.driver.extraJavaOptions -Dhdp.version=2.5.3.0-37" >> /usr/local/spark/conf/spark-defaults.conf  && \
    echo "spark.yarn.am.extraJavaOptions -Dhdp.version=2.5.3.0-37" >> /usr/local/spark/conf/spark-defaults.conf && \
    echo "spark.master=yarn" >>  /usr/local/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.yarn.timeline-service.enabled=false" >> /usr/local/spark/conf/spark-defaults.conf && \
    chown -R "${NB_USER}:users" /usr/local/spark/conf/spark-defaults.conf && \
    # Create an alternative HADOOP_CONF_HOME so we can mount as a volume and repoint
    # using ENV var if needed
    mkdir -p /etc/hadoop/conf/ && \
    chown "${NB_USER}":users /etc/hadoop/conf/

USER ${NB_UID}

# Install useful jupyter extensions and python libraries like :
# - Dashboards
# - PyDoop
# - PyHive
RUN pip install --no-cache-dir 'jupyter_dashboards' 'faker' && \
    jupyter dashboards quick-setup --sys-prefix && \
    pip2 install --no-cache-dir 'pyhive' 'pydoop' 'thrift' 'sasl' 'thrift_sasl' 'faker' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

USER root
# Ensure we overwrite the kernel config so that toree connects to cluster
RUN jupyter toree install --sys-prefix --spark_opts="\
    --master yarn \
    --deploy-mode client \
    --driver-memory 512m \
    --executor-memory 512m \
    --executor-cores 1 \
    --driver-java-options \
    -Dhdp.version=2.5.3.0-37 \
    --conf spark.hadoop.yarn.timeline-service.enabled=false \
"
USER ${NB_UID}
```

Credit: [britishbadger](https://github.com/britishbadger) from [docker-stacks/issues/369](https://github.com/jupyter/docker-stacks/issues/369)

## Run Server inside an already secured environment (i.e., with no token)

(Adapted from [issue 728](https://github.com/jupyter/docker-stacks/issues/728))

The default security is very good.
There are use cases, encouraged by containers, where the jupyter container and the system it runs within lie inside the security boundary.
It is convenient to launch the server without a password or token in these use cases.
In this case, you should use the `start-notebook.sh` script to launch the server with no token:

For JupyterLab:

```bash
docker run -it --rm \
    jupyter/base-notebook \
    start-notebook.sh --IdentityProvider.token=''
```

For Jupyter Notebook:

```bash
docker run -it --rm \
    -e DOCKER_STACKS_JUPYTER_CMD=notebook \
    jupyter/base-notebook \
    start-notebook.sh --IdentityProvider.token=''
```

## Enable nbclassic-extension spellchecker for markdown (or any other nbclassic-extension)

NB: this works for classic notebooks only

```dockerfile
FROM jupyter/minimal-notebook

USER ${NB_UID}

RUN pip install --no-cache-dir 'jupyter_contrib_nbextensions' && \
    jupyter contrib nbextension install --user && \
    # can modify or enable additional extensions here
    jupyter nbclassic-extension enable spellchecker/main --user && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

Ref: <https://github.com/jupyter/docker-stacks/issues/675>

## Enable Delta Lake in Spark notebooks

Please note that the [Delta Lake](https://delta.io/) packages are only available for Spark version > `3.0`.
By adding the properties to `spark-defaults.conf`, the user no longer needs to enable Delta support in each notebook.

```dockerfile
FROM jupyter/pyspark-notebook

ARG DELTA_CORE_VERSION="1.2.1"
RUN pip install --no-cache-dir 'delta-spark==${DELTA_CORE_VERSION}' && \
     fix-permissions "${HOME}" && \
     fix-permissions "${CONDA_DIR}"

USER root

RUN echo 'spark.sql.extensions io.delta.sql.DeltaSparkSessionExtension' >> "${SPARK_HOME}/conf/spark-defaults.conf" && \
    echo 'spark.sql.catalog.spark_catalog org.apache.spark.sql.delta.catalog.DeltaCatalog' >> "${SPARK_HOME}/conf/spark-defaults.conf"

USER ${NB_UID}

# Trigger download of delta lake files
RUN echo "from pyspark.sql import SparkSession" > /tmp/init-delta.py && \
    echo "from delta import *" >> /tmp/init-delta.py && \
    echo "spark = configure_spark_with_delta_pip(SparkSession.builder).getOrCreate()" >> /tmp/init-delta.py && \
    python /tmp/init-delta.py && \
    rm /tmp/init-delta.py
```

## Add Custom Fonts in Scipy notebook

The example below is a Dockerfile to load Source Han Sans with normal weight, usually used for the web.

```dockerfile
FROM jupyter/scipy-notebook

RUN PYV=$(ls "${CONDA_DIR}/lib" | grep ^python) && \
    MPL_DATA="${CONDA_DIR}/lib/${PYV}/site-packages/matplotlib/mpl-data" && \
    wget --progress=dot:giga -P "${MPL_DATA}/fonts/ttf/" https://mirrors.cloud.tencent.com/adobe-fonts/source-han-sans/SubsetOTF/CN/SourceHanSansCN-Normal.otf && \
    sed -i 's/#font.family/font.family/g' "${MPL_DATA}/matplotlibrc" && \
    sed -i 's/#font.sans-serif:/font.sans-serif: Source Han Sans CN,/g' "${MPL_DATA}/matplotlibrc" && \
    sed -i 's/#axes.unicode_minus: True/axes.unicode_minus: False/g' "${MPL_DATA}/matplotlibrc" && \
    rm -rf "/home/${NB_USER}/.cache/matplotlib" && \
    python -c 'import matplotlib.font_manager;print("font loaded: ",("Source Han Sans CN" in [f.name for f in matplotlib.font_manager.fontManager.ttflist]))'
```

## Enable clipboard in pandas on Linux systems

```{admonition} Additional notes
    This solution works on Linux host systems.
    It is not required on Windows and won't work on macOS.
```

To enable the `pandas.read_clipboard()` functionality, you need to have `xclip` installed
(installed in `minimal-notebook` and all the inherited images)
and add these options when running `docker`: `-e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix`, i.e.:

```bash
docker run -it --rm \
    -e DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    jupyter/minimal-notebook
```

## Add ijavascript kernel to container

The example below is a Dockerfile to install the [ijavascript kernel](https://github.com/n-riesco/ijavascript).

```dockerfile
FROM jupyter/scipy-notebook

# install ijavascript
RUN npm install -g ijavascript
RUN ijsinstall
```

## Add Microsoft SQL Server ODBC driver

The following recipe demonstrates how to add functionality to read from and write to an instance of Microsoft SQL server in your notebook.

```dockerfile
FROM jupyter/base-notebook

USER root

ENV MSSQL_DRIVER "ODBC Driver 18 for SQL Server"
ENV PATH="/opt/mssql-tools18/bin:${PATH}"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends curl gnupg2 lsb-release && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update --yes && \
    ACCEPT_EULA=Y apt-get install --yes --no-install-recommends msodbcsql18 && \
    # optional: for bcp and sqlcmd
    ACCEPT_EULA=Y apt-get install --yes --no-install-recommends mssql-tools18 && \
    # optional: for unixODBC development headers
    apt-get install -y unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

RUN mamba install --yes \
    'pyodbc' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

You can now use `pyodbc` and `sqlalchemy` to interact with the database.

Pre-built images are hosted in the [realiserad/jupyter-docker-mssql](https://github.com/Realiserad/jupyter-docker-mssql) repository.
