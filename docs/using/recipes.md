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
    quay.io/jupyter/base-notebook
```

**You should only enable `sudo` if you trust the user and/or if the container is running on an isolated host.**
See [Docker security documentation](https://docs.docker.com/engine/security/userns-remap/) for more information about running containers as `root`.

## Using `mamba install` (recommended) or `pip install` in a Child Docker image

Create a new Dockerfile like the one shown below.
To use a requirements.txt file, first, create your `requirements.txt` file with the listing of packages desired.

```{literalinclude} recipe_code/mamba_install.dockerfile
:language: docker
```

`pip` usage is similar:

```{literalinclude} recipe_code/pip_install.dockerfile
:language: docker
```

Then build a new image.

```bash
docker build --rm --tag my-custom-image .
```

You can then run the image as follows:

```bash
docker run -it --rm \
    -p 8888:8888 \
    my-custom-image
```

## Add a custom conda environment and Jupyter kernel

The default version of `Python` that ships with the image may not be the version you want.
The instructions below permit adding a conda environment with a different `Python` version and making it accessible to Jupyter.
You may also use older image like `jupyter/base-notebook:python-3.10`.
List of all tags can be found [here](https://github.com/jupyter/docker-stacks/wiki)

```{literalinclude} recipe_code/custom_environment.dockerfile
:language: docker
```

## Dask JupyterLab Extension

[Dask JupyterLab Extension](https://github.com/dask/dask-labextension) provides a JupyterLab extension to manage Dask clusters, as well as embed Dask's dashboard plots directly into JupyterLab panes.
Create the Dockerfile as:

```{literalinclude} recipe_code/dask_jupyterlab.dockerfile
:language: docker
```

And build the image as:

```bash
docker build --rm --tag my-custom-image .
```

Once built, run using the command:

```bash
docker run -it --rm \
    -p 8888:8888 \
    -p 8787:8787 \
    my-custom-image
```

## Let's Encrypt a Server

```{warning}
This recipe is not tested and might be broken.
```

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

```{literalinclude} recipe_code/rise_jupyterlab.dockerfile
:language: docker
```

## xgboost

```{literalinclude} recipe_code/xgboost.dockerfile
:language: docker
```

## Running behind an nginx proxy

```{warning}
This recipe is not tested and might be broken.
```

Sometimes it is helpful to run the Jupyter instance behind an nginx proxy, for example:

- you would prefer to access the notebook at a server URL with a path
  (`https://example.com/jupyter`) rather than a port (`https://example.com:8888`)
- you may have many services in addition to Jupyter running on the same server
  and want nginx to help improve server performance in managing the connections

