{%- set stack_name='all-spark-notebook' %}
{%- set base_path='../base-notebook' %}
{%- include 'partial/badges.md' %}

# Jupyter Notebook Python, Scala, R, Spark, Mesos Stack

## What it Gives You

* Jupyter Notebook 4.2.x
* Conda Python 3.x and Python 2.7.x environments
* Conda R 3.3.x environment
* Scala 2.10.x
* pyspark, pandas, matplotlib, scipy, seaborn, scikit-learn pre-installed for Python
* ggplot2, rcurl preinstalled for R
* Spark 1.6.0 for use in local mode or to connect to a cluster of Spark workers
* Mesos client 0.22 binary that can communicate with a Mesos master
{% include 'partial/gives.md' with context %}

{% include 'partial/basic_use.md' with context %}

{% include 'partial/pyspark_local.md' %}

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

{% include 'partial/pyspark_mesos.md' %}

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

{% include 'partial/spark_standalone.md' %}

{% include 'partial/notebook_options.md' %}

{% include 'partial/docker_options.md' %}
* `-p 4040:4040` - Opens the port for the [Spark Monitoring and Instrumentation UI](http://spark.apache.org/docs/latest/monitoring.html). Note every new spark context that is created is put onto an incrementing port (ie. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports. `docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/all-spark-notebook`

{% include 'partial/ssl_certificates.md' with context %}

{% include 'partial/conda_py23_env.md' %}

{% include 'partial/alternative_commands.md' with context %}
