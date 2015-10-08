# Jupyter Notebook Python, Spark, Mesos Stack

## What it Gives You

* Jupyter Notebook server (v4.0.x or v3.2.x, see tag)
* Conda Python 3.4.x and Python 2.7.x environments
* pyspark, pandas, matplotlib, scipy, seaborn, scikit-learn pre-installed
* Spark 1.4.1 for use in local mode or to connect to a cluster of Spark workers
* Mesos client 0.22 binary that can communicate with a Mesos master
* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan` and `/opt/conda`
* **(v4.0.x)** [tini](https://github.com/krallin/tini) as the container entrypoint and [start-notebook.sh](../minimal-notebook/start-notebook.sh) as the default command
* Options for HTTPS, password auth, and passwordless `sudo`

## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

```
docker run -d -p 8888:8888 jupyter/pyspark-notebook
```

## Using Spark Local Mode

This configuration is nice for using Spark on small, local data.

0. Run the container as shown above.
2. Open a Python 2 or 3 notebook.
3. Create a `SparkContext` configured for local mode.

For example, the first few cells in a Python 3 notebook might read:

```python
import pyspark
sc = pyspark.SparkContext('local[*]')

# do something to prove it works
rdd = sc.parallelize(range(1000))
rdd.takeSample(False, 5)
```

In a Python 2 notebook, prefix the above with the following code to ensure the local workers use Python 2 as well.

```python
import os
os.environ['PYSPARK_PYTHON'] = 'python2'

# include pyspark cells from above here ...
```

## Connecting to a Spark Cluster on Mesos

This configuration allows your compute cluster to scale with your data.

0. [Deploy Spark on Mesos](http://spark.apache.org/docs/latest/running-on-mesos.html).
1. Configure each slave with [the `--no-switch_user` flag](https://open.mesosphere.com/reference/mesos-slave/) or create the `jovyan` user on every slave node.
2. Ensure Python 2.x and/or 3.x and any Python libraries you wish to use in your Spark lambda functions are installed on your Spark workers.
3. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
4. Open a Python 2 or 3 notebook.
5. Create a `SparkConf` instance in a new notebook pointing to your Mesos master node (or Zookeeper instance) and Spark binary package location.
6. Create a `SparkContext` using this configuration. 

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
# nodes (e.g., file:///opt/spark/spark-1.4.1-bin-hadoop2.6.tgz) 
conf.set("spark.executor.uri", "hdfs://10.122.193.209/spark/spark-1.4.1-bin-hadoop2.6.tgz")
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

## Docker Options

You may customize the execution of the Docker container and the Notebook server it contains with the following optional arguments.

* `-e PASSWORD="YOURPASS"` - Configures Jupyter Notebook to require the given password. Should be conbined with `USE_HTTPS` on untrusted networks.
* `-e USE_HTTPS=yes` - Configures Jupyter Notebook to accept encrypted HTTPS connections. If a `pem` file containing a SSL certificate and key is not found in `/home/jovyan/.ipython/profile_default/security/notebook.pem`, the container will generate a self-signed certificate for you.
* **(v4.0.x)** `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership.
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Host mounts the default working directory on the host to preserve work even when the container is destroyed and recreated (e.g., during an upgrade).
* **(v3.2.x)** `-v /some/host/folder/for/server.pem:/home/jovyan/.ipython/profile_default/security/notebook.pem` - Mounts a SSL certificate plus key for `USE_HTTPS`. Useful if you have a real certificate for the domain under which you are running the Notebook server.
* **(v4.0.x)** `-v /some/host/folder/for/server.pem:/home/jovyan/.local/share/jupyter/notebook.pem` - Mounts a SSL certificate plus key for `USE_HTTPS`. Useful if you have a real certificate for the domain under which you are running the Notebook server.
* `-e INTERFACE=10.10.10.10` - Configures Jupyter Notebook to listen on the given interface. Defaults to '*', all interfaces, which is appropriate when running using default bridged Docker networking. When using Docker's `--net=host`, you may wish to use this option to specify a particular network interface.
* `-e PORT=8888` - Configures Jupyter Notebook to listen on the given port. Defaults to 8888, which is the port exposed within the Dockerfile for the image. When using Docker's `--net=host`, you may wish to use this option to specify a particular port.

## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. A second Python 2.x Conda environment exists in `/opt/conda/envs/python2`. You can [switch to the python2 environment](http://conda.pydata.org/docs/using/envs.html#change-environments-activate-deactivate) in a shell by entering the following:

```
source activate python2
```

You can return to the default environment with this command:

```
source deactivate
```

The commands `ipython`, `python`, `pip`, `easy_install`, and `conda` (among others) are available in both environments.
