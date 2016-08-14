{%- set stack_name='pyspark-notebook' %}
{%- set base_path='../base-notebook' %}
{%- include 'partial/badges.md' %}

# Jupyter Notebook Python, Spark, Mesos Stack

## What it Gives You

* Jupyter Notebook 4.2.x
* Conda Python 3.x and Python 2.7.x environments
* pyspark, pandas, matplotlib, scipy, seaborn, scikit-learn pre-installed
* Spark 1.6.0 for use in local mode or to connect to a cluster of Spark workers
* Mesos client 0.22 binary that can communicate with a Mesos master
{% include 'partial/gives.md' with context %}

{% include 'partial/basic_use.md' with context %}

{% include 'partial/pyspark_local.md' %}

{% include 'partial/pyspark_mesos.md' %}

{% include 'partial/spark_standalone.md' %}

{% include 'partial/notebook_options.md' %}

{% include 'partial/docker_options.md' %}
* `-p 4040:4040` - Opens the port for the [Spark Monitoring and Instrumentation UI](http://spark.apache.org/docs/latest/monitoring.html). Note every new spark context that is created is put onto an incrementing port (ie. 4040, 4041, 4042, etc.), and it might be necessary to open multiple ports. `docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 jupyter/pyspark-notebook`

{% include 'partial/ssl_certificates.md' with context %}

{% include 'partial/conda_py23_env.md' %}

{% include 'partial/alternative_commands.md' with context %}
