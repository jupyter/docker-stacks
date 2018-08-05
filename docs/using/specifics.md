# Image Specifics

This page provides details about features specific to one or more images.

## Apache Spark

The `jupyter/all-spark-notebook` image supports the use of [Apache Spark](https://spark.apache.org/) in Python, R, and Scala notebooks. The following sections provide some examples of how to get started using them.

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

### Connecting to a Spark Cluster in Standalone Mode

Connection to Spark Cluster on Standalone Mode requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster which is being deployed, run the same version of Spark and Hadoop.
1. [Deploy Spark in Standalone Mode](http://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. The language specific instructions are almost same as mentioned above for using Spark in local mode, only now the `master` URL should be be something like `spark://10.10.10.10:7077`.

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