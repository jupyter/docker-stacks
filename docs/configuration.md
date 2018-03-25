# Options and Configuration

When launched as Docker containers, all of the Jupyter Docker Stacks start a Jupyter Notebook server by default. They do so by executing a `start-notebook.sh` script which configures the internal container environment and then runs `jupyter notebook $*`, passing it any command line arguments received.

This page describes the options supported by the startup script as well as how to bypass it to run alternative commands.

## Notebook Options

You can pass [Jupyter command line options](https://jupyter.readthedocs.io/en/latest/projects/jupyter-command.html) to the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a custom password hashed using `IPython.lib.passwd()` instead of the default token, you can run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, you can run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

For example, to ignore best practice and disable all authentication, you can run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.token=''
```

## Docker Options

You may instruct the `start-notebook.sh` script to customize the container environment before launching
the notebook server. You do so by passing arguments to the `docker run` command.

* `-e NB_USER=jovyan` - Instructs the startup script to change the default container username from `jovyan` to the provided value. Causes the script to rename the `jovyan` user home folder.
* `-e NB_UID=1000` - Instructs the startup script to switch the numeric user ID of `$NB_USER` to the given value. This feature is useful when mounting host volumes with specific owner permissions. For this option to take effect, you must run the container with `--user root`. (The startup script will `su $NB_USER` after adjusting the  user ID.)
* `-e NB_GID=100` - Instructs the startup script to change the numeric group ID of the `$NB_USER` to the given value. This feature is useful when mounting host volumes with specific group permissions. For this option to take effect, you must run the container with `--user root`. (The startup script will `su $NB_USER` after adjusting the group ID.)
* `-e CHOWN_HOME=yes` - Instructs the startup script to recursively change the `$NB_USER` home directory owner and group to the current value of `$NB_UID` and `$NB_GID`. This change will take effect even if the user home directory is mounted from the host using `-v` as described below.
* `-e GRANT_SUDO=yes` - Instructs the startup script to grant the `NB_USER` user passwordless `sudo` capability. You do **not** need too this option to allow the user to `conda` or `pip` install additional packages. This option is useful, however, when you wish to give `$NB_USER` the ability to install OS packages with `apt` or modify other root-owned files in the container. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su $NB_USER` after adding `$NB_USER` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-e GEN_CERT=yes` - Instructs the startup script to generates a self-signed SSL certificate and configure Jupyter Notebook to use it to accept encrypted HTTPS connections.
* `-v /some/host/folder/for/work:/home/jovyan/work` - Mounts a host machine directory as folder in the container. Useful when you want to preserve notebooks and other work even after the container is destroyed. **You must grant the within-container notebook user or group (`NB_UID` or `NB_GID`) write access to the host directory (e.g., `sudo chown 1000 /some/host/folder/for/work`).**
* `-user 5000 --group-add users` - Launches the container with a specific user ID and adds that user to the `users` group so that it can modify files in the default home directory and `/opt/conda`. You can use these arguments as alternatives to setting `$NB_UID` and `$NB_GID`.

## SSL Certificates

You may mount SSL key and certificate files into a container and configure Jupyter Notebook to use them to accept HTTPS connections. For example, to mount a host folder containing a `notebook.key` and `notebook.crt` and use them, you might run the following:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder:/etc/ssl/notebook \
    jupyter/base-notebook start-notebook.sh \
    --NotebookApp.keyfile=/etc/ssl/notebook/notebook.key
    --NotebookApp.certfile=/etc/ssl/notebook/notebook.crt
```

Alternatively, you may mount a single PEM file containing both the key and certificate. For example:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder/notebook.pem:/etc/ssl/notebook.pem \
    jupyter/base-notebook start-notebook.sh \
    --NotebookApp.certfile=/etc/ssl/notebook.pem
```

In either case, Jupyter Notebook expects the key and certificate to be a base64 encoded text file. The certificate file or PEM may contain one or more certificates (e.g., server, intermediate, and root).

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#securing-a-notebook-server) for best practices about securing a public notebook server in general.

## Alternative Commands

### start.sh

The `start-notebook.sh` script actually inherits most of its option handling capability from a more generic `start.sh` script. The `start.sh` script supports all of the features described above, but allows you to specify an arbitrary command to execute. For example, to run the text-based `ipython` console in a container, do the following:

```
docker run -it --rm jupyter/base-notebook start.sh ipython
```

Or, to run JupyterLab instead of the classic notebook, run the following:

```
docker run -it --rm -p 8888:8888 jupyter/base-notebook start.sh jupyter lab
```

This script is particularly useful when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, etc.

### Others

You can bypass the provided scripts and specify your an arbitrary start command. If you do, keep in mind that features supported by the `start.sh` script and its kin will not function (e.g., `GRANT_SUDO`).

## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. The `/opt/conda/bin` directory is part of the default `jovyan` user's `$PATH`. That directory is also whitelisted for use in `sudo` commands by the `start.sh` script.

The `jovyan` user has full read/write access to the `/opt/conda` directory. You can use either `conda` or `pip` to install new packages without any additional permissions.

```
# install a package into the default (python 3.x) environment
pip install some-package
conda install some-package
```

## Apache Spark

The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images support the use of Apache Spark in Python, R, and Scala notebooks. The following sections provide some examples of how to get started using them.

### Using Spark Local Mode

Spark local mode is useful for experimentation on small data when you do not have a Spark cluster available.

#### In a Python Notebook

```python
import pyspark
sc = pyspark.SparkContext('local[*]')

# do something to prove it works
rdd = sc.parallelize(range(1000))
rdd.takeSample(False, 5)
```

#### In a R Notebook

```r
library(SparkR)

as <- sparkR.session("local[*]")

# do something to prove it works
df <- as.DataFrame(iris)
head(filter(df, df$Petal_Width > 0.2))
```

#### In a Spylon Kernel Scala Notebook

Spylon kernel instantiates a `SparkContext` for you in variable `sc` after you configure Spark options in a `%%init_spark` magic cell.

```python
%%init_spark
# Configure Spark to use a local master
launcher.master = "local[*]"
```

```scala
// Now run Scala code that uses the initialized SparkContext in sc
val rdd = sc.parallelize(0 to 999)
rdd.takeSample(false, 5)
```

#### In an Apache Toree Scala Notebook

Apache Toree instantiates a local `SparkContext` for you in variable `sc` when the kernel starts.

```scala
val rdd = sc.parallelize(0 to 999)
rdd.takeSample(false, 5)
```

### Connecting to a Spark Cluster on Mesos

This configuration allows your compute cluster to scale with your data.

0. [Deploy Spark on Mesos](http://spark.apache.org/docs/latest/running-on-mesos.html).
1. Configure each slave with [the `--no-switch_user` flag](https://open.mesosphere.com/reference/mesos-slave/) or create the `$NB_USER` account on every slave node.
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. Follow the language specific instructions below.

#### In a Python Notebook

```python
import os
# make sure pyspark tells workers to use python3 not 2 if both are installed
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'

import pyspark
conf = pyspark.SparkConf()

# point to mesos master or zookeeper entry (e.g., zk://10.10.10.10:2181/mesos)
conf.setMaster("mesos://10.10.10.10:5050")
# point to spark binary package in HDFS or on local filesystem on all slave
# nodes (e.g., file:///opt/spark/spark-2.2.0-bin-hadoop2.7.tgz)
conf.set("spark.executor.uri", "hdfs://10.10.10.10/spark/spark-2.2.0-bin-hadoop2.7.tgz")
# set other options as desired
conf.set("spark.executor.memory", "8g")
conf.set("spark.core.connection.ack.wait.timeout", "1200")

# create the context
sc = pyspark.SparkContext(conf=conf)

# do something to prove it works
rdd = sc.parallelize(range(100000000))
rdd.sumApprox(3)
```

#### In a R Notebook

```r
library(SparkR)

# Point to mesos master or zookeeper entry (e.g., zk://10.10.10.10:2181/mesos)
# Point to spark binary package in HDFS or on local filesystem on all slave
# nodes (e.g., file:///opt/spark/spark-2.2.0-bin-hadoop2.7.tgz) in sparkEnvir
# Set other options in sparkEnvir
sc <- sparkR.session("mesos://10.10.10.10:5050", sparkEnvir=list(
    spark.executor.uri="hdfs://10.10.10.10/spark/spark-2.2.0-bin-hadoop2.7.tgz",
    spark.executor.memory="8g"
    )
)

# do something to prove it works
data(iris)
df <- as.DataFrame(iris)
head(filter(df, df$Petal_Width > 0.2))
```

#### In a Spylon Kernel Scala Notebook

```python
%%init_spark
# Configure the location of the mesos master and spark distribution on HDFS
launcher.master = "mesos://10.10.10.10:5050"
launcher.conf.spark.executor.uri=hdfs://10.10.10.10/spark/spark-2.2.0-bin-hadoop2.7.tgz
```

```scala
// Now run Scala code that uses the initialized SparkContext in sc
val rdd = sc.parallelize(0 to 999)
rdd.takeSample(false, 5)
```

#### In an Apache Toree Scala Notebook

The Apache Toree kernel automatically creates a `SparkContext` when it starts based on configuration information from its command line arguments and environment variables. You can pass information about your Mesos cluster via the `SPARK_OPTS` environment variable when you spawn a container.

For instance, to pass information about a Mesos master, Spark binary location in HDFS, and an executor options, you could start the container like so:

```
docker run -d -p 8888:8888 -e SPARK_OPTS='--master=mesos://10.10.10.10:5050 \
    --spark.executor.uri=hdfs://10.10.10.10/spark/spark-2.2.0-bin-hadoop2.7.tgz \
    --spark.executor.memory=8g' jupyter/all-spark-notebook
```

Note that this is the same information expressed in a notebook in the Python case above. Once the kernel spec has your cluster information, you can test your cluster in an Apache Toree notebook like so:

```scala
// should print the value of --master in the kernel spec
println(sc.master)

// do something to prove it works
val rdd = sc.parallelize(0 to 99999999)
rdd.sum()
```

### Connecting to a Spark Cluster on Standalone Mode

Connection to Spark Cluster on Standalone Mode requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster which is being deployed, run the same version of Spark.
1. [Deploy Spark on Standalone Mode](http://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. The language specific instructions are almost same as mentioned above for Mesos, only the master url would now be something like spark://10.10.10.10:7077