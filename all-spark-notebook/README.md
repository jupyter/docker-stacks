![docker pulls](https://img.shields.io/docker/pulls/jupyter/all-spark-notebook.svg) ![docker stars](https://img.shields.io/docker/stars/jupyter/all-spark-notebook.svg) [![](https://images.microbadger.com/badges/image/jupyter/all-spark-notebook.svg)](https://microbadger.com/images/jupyter/all-spark-notebook "jupyter/all-spark-notebook image metadata")


# Jupyter Notebook Python, Scala, R, Spark, Mesos Stack

## What it Gives You

* Jupyter Notebook 4.3.x
* Conda Python 3.x environment
* Conda R 3.3.x environment
* Scala 2.11.x
* pyspark, pandas, matplotlib, scipy, seaborn, scikit-learn pre-installed for Python
* ggplot2, rcurl preinstalled for R
* Spark 2.2.0 with Hadoop 2.7 for use in local mode or to connect to a cluster of Spark workers
* Mesos client 1.2 binary that can communicate with a Mesos master
* spylon-kernel
* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan` and `/opt/conda`
* [tini](https://github.com/krallin/tini) as the container entrypoint and [start-notebook.sh](../base-notebook/start-notebook.sh) as the default command
* A [start-singleuser.sh](../base-notebook/start-singleuser.sh) script useful for running a single-user instance of the Notebook server, as required by JupyterHub
* A [start.sh](../base-notebook/start.sh) script useful for running alternative commands in the container (e.g. `ipython`, `jupyter kernelgateway`, `jupyter lab`)
* Options for a self-signed HTTPS certificate and passwordless `sudo`

## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 with a randomly generated authentication token configured.

```
docker run -it --rm -p 8888:8888 jupyter/all-spark-notebook
```

Take note of the authentication token included in the notebook startup log messages. Include it in the URL you visit to access the Notebook server or enter it in the Notebook login form.

## Using Spark Local Mode

This configuration is nice for using Spark on small, local data.

### In a Python Notebook

0. Run the container as shown above.
1. Open a Python 2 or 3 notebook.
2. Create a `SparkContext` configured for local mode.

For example, the first few cells in a notebook might read:

```python
import pyspark
sc = pyspark.SparkContext('local[*]')

# do something to prove it works
rdd = sc.parallelize(range(1000))
rdd.takeSample(False, 5)
```

### In a R Notebook

0. Run the container as shown above.
1. Open a R notebook.
2. Initialize a `sparkR` session for local mode.

For example, the first few cells in a R notebook might read:

```
library(SparkR)

as <- sparkR.session("local[*]")

# do something to prove it works
df <- as.DataFrame(iris)
head(filter(df, df$Petal_Width > 0.2))
```

### In an Apache Toree - Scala Notebook

0. Run the container as shown above.
1. Open an Apache Toree - Scala notebook.
2. Use the pre-configured `SparkContext` in variable `sc`.

For example:

```
val rdd = sc.parallelize(0 to 999)
rdd.takeSample(false, 5)
```

### In spylon-kernel - Scala Notebook

0. Run the container as shown above.
1. Open a spylon-kernel notebook
2. Lazily instantiate the sparkcontext by just running any cell without magics

For example

```
val rdd = sc.parallelize(0 to 999)
rdd.takeSample(false, 5)
```

## Connecting to a Spark Cluster on Mesos

This configuration allows your compute cluster to scale with your data.

0. [Deploy Spark on Mesos](http://spark.apache.org/docs/latest/running-on-mesos.html).
1. Configure each slave with [the `--no-switch_user` flag](https://open.mesosphere.com/reference/mesos-slave/) or create the `jovyan` user on every slave node.
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. Follow the language specific instructions below.

### In a Python Notebook

0. Open a Python 2 or 3 notebook.
1. Create a `SparkConf` instance in a new notebook pointing to your Mesos master node (or Zookeeper instance) and Spark binary package location.
2. Create a `SparkContext` using this configuration.

For example, the first few cells in a Python 3 notebook might read:

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

To use Python 2 in the notebook and on the workers, change the `PYSPARK_PYTHON` environment variable to point to the location of the Python 2.x interpreter binary. If you leave this environment variable unset, it defaults to `python`.

Of course, all of this can be hidden in an [IPython kernel startup script](http://ipython.org/ipython-doc/stable/development/config.html?highlight=startup#startup-files), but "explicit is better than implicit." :)

### In a R Notebook

0. Run the container as shown above.
1. Open a R notebook.
2. Initialize `sparkR` Mesos master node (or Zookeeper instance) and Spark binary package location.
3. Initialize `sparkRSQL`.

For example, the first few cells in a R notebook might read:

```
library(SparkR)

# point to mesos master or zookeeper entry (e.g., zk://10.10.10.10:2181/mesos)\
# as the first argument
# point to spark binary package in HDFS or on local filesystem on all slave
# nodes (e.g., file:///opt/spark/spark-2.2.0-bin-hadoop2.7.tgz) in sparkEnvir
# set other options in sparkEnvir
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

### In an Apache Toree - Scala Notebook

0. Open a terminal via *New -> Terminal* in the notebook interface.
1. Add information about your cluster to the `SPARK_OPTS` environment variable when running the container.
2. Open an Apache Toree - Scala notebook.
3. Use the pre-configured `SparkContext` in variable `sc` or `SparkSession` in variable `spark`.

The Apache Toree kernel automatically creates a `SparkContext` when it starts based on configuration information from its command line arguments and environment variables. You can pass information about your Mesos cluster via the `SPARK_OPTS` environment variable when you spawn a container.

For instance, to pass information about a Mesos master, Spark binary location in HDFS, and an executor options, you could start the container like so:

`docker run -d -p 8888:8888 -e SPARK_OPTS '--master=mesos://10.10.10.10:5050 \
    --spark.executor.uri=hdfs://10.10.10.10/spark/spark-2.2.0-bin-hadoop2.7.tgz \
    --spark.executor.memory=8g' jupyter/all-spark-notebook`

Note that this is the same information expressed in a notebook in the Python case above. Once the kernel spec has your cluster information, you can test your cluster in an Apache Toree notebook like so:

```
// should print the value of --master in the kernel spec
println(sc.master)

// do something to prove it works
val rdd = sc.parallelize(0 to 99999999)
rdd.sum()
```
## Connecting to a Spark Cluster on Standalone Mode

Connection to Spark Cluster on Standalone Mode requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster which is being deployed, run the same version of Spark.
1. [Deploy Spark on Standalone Mode](http://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. The language specific instructions are almost same as mentioned above for Mesos, only the master url would now be something like spark://10.10.10.10:7077

## Notebook Options

The Docker container executes a [`start-notebook.sh` script](../base-notebook/start-notebook.sh) script by default. The `start-notebook.sh` script handles the `NB_UID`, `NB_GID` and `GRANT_SUDO` features documented in the next section, and then executes the `jupyter notebook`.

You can pass [Jupyter command line options](https://jupyter.readthedocs.io/en/latest/projects/jupyter-command.html) through the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a custom password hashed ([how-to](http://jupyter-notebook.readthedocs.io/en/latest/public_server.html#preparing-a-hashed-password)) instead of the default token, run the following:

```
docker run -d -p 8888:8888 jupyter/all-spark-notebook start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, run the following:

```
docker run -d -p 8888:8888 jupyter/all-spark-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

For example, to disable all authentication mechanisms (not a recommended practice):

```
docker run -d -p 8888:8888 jupyter/all-spark-notebook start-notebook.sh --NotebookApp.token=''
```

You can sidestep the `start-notebook.sh` script and run your own commands in the container. See the *Alternative Commands* section later in this document for more information.

## Docker Options

You may customize the execution of the Docker container and the command it is running with the following optional arguments.

* `-e GEN_CERT=yes` - Generates a self-signed SSL certificate and configures Jupyter Notebook to use it to accept encrypted HTTPS connections.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the user id.)
* `-e NB_GID=100` - Specify the gid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the group id.)
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adding `jovyan` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Mounts a host machine directory as folder in the container. Useful when you want to preserve notebooks and other work even after the container is destroyed. **You must grant the within-container notebook user or group (`NB_UID` or `NB_GID`) write access to the host directory (e.g., `sudo chown 1000 /some/host/folder/for/work`).**

## SSL Certificates

You may mount SSL key and certificate files into a container and configure Jupyter Notebook to use them to accept HTTPS connections. For example, to mount a host folder containing a `notebook.key` and `notebook.crt`:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder:/etc/ssl/notebook \
    jupyter/all-spark-notebook start-notebook.sh \
    --NotebookApp.keyfile=/etc/ssl/notebook/notebook.key
    --NotebookApp.certfile=/etc/ssl/notebook/notebook.crt
```

Alternatively, you may mount a single PEM file containing both the key and certificate. For example:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder/notebook.pem:/etc/ssl/notebook.pem \
    jupyter/all-spark-notebook start-notebook.sh \
    --NotebookApp.certfile=/etc/ssl/notebook.pem
```

In either case, Jupyter Notebook expects the key and certificate to be a base64 encoded text file. The certificate file or PEM may contain one or more certificates (e.g., server, intermediate, and root).

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#using-ssl-for-encrypted-communication) for best practices about running a public notebook server in general, most of which are encoded in this image.


## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. 

The commands `jupyter`, `ipython`, `python`, `pip`, and `conda` (among others) are available in both environments. For convenience, you can install packages into either environment regardless of what environment is currently active using commands like the following:

```
# install a package into the default (python 3.x) environment
pip install some-package
conda install some-package
```


## Alternative Commands

### start.sh

The `start.sh` script supports the same features as the default `start-notebook.sh` script (e.g., `GRANT_SUDO`), but allows you to specify an arbitrary command to execute. For example, to run the text-based `ipython` console in a container, do the following:

```
docker run -it --rm jupyter/all-spark-notebook start.sh ipython
```

Or, to run JupyterLab instead of the classic notebook, run the following:

```
docker run -it --rm -p 8888:8888 jupyter/all-spark-notebook start.sh jupyter lab
```

This script is particularly useful when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, etc.

### Others

You can bypass the provided scripts and specify your an arbitrary start command. If you do, keep in mind that certain features documented above will not function (e.g., `GRANT_SUDO`).
