## Connecting to a Spark Cluster on Mesos

This configuration allows your compute cluster to scale with your data.

0. [Deploy Spark on Mesos](http://spark.apache.org/docs/latest/running-on-mesos.html).
1. Configure each slave with [the `--no-switch_user` flag](https://open.mesosphere.com/reference/mesos-slave/) or create the `jovyan` user on every slave node.
2. Ensure any libraries you wish to use in your Spark lambda functions are installed on your Spark workers.
3. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.

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
conf.set("spark.executor.uri", "hdfs://10.122.193.209/spark/spark-1.6.0-bin-hadoop2.6.tgz")
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
