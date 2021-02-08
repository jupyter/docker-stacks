# Image Specifics

This page provides details about features specific to one or more images.

## Apache Spark™

### Specific Docker Image Options

* `-p 4040:4040` - The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images open [SparkUI (Spark Monitoring and Instrumentation UI)](http://spark.apache.org/docs/latest/monitoring.html) at default port `4040`, this option map `4040` port inside docker container to `4040` port on host machine . Note every new spark context that is created is put onto an incrementing port (ie. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports. For example: `docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/pyspark-notebook`.

### Build an Image with a Different Version of Spark

You can build a `pyspark-notebook` image (and also the downstream `all-spark-notebook` image) with a different version of Spark by overriding the default value of the following arguments at build time.

* Spark distribution is defined by the combination of the Spark and the Hadoop version and verified by the package checksum, see [Download Apache Spark](https://spark.apache.org/downloads.html) for more information. At this time the build will only work with the set of versions available on the Apache Spark download page, so it will not work with the archived versions.
  * `spark_version`: The Spark version to install (`3.0.0`).
  * `hadoop_version`: The Hadoop version (`3.2`).
  * `spark_checksum`: The package checksum (`BFE4540...`).
* Spark can run with different OpenJDK versions.
  * `openjdk_version`: The version of (JRE headless) the OpenJDK distribution (`11`), see [Ubuntu packages](https://packages.ubuntu.com/search?keywords=openjdk).

For example here is how to build a `pyspark-notebook` image with Spark `2.4.6`, Hadoop `2.7` and OpenJDK `8`.

```bash
# From the root of the project
# Build the image with different arguments
docker build --rm --force-rm \
    -t jupyter/pyspark-notebook:spark-2.4.7 ./pyspark-notebook \
    --build-arg spark_version=2.4.7 \
    --build-arg hadoop_version=2.7 \
    --build-arg spark_checksum=0F5455672045F6110B030CE343C049855B7BA86C0ECB5E39A075FF9D093C7F648DA55DED12E72FFE65D84C32DCD5418A6D764F2D6295A3F894A4286CC80EF478 \
    --build-arg openjdk_version=8

# Check the newly built image
docker run -it --rm jupyter/pyspark-notebook:spark-2.4.7 pyspark --version

# Welcome to
#       ____              __
#      / __/__  ___ _____/ /__
#     _\ \/ _ \/ _ `/ __/  '_/
#    /___/ .__/\_,_/_/ /_/\_\   version 2.4.7
#       /_/
#
# Using Scala version 2.11.12, OpenJDK 64-Bit Server VM, 1.8.0_275
```

### Usage Examples

The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images support the use of [Apache Spark](https://spark.apache.org/) in Python, R, and Scala notebooks. The following sections provide some examples of how to get started using them.

#### Using Spark Local Mode

Spark **local mode** is useful for experimentation on small data when you do not have a Spark cluster available.

##### In Python

In a Python notebook.

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master('local').getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(100 + 1))
rdd.sum()
# 5050
```

##### In R

In a R notebook with [SparkR][sparkr].

```R
library(SparkR)

# Spark session & context
sc <- sparkR.session("local")

# Sum of the first 100 whole numbers
sdf <- createDataFrame(list(1:100))
dapplyCollect(sdf,
              function(x)
              { x <- sum(x)}
             )
# 5050
```

In a R notebook with [sparklyr][sparklyr].

```R
library(sparklyr)

# Spark configuration
conf <- spark_config()
# Set the catalog implementation in-memory
conf$spark.sql.catalogImplementation <- "in-memory"

# Spark session & context
sc <- spark_connect(master = "local", config = conf)

# Sum of the first 100 whole numbers
sdf_len(sc, 100, repartition = 1) %>%
    spark_apply(function(e) sum(e))
# 5050
```

##### In Scala

Spylon kernel instantiates a `SparkContext` for you in variable `sc` after you configure Spark
options in a `%%init_spark` magic cell.

```python
%%init_spark
# Configure Spark to use a local master
launcher.master = "local"
```

```scala
// Sum of the first 100 whole numbers
val rdd = sc.parallelize(0 to 100)
rdd.sum()
// 5050
```

#### Connecting to a Spark Cluster in Standalone Mode

Connection to Spark Cluster on **[Standalone Mode](https://spark.apache.org/docs/latest/spark-standalone.html)** requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster which is being
   deployed, run the same version of Spark.
1. [Deploy Spark in Standalone Mode](http://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network addressable by all of
   your Spark workers. (This is a [Spark networking
   requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
   * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e
   TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.

**Note**: In the following examples we are using the Spark master URL `spark://master:7077` that shall be replaced by the URL of the Spark master.

##### In Python

The **same Python version** need to be used on the notebook (where the driver is located) and on the Spark workers.
The python version used at driver and worker side can be adjusted by setting the environment variables `PYSPARK_PYTHON` and / or `PYSPARK_DRIVER_PYTHON`, see [Spark Configuration][spark-conf] for more information.

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master('spark://master:7077').getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(100 + 1))
rdd.sum()
# 5050
```

##### In R

In a R notebook with [SparkR][sparkr].

```R
library(SparkR)

# Spark session & context
sc <- sparkR.session("spark://master:7077")

# Sum of the first 100 whole numbers
sdf <- createDataFrame(list(1:100))
dapplyCollect(sdf,
              function(x)
              { x <- sum(x)}
             )
# 5050
```

In a R notebook with [sparklyr][sparklyr].

```R
library(sparklyr)

# Spark session & context
# Spark configuration
conf <- spark_config()
# Set the catalog implementation in-memory
conf$spark.sql.catalogImplementation <- "in-memory"
sc <- spark_connect(master = "spark://master:7077", config = conf)

# Sum of the first 100 whole numbers
sdf_len(sc, 100, repartition = 1) %>%
    spark_apply(function(e) sum(e))
# 5050
```

##### In Scala

Spylon kernel instantiates a `SparkContext` for you in variable `sc` after you configure Spark
options in a `%%init_spark` magic cell.

```python
%%init_spark
# Configure Spark to use a local master
launcher.master = "spark://master:7077"
```

```scala
// Sum of the first 100 whole numbers
val rdd = sc.parallelize(0 to 100)
rdd.sum()
// 5050
```

## Tensorflow

The `jupyter/tensorflow-notebook` image supports the use of
[Tensorflow](https://www.tensorflow.org/) in single machine or distributed mode.

### Single Machine Mode

```python
import tensorflow as tf

hello = tf.Variable('Hello World!')

sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init)
sess.run(hello)
```

## SensiML

The `jupyter/sensiml-notebook` image supports the use of
[SensiML](https://www.sensiml.com/) Analytics Toolkit using a SensiML account.

### Single Machine Mode

```python
from sensiml import *

connection = SensiML()

# Here you will be prompted for your username/password

# Now, Open the DashBoard UI:
DashBoard(connection)
```

For further usage examples, see the [SensiML Analytics Studio Notebook documentation](https://sensiml.com/documentation/analytics-studio-notebook/index.html).

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

[sparkr]: https://spark.apache.org/docs/latest/sparkr.html
[sparklyr]: https://spark.rstudio.com/
[spark-conf]: https://spark.apache.org/docs/latest/configuration.html
