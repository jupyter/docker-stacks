# Image Specifics

This page provides details about features specific to one or more images.

## Apache Spark

**Specific Docker Image Options**

* `-p 4040:4040` - The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images open [SparkUI (Spark Monitoring and Instrumentation UI)](http://spark.apache.org/docs/latest/monitoring.html) at default port `4040`, this option map `4040` port inside docker container to `4040` port on host machine . Note every new spark context that is created is put onto an incrementing port (ie. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports. For example: `docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/pyspark-notebook` 

**Usage Examples**

The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images support the use of [Apache Spark](https://spark.apache.org/) in Python, R, and Scala notebooks. The following sections provide some examples of how to get started using them.

### Using Spark Local Mode

Spark **local mode** is useful for experimentation on small data when you do not have a Spark cluster available.

#### In Python

In a Python notebook.

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master('local').getOrCreate()
sc = spark.sparkContext

# Do something to prove it works
rdd = sc.parallelize(range(100))
rdd.sum()
```

#### In R

In a R notebook with [SparkR][sparkr].

```R
library(SparkR)

# Spark session & context
sc <- sparkR.session("local")

# Do something to prove it works
data(iris)
df <- as.DataFrame(iris)
head(filter(df, df$Petal_Width > 0.2))
```

In a R notebook with [sparklyr][sparklyr]

```R
library(sparklyr)
library(dplyr)

# Spark session & context
sc <- spark_connect(master = "local")

# Do something to prove it works
iris_tbl <- copy_to(sc, iris)
iris_tbl %>% 
    filter(Petal_Width > 0.2) %>%
    head()
```

#### In Scala

##### In a Spylon Kernel

Spylon kernel instantiates a `SparkContext` for you in variable `sc` after you configure Spark
options in a `%%init_spark` magic cell.

```python
%%init_spark
# Configure Spark to use a local master
launcher.master = "local"
```

```scala
// Do something to prove it works
val rdd = sc.parallelize(0 to 100)
rdd.sum()
```

##### In an Apache Toree Kernel

Apache Toree instantiates a local `SparkContext` for you in variable `sc` when the kernel starts.

```scala
// do something to prove it works
val rdd = sc.parallelize(0 to 100)
rdd.sum()
```

### Connecting to a Spark Cluster in Standalone Mode

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

#### In Python

The **same Python version** need to be used on the notebook (where the driver is located) and on the Spark workers.
The python version used at driver and worker side can be adjusted by setting the environment variables `PYSPARK_PYTHON` and / or `PYSPARK_DRIVER_PYTHON`, see [Spark Configuration][spark-conf] for more information.

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master('spark://master:7077').getOrCreate()
sc = spark.sparkContext

# Do something to prove it works
rdd = sc.parallelize(range(100))
rdd.sum()
```

#### In R

In a R notebook with [SparkR][sparkr].

```R
library(SparkR)

# Spark session & context
sc <- sparkR.session("spark://master:7077")

# Do something to prove it works
data(iris)
df <- as.DataFrame(iris)
head(filter(df, df$Petal_Width > 0.2))
```

In a R notebook with [sparklyr][sparklyr]

```R
library(sparklyr)
library(dplyr)

# Spark session & context
sc <- spark_connect(master = "spark://master:7077")

# Do something to prove it works
iris_tbl <- copy_to(sc, iris)
iris_tbl %>% 
    filter(Petal_Width > 0.2) %>%
    head()
```

#### In Scala

##### In a Spylon Kernel

Spylon kernel instantiates a `SparkContext` for you in variable `sc` after you configure Spark
options in a `%%init_spark` magic cell.

```python
%%init_spark
# Configure Spark to use a local master
launcher.master = "spark://master:7077"
```

```scala
// Do something to prove it works
val rdd = sc.parallelize(0 to 100)
rdd.sum()
```

##### In an Apache Toree Scala Notebook

The Apache Toree kernel automatically creates a `SparkContext` when it starts based on configuration information from its command line arguments and environment variables. You can pass information about your cluster via the `SPARK_OPTS` environment variable when you spawn a container.

For instance, to pass information about a standalone Spark master, you could start the container like so:

```bash
docker run -d -p 8888:8888 -e SPARK_OPTS='--master=spark://master:7077' \
       jupyter/all-spark-notebook
```

Note that this is the same information expressed in a notebook in the Python case above. Once the kernel spec has your cluster information, you can test your cluster in an Apache Toree notebook like so:

```scala
// should print the value of --master in the kernel spec
println(sc.master)

// do something to prove it works
val rdd = sc.parallelize(0 to 100)
rdd.sum()
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