![docker pulls](https://img.shields.io/docker/pulls/jupyter/all-spark-notebook.svg) ![docker stars](https://img.shields.io/docker/stars/jupyter/all-spark-notebook.svg)

# Jupyter Notebook Python, Scala, R, Spark, Mesos Stack

## What it Gives You

* Jupyter Notebook 4.2.x
* Conda Python 3.x and Python 2.7.x environments
* Conda R 3.2.x environment
* Scala 2.10.x
* pyspark, pandas, matplotlib, scipy, seaborn, scikit-learn pre-installed for Python
* ggplot2, rcurl preinstalled for R
* Spark 1.6.0 for use in local mode or to connect to a cluster of Spark workers
* Mesos client 0.22 binary that can communicate with a Mesos master
* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan` and `/opt/conda`
* [tini](https://github.com/krallin/tini) as the container entrypoint and [start-notebook.sh](../minimal-notebook/start-notebook.sh) as the default command
* A [start-singleuser.sh](../minimal-notebook/start-singleuser.sh) script for use as an alternate command that runs a single-user instance of the Notebook server, as required by [JupyterHub](#JupyterHub)
* Options for HTTPS, password auth, and passwordless `sudo`


## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

```
docker run -d -p 8888:8888 jupyter/all-spark-notebook
```

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
2. Initialize `sparkR` for local mode.
3. Initialize `sparkRSQL`.

For example, the first few cells in a R notebook might read:

```
library(SparkR)

sc <- sparkR.init("local[*]")
sqlContext <- sparkRSQL.init(sc)

# do something to prove it works
data(iris)
df <- createDataFrame(sqlContext, iris)
head(filter(df, df$Petal_Width > 0.2))
```

### In an Apache Toree (Scala) Notebook

0. Run the container as shown above.
1. Open an Apache Toree (Scala) notebook.
2. Use the pre-configured `SparkContext` in variable `sc`.

For example:

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
# nodes (e.g., file:///opt/spark/spark-1.6.0-bin-hadoop2.6.tgz)
conf.set("spark.executor.uri", "hdfs://10.10.10.10/spark/spark-1.6.0-bin-hadoop2.6.tgz")
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
# nodes (e.g., file:///opt/spark/spark-1.6.0-bin-hadoop2.6.tgz) in sparkEnvir
# set other options in sparkEnvir
sc <- sparkR.init("mesos://10.10.10.10:5050", sparkEnvir=list(
    spark.executor.uri="hdfs://10.10.10.10/spark/spark-1.6.0-bin-hadoop2.6.tgz",
    spark.executor.memory="8g"
    )
)
sqlContext <- sparkRSQL.init(sc)

# do something to prove it works
data(iris)
df <- createDataFrame(sqlContext, iris)
head(filter(df, df$Petal_Width > 0.2))
```

### In an Apache Toree (Scala) Notebook

0. Open a terminal via *New -> Terminal* in the notebook interface.
1. Add information about your cluster to the `SPARK_OPTS` environment variable when running the container.
2. Open an Apache Toree (Scala) notebook.
3. Use the pre-configured `SparkContext` in variable `sc`.

The Apache Toree kernel automatically creates a `SparkContext` when it starts based on configuration information from its command line arguments and environment variables. You can pass information about your Mesos cluster via the `SPARK_OPTS` environment variable when you spawn a container.

For instance, to pass information about a Mesos master, Spark binary location in HDFS, and an executor options, you could start the container like so:

`docker run -d -p 8888:8888 -e SPARK_OPTS '--master=mesos://10.10.10.10:5050 \
    --spark.executor.uri=hdfs://10.10.10.10/spark/spark-1.6.0-bin-hadoop2.6.tgz \
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

You can pass [Jupyter command line options](http://jupyter.readthedocs.io/en/latest/projects/config.html#command-line-options-for-configuration) through the [`start-notebook.sh` command](https://github.com/jupyter/docker-stacks/blob/master/minimal-notebook/start-notebook.sh#L15) when launching the container. For example, to set the base URL of the notebook server you might do the following:

```
docker run -d -p 8888:8888 jupyter/all-spark-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

You can sidestep the `start-notebook.sh` script entirely by specifying a command other than `start-notebook.sh`. If you do, the `NB_UID` and `GRANT_SUDO` features documented below will not work. See the Docker Options section for details.

## Docker Options

You may customize the execution of the Docker container and the Notebook server it contains with the following optional arguments.

* `-e PASSWORD="YOURPASS"` - Configures Jupyter Notebook to require the given password. Should be conbined with `USE_HTTPS` on untrusted networks.
* `-e USE_HTTPS=yes` - Configures Jupyter Notebook to accept encrypted HTTPS connections. If a `pem` file containing a SSL certificate and key is not provided (see below), the container will generate a self-signed certificate for you.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the user id.)
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adding `jovyan` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Host mounts the default working directory on the host to preserve work even when the container is destroyed and recreated (e.g., during an upgrade).
* `-v /some/host/folder/for/server.pem:/home/jovyan/.local/share/jupyter/notebook.pem` - Mounts a SSL certificate plus key for `USE_HTTPS`. Useful if you have a real certificate for the domain under which you are running the Notebook server.
* `-p 4040:4040` - Opens the port for the [Spark Monitoring and Instrumentation UI](http://spark.apache.org/docs/latest/monitoring.html). Note every new spark context that is created is put onto an incrementing port (ie. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports. `docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/all-spark-notebook`

## SSL Certificates

The notebook server configuration in this Docker image expects the `notebook.pem` file mentioned above to contain a base64 encoded SSL key and at least one base64 encoded SSL certificate. The file may contain additional certificates (e.g., intermediate and root certificates). 

If you have your key and certificate(s) as separate files, you must concatenate them together into the single expected PEM file. Alternatively, you can build your own configuration and Docker image in which you pass the key and certificate separately.

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](http://jupyter-notebook.readthedocs.io/en/latest/public_server.html#using-ssl-for-encrypted-communication) for best practices about running a public notebook server in general, most of which are encoded in this image.

## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. A second Python 2.x Conda environment exists in `/opt/conda/envs/python2`. You can [switch to the python2 environment](http://conda.pydata.org/docs/using/envs.html#change-environments-activate-deactivate) in a shell by entering the following:

```
source activate python2
```

You can return to the default environment with this command:

```
source deactivate
```

The commands `jupyter`, `ipython`, `python`, `pip`, `easy_install`, and `conda` (among others) are available in both environments. For convenience, you can install packages into either environment regardless of what environment is currently active using commands like the following:

```
# install a package into the python2 environment
pip2 install some-package
conda install -n python2 some-package

# install a package into the default (python 3.x) environment
pip3 install some-package
conda install -n python3 some-package
```

## JupyterHub

[JupyterHub](https://jupyterhub.readthedocs.org) requires a single-user instance of the Jupyter Notebook server per user.   To use this stack with JupyterHub and [DockerSpawner](https://github.com/jupyter/dockerspawner), you must specify the container image name and override the default container run command in your `jupyterhub_config.py`:

```python
# Spawn user containers from this image
c.DockerSpawner.container_image = 'jupyter/all-spark-notebook'

# Have the Spawner override the Docker run command
c.DockerSpawner.extra_create_kwargs.update({
	'command': '/usr/local/bin/start-singleuser.sh'
})
```