Here is a [quick example of NGINX configuration](https://gist.github.com/cboettig/8643341bd3c93b62b5c2) to get started.
You'll need a server, a `.crt` and `.key` file for your server, and `docker` & `docker-compose` installed.
Then download the files at that gist and run `docker-compose up` to test it out.
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

```{literalinclude} recipe_code/manpage_install.dockerfile
:language: docker
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

### Use JupyterHub's DockerSpawner

You can find an example of using DockerSpawner [here](https://github.com/jupyterhub/jupyterhub-deploy-docker/tree/main/basic-example).

### Containers with a specific version of JupyterHub

The version of `jupyterhub` in your image should match the
version in the JupyterHub itself.
To use a specific version of JupyterHub, do the following:

```{literalinclude} recipe_code/jupyterhub_version.dockerfile
:language: docker
```

## Spark

A few suggestions have been made regarding using Docker Stacks with spark.

### Using PySpark with AWS S3

```{warning}
This recipe is not tested and might be broken.
```

Using Spark session for Hadoop 2.7.3

```python
import os

# To figure out what version of Hadoop, run:
# ls /usr/local/spark/jars/hadoop*
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

```{warning}
This recipe is not tested and might be broken.
```

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

```{warning}
This recipe is not tested and might be broken.
```

If you'd like to use packages from [spark-packages.org](https://spark-packages.org/), see
[https://gist.github.com/parente/c95fdaba5a9a066efaab](https://gist.github.com/parente/c95fdaba5a9a066efaab)
for an example of how to specify the package identifier in the environment before creating a
SparkContext.

Ref: <https://github.com/jupyter/docker-stacks/issues/43>

### Use jupyter/all-spark-notebooks with an existing Spark/YARN cluster

```{warning}
This recipe is not tested and might be broken.
```

```dockerfile
FROM quay.io/jupyter/all-spark-notebook

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

The default security is very good.
There are use cases, encouraged by containers, where the jupyter container and the system it runs within lie inside the security boundary.
It is convenient to launch the server without a password or token in these use cases.
In this case, you should use the `start-notebook.py` script to launch the server with no token:

For JupyterLab:

```bash
docker run -it --rm \
    quay.io/jupyter/base-notebook \
    start-notebook.py --IdentityProvider.token=''
```

For Jupyter Notebook:

```bash
docker run -it --rm \
    -e DOCKER_STACKS_JUPYTER_CMD=notebook \
    quay.io/jupyter/base-notebook \
    start-notebook.py --IdentityProvider.token=''
```

## Enable nbclassic-extension spellchecker for markdown (or any other nbclassic-extension)

```{note}
This recipe only works for NBCassic with Jupyter Notebook < 7.
It is recommended to use [jupyterlab-spellchecker](https://github.com/jupyterlab-contrib/spellchecker) in modern environments.
```

```{literalinclude} recipe_code/spellcheck_notebookv6.dockerfile
:language: docker
```

## Enable Delta Lake in Spark notebooks

```{warning}
This recipe is not tested and might be broken.
```

Please note that the [Delta Lake](https://delta.io/) packages are only available for Spark version > `3.0`.
By adding the properties to `spark-defaults.conf`, the user no longer needs to enable Delta support in each notebook.

```dockerfile
FROM quay.io/jupyter/pyspark-notebook

RUN mamba install --yes 'delta-spark' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

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

```{warning}
This recipe is not tested and might be broken.
```

The example below is a Dockerfile to load Source Han Sans with normal weight, usually used for the web.

```dockerfile
FROM quay.io/jupyter/scipy-notebook

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

```{warning}
This recipe is not tested and might be broken.
```

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
    quay.io/jupyter/minimal-notebook
```

## Add ijavascript kernel to container

```{warning}
This recipe is not tested and might be broken.
```

The example below is a Dockerfile to install the [ijavascript kernel](https://github.com/n-riesco/ijavascript).

```dockerfile
FROM quay.io/jupyter/scipy-notebook

# install ijavascript
RUN npm install -g ijavascript
RUN ijsinstall
```

## Add Microsoft SQL Server ODBC driver

The following recipe demonstrates how to add functionality to read from and write to an instance of Microsoft SQL server in your notebook.

```{literalinclude} recipe_code/microsoft_odbc.dockerfile
:language: docker
```

You can now use `pyodbc` and `sqlalchemy` to interact with the database.

Pre-built images are hosted in the [realiserad/jupyter-docker-mssql](https://github.com/Realiserad/jupyter-docker-mssql) repository.

## Add Oracle SQL Instant client, SQL\*Plus and other tools (Version 21.x)

```{note}
This recipe only works for x86_64 architecture.
```

The following recipe demonstrates how to add functionality to connect to a Oracle Database using [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client.html)
in your notebook.
This recipe installs version `21.11.0.0.0`.

Nonetheless, go to the [Oracle Instant Client Download page](https://www.oracle.com/es/database/technologies/instant-client/linux-x86-64-downloads.html) for the complete list of versions available.
You may need to perform different steps for older versions;
the may be explained on the "Installation instructions" section of the Downloads page.

```{literalinclude} recipe_code/oracledb.dockerfile
:language: docker
```
