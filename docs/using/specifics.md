# Image Specifics

This page provides details about features specific to one or more images.

## Apache Spark

**Specific Docker Image Options**
* `-p 4040:4040` - The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images open [SparkUI (Spark Monitoring and Instrumentation UI)](http://spark.apache.org/docs/latest/monitoring.html) at default port `4040`, this option map `4040` port inside docker container to `4040` port on host machine . Note every new spark context that is created is put onto an incrementing port (ie. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports. For example: `docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/pyspark-notebook` 

**Usage Examples**

The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images support the use of [Apache Spark](https://spark.apache.org/) in Python, R, and Scala notebooks. The following sections provide some examples of how to get started using them.

### Using Spark Local Mode

Spark local mode is useful for experimentation on small data when you do not have a Spark cluster available.

#### In a Python Notebook

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
# do something to prove it works
spark.sql('SELECT "Test" as c1').show()
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

### Connecting to a Spark Cluster in Standalone Mode

Connection to Spark Cluster on Standalone Mode requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster which is being deployed, run the same version of Spark.
1. [Deploy Spark in Standalone Mode](http://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. The language specific instructions are almost same as mentioned above for Mesos, only the master url would now be something like spark://10.10.10.10:7077

## Tensorflow

The `jupyter/tensorflow-notebook` image supports the use of [Tensorflow](https://www.tensorflow.org/) in single machine or distributed mode.

### Single Machine Mode

```python
import tensorflow as tf

hello = tf.Variable('Hello World!')

sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init)
sess.run(hello)
```

### Distributed Mode

```python
import tensorflow as tf

hello = tf.Variable('Hello Distributed World!')

server = tf.train.Server.create_local_server()
sess = tf.Session(server.target)
init = tf.global_variables_initializer()

sess.run(init)
sess.run(hello)
```
