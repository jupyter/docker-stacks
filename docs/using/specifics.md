# Image Specifics

This page provides details about features specific to one or more images.

## Apache Spark™

### Specific Docker Image Options

- `-p 4040:4040` - The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images open
  [SparkUI (Spark Monitoring and Instrumentation UI)](https://spark.apache.org/docs/latest/monitoring.html) at default port `4040`,
  this option maps the `4040` port inside the docker container to the `4040` port on the host machine.

  ```{note}
  Every new spark context that is created is put onto an incrementing port (i.e. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports.
  ```

  For example, `docker run --detach -p 8888:8888 -p 4040:4040 -p 4041:4041 quay.io/jupyter/pyspark-notebook`.

#### IPython low-level output capture and forward

Spark images (`pyspark-notebook` and `all-spark-notebook`) have been configured to disable IPython low-level output capture and forward system-wide.
The rationale behind this choice is that Spark logs can be verbose, especially at startup when Ivy is used to load additional jars.
Those logs are still available but only in the container's logs.

If you want to make them appear in the notebook, you can overwrite the configuration in a user-level IPython kernel profile.
To do that, you have to uncomment the following line in your `~/.ipython/profile_default/ipython_kernel_config.py` and restart the kernel.

```python
c.IPKernelApp.capture_fd_output = True
```

If you have no IPython profile, you can initiate a fresh one by running the following command.

```bash
ipython profile create
# [ProfileCreate] Generating default config file: '/home/jovyan/.ipython/profile_default/ipython_config.py'
# [ProfileCreate] Generating default config file: '/home/jovyan/.ipython/profile_default/ipython_kernel_config.py'
```

### Build an Image with a Different Version of Spark

You can build a `pyspark-notebook` image with a different `Spark` version by overriding the default value of the following arguments at build time.
`all-spark-notebook` is inherited from `pyspark-notebook`, so you have to first build `pyspark-notebook` and then `all-spark-notebook` to get the same version in `all-spark-notebook`.

- Spark distribution is defined by the combination of Spark, Hadoop, and Scala versions,
  see [Download Apache Spark](https://spark.apache.org/downloads.html) and the [archive repo](https://archive.apache.org/dist/spark/) for more information.
  - `openjdk_version`: The version of the OpenJDK (JRE headless) distribution (`21` by default).
    - This version needs to match the version supported by the Spark distribution used above.
    - See [Spark Overview](https://spark.apache.org/docs/latest/#downloading) and [Ubuntu packages](https://packages.ubuntu.com/search?keywords=openjdk).
  - `spark_version` (optional): The Spark version to install, for example `4.0.0`.
    If not specified (this is the default), the latest stable Spark version will be installed.
  - `hadoop_version`: The Hadoop version (`3` by default).
  - `scala_version` (optional): The Scala version, for example `2.13` (not specified by default).
    Starting with _Spark >= 3.2_, the distribution file might contain the Scala version.
  - `spark_download_url`: URL to use for Spark downloads.
    You may need to use <https://archive.apache.org/dist/spark/> url if you want to download old Spark versions.

```{note}
Only Spark >= 4.0 can be built this way:
the pandas version is resolved from the `dev/infra/Dockerfile` file of the Spark release,
and the Derby jar replacement expects the version bundled by modern Spark.
Building older versions requires modifying `images/pyspark-notebook/Dockerfile`.
```

For example, here is how to build a `pyspark-notebook` image with Spark `4.0.0` and OpenJDK `17`.

```{warning}
This recipe is not tested and might be broken.
```

```bash
# From the root of the project
# Build the image with different arguments
docker build --rm --force-rm \
    -t my-pyspark-notebook ./images/pyspark-notebook \
    --build-arg openjdk_version=17 \
    --build-arg spark_version=4.0.0 \
    --build-arg spark_download_url="https://archive.apache.org/dist/spark/"

# Check the newly built image
docker run -it --rm my-pyspark-notebook pyspark --version

# WARNING: Using incubator modules: jdk.incubator.vector
# Welcome to
#       ____              __
#      / __/__  ___ _____/ /__
#     _\ \/ _ \/ _ `/ __/  '_/
#    /___/ .__/\_,_/_/ /_/\_\   version 4.0.0
#       /_/

# Using Scala version 2.13.16, OpenJDK 64-Bit Server VM, 17.0.19
# Branch HEAD
# Compiled by user wenchen on 2025-05-19T07:58:03Z
# Revision fa33ea000a0bda9e5a3fa1af98e8e85b8cc5e4d4
# Url https://github.com/apache/spark
# Type --help for more information.
```

### Usage Examples

The `jupyter/pyspark-notebook` and `jupyter/all-spark-notebook` images support the use of [Apache Spark](https://spark.apache.org/) in Python and R notebooks.
The following sections provide some examples of how to get started using them.

#### Using Spark Local Mode

Spark **local mode** is useful for experimentation on small data when you do not have a Spark cluster available.

```{warning}
In these examples, Spark spawns all the main execution components in the same single JVM.
You can read additional info about local mode [here](https://books.japila.pl/apache-spark-internals/local/).
If you want to use all the CPU, one of the simplest ways is to set up a [Spark Standalone Cluster](https://spark.apache.org/docs/latest/spark-standalone.html).
```

##### Local Mode in Python

In a Python notebook.

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master("local").getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(100 + 1))
rdd.sum()
# 5050
```

##### Local Mode in R

```{warning}
SparkR is deprecated from Apache Spark 4.0.0 and will be removed in a future version.
Prefer the [sparklyr][sparklyr] examples below.
```

In an R notebook with [SparkR][sparkr].

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

In an R notebook with [sparklyr][sparklyr].

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

#### Connecting to a Spark Cluster in Standalone Mode

Connection to Spark Cluster on **[Standalone Mode](https://spark.apache.org/docs/latest/spark-standalone.html)** requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster, which is being
   deployed, run the same version of Spark.
1. [Deploy Spark in Standalone Mode](https://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network-addressable by all of
   your Spark workers.
   (This is a [Spark networking requirement](https://spark.apache.org/docs/latest/cluster-overview.html#components).)

   ```{note}
   When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See <https://github.com/jupyter/docker-stacks/issues/64> for details.
   ```

**Note**: In the following examples, we are using the Spark master URL `spark://master:7077` which shall be replaced by the URL of the Spark master.

##### Standalone Mode in Python

The **same Python version** needs to be used on the notebook (where the driver is located) and on the Spark workers.
The Python version used on the driver and worker side can be adjusted by setting the environment variables `PYSPARK_PYTHON` and/or `PYSPARK_DRIVER_PYTHON`,
see [Spark Configuration][spark-conf] for more information.

```python
from pyspark.sql import SparkSession

# Spark session & context
spark = SparkSession.builder.master("spark://master:7077").getOrCreate()
sc = spark.sparkContext

# Sum of the first 100 whole numbers
rdd = sc.parallelize(range(100 + 1))
rdd.sum()
# 5050
```

##### Standalone Mode in R

In an R notebook with [SparkR][sparkr].

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

In an R notebook with [sparklyr][sparklyr].

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

### Define Spark Dependencies

```{note}
This example is given for [Elasticsearch](https://www.elastic.co/docs/reference/elasticsearch-hadoop/installation).
```

Spark dependencies can be declared thanks to the `spark.jars.packages` property
(see [Spark Configuration](https://spark.apache.org/docs/latest/configuration.html#runtime-environment) for more information).

They can be defined as a comma-separated list of Maven coordinates at the creation of the Spark session.

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("elasticsearch")
    .config(
        "spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:7.13.0"
    )
    .getOrCreate()
)
```

Dependencies can also be defined in the `spark-defaults.conf`.
However, it has to be done by `root`, so it should only be considered to build custom images.

```dockerfile
USER root
RUN echo "spark.jars.packages org.elasticsearch:elasticsearch-spark-30_2.12:7.13.0" >> "${SPARK_HOME}/conf/spark-defaults.conf"
USER ${NB_UID}
```

Jars will be downloaded dynamically at the creation of the Spark session and stored by default in `${HOME}/.ivy2/jars` (can be changed by setting `spark.jars.ivy`).

## Tensorflow

The `jupyter/tensorflow-notebook` image supports the use of
[Tensorflow](https://www.tensorflow.org/) in a single machine or distributed mode.

### Single Machine Mode

```python
import tensorflow as tf

print(tf.constant("Hello, TensorFlow"))
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
```

### Distributed Mode

TensorFlow 2 uses [distribution strategies](https://www.tensorflow.org/guide/distributed_training) for distributed computations.
For example, `tf.distribute.MirroredStrategy` performs synchronous training across multiple devices on a single machine
(it also works on a machine without GPUs).

```python
import tensorflow as tf

strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = tf.keras.Sequential([tf.keras.Input(shape=(1,)), tf.keras.layers.Dense(1)])
    model.compile(loss="mse", optimizer="sgd")
```

[sparkr]: https://spark.apache.org/docs/latest/sparkr.html
[sparklyr]: https://spark.posit.co
[spark-conf]: https://spark.apache.org/docs/latest/configuration.html
