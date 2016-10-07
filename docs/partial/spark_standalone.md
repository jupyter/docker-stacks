## Connecting to a Spark Cluster in Standalone Mode

Connection to Spark Cluster in Standalone Mode requires the following set of steps:

0. Verify that the docker image (check the Dockerfile) and the Spark Cluster run the same version of Spark.
1. [Deploy Spark in Standalone Mode](http://spark.apache.org/docs/latest/spark-standalone.html).
2. Run the Docker container with `--net=host` in a location that is network addressable by all of your Spark workers. (This is a [Spark networking requirement](http://spark.apache.org/docs/latest/cluster-overview.html#components).)
    * NOTE: When using `--net=host`, you must also use the flags `--pid=host -e TINI_SUBREAPER=true`. See https://github.com/jupyter/docker-stacks/issues/64 for details.
3. The language specific instructions are almost same as mentioned above for Mesos, only the master url would now be something like spark://10.10.10.10:7077
